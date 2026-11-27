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
    for source_text, source_rel in source_files:
        for m in method_pattern.finditer(source_text):
            if m.group(2) == 'main': continue
            prefix = source_text[max(0, m.start() - 1000):m.start()]
            candidate = prefix[prefix.rfind('/**'):] if '/**' in prefix else ''
            doc_text = candidate.split(close_comment, 1)[0] if close_comment in candidate and not candidate.split(close_comment, 1)[1].strip() else ''
            desc = []
            for line in doc_text.splitlines():
                line = re.sub(r'^\s*\* ?', '', line).strip()
                if line and not line.startswith('@') and not re.search(r'(time|space) complexity', line, re.I):
                    desc.append(line)
            complexity = '; '.join(re.findall(r'(?i)(?:time|space)\s+complexity\s*:\s*[^*]+', doc_text))
            methods.append((source_rel, m.group(2), re.sub(r'\s+', ' ', m.group(1)).strip(), ' '.join(desc), complexity))
    statement_html = ''.join('<p>%s</p>' % esc(x) for x in statement) or '<p>The source file does not include a formal problem statement. This page documents the class as a supporting implementation; add the original problem contract before treating it as a standalone interview question.</p>'
    examples_html = '<pre class="dsa-code"><code>%s</code></pre>' % esc('\n'.join(examples)) if examples else '<p>No canonical sample is documented in the source. Confirm the external problem contract and create representative tests before relying on assumptions.</p>'
    constraints_html = '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in constraints) if constraints else '<p>Explicit constraints are not documented in the source file. Confirm the allowed input size, value range, nullability and mutation rules before finalizing the solution.</p>'
    method_html = ''.join('<article class="dsa-approach"><h3>Implementation %02d — <code>%s</code></h3><p class="dsa-code-note">Source: <code>%s</code></p><p><code>%s</code></p><p>%s</p><p><b>Source complexity note:</b> %s</p></article>' % (i, esc(x[1]), esc(x[0]), esc(x[2]), esc(x[3] or 'No method-level explanation is documented.'), esc(x[4] or 'No complexity annotation is documented; derive it from the implementation.')) for i,x in enumerate(methods,1))
    if not method_html: method_html = '<p>No public method was detected. Review the constructors and public API below.</p>'
    topic_reasoning = DSA_TOPIC_GUIDES.get(topic_slug, '')
    trace_guide, proof_guide, edge_guide = DSA_TOPIC_TRACE_GUIDES.get(topic_slug, ('', '', ''))
    problem_notes = DSA_PROBLEM_NOTES.get(problem_slug, {})
    comments = []
    for x in re.findall(r'//\s*(.+)', all_source):
        x = re.sub(r'\s+', ' ', x).strip()
        if len(x) > 12 and x not in comments: comments.append(x)
        if len(comments) >= 7: break
    steps_html = '<ol>%s</ol>' % ''.join('<li>%s</li>' % esc(x) for x in comments) if comments else '<ol><li>Identify the input state and required output.</li><li>Trace the main loop or recursive state.</li><li>Explain the condition that advances the state and the termination condition.</li><li>Verify that every valid case is considered exactly as required.</li></ol>'
    steps_html = problem_notes.get('steps', steps_html)
    intuition_html = problem_notes.get('intuition', '<p>Identify the information the algorithm must retain, the repeated work it avoids, and the invariant it maintains.</p>' + topic_reasoning)
    trace_html = problem_notes.get('trace', '<p>Use the documented sample above. Trace the selected method line by line and compare the final state with the expected output.</p>' + trace_guide)
    proof_html = problem_notes.get('proof', '<p>Define an invariant before processing. Show that every transition preserves it and that the termination condition implies the required output.</p>' + proof_guide)
    complexity_html = problem_notes.get('complexity', '<p>Derive time and auxiliary space separately for each implementation variant. Count loop iterations, recursive calls, collection operations, preprocessing and output storage.</p>')
    edge_html = problem_notes.get('edge', edge_guide)
    source_links = []
    source_blocks = []
    for source_text, source_rel in source_files:
        source_url = 'https://github.com/kowlutla/DSA/blob/main/src/com/dsa/' + source_rel.replace(' ', '%20')
        source_links.append('<a href="%s" target="_blank" rel="noopener"><code>%s</code></a>' % (source_url, esc(source_rel)))
        source_blocks.append('<h3>%s</h3><pre class="dsa-code"><code>%s</code></pre>' % (esc(source_rel), esc(source_text)))
    description = statement[0] if statement else 'Java implementation reference for ' + problem_title
    entry_kind = 'Problem' if statement else 'Implementation reference'
    return '''<!DOCTYPE html>
<html lang="en"><head><script src="../../../theme.js"></script><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(problem)s — %(topic)s | DSA Handbook</title><meta name="description" content="%(description)s">
<link rel="stylesheet" href="../../../handbook/assets/style.css"><link rel="stylesheet" href="../../../quicknotes/assets/quick.css"><link rel="stylesheet" href="../../assets/dsa.css"><link rel="icon" href="../../../favicon.svg" type="image/svg+xml"></head>
<body><div class="qn"><div id="dsa-page">
<nav class="dsa-breadcrumb" aria-label="Breadcrumb"><a href="../../../index.html">Home</a><span>/</span><a href="../../../dsa/index.html">DSA</a><span>/</span><a href="../%(topic_slug)s.html">%(topic)s</a><span>/</span><span aria-current="page">%(problem)s</span></nav>
<header class="dsa-hero dsa-problem-hero"><p class="dsa-kicker">DATA STRUCTURES &amp; ALGORITHMS / %(topic_upper)s / JAVA</p><h1>%(problem)s</h1><p class="sub">%(description)s</p><div class="dsa-meta"><span>%(entry_kind)s %(number)02d</span><span>Java implementation</span><span>Original DSA source</span></div></header>
<article class="dsa-problem-card" id="problem"><div class="dsa-card-head"><span class="dsa-number">%(number)02d</span><span class="dsa-topic">%(topic_upper)s</span></div>
<nav class="dsa-problem-nav"><a href="#definition">Problem</a><a href="#examples">Examples</a><a href="#intuition">Intuition</a><a href="#approach">Approach</a><a href="#solution">Java</a><a href="#analysis">Analysis</a></nav>
<section id="definition"><h2>1. Problem definition</h2>%(statement)s</section>
<section id="examples"><h2>2. Examples</h2>%(examples)s</section>
<section id="constraints"><h2>3. Constraints and assumptions</h2>%(constraints)s</section>
<section id="intuition"><h2>4. Intuition and key observation</h2>%(intuition_html)s<div class="dsa-insight"><span class="dsa-insight-icon">💡</span><div><b>Key question</b><p>What invariant does the algorithm maintain, and why does each state transition preserve it?</p></div></div></section>
<section id="approach"><h2>5. Approach and implementation variants</h2>%(methods)s<h3>Step-by-step reading guide</h3>%(steps)s</section>
<section id="solution"><h2>6. Java implementation</h2><p>Complete original Java source, including helper methods and comments. Evaluate each public method separately; variants may have different time and space trade-offs.</p><p><b>Original source files:</b> %(source_links)s</p>%(source_blocks)s</section>
<section id="dry-run"><h2>7. Dry run and walkthrough</h2>%(trace_html)s</section>
<section id="correctness"><h2>8. Correctness reasoning</h2>%(proof_html)s</section>
<section id="analysis"><h2>9. Complexity analysis</h2>%(complexity_html)s</section>
<section id="edge-cases"><h2>10. Edge cases and common mistakes</h2>%(edge_html)s<ul class="dsa-mistakes"><li>Empty and minimum-size inputs, if allowed.</li><li>Single-element input, duplicates and all-equal values.</li><li>Sorted, reverse-sorted and highly unbalanced inputs where relevant.</li><li>Negative values, zero, overflow and maximum constraints where relevant.</li><li>Null references, disconnected components, cycles or malformed structures where relevant.</li><li>Mutation, off-by-one errors and assumptions not enforced by the implementation.</li></ul></section>
<section id="interview"><h2>11. Interview follow-ups</h2><ul><li>Explain the invariant without referring to code.</li><li>What is the brute-force baseline and what repeated work is removed?</li><li>Which constraints make this implementation valid?</li><li>Can the auxiliary space or worst-case time be improved?</li><li>How would you test this against a brute-force oracle?</li></ul></section>
<p class="dsa-remember"><b>Revision checkpoint:</b> Restate the contract, explain the invariant, trace one example, justify correctness and derive complexity for the exact method.</p></article>
<div class="dsa-page-actions"><a href="../%(topic_slug)s.html">← Back to %(topic)s</a><a href="../../../search.html">Search the whole site</a></div>
</div></div></body></html>''' % {
        'problem': esc(problem_title), 'topic': esc(topic_title), 'topic_slug': topic_slug,
        'topic_upper': esc(topic_title.upper()), 'number': number, 'entry_kind': entry_kind, 'description': esc(description),
        'statement': statement_html, 'examples': examples_html, 'constraints': constraints_html,
        'methods': method_html, 'steps': steps_html, 'topic_reasoning': topic_reasoning, 'trace_guide': trace_guide, 'proof_guide': proof_guide, 'edge_guide': edge_guide, 'intuition_html': intuition_html, 'trace_html': trace_html, 'proof_html': proof_html, 'complexity_html': complexity_html, 'edge_html': edge_html, 'source_links': ' · '.join(source_links),
        'source_blocks': ''.join(source_blocks)
    }


