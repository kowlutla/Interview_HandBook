"""Builds search-index.js (one record per h2 section of every page). Run after content changes:
python -I C:/Users/kmangali/HLD/tools/build_search.py"""
import os, re, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'index.html', '404.html', 'search.html'}
recs = []


def clean(s):
    s = re.sub(r'(?is)<(script|style|svg)\b.*?</\1>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


for d, _, fs in os.walk(ROOT):
    if 'archive' in d.split(os.sep): continue
    for f in sorted(fs):
        if not f.endswith('.html') or f in SKIP and os.path.dirname(os.path.join(d, f)) == ROOT: continue
        if f in ('index.html', '404.html', 'search.html'): continue
        rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
        s = open(os.path.join(d, f), encoding='utf-8').read()
        m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        title = clean(m.group(1)) if m else f
        part = 'Handbook' if rel.startswith('handbook/') else 'Interview Book' if rel.startswith('interview/') else 'Quick Notes'
        body = s[s.find('<main'):] if '<main' in s else s
        pieces = re.split(r'(?=<h2\b)', body)
        intro = clean(pieces[0])[:400]
        recs.append(dict(u=rel, p=title, g=part, h='', x=intro))
        used = {}
        for pc in pieces[1:]:
            hm = re.match(r'<h2([^>]*)>(.*?)</h2>', pc, re.S)
            if not hm: continue
            idm = re.search(r'id="([^"]+)"', hm.group(1))
            head = clean(hm.group(2))
            if idm: hid = idm.group(1)
            else:
                hid = None  # no stable id in the source: link to the page, not an invented anchor
            if hid: used[hid] = 1
            recs.append(dict(u=rel + ('#' + hid if hid else ''), p=title, g=part, h=head, x=clean(pc[hm.end():])[:500]))
out = 'window.HLD_SEARCH=' + json.dumps(recs, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(os.path.join(ROOT, 'search-index.js'), 'w', encoding='utf-8', newline='\n').write(out)
print('indexed %d sections, %d KB' % (len(recs), len(out) // 1024))
