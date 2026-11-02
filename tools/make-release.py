"""Build the next releases/ package from the previous one.

    python -I tools/make-release.py releases/H5P.AdvancedBlanks-1.1.1.h5p

Takes the previous release (which carries H5P.Question 1.4 and the sample
content, see README) and swaps in this checkout's library files: every file
under H5P.AdvancedBlanks-1.1/ that exists here is replaced by the local copy,
so run `npm run build:prod` first. Writes releases/H5P.AdvancedBlanks-<version>.h5p
named after library.json, and prints what changed.

Why not pack from scratch: the package also has to carry H5P.Question 1.4,
which is not in this repository; the previous release is its source.
"""
import hashlib
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = 'H5P.AdvancedBlanks-1.1/'

prev = zipfile.ZipFile(sys.argv[1])
lib = json.load(open(os.path.join(ROOT, 'library.json'), encoding='utf-8'))
version = '%d.%d.%d' % (lib['majorVersion'], lib['minorVersion'], lib['patchVersion'])
out = os.path.join(ROOT, 'releases', 'H5P.AdvancedBlanks-%s.h5p' % version)
if os.path.exists(out):
    raise SystemExit('exists already: ' + out)

buf = io.BytesIO()
changed = []
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    for info in prev.infolist():
        name = info.filename
        if name.endswith('/'):
            continue
        data = prev.read(name)
        if name.startswith(LIB):
            local = os.path.join(ROOT, *name[len(LIB):].split('/'))
            if os.path.isfile(local):
                new = open(local, 'rb').read()
                if new != data:
                    changed.append('%s (%d -> %d bytes)' % (name, len(data), len(new)))
                    data = new
        z.writestr(name, data)
open(out, 'wb').write(buf.getvalue())

print('wrote', out)
print('sha256', hashlib.sha256(buf.getvalue()).hexdigest())
print('changed:' if changed else 'NOTHING CHANGED', *changed, sep='\n  ')
