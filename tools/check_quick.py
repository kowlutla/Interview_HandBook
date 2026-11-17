"""Checker for quick-notes pages.
Usage (from HLD/quicknotes): python -I tools/check_quick.py notes/q04-caching.html cases/c01-url-shortener.html
Checks: balanced tags, forbidden patterns, handbook links resolve to real files, word/diagram/Q&A minimums."""
import re, sys, os
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site', 'quicknotes')
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'rect', 'circle', 'polygon', 'polyline', 'ellipse', 'stop'}
FORBIDDEN = ['inner' + 'HTML', 'insertAdjacent' + 'HTML', 'outer' + 'HTML', 'document.' + 'write', 'ev' + 'al(', '<script']

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st = []; s.bad = []; s.ids = set(); s.hrefs = []; s.svg = 0; s.details = 0; s.h2 = 0
    def handle_starttag(s, t, a):
        d = dict(a)
        if 'id' in d: s.ids.add(d['id'])
        if t == 'a' and 'href' in d: s.hrefs.append(d['href'])
        if t == 'svg' and 'viewbox' in d: s.svg += 1
        if t == 'details': s.details += 1
        if t == 'h2': s.h2 += 1
        if t not in VOID: s.st.append((t, s.getpos()[0]))
    def handle_startendtag(s, t, a): pass
    def handle_endtag(s, t):
        if t in VOID: return
        if s.st and s.st[-1][0] == t: s.st.pop()
        else: s.bad.append((t, s.getpos()[0]))

def check(path):
    full = os.path.join(ROOT, path)
    src = open(full, encoding='utf-8').read()
    src = re.sub(r'<!--qnav:start-->.*?<!--qnav:end-->|<!--qfoot:start-->.*?<!--qfoot:end-->', '', src, flags=re.S)  # generated sidebar is not page content
    p = P(); p.feed(src)
    errs = []
    if p.bad: errs.append('unbalanced end tags (first 3): %s' % p.bad[:3])
    if p.st: errs.append('unclosed tags (first 3): %s' % p.st[:3])
    for h in p.hrefs:
        if h.startswith('#'):
            if h[1:] not in p.ids: errs.append('broken anchor ' + h)
        elif re.match(r'https?:', h): errs.append('external link ' + h)
        else:
            target = os.path.normpath(os.path.join(os.path.dirname(full), h.split('#')[0]))
            if not os.path.exists(target): errs.append('link target missing (maybe not written yet): ' + h)
    chk = re.sub(r'<script src="(\.\./)+(assets/quick|theme)\.js"></script>', '', src)
    for bad in FORBIDDEN:
        if bad in chk: errs.append('forbidden: ' + bad)
    for need in ('../assets/style.css', '../assets/quick.css', 'class="qn"'):
        if need not in src: errs.append('missing skeleton piece: ' + need)
    words = len(re.sub(r'<[^>]+>', ' ', src).split())
    is_case = '/cases/' in full.replace('\\', '/')
    mw, ms, md = (1800, 2, 6) if is_case else (4500, 4, 20)
    if words < mw: errs.append('too short: %d words (minimum %d)' % (words, mw))
    if p.svg < ms: errs.append('only %d SVG diagrams (want at least %d)' % (p.svg, ms))
    if p.details < md: errs.append('only %d Q&A details blocks (want at least %d)' % (p.details, md))
    print('%s: %d words, %d h2, %d svg, %d qa -> %s' % (path, words, p.h2, p.svg, p.details, 'OK' if not errs else 'PROBLEMS'))
    for e in errs: print('   -', e)
    return not errs

if __name__ == '__main__':
    ok = all([check(f) for f in sys.argv[1:]])
    sys.exit(0 if ok else 1)
