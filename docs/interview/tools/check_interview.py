"""Checker for Interview Book topic pages.
Usage (from HLD/interview): python -I tools/check_interview.py topics/git.html
Checks: balanced tags, forbidden patterns, links resolve, skeleton, question markup, minimum size."""
import re, sys, os
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'rect', 'circle', 'polygon', 'polyline', 'ellipse', 'stop'}
FORBIDDEN = ['inner' + 'HTML', 'insertAdjacent' + 'HTML', 'outer' + 'HTML', 'document.' + 'write', 'ev' + 'al(', '<script']
LEVELS = ('lvl b', 'lvl i', 'lvl s')


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st = []; s.bad = []; s.ids = set(); s.hrefs = []; s.svg = 0; s.iq = 0; s.h2 = 0; s.lvl = 0; s.scn = 0; s.fig = 0
    def handle_starttag(s, t, a):
        d = dict(a)
        if 'id' in d:
            if d['id'] in s.ids: s.bad.append(('duplicate id ' + d['id'], s.getpos()[0]))
            s.ids.add(d['id'])
        if t == 'a' and 'href' in d: s.hrefs.append(d['href'])
        if t == 'svg' and 'viewbox' in d: s.svg += 1
        if t == 'figure': s.fig += 1
        if t == 'details' and (d.get('class') or '').split()[:1] == ['iq']: s.iq += 1
        if t == 'span' and (d.get('class') or '') in LEVELS: s.lvl += 1
        if t == 'details' and 'scn' in (d.get('class') or '').split(): s.scn += 1
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
    src = re.sub(r'<!--qnav:start-->.*?<!--qnav:end-->|<!--qfoot:start-->.*?<!--qfoot:end-->', '', src, flags=re.S)
    p = P(); p.feed(src)
    errs = []
    if p.bad: errs.append('unbalanced end tags / duplicate ids (first 3): %s' % p.bad[:3])
    if p.st: errs.append('unclosed tags (first 3): %s' % p.st[:3])
    for h in p.hrefs:
        if h.startswith('#'):
            if h[1:] not in p.ids: errs.append('broken anchor ' + h)
        elif re.match(r'https?:', h): errs.append('external link ' + h)
        else:
            target = os.path.normpath(os.path.join(os.path.dirname(full), h.split('#')[0]))
            if not os.path.exists(target): errs.append('link target missing: ' + h)
    chk = re.sub(r'<script src="(\.\./)+(quicknotes/assets/quick|theme)\.js"></script>', '', src)
    for bad in FORBIDDEN:
        if bad in chk: errs.append('forbidden: ' + bad)
    for need in ('../../handbook/assets/style.css', '../../quicknotes/assets/quick.css', '../assets/interview.css', 'class="qn"'):
        if need not in src: errs.append('missing skeleton piece: ' + need)
    words = len(re.sub(r'<[^>]+>', ' ', src).split())
    if words < 6000: errs.append('too short: %d words (minimum 6000)' % words)
    if p.svg < 6: errs.append('only %d SVG diagrams (want at least 6)' % p.svg)
    if p.iq < 40: errs.append('only %d questions <details class="iq"> (want at least 40)' % p.iq)
    if p.lvl < p.iq: errs.append('%d questions but %d difficulty badges (every question needs one)' % (p.iq, p.lvl))
    if p.scn < 6: errs.append('only %d scenario questions (details class="iq scn"; want at least 6)' % p.scn)
    print('%s: %d words, %d h2, %d svg, %d questions (%d scenario) -> %s' % (path, words, p.h2, p.svg, p.iq, p.scn, 'OK' if not errs else 'PROBLEMS'))
    for e in errs: print('   -', e)
    return not errs


if __name__ == '__main__':
    ok = all([check(f) for f in sys.argv[1:]])
    sys.exit(0 if ok else 1)
