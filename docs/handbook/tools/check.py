"""Structural checker for handbook pages.
Usage: python -I tools/check.py chapters/NN-slug.html [more files]
Checks: balanced tags, in-page anchors, no unsafe DOM writes, no external src/href,
required skeleton, links to other chapters resolve to ids in assets/chapters.js, size, diagrams, Q&A."""
import re, sys, os
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = open(os.path.join(ROOT, 'assets', 'chapters.js'), encoding='utf-8').read()
IDS = set(re.findall(r'id: "([^"]+)"', manifest))
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'rect', 'circle', 'polygon', 'polyline', 'ellipse', 'stop'}
FORBIDDEN = ['inner' + 'HTML', 'insertAdjacent' + 'HTML', 'outer' + 'HTML', 'document.' + 'write', 'ev' + 'al(']

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st = []; s.bad = []; s.ids = set(); s.hrefs = []; s.h2 = 0; s.svg = 0; s.details = 0
    def handle_starttag(s, t, a):
        d = dict(a)
        if 'id' in d: s.ids.add(d['id'])
        if t == 'a' and 'href' in d: s.hrefs.append(d['href'])
        if t == 'h2': s.h2 += 1
        if t == 'svg' and 'viewbox' in d: s.svg += 1
        if t == 'details': s.details += 1
        if t not in VOID: s.st.append((t, s.getpos()[0]))
    def handle_startendtag(s, t, a): pass
    def handle_endtag(s, t):
        if t in VOID: return
        if s.st and s.st[-1][0] == t: s.st.pop()
        else: s.bad.append((t, s.getpos()[0]))

def check(path):
    src = open(path, encoding='utf-8').read()
    p = P(); p.feed(src)
    errs = []
    if p.bad: errs.append('unbalanced end tags (first 3): %s' % p.bad[:3])
    if p.st: errs.append('unclosed tags (first 3): %s' % p.st[:3])
    for h in p.hrefs:
        if h.startswith('#'):
            if h[1:] not in p.ids and h != '#': errs.append('broken anchor ' + h)
        elif re.match(r'https?:', h): errs.append('external link ' + h)
        else:
            m = re.match(r'(?:\.\./[a-z\-]+/|\./)?([A-Za-z0-9\-]+)\.html', h)
            if m and m.group(1) not in IDS and m.group(1) != 'index': errs.append('link to unknown page ' + h)
    for bad in FORBIDDEN:
        if bad in src: errs.append('forbidden: ' + bad)
    if re.search(r'(src|href)="https?:', src): errs.append('external resource reference')
    for need in ('../assets/style.css', '../assets/chapters.js', '../assets/nav.js', 'id="toc"', 'data-page="'):
        if need not in src: errs.append('missing skeleton piece: ' + need)
    pid = os.path.splitext(os.path.basename(path))[0]
    if 'data-page="%s"' % pid not in src: errs.append('data-page must equal file name %s' % pid)
    if pid not in IDS: errs.append('page id %s not in assets/chapters.js' % pid)
    words = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', ' ', src, flags=re.S)).split())
    kind = 'case' if re.match(r'c\d\d-', pid) else ('cheat' if pid.startswith('cs-') or pid.startswith('ref-') else 'chapter')
    minimum = {'chapter': 5500, 'case': 4000, 'cheat': 800}[kind]
    if pid.startswith('ref-'): minimum = 3000
    if words < minimum: errs.append('too short: %d words (minimum %d for a %s)' % (words, minimum, kind))
    if kind != 'cheat':
        if p.svg < 4: errs.append('only %d inline SVG diagrams (want at least 4)' % p.svg)
        if p.details < 6: errs.append('only %d Q&A details blocks (want at least 6)' % p.details)
    print('%s: %d words, %d h2, %d svg, %d qa -> %s' % (path, words, p.h2, p.svg, p.details, 'OK' if not errs else 'PROBLEMS'))
    for e in errs: print('   -', e)
    return not errs

if __name__ == '__main__':
    ok = all([check(f) for f in sys.argv[1:]])
    sys.exit(0 if ok else 1)
