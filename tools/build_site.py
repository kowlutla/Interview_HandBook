"""Regenerates every navigation piece of the combined interview-prep site so Handbook and Quick Notes stay in sync.
Run from anywhere:  python -I C:\\Users\\kmangali\\HLD\\tools\\build_site.py
Writes: quicknotes sidebar + prev/next on every page, quicknotes/index.html, index.html.
Page titles/descriptions are read from the pages themselves (h1 and the p.sub line); short sidebar titles are in MODS below.
The handbook side is manifest-driven (handbook/assets/chapters.js + nav.js) and already generates itself."""
import os, re, html

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')
QN = os.path.join(ROOT, 'quicknotes')

MODS = [  # id, short title, handbook chapters covered
    ('q01-framework-estimation', 'Framework and estimation', 'Ch 1-2'),
    ('q02-networking-api', 'Networking, APIs, real-time', 'Ch 3-7'),
    ('q03-stateless-tier', 'Stateless tier: LB, gateway, CDN, limits', 'Ch 8-12, 16'),
    ('q04-caching', 'Caching and Redis', 'Ch 13-15'),
    ('q05-data-stores', 'Data stores and storage engines', 'Ch 17-23'),
    ('q06-replication-sharding', 'Replication, sharding, multi-region', 'Ch 24-26'),
    ('q07-distributed-theory', 'Distributed systems theory', 'Ch 27-33'),
    ('q08-async', 'Async: queues, Kafka, events, streams', 'Ch 34-38'),
    ('q09-resilience-ha', 'Resilience, HA/DR, deployment', 'Ch 39-43'),
    ('q10-microservices', 'Microservices in depth', 'Ch 44-53'),
    ('q11-crosscutting', 'Observability, security, privacy', 'Ch 54-56'),
    ('q12-algorithms', 'Algorithms and data structures', 'Ch 57-59'),
    ('q13-delivery-playbook', 'Playbook, delivery, cheat sheet', 'Ch 60-61 + cheat sheets'),
    ('q14-practice-questions', 'Practice question bank', 'All chapters and cases'),
]
MODS = [m for m in MODS if os.path.exists(os.path.join(QN, 'notes', m[0] + '.html'))]
CASES = sorted(f[:-5] for f in os.listdir(os.path.join(QN, 'cases')) if f.endswith('.html'))


def read(p):
    with open(p, encoding='utf-8') as f: return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)


def esc(s): return html.escape(s, quote=True)


HB = read(os.path.join(ROOT, 'handbook', 'assets', 'chapters.js'))
HB_MODS = []  # (module title, [(id, title, dir, first chapter number or None)])
for mm in re.finditer(r'\{ id: "(m\d+)", title: "([^"]+)", dir: "([^"]+)", items: \[(.*?)\n    \]\}', HB, re.S):
    its = [(i.group(1), i.group(2), i.group(3) or mm.group(3)) for i in
           re.finditer(r'\{ id: "([^"]+)", t: "([^"]+)", d: "[^"]*"(?:, done: true)?(?:, dir: "([^"]+)")? \}', mm.group(4))]
    HB_MODS.append((mm.group(1), mm.group(2), its))
HB_TITLE = {i[0]: i[1] for m in HB_MODS for i in m[2]}


def case_title(cid):
    if cid in HB_TITLE: return HB_TITLE[cid]
    h = re.search(r'<h1>(.*?)</h1>', read(os.path.join(QN, 'cases', cid + '.html')), re.S).group(1)
    h = re.sub(r'(?i)^case sheet:\s*', '', h)
    h = re.sub(r'(?i)^design (a |an |the )?', '', h)
    h = re.sub(r'<[^>]+>', '', h).strip()
    return h[:1].upper() + h[1:]


