"""Structural checker for DSA topic indexes and individual problem pages.
Usage: python -I tools/check_dsa.py site/dsa/topics/strings.html site/dsa/topics/strings/isomorphic-strings.html
"""
import os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'rect', 'circle', 'polygon', 'polyline', 'ellipse', 'stop'}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors, self.ids, self.hrefs = [], [], set(), []
        self.problems, self.h2, self.h3 = 0, 0, 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids: self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if tag == 'article' and 'dsa-problem-card' in (a.get('class') or '').split(): self.problems += 1
        if tag == 'h2': self.h2 += 1
        if tag == 'h3': self.h3 += 1
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
    is_problem = os.path.dirname(full).endswith(os.path.join('topics', 'strings'))
    if p.problems < 1: p.errors.append('no DSA problem article found')
    if is_problem and p.h2 < 5: p.errors.append('problem page should contain its problem title and detailed sections')
    if not is_problem and p.h2 < 2: p.errors.append('topic index should contain at least two h2 sections')
    styles = ('../../../handbook/assets/style.css', '../../../quicknotes/assets/quick.css', '../../assets/dsa.css') if is_problem else ('../../handbook/assets/style.css', '../../quicknotes/assets/quick.css', '../assets/dsa.css')
    for required in styles:
        if required not in raw: p.errors.append('missing stylesheet: ' + required)
    if is_problem and 'dsa-breadcrumb' not in raw: p.errors.append('problem page is missing breadcrumbs')
    if not is_problem and 'dsa-problem-summary' not in raw: p.errors.append('topic index must use concise problem summaries')
    print('%s: %d problem article(s), %d h2 headings -> %s' % (path, p.problems, p.h2, 'OK' if not p.errors else 'PROBLEMS'))
    for e in p.errors: print(' - ' + e)
    return not p.errors

def verify_source_coverage():
    source_root = os.path.join(ROOT, 'dsa-source', 'src', 'com', 'dsa')
    if not os.path.isdir(source_root):
        print('DSA source checkout not present; source coverage check skipped')
        return True
    expected = sum(1 for d, _, files in os.walk(source_root) for f in files if f.endswith('.java'))
    topic_root = os.path.join(ROOT, 'site', 'dsa', 'topics')
    topic_pages = [os.path.join(topic_root, f) for f in os.listdir(topic_root)
                   if f.endswith('.html') and os.path.isfile(os.path.join(topic_root, f))]
    actual = 0
    for path in topic_pages:
        raw = open(path, encoding='utf-8').read()
        actual += len(re.findall(r'<article class="dsa-problem-card dsa-problem-summary"', raw))
    ok = len(topic_pages) == 17 and actual == expected
    print('DSA source coverage: %d Java files, %d indexed entries, %d topic pages -> %s' %
          (expected, actual, len(topic_pages), 'OK' if ok else 'INCOMPLETE'))
    return ok


if __name__ == '__main__':
    if len(sys.argv) < 2: raise SystemExit('Pass one or more DSA HTML paths')
    valid = all(check(x) for x in sys.argv[1:])
    raise SystemExit(0 if valid and verify_source_coverage() else 1)
