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
DSA_TOPICS = [('strings', 'Strings')]
DSA_TOPICS = [t for t in DSA_TOPICS if os.path.exists(os.path.join(DSA, 'topics', t[0] + '.html'))]


def dsa_nav(cur, pre):
    """Independent DSA navigation; pre is relative to the DSA root."""
    site = pre + '../'
    o = [
        ('<a class="brand" href="%sindex.html">Data Structures and Algorithms</a>' % pre) if cur else '<div class="brand">Data Structures and Algorithms</div>',
        '<div class="tagline">Java coding problems, patterns and solutions</div>',
        '<div class="qlinks"><a href="%sindex.html">🏠 Home</a><a href="%ssearch.html">🔍 Search the whole site</a></div>' % (site, site),
    ]
    body = []
    for slug, title in DSA_TOPICS:
        cls = 'ch current' if slug == cur else 'ch'
        body.append('<a class="%s" href="%stopics/%s.html"><span class="num">%02d</span><span>%s</span></a>' %
                    (cls, pre, slug, DSA_TOPICS.index((slug, title)) + 1, esc(title)))
        if slug == cur:
            heads = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', read(os.path.join(DSA, 'topics', slug + '.html')), re.S)
            if heads:
                body.append('<div class="onpage">')
                for hid, ht in heads:
                    body.append('<a href="#%s">%s</a>' % (hid, esc(html.unescape(re.sub(r'<[^>]+>', '', ht).strip()))))
                body.append('</div>')
    if body:
        o.append('<details open><summary>Topics</summary>\n%s\n</details>' % '\n'.join(body))
    return '\n'.join(o)


dsa_stats = {}
for i, (slug, title) in enumerate(DSA_TOPICS):
    p = os.path.join(DSA, 'topics', slug + '.html')
    s = read(p)
    s = re.sub(r'<!--dnav:start-->.*?<!--dnav:end-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--dfoot:start-->.*?<!--dfoot:end-->\n?', '', s, flags=re.S)
    dsa_stats[slug] = dict(problems=len(re.findall(r'<details class="dsa-problem', s)),
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

dsa_problems = sum(v['problems'] for v in dsa_stats.values())
dsa_diagrams = sum(v['diagrams'] for v in dsa_stats.values())
dsa_cards = '\n'.join('<a class="card" href="topics/%s.html"><span class="n">Topic %02d</span><span class="t">%s</span><span class="d">%s</span><span class="d">%d problems, %d diagrams</span></a>' %
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
<p class="sub">Java coding problems organized by topic and pattern. Build problem-solving intuition, understand the invariant, practise optimized implementations and revise complexity.</p>
<div class="stats"><div class="stat"><b>%(nt)d</b><span>topics</span></div><div class="stat"><b>%(np)d</b><span>problems</span></div></div>
<div class="tl"><b>How to use this section:</b> Try each problem before opening its solution. Explain the brute-force idea, identify the pattern, implement the optimized approach, and verify it with a dry run and complexity analysis.</div>
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

\n
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
<p class="lead">One place to prepare for senior engineering interviews. Start with <b>System Design</b> (learn it in the Handbook, revise it in the Quick Notes), then practise topic by topic in the <b>Interview Book</b>: Git, Java, DSA, Spring, Kafka and more.</p>
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