def sub_of(path):
    m = re.search(r'<p class="sub">(.*?)</p>', read(path), re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''


def stats(path):
    s = re.sub(r'<!--qnav:start-->.*?<!--qnav:end-->', '', read(path), flags=re.S)
    words = len(re.sub(r'<[^>]+>', ' ', s).split())
    return words, s.count('<details'), len(re.findall(r'<svg[^>]*viewBox', s))


items = []  # flat reading order
for i, (mid, t, ch) in enumerate(MODS, 1):
    items.append(dict(kind='mod', id=mid, num='%02d' % i, title=t, ch=ch, href='notes/%s.html' % mid))
for cid in CASES:
    items.append(dict(kind='case', id=cid, num=cid[1:3], title=case_title(cid), ch='', href='cases/%s.html' % cid))
for it in items:
    it['path'] = os.path.join(QN, it['href'])
    it['desc'] = sub_of(it['path'])
    it['words'], it['qa'], it['svg'] = stats(it['path'])


def badge(ch):
    b = re.sub(r'^Ch ', '', ch).split(' +')[0].replace('-', '–')
    return b if re.match(r'^[0-9]', b) else '★'


def first_ch(ch):
    m = re.match(r'Ch (\d+)', ch)
    return int(m.group(1)) if m else None


def qlinks_html(cur, pre):
    hb = pre + '../handbook/'
    href, label = hb + 'index.html', 'Open the Handbook'
    if cur and re.match(r'c\d\d-', cur):
        for m in HB_MODS:
            for i in m[2]:
                if i[0] == cur: href, label = '%s%s/%s.html' % (hb, i[2], i[0]), 'Full case in the Handbook'
    elif cur:
        x = [y for y in items if y['id'] == cur][0]
        n = first_ch(x['ch'])
        if n:
            for m in HB_MODS:
                for i in m[2]:
                    if re.match(r'%02d-' % n, i[0]): href, label = '%s%s/%s.html' % (hb, i[2], i[0]), 'Full chapters in the Handbook'
    rows = [('🏠 Home', pre + '../index.html'), ('🔍 Search the whole site', pre + '../search.html')]
    o = '<div class="qlinks">'
    if label != 'Open the Handbook': o += '<a class="ctx" href="%s">📖 %s</a>' % (href, label)
    for t, h in rows: o += '<a href="%s">%s</a>' % (h, t)
    return o + '</div>'


def nav_html(cur, pre):
    """Sidebar that mirrors the Handbook: same module names and order, same case titles.
    pre = relative prefix from the page to the quicknotes root ('' for index, '../' for sub pages)"""
    hb = pre + '../handbook/'
    o = [('<a class="brand" href="%sindex.html">System Design Quick Notes</a>' % pre) if cur else '<div class="brand">System Design Quick Notes</div>',
         '<div class="tagline">Lookup sheets for the day before the interview</div>',
         qlinks_html(cur, pre)]
    mods = [x for x in items if x['kind'] == 'mod']
    cases = {x['id']: x for x in items if x['kind'] == 'case'}

    def link(x, label):
        cls = 'ch current' if x['id'] == cur else 'ch'
        num = '<span class="num">%s</span>' % label if label else ''
        s = ['<a class="%s" href="%s%s">%s<span>%s</span></a>' % (cls, pre, x['href'], num, esc(x['title']))]
        if x['id'] == cur:
            heads = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', read(x['path']), re.S)
            if heads:
                s.append('<div class="onpage">')
                for hid, ht in heads:
                    s.append('<a href="#%s">%s</a>' % (hid, esc(html.unescape(re.sub(r'<[^>]+>', '', ht).strip()))))
                s.append('</div>')
        return ''.join(s) if False else '\n'.join(s)

    def group(title, body, ids):
        is_open = (cur is None and title == HB_MODS[0][1]) or cur in ids
        return '<details%s><summary>%s</summary>\n%s\n</details>' % (' open' if is_open else '', esc(title), '\n'.join(body))

    for mid, mtitle, its in HB_MODS:
        nums = [int(i[0][:2]) for i in its if re.match(r'\d\d-', i[0])]
        if mid == 'm11':
            body = [link(cases[i[0]], 'C' + i[0][1:3]) for i in its if i[0] in cases]
            o.append(group(mtitle, body, [i[0] for i in its]))
        elif nums:
            lo, hi = min(nums), max(nums)
            sel = [x for x in mods if first_ch(x['ch']) is not None and lo <= first_ch(x['ch']) <= hi]
            if sel:
                o.append(group(mtitle, [link(x, '') for x in sel], [x['id'] for x in sel]))
        elif mid == 'm12':
            body = ['<a class="ch" href="%s%s/%s.html"><span class="num">★</span><span>%s</span></a>' % (hb, i[2], i[0], esc(i[1])) for i in its]
            o.append(group(mtitle, body, []))
        elif mid == 'm13':
            body = ['<a class="ch" href="%s%s/%s.html"><span class="num">A–Z</span><span>%s</span></a>' % (hb, i[2], i[0], esc(i[1])) for i in its]
            o.append(group('Reference', body, []))
    prac = [x for x in mods if first_ch(x['ch']) is None]
    if prac:
        o.insert(len(o) - 1, group('Practice', [link(x, '') for x in prac], [x['id'] for x in prac]))
    return '\n'.join(o)


def pager_html(idx, pre):
    o = ['<div class="pager">']
    if idx > 0:
        p = items[idx - 1]
        o.append('<a class="prev" href="%s%s"><span class="lbl">Previous</span>%s</a>' % (pre, p['href'], esc(p['title'])))
    if idx < len(items) - 1:
        n = items[idx + 1]
        o.append('<a class="next" href="%s%s"><span class="lbl">Next</span>%s</a>' % (pre, n['href'], esc(n['title'])))
    o.append('</div>')
    return ''.join(o)


for idx, x in enumerate(items):
    s = read(x['path'])
    s = re.sub(r'<!--qnav:start-->.*?<!--qnav:end-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--qfoot:start-->.*?<!--qfoot:end-->\n?', '', s, flags=re.S)
    head = '<!--qnav:start-->\n<div class="layout">\n<nav class="toc" id="toc">\n%s\n</nav>\n<main class="qmain">\n<!--qnav:end-->\n' % nav_html(x['id'], '../')
    foot = '<!--qfoot:start-->\n%s\n</main>\n</div>\n<script src="../assets/quick.js"></script>\n<!--qfoot:end-->\n' % pager_html(idx, '../')
    s = s.replace('<div class="qn">', head + '<div class="qn">', 1)
    s = s.replace('</body>', foot + '</body>', 1)
    write(x['path'], s)

# ---------------- quicknotes/index.html ----------------
tw = sum(x['words'] for x in items); tq = sum(x['qa'] for x in items); ts = sum(x['svg'] for x in items)
mods = [x for x in items if x['kind'] == 'mod']; cases = [x for x in items if x['kind'] == 'case']


def cards(group, label):
    o = ['<div class="grid">']
    for x in group:
        extra = ('<span class="tag">%s</span>' % esc(x['ch'])) if x['ch'] else ''
        o.append('<a class="card" href="%s">%s<span class="n">%s %s</span><span class="t">%s</span><span class="d">%s</span><span class="d">%d diagrams, %d Q&amp;As</span></a>'
                 % (x['href'], extra, label, x['num'], esc(x['title']), esc(x['desc']), x['svg'], x['qa']))
    o.append('</div>')
    return '\n'.join(o)


qindex = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>System Design Quick Notes</title>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/quick.css">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="layout">
<nav class="toc" id="toc">
%(nav)s
</nav>
<main class="qmain">
<div class="qn qhome">
<h1>System Design Quick Notes</h1>
<p class="sub">Fast lookup sheets for the day or two before an interview. Plain words, diagrams, tables and real interview Q&amp;A. Each sheet matches a group of Handbook chapters, so you can jump to the full explanation when something is unclear.</p>
<div class="stats">
<div class="stat"><b>%(nm)d</b><span>study sheets</span></div>
<div class="stat"><b>%(nc)d</b><span>case-study sheets</span></div>
<div class="stat"><b>%(tq)d</b><span>interview Q&amp;As</span></div>
<div class="stat"><b>%(ts)d</b><span>diagrams</span></div>
</div>
<div class="tl"><b>Short on time?</b> Open <a href="notes/q13-delivery-playbook.html">the last-hour sheet</a> first (numbers, decision tables, checklists, time plan). Then read the study sheets for your weak areas, then practise two or three case sheets out loud.</div>
<details class="mod" open><summary class="modsum"><h2 id="study">Study sheets</h2><span class="cnt">%(nm)d sheets</span></summary>
%(modcards)s
</details>
<details class="mod" open><summary class="modsum"><h2 id="cases">Case-study sheets</h2><span class="cnt">%(nc)d sheets</span></summary>
%(casecards)s
</details>
<p><a href="../handbook/index.html">Open the full Handbook</a> | <a href="../index.html">Home</a></p>
</div>
</main>
</div>
<script src="assets/quick.js"></script>
</body>
</html>
''' % dict(nav=nav_html(None, ''), nm=len(mods), nc=len(cases), tq=tq, ts=ts,
           modcards=cards(mods, 'Sheet'), casecards=cards(cases, 'Case'))
write(os.path.join(QN, 'index.html'), qindex)

# ---------------- interview/ (Interview Book: one page per topic) ----------------
IV = os.path.join(ROOT, 'interview')
INT_TOPICS = [  # slug, short title. Order = reading order. Only topics whose page exists are built.
    ('git', 'Git'),
    ('java-fundamentals', 'Java: Language and OOP'),
    ('java-collections', 'Java: Collections'),
    ('java-concurrency', 'Java: Concurrency'),
    ('java-jvm', 'Java: JVM, Memory and GC'),
    ('java-modern', 'Java: 8 to 21 Features'),
    ('java-exceptions-io', 'Java: Exceptions, Generics and I/O'),
    ('spring-framework', 'Spring Framework'),
    ('spring-boot', 'Spring Boot'),
    ('maven-gradle', 'Maven and Gradle'),
    ('ci-cd', 'CI/CD'),
    ('docker-kubernetes', 'Docker, Kubernetes and Helm'),
    ('redis-caching', 'Redis and Caching'),
    ('elasticsearch', 'Elasticsearch'),
    ('hibernate-jpa', 'Hibernate and JPA'),
    ('kafka', 'Kafka'),
    ('microservices-rest', 'Microservices and REST APIs'),
    ('distributed-systems', 'Distributed Systems'),
    ('sql-databases', 'SQL and Databases'),
    ('design-patterns-lld', 'Design Patterns and LLD'),
    ('security-api-design', 'Security and API Design'),
    ('resume-deep-dive', 'Your Projects: Resume Deep Dive'),
    ('data-engineering', 'Data Engineering (Avro, Iceberg)'),
    ('spark', 'Apache Spark'),
    ('hld-approach', 'HLD: Interview Approach and Estimation'),
    ('hld-networking-api', 'HLD: Networking, Load Balancing and APIs'),
    ('hld-scaling-caching', 'HLD: Scaling and Caching'),
    ('hld-databases', 'HLD: Databases and Storage'),
    ('hld-replication-sharding', 'HLD: Replication and Sharding'),
    ('hld-distributed-theory', 'HLD: Distributed Systems Theory'),
    ('hld-async-messaging', 'HLD: Async, Messaging and Events'),
    ('hld-resilience', 'HLD: Resilience and High Availability'),
    ('hld-microservices-arch', 'HLD: Microservices and Architecture'),
    ('hld-cross-cutting', 'HLD: Security, Observability and Operations'),
    ('hld-building-blocks', 'HLD: Algorithms and Building Blocks'),
    ('hld-real-world-scenarios', 'HLD: Real-World Scenarios and Incidents'),
    ('hld-design-tradeoffs', 'HLD: Design Trade-offs and Judgment'),
]
INT_TOPICS = [t for t in INT_TOPICS if os.path.exists(os.path.join(IV, 'topics', t[0] + '.html'))]


IV_GROUPS = [  # (group title, [slugs]); a group is shown only if it has built pages
    ('Orientation', ['git']),
    ('Java', ['java-fundamentals', 'java-collections', 'java-concurrency', 'java-jvm', 'java-modern', 'java-exceptions-io']),
    ('Spring and Persistence', ['spring-framework', 'spring-boot', 'hibernate-jpa', 'sql-databases']),
    ('Build and Delivery', ['maven-gradle', 'ci-cd', 'docker-kubernetes']),
    ('Messaging, Caching and Search', ['kafka', 'redis-caching', 'elasticsearch']),
    ('Architecture', ['microservices-rest', 'distributed-systems', 'design-patterns-lld', 'security-api-design']),
    ('Data Engineering', ['data-engineering', 'spark']),
    ('System Design (HLD)', ['hld-approach', 'hld-networking-api', 'hld-scaling-caching', 'hld-databases', 'hld-replication-sharding', 'hld-distributed-theory', 'hld-async-messaging', 'hld-resilience', 'hld-microservices-arch', 'hld-cross-cutting', 'hld-building-blocks', 'hld-real-world-scenarios', 'hld-design-tradeoffs']),
    ('Your Experience', ['resume-deep-dive']),
]
_ord = [x for _g, _sl in IV_GROUPS for x in _sl]
INT_TOPICS.sort(key=lambda t: _ord.index(t[0]) if t[0] in _ord else 999)
IV_HUBS = {'Java': ('java', 'Java', 'java-'), 'System Design (HLD)': ('hld', 'System Design (HLD)', 'hld-')}  # group -> (hub file/slug, name, topic prefix)
IV_QN = {'redis-caching': 'q04-caching', 'distributed-systems': 'q07-distributed-theory', 'microservices-rest': 'q10-microservices',
         'kafka': 'q08-async', 'sql-databases': 'q05-data-stores', 'design-patterns-lld': 'q12-algorithms'}


def iv_nav(cur, pre):
    """pre = relative prefix from the page to the interview root ('' for the index, '../' for topic pages)."""
    site = pre + '../'
    ctx = ''
    if cur in IV_QN:
        ctx = '<a class="ctx" href="%squicknotes/notes/%s.html">📖 Related Quick Notes sheet</a>' % (site, IV_QN[cur])
    o = [('<a class="brand" href="%sindex.html">Interview Book</a>' % pre) if cur else '<div class="brand">Interview Book</div>',
         '<div class="tagline">Questions with model answers, diagrams and real scenarios</div>',
         '<div class="qlinks">%s<a href="%sindex.html">🏠 Home</a><a href="%ssearch.html">🔍 Search the whole site</a></div>' % (ctx, site, site)]
    titles = dict(INT_TOPICS)

    def item(slug, title, label):
        cls = 'ch current' if slug == cur else 'ch'
        num = '<span class="num">%s</span>' % label if label else ''
        s = ['<a class="%s" href="%stopics/%s.html">%s<span>%s</span></a>' % (cls, pre, slug, num, esc(title))]
        if slug == cur:
            heads = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', read(os.path.join(IV, 'topics', slug + '.html')), re.S)
            if heads:
                s.append('<div class="onpage">')
                for hid, ht in heads: s.append('<a href="#%s">%s</a>' % (hid, esc(html.unescape(re.sub(r'<[^>]+>', '', ht).strip()))))
                s.append('</div>')
        return '\n'.join(s)

    n = 0
    first = True
    for gtitle, slugs in IV_GROUPS:
        slugs = [x for x in slugs if x in titles]
        if not slugs: continue
        body = []
        hub = IV_HUBS.get(gtitle)
        if hub:
            hub_cls = 'ch current' if cur == hub[0] + '-hub' else 'ch'
            body.append('<a class="%s" href="%s%s.html"><span>%s overview</span></a>' % (hub_cls, pre, hub[0], hub[1]))
        for x in slugs:
            n += 1
            t = titles[x].split(': ', 1)[-1] if x.startswith(('java-', 'hld-', 'dsa-')) else titles[x]
            body.append(item(x, t, '%02d' % n))
        is_open = (cur is None and first) or cur in slugs or (hub is not None and cur == hub[0] + '-hub')
        first = False
        o.append('<details%s><summary>%s</summary>\n%s\n</details>' %(' open' if is_open else '', esc(gtitle), '\n'.join(body)))
    return '\n'.join(o)


iv_stats = {}
for i, (slug, title) in enumerate(INT_TOPICS):
    p = os.path.join(IV, 'topics', slug + '.html')
    s = read(p)
    s = re.sub(r'<!--qnav:start-->.*?<!--qnav:end-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--qfoot:start-->.*?<!--qfoot:end-->\n?', '', s, flags=re.S)
    iv_stats[slug] = dict(q=s.count('<details class="iq'), svg=len(re.findall(r'<svg[^>]*viewBox', s)),
                          words=len(re.sub(r'<[^>]+>', ' ', s).split()), sub=sub_of(p))
    pg = ['<div class="pager">']
    if i > 0: pg.append('<a class="prev" href="%s.html"><span class="lbl">Previous</span>%s</a>' % (INT_TOPICS[i - 1][0], esc(INT_TOPICS[i - 1][1])))
    if i < len(INT_TOPICS) - 1: pg.append('<a class="next" href="%s.html"><span class="lbl">Next</span>%s</a>' % (INT_TOPICS[i + 1][0], esc(INT_TOPICS[i + 1][1])))
    pg.append('</div>')
    head = '<!--qnav:start-->\n<div class="layout">\n<nav class="toc" id="toc">\n%s\n</nav>\n<main class="qmain">\n<!--qnav:end-->\n' % iv_nav(slug, '../')
    foot = '<!--qfoot:start-->\n%s\n</main>\n</div>\n<script src="../../quicknotes/assets/quick.js"></script>\n<!--qfoot:end-->\n' % ''.join(pg)
    s = s.replace('<div class="qn">', head + '<div class="qn">', 1).replace('</body>', foot + '</body>', 1)
    write(p, s)

iv_q = sum(v['q'] for v in iv_stats.values())
HUB_PARTS = {h[0]: [(s, t.split(': ', 1)[-1]) for s, t in INT_TOPICS if s.startswith(h[2])] for h in IV_HUBS.values()}
HUB_BY_PREFIX = {h[2]: h for h in IV_HUBS.values()}
mods = []  # (href, title, description, questions, diagrams, unit)
hub_added = set()
for slug, title in INT_TOPICS:
    hk = [p for p in HUB_BY_PREFIX if slug.startswith(p)]
    if hk:
        hb = HUB_BY_PREFIX[hk[0]]
        if hb[0] in hub_added: continue
        hub_added.add(hb[0])
        parts = HUB_PARTS[hb[0]]
        mods.append((hb[0] + '.html', hb[1], ('All %s coding problems in %d topic pages: %s.' if hb[0] == 'dsa' else 'All %s interview questions in %d parts: %s.') % (hb[1], len(parts), ', '.join(t for _, t in parts)),
                     sum(iv_stats[s]['q'] for s, _ in parts), sum(iv_stats[s]['svg'] for s, _ in parts)))
    else:
        mods.append(('topics/%s.html' % slug, title, iv_stats[slug]['sub'], iv_stats[slug]['q'], iv_stats[slug]['svg']))
def card_label(h):
    """Home-page card number = the sidebar number(s) of the topic(s) behind the card."""
    if not h.startswith('topics/'):
        pre = [hb[2] for hb in IV_HUBS.values() if hb[0] + '.html' == h][0]
        ns = [i + 1 for i, (sl, _t) in enumerate(INT_TOPICS) if sl.startswith(pre)]
        return 'Topics %02d to %02d' % (ns[0], ns[-1])
    sl = h.split('/')[1][:-5]
    return 'Topic %02d' % ([i for i, (a, _t) in enumerate(INT_TOPICS) if a == sl][0] + 1)


iv_cards = '\n'.join('<a class="card" href="%s"><span class="n">%s</span><span class="t">%s</span><span class="d">%s</span><span class="d">%d %s, %d diagrams</span></a>'
                     % (h, card_label(h), esc(t), esc(d), q, 'problems' if h == 'dsa.html' else 'questions', g) for (h, t, d, q, g) in mods)
for hb in IV_HUBS.values():
    JAVA_PARTS = HUB_PARTS[hb[0]]
    if not JAVA_PARTS: continue
    java_cards = '\n'.join('<a class="card" href="topics/%s.html"><span class="n">Part %d</span><span class="t">%s</span><span class="d">%s</span><span class="d">%d %s, %d diagrams</span></a>'
                           % (s, i + 1, esc(t), esc(iv_stats[s]['sub']), iv_stats[s]['q'], 'problems' if hb[0] == 'dsa' else 'questions', iv_stats[s]['svg']) for i, (s, t) in enumerate(JAVA_PARTS))
    jq = sum(iv_stats[s]['q'] for s, _ in JAVA_PARTS)
    java_page = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s | Interview Book</title>
<link rel="stylesheet" href="../handbook/assets/style.css">
<link rel="stylesheet" href="../quicknotes/assets/quick.css">
<link rel="stylesheet" href="assets/interview.css">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="layout">
<nav class="toc" id="toc">
%s
</nav>
<main class="qmain">
<div class="qn qhome">
<h1>%s interview questions</h1>
<p class="sub">Everything about %s in one place, split into %d parts. Work through them in order, or jump to the part you need.</p>
<div class="stats">
<div class="stat"><b>%d</b><span>parts</span></div>
<div class="stat"><b>%d</b><span>%s</span></div>
</div>
<div class="grid">
%s
</div>
</div>
</main>
</div>
<script src="../quicknotes/assets/quick.js"></script>
</body>
</html>
''' % (hb[1], iv_nav(hb[0] + '-hub', ''), hb[1], hb[1], len(JAVA_PARTS), len(JAVA_PARTS), jq, 'problems' if hb[0] == 'dsa' else 'questions', java_cards)
    write(os.path.join(IV, hb[0] + '.html'), java_page)
iv_index = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interview Book</title>
<link rel="stylesheet" href="../handbook/assets/style.css">
<link rel="stylesheet" href="../quicknotes/assets/quick.css">
<link rel="stylesheet" href="assets/interview.css">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="layout">
<nav class="toc" id="toc">
%(nav)s
</nav>
<main class="qmain">
<div class="qn qhome">
<h1>Interview Book</h1>
<p class="sub">Interview questions for each topic with model answers, diagrams, follow-up questions and real production scenarios. Every question is marked Basic, Intermediate or Senior, so you can start at your level and move up.</p>
<div class="stats">
<div class="stat"><b>%(nt)d</b><span>topics</span></div>
<div class="stat"><b>%(nq)d</b><span>questions</span></div>
</div>
<div class="tl"><b>How to use it:</b> read a question, answer it out loud before you open it, then compare. Use the follow-ups to practise going one level deeper, and the scenario questions to practise thinking under pressure.</div>
<div class="grid">
%(cards)s
</div>
</div>
</main>
</div>
<script src="../quicknotes/assets/quick.js"></script>
</body>
</html>
''' % dict(nav=iv_nav(None, ''), nt=len(mods), nq=iv_q, cards=iv_cards)
if INT_TOPICS: write(os.path.join(IV, 'index.html'), iv_index)


# ---------------- dsa/ (independent Data Structures and Algorithms section) ----------------
DSA = os.path.join(ROOT, 'dsa')
DSA_SOURCE = os.path.join(os.path.dirname(ROOT), 'dsa-source', 'src', 'com', 'dsa')

# The order is a deliberate learning progression: fundamentals first, then core
# data structures, trees/greedy, and finally graph and dynamic-programming topics.
DSA_TOPIC_CONFIG = [
    ('foundations', 'Foundations', 'Learn algorithm analysis, constraints, data-structure selection and a repeatable problem-solving process.', 'Asymptotic analysis; time and auxiliary space; Java correctness; data-structure selection; testing.'),
    ('patterns', 'Patterns', 'Translate visual patterns into row/column relationships and precise loop bounds.', 'Nested loops; row and column progression; symmetry; spacing and boundaries.'),
    ('mathematical', 'Mathematics', 'Build fluency with digits, divisibility, primes, factors, powers, roots and numeric edge cases.', 'Digit extraction; divisors and primes; modular arithmetic; numeric limits.'),
    ('arrays', 'Arrays', 'Learn traversal, in-place updates, two pointers, prefix sums, hashing, subarrays and greedy reasoning.', 'Single-pass traversal; two pointers; prefix sums; sliding windows; frequency maps.'),
    ('strings', 'Strings', 'Treat strings as indexed character sequences; reason about frequency, mappings, matching and character constraints.', 'Frequency counting; one-to-one mappings; pattern matching; parsing.'),
    ('sorting', 'Sorting', 'Understand comparison sorting, stability, partitioning, divide and conquer, and sorting as preprocessing.', 'Elementary sorts; merge sort; quick sort; partitioning; stability.'),
    ('binarysearch', 'Binary Search', 'Progress from bounds and sorted data to rotated arrays, answer-space search and matrix search.', 'Lower/upper bounds; first and last occurrence; rotated arrays; answer-space search.'),
    ('matrix', 'Matrix', 'Model a matrix with row and column coordinates; practise boundaries, traversal and in-place transformations.', 'Spiral traversal; row/column marking; matrix rotation; neighbourhoods.'),
    ('linkedlist', 'Linked Lists', 'Master pointer movement, dummy nodes, fast/slow pointers, reversal, cycle detection and merging.', 'Pointer fundamentals; reversal; cycle detection; intersection; merge and clone.'),
    ('recursion', 'Recursion & Backtracking', 'Learn base cases, recursive state, call-stack behaviour, subsequences, permutations and constraint-driven search.', 'Recursive decomposition; subsequences; combinations; permutations; pruning.'),
    ('bit_magic', 'Bit Manipulation', 'Work with binary representation, masks, shifts, XOR properties, set bits and bitwise state compression.', 'Bitwise operators; masks and shifts; set-bit counting; XOR properties.'),
    ('stack', 'Stacks', 'Use LIFO state for nested structure, expression validity, monotonic relationships, spans and range contributions.', 'Stack operations; valid parentheses; monotonic stacks; next/previous greater; range contributions.'),
    ('queue', 'Queues', 'Understand FIFO processing, queue implementations and queue-based simulation.', 'Array and linked queues; queue using stacks; FIFO processing.'),
    ('binary_tree', 'Binary Trees', 'Progress from representations and traversals to views, path problems, construction, serialization and transformations.', 'Tree traversals; level order; height and diameter; views; construction; serialization.'),
    ('binary_search_tree', 'Binary Search Trees', 'Use the ordering invariant for search, insertion, deletion, neighbours and order-statistic queries.', 'BST invariant; search/insert/delete; floor and ceil; kth element; validation.'),
    ('greedy', 'Greedy Algorithms', 'Learn to justify local choices, sort by the right criterion and reason about intervals and resources.', 'Scheduling; intervals; reachability; resource allocation; greedy-choice proofs.'),
    ('graphs', 'Graphs', 'Build from representations and traversals to components, cycle detection, topological order and shortest paths.', 'BFS and DFS; components; cycles; bipartite graphs; topological sort; shortest paths.'),
    ('dynamic_programming', 'Dynamic Programming', 'Move from state definition and recurrence to memoization, tabulation, space optimization and advanced DP patterns.', 'State and transition; memoization; tabulation; knapsack; subsequences; grids; stocks.')
]
DSA_TOPIC_TITLES = {slug: title for slug, title, _, _ in DSA_TOPIC_CONFIG}
DSA_MATRIX_FILES = {'A22SetMatrixZeroes.java', 'A23RotateImageAntiClockWise.java', 'A23RotateImageClockwise.java'}

def dsa_slug(filename):
    name = re.sub(r'\.java$', '', filename)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    name = re.sub(r'([A-Z])([A-Z][a-z])', r'\1-\2', name)
    return re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()

def dsa_title(filename):
    name = re.sub(r'\.java$', '', filename)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    name = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', name)
    return re.sub(r'\s+', ' ', re.sub(r'[_-]+', ' ', name)).strip()

def dsa_source_summary(source, title):
    match = re.search(r'/\*\*(.*?)\*/', source, re.S)
    if match:
        lines = [re.sub(r'^\s*\* ?|^\s*/\*\*?', '', line).strip()
                 for line in match.group(1).splitlines()]
        summary = ' '.join(x for x in lines if x and not x.startswith('@') and not re.search(r'(time|space) complexity', x, re.I))
        if summary:
            return summary[:2200]
    return 'Study the ' + title.lower() + ' implementation. Identify its input contract, the key observation, the invariant maintained by the algorithm, and the boundary cases.'

DSA_TOPIC_GUIDES = {
    'patterns': '<section class="dsa-section"><h2>Core reasoning</h2><ul><li>Write down what each row and column represents before choosing loop bounds.</li><li>Separate the number of rows, leading spaces and printed symbols; derive each from the row index.</li><li>Check the first and last row explicitly. Pattern questions are especially prone to off-by-one errors.</li></ul></section>',
    'mathematical': '<section class="dsa-section"><h2>Core reasoning</h2><ul><li>For divisor checks, iterate only while <code>i * i &lt;= n</code> using a wide type for the product; divisors occur in pairs.</li><li>For repeated prime queries, a sieve is usually better than testing every number independently.</li><li>Normalize modulo results when negative values are possible, and guard against overflow in products and factorial-like calculations.</li></ul></section>',
    'arrays': '<section class="dsa-section"><h2>Core patterns</h2><ul><li><b>Two pointers:</b> useful when sorted order or a monotonic movement rule lets one pointer move without revisiting discarded candidates.</li><li><b>Sliding window:</b> works when expanding and shrinking the window preserves a monotonic condition; a simple sum window is not generally valid with arbitrary negative values.</li><li><b>Prefix sums + hashing:</b> support subarray-sum questions with negative values where a conventional sliding window fails.</li><li><b>Kadane and greedy scans:</b> maintain the best state ending at the current position instead of recomputing every subarray.</li></ul></section>',
    'strings': '<section class="dsa-section"><h2>Core patterns</h2><ul><li>Frequency arrays are efficient only when the character domain is bounded and stated; otherwise use a map.</li><li>One-to-one transformations require checking both forward and reverse mappings.</li><li>For substring problems, distinguish a contiguous substring from a subsequence whose characters may be separated.</li><li>Java <code>char</code> represents a UTF-16 code unit. Use code-point APIs when the contract requires full Unicode characters.</li></ul></section>',
    'sorting': '<section class="dsa-section"><h2>How to compare sorting algorithms</h2><ul><li>Compare time in best, average and worst cases, auxiliary space, stability and whether the algorithm is in-place.</li><li>Merge sort gives predictable <code>O(n log n)</code> time but needs auxiliary storage for arrays; quicksort is often fast in practice but pivot choices affect worst-case behaviour.</li><li>Sorting can simplify a problem, but account for the <code>O(n log n)</code> preprocessing cost and whether original indices must be preserved.</li><li>Use overflow-safe comparators such as <code>Integer.compare</code>, not subtraction.</li></ul></section>',
    'binarysearch': '<section class="dsa-section"><h2>Binary-search invariants</h2><ul><li>Define the search interval and what each boundary means before writing the loop.</li><li>For lower bound, find the first position whose value is greater than or equal to the target; upper bound finds the first position strictly greater.</li><li>Binary search on the answer requires a monotonic feasibility predicate: once a candidate is feasible, all larger or all smaller candidates must remain feasible.</li><li>Use overflow-safe midpoint calculation: <code>mid = low + (high - low) / 2</code>.</li></ul></section>',
    'matrix': '<section class="dsa-section"><h2>Coordinate reasoning</h2><ul><li>Keep row and column bounds separate; rectangular matrices are not necessarily square.</li><li>For spiral traversal, shrink the top, bottom, left and right boundaries after each completed edge and guard against revisiting the final row or column.</li><li>For clockwise rotation of a square matrix, transpose and then reverse each row; anticlockwise rotation uses a different reflection order.</li><li>State whether an operation is in-place and whether the input dimensions permit it.</li></ul></section>',
    'linkedlist': '<section class="dsa-section"><h2>Pointer invariants</h2><ul><li>Save the next reference before rewiring a node; otherwise the remaining list can become unreachable.</li><li>A dummy head removes special cases when deleting or inserting near the head.</li><li>Fast/slow pointers solve middle-node and cycle questions; explain why their relative speed produces the required meeting or stopping point.</li><li>When reversing links, track previous, current and next explicitly. Check whether the method mutates the original list.</li></ul></section>',
    'recursion': '<section class="dsa-section"><h2>Backtracking state</h2><ul><li>Define the recursive state, the decision at each level, the base case and the progress measure.</li><li>In backtracking, apply a choice, recurse, then undo exactly that choice before exploring the next branch.</li><li>Sort or use a per-level duplicate guard when the problem requires unique combinations or permutations.</li><li>Prune only when the current partial state cannot lead to a valid answer; premature pruning can remove valid solutions.</li></ul></section>',
    'bit_magic': '<section class="dsa-section"><h2>Bitwise reasoning</h2><ul><li>Use masks to test, set, clear and toggle individual bits; parenthesize shifts and bitwise operations clearly.</li><li>XOR is associative and commutative, with <code>x ^ x = 0</code> and <code>x ^ 0 = x</code>; this explains many single-occurrence problems.</li><li>Java integer shifts operate on 32-bit or 64-bit values, and signed right shift differs from unsigned right shift.</li><li>Check sign, width and overflow assumptions before using bit tricks on negative values.</li></ul></section>',
    'stack': '<section class="dsa-section"><h2>Monotonic-stack reasoning</h2><ul><li>Maintain a stack whose values or indices are monotonic; pop elements when the current value resolves their next greater/smaller relationship.</li><li>Store indices when distance, width or contribution matters.</li><li>For duplicate values, choose strict versus non-strict comparisons deliberately so equal elements are assigned to exactly one range.</li><li>In amortized analysis, each element is pushed once and popped at most once, giving linear total stack work.</li></ul></section>',
    'queue': '<section class="dsa-section"><h2>FIFO reasoning</h2><ul><li>A queue processes work in arrival order; a deque supports efficient operations at both ends.</li><li>In BFS, mark a vertex visited when enqueuing it to avoid duplicate queue entries.</li><li>For level-order traversal, capture the queue size at the start of a level so newly enqueued nodes belong to the next level.</li><li>When implementing a queue with stacks, explain which operations are amortized and why each element moves only a bounded number of times.</li></ul></section>',
    'binary_tree': '<section class="dsa-section"><h2>Tree reasoning</h2><ul><li>For DFS, decide whether information is needed before visiting children, between children or after both children; this determines preorder, inorder or postorder.</li><li>For BFS, use a queue and process a fixed level size when the answer is level-based.</li><li>Clarify whether height counts nodes or edges; this changes base cases and diameter formulas.</li><li>For path problems, distinguish root-to-leaf paths from paths that may start and end at any nodes.</li></ul></section>',
    'binary_search_tree': '<section class="dsa-section"><h2>BST invariant</h2><ul><li>Every node must obey the chosen duplicate policy across its entire left and right subtrees, not just against its immediate children.</li><li>Inorder traversal of a valid BST produces sorted keys.</li><li>For deletion with two children, replace the node with its inorder successor or predecessor, then remove that replacement from its original location.</li><li>State whether operations are recursive or iterative and whether the tree is balanced; an ordinary BST can degrade to linear height.</li></ul></section>',
    'greedy': '<section class="dsa-section"><h2>Proving a greedy choice</h2><ul><li>A locally attractive choice is not enough. Explain why an optimal solution can be transformed to include that choice without becoming worse.</li><li>Sorting by earliest finish time is appropriate for maximum non-overlapping interval selection; other interval problems may require a different ordering.</li><li>For scheduling and resource problems, define the feasibility condition before choosing the next item.</li><li>Test small counterexamples to challenge the proposed greedy rule before committing to it.</li></ul></section>',
    'graphs': '<section class="dsa-section"><h2>Graph fundamentals</h2><ul><li>An adjacency list uses <code>O(V + E)</code> space and supports traversal in <code>O(V + E)</code>; an adjacency matrix uses <code>O(V²)</code> space.</li><li>BFS finds shortest paths by edge count in unweighted graphs. Dijkstra requires non-negative edge weights.</li><li>Topological ordering exists only for a directed acyclic graph; a cycle prevents a complete ordering.</li><li>For disconnected graphs, start traversal from every unvisited vertex if the task covers the whole graph.</li></ul></section>',
    'dynamic_programming': '<section class="dsa-section"><h2>DP design framework</h2><ul><li>Define a state that contains exactly the information needed to make future decisions; write the recurrence before coding.</li><li>Base cases represent the smallest subproblems. Tabulation order must ensure every dependency is already computed.</li><li>Memoization avoids recomputing states; tabulation makes evaluation order explicit. Both should represent the same recurrence.</li><li>Space optimization is valid only when discarded states are no longer needed. For 0/1 knapsack, one-dimensional updates run backward; for unbounded choices, update direction may differ.</li><li>Count states and transitions to derive time and space complexity instead of guessing from the code shape.</li></ul></section>'
}

def dsa_problem_page(topic_slug, topic_title, number, problem_slug, problem_title, source_files):
    """Create one standalone study page per problem, combining alternative Java source files."""
    source = source_files[0][0]
    all_source = '\n'.join(item[0] for item in source_files)
    close_comment = chr(42) + chr(47)
    doc = re.match(r'\s*/\*\*(.*?)' + re.escape(close_comment), source, re.S)
    lines = []
    if doc:
        for line in doc.group(1).splitlines():
            line = re.sub(r'^\s*\* ?', '', line).strip()
            if line and not line.startswith('@') and not re.match(r'author\b', line, re.I):
                lines.append(re.sub(r'\s+', ' ', line))
    statement, examples, constraints = [], [], []
    mode = 'statement'
    for line in lines:
        low = line.lower()
        if re.match(r'(example|sample input|sample output)', low):
            mode = 'examples'
        elif re.match(r'(constraints?|expected time|expected space|time complexity|space complexity)', low):
            mode = 'constraints'
        (statement if mode == 'statement' else examples if mode == 'examples' else constraints).append(line)
    method_pattern = re.compile(r'(public\s+(?:static\s+)?(?:[\w<>\[\], ?]+\s+)+(\w+)\s*\([^;{}]*\)\s*\{)', re.S)
    methods = []
    for m in method_pattern.finditer(all_source):
        if m.group(2) == 'main': continue
        prefix = all_source[max(0, m.start() - 1000):m.start()]
        doc_text = prefix.rsplit('/**', 1)[-1].split(close_comment, 1)[0] if '/**' in prefix and close_comment in prefix.rsplit('/**', 1)[-1] else ''
        desc = []
        for line in doc_text.splitlines():
            line = re.sub(r'^\s*\* ?', '', line).strip()
            if line and not line.startswith('@') and not re.search(r'(time|space) complexity', line, re.I):
                desc.append(line)
        complexity = '; '.join(re.findall(r'(?i)(?:time|space)\s+complexity\s*:\s*[^*]+', doc_text))
        methods.append((m.group(2), re.sub(r'\s+', ' ', m.group(1)).strip(), ' '.join(desc), complexity))
    statement_html = ''.join('<p>%s</p>' % esc(x) for x in statement) or '<p>The source file does not include a formal problem statement. This page documents the class as a supporting implementation; add the original problem contract before treating it as a standalone interview question.</p>'
    examples_html = '<pre class="dsa-code"><code>%s</code></pre>' % esc('\n'.join(examples)) if examples else '<p>No canonical sample is documented in the source. Confirm the external problem contract and create representative tests before relying on assumptions.</p>'
    constraints_html = '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in constraints) if constraints else '<p>Explicit constraints are not documented in the source file. Confirm the allowed input size, value range, nullability and mutation rules before finalizing the solution.</p>'
    method_html = ''.join('<article class="dsa-approach"><h3>Implementation %02d — <code>%s</code></h3><p><code>%s</code></p><p>%s</p><p><b>Source complexity note:</b> %s</p></article>' % (i, esc(x[0]), esc(x[1]), esc(x[2] or 'No method-level explanation is documented.'), esc(x[3] or 'No complexity annotation is documented; derive it from the implementation.')) for i,x in enumerate(methods,1))
    if not method_html: method_html = '<p>No public method was detected. Review the constructors and public API below.</p>'
    comments = []
    for x in re.findall(r'//\s*(.+)', all_source):
        x = re.sub(r'\s+', ' ', x).strip()
        if len(x) > 12 and x not in comments: comments.append(x)
        if len(comments) >= 7: break
    steps_html = '<ol>%s</ol>' % ''.join('<li>%s</li>' % esc(x) for x in comments) if comments else '<ol><li>Identify the input state and required output.</li><li>Trace the main loop or recursive state.</li><li>Explain the condition that advances the state and the termination condition.</li><li>Verify that every valid case is considered exactly as required.</li></ol>'
    source_links = []
    source_blocks = []
    for source_text, source_rel in source_files:
        source_url = 'https://github.com/kowlutla/DSA/blob/main/src/com/dsa/' + source_rel.replace(' ', '%20')
        source_links.append('<a href="%s" target="_blank" rel="noopener"><code>%s</code></a>' % (source_url, esc(source_rel)))
        source_blocks.append('<h3>%s</h3><pre class="dsa-code"><code>%s</code></pre>' % (esc(source_rel), esc(source_text)))
    description = statement[0] if statement else 'Java implementation reference for ' + problem_title
    return '''<!DOCTYPE html>
<html lang="en"><head><script src="../../../theme.js"></script><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(problem)s — %(topic)s | DSA Handbook</title><meta name="description" content="%(description)s">
<link rel="stylesheet" href="../../../handbook/assets/style.css"><link rel="stylesheet" href="../../../quicknotes/assets/quick.css"><link rel="stylesheet" href="../../assets/dsa.css"><link rel="icon" href="../../../favicon.svg" type="image/svg+xml"></head>
<body><div class="qn"><div id="dsa-page">
<nav class="dsa-breadcrumb" aria-label="Breadcrumb"><a href="../../../index.html">Home</a><span>/</span><a href="../../../dsa/index.html">DSA</a><span>/</span><a href="../%(topic_slug)s.html">%(topic)s</a><span>/</span><span aria-current="page">%(problem)s</span></nav>
<header class="dsa-hero dsa-problem-hero"><p class="dsa-kicker">DATA STRUCTURES &amp; ALGORITHMS / %(topic_upper)s / JAVA</p><h1>%(problem)s</h1><p class="sub">%(description)s</p><div class="dsa-meta"><span>Problem %(number)02d</span><span>Java implementation</span><span>Original DSA source</span></div></header>
<article class="dsa-problem-card" id="problem"><div class="dsa-card-head"><span class="dsa-number">%(number)02d</span><span class="dsa-topic">%(topic_upper)s</span></div>
<nav class="dsa-problem-nav"><a href="#definition">Problem</a><a href="#examples">Examples</a><a href="#intuition">Intuition</a><a href="#approach">Approach</a><a href="#solution">Java</a><a href="#analysis">Analysis</a></nav>
<section id="definition"><h2>1. Problem definition</h2>%(statement)s</section>
<section id="examples"><h2>2. Examples</h2>%(examples)s</section>
<section id="constraints"><h2>3. Constraints and assumptions</h2>%(constraints)s</section>
<section id="intuition"><h2>4. Intuition and key observation</h2><p>Start from the operations demanded by the problem: search, count, order, compare, connect, construct or optimize. Identify which information must be retained while processing the input and which repeated work can be avoided. Evaluate the implementation against the exact contract and constraints above.</p><div class="dsa-insight"><span class="dsa-insight-icon">💡</span><div><b>Key question</b><p>What invariant does the algorithm maintain, and why does each state transition preserve it?</p></div></div></section>
<section id="approach"><h2>5. Approach and implementation variants</h2>%(methods)s<h3>Step-by-step reading guide</h3>%(steps)s</section>
<section id="solution"><h2>6. Java implementation</h2><p>Complete original Java source, including helper methods and comments. Evaluate each public method separately; variants may have different time and space trade-offs.</p><p><b>Original source files:</b> %(source_links)s</p>%(source_blocks)s</section>
<section id="dry-run"><h2>7. Dry run and walkthrough</h2><p>Use the documented sample above. Trace the selected method line by line, recording indices/pointers, accumulated values, recursive state or data-structure contents. Check that the final state produces the documented output. Where the source has no sample, first define tests from the confirmed problem contract rather than inventing constraints.</p></section>
<section id="correctness"><h2>8. Correctness reasoning</h2><p>Define an invariant that is true before processing starts. Show that each loop iteration or recursive transition preserves it. At termination, connect the invariant to the required output. For recursion, justify the base case and show that every recursive branch makes progress toward it.</p></section>
<section id="analysis"><h2>9. Complexity analysis</h2><p>Use method-level annotations above when present, then verify them against the actual implementation. Count loop iterations, recursive calls, collection operations, sorting and preprocessing.</p><div class="dsa-complexity"><div><small>TIME</small><strong>Per-method analysis</strong><p>Derive from the exact variant; do not assume all methods in one class have the same complexity.</p></div><div><small>AUXILIARY SPACE</small><strong>Per-method analysis</strong><p>Count extra collections, arrays and recursion depth. State whether output space is excluded.</p></div></div></section>
<section id="edge-cases"><h2>10. Edge cases and common mistakes</h2><ul class="dsa-mistakes"><li>Empty and minimum-size inputs, if allowed.</li><li>Single-element input, duplicates and all-equal values.</li><li>Sorted, reverse-sorted and highly unbalanced inputs where relevant.</li><li>Negative values, zero, overflow and maximum constraints where relevant.</li><li>Null references, disconnected components, cycles or malformed structures where relevant.</li><li>Mutation, off-by-one errors and assumptions not enforced by the implementation.</li></ul></section>
<section id="interview"><h2>11. Interview follow-ups</h2><ul><li>Explain the invariant without referring to code.</li><li>What is the brute-force baseline and what repeated work is removed?</li><li>Which constraints make this implementation valid?</li><li>Can the auxiliary space or worst-case time be improved?</li><li>How would you test this against a brute-force oracle?</li></ul></section>
<p class="dsa-remember"><b>Revision checkpoint:</b> Restate the contract, explain the invariant, trace one example, justify correctness and derive complexity for the exact method.</p></article>
<div class="dsa-page-actions"><a href="../%(topic_slug)s.html">← Back to %(topic)s</a><a href="../../../search.html">Search the whole site</a></div>
</div></div></body></html>''' % {
        'problem': esc(problem_title), 'topic': esc(topic_title), 'topic_slug': topic_slug,
        'topic_upper': esc(topic_title.upper()), 'number': number, 'description': esc(description),
        'statement': statement_html, 'examples': examples_html, 'constraints': constraints_html,
        'methods': method_html, 'steps': steps_html, 'source_links': ' · '.join(source_links),
        'source_blocks': ''.join(source_blocks)
    }


def generate_dsa_topics():
    """Generate complete topic pages from the checked-out kowlutla/DSA source."""
    if not os.path.isdir(DSA_SOURCE):
        print('DSA source checkout not found; building the checked-in Strings prototype only.')
        return [('strings', 'Strings')], {'strings': [
            ('isomorphic-strings', 'Isomorphic Strings'),
            ('minimum-number-following-pattern', 'Minimum Number Following an I/D Pattern')
        ]}

    catalog = {}
    for slug, title, description, patterns in DSA_TOPIC_CONFIG:
        folder = os.path.join(DSA_SOURCE, slug)
        if slug == 'foundations':
            files = []
        else:
            if not os.path.isdir(folder):
                continue
            files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.java')]
        if slug == 'arrays':
            files = [p for p in files if os.path.basename(p) not in DSA_MATRIX_FILES]
        if slug == 'matrix':
            array_folder = os.path.join(DSA_SOURCE, 'arrays')
            files += [os.path.join(array_folder, f) for f in DSA_MATRIX_FILES
                      if os.path.isfile(os.path.join(array_folder, f))]
        files.sort(key=lambda p: [int(x) if x.isdigit() else x.lower()
                                  for x in re.split(r'(\d+)', os.path.basename(p))])
        grouped = {}
        for path in files:
            filename = os.path.basename(path)[:-5]
            base = re.sub(r'\\d+

        if slug == 'strings':
            continue  # The two Strings problems have individually authored teaching pages.

        cards = []
        for number, (problem_slug, problem_title, source_paths) in enumerate(catalog[slug], 1):
            source_files = [(read(path), os.path.relpath(path, DSA_SOURCE).replace(os.sep, '/')) for path in source_paths]
            source = source_files[0][0]
            rel_source = source_files[0][1]
            summary = dsa_source_summary(source, problem_title)
            source_links = ' · '.join('<a href="https://github.com/kowlutla/DSA/blob/main/src/com/dsa/%s"><code>%s</code></a>' % (rel.replace(' ', '%20'), esc(rel)) for _, rel in source_files)
            detail_dir = os.path.join(DSA, 'topics', slug)
            os.makedirs(detail_dir, exist_ok=True)
            detail_path = os.path.join(detail_dir, problem_slug + '.html')
            write(detail_path, dsa_problem_page(slug, title, number, problem_slug, problem_title, source_files))
            detail_href = slug + '/' + problem_slug + '.html'
            cards.append(
                '<article class="dsa-problem-card dsa-problem-summary" id="%s">'
                '<div class="dsa-card-head"><div><span class="dsa-number">%02d</span>'
                '<span class="dsa-topic">%s</span></div></div>'
                '<h3><a href="%s">%02d - %s</a></h3><p>%s</p>'
                '<p class="dsa-code-note"><b>Original source:</b> <a href="%s"><code>%s</code></a></p>'
                '<p><a href="%s">Open full problem page →</a></p></article>' %
                (problem_slug, number, esc(title.upper()), esc(detail_href), number,
                 esc(problem_title), esc(summary[:500]), source_url, esc(rel_source), esc(detail_href))
            )

        foundation_content = ''
        if slug == 'foundations':
            foundation_content = """<section class="dsa-section">
<h2>1. What DSA means</h2>
<p><b>Data structures</b> organize information; <b>algorithms</b> define the steps that transform it into an answer. Choose them together: the right structure makes the operations required by the algorithm efficient.</p>
<h2>2. A repeatable problem-solving workflow</h2>
<ol><li><b>Clarify the contract:</b> inputs, outputs, duplicates, ordering, mutation, null/empty cases and whether one or all answers are required.</li><li><b>Read the constraints:</b> estimate the largest input and rule out approaches that cannot finish in time or memory.</li><li><b>Build a correct baseline:</b> use a simple approach to understand the search space before optimizing.</li><li><b>Find repeated work:</b> look for rescans, recomputed prefixes, duplicate states and expensive membership checks.</li><li><b>Choose a pattern and data structure:</b> base the choice on required operations, not familiarity.</li><li><b>State an invariant:</b> explain what remains true after each iteration or recursive call.</li><li><b>Prove and test:</b> justify coverage and correctness, then test boundary cases and derive complexity.</li></ol>
<h2>3. Complexity analysis</h2>
<p>Big-O describes an asymptotic upper bound on growth; Big-Theta is a tight bound and Big-Omega is a lower bound. Ignore constants and lower-order terms when comparing growth, but keep input assumptions explicit.</p>
<table><thead><tr><th>Complexity</th><th>Typical example</th><th>Growth</th></tr></thead><tbody><tr><td><code>O(1)</code></td><td>Array access by index</td><td>Constant</td></tr><tr><td><code>O(log n)</code></td><td>Binary search</td><td>Problem size shrinks by a factor</td></tr><tr><td><code>O(n)</code></td><td>One traversal</td><td>Linear</td></tr><tr><td><code>O(n log n)</code></td><td>Efficient comparison sorting</td><td>Linear work across logarithmic levels</td></tr><tr><td><code>O(n²)</code></td><td>All pairs / nested scans</td><td>Quadratic</td></tr><tr><td><code>O(2ⁿ)</code></td><td>Enumerating subsets</td><td>Exponential</td></tr><tr><td><code>O(n!)</code></td><td>Enumerating permutations</td><td>Factorial</td></tr></tbody></table>
<p>Time complexity counts operations as input grows. Auxiliary space counts extra working memory, usually excluding input and required output. Include recursion call-stack space when it grows with input.</p>
<h2>4. Choosing a data structure</h2>
<table><thead><tr><th>Need</th><th>Typical choice</th><th>Reason</th></tr></thead><tbody><tr><td>Indexed sequential data</td><td>Array / ArrayList</td><td>Constant-time indexed reads</td></tr><tr><td>Average-case key lookup</td><td>HashMap / HashSet</td><td>Expected constant-time lookup</td></tr><tr><td>Last-in, first-out</td><td>Stack / Deque</td><td>Efficient operations at one end</td></tr><tr><td>First-in, first-out</td><td>Queue / Deque</td><td>Efficient operations at opposite ends</td></tr><tr><td>Repeated min/max extraction</td><td>PriorityQueue</td><td>Efficient access to the highest-priority item</td></tr><tr><td>Ordered neighbour queries</td><td>TreeMap / balanced tree</td><td>Maintains sorted keys</td></tr><tr><td>Relationships and connectivity</td><td>Graph adjacency list</td><td>Represents vertices and edges</td></tr></tbody></table>
<h2>5. Java correctness checks</h2>
<ul><li>Use <code>long</code> when sums, products or counts can exceed the <code>int</code> range; widen before multiplication.</li><li>Use <code>equals</code> for object-value equality; <code>==</code> compares primitive values or object references.</li><li>Java <code>char</code> is a UTF-16 code unit, not always a full Unicode code point.</li><li>Avoid subtraction-based comparators that can overflow; prefer <code>Integer.compare(a, b)</code>.</li><li>Recursive depth can overflow the Java call stack; consider iterative traversal for unbounded depth.</li><li>Check whether APIs mutate input and whether a map key is absent or mapped to a default value.</li></ul>
<h2>6. Correctness and edge-case checklist</h2>
<ul><li>Empty and single-element input</li><li>Duplicates, sorted and reverse-sorted input</li><li>Negative values and zero where allowed</li><li>Minimum and maximum constraint values</li><li>Disconnected graphs, cycles and unreachable nodes where relevant</li><li>Empty strings, repeated characters and Unicode where relevant</li><li>Overflow, off-by-one errors and invalid assumptions</li></ul>
<p class="dsa-remember"><b>Interview habit:</b> explain the invariant and why the data structure fits before walking through code.</p>
</section>"""
        page = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s | DSA Problem-Solving Handbook</title>
<meta name="description" content="%(description)s">
<link rel="stylesheet" href="../../handbook/assets/style.css">
<link rel="stylesheet" href="../../quicknotes/assets/quick.css">
<link rel="stylesheet" href="../assets/dsa.css">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="qn"><div id="dsa-page">
<nav class="dsa-breadcrumb" aria-label="Breadcrumb"><a href="../../index.html">Home</a><span>/</span><a href="../index.html">DSA</a><span>/</span><span aria-current="page">%(title)s</span></nav>
<header class="dsa-hero">
<p class="dsa-kicker">DATA STRUCTURES &amp; ALGORITHMS / JAVA</p>
<h1>%(title)s</h1><p class="sub">%(description)s</p>
<div class="dsa-meta"><span>%(count)d source entries</span><span>Java</span><span>%(level)s</span></div>
</header>
%(foundation_content)s
%(topic_guide)s
<section class="dsa-section">
<h2>How to study this topic</h2>
<p>Work through the problems in order. Before reading the implementation, restate the input contract and constraints. Then identify the key observation, explain why the chosen data structure fits, trace the important state, and derive the complexity from the actual operations.</p>
<h3>Patterns and concepts</h3><p>%(patterns)s</p>
<div class="dsa-callout"><b>For every problem:</b> Explain the invariant, test empty and boundary inputs, check integer and character constraints, and distinguish auxiliary space from output space. Do not assume a complexity claim without checking the loops and data-structure operations.</div>
</section>
<section class="dsa-section">
<h2>How to reason through a solution</h2>
<p>For each entry, identify the state that changes, the condition that advances the algorithm, and the point at which the result becomes final. Check whether the implementation mutates its input, relies on sorted data, assumes a restricted value range, or uses recursion depth proportional to the input.</p>
</section>
<section class="dsa-section">
<h2>Problem and implementation index</h2>
<p>This index includes every Java source file in the topic folder. Foundational node/stack/queue classes, demonstrations and alternative implementations are retained alongside interview problems so the source repository is fully represented.</p>
%(cards)s
</section>
<div class="dsa-page-actions"><a href="../index.html">← All DSA topics</a><a href="../../search.html">Search the whole site</a></div>
</div></div>
</body></html>''' % {
            'title': esc(title), 'description': esc(description), 'count': len(files),
            'level': 'Foundations' if slug in ('patterns','mathematical','arrays','strings','sorting') else 'Core to advanced',
            'patterns': esc(patterns), 'cards': ''.join(cards), 'foundation_content': foundation_content, 'topic_guide': DSA_TOPIC_GUIDES.get(slug, '')
        }
        write(os.path.join(DSA, 'topics', slug + '.html'), page)

    return [(slug, title) for slug, title, _, _ in DSA_TOPIC_CONFIG if slug in catalog], {
        slug: [(problem_slug, problem_title) for problem_slug, problem_title, _ in entries]
        for slug, entries in catalog.items()
    }

DSA_TOPICS, DSA_PROBLEMS = generate_dsa_topics()
DSA_TOPICS = [t for t in DSA_TOPICS if os.path.exists(os.path.join(DSA, 'topics', t[0] + '.html'))]
print('DSA build: %d topics, %d Java source entries' % (len(DSA_TOPICS), sum(len(v) for v in DSA_PROBLEMS.values())))
print('DSA build: %d topics, %d Java source entries' % (len(DSA_TOPICS), sum(len(v) for v in DSA_PROBLEMS.values())))

def dsa_nav(cur, pre, active_problem=None):
    """Use the same sidebar structure and shared classes as the Interview Book."""
    site = pre + '../'
    brand = ('<a class="brand" href="%sindex.html">Data Structures &amp; Algorithms</a>' % pre
             if cur or active_problem else
             '<div class="brand">Data Structures &amp; Algorithms</div>')
    o = [brand, '<div class="tagline">Java problem-solving handbook</div>',
         '<div class="qlinks"><a href="%sindex.html">🏠 Home</a><a href="%ssearch.html">🔍 Search the whole site</a></div>' % (site, site)]
    topic_groups = []
    for index, (slug, title) in enumerate(DSA_TOPICS, 1):
        problem_links = []
        for number, (problem_slug, problem_title) in enumerate(DSA_PROBLEMS.get(slug, []), 1):
            active = ' current' if active_problem == problem_slug else ''
            nested_page = os.path.join(DSA, 'topics', slug, problem_slug + '.html')
            href = pre + ('topics/%s/%s.html' % (slug, problem_slug)) if os.path.exists(nested_page) else pre + 'topics/%s.html#%s' % (slug, problem_slug)
            problem_links.append('<a class="ch%s" href="%s"><span class="num">%02d -</span><span>%s</span></a>' %
                                 (active, href, number, esc(problem_title)))
        is_open = ' open' if slug == cur else ''
        topic_groups.append('<details%s><summary>%02d %s</summary>%s</details>' %
                            (is_open, index, esc(title), ''.join(problem_links)))
    topics_open = ' open' if cur is None or cur in dict(DSA_TOPICS) else ''
    o.append('<details%s><summary>Topics</summary>%s</details>' % (topics_open, ''.join(topic_groups)))
    return ''.join(o)

dsa_stats = {}
for i, (slug, title) in enumerate(DSA_TOPICS):
    p = os.path.join(DSA, 'topics', slug + '.html')
    s = read(p)
    s = re.sub(r'<!--dnav:start-->.*?<!--dnav:end-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--dfoot:start-->.*?<!--dfoot:end-->\n?', '', s, flags=re.S)
    dsa_stats[slug] = dict(problems=len(re.findall(r'<article class="dsa-problem-card dsa-problem-summary"', s)),
                           diagrams=len(re.findall(r'<svg[^>]*viewBox', s)),
                           words=len(re.sub(r'<[^>]+>', ' ', s).split()), sub=sub_of(p))
    pager = ['<div class="pager">']
    if i > 0: pager.append('<a class="prev" href="%s.html"><span class="lbl">Previous</span>%s</a>' % (DSA_TOPICS[i-1][0], esc(DSA_TOPICS[i-1][1])))
    if i < len(DSA_TOPICS)-1: pager.append('<a class="next" href="%s.html"><span class="lbl">Next</span>%s</a>' % (DSA_TOPICS[i+1][0], esc(DSA_TOPICS[i+1][1])))
    pager.append('</div>')
    head = '<!--dnav:start-->\n<div class="layout">\n<nav class="toc" id="toc">\n%s\n</nav>\n<main class="qmain">\n<!--dnav:end-->\n' % dsa_nav(slug, '../')
    foot = '<!--dfoot:start-->\n%s\n</main>\n</div>\n<script src="../../quicknotes/assets/quick.js"></script>\n<!--dfoot:end-->\n' % ''.join(pager)
    s = s.replace('<div class="qn">', head + '<div class="qn">', 1).replace('</body>', foot + '</body>', 1)
    write(p, s)

# Individual, deeply authored problem pages remain separate from the generated source index.
dsa_problem_count = 0
for topic_slug, problems in DSA_PROBLEMS.items():
    for index, (problem_slug, problem_title) in enumerate(problems):
        p = os.path.join(DSA, 'topics', topic_slug, problem_slug + '.html')
        if not os.path.exists(p):
            continue
        s = read(p)
        s = re.sub(r'<!--dnav:start-->.*?<!--dnav:end-->\n?', '', s, flags=re.S)
        s = re.sub(r'<!--dfoot:start-->.*?<!--dfoot:end-->\n?', '', s, flags=re.S)
        pager = ['<div class="pager">']
        if index > 0:
            prev_slug, prev_title = problems[index - 1]
            pager.append('<a class="prev" href="%s.html"><span class="lbl">Previous problem</span>%s</a>' % (prev_slug, esc(prev_title)))
        if index < len(problems) - 1:
            next_slug, next_title = problems[index + 1]
            pager.append('<a class="next" href="%s.html"><span class="lbl">Next problem</span>%s</a>' % (next_slug, esc(next_title)))
        pager.append('</div>')
        head = '<!--dnav:start-->\n<div class="layout">\n<nav class="toc" id="toc">\n%s\n</nav>\n<main class="qmain">\n<!--dnav:end-->\n' % dsa_nav(topic_slug, '../../', problem_slug)
        foot = '<!--dfoot:start-->\n%s\n</main>\n</div>\n<script src="../../../quicknotes/assets/quick.js"></script>\n<!--dfoot:end-->\n' % ''.join(pager)
        s = s.replace('<div class="qn">', head + '<div class="qn">', 1).replace('</body>', foot + '</body>', 1)
        write(p, s)
        dsa_problem_count += 1

dsa_problems = sum(v['problems'] for v in dsa_stats.values())
dsa_diagrams = sum(v['diagrams'] for v in dsa_stats.values())
dsa_cards = '\n'.join('<a class="card" href="topics/%s.html"><span class="n">Topic %02d</span><span class="t">%s</span><span class="d">%s</span><span class="d">%d source entries, %d diagrams</span></a>' %
                         (slug, i+1, esc(title), esc(dsa_stats[slug]['sub']), dsa_stats[slug]['problems'], dsa_stats[slug]['diagrams'])
                         for i, (slug, title) in enumerate(DSA_TOPICS))
dsa_index = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Data Structures and Algorithms | DSA</title>
<link rel="stylesheet" href="../handbook/assets/style.css">
<link rel="stylesheet" href="../quicknotes/assets/quick.css">
<link rel="stylesheet" href="assets/dsa.css">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="layout">
<nav class="toc" id="toc">%(nav)s</nav>
<main class="qmain">
<div class="qn qhome">
<h1>Data Structures and Algorithms</h1>
<p class="sub">A complete Java DSA learning path, from programming-pattern fundamentals to advanced graph and dynamic-programming problems. Each topic contains the source implementations from the DSA repository.</p>
<div class="stats"><div class="stat"><b>%(nt)d</b><span>topics</span></div><div class="stat"><b>%(np)d</b><span>source entries</span></div></div>
<div class="tl"><b>How to use this section:</b> Follow the numbered topics in order. Study the concept and problem statement first, attempt the solution, then inspect the original Java implementation and derive its invariant and complexity.</div>
<div class="grid">%(cards)s</div>
<p><a href="../index.html">Home</a> · <a href="../search.html">Search the whole site</a></p>
</div>
</main>
</div>
<script src="../quicknotes/assets/quick.js"></script>
</body>
</html>
''' % dict(nav=dsa_nav(None, ''), nt=len(DSA_TOPICS), np=dsa_problems, cards=dsa_cards)
write(os.path.join(DSA, 'index.html'), dsa_index)


# ---------------- index.html ----------------
hb = read(os.path.join(ROOT, 'handbook', 'assets', 'chapters.js'))
n_pages = len(re.findall(r'done: true', hb))
hand_words = 0
for sub in ('chapters', 'case-studies', 'cheatsheets'):
    d = os.path.join(ROOT, 'handbook', sub)
    for f in os.listdir(d):
        if f.endswith('.html'): hand_words += len(re.sub(r'<[^>]+>', ' ', read(os.path.join(d, f))).split())

top = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interview Prep: System Design and Core Topics</title>
<link rel="stylesheet" href="handbook/assets/style.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
  .top { max-width: 1000px; margin: 0 auto; padding: 56px 24px 90px; }
  .top h1 { font-size: 2.8rem; margin: 0 0 8px; }
  .top .lead { color: var(--muted); font-size: 1.1rem; max-width: 720px; }
  .two2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px; margin: 34px 0; }
  .big { display: block; border: 1px solid var(--line); background: var(--card); border-radius: 16px; padding: 26px 28px; text-decoration: none; color: var(--fg); }
  .big:hover { border-color: var(--accent); background: var(--accent-soft); }
  .big .k { color: var(--accent); font-weight: 700; font-size: 13px; letter-spacing: .08em; text-transform: uppercase; }
  .big .t { display: block; font-size: 1.5rem; font-weight: 700; margin: 6px 0 8px; }
  .big .d { color: var(--muted); display: block; line-height: 1.55; }
  .big .m { display: block; margin-top: 14px; font-size: 14px; color: var(--fg); }
  .how { border-left: 4px solid var(--accent); background: var(--accent-soft); border-radius: 6px; padding: 12px 18px; margin: 10px 0 26px; }
  .quick a { display: inline-block; margin: 4px 10px 4px 0; padding: 4px 14px; border: 1px solid var(--line); border-radius: 20px; text-decoration: none; background: var(--card); }
  .quick a:hover { border-color: var(--accent); }
</style>
</head>
<body>
<div class="top">
<h1>Interview Prep</h1>
<p class="lead">One place to prepare for senior engineering interviews. Start with <b>System Design</b> (learn it in the Handbook, revise it in the Quick Notes), then practise topic by topic in the <b>Interview Book</b>: Git, Java, Spring, Kafka and more.</p>
<h2>System Design</h2>
<div class="two2">
<a class="big" href="handbook/index.html"><span class="k">Learn</span><span class="t">System Design Handbook</span><span class="d">Complete, from the ground up: every component in depth, microservices, %(nc)d worked case studies, and cheat sheets. Detailed prose with diagrams.</span><span class="m">%(np)d pages, about %(hw)dk words</span></a>
<a class="big" href="quicknotes/index.html"><span class="k">Revise</span><span class="t">System Design Quick Notes</span><span class="d">Lookup sheets for the day before: key definitions, tables, numbers, say-aloud scripts, diagrams and detailed interview Q&amp;A in plain words.</span><span class="m">%(nm)d study sheets, %(nc)d case sheets, %(tq)d Q&amp;As</span></a>
</div>
<h2>Interview Book</h2>
<div class="two2">
%(ivcard)s
</div>
<h2>DSA</h2>
<div class="two2">
%(dsacard)s
</div>
<div class="how"><b>Suggested use:</b> for system design, read the Handbook chapter first, then the matching Quick Notes sheet to lock it in; in the final two days read only the Quick Notes. For everything else, work through the Interview Book topic by topic: answer each question out loud before you open it.</div>
<h2>Jump straight to</h2>
<div class="quick">
<a href="quicknotes/notes/q13-delivery-playbook.html">Last-hour cheat sheet</a>
<a href="quicknotes/notes/q01-framework-estimation.html">Framework and estimation</a>
<a href="handbook/cheatsheets/cs-numbers.html">Numbers to remember</a>
<a href="handbook/cheatsheets/cs-decision-tables.html">Decision tables</a>
<a href="quicknotes/index.html#cases">All case sheets</a>
<a href="handbook/index.html">Handbook contents</a>
<a href="search.html">Search</a>
<a href="handbook/reference/ref-glossary.html">Glossary A-Z</a>
</div>
</div>
</body>
</html>
''' % dict(np=n_pages, hw=round(hand_words / 1000), nm=len(mods), nc=len(cases), tq=tq,
    ivcard=('<a class="big" href="interview/index.html"><span class="k">Practise</span><span class="t">Interview Book</span><span class="d">Interview questions topic by topic (Git, Java, Spring, Kafka and more) with model answers, diagrams, follow-ups and real production scenarios.</span><span class="m">%d topics, %d questions</span></a>' % (len(mods), iv_q)) if INT_TOPICS else '',
    dsacard=('<a class="big" href="dsa/index.html"><span class="k">Practise</span><span class="t">Data Structures and Algorithms</span><span class="d">Java coding problems organized by topic and pattern, with intuition, optimized solutions, dry runs and complexity analysis.</span><span class="m">%d topic pages, %d problems</span></a>' % (len(DSA_TOPICS), dsa_problems)) if DSA_TOPICS else '')
write(os.path.join(ROOT, 'index.html'), top)
print('built: %d quicknotes pages, %d words, %d Q&As, %d diagrams; handbook %d pages' % (len(items), tw, tq, ts, n_pages))
, '', filename)
            grouped.setdefault(base, []).append(path)
        catalog[slug] = []
        for base, paths in grouped.items():
            # Numbered suffixes such as Solution1/Solution2 are alternate implementations
            # of one problem; keep them together on one problem page.
            display_name = base if len(paths) > 1 else os.path.basename(paths[0])[:-5]
            catalog[slug].append((dsa_slug(display_name), dsa_title(display_name), paths))
        if slug == 'strings':
            catalog[slug] = [
                ('isomorphic-strings', 'Isomorphic Strings', [os.path.join(folder, 'IsomorphicStrings.java')]),
                ('minimum-number-following-pattern', 'Minimum Number Following an I/D Pattern', [os.path.join(folder, 'NumberFollowingAPattern.java')])
            ]

        if slug == 'strings':
            continue  # The two Strings problems have individually authored teaching pages.

        cards = []
        for number, (problem_slug, problem_title, source_path) in enumerate(catalog[slug], 1):
            source = read(source_path)
            rel_source = os.path.relpath(source_path, DSA_SOURCE).replace(os.sep, '/')
            summary = dsa_source_summary(source, problem_title)
            source_url = 'https://github.com/kowlutla/DSA/blob/main/src/com/dsa/' + rel_source.replace(' ', '%20')
            detail_dir = os.path.join(DSA, 'topics', slug)
            os.makedirs(detail_dir, exist_ok=True)
            detail_path = os.path.join(detail_dir, problem_slug + '.html')
            write(detail_path, dsa_problem_page(slug, title, number, problem_slug, problem_title, source, rel_source))
            detail_href = slug + '/' + problem_slug + '.html'
            cards.append(
                '<article class="dsa-problem-card dsa-problem-summary" id="%s">'
                '<div class="dsa-card-head"><div><span class="dsa-number">%02d</span>'
                '<span class="dsa-topic">%s</span></div></div>'
                '<h3><a href="%s">%02d - %s</a></h3><p>%s</p>'
                '<p class="dsa-code-note"><b>Original source:</b> <a href="%s"><code>%s</code></a></p>'
                '<p><a href="%s">Open full problem page →</a></p></article>' %
                (problem_slug, number, esc(title.upper()), esc(detail_href), number,
                 esc(problem_title), esc(summary[:500]), source_url, esc(rel_source), esc(detail_href))
            )

        foundation_content = ''
        if slug == 'foundations':
            foundation_content = """<section class="dsa-section">
<h2>1. What DSA means</h2>
<p><b>Data structures</b> organize information; <b>algorithms</b> define the steps that transform it into an answer. Choose them together: the right structure makes the operations required by the algorithm efficient.</p>
<h2>2. A repeatable problem-solving workflow</h2>
<ol><li><b>Clarify the contract:</b> inputs, outputs, duplicates, ordering, mutation, null/empty cases and whether one or all answers are required.</li><li><b>Read the constraints:</b> estimate the largest input and rule out approaches that cannot finish in time or memory.</li><li><b>Build a correct baseline:</b> use a simple approach to understand the search space before optimizing.</li><li><b>Find repeated work:</b> look for rescans, recomputed prefixes, duplicate states and expensive membership checks.</li><li><b>Choose a pattern and data structure:</b> base the choice on required operations, not familiarity.</li><li><b>State an invariant:</b> explain what remains true after each iteration or recursive call.</li><li><b>Prove and test:</b> justify coverage and correctness, then test boundary cases and derive complexity.</li></ol>
<h2>3. Complexity analysis</h2>
<p>Big-O describes an asymptotic upper bound on growth; Big-Theta is a tight bound and Big-Omega is a lower bound. Ignore constants and lower-order terms when comparing growth, but keep input assumptions explicit.</p>
<table><thead><tr><th>Complexity</th><th>Typical example</th><th>Growth</th></tr></thead><tbody><tr><td><code>O(1)</code></td><td>Array access by index</td><td>Constant</td></tr><tr><td><code>O(log n)</code></td><td>Binary search</td><td>Problem size shrinks by a factor</td></tr><tr><td><code>O(n)</code></td><td>One traversal</td><td>Linear</td></tr><tr><td><code>O(n log n)</code></td><td>Efficient comparison sorting</td><td>Linear work across logarithmic levels</td></tr><tr><td><code>O(n²)</code></td><td>All pairs / nested scans</td><td>Quadratic</td></tr><tr><td><code>O(2ⁿ)</code></td><td>Enumerating subsets</td><td>Exponential</td></tr><tr><td><code>O(n!)</code></td><td>Enumerating permutations</td><td>Factorial</td></tr></tbody></table>
<p>Time complexity counts operations as input grows. Auxiliary space counts extra working memory, usually excluding input and required output. Include recursion call-stack space when it grows with input.</p>
<h2>4. Choosing a data structure</h2>
<table><thead><tr><th>Need</th><th>Typical choice</th><th>Reason</th></tr></thead><tbody><tr><td>Indexed sequential data</td><td>Array / ArrayList</td><td>Constant-time indexed reads</td></tr><tr><td>Average-case key lookup</td><td>HashMap / HashSet</td><td>Expected constant-time lookup</td></tr><tr><td>Last-in, first-out</td><td>Stack / Deque</td><td>Efficient operations at one end</td></tr><tr><td>First-in, first-out</td><td>Queue / Deque</td><td>Efficient operations at opposite ends</td></tr><tr><td>Repeated min/max extraction</td><td>PriorityQueue</td><td>Efficient access to the highest-priority item</td></tr><tr><td>Ordered neighbour queries</td><td>TreeMap / balanced tree</td><td>Maintains sorted keys</td></tr><tr><td>Relationships and connectivity</td><td>Graph adjacency list</td><td>Represents vertices and edges</td></tr></tbody></table>
<h2>5. Java correctness checks</h2>
<ul><li>Use <code>long</code> when sums, products or counts can exceed the <code>int</code> range; widen before multiplication.</li><li>Use <code>equals</code> for object-value equality; <code>==</code> compares primitive values or object references.</li><li>Java <code>char</code> is a UTF-16 code unit, not always a full Unicode code point.</li><li>Avoid subtraction-based comparators that can overflow; prefer <code>Integer.compare(a, b)</code>.</li><li>Recursive depth can overflow the Java call stack; consider iterative traversal for unbounded depth.</li><li>Check whether APIs mutate input and whether a map key is absent or mapped to a default value.</li></ul>
<h2>6. Correctness and edge-case checklist</h2>
<ul><li>Empty and single-element input</li><li>Duplicates, sorted and reverse-sorted input</li><li>Negative values and zero where allowed</li><li>Minimum and maximum constraint values</li><li>Disconnected graphs, cycles and unreachable nodes where relevant</li><li>Empty strings, repeated characters and Unicode where relevant</li><li>Overflow, off-by-one errors and invalid assumptions</li></ul>
<p class="dsa-remember"><b>Interview habit:</b> explain the invariant and why the data structure fits before walking through code.</p>
</section>"""
        page = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s | DSA Problem-Solving Handbook</title>
