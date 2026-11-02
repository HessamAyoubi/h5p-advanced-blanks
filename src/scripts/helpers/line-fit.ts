/**
 * Keeps a growing text field inside the free space of its own line.
 *
 * The field's width follows its size attribute: the longest correct answer,
 * and from 1.1.2 the text typed so far. Left alone it grows until it fills a
 * whole row and pushes the words that shared its line ("... wird geholfen.")
 * onto the next one. This caps it, as an inline max-width, at its current
 * width plus the space still free at the end of its line: it grows until the
 * line is full, then the text scrolls inside it like in any input.
 *
 * Disabled fields (correct answer, shown solution) are left uncapped: nobody
 * types there, and a solution should be readable in full.
 */
export function fitToLine(input: HTMLInputElement): void {
  if (input.disabled) {
    input.style.removeProperty('max-width');
    return;
  }
  const blank = (input.closest('.blank') || input) as HTMLElement;
  const block = blockAncestor(blank);
  if (!block) {
    return;
  }

  const field = input.getBoundingClientRect();
  if (field.width === 0) {
    return; // Not rendered (hidden tab, collapsed container): measure later.
  }
  const style = getComputedStyle(block);
  const box = block.getBoundingClientRect();
  const lineEnd = box.right - parseFloat(style.paddingRight) - parseFloat(style.borderRightWidth);
  const lineWidth = lineEnd - (box.left + parseFloat(style.paddingLeft) + parseFloat(style.borderLeftWidth));

  // Rightmost thing on the field's line: the blank itself (its hint button
  // included) or whatever follows it on the same line.
  let used = blank.getBoundingClientRect().right;
  const after = document.createRange();
  after.setStartAfter(blank);
  after.setEnd(block, block.childNodes.length);
  const rects = after.getClientRects();
  for (let i = 0; i < rects.length; i++) {
    const r = rects[i];
    if (r.width > 0 && r.top < field.bottom - 1 && r.bottom > field.top + 1) {
      used = Math.max(used, r.right);
    }
  }

  const cap = Math.min(lineWidth, field.width + Math.max(0, lineEnd - used - 1));
  // !important: the site CSS caps these fields with max-width ... !important,
  // and only an inline !important outranks that.
  input.style.setProperty('max-width', Math.floor(cap) + 'px', 'important');
}

function blockAncestor(el: HTMLElement): HTMLElement | null {
  let node = el.parentElement;
  while (node) {
    const display = getComputedStyle(node).display;
    if (display !== 'inline' && display !== 'inline-block' && display !== 'contents') {
      return node;
    }
    node = node.parentElement;
  }
  return null;
}
