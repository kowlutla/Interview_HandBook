"""Whole-site link and anchor checker.  Run: python -I tools/check_site.py
Checks every href/src in every .html under the site root: file exists, and #anchor exists in target page.
Skips external (http/https/mailto) links and nav-generated anchors on handbook pages (built by nav.js)."""
import os, re, sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'a' and a.get('name'): self.ids.add(a['name'])
        for k in ('href', 'src'):
            if a.get(k): self.links.append(a[k])


pages = {}
for d, _, fs in os.walk(ROOT):
    if os.sep + '.git' in d or 'archive' in d.split(os.sep): continue
    for f in fs:
        if f.endswith('.html'):
            p = P()
            raw = open(os.path.join(d, f), encoding='utf-8').read()
            p.feed(raw)
            p.raw = raw
            pages[os.path.normpath(os.path.join(d, f))] = p

errs = 0
# stray authoring markers and double-escaped entities (visible garbage in the rendered page)
LEAKS = [(re.compile(r'^@[a-z]+[ 	]*$', re.M), 'stray marker line'),
         (re.compile(r'&amp;(amp|lt|gt|quot|nbsp);'), 'double-escaped entity'),
         (re.compile(r'(TODO|FIXME)'), 'TODO/FIXME left in page')]
for path, p in sorted(pages.items()):
    for rx, what in LEAKS:
        m = rx.search(p.raw)
        if m:
            print('LEAK   ', os.path.relpath(path, ROOT), '->', what, repr(m.group(0)[:30])); errs += 1
for path, p in sorted(pages.items()):
    for l in p.links:
        if re.match(r'(https?:|mailto:|data:|javascript:|/)', l): continue
        target, _, frag = l.partition('#')
        target = target.split('?')[0]
        tp = path if not target else os.path.normpath(os.path.join(os.path.dirname(path), target))
        if os.path.isdir(tp): tp = os.path.join(tp, 'index.html')
        if not os.path.exists(tp):
            print('MISSING', os.path.relpath(path, ROOT), '->', l); errs += 1; continue
        if frag and tp in pages and frag not in pages[tp].ids and frag != 'top':
            print('ANCHOR ', os.path.relpath(path, ROOT), '->', l); errs += 1
print('%d pages checked, %d problems' % (len(pages), errs))
sys.exit(1 if errs else 0)