<meta name="description" content="%(description)s">
<link rel="stylesheet" href="../../handbook/assets/style.css">
<link rel="stylesheet" href="../../quicknotes/assets/quick.css">
<link rel="stylesheet" href="../assets/dsa.css">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="qn"><div id="dsa-page">
<nav class="dsa-breadcrumb" aria-label="Breadcrumb"><a href="../../index.html">Home</a><span>/</span><a href="../index.html">DSA</a><span>/</span><span aria-current="page">%(title)s</span></nav>
<header class="dsa-hero">
<p class="dsa-kicker">DATA STRUCTURES &amp; ALGORITHMS / JAVA</p>
<h1>%(title)s</h1><p class="sub">%(description)s</p>
<div class="dsa-meta"><span>%(count)d source entries</span><span>Java</span><span>%(level)s</span></div>
</header>
%(foundation_content)s
%(topic_guide)s
<section class="dsa-section">
<h2>How to study this topic</h2>
<p>Work through the problems in order. Before reading the implementation, restate the input contract and constraints. Then identify the key observation, explain why the chosen data structure fits, trace the important state, and derive the complexity from the actual operations.</p>
<h3>Patterns and concepts</h3><p>%(patterns)s</p>
<div class="dsa-callout"><b>For every problem:</b> Explain the invariant, test empty and boundary inputs, check integer and character constraints, and distinguish auxiliary space from output space. Do not assume a complexity claim without checking the loops and data-structure operations.</div>
</section>
<section class="dsa-section">
<h2>How to reason through a solution</h2>
<p>For each entry, identify the state that changes, the condition that advances the algorithm, and the point at which the result becomes final. Check whether the implementation mutates its input, relies on sorted data, assumes a restricted value range, or uses recursion depth proportional to the input.</p>
</section>
<section class="dsa-section">
<h2>Problem and implementation index</h2>
<p>This index includes every Java source file in the topic folder. Foundational node/stack/queue classes, demonstrations and alternative implementations are retained alongside interview problems so the source repository is fully represented.</p>
%(cards)s
</section>
<div class="dsa-page-actions"><a href="../index.html">← All DSA topics</a><a href="../../search.html">Search the whole site</a></div>
</div></div>
</body></html>''' % {
            'title': esc(title), 'description': esc(description), 'count': len(files),
            'level': 'Foundations' if slug in ('patterns','mathematical','arrays','strings','sorting') else 'Core to advanced',
            'patterns': esc(patterns), 'cards': ''.join(cards), 'foundation_content': foundation_content, 'topic_guide': DSA_TOPIC_GUIDES.get(slug, '')
        }
        write(os.path.join(DSA, 'topics', slug + '.html'), page)

    return [(slug, title) for slug, title, _, _ in DSA_TOPIC_CONFIG if slug in catalog], {
        slug: [(problem_slug, problem_title) for problem_slug, problem_title, _ in entries]
        for slug, entries in catalog.items()
    }

DSA_TOPICS, DSA_PROBLEMS = generate_dsa_topics()
DSA_TOPICS = [t for t in DSA_TOPICS if os.path.exists(os.path.join(DSA, 'topics', t[0] + '.html'))]
print('DSA build: %d topics, %d Java source entries' % (len(DSA_TOPICS), sum(len(v) for v in DSA_PROBLEMS.values())))
print('DSA build: %d topics, %d Java source entries' % (len(DSA_TOPICS), sum(len(v) for v in DSA_PROBLEMS.values())))

def dsa_nav(cur, pre, active_problem=None):
    """Use the same sidebar structure and shared classes as the Interview Book."""
    site = pre + '../'
    brand = ('<a class="brand" href="%sindex.html">Data Structures &amp; Algorithms</a>' % pre
             if cur or active_problem else
             '<div class="brand">Data Structures &amp; Algorithms</div>')
    o = [brand, '<div class="tagline">Java problem-solving handbook</div>',
         '<div class="qlinks"><a href="%sindex.html">🏠 Home</a><a href="%ssearch.html">🔍 Search the whole site</a></div>' % (site, site)]
    topic_groups = []
    for index, (slug, title) in enumerate(DSA_TOPICS, 1):
        problem_links = []
        for number, (problem_slug, problem_title) in enumerate(DSA_PROBLEMS.get(slug, []), 1):
            active = ' current' if active_problem == problem_slug else ''
            nested_page = os.path.join(DSA, 'topics', slug, problem_slug + '.html')
            href = pre + ('topics/%s/%s.html' % (slug, problem_slug)) if os.path.exists(nested_page) else pre + 'topics/%s.html#%s' % (slug, problem_slug)
            problem_links.append('<a class="ch%s" href="%s"><span class="num">%02d -</span><span>%s</span></a>' %
                                 (active, href, number, esc(problem_title)))
        is_open = ' open' if slug == cur else ''
        topic_groups.append('<details%s><summary>%02d %s</summary>%s</details>' %
                            (is_open, index, esc(title), ''.join(problem_links)))
    topics_open = ' open' if cur is None or cur in dict(DSA_TOPICS) else ''
    o.append('<details%s><summary>Topics</summary>%s</details>' % (topics_open, ''.join(topic_groups)))
    return ''.join(o)

dsa_stats = {}
for i, (slug, title) in enumerate(DSA_TOPICS):
    p = os.path.join(DSA, 'topics', slug + '.html')
    s = read(p)
    s = re.sub(r'<!--dnav:start-->.*?<!--dnav:end-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--dfoot:start-->.*?<!--dfoot:end-->\n?', '', s, flags=re.S)
    dsa_stats[slug] = dict(problems=len(re.findall(r'<article class="dsa-problem-card dsa-problem-summary"', s)),
                           diagrams=len(re.findall(r'<svg[^>]*viewBox', s)),
                           words=len(re.sub(r'<[^>]+>', ' ', s).split()), sub=sub_of(p))
    pager = ['<div class="pager">']
    if i > 0: pager.append('<a class="prev" href="%s.html"><span class="lbl">Previous</span>%s</a>' % (DSA_TOPICS[i-1][0], esc(DSA_TOPICS[i-1][1])))
    if i < len(DSA_TOPICS)-1: pager.append('<a class="next" href="%s.html"><span class="lbl">Next</span>%s</a>' % (DSA_TOPICS[i+1][0], esc(DSA_TOPICS[i+1][1])))
    pager.append('</div>')
    head = '<!--dnav:start-->\n<div class="layout">\n<nav class="toc" id="toc">\n%s\n</nav>\n<main class="qmain">\n<!--dnav:end-->\n' % dsa_nav(slug, '../')
    foot = '<!--dfoot:start-->\n%s\n</main>\n</div>\n<script src="../../quicknotes/assets/quick.js"></script>\n<!--dfoot:end-->\n' % ''.join(pager)
    s = s.replace('<div class="qn">', head + '<div class="qn">', 1).replace('</body>', foot + '</body>', 1)
    write(p, s)

# Individual, deeply authored problem pages remain separate from the generated source index.
dsa_problem_count = 0
for topic_slug, problems in DSA_PROBLEMS.items():
    for index, (problem_slug, problem_title) in enumerate(problems):
        p = os.path.join(DSA, 'topics', topic_slug, problem_slug + '.html')
        if not os.path.exists(p):
            continue
        s = read(p)
        s = re.sub(r'<!--dnav:start-->.*?<!--dnav:end-->\n?', '', s, flags=re.S)
        s = re.sub(r'<!--dfoot:start-->.*?<!--dfoot:end-->\n?', '', s, flags=re.S)
        pager = ['<div class="pager">']
        if index > 0:
            prev_slug, prev_title = problems[index - 1]
            pager.append('<a class="prev" href="%s.html"><span class="lbl">Previous problem</span>%s</a>' % (prev_slug, esc(prev_title)))
        if index < len(problems) - 1:
            next_slug, next_title = problems[index + 1]
            pager.append('<a class="next" href="%s.html"><span class="lbl">Next problem</span>%s</a>' % (next_slug, esc(next_title)))
        pager.append('</div>')
        head = '<!--dnav:start-->\n<div class="layout">\n<nav class="toc" id="toc">\n%s\n</nav>\n<main class="qmain">\n<!--dnav:end-->\n' % dsa_nav(topic_slug, '../../', problem_slug)
        foot = '<!--dfoot:start-->\n%s\n</main>\n</div>\n<script src="../../../quicknotes/assets/quick.js"></script>\n<!--dfoot:end-->\n' % ''.join(pager)
        s = s.replace('<div class="qn">', head + '<div class="qn">', 1).replace('</body>', foot + '</body>', 1)
        write(p, s)
        dsa_problem_count += 1

dsa_problems = sum(v['problems'] for v in dsa_stats.values())
dsa_diagrams = sum(v['diagrams'] for v in dsa_stats.values())
dsa_cards = '\n'.join('<a class="card" href="topics/%s.html"><span class="n">Topic %02d</span><span class="t">%s</span><span class="d">%s</span><span class="d">%d source entries, %d diagrams</span></a>' %
                         (slug, i+1, esc(title), esc(dsa_stats[slug]['sub']), dsa_stats[slug]['problems'], dsa_stats[slug]['diagrams'])
                         for i, (slug, title) in enumerate(DSA_TOPICS))
dsa_index = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Data Structures and Algorithms | DSA</title>
<link rel="stylesheet" href="../handbook/assets/style.css">
<link rel="stylesheet" href="../quicknotes/assets/quick.css">
<link rel="stylesheet" href="assets/dsa.css">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="layout">
<nav class="toc" id="toc">%(nav)s</nav>
<main class="qmain">
<div class="qn qhome">
<h1>Data Structures and Algorithms</h1>
<p class="sub">A complete Java DSA learning path, from programming-pattern fundamentals to advanced graph and dynamic-programming problems. Each topic contains the source implementations from the DSA repository.</p>
<div class="stats"><div class="stat"><b>%(nt)d</b><span>topics</span></div><div class="stat"><b>%(np)d</b><span>source entries</span></div></div>
<div class="tl"><b>How to use this section:</b> Follow the numbered topics in order. Study the concept and problem statement first, attempt the solution, then inspect the original Java implementation and derive its invariant and complexity.</div>
<div class="grid">%(cards)s</div>
<p><a href="../index.html">Home</a> · <a href="../search.html">Search the whole site</a></p>
</div>
</main>
</div>
<script src="../quicknotes/assets/quick.js"></script>
</body>
</html>
''' % dict(nav=dsa_nav(None, ''), nt=len(DSA_TOPICS), np=dsa_problems, cards=dsa_cards)
write(os.path.join(DSA, 'index.html'), dsa_index)