DSA_TOPIC_TRACE_GUIDES = {
    'patterns': ('<p>Track the row index, column index, leading spaces and printed symbols. Verify the first row, middle row and final row separately.</p>', '<p>Show that the loop bounds print exactly the required number of symbols in each row and that the row-to-row pattern changes as specified.</p>', '<p>Test n = 1, the smallest supported size, odd/even sizes and the final row boundary.</p>'),
    'mathematical': ('<p>Write each intermediate quotient, remainder, divisor or running product. Check termination and whether integer arithmetic overflows.</p>', '<p>Show that the arithmetic transformation preserves the quantity being computed; for divisor and prime checks, justify why the tested range is sufficient.</p>', '<p>Test 0, 1, negative inputs if allowed, perfect squares, prime/composite boundaries and values near integer limits.</p>'),
    'arrays': ('<p>Draw the array with indices. At each step record the active window or pointers, running sum/count, map contents and current best answer.</p>', '<p>State what the current prefix/window represents. Prove that pointer movement or map lookup never discards a candidate that could improve the answer.</p>', '<p>Test empty/singleton arrays, duplicates, all equal values, negative values, zero, sorted/reverse order and integer overflow.</p>'),
    'strings': ('<p>Write each character index and the frequency/map state after processing it. For mappings, record both directions; for windows, show left/right boundaries.</p>', '<p>Show that each character is processed consistently and that the maintained mapping/window/prefix state exactly represents the processed prefix.</p>', '<p>Test empty strings, one character, repeated characters, case sensitivity, non-ASCII input and mismatched lengths.</p>'),
    'sorting': ('<p>Record the active range, pivot or merge halves, and the array after each partition/merge. Include duplicate and equal-key behaviour.</p>', '<p>Show that each partition/merge preserves all elements and establishes the required order; verify the recursive ranges shrink.</p>', '<p>Test empty/singleton arrays, duplicates, sorted/reverse-sorted input and stability where required.</p>'),
    'binarysearch': ('<p>For every iteration, record low, high, mid, value[mid] and the interval that remains possible. Track the exact loop invariant.</p>', '<p>Prove the target or answer remains inside the candidate interval and that each iteration strictly reduces the interval.</p>', '<p>Test empty input, one element, target below/above range, duplicates, boundaries and integer-safe midpoint arithmetic.</p>'),
    'matrix': ('<p>Draw row/column coordinates and mark the current top, bottom, left and right boundaries or the visited cells.</p>', '<p>Show that each step visits or transforms the intended cells exactly once and that boundary updates do not skip or revisit cells.</p>', '<p>Test 1x1, one row, one column, rectangular matrices and square-only operations on invalid dimensions.</p>'),
    'linkedlist': ('<p>Draw nodes and arrows before and after each pointer update. Record prev, current, next, slow and fast references explicitly.</p>', '<p>Show that no unprocessed node becomes unreachable and that the final head/tail and links satisfy the required list structure.</p>', '<p>Test null head, one node, two nodes, even/odd length, cycles, self-loop and random pointers that are null or self-referential.</p>'),
    'recursion': ('<p>Draw the call tree for a small input. Record parameters, current path/choices, base-case hits and the exact state restored during backtracking.</p>', '<p>Show that every recursive call makes progress, every valid choice is explored, and backtracking restores the state before the next branch.</p>', '<p>Test the smallest input, no-solution cases, duplicate candidates, maximum recursion depth and whether duplicate outputs are allowed.</p>'),
    'bit_magic': ('<p>Write values in binary and show the mask before and after each AND/OR/XOR/shift operation. State the bit width.</p>', '<p>Use the relevant bitwise identity to show that the transformation preserves or isolates the required bits.</p>', '<p>Test zero, negative values, sign bit, highest set bit and Java 32-bit versus 64-bit shift behaviour.</p>'),
    'stack': ('<p>Show the stack from bottom to top before and after each push/pop. For monotonic stacks, record whether values or indices are stored.</p>', '<p>Explain why every popped item has found its next greater/smaller boundary or can no longer affect the answer; each item should be pushed/popped a bounded number of times.</p>', '<p>Test empty stack, strictly increasing/decreasing data, duplicates and equal-height boundary handling.</p>'),
    'queue': ('<p>Record the queue front-to-back after each enqueue/dequeue, plus visited/distance/level state where relevant.</p>', '<p>Show that FIFO order processes states in the intended order and that marking/processing rules prevent duplicate or missed work.</p>', '<p>Test empty queue, one item, repeated states, disconnected components and level transitions.</p>'),
    'binary_tree': ('<p>Draw the tree and annotate the recursive return value or queue contents at each level. State whether height counts nodes or edges.</p>', '<p>Prove the subtree result is correct and show how combining left/right results gives the parent result; handle the null-node base case.</p>', '<p>Test empty tree, one node, skewed tree, balanced tree, negative node values and paths that do not pass through the root.</p>'),
    'binary_search_tree': ('<p>Draw the BST and mark the search path, predecessor/successor or replacement node. Check the ordering bounds for every subtree.</p>', '<p>Show that each insertion/deletion preserves the BST ordering invariant across the entire affected subtree.</p>', '<p>Test empty tree, root deletion, leaf/one-child/two-child deletion, duplicates and a fully skewed tree.</p>'),
    'greedy': ('<p>Sort or order the candidates as the algorithm does. At each step record the chosen candidate, remaining resources and feasibility condition.</p>', '<p>Explain the exchange argument or greedy-choice property that allows an optimal solution to include the locally selected candidate.</p>', '<p>Test equal endpoints, overlapping intervals, zero-sized resources, ties and counterexamples to alternative greedy orders.</p>'),
    'graphs': ('<p>Draw the graph or adjacency list. Record queue/stack, visited set, parent, distance and priority-queue entries after each step.</p>', '<p>Explain why each vertex/edge is processed correctly. For shortest paths, state the weight assumptions; for topological sort, relate completion to indegree or DFS state.</p>', '<p>Test isolated vertices, disconnected graphs, self-loops, cycles, parallel edges if allowed, zero weights and unreachable targets.</p>'),
    'dynamic_programming': ('<p>Write the DP state and table dimensions. Fill a small table in dependency order and annotate the recurrence used for each cell/state.</p>', '<p>Prove the recurrence by considering all valid final choices, establish base cases, and show that the iteration order computes dependencies first.</p>', '<p>Test zero capacity/target, empty sequence, one item, repeated values, impossible states and update direction in 1-D optimization.</p>')
}
DSA_PROBLEM_NOTES = {
    'a12-longest-subarray-with-sum-k': {
        'intuition': '<p>Let <code>prefix[i]</code> be the sum through index i. A subarray ending at i has sum k exactly when an earlier prefix sum equals <code>prefix[i] - k</code>. With non-negative values, a sliding window is also possible because extending the right edge never decreases the sum and moving the left edge never increases it.</p>',
        'steps': '<ol><li>For the brute-force version, fix a start index and extend the end index while maintaining the sum.</li><li>For the non-negative sliding window, add the right value, then shrink from the left while the sum exceeds k.</li><li>For arbitrary signed values, maintain a prefix-sum map storing the earliest index for each prefix sum.</li><li>At each index, check whether the required prefix sum exists and update the maximum length.</li></ol>',
        'trace': '<p>For <code>[1,2,3,1,1,1,1]</code> and <code>k=3</code>, the longest matches are <code>[1,2]</code>, <code>[3]</code> and windows of three ones. The maximum length is 3. In the prefix-map variant, record the running prefix and look up <code>prefix-k</code>; keep the earliest index so the resulting subarray is as long as possible.</p>',
        'proof': '<p>For the prefix-map approach, a subarray (j+1..i) sums to k iff <code>prefix[i] - prefix[j] = k</code>. Looking up <code>prefix[i]-k</code> therefore finds every matching earlier boundary. Keeping the earliest occurrence maximizes the length for a fixed i. The sliding-window variant is correct only when all values are non-negative, because its sum changes monotonically as the window expands or contracts.</p>',
        'complexity': '<p><b>Brute force:</b> O(n²) time and O(1) extra space. <b>Sliding window:</b> O(n) time and O(1) extra space because each pointer advances at most n times. <b>Prefix sum + map:</b> expected O(n) time and O(n) extra space. The sliding-window and early-break brute-force variants rely on non-negative array elements; the prefix-map variant handles negative values.</p>',
        'edge': '<p>Check k = 0, repeated prefix sums, all-zero arrays, no matching subarray, a match starting at index 0, negative values, and sums large enough to require <code>long</code>.</p>'
    },
    'a13-pair-sum': {
        'intuition': '<p>For each value x, its partner must be <code>target - x</code>. The three source variants explore the standard trade-off: enumerate every pair, remember values already seen in a hash map, or sort and move two pointers according to the current sum.</p>',
        'steps': '<ol><li><b>Brute force:</b> test every pair with i less than j.</li><li><b>Hashing:</b> before storing the current value, check whether its complement has already appeared. This prevents using the same element twice.</li><li><b>Sorting + two pointers:</b> sort, compare the smallest-plus-largest sum with target, and move the pointer that can move the sum toward the target.</li></ol>',
        'trace': '<p>For <code>[4,1,2,3,1]</code> and target 5, the hash-map scan sees 4 first, then finds its complement 1 when it reaches the next element. The answer is YES. With two pointers after sorting to <code>[1,1,2,3,4]</code>, the scan finds 1 + 4 = 5.</p>',
        'proof': '<p>The hash-map variant checks the exact complement required for the current element and stores only earlier elements, so any reported pair uses two distinct indices. In the sorted variant, if the sum is too small, moving the right pointer left cannot help; if too large, moving the left pointer right cannot help. Thus each pointer move safely eliminates pairs.</p>',
        'complexity': '<p>Brute force is O(n²) time and O(1) extra space. Hashing is expected O(n) time and O(n) space. Sorting plus two pointers is O(n log n) time; the scan is O(n). The source sorting variant mutates the input array, so preserve a copy if callers require original order. Use a wider sum type if values can overflow int.</p>',
        'edge': '<p>Test fewer than two elements, duplicates such as [3,3] with target 6, negative values, no solution, multiple valid pairs, and integer overflow in the pair sum.</p>'
    },
    'a14-sort-colors-of01and2s': {
        'intuition': '<p>The array contains only three possible values, so a comparison sort is unnecessary. One pass can partition the array into three regions: 0s already placed at the front, 1s in the middle, and 2s at the end.</p>',
        'steps': '<ol><li>Maintain <code>low</code> as the next position for 0, <code>mid</code> as the current element, and <code>high</code> as the next position for 2.</li><li>If <code>nums[mid] == 0</code>, swap low and mid, then advance both.</li><li>If it is 1, advance mid.</li><li>If it is 2, swap mid and high and decrement high; do not advance mid because the incoming value is unclassified.</li></ol>',
        'trace': '<p>For <code>[2,0,2,1,1,0]</code>, the invariant partitions the array into processed 0s, processed 1s, unknown values and processed 2s. The 2 at mid is swapped with the high element and re-examined; the 0s move to the left, producing <code>[0,0,1,1,2,2]</code>.</p>',
        'proof': '<p>At every iteration, indices below low contain only 0, indices from low to mid-1 contain only 1, and indices above high contain only 2. Each branch expands one known region and reduces the unknown interval. When mid passes high, no unknown elements remain, so the whole array is sorted.</p>',
        'complexity': '<p>The Dutch National Flag variant is O(n) time because mid advances or high retreats on every iteration, and O(1) auxiliary space because it swaps in place. The counting variant is also O(n) time but performs a counting pass followed by a rewrite pass.</p>',
        'edge': '<p>Test arrays containing only 0s, only 1s, only 2s, already sorted input, reverse order, one element and the two-element cases. The contract restricts values to 0, 1 and 2.</p>'
    },
    'a16-maximum-subarray-sum': {
        'intuition': '<p>A negative running prefix can never help a future subarray: dropping it makes every extension at least as large. Kadane’s algorithm therefore keeps the best sum ending at the current position and the best sum seen globally.</p>',
        'steps': '<ol><li>Add the current value to the running sum.</li><li>Update the global maximum.</li><li>If the running sum becomes negative, reset it to zero because a future subarray is better started after this point.</li><li>Continue to the end and return the global maximum.</li></ol>',
        'trace': '<p>For <code>[1,2,7,-4,3,2,-10,9,1]</code>, the best running segment reaches 9 after <code>[1,2,7,-4,3,2]</code>. Adding -10 makes the running sum negative, so it is discarded; the final segment [9,1] reaches only 10. The maximum remains 11.</p>',
        'proof': '<p>For each index, the best subarray ending there is either the current element alone or the previous best-ending sum plus the current element. The recurrence <code>endingHere = max(x, endingHere + x)</code> considers both possibilities. Taking the maximum over all positions yields the best subarray overall.</p>',
        'complexity': '<p>Kadane’s scan is O(n) time and O(1) auxiliary space. The empty-subarray convention in this problem means the answer cannot be below zero; check that the implementation initializes or updates the best answer accordingly for all-negative input.</p>',
        'edge': '<p>Test all-negative arrays, all-positive arrays, one element, zeros, a best segment at the beginning or end, and sums that can exceed int.</p>'
    },
    'a19-next-permutation': {
        'intuition': '<p>Permutations are ordered lexicographically. To get the immediate next one, change the rightmost position that can still be increased, and make the suffix as small as possible afterward.</p>',
        'steps': '<ol><li>Scan from right to left to find the first index i with <code>a[i] &lt; a[i+1]</code>; this is the pivot.</li><li>If no pivot exists, the array is descending and already the last permutation; reverse the whole array.</li><li>Otherwise, find the rightmost element greater than the pivot and swap them.</li><li>Reverse the suffix after the pivot to put it in ascending order, which is its smallest possible arrangement.</li></ol>',
        'trace': '<p>For <code>[1,2,3,6,5,4]</code>, the rightmost ascent is 3 before 6. Swap 3 with the smallest suffix element greater than it (4), then reverse the remaining suffix to obtain <code>[1,2,4,3,5,6]</code>. For [3,2,1], no pivot exists, so reversing gives [1,2,3].</p>',
        'proof': '<p>The suffix to the right of the pivot is non-increasing, so it is the largest arrangement of those elements. Increasing the rightmost possible pivot gives the smallest possible increase; choosing the rightmost greater successor minimizes that increase, and reversing the suffix produces its smallest order. Therefore no permutation lies between the original and the result.</p>',
        'complexity': '<p>O(n) time: the pivot scan, successor scan and suffix reversal each take at most n steps. O(1) auxiliary space when the array/list is modified in place.</p>',
        'edge': '<p>Test an already descending sequence, an ascending sequence, duplicates, two elements, one element and a pivot at index 0.</p>'
    },
    'a21-longest-consecutive-subsequence': {
        'intuition': '<p>Sorting makes consecutive values adjacent but costs O(n log n). A hash set can do better: only start counting from values that have no predecessor (x-1), so each consecutive run is scanned once from its true beginning.</p>',
        'steps': '<ol><li>Insert all values into a set to remove duplicates and support expected O(1) membership checks.</li><li>For each value x, start a run only if x-1 is absent.</li><li>While x+1, x+2, and so on exist, extend the run.</li><li>Track the longest run length.</li></ol>',
        'trace': '<p>For <code>[2,6,1,9,4,5,3]</code>, the set contains 1 through 6 plus 9. Only 1 starts the long run because 0 is absent. Counting 1,2,3,4,5,6 gives length 6; values 2–6 are skipped as starts because their predecessors exist.</p>',
        'proof': '<p>Every maximal consecutive run has exactly one value whose predecessor is absent: its minimum. Starting only at these minima visits every run and never repeats a run from an interior value. The maximum counted run is therefore the longest consecutive subsequence.</p>',
        'complexity': '<p>Expected O(n) time and O(n) space for the hash set. Each value is inserted once and belongs to at most one forward run scan. Hash-table operations are expected constant time, not a strict worst-case guarantee.</p>',
        'edge': '<p>Test duplicates, empty input if allowed, negative values, a single run, no consecutive values, integer boundary values and very large consecutive runs.</p>'
    },
    'a25-count-sub-arrays-with-sum-k': {
        'intuition': '<p>Use prefix sums. If the running prefix is S and an earlier prefix was S-k, the elements between those positions sum to k. Unlike a simple sliding window, this works when the array contains negative values.</p>',
        'steps': '<ol><li>Initialize a frequency map with prefix sum 0 occurring once; this counts subarrays that begin at index 0.</li><li>For each value, update the running prefix sum.</li><li>Add the frequency of <code>prefix-k</code> to the answer.</li><li>Increment the frequency of the current prefix sum.</li></ol>',
        'trace': '<p>For <code>[10,2,-2,-20,10]</code> and k = -10, the matching subarrays are [10,2,-2,-20], [2,-2,-20,10] and [-20,10]. The prefix-frequency lookup counts each matching earlier boundary, including repeated prefix sums.</p>',
        'proof': '<p>A subarray from j+1 through i has sum k exactly when <code>prefix[i] - prefix[j] = k</code>. Rearranging gives <code>prefix[j] = prefix[i] - k</code>. The map stores the number of earlier boundaries with that prefix, so adding its frequency counts every valid subarray ending at i exactly once.</p>',
        'complexity': '<p>Expected O(n) time and O(n) auxiliary space. Each element causes one prefix update, one map lookup and one map update. Use long for prefix sums and the answer if the constraints allow large totals.</p>',
        'edge': '<p>Test negative values, zero values, k = 0, repeated prefix sums, a subarray starting at index 0, no matching subarray and large cumulative sums.</p>'
    },
    'a28-three-sum-problem': {
        'intuition': '<p>Sort the array and fix one value. The remaining task is a two-sum search on the suffix. Because the suffix is sorted, two pointers can move inward based on whether the sum is too small or too large.</p>',
        'steps': '<ol><li>Sort the array.</li><li>For each index i, skip it when it equals the previous fixed value to avoid duplicate triplets.</li><li>Set left = i+1 and right = n-1; compute the three-value sum using a wide type.</li><li>If the sum is negative, move left; if positive, move right; if zero, record the triplet and skip duplicate values at both pointers.</li></ol>',
        'trace': '<p>For <code>[-1,0,1,2,-1,-4]</code>, sorting gives [-4,-1,-1,0,1,2]. Fixing -1 and moving two pointers finds [-1,-1,2] and [-1,0,1]. Duplicate skipping prevents returning the same triplet more than once.</p>',
        'proof': '<p>After sorting, for a fixed i, increasing left increases or preserves the sum, while decreasing right decreases or preserves it. Therefore the pointer movement cannot skip a solution. Skipping equal fixed values and equal pointer values removes duplicate triplets without removing a distinct value combination.</p>',
        'complexity': '<p>O(n²) time after sorting: there are O(n) fixed positions and an O(n) two-pointer scan for each. Sorting costs O(n log n). Auxiliary space depends on the sorting implementation; the result list is output space and is excluded from auxiliary-space analysis.</p>',
        'edge': '<p>Test fewer than three elements, all zeros, no valid triplet, many duplicates, positive-only/negative-only arrays and sums that require long arithmetic.</p>'
    },
    'st11-trapping-rain-water': {
        'intuition': '<p>Water above a bar is <code>min(maxLeft,maxRight)-height[i]</code>. The shorter boundary limits the water level. The source contains brute-force, prefix/suffix and two-pointer variants.</p>',
        'steps': '<ol><li>For each bar, determine the tallest wall on its left and right.</li><li>In the two-pointer method, process the shorter boundary because the opposite boundary is already at least as tall.</li><li>Add the difference between the known side maximum and the current height when positive.</li></ol>',
        'trace': '<p>For <code>[3,0,0,2,0,4]</code>, the trapped water is 3 + 3 + 1 + 3 = 10 units. Track leftMax and rightMax as the pointers move; each processed side is safe because the opposite boundary is no shorter.</p>',
        'proof': '<p>When the left height is no greater than the right height, a right boundary at least as high already exists, so the left-side maximum determines the water above the left bar. The symmetric argument holds on the right. Each pointer step finalizes one position.</p>',
        'complexity': '<p>Two pointers: O(n) time, O(1) auxiliary space. Prefix/suffix arrays: O(n) time, O(n) space. Per-position rescanning: O(n²) time, O(1) space.</p>',
        'edge': '<p>Test fewer than three bars, monotonic heights, equal heights, a flat valley, one peak and large accumulated water.</p>'
    },
    'l33-clone-linked-list-with-random-pointer': {
        'intuition': '<p>The clone must preserve next and random links while ensuring cloned links never point into the original list. A HashMap translates original node identity to clone identity; interleaving makes the clone of a node its immediate successor.</p>',
        'steps': '<ol><li>Map approach: create all clone nodes and store original→clone mappings.</li><li>In a second pass, set clone.next and clone.random by looking up the original targets.</li><li>Interleaving approach: insert each clone after its original, assign random links through <code>original.random.next</code>, then split the two lists and restore the original.</li></ol>',
        'trace': '<p>For 1→2→3 with 1.random→3, interleaving produces 1→1′→2→2′→3→3′. The random pointer of 1′ targets 3′. The final pass restores 1→2→3 and creates 1′→2′→3′.</p>',
        'proof': '<p>The map is a one-to-one correspondence between original and cloned nodes, so translating each pointer through it preserves the graph. In the interleaved version, every clone is adjacent to its original, allowing random targets to be translated in O(1); separation then restores both lists.</p>',
        'complexity': '<p>Both approaches take O(n) time. HashMap uses O(n) auxiliary space. Interleaving uses O(1) auxiliary space excluding the newly allocated clone nodes, but temporarily mutates the original list and must restore it.</p>',
        'edge': '<p>Test empty list, one node, null random pointers, self-random pointers, random-to-head/tail and several nodes sharing one random target.</p>'
    },
    'bt15-diameter-of-binary-tree': {
        'intuition': '<p>A longest path through a node has <code>leftHeight + rightHeight + 1</code> nodes. The overall diameter may instead lie wholly in one subtree, so retain the maximum seen across all nodes.</p>',
        'steps': '<ol><li>Naive variant recomputes subtree heights at each node and recursively calculates both subtree diameters.</li><li>Optimized postorder variant computes each child height once.</li><li>At each node, update the diameter with leftHeight + rightHeight, then return 1 + max(leftHeight,rightHeight).</li></ol>',
        'trace': '<p>For 10 with children 20 and 30, and 20 with children 40 and 60, the longest path 40→20→10→30 contains four nodes. The optimized recursion computes heights bottom-up and updates the answer at the root.</p>',
        'proof': '<p>Any longest path in a subtree is either entirely in its left child, entirely in its right child, or passes through the current node. Postorder provides the two child heights, so comparing these cases at every node considers every possible path.</p>',
        'complexity': '<p>Naive: O(n²) worst-case time due to repeated height calculations. Optimized: O(n) time, visiting each node once. Both use O(h) recursion stack space.</p>',
        'edge': '<p>Test empty tree, one node, skewed tree, balanced tree and a diameter entirely inside one subtree. This source definition counts nodes, not edges.</p>'
    },
    'dp25-longest-common-subsequence': {
        'intuition': '<p>Let dp[i][j] be the LCS length of the first i characters of s and first j characters of t. Matching final characters extend the diagonal state; otherwise one of the two final characters must be excluded.</p>',
        'steps': '<ol><li>Base case: either prefix empty gives 0.</li><li>If s[i−1] equals t[j−1], use 1 + dp[i−1][j−1].</li><li>Otherwise use max(dp[i−1][j], dp[i][j−1]).</li><li>Memoization caches states; tabulation fills smaller prefixes first; space optimization keeps only the previous and current rows.</li></ol>',
        'trace': '<p>For <code>abcde</code> and <code>ace</code>, the matches a, c and e extend the common subsequence to length 3. The LCS is "ace".</p>',
        'proof': '<p>If the final characters match, an optimal subsequence can include that character and the best preceding prefixes. If they differ, an optimal answer must omit at least one final character, so the maximum of the two smaller-prefix states is sufficient. These cases cover all possibilities.</p>',
        'complexity': '<p>Naive recursion is exponential due to repeated states. Memoization/tabulation take O(n·m) time and O(n·m) space. Two-row optimization takes O(n·m) time and O(m) auxiliary space; use the shorter string as the column dimension for O(min(n,m)) space.</p>',
        'edge': '<p>Test empty strings, identical strings, no common characters, repeated characters and highly unbalanced lengths.</p>'
    },
    'lower-bound': {
        'intuition': '<p>Lower bound is the first index whose value is greater than or equal to x. It is not exact-match search; if no value qualifies, the answer is n.</p>',
        'steps': '<ol><li>Initialize the candidate answer to n.</li><li>If arr[mid] ≥ x, save mid and search left for an earlier valid index.</li><li>If arr[mid] &lt; x, discard mid and its left side.</li><li>Return the saved candidate when the interval is empty.</li></ol>',
        'trace': '<p>For <code>[1,3,5,7,9,11,13]</code> and x=6, the first qualifying value is 7 at index 3. For x=14, no element qualifies and the result is 7 (n).</p>',
        'proof': '<p>Sorted order means that when arr[mid] ≥ x, mid and everything right are valid candidates, so the first valid index is at mid or left. When arr[mid] &lt; x, mid and everything left are invalid. Each step preserves the first-valid-index candidate.</p>',
        'complexity': '<p>O(log n) time and O(1) auxiliary space. The input must be sorted in non-decreasing order.</p>',
        'edge': '<p>Test x below minimum, equal to minimum, between values, duplicate values, equal to maximum and greater than maximum.</p>'
    },
    'koko-eating-bananas': {
        'intuition': '<p>At speed k, hours required are the sum of <code>ceil(pile/k)</code>. Feasibility is monotonic: a speed that works implies every larger speed also works, so binary search finds the minimum feasible speed.</p>',
        'steps': '<ol><li>Search speed from 1 to the largest pile.</li><li>For mid, sum the ceiling-divided hours for every pile.</li><li>If total hours ≤ h, save mid and search slower; otherwise search faster.</li><li>The final candidate is the minimum feasible speed.</li></ol>',
        'trace': '<p>For piles <code>[3,6,7,11]</code> and h=8, speed 4 needs 1+2+2+3 = 8 hours. Speed 3 needs 1+2+3+4 = 10 hours, so it is too slow. The minimum valid speed is 4.</p>',
        'proof': '<p>The required hours never increase as speed increases. Binary search maintains the boundary between infeasible and feasible speeds; a feasible midpoint allows searching left, while an infeasible midpoint requires searching right.</p>',
        'complexity': '<p>For n piles and maximum pile size M, each feasibility check is O(n), and there are O(log M) checks: O(n log M) time and O(1) auxiliary space. Accumulate hours in long.</p>',
        'edge': '<p>Test h equal to the number of piles, h much larger than the pile count, one pile, equal piles and large values that could overflow an int hour sum.</p>'
    },
    'g21-topological-sort': {
        'intuition': '<p>A topological order places u before v for every directed edge u→v. DFS pushes a vertex only after all its outgoing neighbours finish; popping the stack reverses finishing order.</p>',
        'steps': '<ol><li>Build an adjacency list.</li><li>Run DFS from every unvisited vertex, including disconnected components.</li><li>After exploring all neighbours, push the current vertex.</li><li>Pop the stack to produce the ordering.</li></ol>',
        'trace': '<p>For edges 3→1, 1→2, 0→2 and 0→4, a valid order is <code>3,1,0,4,2</code>. Other orders may also be correct as long as every edge points forward.</p>',
        'proof': '<p>In a DAG, DFS finishes every reachable neighbour before the current vertex. Therefore the current vertex is pushed later and popped earlier, placing it before each outgoing neighbour. Visiting all vertices covers disconnected components too.</p>',
        'complexity': '<p>O(V+E) time and O(V) auxiliary space for visited state, stack and recursion. This implementation assumes a DAG; it does not detect cycles.</p>',
        'edge': '<p>Test isolated vertices, disconnected DAGs, a chain, multiple valid orders and a directed cycle that violates the precondition.</p>'
    }
,
    "a1-largest-number-in-array": {
        "intuition": "<p>The maximum is the largest value seen so far. One scan compares each element with the current candidate exactly once.</p>",
        "steps": "<ol><li>Initialize the candidate from the first element.</li><li>Scan the remaining values.</li><li>Replace the candidate whenever a larger value appears.</li><li>Return the candidate.</li></ol>",
        "trace": "<p>For <code>[5,10,3,8,15]</code>, the candidate changes 5 → 10 → 15. The answer is 15.</p>",
        "proof": "<p>After each iteration, the candidate is the maximum of the prefix processed so far. At termination that prefix is the entire array.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>The implementation reads <code>arr[0]</code>, so empty input needs a guard. Test one element, negative values, duplicate maxima and sorted/reverse-sorted input.</p>",
    },
    "a2-second-largest-and-smallest-numbers": {
        "intuition": "<p>Maintain the best and second-best candidates for both directions during one scan. The stated contract requires unique, non-negative values.</p>",
        "steps": "<ol><li>Initialize largest and second-largest candidates below the valid range, and smallest candidates above it.</li><li>Update the largest pair for each value.</li><li>Independently update the smallest pair.</li><li>Return second-largest followed by second-smallest.</li></ol>",
        "trace": "<p>For <code>[1,2,3,4,5]</code>, the largest pair is 5 and 4; the smallest pair is 1 and 2. Return <code>[4,2]</code>.</p>",
        "proof": "<p>Each update preserves the two best distinct values seen so far. A new extreme displaces the old extreme into second place; otherwise it may improve only the second candidate.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>The source initializes largest candidates to -1, which relies on non-negative input. Fewer than two values cannot provide both answers. Clarify whether duplicates count as distinct ranks if the contract changes.</p>",
    },
    "a3-check-array-sorted-or-not": {
        "intuition": "<p>A non-decreasing array has no adjacent inversion. Checking neighbouring pairs is sufficient; comparing all pairs is unnecessary.</p>",
        "steps": "<ol><li>Visit indices 0 through n-2.</li><li>If <code>arr[i] &gt; arr[i+1]</code>, return false.</li><li>If no inversion exists, return true.</li></ol>",
        "trace": "<p><code>[10,20,30,40]</code> has no inversion and returns true. <code>[90,80,100,70]</code> fails at 90 &gt; 80 and returns false.</p>",
        "proof": "<p>If every adjacent pair is ordered, transitivity implies every earlier element is no greater than every later element. One adjacent inversion disproves sortedness.</p>",
        "complexity": "<p>O(n) worst-case time and O(1) auxiliary space; the scan exits early on the first inversion.</p>",
        "edge": "<p>Empty and one-element arrays are sorted by convention. Equal neighbours are allowed: the requirement is non-decreasing, not strictly increasing.</p>",
    },
    "a3-check-rotated-array-is-sorted-or-not": {
        "intuition": "<p>A sorted array viewed cyclically has at most one descent (a position where the next value is smaller), including the wraparound pair from the last value to the first.</p>",
        "steps": "<ol><li>Compare every value with its cyclic successor.</li><li>Count positions where the current value is greater than the next.</li><li>Return false as soon as the count exceeds one; otherwise return true.</li></ol>",
        "trace": "<p><code>[3,4,5,1,2]</code> has one descent (5 to 1), so it is valid. <code>[2,1,3,4]</code> has two cyclic descents and is invalid.</p>",
        "proof": "<p>Rotating a non-decreasing sequence introduces at most one boundary where the maximum suffix meets the minimum prefix. If there is at most one cyclic descent, starting after it produces a non-decreasing traversal.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Duplicates do not count as descents. Guard empty input before modulo; one-element and all-equal arrays are valid.</p>",
    },
    "a4-remove-duplicates-from-sorted-array": {
        "intuition": "<p>Sorted duplicates are adjacent. A write pointer compacts each newly encountered distinct value into the prefix while a read pointer scans the input.</p>",
        "steps": "<ol><li>Return 0 for an empty array.</li><li>Keep the first value and set the next write position to 1.</li><li>Scan the remaining values; when one differs from the last retained value, write it and advance the write pointer.</li><li>Return the number of retained values. Only that prefix is meaningful.</li></ol>",
        "trace": "<p>For <code>[1,2,2,4]</code>, retain 1, retain the first 2, skip the duplicate 2, then retain 4. The prefix is <code>[1,2,4]</code>; return 3.</p>",
        "proof": "<p>Before each read step, the written prefix contains exactly the distinct values in the processed input prefix, in sorted order. Writing only when the value differs from the last retained value preserves uniqueness.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space; the input is modified in place.</p>",
        "edge": "<p>Test empty, one-element, all-equal and all-distinct arrays, plus duplicates at either end. Ignore the stale suffix beyond the returned length. The algorithm requires sorted input.</p>",
    },
    "upper-bound": {
        "intuition": "<p>The upper bound is the first index whose value is strictly greater than the target. It is a boundary-search problem, not an ordinary search for an arbitrary matching element.</p>",
        "steps": "<ol><li>Search the half-open candidate range using start and end.</li><li>If the middle value is greater than x, remember mid and continue left.</li><li>Otherwise continue right.</li><li>If no qualifying value exists, return n.</li></ol>",
        "trace": "<p>For <code>[1,2,2,4,7]</code> and x=2, values at indices 0–2 are not strictly greater; index 3 contains 4, so upper bound is 3.</p>",
        "proof": "<p>At every step, indices before start are known to be at most x, and indices at or after the candidate boundary are known to be greater than x. The search narrows to the first index satisfying the predicate.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test x below all values, above all values (answer n), duplicates, an empty array and a target exactly equal to the final element. Input must be sorted non-decreasingly.</p>",
    },
    "floor-in-a-sorted-array": {
        "intuition": "<p>The floor is the greatest value less than or equal to x. In a sorted array, the answer is the rightmost index satisfying that predicate.</p>",
        "steps": "<ol><li>Binary-search the sorted array.</li><li>If a[mid] is at most x, save mid and search right for a larger valid value.</li><li>If a[mid] exceeds x, search left.</li><li>Return the saved index, or -1 if no value qualifies.</li></ol>",
        "trace": "<p>For <code>[1,2,8,10,12]</code> and x=5, 2 is the greatest value not exceeding 5, so return index 1.</p>",
        "proof": "<p>When a[mid] is at most x, mid is a valid floor candidate and no index left of mid can be a better (larger) value. Searching right is therefore safe. When a[mid] exceeds x, mid and everything to its right are invalid.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Return -1 when x is smaller than the first value. If x is at least the last value, return n-1. The source contract says there are no duplicates, though the rightmost-valid formulation also handles them.</p>",
    },
    "ceil-in-a-sorted-array": {
        "intuition": "<p>The ceiling is the smallest value greater than or equal to x. In a sorted array, it is the leftmost index satisfying that predicate.</p>",
        "steps": "<ol><li>Binary-search the sorted array.</li><li>If a[mid] is at least x, save mid and search left for a smaller valid value.</li><li>If a[mid] is below x, search right.</li><li>Return the saved index, or -1 when no value qualifies.</li></ol>",
        "trace": "<p>For <code>[1,2,8,10,12]</code> and x=5, the first value at least 5 is 8, at index 2.</p>",
        "proof": "<p>When a[mid] is at least x, mid is valid and all indices to its right are no better, so search left. When a[mid] is below x, it and every earlier value are invalid, so search right.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Return -1 when x exceeds the last value. If x is at most the first value, return 0. Empty input also returns -1.</p>",
    },
    "first-and-last-position-of-a-number": {
        "intuition": "<p>Two boundary searches find the first position not less than target and the first position greater than target. If the target exists, the last position is one before the second boundary.</p>",
        "steps": "<ol><li>Binary-search for the first index with value at least target.</li><li>If that index is n or its value differs from target, return [-1,-1].</li><li>Binary-search for the first index with value greater than target.</li><li>Return the first index and the second boundary minus one.</li></ol>",
        "trace": "<p>For <code>[5,7,7,8,8,10]</code> and target 8, the lower boundary is 3 and the upper boundary is 5. The answer is <code>[3,4]</code>.</p>",
        "proof": "<p>Sorted order makes all target occurrences contiguous. The first boundary excludes every smaller value; the second excludes every value equal to or smaller than target. Their interval is exactly the target's range.</p>",
        "complexity": "<p>O(log n) time for two binary searches and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty input, target absent, all elements equal to target, target at either endpoint and a single occurrence. Avoid reading nums[n] when the lower boundary equals n.</p>",
    },
    "count-occurrences-in-sorted-array": {
        "intuition": "<p>All occurrences of x form one contiguous block. Find its first and last positions with lower/upper-bound searches; the count is the width of that block.</p>",
        "steps": "<ol><li>Find the first index with value at least x.</li><li>If that index is outside the array or does not contain x, return 0.</li><li>Find the first index with value greater than x.</li><li>Return upperBound minus lowerBound.</li></ol>",
        "trace": "<p>For <code>[2,2,3,3,3,3,4]</code> and x=3, the lower boundary is 2 and upper boundary is 6. Count = 6 - 2 = 4.</p>",
        "proof": "<p>Because the array is sorted, every occurrence of x lies between the first value not less than x and the first value greater than x. No index outside that half-open interval can contain x.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test no occurrence, one occurrence, all values equal x, x at either end and an empty array. Confirm whether the implementation returns 0 rather than -1 for absence.</p>",
    },
    "search-insert-position": {
        "intuition": "<p>The insertion index is the first position whose value is greater than or equal to target. If all values are smaller, the insertion point is n.</p>",
        "steps": "<ol><li>Maintain a candidate result initialized to n.</li><li>If nums[mid] is at least target, save mid and search left.</li><li>Otherwise search right.</li><li>Return the first valid boundary.</li></ol>",
        "trace": "<p>For <code>[1,3,5,6]</code>, target 2 belongs before 3, so return 1. Target 7 belongs after the final element, so return 4.</p>",
        "proof": "<p>The search maintains that all indices before start are too small and the saved result is a valid insertion boundary. Repeatedly moving left on values at least target finds the earliest legal position.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test target before the first value, after the last, equal to an existing value, empty input and one-element input. The source contract specifies distinct sorted integers, but the lower-bound logic also works with duplicates.</p>",
    },
    "search-in-rotated-array": {
        "intuition": "<p>A rotation of a strictly increasing array has at least one sorted half in every binary-search iteration. Identify that half and check whether the target lies within its inclusive range.</p>",
        "steps": "<ol><li>Compute mid and return if it matches target.</li><li>If the left segment from low to mid is sorted, keep it only when target lies within its range.</li><li>Otherwise the right segment is sorted; keep it only when target lies within that range.</li><li>Repeat until found or the interval is empty.</li></ol>",
        "trace": "<p>For <code>[4,5,6,7,0,1,2]</code> and target 0, the first midpoint is 7. The left segment is sorted but does not contain 0, so search the right segment; the next steps reach index 4.</p>",
        "proof": "<p>With distinct values, the rotation pivot separates the array into two sorted runs. At least one side of mid lies wholly within one run. Range comparison determines whether the target can be in that sorted side; discarding the other side cannot remove a valid target.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space when all values are distinct.</p>",
        "edge": "<p>Test an unrotated array, rotation by one, target at either side of the pivot, missing target, one element and empty input. The logarithmic guarantee depends on distinct values.</p>",
    },
    "search-in-sorted-rotated-array2": {
        "intuition": "<p>Duplicates can make both ends and the midpoint equal, so neither half can be identified as sorted. In that ambiguous case, safely trim equal boundary values before applying the usual sorted-half logic.</p>",
        "steps": "<ol><li>Return true if nums[mid] equals target.</li><li>If nums[low], nums[mid] and nums[high] are equal, increment low and decrement high.</li><li>Otherwise identify the sorted half and test whether target lies in its range.</li><li>Continue until found or the search interval is empty.</li></ol>",
        "trace": "<p>For <code>[2,5,6,0,0,1,2]</code> and target 0, the algorithm identifies a sorted half and narrows toward the zero block. For target 3, the interval is exhausted and it returns false.</p>",
        "proof": "<p>When the three boundary values are equal, removing the outer equal values cannot remove the only evidence that target exists: if target equals them, the midpoint or boundary comparison would already have found it; otherwise those boundary positions are not informative. In other iterations, sorted-half range checks remain valid.</p>",
        "complexity": "<p>Average and typical cases are O(log n), but worst-case time is O(n) when many duplicates force one-step boundary trimming. Auxiliary space is O(1).</p>",
        "edge": "<p>Test all-equal values, target equal to duplicated boundaries, duplicates spanning the rotation pivot, one element and empty input. Do not claim strict O(log n) worst-case time when duplicates are allowed.</p>",
    },
,
    "a10-max-consecutive-ones": {
        "intuition": "<p>The repository groups two related variants: maximum consecutive ones with no flips, and maximum consecutive ones when at most k zeros may be flipped. The first is a simple run counter; the second is a sliding window containing at most k zeros.</p>",
        "steps": "<ol><li><b>Basic variant:</b> increment the current run on 1, reset it on 0, and maintain the maximum.</li><li><b>At-most-k variant:</b> expand the right edge, count zeros, and move the left edge until the window contains no more than k zeros.</li><li>Update the best window length after each valid expansion.</li></ol>",
        "trace": "<p>For the basic input <code>[1,1,0,1,1,1]</code>, the longest run is 3. For <code>[1,1,1,0,0,0,1,1,1,1,0]</code> with k=2, the longest window with at most two zeros has length 6.</p>",
        "proof": "<p>The basic counter stores the length of the all-ones suffix ending at the current index. In the second variant, the sliding window is restored to validity whenever its zero count exceeds k; each valid window ending at the current right edge is considered. Both methods therefore cover every possible optimal run/window.</p>",
        "complexity": "<p>Both variants run in O(n) time and O(1) auxiliary space. Each array position is visited a constant number of times; in the window variant both pointers only move forward.</p>",
        "edge": "<p>Test empty input, all zeros, all ones, k=0, k greater than the number of zeros and a long zero block. The two variants have different contracts; do not confuse the meaning of k.</p>",
    },
    "a5-a6-rotate-array-clock-wise": {
        "intuition": "<p>Rotation is cyclic. Repeating a one-position right shift is easy to follow but costs O(nk); three reversals provide a linear-time in-place alternative.</p>",
        "steps": "<ol><li>Normalize k with <code>k %= n</code> after checking n is non-zero.</li><li>Reverse the entire array.</li><li>Reverse the first k values.</li><li>Reverse the remaining n-k values.</li></ol>",
        "trace": "<p>Right-rotate <code>[1,2,3,4,5]</code> by 2: full reversal gives [5,4,3,2,1]; reversing the first two and final three values gives <code>[4,5,1,2,3]</code>.</p>",
        "proof": "<p>Full reversal puts the original final k values at the front and the original first n-k values at the back, but reverses both blocks. Reversing each block restores their internal order, yielding the required right rotation.</p>",
        "complexity": "<p>The repeated-shift source implementation is O(nk) time and O(1) extra space. The three-reversal method is O(n) time and O(1) extra space.</p>",
        "edge": "<p>Normalize k when it exceeds n; k=0 and k=n leave the array unchanged. Guard empty input before modulo. The class comment says left rotation, but the inspected helper shifts the last element to index 0, which is a right shift: trust the method behavior and resolve this documentation mismatch.</p>",
    },
    "a5-a6-rotate-array-anti-clock-wise": {
        "intuition": "<p>A left rotation by k moves the first k elements to the end while preserving their order. The reversal method avoids performing k separate shifts.</p>",
        "steps": "<ol><li>Normalize k to the range 0 through n-1.</li><li>Reverse the first k values.</li><li>Reverse the remaining n-k values.</li><li>Reverse the entire array.</li></ol>",
        "trace": "<p>For <code>[1,2,3,4,5]</code> and k=2, reverse the first block, then the second block, then the whole array. The result is <code>[3,4,5,1,2]</code>.</p>",
        "proof": "<p>The first two reversals reverse each block internally. Reversing the whole array restores the internal order of both blocks and swaps their positions, exactly matching a left rotation.</p>",
        "complexity": "<p>The source's repeated-shift method is O(nk) time and O(1) space. Three reversals give O(n) time and O(1) extra space.</p>",
        "edge": "<p>Check k=0, k=n, k greater than n, n=1 and empty input. Normalize k and avoid indexing an empty array.</p>",
    },
    "a7-move-all-zeros-to-end": {
        "intuition": "<p>Preserve the relative order of non-zero values while moving zeros to the suffix. A read pointer finds non-zero values and a write pointer compacts them into the front.</p>",
        "steps": "<ol><li>Set write to zero.</li><li>Scan from left to right.</li><li>For each non-zero value, write it at the write index and advance write.</li><li>Fill the remaining positions with zero.</li></ol>",
        "trace": "<p>For <code>[0,1,0,3,12]</code>, compacting non-zero values gives [1,3,12] in the prefix; filling the rest gives <code>[1,3,12,0,0]</code>.</p>",
        "proof": "<p>The scan visits non-zero values in their original order and writes each exactly once. Every remaining slot corresponds to a zero that was skipped, so filling the suffix preserves all values and stable order.</p>",
        "complexity": "<p>The source includes an auxiliary-array variant using O(n) extra space and an in-place compaction variant using O(1) auxiliary space. Both are O(n) time.</p>",
        "edge": "<p>Test all zeros, no zeros, leading/trailing zeros, alternating zeros, negative non-zero values and one element. The non-zero relative order must remain unchanged.</p>",
    },
    "a8-intersection-of-two-arrays": {
        "intuition": "<p>The result contains unique values present in both arrays. Sorting both arrays enables a two-pointer scan; a set-based approach is another option when arbitrary output order is acceptable.</p>",
        "steps": "<ol><li>Sort both arrays for the two-pointer variant.</li><li>Advance the pointer holding the smaller value.</li><li>When values match, append the value once and advance both pointers past duplicates.</li><li>Return the unique intersection.</li></ol>",
        "trace": "<p>For <code>[4,9,5]</code> and <code>[9,4,9,8,4]</code>, sorted inputs are [4,5,9] and [4,4,8,9,9]. The unique matches are 4 and 9.</p>",
        "proof": "<p>If the current values differ, the smaller one cannot match the current or any later value in the other sorted array, so advancing its pointer is safe. Equal values are common; skipping duplicate runs ensures uniqueness.</p>",
        "complexity": "<p>Sorting costs O(n log n + m log m), followed by an O(n+m) scan. Result storage is O(min(n,m)) in the worst case. Sorting mutates the input arrays unless copies are made.</p>",
        "edge": "<p>Test empty arrays, disjoint inputs, all values shared, duplicates on either side, negative values and arbitrary output ordering. The returned elements must be unique.</p>",
    },
    "a8-merge-two-sorted-arrays": {
        "intuition": "<p>The union is the sorted set of distinct values from both sorted arrays. Merge by repeatedly choosing the smaller unconsumed value and skip duplicates.</p>",
        "steps": "<ol><li>Maintain one pointer in each sorted input.</li><li>Choose the smaller current value; if equal, consume both.</li><li>Append only when the chosen value differs from the last output value.</li><li>Consume the remaining suffix of either input.</li></ol>",
        "trace": "<p>For <code>[1,2,3,4,6]</code> and <code>[2,3,5]</code>, emit 1, 2, 3, 4, 5, 6. Common values and repeated values appear only once.</p>",
        "proof": "<p>The smallest unconsumed value must be at one of the two sorted-array pointers. Emitting that minimum preserves sorted order. Comparing with the last output value removes duplicates without losing any distinct value.</p>",
        "complexity": "<p>O(n+m) time and O(n+m) output space in the worst case.</p>",
        "edge": "<p>Check empty inputs, disjoint ranges, identical arrays, duplicates within one input and duplicates across both. Both inputs must be sorted.</p>",
    },
    "a9-missing-number": {
        "intuition": "<p>The array contains n distinct values from 0 through n, with one missing. XOR cancels equal pairs because <code>x ^ x = 0</code> and <code>x ^ 0 = x</code>.</p>",
        "steps": "<ol><li>Initialize an accumulator with n, or XOR expected indices and input values together.</li><li>XOR every expected value and every array value into the accumulator.</li><li>All present values cancel, leaving the missing value.</li></ol>",
        "trace": "<p>For <code>[3,0,1]</code>, the expected range is 0..3. XORing 0,1,2,3 with the input 3,0,1 cancels those repeated values and leaves 2.</p>",
        "proof": "<p>XOR is associative and commutative. Every present number occurs once in the expected range and once in the array, so it cancels; only the missing number remains.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space. The sum formula is another linear approach, but use long arithmetic to avoid overflow.</p>",
        "edge": "<p>Test missing 0, missing n, n=1 and shuffled input. The proof requires distinct values and the exact range [0,n].</p>",
    },
    "a11-single-number": {
        "intuition": "<p>XOR cancels pairs regardless of their positions. XOR every value; all paired values disappear and the unique value remains.</p>",
        "steps": "<ol><li>Initialize result to zero.</li><li>XOR each array element into result.</li><li>Return result.</li></ol>",
        "trace": "<p>For <code>[4,1,2,1,2]</code>, the two 1s cancel and the two 2s cancel, leaving 4.</p>",
        "proof": "<p>XOR is associative and commutative, and <code>x ^ x = 0</code>. Every paired value contributes zero, while the unpaired value contributes itself.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space, matching the required bounds.</p>",
        "edge": "<p>Negative integers work with Java bitwise XOR. Test one element, the unique value at either end and arbitrary ordering. The source contract guarantees a non-empty array and exactly one unpaired value.</p>",
    },
    "a17-best-time-to-buy-and-sell-stock": {
        "intuition": "<p>For each selling day, the best earlier buy is the minimum price seen so far. The profit for that day is today's price minus that minimum.</p>",
        "steps": "<ol><li>Initialize minimum price from the first day and best profit to zero.</li><li>For each later day, calculate profit if selling today.</li><li>Update the best profit, then update the minimum price for future days.</li><li>Return the best profit.</li></ol>",
        "trace": "<p>For <code>[7,1,5,4,3,6]</code>, the minimum becomes 1. Selling at 6 yields profit 5, the best valid transaction.</p>",
        "proof": "<p>For a fixed selling day, buying at the minimum earlier price maximizes profit. The scan evaluates that optimal transaction for every selling day, so the maximum candidate is globally optimal.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Decreasing prices return 0 when no profitable trade exists. Test one day, equal prices, minimum at the first or last day and large values.</p>",
    },
    "a18-rearrange-array-elements-by-sign": {
        "intuition": "<p>The output alternates positive and negative values, starts positive and preserves the order within each sign. Separate destination indices for each sign achieve this in one pass.</p>",
        "steps": "<ol><li>Create an output array of equal length.</li><li>Set the positive write index to 0 and negative write index to 1.</li><li>Scan input left to right, writing positives to even positions and negatives to odd positions.</li><li>Return the new array.</li></ol>",
        "trace": "<p>For <code>[3,1,-2,-5,2,-4]</code>, positives fill indices 0,2,4 and negatives fill 1,3,5. The result is <code>[3,-2,1,-5,2,-4]</code>.</p>",
        "proof": "<p>Each sign uses a monotonically increasing sequence of output positions. Since values are visited in input order, their relative order is preserved. Equal counts ensure every position is filled exactly once.</p>",
        "complexity": "<p>O(n) time and O(n) auxiliary space for the returned array.</p>",
        "edge": "<p>The stated contract requires even length and equal positive/negative counts. Clarify how zero is classified if the input contract changes; the sample excludes zero.</p>",
    },
    "a20-leaders-in-array": {
        "intuition": "<p>An element is a leader when no value to its right is greater. A right-to-left scan maintains the maximum suffix value, making each leader check constant time.</p>",
        "steps": "<ol><li>Initialize the suffix maximum with the rightmost element and record it.</li><li>Scan leftward.</li><li>Record a value when it is greater than or equal to the suffix maximum.</li><li>Update the suffix maximum; reverse collected results if output must be left-to-right.</li></ol>",
        "trace": "<p>For <code>[16,17,4,3,5,2]</code>, scanning backward records 2, 5 and 17. In original order the leaders are <code>[17,5,2]</code>.</p>",
        "proof": "<p>The maintained value is the maximum of all elements strictly to the current index's right. Comparing the current value with it is exactly the leader definition; updating it preserves the invariant.</p>",
        "complexity": "<p>O(n) time and O(n) result space for a list-based implementation.</p>",
        "edge": "<p>The rightmost element is always a leader. Equal values qualify because the definition uses greater-than-or-equal. Test increasing, decreasing, all-equal and single-element arrays.</p>",
    },

    "a22-set-matrix-zeroes": {
        "intuition": "<p>A zero at (r,c) requires row r and column c to become zero. The key is to remember which rows and columns were originally marked, without allowing newly written zeros to trigger additional rows or columns.</p>",
        "steps": "<ol><li>Record whether the first row and first column originally contain zero.</li><li>Use the first cell of each remaining row and column as marker storage.</li><li>Scan the interior and mark its row/column when an original zero is found.</li><li>Zero marked rows and columns, then apply the saved first-row/first-column flags.</li></ol>",
        "trace": "<p>For <code>[[1,1,1],[1,0,1],[1,1,1]]</code>, the zero at (1,1) marks row 1 and column 1. Applying the markers yields <code>[[1,0,1],[0,0,0],[1,0,1]]</code>.</p>",
        "proof": "<p>Marker cells encode exactly which rows and columns contain an original zero. The separate flags preserve the information for the first row and first column, whose marker cells overlap. Applying markers after the discovery pass prevents newly written zeros from being mistaken for original input zeros.</p>",
        "complexity": "<p>The marker-in-first-row/column approach is O(mn) time and O(1) auxiliary space. A simpler boolean row/column array solution is O(mn) time and O(m+n) extra space.</p>",
        "edge": "<p>Test zero in the first row, first column, top-left cell, multiple zeros, no zeros, one row, one column and rectangular matrices. The source also has a sentinel-marker variant; ensure the sentinel cannot be a legitimate input value before using it.</p>",
    },
    "a24-matrix-spiral-order": {
        "intuition": "<p>Maintain the unvisited rectangle using top, bottom, left and right boundaries. Each iteration traverses one outer layer and then shrinks the rectangle inward.</p>",
        "steps": "<ol><li>Traverse the top row from left to right, then increment top.</li><li>Traverse the right column from top to bottom, then decrement right.</li><li>If rows remain, traverse the bottom row right to left, then decrement bottom.</li><li>If columns remain, traverse the left column bottom to top, then increment left.</li><li>Repeat while the boundaries still describe an unvisited cell.</li></ol>",
        "trace": "<p>For a 3×4 matrix containing 1 through 12 row-wise, the first layer is <code>1,2,3,4,8,12,11,10,9,5</code>; the remaining inner row contributes <code>6,7</code>. The full order is <code>1,2,3,4,8,12,11,10,9,5,6,7</code>.</p>",
        "proof": "<p>The four boundary traversals visit the current outer layer exactly once. Shrinking the corresponding boundary removes that layer from future consideration. The remaining rectangle is therefore precisely the set of unvisited cells.</p>",
        "complexity": "<p>O(mn) time because every cell is emitted once, and O(1) auxiliary traversal space excluding the output list.</p>",
        "edge": "<p>Test 1×1, 1×n, m×1, 2×2, rectangular matrices, and dimensions where the final layer contains only one row or one column. Guard bottom/left traversals after shrinking to avoid duplicates.</p>",
    },
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
                                  for x in re.split(r'([0-9]+)', os.path.basename(p))])
        grouped = {}
        for path in files:
            filename = os.path.basename(path)[:-5]
            base = filename.rstrip('0123456789')
            grouped.setdefault(base, []).append(path)
        catalog[slug] = []
        for base, paths in grouped.items():
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
        for number, (problem_slug, problem_title, source_paths) in enumerate(catalog[slug], 1):
            source_files = [(read(path), os.path.relpath(path, DSA_SOURCE).replace(os.sep, '/')) for path in source_paths]
            source = source_files[0][0]
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
                '<p class="dsa-code-note"><b>Original source:</b> %s</p>'
                '<p><a href="%s">Open full problem page →</a></p></article>' %
                (problem_slug, number, esc(title.upper()), esc(detail_href), number,
                 esc(problem_title), esc(summary[:500]), source_links, esc(detail_href))
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
print('DSA build: %d topics, %d problem/reference pages, %d curated problem explanations' % (len(DSA_TOPICS), sum(len(v) for v in DSA_PROBLEMS.values()), len(DSA_PROBLEM_NOTES)))
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
