"""Focused structural checker for DSA topic pages.
Usage: python -I tools/check_dsa.py site/dsa/topics/strings.html
"""
import os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'rect', 'circle', 'polygon', 'polyline', 'ellipse', 'stop'}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors, self.ids, self.hrefs = [], [], set(), []
        self.problems, self.h2 = 0, 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids: self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if tag == 'details' and 'dsa-problem' in (a.get('class') or '').split(): self.problems += 1
        if tag == 'h2': self.h2 += 1
        if tag not in VOID: self.stack.append(tag)
    def handle_startendtag(self, tag, attrs): pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.stack and self.stack[-1] == tag: self.stack.pop()
        else: self.errors.append('unexpected closing tag: ' + tag)

def check(path):
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    raw = open(full, encoding='utf-8').read()
    p = Page(); p.feed(raw)
    for h in p.hrefs:
        if h.startswith(('http:', 'https:', 'mailto:', '#')): continue
        target = os.path.normpath(os.path.join(os.path.dirname(full), h.split('#')[0]))
        if not os.path.exists(target): p.errors.append('missing link target: ' + h)
    for anchor in re.findall(r'href="#([^"]+)"', raw):
        if anchor not in p.ids: p.errors.append('missing anchor: #' + anchor)
    if p.stack: p.errors.append('unclosed tags: ' + repr(p.stack[-5:]))
    if p.problems < 1: p.errors.append('no DSA problem blocks found')
    if p.h2 < 3: p.errors.append('expected at least three topic sections')
    for required in ('../../handbook/assets/style.css', '../../quicknotes/assets/quick.css', '../assets/dsa.css'):
        if required not in raw: p.errors.append('missing stylesheet: ' + required)
    print('%s: %d problems, %d sections -> %s' % (path, p.problems, p.h2, 'OK' if not p.errors else 'PROBLEMS'))
    for e in p.errors: print(' - ' + e)
    return not p.errors

if __name__ == '__main__':
    if len(sys.argv) < 2: raise SystemExit('Pass one or more DSA HTML paths')
    raise SystemExit(0 if all(check(x) for x in sys.argv[1:]) else 1)