# ---------------- index.html ----------------
hb = read(os.path.join(ROOT, 'handbook', 'assets', 'chapters.js'))
n_pages = len(re.findall(r'done: true', hb))
hand_words = 0
for sub in ('chapters', 'case-studies', 'cheatsheets'):
    d = os.path.join(ROOT, 'handbook', sub)
    for f in os.listdir(d):
        if f.endswith('.html'): hand_words += len(re.sub(r'<[^>]+>', ' ', read(os.path.join(d, f))).split())

top = '''<!DOCTYPE html>
<html lang="en">
<head>
<script src="theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interview Prep: System Design and Core Topics</title>
<link rel="stylesheet" href="handbook/assets/style.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
  .top { max-width: 1000px; margin: 0 auto; padding: 56px 24px 90px; }
  .top h1 { font-size: 2.8rem; margin: 0 0 8px; }
  .top .lead { color: var(--muted); font-size: 1.1rem; max-width: 720px; }
  .two2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px; margin: 34px 0; }
  .big { display: block; border: 1px solid var(--line); background: var(--card); border-radius: 16px; padding: 26px 28px; text-decoration: none; color: var(--fg); }
  .big:hover { border-color: var(--accent); background: var(--accent-soft); }
  .big .k { color: var(--accent); font-weight: 700; font-size: 13px; letter-spacing: .08em; text-transform: uppercase; }
  .big .t { display: block; font-size: 1.5rem; font-weight: 700; margin: 6px 0 8px; }
  .big .d { color: var(--muted); display: block; line-height: 1.55; }
  .big .m { display: block; margin-top: 14px; font-size: 14px; color: var(--fg); }
  .how { border-left: 4px solid var(--accent); background: var(--accent-soft); border-radius: 6px; padding: 12px 18px; margin: 10px 0 26px; }
  .quick a { display: inline-block; margin: 4px 10px 4px 0; padding: 4px 14px; border: 1px solid var(--line); border-radius: 20px; text-decoration: none; background: var(--card); }
  .quick a:hover { border-color: var(--accent); }
</style>
</head>
<body>
<div class="top">
<h1>Interview Prep</h1>
<p class="lead">One place to prepare for senior engineering interviews. Start with <b>System Design</b> (learn it in the Handbook, revise it in the Quick Notes), then practise topic by topic in the <b>Interview Book</b>: Git, Java, Spring, Kafka and more.</p>
<h2>System Design</h2>
<div class="two2">
<a class="big" href="handbook/index.html"><span class="k">Learn</span><span class="t">System Design Handbook</span><span class="d">Complete, from the ground up: every component in depth, microservices, %(nc)d worked case studies, and cheat sheets. Detailed prose with diagrams.</span><span class="m">%(np)d pages, about %(hw)dk words</span></a>
<a class="big" href="quicknotes/index.html"><span class="k">Revise</span><span class="t">System Design Quick Notes</span><span class="d">Lookup sheets for the day before: key definitions, tables, numbers, say-aloud scripts, diagrams and detailed interview Q&amp;A in plain words.</span><span class="m">%(nm)d study sheets, %(nc)d case sheets, %(tq)d Q&amp;As</span></a>
</div>
<h2>Interview Book</h2>
<div class="two2">
%(ivcard)s
</div>
<h2>DSA</h2>
<div class="two2">
%(dsacard)s
</div>
<div class="how"><b>Suggested use:</b> for system design, read the Handbook chapter first, then the matching Quick Notes sheet to lock it in; in the final two days read only the Quick Notes. For everything else, work through the Interview Book topic by topic: answer each question out loud before you open it.</div>
<h2>Jump straight to</h2>
<div class="quick">
<a href="quicknotes/notes/q13-delivery-playbook.html">Last-hour cheat sheet</a>
<a href="quicknotes/notes/q01-framework-estimation.html">Framework and estimation</a>
<a href="handbook/cheatsheets/cs-numbers.html">Numbers to remember</a>
<a href="handbook/cheatsheets/cs-decision-tables.html">Decision tables</a>
<a href="quicknotes/index.html#cases">All case sheets</a>
<a href="handbook/index.html">Handbook contents</a>
<a href="search.html">Search</a>
<a href="handbook/reference/ref-glossary.html">Glossary A-Z</a>
</div>
</div>
</body>
</html>
''' % dict(np=n_pages, hw=round(hand_words / 1000), nm=len(mods), nc=len(cases), tq=tq,
    ivcard=('<a class="big" href="interview/index.html"><span class="k">Practise</span><span class="t">Interview Book</span><span class="d">Interview questions topic by topic (Git, Java, Spring, Kafka and more) with model answers, diagrams, follow-ups and real production scenarios.</span><span class="m">%d topics, %d questions</span></a>' % (len(mods), iv_q)) if INT_TOPICS else '',
    dsacard=('<a class="big" href="dsa/index.html"><span class="k">Practise</span><span class="t">Data Structures and Algorithms</span><span class="d">Java coding problems organized by topic and pattern, with intuition, optimized solutions, dry runs and complexity analysis.</span><span class="m">%d topic pages, %d problems</span></a>' % (len(DSA_TOPICS), dsa_problems)) if DSA_TOPICS else '')
write(os.path.join(ROOT, 'index.html'), top)
print('built: %d quicknotes pages, %d words, %d Q&As, %d diagrams; handbook %d pages' % (len(items), tw, tq, ts, n_pages))
