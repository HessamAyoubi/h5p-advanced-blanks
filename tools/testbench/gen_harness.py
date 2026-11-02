"""Local test bench for H5P.AdvancedBlanks 1.1.2 + the site CSS.

Writes harness/ with:
  site-old.css  the academy's live H5P Custom CSS, fetched as-is
  site-new.css  the same with the input-width edits (EDITS below, the exact
                anchors the installer applies on the server)
  frame.html    one H5P page like the site's iframe: H5P core + the library's
                dependencies from the academy, the LOCAL 1.1.2 build, and test
                content shaped like lesson "Position vom Verb"
  index.html    frame.html in iframes at desktop, tablet and phone widths
  ractive.min.js, dist.js  copied from the repo's dist/
"""
import json
import os
import shutil
import sys
import urllib.request

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/130.0 Safari/537.36')
SITE = 'https://academy.lingonex.de'
LIBS = SITE + '/wp-content/uploads/h5p/libraries/'
CORE = SITE + '/wp-content/plugins/h5p/h5p-php-library/'
REPO = r'C:\Files\IT Stuff\GitHub\h5p-advanced-blanks'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'harness')

EDITS = json.load(open(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'css-edits.json'), encoding='utf-8'))


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def apply_edits(css):
    crlf = '\r\n' in css
    out = css
    for key, (old, new) in EDITS.items():
        if crlf:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        n = css.count(old)
        if n != 1:
            raise SystemExit('anchor %s found %d times' % (key, n))
        out = out.replace(old, new)
    return out


os.makedirs(OUT, exist_ok=True)
old_css = get(SITE + '/wp-content/uploads/h5p-custom-style.css').decode('utf-8')
open(os.path.join(OUT, 'site-old.css'), 'w', encoding='utf-8', newline='').write(old_css)
open(os.path.join(OUT, 'site-new.css'), 'w', encoding='utf-8', newline='').write(apply_edits(old_css))
for f in ('ractive.min.js', 'dist.js'):
    shutil.copyfile(os.path.join(REPO, 'dist', f), os.path.join(OUT, f))

# Dependencies first (topological), from the academy's library.json files.
lib = json.load(open(os.path.join(REPO, 'library.json'), encoding='utf-8'))
order, seen = [], set()


def visit(name):
    if name in seen:
        return
    seen.add(name)
    j = json.loads(get(LIBS + name + '/library.json'))
    for d in j.get('preloadedDependencies', []):
        visit('%s-%d.%d' % (d['machineName'], d['majorVersion'], d['minorVersion']))
    order.append((name, j))


for d in lib['preloadedDependencies']:
    visit('%s-%d.%d' % (d['machineName'], d['majorVersion'], d['minorVersion']))

css_tags = ['<link rel="stylesheet" href="%sstyles/%s">' % (CORE, s) for s in (
    'h5p-fonts.css', 'h5p.css', 'h5p-confirmation-dialog.css', 'h5p-core-button.css',
    'h5p-theme.css', 'h5p-theme-variables.css', 'h5p-tooltip.css', 'h5p-table.css')]
js_tags = ['<script src="%sjs/%s"></script>' % (CORE, s) for s in (
    'jquery.js', 'h5p.js', 'h5p-event-dispatcher.js', 'h5p-x-api-event.js', 'h5p-x-api.js',
    'h5p-content-type.js', 'h5p-confirmation-dialog.js', 'h5p-action-bar.js',
    'request-queue.js', 'h5p-tooltip.js')]
for name, j in order:
    css_tags += ['<link rel="stylesheet" href="%s%s/%s">' % (LIBS, name, x['path']) for x in j.get('preloadedCss', [])]
    js_tags += ['<script src="%s%s/%s"></script>' % (LIBS, name, x['path']) for x in j.get('preloadedJs', [])]
js_tags += ['<script src="ractive.min.js"></script>', '<script src="dist.js"></script>']

params = json.load(open(os.path.join(HERE, 'test-content.json'), encoding='utf-8'))
integration = {
    'baseUrl': SITE, 'url': SITE + '/wp-content/uploads/h5p', 'postUserStatistics': False,
    'saveFreq': False, 'siteUrl': SITE, 'l10n': {'H5P': {}}, 'core': {'scripts': [], 'styles': []},
    'contents': {'cid-1': {
        'library': 'H5P.AdvancedBlanks 1.1', 'jsonContent': json.dumps(params), 'fullScreen': '0',
        'exportUrl': '', 'embedCode': '', 'resizeCode': '', 'mainId': 1, 'url': SITE,
        'title': 'test', 'contentUserData': [], 'metadata': {'title': 'test'},
        'displayOptions': {'frame': False, 'export': False, 'embed': False, 'copyright': False, 'icon': False, 'copy': False},
    }},
}

frame = '''<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AdvancedBlanks test frame</title>
%s
<link rel="stylesheet" id="sitecss" href="site-new.css">
<script>
  if (location.search.indexOf('css=old') !== -1) {
    document.getElementById('sitecss').href = 'site-old.css';
  }
  window.H5PIntegration = %s;
</script>
%s
</head>
<body style="margin:0">
<div class="h5p-content" data-content-id="1"></div>
</body></html>
''' % ('\n'.join(css_tags), json.dumps(integration), '\n'.join(js_tags))
open(os.path.join(OUT, 'frame.html'), 'w', encoding='utf-8').write(frame)

index = '''<!doctype html>
<html><head><meta charset="utf-8"><title>AdvancedBlanks widths</title>
<style>
 body { font: 14px system-ui, sans-serif; margin: 16px; background: #f1f1f1; }
 .row { display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap; }
 figure { margin: 0; } figcaption { margin: 0 0 4px; font-weight: 600; }
 iframe { border: 1px solid #bbb; background: #fff; height: 1500px; }
</style></head><body>
<p>CSS: <b id="m"></b> &middot; <a href="?css=old">old (150px cap)</a> &middot; <a href="?">new</a></p>
<div class="row">
 <figure><figcaption>desktop lesson column 760px</figcaption><iframe id="f760" width="760"></iframe></figure>
 <figure><figcaption>narrow 480px</figcaption><iframe id="f480" width="480"></iframe></figure>
 <figure><figcaption>phone 320px</figcaption><iframe id="f320" width="320"></iframe></figure>
</div>
<script>
 var q = location.search.indexOf('css=old') !== -1 ? '?css=old' : '';
 document.getElementById('m').textContent = q ? 'old' : 'new';
 ['f760', 'f480', 'f320'].forEach(function (id) { document.getElementById(id).src = 'frame.html' + q; });
</script>
</body></html>
'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
print('libraries:', ', '.join(n for n, _ in order))
print('wrote', OUT)
