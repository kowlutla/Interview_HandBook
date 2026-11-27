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
    topics_root = os.path.join(ROOT, 'site', 'dsa', 'topics')
    relative_to_topics = os.path.relpath(full, topics_root)
    is_problem = bool(os.path.dirname(relative_to_topics))
    is_foundations = full.endswith(os.path.join('topics', 'foundations.html'))
    if p.problems < 1 and not is_foundations: p.errors.append('no DSA problem article found')
    if is_problem and p.h2 < 5: p.errors.append('problem page should contain its problem title and detailed sections')
    if not is_problem and p.h2 < 2: p.errors.append('topic index should contain at least two h2 sections')
    styles = ('../../../handbook/assets/style.css', '../../../quicknotes/assets/quick.css', '../../assets/dsa.css') if is_problem else ('../../handbook/assets/style.css', '../../quicknotes/assets/quick.css', '../assets/dsa.css')
    for required in styles:
        if required not in raw: p.errors.append('missing stylesheet: ' + required)
    if is_problem and 'dsa-breadcrumb' not in raw: p.errors.append('problem page is missing breadcrumbs')
    if not is_problem and not is_foundations and 'dsa-problem-summary' not in raw: p.errors.append('topic index must use concise problem summaries')
    if is_problem and not any(x in raw for x in ('id="definition"', 'id="iso-understand"', 'id="id-understand"')): p.errors.append('problem page is missing the problem definition section')
    if is_problem and not any(x in raw for x in ('id="dry-run"', 'id="iso-walkthrough"', 'id="id-walkthrough"')): p.errors.append('problem page is missing the walkthrough section')
    if is_problem and not any(x in raw for x in ('id="correctness"', 'id="iso-proof"', 'id="id-proof"')): p.errors.append('problem page is missing correctness reasoning')
    if is_problem and not any(x in raw for x in ('id="analysis"', 'id="iso-complexity"', 'id="id-complexity"')): p.errors.append('problem page is missing complexity analysis')
    print('%s: %d problem article(s), %d h2 headings -> %s' % (path, p.problems, p.h2, 'OK' if not p.errors else 'PROBLEMS'))
    for e in p.errors: print(' - ' + e)
    return not p.errors

def verify_source_coverage():
    source_root = os.path.join(ROOT, 'dsa-source', 'src', 'com', 'dsa')
    if not os.path.isdir(source_root):
        print('DSA source checkout not present; source coverage check skipped')
        return True
    expected_files = sum(1 for d, _, files in os.walk(source_root) for f in files if f.endswith('.java'))
    topic_slugs = ['patterns','mathematical','arrays','strings','sorting','binarysearch','matrix','linkedlist','recursion','bit_magic','stack','queue','binary_tree','binary_search_tree','greedy','graphs','dynamic_programming']
    expected_pages = 0
    grouped_source_files = 0
    for slug in topic_slugs:
        folder = os.path.join(source_root, slug)
        if not os.path.isdir(folder): continue
        names = [f[:-5] for f in os.listdir(folder) if f.endswith('.java')]
        if slug == 'arrays': names = [n for n in names if n + '.java' not in {'A22SetMatrixZeroes.java','A23RotateImageAntiClockWise.java','A23RotateImageClockwise.java'}]
        if slug == 'matrix':
            names += [f[:-5] for f in ('A22SetMatrixZeroes.java','A23RotateImageAntiClockWise.java','A23RotateImageClockwise.java') if os.path.isfile(os.path.join(source_root,'arrays',f))]
        grouped = {}
        for name in names: grouped.setdefault(name.rstrip('0123456789'), []).append(name)
        expected_pages += len(grouped)
        grouped_source_files += sum(len(v) for v in grouped.values())
    topic_root = os.path.join(ROOT, 'site', 'dsa', 'topics')
    topic_pages = [os.path.join(topic_root, f) for f in os.listdir(topic_root)
                   if f.endswith('.html') and os.path.isfile(os.path.join(topic_root, f))]
    actual = 0
    for path in topic_pages:
        raw = open(path, encoding='utf-8').read()
        actual += len(re.findall(r'<article class="dsa-problem-card dsa-problem-summary"', raw))
    detail_pages = 0
    # These 20 authored pattern walkthroughs supplement (rather than replace)
    # the source-generated reference pages. Count them as curated additions,
    # not as extra source entries in the one-to-one coverage check.
    curated_pattern_additions = {
        'alpha-hill.html', 'alphabet-ramp.html', 'ascending-number-triangle.html',
        'binary-number-triangle.html', 'concentric-number-square.html',
        'descending-alpha-triangle.html', 'diamond-star.html', 'floyd-triangle.html',
        'half-diamond.html', 'hollow-square.html', 'increasing-letter-triangle.html',
        'inverted-number-triangle.html', 'inverted-right-triangle.html',
        'number-crown.html', 'repeated-row-number.html', 'reverse-letter-triangle.html',
        'right-angle-star.html', 'solid-square.html', 'symmetric-butterfly.html',
        'symmetric-void.html',
    }
    quality_gaps = {'statement': 0, 'examples': 0, 'constraints': 0, 'method_explanation': 0, 'complexity_note': 0}
    for current, _, names in os.walk(topic_root):
        if os.path.relpath(current, topic_root) == '.': continue
        for name in names:
            if not name.endswith('.html'): continue
            if os.path.relpath(current, topic_root) == 'patterns' and name in curated_pattern_additions:
                continue
            detail_pages += 1
            raw = open(os.path.join(current, name), encoding='utf-8').read()
            if 'does not include a formal problem statement' in raw: quality_gaps['statement'] += 1
            if 'No canonical sample is documented' in raw: quality_gaps['examples'] += 1
            if 'Explicit constraints are not documented' in raw: quality_gaps['constraints'] += 1
            if 'No method-level explanation is documented' in raw: quality_gaps['method_explanation'] += 1
            if 'No complexity annotation is documented' in raw: quality_gaps['complexity_note'] += 1
    ok = len(topic_pages) == 18 and grouped_source_files == expected_files and actual == expected_pages and detail_pages == expected_pages
    print('DSA coverage: %d Java files grouped into %d problem/reference pages; %d indexed entries, %d standalone pages, %d topic pages -> %s' %
          (expected_files, expected_pages, actual, detail_pages, len(topic_pages), 'OK' if ok else 'INCOMPLETE'))
    print('Source-documentation gaps (pages needing manual enrichment): ' + ', '.join('%s=%d' % (k, v) for k, v in quality_gaps.items()))
    return ok


if __name__ == '__main__':
    if len(sys.argv) < 2: raise SystemExit('Pass one or more DSA HTML paths')
    valid = all(check(x) for x in sys.argv[1:])
    raise SystemExit(0 if valid and verify_source_coverage() else 1)
