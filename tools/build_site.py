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
    },
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

    "aggressive-cows": {
        "intuition": "<p>Binary-search the answer: the minimum distance between placed cows. Feasibility is monotonic—if k cows can be placed with distance d, they can also be placed with any smaller distance.</p>",
        "steps": "<ol><li>Sort stall positions.</li><li>Search candidate minimum distances from 0 to maxPosition-minPosition.</li><li>For a candidate distance, place the first cow at the first stall, then greedily place each next cow at the earliest stall at least d away.</li><li>If at least k cows fit, try a larger distance; otherwise try a smaller one.</li></ol>",
        "trace": "<p>For stalls <code>[0,3,4,7,9,10]</code> and k=4, distance 3 allows placements at 0,3,7,10. Distance 4 cannot place all four, so the maximum feasible minimum distance is 3.</p>",
        "proof": "<p>For a fixed distance, earliest-feasible greedy placement leaves at least as much room as any alternative placement for subsequent cows. Thus it maximizes the number placed. Feasibility decreases monotonically as distance increases, making binary search valid.</p>",
        "complexity": "<p>Sorting costs O(n log n). Each feasibility check is O(n), and binary search performs O(log R) checks over distance range R. Extra space depends on sorting implementation.</p>",
        "edge": "<p>Check k=1, k=n, duplicate stall positions, unsorted input and large coordinate differences. Use a sufficiently wide type for distances.</p>",
    },
    "allocate-minimum-number-of-pages": {
        "intuition": "<p>Minimize the maximum pages assigned to any student while preserving contiguous book order. Binary-search that maximum load; feasibility is monotonic because allowing a larger limit cannot require more students.</p>",
        "steps": "<ol><li>Reject the case where students exceed the number of books.</li><li>Set the lower bound to the largest single book and upper bound to the sum of all pages.</li><li>For a candidate limit, greedily assign consecutive books to the current student until the next book would exceed the limit.</li><li>Count students required; if the count is at most m, lower the limit, otherwise raise it.</li></ol>",
        "trace": "<p>For <code>[12,34,67,90]</code> and two students, a limit of 113 permits [12,34,67] and [90]. Any smaller limit needs more than two contiguous groups, so 113 is optimal.</p>",
        "proof": "<p>The greedy feasibility check uses the fewest students possible for a fixed maximum load because each student receives the longest valid contiguous prefix. If that minimum count exceeds m, no allocation under the limit exists. Feasibility is monotonic in the limit.</p>",
        "complexity": "<p>O(n log(sumPages)) time after computing bounds; O(1) auxiliary space beyond input. Use long for the total page count if constraints require it.</p>",
        "edge": "<p>Students greater than books is impossible; one student receives all books; m equal to n gives the largest book size. Empty input and zero-page books need explicit contract handling.</p>",
    },
    "capacity-to-ship-packages-within-d-days": {
        "intuition": "<p>For a fixed ship capacity, simulate loading packages in their given order and count days. A larger capacity can never require more days, so binary-search the smallest feasible capacity.</p>",
        "steps": "<ol><li>Set the minimum capacity to the heaviest package and maximum to the sum of all weights.</li><li>For a candidate capacity, greedily load packages until the next would exceed it, then start a new day.</li><li>If required days are at most the deadline, try a smaller capacity; otherwise try a larger one.</li><li>Return the smallest feasible capacity.</li></ol>",
        "trace": "<p>For weights <code>[1,2,3,4,5,6,7,8,9,10]</code> and 5 days, capacity 15 yields groups [1..5], [6,7], [8], [9], [10]. Capacity 14 needs more than five days, so 15 is minimal.</p>",
        "proof": "<p>The greedy simulation packs the longest possible prefix each day, minimizing the number of days for a fixed capacity. Feasibility is monotonic: increasing capacity cannot increase the required day count.</p>",
        "complexity": "<p>O(n log(sumWeights)) time and O(1) auxiliary space. Use long for accumulated weights if their sum may exceed int.</p>",
        "edge": "<p>Test one day, days equal to package count, one package, a single very heavy package, and days greater than package count. Package order cannot be rearranged.</p>",
    },
    "kth-missing-positive-number": {
        "intuition": "<p>At index i, a strictly increasing positive array should contain i+1 if no positive numbers are missing. The number missing through that index is <code>arr[i]-(i+1)</code>, which is non-decreasing.</p>",
        "steps": "<ol><li>Binary-search the first index where <code>arr[i]-(i+1) &gt;= k</code>.</li><li>Values before that index have fewer than k missing positives; values from it onward have at least k.</li><li>Derive the answer from the boundary, or use a linear scan for a simpler baseline.</li></ol>",
        "trace": "<p>For <code>[2,3,4,7,11]</code> and k=5, missing counts at indices are 1,1,1,3,6. The first count reaching 5 is at index 4; the fifth missing positive is 9.</p>",
        "proof": "<p>The missing-count function is monotonic because the array is strictly increasing and each next element can increase the gap count but cannot reduce it. Binary search locates the transition from fewer than k missing values to at least k.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space for the binary-search approach; O(n) for a direct scan.</p>",
        "edge": "<p>Test k smaller than the first array value, no missing values between early elements, consecutive arrays beginning at 1, and k larger than all gaps represented by the array.</p>",
    },
    "median-of-two-sorted-arrays": {
        "intuition": "<p>Partition both sorted arrays so the left halves contain exactly half of the combined elements. A correct partition has every left-side value no greater than every right-side value.</p>",
        "steps": "<ol><li>Binary-search the partition in the smaller array and derive the complementary partition in the other array.</li><li>Read the four boundary values around the partitions, using negative/positive infinity when a side is empty.</li><li>If the left maximum of one side exceeds the right minimum of the other, move the partition in the appropriate direction.</li><li>When both cross-boundary inequalities hold, return the left maximum for odd total length or the average of the two middle boundaries for even length.</li></ol>",
        "trace": "<p>For <code>[1,3]</code> and <code>[2]</code>, choose left partitions [1] and [2]. The left maximum is 2 and the right minimum is 3, so the median is 2.</p>",
        "proof": "<p>The partition sizes ensure the left side contains half the combined elements. The two cross-boundary inequalities ensure all left values are at most all right values. Therefore the median is the maximum of the left side for odd length, or the average of that maximum and the minimum of the right side for even length.</p>",
        "complexity": "<p>O(log(min(m,n))) time and O(1) auxiliary space. Always binary-search the smaller array.</p>",
        "edge": "<p>Test one array empty, total length one, all values in one array smaller, interleaved arrays, duplicates and even-length averaging. Use a wider numeric type when adding the two middle values.</p>",
    },
    "median-in-row-wise-sorted-matrix": {
        "intuition": "<p>Each row is sorted, but the matrix as a whole may not be. Binary-search the value domain and count how many matrix elements are less than or equal to a candidate using a binary search in each row.</p>",
        "steps": "<ol><li>Find the minimum first-column value and maximum last-column value to bound the answer.</li><li>Binary-search a candidate value.</li><li>For each row, use upper bound to count values less than or equal to the candidate.</li><li>If the count is at most half the total elements, search higher; otherwise search lower.</li></ol>",
        "trace": "<p>For <code>[[1,3,5],[2,6,9],[3,6,9]]</code>, the sorted multiset is [1,2,3,3,5,6,6,9,9]. The middle value is 5.</p>",
        "proof": "<p>The count of elements at most x is monotonic in x. The median is the smallest value for which that count exceeds half the matrix size. Binary search over values finds this threshold.</p>",
        "complexity": "<p>O(r log c log(valueRange)) time and O(1) auxiliary space, assuming each row is sorted. The source problem specifies odd row and column counts.</p>",
        "edge": "<p>Test one row, one column, duplicates, negative values, large value ranges and rectangular dimensions. Do not assume columns are sorted.</p>",
    },
    "minimum-days-to-make-bouquets": {
        "intuition": "<p>For a candidate day, a flower is available if its bloom day is no greater than that candidate. Scan contiguous available flowers to count bouquets of k adjacent flowers. Feasibility is monotonic as days increase.</p>",
        "steps": "<ol><li>If m*k exceeds the number of flowers, return -1 (use wide arithmetic for the product).</li><li>Binary-search between the minimum and maximum bloom days.</li><li>For a candidate day, count consecutive bloomed flowers and add one bouquet each time k adjacent flowers are collected.</li><li>If at least m bouquets can be made, search earlier days; otherwise search later days.</li></ol>",
        "trace": "<p>For bloom days <code>[1,10,3,10,2]</code>, m=3 and k=1, day 3 is sufficient: flowers at positions 0,2,4 have bloomed. Earlier than day 3, fewer than three flowers are available.</p>",
        "proof": "<p>For a fixed day, the scan counts disjoint groups of k consecutive bloomed flowers from left to right. If a day is feasible, every later day is also feasible because additional flowers can only become available. Binary search therefore finds the earliest feasible day.</p>",
        "complexity": "<p>O(n log D) time where D is the bloom-day range, and O(1) auxiliary space.</p>",
        "edge": "<p>Test impossible m*k, m=1, k=1, all flowers blooming on the same day, separated runs and integer overflow in m*k.</p>",
    },
    "minimum-in-sorted-rotated-array": {
        "intuition": "<p>In a rotated strictly increasing array, the minimum is the only element smaller than its predecessor. Compare the midpoint with the right boundary to determine which side contains the pivot.</p>",
        "steps": "<ol><li>Set low and high to the array bounds.</li><li>If nums[mid] is greater than nums[high], the minimum lies to the right; set low to mid+1.</li><li>Otherwise the minimum is at mid or to its left; set high to mid.</li><li>When low equals high, that index contains the minimum.</li></ol>",
        "trace": "<p>For <code>[4,5,6,7,0,1,2]</code>, midpoint 7 is greater than the rightmost value 2, so search right. The interval converges to index 4, containing 0.</p>",
        "proof": "<p>If nums[mid] exceeds nums[high], the sorted segment cannot contain the rotation drop before mid, so the minimum is to its right. Otherwise the interval from mid through high is sorted and mid is a valid candidate, so discarding the right half beyond mid is safe.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space for distinct values.</p>",
        "edge": "<p>Test an unrotated array, rotation by one, minimum at either boundary, one element and empty input. Duplicate values require a different comparison rule and can degrade the worst case to O(n).</p>",
    },
    "nth-square-root": {
        "intuition": "<p>For non-negative M, the integer nth root is the value x such that x^n=M exactly. Binary-search candidate x and compare its power with M, stopping early if multiplication already exceeds M.</p>",
        "steps": "<ol><li>Handle invalid exponent and negative-input semantics explicitly.</li><li>Search candidate roots in a safe interval, such as 0 through M for M greater than 1.</li><li>Compute x^n with overflow-aware multiplication and stop once it exceeds M.</li><li>If the power equals M, return x; otherwise narrow the search.</li><li>Return -1 if no integer root exists.</li></ol>",
        "trace": "<p>For n=3 and M=27, candidate 3 gives 3×3×3=27, so return 3. For n=3 and M=28, no integer candidate has an exact cube equal to 28, so return -1.</p>",
        "proof": "<p>For non-negative candidates, x^n is monotonic in x. Binary search can therefore discard candidates below or above the target. Returning only on exact equality enforces the integer-root requirement.</p>",
        "complexity": "<p>O(n log M) time for repeated multiplication during binary search and O(1) auxiliary space. Overflow must be detected before it corrupts comparisons.</p>",
        "edge": "<p>Test M=0, M=1, exponent 1, perfect and non-perfect powers, exponent larger than M, and negative M. Confirm the problem's convention for negative values and even/odd exponents.</p>",
    },
    "peak-element": {
        "intuition": "<p>A peak is greater than its neighbours. Compare the midpoint with its right neighbour: if the slope rises, a peak must exist to the right; otherwise a peak exists at mid or to the left.</p>",
        "steps": "<ol><li>Binary-search while low is less than high.</li><li>If nums[mid] is less than nums[mid+1], move low to mid+1.</li><li>Otherwise move high to mid.</li><li>Return low when the interval converges.</li></ol>",
        "trace": "<p>For <code>[1,2,3,1]</code>, the slope rises through the midpoint, moving the search right until index 2 is found. Value 3 is greater than both neighbours.</p>",
        "proof": "<p>On an increasing slope, moving right cannot lose all peaks: following the slope must eventually reach a local maximum or the right boundary, which is treated as negative infinity beyond the array. On a falling or flat-to-lower step, mid is on a side from which a peak exists at or to its left. The interval always retains at least one peak.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test one element, strictly increasing, strictly decreasing, multiple peaks and peaks at either endpoint. The source contract defines outside neighbours as negative infinity and asks for any peak.</p>",
    },
    "a26-majority-element2": {
        "intuition": "<p>There can be at most two values occurring more than floor(n/3) times. The extended Boyer–Moore algorithm tracks two candidates and cancels groups of three distinct values.</p>",
        "steps": "<ol><li>Maintain two candidates with two counters.</li><li>Increment a matching candidate; otherwise fill an empty candidate slot.</li><li>If neither matches and both slots are occupied, decrement both counters.</li><li>Count the final candidates in a second pass and return only those whose frequency exceeds n/3.</li></ol>",
        "trace": "<p>For <code>[1,1,1,3,3,2,2,2]</code>, the surviving candidates are 1 and 2. A verification pass confirms each appears more than 8/3 times.</p>",
        "proof": "<p>Removing any group of three distinct values cannot eliminate every occurrence of a value that appears more than n/3 times. At most two such frequent values can exist, so two candidate slots suffice. The final verification is necessary because candidates may survive even when no qualifying value exists.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space, excluding the returned list.</p>",
        "edge": "<p>Test no qualifying value, exactly one, two qualifying values, all values equal and negative values. Always verify candidate counts unless the problem explicitly guarantees their existence.</p>",
    },
    "a27-triplet-sum-in-array": {
        "intuition": "<p>After sorting, fix one element and use two pointers to find whether two remaining values complete the target sum. Sorting makes it possible to move a pointer based on whether the current sum is too small or too large.</p>",
        "steps": "<ol><li>Sort the array.</li><li>For each index i, initialize left=i+1 and right=n-1.</li><li>Compute the three-value sum using long arithmetic.</li><li>If it equals target, report success; if smaller, increment left; if larger, decrement right.</li></ol>",
        "trace": "<p>For <code>[1,4,45,6,10,8]</code> and target 22, after sorting, the triplet 4, 8 and 10 sums to 22.</p>",
        "proof": "<p>For a fixed first value, the remaining values are sorted. If the sum is too small, increasing the left value is the only direction that can increase the sum; if too large, decreasing the right value can reduce it. This explores all possible pairs for each fixed index without nested pair enumeration.</p>",
        "complexity": "<p>O(n log n) for sorting plus O(n²) for the fixed-index two-pointer scan; O(1) auxiliary space if sorting in place (excluding sort implementation details).</p>",
        "edge": "<p>Use long for the sum to avoid integer overflow. Test fewer than three elements, duplicates, negative values, no solution and multiple valid triplets. Clarify whether the task asks for existence, count or all unique triplets.</p>",
    },
    "find-duplicates-in-an-array-from0to-n": {
        "intuition": "<p>The repository title suggests a bounded integer domain. The correct strategy depends on the exact constraint: a frequency structure is straightforward, while in-place marking or cyclic placement may reduce extra space when the value range permits it.</p>",
        "steps": "<ol><li>Confirm the precise range and duplicate-count contract from the source method.</li><li>Choose a frequency/counting approach if extra space is allowed.</li><li>If the source uses index marking, explain how the value maps to a visited index and how mutation is restored if required.</li><li>Return duplicates according to the stated output convention.</li></ol>",
        "trace": "<p>For a bounded example <code>[0,1,2,1,3]</code>, a frequency scan identifies 1 as repeated. The exact output order and whether each duplicate is emitted once must follow the source contract.</p>",
        "proof": "<p>A frequency-based solution is correct because a value is reported exactly when its count crosses the required repetition threshold. In-place variants require a separate proof that their index encoding is collision-safe under the documented range.</p>",
        "complexity": "<p>Depends on the implementation in the source file. State the actual method's time and auxiliary-space costs rather than assuming the title implies a particular technique.</p>",
        "edge": "<p>Check the minimum and maximum allowed value, repeated values occurring more than twice, multiple distinct duplicates, mutation requirements and whether the input guarantees exactly one duplicate.</p>",
    },
    "find-smallest-letter-greater-than-target": {
        "intuition": "<p>The answer is the first character strictly greater than target in a sorted character array. If no such character exists, the answer wraps to the first character.</p>",
        "steps": "<ol><li>Binary-search for the first index whose character is greater than target.</li><li>When the middle character is greater, save it and search left.</li><li>Otherwise search right.</li><li>Return the saved character, or the first array element when the search reaches the end.</li></ol>",
        "trace": "<p>For <code>['c','f','j']</code> and target 'd', the first character greater than 'd' is 'f'. For target 'j', the search reaches the end and wraps to 'c'.</p>",
        "proof": "<p>Sorted order means all characters at or before a qualifying boundary are no greater than target, while all characters at or after it are greater. Binary search finds the first qualifying index; wraparound handles the no-candidate case.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test target smaller than the first character, equal to a character, between adjacent characters, equal to or greater than the final character, and duplicate characters. The array must be non-empty and sorted.</p>",
    },
    "find-transition-point": {
        "intuition": "<p>In a binary array consisting of zeros followed by ones, the transition point is the first index containing 1. This is a lower-bound search for the predicate value == 1.</p>",
        "steps": "<ol><li>Set low to 0 and high to n-1.</li><li>If the middle value is 1, save mid and continue left.</li><li>If it is 0, continue right.</li><li>Return the first-one index, or -1 if no 1 exists.</li></ol>",
        "trace": "<p>For <code>[0,0,0,1,1]</code>, the first one is at index 3, so the transition point is 3.</p>",
        "proof": "<p>The zero-to-one ordering makes the predicate monotonic: once an index contains 1, every later index also contains 1. Binary search finds the first true position.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test all zeros (answer -1), all ones (answer 0), empty input, one element and the transition at either boundary. The monotonic binary-array contract is essential.</p>",
    },
    "max-sum-subarray-of-size-k": {
        "intuition": "<p>Every candidate has exactly k consecutive elements. Sliding the window avoids recomputing each sum from scratch: subtract the element leaving and add the element entering.</p>",
        "steps": "<ol><li>Compute the sum of the first k elements.</li><li>Initialize the maximum with that sum.</li><li>For each next index, subtract the outgoing value and add the incoming value.</li><li>Update the maximum after each shift.</li></ol>",
        "trace": "<p>For <code>[100,200,300,400]</code> and k=2, the window sums are 300, 500 and 700. The maximum is 700.</p>",
        "proof": "<p>After each shift, the maintained sum equals exactly the k elements in the current window because one value leaves and one enters. Every length-k contiguous subarray appears once as the window slides, so the maximum is found.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space after initializing the first window.</p>",
        "edge": "<p>Check k=1, k=n, invalid k values, negative values and integer overflow. Initialize the maximum to the first window sum rather than zero so all-negative arrays work.</p>",
    },
    "minimum-distance-between-two-numbers": {
        "intuition": "<p>The minimum distance between occurrences of x and y can be found in one scan. When one target is encountered, compare it with the most recent occurrence of the other target.</p>",
        "steps": "<ol><li>Track the latest index of x and y, initially -1.</li><li>When the current value equals x, update its latest index and compare with the latest y index.</li><li>Do the symmetric operation for y.</li><li>Return the minimum absolute index difference, or the source's not-found sentinel.</li></ol>",
        "trace": "<p>For <code>[1,2,3,2,1]</code>, x=1 and y=2, adjacent occurrences at indices 0 and 1 give distance 1; later occurrences do not improve it.</p>",
        "proof": "<p>For any occurrence of x, the closest y occurrence on its left is the most recent y seen so far; a farther-left y cannot yield a smaller distance. Scanning also evaluates the symmetric case when y is encountered.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test x==y separately because the interpretation may change; test either value absent, multiple occurrences, adjacent occurrences and arrays of length one. Match the source's required return value when no pair exists.</p>",
    },
    "minimum-number-of-jumps": {
        "intuition": "<p>For the classic minimum-jumps problem, each index tells how far it can reach. A greedy scan tracks the farthest reachable index and the end of the current jump layer; when the current layer ends, one more jump is required.</p>",
        "steps": "<ol><li>Track the farthest index reachable so far, the end of the current jump range and the number of jumps.</li><li>At each index, extend farthest with <code>i + arr[i]</code>.</li><li>When i reaches the current range end, increment jumps and move the range end to farthest.</li><li>If farthest does not advance, the destination is unreachable; follow the source contract for that case.</li></ol>",
        "trace": "<p>For <code>[2,3,1,1,4]</code>, the first jump can reach indices 1 or 2. From index 1, the farthest reach becomes index 4, so the destination is reached in two jumps.</p>",
        "proof": "<p>Indices in the current range are exactly those reachable with the current number of jumps. Extending to the farthest reach gives the largest next range available with one additional jump; choosing a shorter reach cannot improve the number of jumps.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space for the greedy approach.</p>",
        "edge": "<p>Test a single element (zero jumps), a zero at the start, a zero that blocks progress, an already reachable destination and large jump values. Confirm whether unreachable input returns -1 or another sentinel.</p>",
    },
    "kth-element-of-two-sorted-arrays": {
        "intuition": "<p>The kth element in the merged order can be found without building the merged array. Choose how many elements to take from each array so the left partition contains exactly k elements and every left value is no greater than every right value.</p>",
        "steps": "<ol><li>Binary-search the number of elements taken from the smaller array.</li><li>Let the other partition take k minus that count.</li><li>Inspect the four boundary values around the partitions.</li><li>If the left maximum of one array exceeds the right minimum of the other, adjust the partition; otherwise the kth value is the maximum of the two left boundaries.</li></ol>",
        "trace": "<p>For <code>[2,3,45]</code>, <code>[4,6,7,8]</code> and k=4 (1-based), the correct partition has left side values 2,3,4,6; its maximum is 6.</p>",
        "proof": "<p>A valid partition contains exactly k elements on the left and satisfies both cross-array ordering inequalities. Therefore those k values are exactly the k smallest values in the combined order, and their maximum is the kth element.</p>",
        "complexity": "<p>O(log(min(n,m))) time and O(1) auxiliary space. The implementation must handle empty partitions using negative/positive infinity sentinels.</p>",
        "edge": "<p>Validate 1 ≤ k ≤ n+m. Test one array empty, k=1, k=n+m, all values in one array smaller than the other, duplicates and unequal array lengths. The problem uses 1-based k.</p>",
    },
    "kth-missing-positive-number": {
        "intuition": "<p>At index i (0-based), the number of missing positive integers before arr[i] is <code>arr[i] - (i+1)</code>. This count is non-decreasing, so binary search finds the first index where at least k numbers are missing.</p>",
        "steps": "<ol><li>Binary-search indices from 0 to n-1.</li><li>Compute missing count as <code>arr[mid] - mid - 1</code>.</li><li>If the count is below k, search right; otherwise search left.</li><li>After the boundary, derive the answer from the number of missing values before that index.</li></ol>",
        "trace": "<p>For <code>[2,3,4,7,11]</code> and k=5, missing counts at indices are 1,1,1,3,6. The boundary lies at index 4; the fifth missing positive is 9.</p>",
        "proof": "<p>The missing-count function is monotonic because the array is strictly increasing. The boundary separates indices with fewer than k missing values from those with at least k; the arithmetic after that boundary gives the kth absent positive integer.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space for the binary-search variant. A linear scan is simpler but O(n).</p>",
        "edge": "<p>Test k smaller than the first array value, k larger than all missing values before the last element, consecutive starting at 1, and a single element. Input must be strictly increasing and positive.</p>",
    },
    "median-of-two-sorted-arrays": {
        "intuition": "<p>The median is determined by the middle one or two values of the combined sorted order. A partition-based binary search finds a split with half the elements on the left and all left values no greater than all right values.</p>",
        "steps": "<ol><li>Binary-search the partition in the smaller array.</li><li>Choose the complementary partition in the other array so the left side contains half the total elements.</li><li>Compare the left and right boundary values from both arrays.</li><li>If the partition is valid, return the maximum left value for odd total length, or the average of maximum-left and minimum-right for even length.</li><li>Otherwise move the partition in the direction indicated by the crossed boundaries.</li></ol>",
        "trace": "<p>For <code>[1,2]</code> and <code>[3,4]</code>, the combined order is [1,2,3,4]. The two middle values are 2 and 3, so the median is 2.5.</p>",
        "proof": "<p>A valid partition puts exactly half the elements on the left (or one extra for odd length) and guarantees every left value is at most every right value. Thus the median is precisely the boundary value(s) between the two halves.</p>",
        "complexity": "<p>O(log(min(m,n))) time and O(1) auxiliary space. Avoid physically merging the arrays.</p>",
        "edge": "<p>Test one array empty, both arrays of different sizes, odd/even total length, duplicates, disjoint ranges and negative values. Use safe sentinels for empty partition sides and widen before adding the two middle values.</p>",
    },
    "minimum-in-sorted-rotated-array": {
        "intuition": "<p>A rotation of a strictly increasing array contains two sorted runs. Compare the middle value with the rightmost value to decide which side contains the minimum.</p>",
        "steps": "<ol><li>Set low and high to the array bounds.</li><li>If nums[mid] is greater than nums[high], the minimum lies to the right of mid.</li><li>Otherwise the minimum is at mid or to its left, so set high=mid.</li><li>When low equals high, that position is the minimum.</li></ol>",
        "trace": "<p>For <code>[4,5,6,7,0,1,2]</code>, mid initially points to 7, which is greater than the rightmost 2, so search right. The interval eventually converges on 0.</p>",
        "proof": "<p>When nums[mid] exceeds nums[high], the sorted rotation boundary must lie strictly to the right of mid. Otherwise the segment from mid through high is sorted and nums[mid] cannot be the minimum unless it is the leftmost candidate; retaining mid and searching left is safe.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space for distinct values.</p>",
        "edge": "<p>Test no rotation, rotation by one, minimum at either endpoint, one element and empty input. The standard comparison may degrade with duplicates; this source contract specifies unique elements.</p>",
    },
    "peak-element": {
        "intuition": "<p>A peak is greater than its neighbours. Compare the middle element with its right neighbour: an upward slope guarantees a peak to the right; a downward slope guarantees a peak at or to the left.</p>",
        "steps": "<ol><li>Binary-search the index range.</li><li>If nums[mid] is greater than nums[mid+1], keep the left half including mid.</li><li>Otherwise keep the right half beginning at mid+1.</li><li>When the interval converges, return that peak index.</li></ol>",
        "trace": "<p>For <code>[1,2,3,1]</code>, the slope rises toward 3 and then falls, so the search converges to index 2.</p>",
        "proof": "<p>If the slope rises from mid to mid+1, following the slope right must eventually reach a local maximum or the boundary, which is treated as negative infinity. If it falls, a peak exists on the left side including mid. Each decision therefore retains at least one peak.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test a strictly increasing array (peak at last index), strictly decreasing array (peak at first), one element and multiple peaks. The source problem guarantees adjacent values differ for the standard binary-search argument.</p>",
    },
    "search-a2d-matrix": {
        "intuition": "<p>Because each row is sorted and each row starts after the previous row ends, the matrix is globally sorted when read row by row. Treat it as a virtual one-dimensional array.</p>",
        "steps": "<ol><li>Let total elements be m*n and binary-search virtual indices from 0 to m*n-1.</li><li>Map index mid to row <code>mid / n</code> and column <code>mid % n</code>.</li><li>Compare that matrix value with target and adjust the binary-search bounds.</li><li>Return true on a match, otherwise false.</li></ol>",
        "trace": "<p>For <code>[[1,3,5,7],[10,11,16,20],[23,30,34,60]]</code>, target 3 maps to virtual index 1 (row 0, column 1), so it is found.</p>",
        "proof": "<p>The row-boundary condition guarantees that the virtual sequence is sorted. The index mapping is a bijection between [0,m*n) and all matrix cells, so ordinary binary search remains valid.</p>",
        "complexity": "<p>O(log(m*n)) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test one row, one column, first/last cell, target between row boundaries, missing target and empty dimensions if permitted. Use care with m*n integer overflow for very large dimensions.</p>",
    },
    "aggressive-cows": {
        "intuition": "<p>Sort stall positions and binary-search the minimum separation. Feasibility is monotonic: if cows can be placed with distance d, they can also be placed with any smaller distance.</p>",
        "steps": "<ol><li>Sort stall positions.</li><li>Search candidate minimum distances between 0 and maxPosition-minPosition.</li><li>For a candidate d, greedily place the first cow at the first stall, then each next cow at the earliest stall at least d away.</li><li>If at least k cows fit, try a larger distance; otherwise reduce it.</li></ol>",
        "trace": "<p>For stalls <code>[0,3,4,7,9,10]</code> and k=4, placing at 0,3,7,10 achieves minimum distance 3. A distance of 4 cannot place all four cows.</p>",
        "proof": "<p>For a fixed d, earliest-feasible placement leaves maximum remaining room for later cows, so the greedy check succeeds whenever any placement can succeed. Feasibility is monotonic in d, making binary search valid.</p>",
        "complexity": "<p>O(n log n + n log R) time, where R is the coordinate range; O(1) or O(log n) auxiliary space depending on sorting implementation.</p>",
        "edge": "<p>Check k=2, k=n, duplicate stall coordinates, unsorted input and coordinate ranges large enough to require long arithmetic. The number of stalls must be at least k.</p>",
    },
    "capacity-to-ship-packages-within-d-days": {
        "intuition": "<p>For a chosen ship capacity, greedily load packages in order until the next package would exceed capacity, then start a new day. The minimum feasible capacity is found by binary-searching a monotonic condition.</p>",
        "steps": "<ol><li>Set the lower bound to the heaviest package and upper bound to the sum of all weights.</li><li>For a candidate capacity, simulate loading packages in their original order and count required days.</li><li>If required days are at most the allowed days, try a smaller capacity.</li><li>Otherwise increase capacity.</li></ol>",
        "trace": "<p>For weights 1 through 10 and 5 days, capacity 15 allows loads [1..5], [6,7], [8], [9], [10]. Capacity 14 needs more than five days under the required order.</p>",
        "proof": "<p>Greedy packing maximizes the amount loaded each day without violating order or capacity, so it uses the fewest days for that capacity. If a capacity is feasible, every larger capacity is feasible; binary search finds the smallest feasible value.</p>",
        "complexity": "<p>O(n log(sum(weights)-max(weights))) time and O(1) auxiliary space. Use long for the total weight when constraints may exceed int.</p>",
        "edge": "<p>Test one package, days=1, days equal to package count, a single very heavy package and invalid days fewer than one. A package cannot be split across days.</p>",
    },
    "allocate-minimum-number-of-pages": {
        "intuition": "<p>Books must be assigned contiguously and each student must receive at least one book. Binary-search the maximum pages allowed per student; a greedy scan determines how many students that limit requires.</p>",
        "steps": "<ol><li>If students exceed books, return -1 because every student needs at least one book.</li><li>Set low to the largest book and high to the sum of pages.</li><li>For a candidate maximum, greedily add consecutive books until the next would exceed it, then allocate a new student.</li><li>If the required student count is at most m, try a smaller maximum; otherwise increase it.</li></ol>",
        "trace": "<p>For pages <code>[12,34,67,90]</code> and 2 students, the best split is [12,34,67] and [90], giving a maximum of 113.</p>",
        "proof": "<p>For a fixed page limit, greedy contiguous allocation minimizes the number of students needed because each student receives the longest feasible prefix. Feasibility is monotonic: increasing the limit cannot require more students. Binary search therefore finds the minimum feasible maximum.</p>",
        "complexity": "<p>O(n log(sum(pages)-max(pages))) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test students greater than books, one student, one book per student, large page totals and empty input. Use long for sums where constraints require it. Some formulations require exactly m non-empty groups; if greedy uses fewer than m and m≤n, groups can be split without increasing the maximum.</p>",
    },

    "a23-rotate-image-clockwise": {
        "intuition": "<p>A 90-degree clockwise rotation maps each cell (r,c) to (c,n-1-r). For a square matrix, transpose it and then reverse every row to achieve that mapping in place.</p>",
        "steps": "<ol><li>Transpose the matrix by swapping only entries above the main diagonal with their mirrored entries below it.</li><li>Reverse each row.</li><li>Return the modified matrix.</li></ol>",
        "trace": "<p>For <code>[[1,2,3],[4,5,6],[7,8,9]]</code>, transposition gives [[1,4,7],[2,5,8],[3,6,9]]. Reversing each row yields <code>[[7,4,1],[8,5,2],[9,6,3]]</code>.</p>",
        "proof": "<p>Transposition maps (r,c) to (c,r); reversing each row maps the transposed coordinate to (c,n-1-r). This is exactly the clockwise rotation mapping.</p>",
        "complexity": "<p>The transpose-and-reverse approach is O(n²) time and O(1) auxiliary space. The source also contains an auxiliary-matrix variant using O(n²) extra space.</p>",
        "edge": "<p>The operation assumes an n×n square matrix. Test n=1, n=2, odd/even dimensions and confirm whether mutation in place is required.</p>",
    },
    "a23-rotate-image-anti-clock-wise": {
        "intuition": "<p>A 90-degree counter-clockwise rotation maps (r,c) to (n-1-c,r). Transpose the matrix and reverse each column, or use the equivalent row-reversal/transpose order.</p>",
        "steps": "<ol><li>Transpose the square matrix.</li><li>Reverse each column from top to bottom.</li><li>Return the matrix.</li></ol>",
        "trace": "<p>For <code>[[1,2,3],[4,5,6],[7,8,9]]</code>, the counter-clockwise result is <code>[[3,6,9],[2,5,8],[1,4,7]]</code>.</p>",
        "proof": "<p>Transposition swaps coordinates. Reversing each column maps the transposed coordinate to (n-1-c,r), the required counter-clockwise destination.</p>",
        "complexity": "<p>O(n²) time and O(1) auxiliary space for the in-place method.</p>",
        "edge": "<p>The source problem requires a square matrix and no extra matrix. Test 1×1, 2×2, odd/even sizes and verify that the transformation is not accidentally clockwise.</p>",
    },
    "pythagorean-triplet": {
        "intuition": "<p>For a triplet a²+b²=c², sort the squared values. Fix the largest square as c² and use two pointers to find two smaller squares whose sum equals it.</p>",
        "steps": "<ol><li>Square each value, ensuring the multiplication uses a wide type.</li><li>Sort the squared values.</li><li>For each rightmost value as c², set left and middle pointers at the ends of the remaining prefix.</li><li>Move the pointer that makes the sum approach c² until a match is found or the interval closes.</li></ol>",
        "trace": "<p>For values <code>[3,1,4,6,5]</code>, the squares include 9,1,16,36,25. The values 9 and 16 sum to 25, so 3,4,5 form a Pythagorean triplet.</p>",
        "proof": "<p>After sorting, for a fixed c², if the two-pointer sum is too small, increasing the smaller square is the only safe way to increase it. If too large, decreasing the larger square is safe. Trying each possible largest square covers every triplet.</p>",
        "complexity": "<p>O(n²) time after O(n log n) sorting. The source squares values in the input array, so it mutates input. Use long for squares and sums to avoid overflow.</p>",
        "edge": "<p>Test duplicates, no triplet, negative values if allowed (squaring removes sign), zero values and large magnitudes. The three values must come from different indices.</p>",
    },
    "subarray-with-given-sum": {
        "intuition": "<p>The source contract restricts values to positive integers. A sliding window works because expanding right increases the sum and shrinking left decreases it. This monotonicity would not hold with negative values.</p>",
        "steps": "<ol><li>Initialize left=0 and running sum=0.</li><li>Expand right, adding each value.</li><li>While the sum exceeds target, subtract the leftmost value and advance left.</li><li>When the sum equals target, return the 1-based start and end indices.</li><li>If no window matches, return [-1].</li></ol>",
        "trace": "<p>For <code>[1,2,3,7,5]</code> and target 12, the window [2,3,7] sums to 12. Its 1-based positions are 2 through 4.</p>",
        "proof": "<p>With positive values, any window whose sum is too large can only become smaller by removing its leftmost value; any window whose sum is too small can only become larger by extending right. Thus the two pointers do not skip a valid first-occurring window.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space, excluding the returned index list.</p>",
        "edge": "<p>Test target equal to one value, match at either boundary, no match, multiple matches (return the earliest by left-to-right contract), and target zero. Do not reuse this sliding-window proof for signed arrays.</p>",
    },
    "l10-middle-element-of-linked-list": {
        "intuition": "<p>Use two pointers: slow advances one node at a time and fast advances two. When fast reaches the end, slow is at the middle. This naturally returns the second middle for even-length lists.</p>",
        "steps": "<ol><li>Initialize slow and fast at the head.</li><li>While fast and fast.next exist, move slow by one and fast by two.</li><li>Return slow.</li></ol>",
        "trace": "<p>For <code>1→2→3→4→5→6</code>, slow visits 1, 2, 3, 4 while fast visits 1, 3, 5 and then passes the end. Slow points to 4, the second middle.</p>",
        "proof": "<p>Fast moves twice as many links as slow. When fast has traversed the list, slow has traversed half as many, so it reaches the middle. The loop condition makes the even-length case stop at the second middle.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty, one node, two nodes, odd length and even length. The required convention here is the second middle when the length is even.</p>",
    },
    "l11-reverse-singly-linked-list-iterative": {
        "intuition": "<p>Reverse each next pointer while traversing once. Keep the already reversed prefix in prev and save the unprocessed suffix before changing a link.</p>",
        "steps": "<ol><li>Initialize prev=null and current=head.</li><li>Save current.next in next.</li><li>Point current.next to prev.</li><li>Advance prev=current and current=next.</li><li>When current becomes null, prev is the new head.</li></ol>",
        "trace": "<p>For <code>1→2→3</code>, after the first iteration: 1→null; after the second: 2→1; after the third: 3→2→1. Return node 3.</p>",
        "proof": "<p>At each iteration, prev is the head of the reversed prefix and current begins the untouched suffix. Saving next before rewiring preserves access to the suffix. Each step moves one node from the suffix to the front of the prefix; at termination the suffix is empty.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Empty and single-node lists return unchanged. Test two nodes, longer lists and ensure the old head becomes the tail with next=null. The source includes stack/deque-style alternatives as well as pointer reversal; explain the actual selected method's space cost.</p>",
    },
    "l13-detect-loop-in-linked-list": {
        "intuition": "<p>Floyd's tortoise-and-hare algorithm detects a cycle with two pointers moving at different speeds. If a cycle exists, the faster pointer eventually catches the slower one.</p>",
        "steps": "<ol><li>Initialize slow and fast at the head.</li><li>Move slow one link and fast two links while fast and fast.next exist.</li><li>If they meet, a cycle exists.</li><li>If fast reaches null, the list is acyclic.</li></ol>",
        "trace": "<p>For a list whose tail points back to the second node, fast gains one node per iteration relative to slow while both are inside the cycle; eventually their references become equal.</p>",
        "proof": "<p>Inside a cycle of length L, the relative distance between fast and slow changes by one modulo L per iteration. It must eventually become zero, so they meet. In an acyclic list, fast eventually reaches null.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space. A HashSet alternative uses O(n) extra space.</p>",
        "edge": "<p>Test empty list, one node without a loop, a self-loop, a loop beginning at the head and a loop beginning in the middle. Compare node references, not node values.</p>",
    },
    "l14-first-node-in-loop": {
        "intuition": "<p>After Floyd's pointers meet inside a cycle, reset one pointer to the head. Move both one step at a time; their next meeting is the cycle entry.</p>",
        "steps": "<ol><li>Run Floyd's cycle-detection phase.</li><li>If no meeting occurs, return the no-cycle result.</li><li>Reset one pointer to head while leaving the other at the meeting node.</li><li>Advance both one link at a time until they meet; that node is the loop entry.</li></ol>",
        "trace": "<p>For <code>1→3→2→4→5</code> with 5 pointing back to 3, the first Floyd meeting is somewhere inside the cycle. Resetting one pointer to 1 and advancing both one step at a time makes them meet at node 3.</p>",
        "proof": "<p>Let the non-cycle prefix length be μ and the cycle length be λ. At the first meeting, the slow pointer has travelled μ+t and the fast pointer 2(μ+t); their difference is a multiple of λ. This implies the meeting point is t links before the entry modulo λ. Advancing one pointer from head and one from the meeting point by equal distances makes them meet at the entry.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test no cycle, self-loop, cycle beginning at head, cycle after a long prefix and a cycle of length one. Return node identity or its value according to the method contract.</p>",
    },
    "l16-linked-list-is-palindrome": {
        "intuition": "<p>A palindrome reads the same from both ends. An O(1)-space approach finds the midpoint, reverses the second half, compares both halves, and optionally restores the original links.</p>",
        "steps": "<ol><li>Use slow/fast pointers to find the midpoint.</li><li>Reverse the second half of the list.</li><li>Compare nodes from the head and from the reversed half until the latter ends.</li><li>Return false on the first mismatch; restore the second half if the API should preserve input.</li></ol>",
        "trace": "<p>For <code>1→2→2→1</code>, split around the middle and reverse the second half. Compare 1 with 1, then 2 with 2: all pairs match, so it is a palindrome.</p>",
        "proof": "<p>Reversing the second half aligns corresponding nodes from opposite ends. Equality at every aligned pair is equivalent to the original sequence being symmetric; one mismatch disproves symmetry.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space for in-place reversal. A stack/array comparison is simpler but uses O(n) extra space.</p>",
        "edge": "<p>Empty and one-node lists are palindromes. Test even and odd lengths, first/last mismatch and repeated values. Consider restoring the list even when a mismatch is found.</p>",
    },
    "l18-nth-node-from-end": {
        "intuition": "<p>Keep two pointers n nodes apart. When the leading pointer reaches the end, the trailing pointer is at the nth node from the end.</p>",
        "steps": "<ol><li>Advance fast by n nodes; if it cannot, n exceeds the list length.</li><li>Move fast and slow together until fast reaches null.</li><li>Return slow's value/node as required.</li></ol>",
        "trace": "<p>For <code>1→2→3→4→5</code> and n=2, advance fast to node 2, then move both together. Fast reaches null when slow is at node 4, the second node from the end.</p>",
        "proof": "<p>The distance between fast and slow remains n links. When fast is at the end, exactly n nodes (counting the slow node) remain from slow through the tail, so slow is the desired node.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test n=1, n equal to list length, n greater than length, empty list and invalid n≤0. Follow the source's sentinel for an out-of-range request.</p>",
    },
    "l19-remove-nth-node-from-end": {
        "intuition": "<p>A dummy node simplifies deletion when the target is the head. Keep fast n+1 links ahead of slow; when fast reaches null, slow is immediately before the node to remove.</p>",
        "steps": "<ol><li>Create a dummy node pointing to head.</li><li>Start fast and slow at dummy; advance fast n+1 steps.</li><li>Move both until fast is null.</li><li>Bypass slow.next and return dummy.next.</li></ol>",
        "trace": "<p>For <code>[1,2,3,4,5]</code> and n=2, slow stops at node 3, whose next node 4 is removed. The resulting list is <code>[1,2,3,5]</code>.</p>",
        "proof": "<p>The n+1 pointer gap ensures that when fast reaches null, slow is one node before the nth node from the end. Updating one next reference removes exactly that node; the dummy handles removal of the original head uniformly.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test deleting the head, deleting the tail, a one-node list, n equal to length and invalid n. Validate n before advancing fast if the API does not guarantee a valid position.</p>",
    },
    "l22-intersection-point-of-yll": {
        "intuition": "<p>Two singly linked lists that intersect share the same physical tail from their first common node onward. Pointer switching aligns traversal distances without computing lengths.</p>",
        "steps": "<ol><li>Initialize pointers a and b at the two heads.</li><li>Advance each by one node.</li><li>When a reaches null, redirect it to headB; when b reaches null, redirect it to headA.</li><li>They meet at the shared node, or both become null if there is no intersection.</li></ol>",
        "trace": "<p>If list A is <code>3→6→9→15→30</code> and list B is <code>10→15→30</code>, after switching heads both pointers traverse equal total lengths and meet at the same node 15.</p>",
        "proof": "<p>Each pointer traverses lengthA+lengthB links. The extra prefix length on one list is compensated by the other list's prefix after switching. Therefore they reach the first common node at the same time; without an intersection both reach null together.</p>",
        "complexity": "<p>O(n+m) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test identical heads, intersection at the tail, different prefix lengths and no intersection. Compare node references, not equal data values; two separate nodes may contain the same value.</p>",
    },
    "l24-add-two-numbers": {
        "intuition": "<p>Digits are stored least-significant first, so addition proceeds from the head just like column addition. A carry is propagated to the next digit.</p>",
        "steps": "<ol><li>Use a dummy result node and a tail pointer.</li><li>While either input remains or carry is non-zero, add available digits and carry.</li><li>Create a node with sum modulo 10 and update carry to sum divided by 10.</li><li>Advance the input pointers and continue.</li></ol>",
        "trace": "<p><code>[2,4,3]</code> represents 342 and <code>[5,6,4]</code> represents 465. Add 2+5=7, 4+6=10 (write 0, carry 1), 3+4+1=8. Result: <code>[7,0,8]</code>.</p>",
        "proof": "<p>At each digit position, the algorithm computes the correct decimal digit and carry for the sum of the two input digits plus the incoming carry. Induction over positions establishes that the result prefix represents the sum modulo the corresponding power of ten.</p>",
        "complexity": "<p>O(max(n,m)) time and O(max(n,m)) output space. Only a constant number of working variables are used.</p>",
        "edge": "<p>Test unequal lengths, carry remaining after both lists end, adding zero, long runs of 9 and the single-node case. Each input digit must be in [0,9].</p>",
    },
    "l26-merge-sort-for-linked-list": {
        "intuition": "<p>Merge sort suits linked lists because splitting and merging require pointer changes rather than random access. Recursively split the list, sort both halves and merge them in order.</p>",
        "steps": "<ol><li>Find the midpoint with slow/fast pointers and split the list into two disjoint halves.</li><li>Recursively sort each half until it contains at most one node.</li><li>Merge the two sorted lists by repeatedly linking the smaller head node.</li><li>Return the merged head.</li></ol>",
        "trace": "<p>For <code>3→5→2→4→1</code>, split into [3,5,2] and [4,1], recursively sort to [2,3,5] and [1,4], then merge to <code>1→2→3→4→5</code>.</p>",
        "proof": "<p>Base lists of length zero or one are sorted. Assuming the recursive halves are sorted, the merge step repeatedly selects the smallest remaining head, producing a sorted list containing every node exactly once. By induction the whole list is sorted.</p>",
        "complexity": "<p>O(n log n) time. Recursive splitting/merge uses O(log n) call-stack space; an iterative bottom-up variant can achieve O(1) auxiliary space.</p>",
        "edge": "<p>Test empty, one node, duplicates, already sorted, reverse sorted and odd-length lists. The repository note specifies that the extra node in an odd split goes to the first half.</p>",
    },
    "l30-reverse-linked-list-in-groups": {
        "intuition": "<p>Reverse each consecutive block of up to k nodes, then connect the reversed block to the next one. The source statement explicitly says a final group smaller than k must also be reversed.</p>",
        "steps": "<ol><li>Identify the current group of at most k nodes.</li><li>Reverse the links within that group while retaining its original head as the new tail.</li><li>Connect the previous group's tail to the reversed group's head.</li><li>Continue with the next group and return the new head.</li></ol>",
        "trace": "<p>For <code>1→2→3→4→5</code> and k=3, reverse [1,2,3] to [3,2,1], then reverse the remaining [4,5] to [5,4]. Result: <code>3→2→1→5→4</code>.</p>",
        "proof": "<p>Each iteration reverses exactly the links within one disjoint segment and reconnects its endpoints. Every node remains in exactly one segment, and each segment's order is reversed; concatenating the segments yields the required list.</p>",
        "complexity": "<p>O(n) time because each node is processed once. Auxiliary space is O(1) for iterative reversal or O(n/k) recursive frames for recursive group processing.</p>",
        "edge": "<p>Test k=1, k larger than list length, exact multiples of k, a final partial group and empty input. Some common variants leave the final partial group unchanged; this repository's problem statement requires reversing it.</p>",
    },
    "bt13-height-of-binary-tree": {
        "intuition": "<p>The height of a node is one plus the greater height of its children. A null child contributes zero, so the recursion naturally computes height bottom-up.</p>",
        "steps": "<ol><li>If the node is null, return 0.</li><li>Recursively compute the left subtree height.</li><li>Recursively compute the right subtree height.</li><li>Return 1 plus the larger height.</li></ol>",
        "trace": "<p>For a root with two leaf children, each leaf returns 1 and the root returns 1+max(1,1)=2.</p>",
        "proof": "<p>By induction, null subtrees have height zero and each non-null subtree returns one plus the maximum child height. This is exactly the longest root-to-leaf path measured in nodes.</p>",
        "complexity": "<p>O(n) time because every node is visited once; O(h) recursion stack, where h is tree height (O(log n) balanced, O(n) skewed).</p>",
        "edge": "<p>Test an empty tree, one node, a left/right skewed tree and a complete tree. Clarify whether the problem defines height in edges or nodes; this source's examples count nodes.</p>",
    },
    "bt14-check-for-balanced-tree": {
        "intuition": "<p>A tree is height-balanced when every node's left and right subtree heights differ by at most one. A post-order traversal can compute heights and detect imbalance in the same pass.</p>",
        "steps": "<ol><li>Return height 0 for null.</li><li>Compute the left subtree result; propagate an unbalanced sentinel immediately.</li><li>Compute the right result and propagate failure if needed.</li><li>If the height difference exceeds one, return the sentinel; otherwise return one plus the greater height.</li></ol>",
        "trace": "<p>A node with left height 2 and right height 1 is locally balanced and returns height 3. A node with heights 3 and 1 is unbalanced, so failure propagates to the root.</p>",
        "proof": "<p>Post-order ensures both child results are known before checking the current node. If either child is unbalanced, the whole tree is unbalanced. Otherwise checking the current height difference completes the condition for this subtree.</p>",
        "complexity": "<p>O(n) time and O(h) recursion stack. Recomputing subtree heights independently at every node can degrade to O(n²) on a skewed tree.</p>",
        "edge": "<p>Empty and single-node trees are balanced. Test a perfect tree, a chain, and a tree where only a deep subtree violates the height condition.</p>",
    },
    "bt16-maximum-path-sum-from-any-node": {
        "intuition": "<p>A maximum path may start and end anywhere, but when returning a contribution to a parent it can extend through only one child. At each node, combine both positive child gains to update the global best.</p>",
        "steps": "<ol><li>For null, return zero.</li><li>Recursively obtain left and right gains, discarding negative gains with max(0,gain).</li><li>Update the global answer with node value + left gain + right gain.</li><li>Return node value + max(left gain,right gain) to the parent.</li></ol>",
        "trace": "<p>For root 10 with left child 2 and grandchildren 20 and 1, the best path is 20→2→10, with sum 32. The root's return value to its parent would include only one branch.</p>",
        "proof": "<p>Any simple path passing through a node can use at most two incident child directions. The global update considers the best path whose highest node is the current node. The recursive return must be a single downward chain because a parent can connect to only one child branch without creating a fork.</p>",
        "complexity": "<p>O(n) time and O(h) recursion stack.</p>",
        "edge": "<p>All-negative trees must return the largest single node, not zero. Initialize the global maximum to negative infinity. Test one node, skewed trees, zero/negative gains and large sums.</p>",
    },
    "bt18-zig-zag-tree-traversal": {
        "intuition": "<p>Zig-zag traversal is level-order BFS with alternating output direction. Process one complete level at a time and place each value at the appropriate index in that level's result.</p>",
        "steps": "<ol><li>Push the root into a queue.</li><li>For each level, capture the queue size so only current-level nodes are processed.</li><li>Write values left-to-right on one level and right-to-left on the next.</li><li>Enqueue left and right children in normal BFS order.</li></ol>",
        "trace": "<p>For a complete tree with root 1, children 2 and 3, and leaves 4,5,6,7, levels emit [1], then [3,2], then [4,5,6,7].</p>",
        "proof": "<p>The queue preserves breadth-first level order. Capturing its size isolates each level; choosing the output index based on the level direction reverses only that level without changing which nodes are visited.</p>",
        "complexity": "<p>O(n) time and O(w) queue/output working space, where w is maximum tree width; total returned output is O(n).</p>",
        "edge": "<p>Test empty tree, one node, a skewed tree, incomplete final levels and levels with a single child. Do not reverse the queue itself; only the order of values in the current result level changes.</p>",
    },
    "bt28-lowest-common-ancestor": {
        "intuition": "<p>The lowest common ancestor is the deepest node whose subtree contains both targets. A post-order recursion returns a target when found and combines non-null results from the two sides.</p>",
        "steps": "<ol><li>If the current node is null or equals either target, return it.</li><li>Search the left subtree.</li><li>Search the right subtree.</li><li>If both results are non-null, the current node is the LCA; otherwise return whichever side found a target.</li></ol>",
        "trace": "<p>In a tree with root 1 and children 2 and 3, searching for 2 and 3 returns one target from each subtree, so root 1 is their LCA.</p>",
        "proof": "<p>If targets occur in separate child subtrees, the current node is their first shared ancestor. If both are in one subtree, that subtree's recursive result contains the deeper LCA. If the current node is itself a target, it is an ancestor of the other target or the target itself.</p>",
        "complexity": "<p>O(n) time and O(h) recursion stack.</p>",
        "edge": "<p>Test one target equal to the root, one target an ancestor of the other, targets in opposite subtrees and absent targets. The source assumes unique values and either both targets exist or neither exists; node-reference variants avoid ambiguity from duplicate values.</p>",
    },
    "bt42-serialize-and-deserialize-binary-tree": {
        "intuition": "<p>Serialization must preserve both node values and the shape of the tree. A traversal that records explicit null markers distinguishes missing children from different tree structures.</p>",
        "steps": "<ol><li>Traverse the tree in a defined order (commonly level-order).</li><li>Encode each node value and an explicit marker for each null child.</li><li>For deserialization, read tokens in the same order and reconstruct child links using a queue or recursive cursor.</li><li>Ensure the decoder consumes exactly the serialized representation.</li></ol>",
        "trace": "<p>A root 1 with children 2 and 3 needs a representation that records root, left child and right child. If a child is missing, a null marker must be present so the decoder does not attach a later node to the wrong parent.</p>",
        "proof": "<p>Each non-null token creates one node and each null token specifies an absent child. Because the traversal order and null positions are deterministic, decoding consumes the same structural decisions made during encoding and reconstructs an equivalent tree.</p>",
        "complexity": "<p>O(n) time and O(n) serialized/output storage; the queue or recursion stack is O(w) for level-order or O(h) for recursive traversal.</p>",
        "edge": "<p>Test empty tree, single node, left-only/right-only chains, repeated values and asymmetric shapes. Values alone are insufficient; null markers or an equivalent unambiguous structure are required.</p>",
    },

    "a15-majority-element": {
        "intuition": "<p>The majority value occurs more than half the time. Boyer–Moore voting cancels pairs of different values; a true majority cannot be fully cancelled.</p>",
        "steps": "<ol><li>Maintain a candidate and a balance.</li><li>When balance is zero, choose the current value.</li><li>Increment for a match and decrement for a mismatch.</li><li>If existence is not guaranteed, count the candidate in a second pass and verify frequency &gt; n/2.</li></ol>",
        "trace": "<p>For <code>[2,2,1,1,1,2,2]</code>, pairwise cancellation leaves candidate 2; its frequency is 4, greater than 7/2.</p>",
        "proof": "<p>Removing pairs of unequal values removes at most one majority occurrence per pair. Since the majority has more than n/2 occurrences, it cannot be completely eliminated. Verification is required if the input may have no majority.</p>",
        "complexity": "<p>Boyer–Moore takes O(n) time and O(1) auxiliary space. A hash-map variant takes O(n) expected time and O(n) space.</p>",
        "edge": "<p>Test no majority, exactly n/2 occurrences, n=1, negative values and repeated values at both ends. The threshold is strictly greater than n/2.</p>",
    },
    "frequencies-of-limited-range-array-elements": {
        "intuition": "<p>For each value v in 1..N, the output position v-1 must contain its frequency. Values greater than N are irrelevant. A frequency array is easiest to reason about; in-place encoding can reduce extra space.</p>",
        "steps": "<ol><li>Count only values between 1 and N.</li><li>For each value v, increment its frequency.</li><li>Overwrite arr[i] with the count of i+1.</li><li>Use a separate count array for clarity, or carefully encode counts in the input only after preserving original values.</li></ol>",
        "trace": "<p>For N=5 and input <code>[2,3,2,3,5]</code>, frequencies of 1 through 5 are <code>[0,2,2,0,1]</code>. The modified array stores this sequence.</p>",
        "proof": "<p>The count table records one increment for every valid occurrence of a value. Writing count[v] to output index v-1 therefore places exactly the required frequency in each position.</p>",
        "complexity": "<p>The auxiliary counting approach is O(n) time and O(n) extra space. An in-place encoding variant can achieve O(n) time and O(1) extra space under the source problem's bounded-value assumptions.</p>",
        "edge": "<p>Test absent values, repeated values, values greater than N, minimum value 1, maximum value N and all entries out of the counted range. The problem uses 1-based value labels but zero-based Java indices.</p>",
    },
    "leaders-in-array": {
        "intuition": "<p>A leader is at least as large as every value to its right. Scan from right to left while maintaining the maximum suffix value.</p>",
        "steps": "<ol><li>Start with the rightmost element as the suffix maximum and a leader.</li><li>Move left and record each value greater than or equal to the suffix maximum.</li><li>Update the suffix maximum after each comparison.</li><li>Reverse the collected list if the expected output is left-to-right.</li></ol>",
        "trace": "<p>For <code>[16,17,4,3,5,2]</code>, the reverse scan records 2, 5 and 17. Reversing gives <code>[17,5,2]</code>.</p>",
        "proof": "<p>The suffix maximum is exactly the largest value strictly to the current index's right. A current value is a leader iff it is at least that maximum, so the test is both necessary and sufficient.</p>",
        "complexity": "<p>O(n) time and O(n) result storage in a list-based implementation.</p>",
        "edge": "<p>The rightmost value is always a leader; equal values qualify. Test increasing, decreasing, all-equal and single-element arrays.</p>",
    },
    "majority-element": {
        "intuition": "<p>The task asks for a value occurring strictly more than n/2 times, but unlike the LeetCode variant, the source examples allow no majority and require -1. Use Boyer–Moore to propose a candidate, then verify it.</p>",
        "steps": "<ol><li>Run Boyer–Moore voting to obtain a candidate.</li><li>Count occurrences of that candidate in a second pass.</li><li>Return the candidate only when its count is greater than n/2; otherwise return -1.</li></ol>",
        "trace": "<p>For <code>[3,1,3,3,2]</code>, candidate 3 occurs three times, exceeding 5/2, so return 3. For <code>[1,2,3]</code>, no candidate passes verification, so return -1.</p>",
        "proof": "<p>Cancellation guarantees that if a majority exists, Boyer–Moore returns it. The second pass checks the strict frequency condition, so the algorithm also handles arrays without a majority.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space for voting plus verification; sorting or hash-map variants use more time or space.</p>",
        "edge": "<p>Test no majority, exactly half, all equal, one element and negative values. Do not return the candidate without verifying because the source contract does not guarantee existence.</p>",
    },
    "maximum-sub-array-sum": {
        "intuition": "<p>For a non-empty maximum-sum subarray, the best subarray ending at the current index either starts here or extends the best subarray ending at the previous index. This is Kadane's recurrence.</p>",
        "steps": "<ol><li>Initialize the best-ending-here and global best from the first value.</li><li>For each next value x, set ending-here to <code>max(x, endingHere+x)</code>.</li><li>Update the global best.</li><li>Return the global best.</li></ol>",
        "trace": "<p>For <code>[-2,1,-3,4,-1,2,1,-5,4]</code>, the best segment is <code>[4,-1,2,1]</code>, with sum 6.</p>",
        "proof": "<p>Any subarray ending at i either consists only of a[i] or extends a subarray ending at i-1. The recurrence chooses the better of these exhaustive possibilities. The maximum across all endpoints is the global optimum.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space. The source uses long for the returned sum, but intermediate variables must also be wide enough for the input constraints.</p>",
        "edge": "<p>Because the subarray must contain at least one element, all-negative input returns its largest element, not zero. Test one value, zeros, overflow-sized sums and best segments at either boundary.</p>",
    },
    "missing-number-in-array": {
        "intuition": "<p>The input contains N-1 distinct values from 1 through N. XOR the complete expected range with all input values; matching values cancel and the missing value remains.</p>",
        "steps": "<ol><li>Initialize xor to zero.</li><li>XOR every integer from 1 through N.</li><li>XOR every array element.</li><li>Return the remaining XOR value.</li></ol>",
        "trace": "<p>For N=5 and array <code>[1,2,4,5]</code>, XORing 1..5 and the array leaves 3.</p>",
        "proof": "<p>XOR is associative and commutative, and each present number appears twice across the expected range and input. Those pairs cancel; the missing number appears once.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test missing 1, missing N, N=1 and shuffled input. The argument depends on distinct values and the exact range 1..N.</p>",
    },
    "small-sum": {
        "intuition": "<p>This source defines a circular-array calculation, not the commonly named merge-sort “small sum” problem. For each index i, add arr[i] unchanged when it is smaller than its next circular neighbour; otherwise add arr[i] modulo K.</p>",
        "steps": "<ol><li>Iterate through indices 0 to n-1.</li><li>Let next be arr[(i+1) % n] to include the circular last-to-first comparison.</li><li>If arr[i] is less than next, add arr[i]; otherwise add arr[i] % K.</li><li>Reduce the running total modulo 1,000,000,007 as required by the source.</li></ol>",
        "trace": "<p>For a circular sequence, the final element must be compared with the first, not omitted. At each position the branch depends only on that adjacent circular pair; the accumulated value is reduced modulo the fixed modulus.</p>",
        "proof": "<p>The algorithm directly implements the problem's per-index rule: every element is considered once, its contribution is selected from the comparison with its circular successor, and modular reduction preserves the final residue.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test n=1 (the element is its own circular neighbour), K=0 (invalid for modulo and must be excluded), negative values if allowed, equal neighbours and the last-to-first comparison. Confirm whether values are guaranteed non-negative.</p>",
    },
    "sort-array-of0s1s-and2s": {
        "intuition": "<p>Only three values are possible. Count them in one pass and rewrite the array, or use the Dutch National Flag algorithm to partition in one pass and constant space.</p>",
        "steps": "<ol><li><b>Counting:</b> count 0s, 1s and 2s, then overwrite the array with those counts.</li><li><b>Three pointers:</b> maintain a processed 0 region, a processed 1 region, an unknown region and a processed 2 region.</li><li>Swap 0s left, leave 1s in place, and swap 2s right; re-examine a value swapped in from the right.</li></ol>",
        "trace": "<p>For <code>[2,0,2,1,1,0]</code>, the three-pointer method produces <code>[0,0,1,1,2,2]</code>. When a 2 is swapped with the high boundary, mid does not advance because the incoming value is still unknown.</p>",
        "proof": "<p>The counting method writes exactly the observed number of each value. In the Dutch National Flag method, each iteration expands one classified region and shrinks the unknown interval; termination leaves no unclassified elements.</p>",
        "complexity": "<p>Counting uses O(n) time and O(1) extra space (three counters). Dutch National Flag also uses O(n) time and O(1) extra space.</p>",
        "edge": "<p>Test all one value, sorted, reverse-sorted, duplicates, one element and empty input. The contract restricts every value to 0, 1 or 2.</p>",
    },
    "g5-bredth-first-search": {
        "intuition": "<p>BFS explores vertices in increasing distance (number of edges) from the start. A queue ensures nodes discovered earlier are processed first; a visited marker prevents repeated work.</p>",
        "steps": "<ol><li>Mark source 0 visited and enqueue it.</li><li>While the queue is non-empty, dequeue a vertex and append it to the traversal.</li><li>Visit its adjacency-list neighbours in the required order; mark each before enqueueing it.</li><li>Stop when the reachable component has been exhausted.</li></ol>",
        "trace": "<p>With adjacency list 0→[1,2,3] and 2→[4], the queue visits 0, then 1,2,3, and finally 4. Traversal: <code>0,1,2,3,4</code>.</p>",
        "proof": "<p>Every reachable vertex is enqueued when first discovered, and visited is set before enqueueing so it enters once. FIFO order processes all vertices at distance d before distance d+1, which is the defining BFS order.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space for adjacency-list representation.</p>",
        "edge": "<p>Test isolated source, disconnected vertices, self-loops, cycles and multiple paths to one vertex. The stated problem returns only vertices reachable from source 0; neighbour iteration order affects the exact traversal sequence.</p>",
    },
    "g6-depth-first-search": {
        "intuition": "<p>DFS explores one path as deeply as possible before backtracking. Recursion (or an explicit stack) stores the active traversal path, while visited prevents cycles.</p>",
        "steps": "<ol><li>Start at vertex 0 and mark it visited.</li><li>Append the vertex to the traversal.</li><li>Visit each unvisited neighbour recursively in adjacency-list order.</li><li>Backtrack when no unvisited neighbour remains.</li></ol>",
        "trace": "<p>For 0 adjacent to [2,3,1], with 2 adjacent to 4, DFS visits 0→2→4, backtracks, then visits 3 and 1. Output: <code>0,2,4,3,1</code>.</p>",
        "proof": "<p>Each vertex is marked before exploring its neighbours, so it is processed once. Recursive calls completely explore a neighbour's reachable unvisited region before returning, matching depth-first traversal.</p>",
        "complexity": "<p>O(V+E) time and O(V) space for visited plus recursion/stack.</p>",
        "edge": "<p>Test a chain (deep recursion), cycles, self-loops, multiple components and adjacency ordering. The source statement assumes a connected graph; for a disconnected graph, a full-graph traversal needs an outer loop over unvisited vertices.</p>",
    },
    "g10-rotting-oranges": {
        "intuition": "<p>All initially rotten oranges spread simultaneously. Multi-source BFS starts from every rotten cell at time zero; BFS layers correspond to elapsed minutes.</p>",
        "steps": "<ol><li>Count fresh oranges and enqueue every initially rotten cell.</li><li>Process the queue level by level.</li><li>For each rotten cell, turn each adjacent fresh cell rotten, decrement fresh count and enqueue it.</li><li>Increment elapsed minutes after each non-empty BFS layer.</li><li>Return elapsed time if no fresh oranges remain, otherwise -1.</li></ol>",
        "trace": "<p>For <code>[[2,1,1],[1,1,0],[0,1,1]]</code>, the initial rotten cell infects its neighbours in minute 1, and the infection advances one grid layer per minute until all reachable fresh cells rot at minute 4.</p>",
        "proof": "<p>Every fresh cell is first reached at its minimum grid distance from the set of initially rotten cells because BFS processes increasing distance layers. That distance is exactly the earliest minute it can become rotten. If fresh cells remain after BFS, they are unreachable.</p>",
        "complexity": "<p>O(mn) time and O(mn) queue/visited space; each cell is enqueued at most once.</p>",
        "edge": "<p>Test no fresh oranges (answer 0), no initial rotten orange but fresh remain (answer -1), isolated fresh cells, one cell and rectangular grids. Use four-directional adjacency only.</p>",
    },
    "g11-detect-cycle-in-undirected-graph-bfs": {
        "intuition": "<p>In an undirected graph, seeing an already visited neighbour indicates a cycle unless that neighbour is the current vertex's parent. BFS therefore stores both vertex and parent.</p>",
        "steps": "<ol><li>Start BFS from each unvisited vertex to cover disconnected components.</li><li>Queue (node,parent), mark the node visited.</li><li>For each neighbour, enqueue it if unvisited.</li><li>If it is already visited and is not the current node's parent, a cycle exists.</li></ol>",
        "trace": "<p>For edges 1-2, 2-3, 3-4 and 4-1, BFS eventually reaches a visited neighbour through an edge other than the parent edge, proving a cycle.</p>",
        "proof": "<p>A BFS tree contains exactly the discovery edges. Any additional undirected edge joining already discovered vertices other than a parent-child reverse edge closes a cycle. Conversely, a cycle necessarily contains such a non-tree edge.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space.</p>",
        "edge": "<p>Test a tree, disconnected graph with a cycle in one component, self-loops and parallel edges. Parent-by-vertex logic assumes the graph representation's multiedge semantics; edge IDs are safer when parallel edges are allowed.</p>",
    },
    "g19-detect-cycle-in-directed-graph-dfs": {
        "intuition": "<p>A directed cycle exists when DFS reaches a vertex that is already on the current recursion path. A vertex visited in a previous, completed path does not by itself imply a cycle.</p>",
        "steps": "<ol><li>Maintain visited and recursion-stack (or three-colour) state.</li><li>On entering a vertex, mark it visited and active.</li><li>For each outgoing edge, recurse if the neighbour is unvisited.</li><li>If an edge points to an active neighbour, report a cycle.</li><li>Mark the vertex inactive when its DFS call completes.</li></ol>",
        "trace": "<p>For directed edges 0→1, 1→2 and 2→0, DFS from 0 reaches 0 again while it is still active, so a cycle is detected.</p>",
        "proof": "<p>An edge to an active ancestor closes a directed path into a cycle. If no edge ever reaches an active vertex, every DFS path terminates without a back edge, so the graph is acyclic.</p>",
        "complexity": "<p>O(V+E) time and O(V) space for visited/active state and recursion stack.</p>",
        "edge": "<p>Test a DAG with cross edges, a self-loop, disconnected components and a cycle outside the first component. Do not confuse globally visited with currently active.</p>",
    },
    "g22-kahn-algorithm-topo-sort-bfs": {
        "intuition": "<p>Kahn's algorithm repeatedly removes vertices with in-degree zero. Such a vertex has no remaining prerequisite, so it can safely appear next in a topological order.</p>",
        "steps": "<ol><li>Compute in-degree for every vertex.</li><li>Enqueue all vertices with in-degree zero.</li><li>Dequeue a vertex, append it to the ordering and decrement the in-degree of each outgoing neighbour.</li><li>Enqueue a neighbour when its in-degree becomes zero.</li><li>If fewer than V vertices are output, the graph contains a cycle.</li></ol>",
        "trace": "<p>For edges 0→2, 1→2, 2→3, the initial queue contains 0 and 1. Removing both makes 2 ready; removing 2 makes 3 ready. One valid order is <code>0,1,2,3</code>.</p>",
        "proof": "<p>A zero-in-degree vertex has no incoming edge from any remaining vertex, so placing it next cannot violate a dependency. Removing it preserves the same property for the residual graph. If vertices remain but none has zero in-degree, every remaining vertex depends (directly or indirectly) on another, which implies a directed cycle.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space.</p>",
        "edge": "<p>Test multiple valid orders, disconnected DAGs, isolated vertices, self-loops and cycles. A topological order exists only for a directed acyclic graph.</p>",
    },
    "g31-dijkstras-shortest-path-pq": {
        "intuition": "<p>Dijkstra's algorithm finalizes the shortest known distance by repeatedly extracting the unsettled vertex with the smallest tentative distance from a min-priority queue. Its correctness relies on non-negative edge weights.</p>",
        "steps": "<ol><li>Initialize all distances to infinity and source distance to zero.</li><li>Insert (0,source) into a min-priority queue.</li><li>Extract the smallest-distance pair; skip stale entries if its distance no longer matches the best known value.</li><li>Relax every outgoing edge: if dist[u]+weight improves dist[v], update and enqueue the new pair.</li><li>Return the distance array.</li></ol>",
        "trace": "<p>For source 0 with edge 0-1 weight 5 and 0-2 weight 8, the initial distances become 5 and 8. If a later route reaches 2 through 1 with total cost 7, relaxation improves dist[2] from 8 to 7.</p>",
        "proof": "<p>When the minimum tentative-distance vertex is extracted, any alternative path to it through an unsettled vertex would have to be at least as costly because all remaining edge weights are non-negative. Therefore its distance is final. Relaxation then maintains best known paths to neighbours.</p>",
        "complexity": "<p>O((V+E) log V) with a binary heap and adjacency lists (often expressed O(E log V)); O(V+E) storage including graph and queue.</p>",
        "edge": "<p>Dijkstra is not valid with negative edge weights. Use long distances if path sums may overflow int. Test disconnected vertices, zero-weight edges, stale priority-queue entries and source equal to destination.</p>",
    },
    "g24-course-schedule-1-bfs": {
        "intuition": "<p>Course prerequisites form a directed graph. All courses can be completed exactly when this graph is acyclic, so Kahn's topological-sort algorithm can determine whether every course is removable.</p>",
        "steps": "<ol><li>Create an edge from prerequisite to dependent course.</li><li>Compute in-degrees and enqueue all courses with zero prerequisites.</li><li>Process each course and reduce the in-degree of its dependants.</li><li>Count processed courses.</li><li>Return true if and only if the count equals numCourses.</li></ol>",
        "trace": "<p>For prerequisite pair [1,0], the edge is 0→1. Course 0 has in-degree zero, so take it first; course 1 then becomes available. Both are processed and the answer is true.</p>",
        "proof": "<p>If all vertices are processed, the produced order satisfies every prerequisite edge, so a valid course order exists. If processing stops early, remaining vertices have positive in-degree and form or depend on a cycle, making completion impossible.</p>",
        "complexity": "<p>O(V+E) time and O(V+E) space.</p>",
        "edge": "<p>Test no prerequisites, a self-prerequisite, a multi-course cycle, duplicate prerequisite pairs and disconnected dependency chains. Carefully preserve the direction prerequisite→course.</p>",
    },
    "g27-shortest-path-in-undirected-graph-unit-length": {
        "intuition": "<p>When every edge has equal weight one, BFS discovers vertices in non-decreasing number of edges from the source. The first distance assigned to a vertex is therefore its shortest path length.</p>",
        "steps": "<ol><li>Initialize distances to -1 and source distance to zero.</li><li>Enqueue the source.</li><li>For each dequeued vertex, visit unvisited neighbours, set their distance to current distance + 1 and enqueue them.</li><li>Leave unreachable vertices at -1.</li></ol>",
        "trace": "<p>For edges 0-1 and 0-3, the first layer has distance 1. From 1, vertex 2 is reached at distance 2; from 3, vertex 4 is reached at distance 2.</p>",
        "proof": "<p>BFS processes all vertices at distance d before any at d+1. A vertex is first discovered along a shortest path because any shorter path would have been processed in an earlier layer.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space.</p>",
        "edge": "<p>Test source itself (distance 0), disconnected vertices (-1), multiple shortest paths and a graph with a single vertex. BFS is valid because all edges have equal unit weight.</p>",
    },

    "max-ones-in-row-of-matrix": {
        "intuition": "<p>Each row is sorted with all zeros before ones. The row with the most ones has the smallest first-one index; its count is columns minus that index.</p>",
        "steps": "<ol><li>For each row, binary-search the first 1.</li><li>Compute ones as m-firstOneIndex, or zero if no 1 exists.</li><li>Track the row with the largest count.</li><li>Return its index, following the source's convention for ties or no ones.</li></ol>",
        "trace": "<p>For rows [0,0,1,1], [0,1,1,1] and [0,0,0,0], the counts are 2, 3 and 0. The second row has the maximum number of ones.</p>",
        "proof": "<p>In a sorted binary row, every position from the first 1 to the end is 1, and every earlier position is 0. Thus one lower-bound search determines the exact count for that row; comparing all rows finds the maximum.</p>",
        "complexity": "<p>O(r log c) time and O(1) auxiliary space for r rows and c columns.</p>",
        "edge": "<p>Test all-zero rows, all-one rows, ties, one column, one row and an empty matrix. The binary-search method requires each row to be sorted.</p>",
    },
    "painters-partition-problem": {
        "intuition": "<p>Minimize the maximum time/load assigned to any painter while preserving contiguous board order. Binary-search the maximum allowed load because feasibility is monotonic.</p>",
        "steps": "<ol><li>Set the lower bound to the largest board and upper bound to the sum of all board lengths.</li><li>For a candidate limit, greedily assign consecutive boards to a painter until the next board exceeds the limit.</li><li>Count painters required.</li><li>If the count is within the available painters, search for a smaller limit; otherwise search larger.</li></ol>",
        "trace": "<p>For board lengths <code>[10,20,30,40]</code> and two painters, a limit of 60 permits [10,20,30] and [40], while 50 requires three painters. The minimum feasible maximum is 60.</p>",
        "proof": "<p>For a fixed limit, assigning the longest possible contiguous prefix to each painter minimizes the number of painters required. If this count exceeds the available painters, no partition under that limit exists. Feasibility is monotonic as the limit increases.</p>",
        "complexity": "<p>O(n log(sumBoards)) time and O(1) auxiliary space. Multiply by painter speed only if the specific problem contract includes it; do not mix variants.</p>",
        "edge": "<p>Test painters greater than boards, one painter, one board, zero-length boards and large sums. Some versions require modulo arithmetic or return -1 for impossible allocations; follow the exact source signature and contract.</p>",
    },
    "peak-element-ii": {
        "intuition": "<p>In a matrix where adjacent cells differ and a peak is greater than its four neighbours, binary-search columns. Find the maximum element in the middle column; if a horizontal neighbour is larger, a peak exists in that direction.</p>",
        "steps": "<ol><li>Choose the middle column.</li><li>Find the row containing the maximum value in that column.</li><li>Compare that cell with its left and right neighbours, treating out-of-bounds as negative infinity.</li><li>If neither horizontal neighbour is larger, the selected cell is a peak.</li><li>Otherwise move toward the larger neighbour's half of the columns.</li></ol>",
        "trace": "<p>For a middle-column maximum at row r, if the right neighbour is larger, move the search to columns right of mid. Repeating this process narrows the column interval until a cell dominates all four neighbours.</p>",
        "proof": "<p>The selected cell is maximum in its column, so its vertical neighbours are smaller. If a horizontal neighbour is larger, following that direction cannot decrease immediately; the process must eventually reach a column maximum with no larger horizontal neighbour, which is a peak.</p>",
        "complexity": "<p>O(r log c) time and O(1) auxiliary space for r rows and c columns.</p>",
        "edge": "<p>Test one row, one column, a peak on a boundary, rectangular matrices and negative values. Confirm the exact definition of adjacency and the problem's guarantee that a peak exists.</p>",
    },
    "search-a2-d-matrix": {
        "intuition": "<p>When the matrix is globally row-major sorted (each row starts after the previous row ends), it behaves like a sorted one-dimensional array of length m*n.</p>",
        "steps": "<ol><li>Binary-search virtual indices from 0 to m*n-1.</li><li>Convert mid to row <code>mid / n</code> and column <code>mid % n</code>.</li><li>Compare the matrix value with target and discard the appropriate half.</li><li>Return true on equality, otherwise false after the interval closes.</li></ol>",
        "trace": "<p>For <code>[[1,3,5],[7,9,11]]</code>, virtual index 4 maps to row 1, column 1 and value 9. Searching target 9 returns true.</p>",
        "proof": "<p>The row-major mapping preserves order under the problem's global sortedness condition. Ordinary binary search therefore applies to the virtual sequence without materializing it.</p>",
        "complexity": "<p>O(log(mn)) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty dimensions if allowed, one row, one column, first/last value, target in the gap between rows and absent target. Compute m*n safely to avoid integer overflow.</p>",
    },
    "search-a2-d-matrix-ii": {
        "intuition": "<p>Rows and columns are independently sorted, but the matrix is not necessarily globally row-major sorted. Start at the top-right corner: moving left decreases values, moving down increases them.</p>",
        "steps": "<ol><li>Start at row 0, column m-1.</li><li>If the current value equals target, return true.</li><li>If it is greater than target, move left.</li><li>If it is smaller than target, move down.</li><li>Stop when the position leaves the matrix.</li></ol>",
        "trace": "<p>For <code>[[1,4,7],[2,5,8],[3,6,9]]</code> and target 6, start at 7, move left to 4, down to 5, then down to 6 and return true.</p>",
        "proof": "<p>At the top-right corner, every value below is at least the current value and every value to the left is at most it. If current is too large, its entire column segment below cannot be smaller, so discard the column; if too small, its entire row segment to the left cannot be larger, so discard the row. Each step removes only impossible cells.</p>",
        "complexity": "<p>O(r+c) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test one row, one column, target smaller/larger than all values, duplicates and empty matrix. Do not apply the flattened binary search unless the stronger global row-major ordering is guaranteed.</p>",
    },
    "single-element-in-sorted-array": {
        "intuition": "<p>In a sorted array where every value appears exactly twice except one, pairs occupy even-odd index positions before the singleton and odd-even positions after it. Binary-search this index-parity pattern.</p>",
        "steps": "<ol><li>Search an even-aligned midpoint.</li><li>If nums[mid] equals nums[mid+1], the singleton lies after this pair; move low to mid+2.</li><li>Otherwise the singleton is at mid or to its left; move high to mid.</li><li>Return the converged index.</li></ol>",
        "trace": "<p>For <code>[1,1,2,3,3,4,4,8,8]</code>, pairs align at indices (0,1), (3,4), etc. The parity mismatch identifies 2 at index 2.</p>",
        "proof": "<p>Before the singleton, each pair begins at an even index; after it, each pair begins at an odd index. The comparison at an even midpoint determines which side still follows the pre-singleton pattern, so binary search preserves the singleton-containing half.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test singleton at index 0 or n-1, array length one, negative values and the maximum permitted size. The input length must be odd and all non-singleton values must occur exactly twice.</p>",
    },
    "smallest-divisor-given-threshold": {
        "intuition": "<p>For divisor d, compute the sum of rounded-up quotients <code>ceil(nums[i]/d)</code>. This sum decreases or stays constant as d increases, so binary-search the smallest divisor meeting the threshold.</p>",
        "steps": "<ol><li>Search divisors from 1 to max(nums).</li><li>For a candidate d, sum <code>(value+d-1)/d</code> using a wide accumulator.</li><li>If the sum is at most threshold, try a smaller divisor.</li><li>Otherwise increase the divisor.</li></ol>",
        "trace": "<p>For <code>[1,2,5,9]</code> and threshold 6, divisor 5 gives 1+1+1+2=5, which is feasible; smaller divisors are tested to find the minimum feasible value.</p>",
        "proof": "<p>Each rounded quotient is non-increasing as divisor grows, so the total is non-increasing. The feasible divisors form a suffix of the search interval, and binary search finds its first element.</p>",
        "complexity": "<p>O(n log M) time where M is the maximum array value, and O(1) auxiliary space.</p>",
        "edge": "<p>Test threshold equal to n, threshold below n (impossible under positive inputs), one value, all equal values and large sums. Use overflow-safe ceiling division and long for the accumulated sum.</p>",
    },
    "sorted-array-rotation": {
        "intuition": "<p>The number of rotations of a strictly increasing array equals the index of its minimum (under the common right-rotation convention). Binary search locates that minimum.</p>",
        "steps": "<ol><li>Compare the midpoint with the rightmost value.</li><li>If nums[mid] is greater, the minimum lies to the right.</li><li>Otherwise the minimum is at mid or to the left.</li><li>When the interval converges, return the minimum index as the rotation count.</li></ol>",
        "trace": "<p>For <code>[4,5,6,7,0,1,2]</code>, binary search converges to index 4, indicating four right rotations of the original sorted sequence.</p>",
        "proof": "<p>The minimum is the pivot separating the two sorted runs. Comparing mid with the right boundary determines which side contains that pivot, so each iteration safely halves the interval.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space for distinct values.</p>",
        "edge": "<p>Test an unrotated array, rotation by one, minimum at either end, one element and duplicates if allowed. The count convention depends on whether rotations are defined left or right; state it explicitly.</p>",
    },
    "split-array-largest-sum": {
        "intuition": "<p>Split the array into at most k non-empty contiguous parts while minimizing the largest part sum. Binary-search that largest sum; feasibility is monotonic as the allowed sum increases.</p>",
        "steps": "<ol><li>Set low to the largest element and high to the total sum.</li><li>For a candidate maximum, greedily form contiguous parts, starting a new part when the next value would exceed the limit.</li><li>If the required part count is at most k, try a smaller limit.</li><li>Otherwise increase the limit.</li></ol>",
        "trace": "<p>For <code>[7,2,5,10,8]</code> and k=2, a limit of 18 permits [7,2,5] and [10,8]. A smaller limit cannot split the array into two contiguous parts, so 18 is optimal.</p>",
        "proof": "<p>For a fixed limit, greedy longest-prefix partitioning minimizes the number of parts. If it requires more than k, no partition under that limit is possible. Feasibility is monotonic in the limit.</p>",
        "complexity": "<p>O(n log(sum)) time and O(1) auxiliary space. The problem's non-negative values are important for monotonicity and greedy feasibility.</p>",
        "edge": "<p>Test k=1, k=n, all zeros, one large element and values near integer limits. Use long for total and running sums. Distinguish “exactly k” from “at most k”; with non-negative values, extra splits can be introduced when needed.</p>",
    },
    "square-root-of-number": {
        "intuition": "<p>The integer square root is the greatest integer x such that x² is no greater than n. This predicate is monotonic, so binary search finds the boundary.</p>",
        "steps": "<ol><li>Search candidates from 0 through n (or a tighter upper bound).</li><li>Compute the square using long arithmetic or compare <code>mid &lt;= n/mid</code> to avoid overflow.</li><li>If mid² is at most n, save mid and search higher.</li><li>Otherwise search lower.</li></ol>",
        "trace": "<p>For n=27, 5²=25 is valid while 6²=36 is too large, so the integer square root is 5.</p>",
        "proof": "<p>The predicate x²≤n is true for all integers up to floor(sqrt(n)) and false afterward. Binary search finds the last true candidate.</p>",
        "complexity": "<p>O(log n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test n=0, n=1, perfect squares, values between squares and maximum int. Avoid multiplying two ints if the product can overflow.</p>",
    },
    "climbing-stairs": {
        "intuition": "<p>To reach step n, the final move must come from n-1 or n-2. Therefore the number of ways is the sum of the ways to reach those two previous steps.</p>",
        "steps": "<ol><li>Define dp[i] as the number of ways to reach step i.</li><li>Set dp[0]=1 and dp[1]=1 (with base cases adapted to the source indexing).</li><li>For each i≥2, compute dp[i]=dp[i-1]+dp[i-2].</li><li>Return dp[n]. A rolling pair of variables reduces space.</li></ol>",
        "trace": "<p>For n=4, ways are 1, 1, 2, 3, 5 for steps 0 through 4. The answer is 5.</p>",
        "proof": "<p>Every valid sequence ending at step n has a unique final move of either one or two steps. Removing that final move gives a unique sequence ending at n-1 or n-2, and these cases do not overlap.</p>",
        "complexity": "<p>O(n) time. A tabulation array uses O(n) space; rolling two previous values uses O(1) auxiliary space.</p>",
        "edge": "<p>Check n=0, n=1 and n=2, and integer overflow for large n. The exact base-case convention for n=0 should match the method contract.</p>",
    },
    "dp20-coin-change": {
        "intuition": "<p>This asks for the minimum number of unlimited-use coins that form an amount. For each amount, consider using one coin c last; the remaining subproblem is amount-c.</p>",
        "steps": "<ol><li>Define dp[a] as the minimum coins needed for amount a.</li><li>Initialize dp[0]=0 and all other states to an unreachable sentinel.</li><li>For each amount, try every coin not exceeding it.</li><li>Relax with dp[a]=min(dp[a],1+dp[a-c]) when the smaller state is reachable.</li><li>Return -1 if the target state remains unreachable.</li></ol>",
        "trace": "<p>For coins [1,2,5] and amount 11, a minimum solution is 5+5+1, so dp[11]=3.</p>",
        "proof": "<p>Any optimal non-empty solution uses some final coin c. The preceding coins must form an optimal solution for amount-c; otherwise replacing them with a better subsolution would improve the original solution. Considering every possible final coin therefore finds the optimum.</p>",
        "complexity": "<p>O(amount × numberOfCoins) time and O(amount) space for bottom-up DP.</p>",
        "edge": "<p>Amount zero requires zero coins. Test impossible amounts, duplicate denominations, coin larger than amount and large amount overflow. Guard the unreachable sentinel before adding one.</p>",
    },
    "dp21-target-sum": {
        "intuition": "<p>Assigning plus/minus signs partitions numbers into a positive subset P and a negative subset N. With total S, equations P-N=target and P+N=S imply P=(S+target)/2, converting the problem into subset-count DP.</p>",
        "steps": "<ol><li>Compute total sum S; if |target| exceeds S or S+target is odd, return 0.</li><li>Set required subset sum to (S+target)/2.</li><li>Count subsets reaching that sum using 1D DP.</li><li>For each value, iterate sums downward so each array element is used once.</li></ol>",
        "trace": "<p>For five 1s and target 3, the required positive subset sum is (5+3)/2=4. Choosing which four positions receive + yields five sign assignments.</p>",
        "proof": "<p>The sign assignment and the choice of positive subset are in one-to-one correspondence. The algebraic transformation preserves the target condition, and subset-count DP counts every valid subset exactly once.</p>",
        "complexity": "<p>O(n × subsetSum) time and O(subsetSum) space for 1D DP.</p>",
        "edge": "<p>Test negative target, target outside [-S,S], odd parity of S+target, zero-valued elements and empty input. Zeros double the number of assignments for every existing state; count type may overflow int for large inputs.</p>",
    },
    "dp22-coin-change2": {
        "intuition": "<p>Unlike minimum coin change, this problem counts combinations. Process denominations one at a time and update sums in ascending order so the current coin can be reused without counting different coin orders as different combinations.</p>",
        "steps": "<ol><li>Set dp[0]=1 because there is one way to make amount zero: choose no coins.</li><li>For each coin, iterate sums from coin through amount in ascending order.</li><li>Add dp[sum-coin] to dp[sum].</li><li>Return dp[amount].</li></ol>",
        "trace": "<p>For coins [1,2,3] and amount 4, the combinations are 1+1+1+1, 1+1+2, 2+2 and 1+3: four ways.</p>",
        "proof": "<p>When processing a denomination, dp[sum] counts combinations using denominations processed so far. Adding dp[sum-coin] appends at least one current coin to each combination for the smaller sum. Ascending iteration permits unlimited copies, while processing denominations in a fixed order prevents permutations from being counted separately.</p>",
        "complexity": "<p>O(numberOfCoins × amount) time and O(amount) space.</p>",
        "edge": "<p>Amount zero returns 1; a positive amount with no usable coins returns 0. Test duplicate coin denominations, coin larger than amount and large counts that may overflow the chosen numeric type.</p>",
    },
    "dp33-edit-distance": {
        "intuition": "<p>Convert a prefix of word1 into a prefix of word2. If the final characters match, no new operation is needed; otherwise the last step must be insert, delete or replace.</p>",
        "steps": "<ol><li>Define dp[i][j] as the minimum edits to convert the first i characters of word1 to the first j characters of word2.</li><li>Initialize dp[i][0]=i and dp[0][j]=j.</li><li>If characters match, copy dp[i-1][j-1].</li><li>Otherwise take 1 plus the minimum of delete, insert and replace states.</li></ol>",
        "trace": "<p>For <code>horse → ros</code>, one optimal sequence is replace h with r, delete the next r, then delete e: three operations.</p>",
        "proof": "<p>Any optimal edit sequence for two prefixes ends either with matching final characters (which need no operation) or with one of the three allowed edits. Removing that final operation yields the corresponding smaller prefix subproblem, so the recurrence considers all possible optimal endings.</p>",
        "complexity": "<p>O(mn) time and O(mn) space for the full table. Space can be reduced to O(min(m,n)) when only the distance is required.</p>",
        "edge": "<p>Test either string empty, identical strings, no shared characters, one string being a prefix of the other and repeated characters. Be explicit about whether the task also requires reconstructing the edit sequence.</p>",
    },
    "house-robber": {
        "intuition": "<p>At each house, either skip it and keep the best result through the previous house, or rob it and add its value to the best result two houses back.</p>",
        "steps": "<ol><li>Maintain prev1 as the best total through the previous house and prev2 as the best total two houses back.</li><li>For each value x, compute current=max(prev1,prev2+x).</li><li>Shift prev2=prev1 and prev1=current.</li><li>Return prev1.</li></ol>",
        "trace": "<p>For <code>[1,2,3,1]</code>, best totals evolve to 1, 2, 4, 4. The optimal choice is houses with values 1 and 3.</p>",
        "proof": "<p>An optimal solution for the first i houses either excludes house i, leaving the optimum for i-1, or includes it, forcing exclusion of i-1 and leaving the optimum for i-2. Taking the maximum covers both exhaustive cases.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space with rolling state.</p>",
        "edge": "<p>Test empty input, one house, two houses, all zeros and negative values if allowed. Whether robbing no houses is permitted affects the result for all-negative input; follow the problem's non-negative-value contract.</p>",
    },
    "knapsack-problem01": {
        "intuition": "<p>Each item is either selected once or not selected. For every item and capacity, compare skipping it with taking it and adding its value to the best solution at the remaining capacity.</p>",
        "steps": "<ol><li>Define dp[i][w] as the maximum value using the first i items with capacity w.</li><li>Initialize zero-item and zero-capacity states to zero.</li><li>If item i is too heavy, copy the previous row.</li><li>Otherwise take the maximum of skipping it and selecting it plus dp[i-1][w-weight].</li><li>For 1D compression, iterate capacities downward to avoid reusing an item.</li></ol>",
        "trace": "<p>For capacity 4 with items (weight,value) (4,1), (5,2), (1,3), the best choice is the third item alone, with value 3.</p>",
        "proof": "<p>Every feasible subset either contains the current item or does not. The two recurrence branches represent these disjoint cases, and the selected branch leaves a smaller-capacity problem over earlier items. Taking the maximum therefore yields the optimum.</p>",
        "complexity": "<p>O(nW) time. A 2D table uses O(nW) space; a 1D compressed array uses O(W) space with descending capacity iteration.</p>",
        "edge": "<p>Test capacity zero, no items, item weight exactly capacity, all items too heavy and zero-weight items if permitted. Descending iteration is essential in 1D 0/1 DP; ascending iteration would allow repeated use.</p>",
    },
    "grid-unique-paths1": {
        "intuition": "<p>To reach cell (r,c), the final move must come from above or from the left. The number of paths is the sum of those two predecessor counts.</p>",
        "steps": "<ol><li>Define dp[r][c] as the number of paths from the top-left to the cell.</li><li>Initialize the first row and first column to one, because there is only one way to move along either boundary.</li><li>For other cells, set dp[r][c]=dp[r-1][c]+dp[r][c-1].</li><li>Return the bottom-right state.</li></ol>",
        "trace": "<p>In a 2×2 grid, the destination can be reached right-then-down or down-then-right, so there are 2 paths.</p>",
        "proof": "<p>Every path to a non-origin cell has exactly one final move: from above or from the left. These cases are disjoint and cover all paths, so adding the two predecessor counts is correct.</p>",
        "complexity": "<p>O(rows×columns) time. A 2D table uses O(rows×columns) space; a rolling row uses O(columns) space.</p>",
        "edge": "<p>A one-row or one-column grid has exactly one path. Check 1×1, rectangular dimensions and count overflow for large grids. This source problem permits only right and down moves.</p>",
    },
    "frog-jump": {
        "intuition": "<p>The frog can reach stair i from i-1 or i-2. Each transition adds the absolute height difference, so dynamic programming stores the minimum energy to reach each stair.</p>",
        "steps": "<ol><li>Set dp[0]=0.</li><li>For each i≥1, compute the one-step cost from i-1.</li><li>If i≥2, also compute the two-step cost from i-2.</li><li>Store the smaller valid cost and return dp[n-1].</li></ol>",
        "trace": "<p>For heights <code>[10,20,30,10]</code>, the minimum costs are 0, 10, 20, 20. The final jump from stair 1 to 3 costs 10, giving total energy 20.</p>",
        "proof": "<p>The final jump into stair i must originate at i-1 or i-2. Replacing the path to either predecessor with a cheaper path can never worsen the final cost, so the minimum of those predecessor costs plus their jump costs is optimal.</p>",
        "complexity": "<p>O(n) time and O(n) space for a DP array; O(1) auxiliary space is possible by retaining only the previous two states.</p>",
        "edge": "<p>Test one stair (zero energy), two stairs, equal heights, large height differences and empty input if permitted. Compute absolute differences in a wide type to avoid overflow.</p>",
    },

    "bubble-sort": {
        "intuition": "<p>Bubble sort repeatedly compares adjacent values and swaps them when out of order. After each complete pass, the largest remaining value has moved to the end of the unsorted prefix.</p>",
        "steps": "<ol><li>Start at the beginning of the unsorted prefix.</li><li>Compare adjacent values and swap when their order is wrong.</li><li>Reduce the unsorted boundary after each pass.</li><li>Stop when a pass makes no swaps, if the implementation uses the early-exit optimization.</li></ol>",
        "trace": "<p>For <code>[5,1,4,2]</code>, the first pass bubbles 5 to the end; later passes place 4 and then 2, producing <code>[1,2,4,5]</code>.</p>",
        "proof": "<p>Each pass places the maximum value of the current unsorted prefix at its final sorted position. Repeating this process reduces the unsorted prefix until every position is correct.</p>",
        "complexity": "<p>O(n²) average/worst-case time. Best case is O(n) with a swap flag; without early exit it remains O(n²). O(1) auxiliary space. Stable when equal values are not swapped.</p>",
        "edge": "<p>Test empty, one-element, sorted, reverse-sorted and duplicate-heavy arrays. Verify both increasing and decreasing methods use the correct comparison direction.</p>",
    },
    "insertion-sort": {
        "intuition": "<p>Maintain a sorted prefix. Insert the next value into its correct position by shifting larger prefix values one place to the right.</p>",
        "steps": "<ol><li>Assume the first element is sorted.</li><li>Take the next element as the key.</li><li>Shift larger preceding elements right until the insertion position is found.</li><li>Place the key and continue.</li></ol>",
        "trace": "<p>For <code>[5,1,4,2]</code>, insert 1 before 5, then insert 4 between 1 and 5, then insert 2 between 1 and 4. Result: <code>[1,2,4,5]</code>.</p>",
        "proof": "<p>Before each iteration, the prefix is sorted. Shifting values greater than the key creates one vacant position at the correct insertion point, so the expanded prefix remains sorted.</p>",
        "complexity": "<p>O(n²) average/worst-case and O(n) best-case on already sorted input. O(1) auxiliary space. Stable when shifts occur only for strictly greater values; adaptive for nearly sorted data.</p>",
        "edge": "<p>Test sorted, reverse-sorted, duplicates, negative values and a one-element array. Check that equal values retain their original relative order.</p>",
    },
    "merge-sort": {
        "intuition": "<p>Divide the array into halves until each subarray has one element, then merge sorted halves. Merging two sorted sequences is linear in their combined length.</p>",
        "steps": "<ol><li>Split the current range at its midpoint.</li><li>Recursively sort the left and right halves.</li><li>Merge them by repeatedly taking the smaller front value.</li><li>Copy any remaining values from either half.</li></ol>",
        "trace": "<p><code>[5,1,4,2]</code> splits into [5,1] and [4,2], which sort to [1,5] and [2,4]. Merging yields <code>[1,2,4,5]</code>.</p>",
        "proof": "<p>Single-element arrays are sorted. Assuming each recursive half is sorted, the merge procedure repeatedly selects the smallest remaining value, so the merged range is sorted and contains every input value exactly once.</p>",
        "complexity": "<p>O(n log n) time in best, average and worst cases. Typical array merge sort uses O(n) auxiliary storage plus O(log n) recursion depth. Stable when ties are taken from the left half first.</p>",
        "edge": "<p>Test odd lengths, duplicates, already sorted and reverse-sorted input, empty ranges and integer extremes. Ensure merge indices do not skip or duplicate elements.</p>",
    },
    "quick-sort": {
        "intuition": "<p>Partition the array around a pivot so values on one side are no greater and values on the other side are no smaller; recursively sort the two partitions.</p>",
        "steps": "<ol><li>Choose a pivot according to the implementation.</li><li>Partition the current range so the pivot reaches its final position or the two partitions satisfy the partition invariant.</li><li>Recursively sort the left and right partitions.</li><li>Stop when a partition has fewer than two elements.</li></ol>",
        "trace": "<p>For <code>[5,1,4,2]</code>, choosing pivot 2 partitions smaller values to its left and larger values to its right. Recursively sorting each side yields <code>[1,2,4,5]</code>.</p>",
        "proof": "<p>Partitioning places every value in the correct side relative to the pivot. Once both sides are recursively sorted, all left values precede the pivot and all right values follow it, so the full range is sorted.</p>",
        "complexity": "<p>Expected/average O(n log n) with balanced partitions; worst-case O(n²) with repeatedly unbalanced partitions. In-place partitioning uses O(log n) expected recursion stack, O(n) worst case. Usually unstable.</p>",
        "edge": "<p>Test sorted and reverse-sorted arrays, many duplicates, all equal values and pivot extremes. Randomized or median-based pivot selection reduces the chance of consistently poor partitions.</p>",
    },
    "recursive-bubble-sort": {
        "intuition": "<p>Recursive bubble sort performs one bubble pass, which places the maximum at the end, then recursively sorts the remaining prefix.</p>",
        "steps": "<ol><li>Use the unsorted prefix length as the recursive state.</li><li>Compare and swap adjacent out-of-order values in one pass.</li><li>Reduce the prefix length by one.</li><li>Stop when fewer than two values remain.</li></ol>",
        "trace": "<p>For <code>[4,2,3,1]</code>, the first pass places 4 at the end; recursive calls then sort [2,3,1], then [2,1], giving [1,2,3,4].</p>",
        "proof": "<p>One pass places the maximum of the current prefix in its final position. By induction, the recursive call sorts the remaining prefix, so the whole array becomes sorted.</p>",
        "complexity": "<p>O(n²) time and O(n) recursion-stack space. An early-exit check can improve best-case time to O(n), if implemented.</p>",
        "edge": "<p>Test empty, one-element, sorted, reverse-sorted and duplicates. Watch the recursion base case and ensure the active prefix shrinks on every call.</p>",
    },
    "recursive-insertion-sort": {
        "intuition": "<p>Recursively sort the first n-1 elements, then insert the final element into its correct place in that sorted prefix.</p>",
        "steps": "<ol><li>Return when the prefix length is at most one.</li><li>Recursively sort the prefix excluding its final element.</li><li>Save the final value as key.</li><li>Shift larger values right and insert key into the gap.</li></ol>",
        "trace": "<p>For <code>[4,2,3]</code>, sort [4,2] recursively to [2,4], then insert 3 between them to obtain [2,3,4].</p>",
        "proof": "<p>By induction, the recursive call leaves the first n-1 values sorted. Inserting the nth value into its ordered position preserves sortedness and retains all values.</p>",
        "complexity": "<p>O(n²) worst/average time and O(n) recursion-stack space. The insertion work for each level can be linear in the prefix length.</p>",
        "edge": "<p>Test already sorted, reverse-sorted, duplicates, negative values and n=0/1. Ensure recursive depth is acceptable for the input size.</p>",
    },
    "selection-sort": {
        "intuition": "<p>At each position, select the smallest value from the unsorted suffix and swap it into the next sorted position.</p>",
        "steps": "<ol><li>For each index i, assume the prefix before i is sorted.</li><li>Scan the suffix to find its minimum index.</li><li>Swap that minimum with arr[i].</li><li>Advance i and repeat.</li></ol>",
        "trace": "<p>For <code>[5,1,4,2]</code>, the first pass selects 1 and swaps it to index 0; the next selects 2 for index 1; the remaining suffix [4,5] is already ordered.</p>",
        "proof": "<p>The selected minimum is no greater than any value in the suffix, so placing it at index i extends the sorted prefix correctly. Repeating until the suffix is empty sorts the array.</p>",
        "complexity": "<p>O(n²) comparisons in best, average and worst cases; O(1) auxiliary space. Standard selection sort is not stable and performs at most O(n) swaps.</p>",
        "edge": "<p>Test sorted, reverse-sorted, duplicates and one element. Verify that the minimum search starts at i and that the swap does not run beyond the array.</p>",
    },
    "sorting-algorithm": {
        "intuition": "<p>This file defines a shared interface for increasing/decreasing sorting implementations and a helper that generates sample integer arrays. It is a reusable contract, not a standalone sorting algorithm.</p>",
        "steps": "<ol><li>Implement both interface methods in a concrete sorter.</li><li>Define whether sorting mutates the supplied array.</li><li>Use the same comparison policy consistently for ascending and descending order.</li><li>Test with deterministic arrays rather than relying only on randomly generated examples.</li></ol>",
        "trace": "<p>Given <code>[4,1,3]</code>, an increasing implementation should produce [1,3,4], while a decreasing implementation should produce [4,3,1].</p>",
        "proof": "<p>The interface itself provides no correctness guarantee; each implementation must establish that its output is ordered and is a permutation of the input. Tests should verify both properties.</p>",
        "complexity": "<p>Complexity belongs to each concrete algorithm, not the interface. The random-array helper is O(n) time and O(n) storage for the generated array.</p>",
        "edge": "<p>Test empty arrays, duplicates, negative values and both sort directions. Randomized test data should use a fixed seed in reproducible unit tests.</p>",
    },

    "l12-reverse-singly-linked-list-recursion": {
        "intuition": "<p>Recursively reverse the suffix after the head, then attach the old head to the tail of that reversed suffix. The base case is an empty or single-node list.</p>",
        "steps": "<ol><li>Return head when it is null or has no next node.</li><li>Recursively reverse head.next and store the new head.</li><li>Set <code>head.next.next = head</code>.</li><li>Set <code>head.next = null</code> to terminate the old head, then return the new head.</li></ol>",
        "trace": "<p>For <code>1→2→3</code>, reverse [2→3] to [3→2], link 2→1, and terminate 1. The result is <code>3→2→1</code>.</p>",
        "proof": "<p>Assume the recursive call correctly reverses the suffix. Its original head becomes the suffix tail; linking that tail to the current head and clearing the old forward link extends the reversed suffix to include the current node.</p>",
        "complexity": "<p>O(n) time and O(n) recursion-stack space.</p>",
        "edge": "<p>Test empty, one node, two nodes and a long list. Recursive depth can overflow the Java stack for very long lists; the iterative three-pointer method uses O(1) auxiliary space.</p>",
    },
    "l15-length-of-loop": {
        "intuition": "<p>Floyd's tortoise-and-hare algorithm detects a cycle. Once slow and fast meet inside the cycle, keep one pointer fixed and move the other until it returns to the meeting node; the number of steps is the cycle length.</p>",
        "steps": "<ol><li>Move slow by one and fast by two until they meet or fast reaches null.</li><li>If no meeting occurs, return 0.</li><li>Starting from the meeting node, move one pointer around the cycle once while counting nodes.</li><li>Return the count.</li></ol>",
        "trace": "<p>If the cycle is <code>33→10→21→39→90→58→45→33</code>, one complete traversal returns to 33 after seven nodes, so the loop length is 7.</p>",
        "proof": "<p>In a cycle, the two pointers move at different speeds and eventually meet. Traversing from the meeting node until it is reached again visits every cycle node exactly once, so the counter equals the cycle length.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space. The detection and counting passes each traverse at most a linear number of links.</p>",
        "edge": "<p>Test no cycle, self-loop, a cycle beginning at head, a cycle after a long prefix and a two-node cycle. Return 0 when no loop exists.</p>",
    },
    "l17-odd-even-linked-list": {
        "intuition": "<p>Group nodes by their original 1-based positions, not by their stored values. Maintain separate odd and even chains while preserving each chain's order.</p>",
        "steps": "<ol><li>Keep the first node as the odd head and the second as the even head.</li><li>Advance odd to the next odd-position node and even to the next even-position node.</li><li>Reconnect each chain as it advances.</li><li>Append the even head after the odd tail.</li></ol>",
        "trace": "<p>For <code>1→2→3→4→5</code>, the odd chain becomes 1→3→5 and the even chain 2→4. Join them to obtain <code>1→3→5→2→4</code>.</p>",
        "proof": "<p>Each pointer advances by two original links, so it visits nodes of one parity in their original order. Joining the odd chain to the even head concatenates the two stable partitions.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space for the in-place pointer method.</p>",
        "edge": "<p>Test empty, one node, two nodes, odd/even length and repeated values. Do not confuse odd/even positions with odd/even node data.</p>",
    },
    "l17-segregate-even-odd-nodes": {
        "intuition": "<p>Partition nodes by the parity of their values, placing even-valued nodes before odd-valued nodes while preserving order within each group.</p>",
        "steps": "<ol><li>Create even and odd dummy heads and tails.</li><li>Traverse the original list once.</li><li>Detach each node and append it to the even or odd chain based on its value.</li><li>Join the even chain to the odd chain and return the appropriate head.</li></ol>",
        "trace": "<p>For <code>17→15→8→9→2→4→6</code>, the stable even chain is 8→2→4→6 and the odd chain is 17→15→9. Join to obtain <code>8→2→4→6→17→15→9</code>.</p>",
        "proof": "<p>Every node is visited once and appended to exactly one chain. Appending at the tail preserves encounter order in each partition; concatenating the chains places all even values before all odd values.</p>",
        "complexity": "<p>O(n) time. O(1) auxiliary space when using a constant number of pointers and reusing nodes.</p>",
        "edge": "<p>Test all-even, all-odd, empty, one node, negative values and zero (zero is even). Preserve node identity if callers hold references to existing nodes.</p>",
    },
    "l20-delete-middle-element-of-list": {
        "intuition": "<p>Slow and fast pointers find the middle in one pass. Keep a previous pointer so the node selected by the problem's even-length convention can be unlinked.</p>",
        "steps": "<ol><li>Handle an empty list and the single-node case.</li><li>Initialize slow and fast at the head and previous as null.</li><li>Advance slow by one and fast by two while fast and fast.next exist, updating previous.</li><li>Unlink slow from previous; return the updated head.</li></ol>",
        "trace": "<p>For <code>1→2→3→4→5</code>, slow reaches 3 and that node is removed, producing 1→2→4→5. For six nodes, the second middle (node 4) is removed.</p>",
        "proof": "<p>Fast advances twice as quickly as slow, so when fast reaches the end, slow is at the required middle position. The previous pointer identifies the link that must bypass slow.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test one node (return null), two nodes (delete the second middle), odd/even lengths and head/tail boundaries. Match the source's convention for even-length lists.</p>",
    },
    "l21-sort-list-of01and2s": {
        "intuition": "<p>Every node contains only 0, 1 or 2. Count the three values and rewrite node data, or build three stable chains if node values must not be changed.</p>",
        "steps": "<ol><li>Traverse once and count zeros, ones and twos.</li><li>Traverse again, writing the counted number of 0s, then 1s, then 2s into node data.</li><li>If data mutation is not permitted, instead detach nodes and append them to three bucket lists before concatenating.</li></ol>",
        "trace": "<p>For <code>1→2→2→1→2→0→2→2</code>, counts are one zero, two ones and five twos. Rewrite as <code>0→1→1→2→2→2→2→2</code>.</p>",
        "proof": "<p>The first pass counts every node in its value class. The second pass writes exactly those counts in sorted order, so all nodes' values are retained and ordered.</p>",
        "complexity": "<p>O(n) time and O(1) extra space for counting and rewriting data. Three-chain partitioning is also O(n) and uses O(1) pointer space.</p>",
        "edge": "<p>Test all one value, empty list, one node, duplicates and values outside 0..2. Clarify whether changing node data is allowed or node relinking is required.</p>",
    },
    "l23-add1-to-linked-list": {
        "intuition": "<p>The list stores a number in forward digit order, so carry propagates from the tail toward the head. Reverse the list, add one like elementary arithmetic, then reverse it back.</p>",
        "steps": "<ol><li>Reverse the digit list.</li><li>Set carry to 1 and add it to each digit.</li><li>Store digit modulo 10 and propagate the quotient as carry.</li><li>If carry remains after the final node, append a new digit.</li><li>Reverse the list back.</li></ol>",
        "trace": "<p><code>4→5→6</code> represents 456. Reversing gives 6→5→4; adding one changes the first digit to 7, then reverse back to <code>4→5→7</code>.</p>",
        "proof": "<p>After reversal, the least significant digit is processed first, exactly as in positional addition. Each node stores the current digit modulo 10 and the remaining carry is passed to the next more significant digit. Reversing restores forward representation.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space for in-place reversal and carry propagation.</p>",
        "edge": "<p>Test 0, a number not ending in 9, trailing 9s, all 9s (999 becomes 1000), leading zeros if allowed and empty input contract.</p>",
    },
    "l25-add-two-numbers-with-leading-zeros": {
        "intuition": "<p>Add the two forward-order digit lists from least significant digit to most significant digit. Reverse both inputs, add with carry, reverse the result and remove leading zeros.</p>",
        "steps": "<ol><li>Normalize leading zeros or reverse the input lists.</li><li>Add corresponding digits while either list remains or carry is non-zero.</li><li>Create each result digit from sum modulo 10 and update carry with sum divided by 10.</li><li>Reverse the result if built least-significant-first.</li><li>Remove leading zeros, retaining a single zero node for a zero result.</li></ol>",
        "trace": "<p><code>0063 + 07 = 63 + 7 = 70</code>. The output list is <code>7→0</code>, with no leading zero nodes.</p>",
        "proof": "<p>Each iteration performs one column of ordinary decimal addition. The carry contains the overflow from the previous column; after both lists are exhausted, any remaining carry becomes a final digit. Trimming leading zeros preserves numeric value.</p>",
        "complexity": "<p>O(n+m) time and O(max(n,m)) output space. Reversing inputs in place uses O(1) auxiliary pointer space but mutates them; copies avoid mutation.</p>",
        "edge": "<p>Test unequal lengths, carry across every digit, final carry, leading zeros in either input, zero plus zero and null/empty list behavior. Output should not have leading zeros unless it represents zero.</p>",
    },
    "l27-delete-all-occurrences-of-key": {
        "intuition": "<p>In a doubly linked list, each matching node can be removed by reconnecting its previous and next neighbours. Handle head changes separately because the head has no predecessor.</p>",
        "steps": "<ol><li>Traverse while saving the next pointer before any deletion.</li><li>If the current value matches key, connect previous to next.</li><li>If next exists, update its previous pointer.</li><li>If current is the head, advance head.</li><li>Continue using the saved next pointer.</li></ol>",
        "trace": "<p>For <code>2↔2↔10↔8↔4↔2↔5↔2</code> and key 2, remove each matching node. The result is <code>10↔8↔4↔5</code>.</p>",
        "proof": "<p>Deleting a node changes only its adjacent links. Updating both directions preserves the doubly linked invariant, and saving next before unlinking ensures traversal continues over every original node exactly once.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test key absent, every node matches, consecutive head matches, tail match, single node and repeated matches. Ensure both next and previous pointers remain consistent.</p>",
    },
    "l28-pairs-with-given-sum-in-doubly-linked-list": {
        "intuition": "<p>Because the doubly linked list is sorted, use two pointers at the head and tail. Their sum tells which pointer to move, just like two-sum on a sorted array.</p>",
        "steps": "<ol><li>Set left=head and right=tail.</li><li>While left is before right, compare their sum with target.</li><li>If sum is too small, advance left; if too large, move right backward.</li><li>If equal, record the pair and move both pointers inward.</li></ol>",
        "trace": "<p>For <code>1↔2↔4↔5↔6↔8↔9</code> and target 7, the pairs are (1,6) and (2,5).</p>",
        "proof": "<p>If the sum is too small, pairing the current left value with any value no greater than right cannot reach target, so left must advance. If too large, right must move backward. Each pointer movement safely eliminates impossible pairs.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary pointer space, excluding the returned pair collection.</p>",
        "edge": "<p>Test no pair, one pair, multiple pairs, target below/above all sums and pointer crossing. The source assumes sorted, positive, distinct values; duplicates require a defined pair multiplicity policy.</p>",
    },
    "l29-remove-duplicates-from-sorted-doubly-linked-list": {
        "intuition": "<p>In a sorted doubly linked list, duplicate values appear consecutively. Keep the first node of each run and unlink subsequent nodes with the same value.</p>",
        "steps": "<ol><li>Start at the head and inspect each node's next pointer.</li><li>While next exists and has the same value, bypass that duplicate node.</li><li>Update the successor's previous pointer after bypassing.</li><li>Advance to the next distinct node.</li></ol>",
        "trace": "<p>For <code>1↔1↔1↔2↔3↔4</code>, retain the first 1 and remove the next two. The result is <code>1↔2↔3↔4</code>.</p>",
        "proof": "<p>Sorted order guarantees all duplicates of a value form one contiguous run. Retaining the first and bypassing the rest leaves exactly one node per distinct value while preserving order and repairing backward links.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty, one node, all duplicates, no duplicates, duplicate runs at the head and tail. Verify previous pointers after each deletion.</p>",
    },
    "l31-rotate-linked-list-by-k-anti-clockwise": {
        "intuition": "<p>A left rotation by k moves the first k nodes to the tail. Find the kth node, connect the old tail to the old head temporarily, then break the cycle after the kth node.</p>",
        "steps": "<ol><li>Handle empty/single-node lists and normalize k if the contract permits k greater than length.</li><li>Find the length and tail.</li><li>Find the kth node and set newHead to kth.next.</li><li>Connect tail.next to old head.</li><li>Set kth.next to null and return newHead.</li></ol>",
        "trace": "<p>For <code>2→4→7→8→9</code> and k=3, the new head is 8. Connect old tail 9 to old head 2, then break after 7 to obtain <code>8→9→2→4→7</code>.</p>",
        "proof": "<p>The temporary circular link preserves the original cyclic order. Choosing the node after the first k nodes as the new head and breaking at the kth node yields exactly the original suffix followed by the original prefix.</p>",
        "complexity": "<p>O(n) time to find length and boundary nodes; O(1) auxiliary space.</p>",
        "edge": "<p>Test k=0, k=length, k=1, one node and empty list. If k may exceed length, use k modulo length; the source contract says k is at most length.</p>",
    },
    "l32-flattening-linked-list": {
        "intuition": "<p>Each top-level node heads a sorted bottom chain. Flattening is a multiway merge of these sorted chains; merge two lists at a time or use a min-heap across all heads.</p>",
        "steps": "<ol><li>Recursively flatten the list to the right, or iterate over top-level heads.</li><li>Merge the current bottom chain with the already flattened remainder by comparing node values.</li><li>Link chosen nodes through bottom pointers.</li><li>Clear or ignore next pointers according to the required flattened representation.</li></ol>",
        "trace": "<p>Merge the sorted chains 5→7→8 and 10→20, then merge the result with 19→22→50 and 28→35→40→45. The final bottom chain is sorted across all nodes.</p>",
        "proof": "<p>Merging two sorted chains produces one sorted chain containing all nodes from both. Repeating this merge across all top-level lists preserves sorted order and includes every node exactly once.</p>",
        "complexity": "<p>Pairwise merging is typically O(N*k) for k chains of total N nodes in a simple recursive implementation; a heap-based merge is O(N log k). Auxiliary space depends on recursion or heap usage.</p>",
        "edge": "<p>Test one chain, empty chains, duplicate values, highly uneven chain lengths and null bottom pointers. The output is traversed using bottom, not next.</p>",
    },
    "l34-browser-history": {
        "intuition": "<p>Browser history is a sequence with a current position. Visiting a new URL discards the forward suffix; back and forward move the current position within bounds.</p>",
        "steps": "<ol><li>Store the homepage as the initial history and set current index to 0.</li><li>On visit, remove entries after current, append the new URL and move current to the end.</li><li>On back, subtract at most the available number of previous steps.</li><li>On forward, add at most the available number of next steps.</li><li>Return the URL at current.</li></ol>",
        "trace": "<p>After visiting A, B, C, backing twice reaches A. Forward once reaches B. Visiting D from B removes C from forward history, leaving homepage→A→B→D.</p>",
        "proof": "<p>The list represents the complete retained navigation sequence and current index identifies the active page. Truncating after current enforces the rule that a new visit clears forward history; bounded index movement implements back/forward semantics.</p>",
        "complexity": "<p>With an array/list, visit is O(f) to remove the forward suffix in the worst case, while back/forward are O(1). A doubly linked list gives O(1) movement and truncation when nodes are maintained directly.</p>",
        "edge": "<p>Test back beyond the homepage, forward beyond the latest page, visit after moving backward, repeated visits to the same URL and zero steps. New visits must discard all forward entries.</p>",
    },
    "l3-delete-nth-node": {
        "intuition": "<p>Delete a node by its 1-based position. A previous pointer is needed to bypass the selected node; deleting position 1 is a special head update.</p>",
        "steps": "<ol><li>If x is 1, return head.next.</li><li>Traverse to the node immediately before position x.</li><li>If the requested node exists, set previous.next to target.next.</li><li>Return the possibly updated head.</li></ol>",
        "trace": "<p>For <code>1→5→2→9</code> and x=2, bypass node 5 by setting 1.next to 2. Result: <code>1→2→9</code>.</p>",
        "proof": "<p>For a non-head node, replacing the predecessor's next pointer with the target's successor removes exactly the target from the reachable chain. For the head, returning the second node removes the first.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test deleting head, tail, only node, invalid x greater than length and empty input. Confirm whether invalid positions are ignored or reported by the API.</p>",
    },
    "bst2-search-for-node-in-bst": {
        "intuition": "<p>A BST orders every key in the left subtree below the node and every key in the right subtree above it. Compare the target with the current node and discard one entire subtree at each step.</p>",
        "steps": "<ol><li>Start at the root.</li><li>If the current key equals the target, report found.</li><li>If target is smaller, move left; if larger, move right.</li><li>If the pointer becomes null, the key is absent.</li></ol>",
        "trace": "<p>At node 2, searching for 87 moves right to 81; 87 is greater, so move right again and find 87.</p>",
        "proof": "<p>The BST ordering invariant guarantees that when target is smaller than the current key it cannot occur in the right subtree, and vice versa. Each comparison therefore safely eliminates one subtree.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space iteratively, where h is tree height. This is O(log n) for a balanced BST and O(n) in the worst case.</p>",
        "edge": "<p>Test empty tree, root match, missing key, minimum/maximum key and a skewed tree. State how duplicates are handled; the source contract should define whether keys are unique.</p>",
    },
    "bst6-insert-node": {
        "intuition": "<p>Insertion follows the same comparisons as search. The first null child reached is the unique position that preserves the BST ordering invariant.</p>",
        "steps": "<ol><li>If the tree is empty, create and return the root.</li><li>Walk down the tree, comparing key with current node.</li><li>Move left or right according to the ordering.</li><li>When the chosen child is null, attach the new node there and return the original root.</li><li>If the key already exists, leave the tree unchanged as required by this source statement.</li></ol>",
        "trace": "<p>Insert 4 into a tree with root 2 and children 1 and 3: compare 4 with 2 (right), then with 3 (right), then attach 4 as the right child of 3.</p>",
        "proof": "<p>Every descent follows the only subtree that can contain the key under BST ordering. Attaching at the first null child places the new key within all ancestor bounds, preserving the invariant. Existing keys are not inserted again.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space for iterative insertion; recursive insertion uses O(h) call stack.</p>",
        "edge": "<p>Test empty tree, duplicate key, insertion as new minimum/maximum, insertion into a skewed tree and negative keys if allowed. Return the original root unless the tree was empty.</p>",
    },
    "bst7-delete-node": {
        "intuition": "<p>Deletion has three structural cases: leaf, one child, or two children. The two-child case is handled by replacing the node's key with its in-order successor (or predecessor), then deleting that replacement node from its simpler location.</p>",
        "steps": "<ol><li>Search for the key while retaining the parent/link context.</li><li>If absent, return the tree unchanged.</li><li>If the node has zero or one child, replace its link with its only child (or null).</li><li>If it has two children, find the minimum in the right subtree, copy its value, and delete that successor node.</li><li>Return the possibly changed root.</li></ol>",
        "trace": "<p>Deleting a node with two children uses the smallest value in its right subtree. That successor is greater than every value in the left subtree and no greater than the remaining right-subtree values, so it can replace the deleted key.</p>",
        "proof": "<p>For zero/one child, splicing in the child preserves all ancestor ordering bounds. For two children, the in-order successor is the smallest key greater than the deleted key; replacing the key with it preserves the ordering, and removing the successor cannot violate the right subtree because it has no left child.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space iteratively; recursive implementations use O(h) stack.</p>",
        "edge": "<p>Test deleting the root, leaf, node with only left/right child, node with two children, absent key and deleting the only node. Ensure parent/root references are updated correctly.</p>",
    },
    "bst8-kth-smallest-in-bst": {
        "intuition": "<p>In-order traversal of a BST visits keys in ascending order. The kth visited node is therefore the kth smallest. An explicit stack performs iterative in-order traversal.</p>",
        "steps": "<ol><li>Push the current node and all its left descendants onto a stack.</li><li>Pop the next node; decrement k and return its value when k reaches zero.</li><li>Move to the popped node's right child and repeat.</li><li>If traversal ends before k nodes, the requested rank is invalid.</li></ol>",
        "trace": "<p>For BST root 2 with children 1 and 3, in-order order is 1,2,3. For k=2, the second popped node is 2.</p>",
        "proof": "<p>BST ordering ensures all left-subtree values are smaller than the node and all right-subtree values are larger. In-order traversal lists every node exactly once in sorted order, so counting to k returns the kth smallest.</p>",
        "complexity": "<p>O(h+k) time until the kth node is visited and O(h) auxiliary stack space. A full traversal is O(n).</p>",
        "edge": "<p>Test k=1, k=n, k=0, k greater than n, duplicate-key policy and a skewed tree. The source requirement says O(1) extra space; if its implementation uses a stack, note that this is O(h) auxiliary space and a Morris traversal is needed for strict O(1) auxiliary space.</p>",
    },
    "bst11-lowest-common-ancestor-in-bst": {
        "intuition": "<p>In a BST, the LCA is the first node whose key lies between the two target values. If both targets are smaller, move left; if both are larger, move right.</p>",
        "steps": "<ol><li>Normalize the two target values as low and high.</li><li>Start at the root.</li><li>If current key is greater than high, move left.</li><li>If current key is smaller than low, move right.</li><li>Otherwise current lies between the targets and is their LCA.</li></ol>",
        "trace": "<p>For targets 7 and 8 in a BST rooted at 5, move right to 6, then right to 7. Since 7 lies within [7,8], it is the LCA.</p>",
        "proof": "<p>When both targets lie on one side, their lowest common ancestor must also lie on that side, so moving there cannot skip the answer. When they split across sides or one equals the current node, the current node is the first node common to both search paths.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space iteratively.</p>",
        "edge": "<p>Test one target as ancestor of the other, targets in opposite subtrees, one target equal to root and absent values. The source assumes unique values and distinct target values.</p>",
    },
    "bst14-bst-iterator": {
        "intuition": "<p>The iterator should produce BST values in ascending order without materializing the entire traversal. Keep a stack of the path to the next smallest unvisited node.</p>",
        "steps": "<ol><li>During construction, push the root and its full left spine.</li><li><code>hasNext()</code> checks whether the stack is non-empty.</li><li><code>next()</code> pops the smallest pending node.</li><li>Then push the left spine of that node's right subtree.</li></ol>",
        "trace": "<p>For a BST with values 1,2,3, the initial stack contains the path to 1. Calling next returns 1 and pushes the path from 2; subsequent calls return 2 then 3.</p>",
        "proof": "<p>The stack contains the unvisited ancestors that may be next in in-order order. Popping the top yields the smallest pending node; its right subtree is the only region that can follow it, and pushing that subtree's left spine restores the invariant.</p>",
        "complexity": "<p>O(h) initialization, O(1) amortized time per next() because each node is pushed and popped once, and O(h) auxiliary space.</p>",
        "edge": "<p>Test empty tree, one node, skewed trees and repeated hasNext calls. The source guarantees next() is called only when hasNext() is true.</p>",
    },
    "st5-valid-parentheses": {
        "intuition": "<p>Balanced brackets are properly nested, so the most recently opened bracket must be the first one closed. This is exactly last-in, first-out behaviour.</p>",
        "steps": "<ol><li>Scan characters from left to right.</li><li>Push each opening bracket.</li><li>For a closing bracket, reject if the stack is empty or its top is not the matching opener.</li><li>Pop the matching opener.</li><li>At the end, the string is valid only if the stack is empty.</li></ol>",
        "trace": "<p>For <code>{[()]}</code>, push {, [, (, then each closer matches and pops the top. The stack ends empty, so the string is valid.</p>",
        "proof": "<p>Every closing bracket must match the most recent unmatched opener; otherwise nesting order is violated. The stack stores exactly those unmatched openers. Matching/pop preserves this invariant, and an empty final stack means every opener was closed.</p>",
        "complexity": "<p>O(n) time and O(n) worst-case auxiliary space.</p>",
        "edge": "<p>Test empty string, only openers, only closers, mismatched types, correct nesting and adjacent pairs. A string containing non-bracket characters must follow the exact problem contract.</p>",
    },
    "st6-min-stack1": {
        "intuition": "<p>A normal stack exposes only the top, but getMin must return the smallest value among all active elements in O(1). Store the minimum associated with each pushed element (or maintain an auxiliary minimum stack).</p>",
        "steps": "<ol><li>On push, compute the new minimum as min(value,currentMinimum).</li><li>Store the value and its corresponding minimum.</li><li>On pop, remove both top records.</li><li>top returns the stored value; getMin returns the minimum stored at the top.</li></ol>",
        "trace": "<p>Push 5, then 2, then 7. The minimum snapshots are 5, 2, 2. After popping 7, getMin remains 2; after popping 2, it returns 5.</p>",
        "proof": "<p>Each stack entry records the minimum of the prefix ending at that entry. Since pop removes the final prefix element, the previous entry automatically exposes the previous minimum. Thus getMin reads the correct value in constant time.</p>",
        "complexity": "<p>O(1) time per push, pop, top and getMin. The auxiliary minimum information costs O(n) space.</p>",
        "edge": "<p>Test duplicate minimum values, popping the current minimum, negative values, one element and empty-stack API behaviour. Ensure minimum state is restored correctly after pop.</p>",
    },
    "st8-next-greater-element": {
        "intuition": "<p>The next greater element is the nearest value to the right that is strictly larger. A monotonic decreasing stack stores indices whose answer has not yet been found.</p>",
        "steps": "<ol><li>Scan the array from left to right.</li><li>While the stack is non-empty and the current value is greater than the value at its top index, assign the current value as that index's answer and pop.</li><li>Push the current index.</li><li>Initialize all answers to -1; indices remaining in the stack have no greater value to their right.</li></ol>",
        "trace": "<p>For <code>[1,3,2,4]</code>, 3 resolves 1's answer; 4 resolves both 2 and 3. The final answer is <code>[3,4,4,-1]</code>.</p>",
        "proof": "<p>When current value is greater than a stacked value, it is the first greater value encountered to that value's right because the scan has not previously found one. Popping it finalizes the answer. Each index is pushed and popped at most once.</p>",
        "complexity": "<p>O(n) time and O(n) auxiliary space. Although there is a while loop inside the scan, each element enters and leaves the stack at most once.</p>",
        "edge": "<p>Test strictly increasing/decreasing arrays, duplicates (strictly greater means equal values do not resolve), negative values, one element and empty input.</p>",
    },
    "st13-asteroid-collision": {
        "intuition": "<p>Only a right-moving asteroid followed by a left-moving asteroid can collide. A stack stores surviving asteroids; each incoming negative asteroid may repeatedly collide with positive asteroids at the top.</p>",
        "steps": "<ol><li>Process asteroids from left to right.</li><li>While current is negative and stack top is positive, compare magnitudes.</li><li>If top is smaller, pop it and continue; if equal, pop it and destroy current; if top is larger, destroy current.</li><li>If current survives, push it.</li><li>Return the stack in order.</li></ol>",
        "trace": "<p>For <code>[3,5,-3]</code>, -3 collides with 5 and is destroyed because 5 is larger. The survivors are [3,5].</p>",
        "proof": "<p>Any possible collision must involve a previously processed right-moving asteroid and the current left-moving one. Resolving the top collision first is necessary because that is the nearest possible opponent; after a smaller asteroid explodes, the current one may meet the next survivor. The stack therefore maintains the surviving order.</p>",
        "complexity": "<p>O(n) time and O(n) auxiliary space; each asteroid is pushed and popped at most once.</p>",
        "edge": "<p>Test same-direction asteroids, equal-size collision, chains of collisions, zero if allowed and large negative values. Compare magnitudes carefully because abs(Integer.MIN_VALUE) overflows.</p>",
    },

    "bt17-check-two-binary-trees-identical": {
        "intuition": "<p>Two binary trees are identical only when their structure and corresponding node values match. Recursively compare matching positions.</p>",
        "steps": "<ol><li>If both nodes are null, return true.</li><li>If exactly one is null or values differ, return false.</li><li>Compare left subtrees and right subtrees recursively.</li><li>Return true only when both comparisons succeed.</li></ol>",
        "trace": "<p>Trees with root 1, left child 2 and right child 3 are identical. A second tree with children swapped is not, even though it contains the same values.</p>",
        "proof": "<p>The recursive definition checks the root value and requires equality of both corresponding subtrees. By induction, it checks every node and every null/non-null structural position.</p>",
        "complexity": "<p>O(min(n,m)) time until a mismatch is found; O(h) recursion space. Worst case visits all corresponding nodes.</p>",
        "edge": "<p>Test both empty, one empty, different root values, same values but different structure, and identical skewed trees.</p>",
    },
    "bt19-boundary-traversal-of-binary-tree": {
        "intuition": "<p>The boundary is the root, then the left boundary excluding leaves, all leaves left-to-right, and the right boundary excluding leaves in reverse order. Separating these phases prevents duplicates.</p>",
        "steps": "<ol><li>Add the root once.</li><li>Walk down the left boundary, preferring left then right, excluding leaves.</li><li>Traverse all leaves from left to right.</li><li>Collect the right boundary, preferring right then left, excluding leaves; append it in reverse.</li></ol>",
        "trace": "<p>For root 1, left boundary 2, leaves 4,8,9,6,7 and right boundary 3, the traversal is <code>1,2,4,8,9,6,7,3</code>.</p>",
        "proof": "<p>The phases partition boundary nodes into root, non-leaf left edge, leaves, and non-leaf right edge. Each phase follows the required direction and excludes nodes owned by earlier phases, so every boundary node appears exactly once in boundary order.</p>",
        "complexity": "<p>O(n) time and O(h) auxiliary recursion/stack space for leaf and boundary traversal, excluding output.</p>",
        "edge": "<p>Test empty, single node, root with only left or right subtree, skewed tree and a root whose child is a leaf. Avoid adding leaf nodes twice.</p>",
    },
    "bt20-vertical-order-traversal": {
        "intuition": "<p>Assign each node a horizontal distance (column) from the root: left decreases it and right increases it. BFS preserves top-to-bottom order; store values by column and then emit columns from smallest to largest.</p>",
        "steps": "<ol><li>Queue pairs of node and column, starting at column 0.</li><li>For each dequeued node, append its value to that column's sequence.</li><li>Enqueue left child at column-1 and right child at column+1.</li><li>Output columns in ascending column order, preserving BFS order within each column.</li></ol>",
        "trace": "<p>For a root 1 with children 2 and 3, their columns are -1 and +1; root is column 0. Deeper nodes are appended to the column they occupy in level order.</p>",
        "proof": "<p>The column coordinate uniquely represents horizontal displacement. BFS visits nodes in non-decreasing depth, so insertion order within each column matches the required level-order tie handling. Sorting column keys yields left-to-right output.</p>",
        "complexity": "<p>O(n log c) time when ordered maps sort c columns; O(n) storage. A hash map plus sorted keys has similar ordering cost.</p>",
        "edge": "<p>Test left/right skewed trees, multiple nodes sharing a column and depth, negative columns and empty tree. Some vertical traversal variants additionally sort ties by node value; follow the exact source contract.</p>",
    },
    "bt21-top-view-of-binary-tree": {
        "intuition": "<p>Each horizontal distance contributes the first node encountered from the top. BFS visits shallower nodes before deeper nodes, so the first value recorded for a column is visible from above.</p>",
        "steps": "<ol><li>Queue the root with horizontal distance 0.</li><li>For each node, store its value only if its distance has not been seen.</li><li>Enqueue left at distance-1 and right at distance+1.</li><li>Return recorded values in ascending horizontal-distance order.</li></ol>",
        "trace": "<p>For root 1 with children 2 and 3, the columns -1, 0, +1 first receive 2, 1, 3; top view is <code>[2,1,3]</code>.</p>",
        "proof": "<p>BFS processes nodes in increasing depth. The first node encountered at a horizontal distance is therefore a shallowest node at that column; retaining it implements the top-view rule. Ordered columns produce left-to-right output.</p>",
        "complexity": "<p>O(n log c) time with an ordered map of c columns, and O(n) queue/map space.</p>",
        "edge": "<p>Test a single node, left/right chains, two nodes sharing a column and a deeper node hidden behind a shallower one. Tie behavior must match the source's BFS ordering rule.</p>",
    },
    "bt22-bottom-view-of-binary-tree": {
        "intuition": "<p>For each horizontal distance, keep the node that is deepest. BFS visits nodes level by level; overwriting the value for a column means the last visited node becomes its bottom view.</p>",
        "steps": "<ol><li>Queue the root with horizontal distance 0.</li><li>For every dequeued node, overwrite the map entry for its column.</li><li>Enqueue left and right children at column-1 and column+1.</li><li>Return map values in ascending column order.</li></ol>",
        "trace": "<p>For the common example rooted at 20, the bottom view across columns is <code>5,10,3,14,25</code>. At a shared depth and column, later BFS order wins as specified by the source.</p>",
        "proof": "<p>BFS visits nodes in non-decreasing depth. Overwriting a column on each visit leaves a deepest node for that column. Ordered column keys provide left-to-right output; processing order resolves equal-depth ties.</p>",
        "complexity": "<p>O(n log c) time with ordered columns and O(n) auxiliary queue/map space.</p>",
        "edge": "<p>Test left/right chains, nodes sharing a column at different depths, equal-depth collisions, a single node and empty tree. Tie policy matters when two nodes have the same depth and horizontal distance.</p>",
    },
    "bt23-left-view-of-binary-tree": {
        "intuition": "<p>The left view contains the first node encountered at each depth. Level-order traversal makes that node the first item in each level.</p>",
        "steps": "<ol><li>Run BFS using a queue.</li><li>Capture the queue size at the start of each level.</li><li>Record the first node removed for that level.</li><li>Enqueue its children and continue.</li></ol>",
        "trace": "<p>For a tree with root 1, left child 2, and left grandchild 4, the first node at each level is 1, 2, 4, so the left view is <code>[1,2,4]</code>.</p>",
        "proof": "<p>BFS processes each level from left to right. The first dequeued node at a depth is therefore the leftmost node at that depth and is exactly the visible left-view node.</p>",
        "complexity": "<p>O(n) time and O(w) queue space, where w is maximum tree width.</p>",
        "edge": "<p>Test empty tree, one node, right-only chains (the right child is still visible), and levels where the left subtree is missing.</p>",
    },
    "gd4-jump-game": {
        "intuition": "<p>Track the farthest index reachable from any position visited so far. If the current index lies beyond that frontier, it cannot be reached; otherwise extend the frontier by the current jump capacity.</p>",
        "steps": "<ol><li>Initialize farthest=0.</li><li>Scan indices from left to right while i≤farthest.</li><li>Update farthest=max(farthest,i+arr[i]).</li><li>If farthest reaches the final index, return true; if the scan stops first, return false.</li></ol>",
        "trace": "<p>For <code>[1,2,0,3,0,0]</code>, index 0 reaches 1; index 1 extends reach to 3; index 3 reaches the final index 5. The destination is reachable.</p>",
        "proof": "<p>Farthest is the maximum endpoint reachable using any already reachable index at or before the current scan position. An index beyond farthest is unreachable, so no later index can be used to extend reach. The scan therefore determines reachability exactly.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test one element (already at destination), zero at the first index, a zero that blocks progress, a jump directly to the end and large jump values. Input values are non-negative maximum jump lengths.</p>",
    },
    "gd5-jump-game-ii": {
        "intuition": "<p>Think of all indices reachable with the current number of jumps as one BFS-like layer. Scan that layer to find the farthest endpoint for the next jump, then advance to the next layer.</p>",
        "steps": "<ol><li>Track current layer end, farthest reach and jump count.</li><li>Scan indices within the current layer, updating farthest with i+arr[i].</li><li>When i reaches the layer end, increment jumps and set the next layer end to farthest.</li><li>If farthest cannot advance, the end is unreachable; return -1.</li></ol>",
        "trace": "<p>For <code>[1,3,5,8,9,2,6,7,6,8,9]</code>, the first layer reaches index 1, the next layer extends to index 4, and the next reaches the last index: three jumps.</p>",
        "proof": "<p>All indices in a layer are reachable using the same number of jumps. The farthest endpoint among them is the largest set of positions reachable with one additional jump. Choosing this maximal next layer cannot require more jumps than choosing a shorter reach, so the greedy layer expansion is optimal.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test one element, immediate jump to end, zeros that block progress, exact landing on the last index and unreachable input. Follow the source contract and return -1 when unreachable.</p>",
    },
    "gd7-nmeetings-in-one-room": {
        "intuition": "<p>To maximize the number of non-overlapping meetings, choose the meeting that finishes earliest among those currently available. This leaves the largest possible remaining time for later meetings.</p>",
        "steps": "<ol><li>Pair each start and end time with its original index if required.</li><li>Sort meetings by increasing end time.</li><li>Select the first meeting.</li><li>Select each later meeting only when its start is strictly greater than the end of the last selected meeting.</li><li>Return the selected count or indices as required.</li></ol>",
        "trace": "<p>For intervals (1,2), (3,4), (0,6), (5,7), (8,9), (5,9), select (1,2), (3,4), (5,7), (8,9): four meetings.</p>",
        "proof": "<p>Let G be the earliest-finishing available meeting and O the first meeting in an optimal schedule. Since G ends no later than O, replacing O with G cannot invalidate any meeting that followed O. Thus some optimal schedule begins with G; applying the same argument to the remaining time proves the greedy choice optimal.</p>",
        "complexity": "<p>O(n log n) time for sorting and O(n) storage if meeting records are created.</p>",
        "edge": "<p>The source says a meeting starting exactly when another ends is not allowed, so use start &gt; lastEnd, not ≥. Test identical end times, meetings that all overlap, already sorted input and tie-breaking when original indices matter.</p>",
    },
    "gd9-merge-overlapping-intervals": {
        "intuition": "<p>After sorting intervals by start time, any interval that overlaps the current merged interval can be absorbed by extending its end. A gap means the current interval is complete.</p>",
        "steps": "<ol><li>Sort intervals by start.</li><li>Initialize the current merged interval from the first interval.</li><li>For each next interval, if its start is at most the current end, extend current end to the maximum end.</li><li>Otherwise emit the current interval and start a new one.</li><li>Emit the final interval.</li></ol>",
        "trace": "<p>For <code>[[1,3],[2,4],[6,8],[9,10]]</code>, [1,3] and [2,4] merge into [1,4]; [6,8] and [9,10] remain separate.</p>",
        "proof": "<p>Sorting ensures no later interval can start before the current interval. If the next start is within the current end, their union is one continuous interval; otherwise a gap proves they cannot overlap with any later interval in this group. The emitted intervals are therefore disjoint and cover the same points as the input.</p>",
        "complexity": "<p>O(n log n) time for sorting and O(n) output space. If sorting in place, extra working space depends on the sorting implementation.</p>",
        "edge": "<p>Test empty input, one interval, nested intervals, identical intervals, touching endpoints and already disjoint intervals. Whether endpoint equality counts as overlap depends on the problem's interval convention.</p>",
    },
    "gd10-insert-interval": {
        "intuition": "<p>The existing intervals are already sorted and non-overlapping. The new interval can be inserted by copying intervals before it, merging all overlaps into it, then appending the remaining intervals.</p>",
        "steps": "<ol><li>Append all intervals ending before the new interval starts.</li><li>While intervals start before or at the new interval's end, expand the new interval's start/end to include them.</li><li>Append the merged new interval.</li><li>Append all remaining intervals.</li></ol>",
        "trace": "<p>Insert [5,6] into <code>[[1,3],[10,15],[20,30]]</code>. Copy [1,3], insert [5,6], then append [10,15] and [20,30].</p>",
        "proof": "<p>Because the input is sorted and non-overlapping, every interval before the overlap region is permanently separate. All intervals intersecting the new interval form one contiguous block in sorted order, whose union is represented by the minimum start and maximum end. Later intervals cannot overlap that merged range once the scan exits.</p>",
        "complexity": "<p>O(n) time and O(n) output space.</p>",
        "edge": "<p>Test insertion at beginning/end, no overlap, overlap with one or many intervals, new interval containing all existing intervals and touching endpoints. The source contract determines whether endpoint equality is overlap.</p>",
    },
    "gd12-valid-parenthesis-string": {
        "intuition": "<p>The asterisk can act as an opening bracket, closing bracket or empty string. Track the minimum and maximum possible number of unmatched opening brackets after each prefix rather than exploring all choices.</p>",
        "steps": "<ol><li>Initialize minOpen=maxOpen=0.</li><li>For '(' increment both bounds.</li><li>For ')' decrement both bounds.</li><li>For '*', decrement minOpen (treat as ')') and increment maxOpen (treat as '(').</li><li>Clamp minOpen at zero; if maxOpen becomes negative, no interpretation can be valid.</li><li>At the end, valid iff minOpen is zero.</li></ol>",
        "trace": "<p>For <code>(*)</code>, the star may be empty or a closing bracket. The range of possible unmatched opens includes zero at the end, so the string is valid.</p>",
        "proof": "<p>The interval [minOpen,maxOpen] bounds all achievable unmatched-open counts for the processed prefix. Each character transforms every possible count by -1, 0 or +1 as allowed; clamping the minimum at zero removes impossible negative counts. If maxOpen falls below zero no assignment can balance the prefix; if zero is achievable at the end, a valid assignment exists.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty string, only opens, only closes, stars alone, star as empty, multiple valid interpretations and a prefix with too many closing brackets. This greedy range technique relies on the exact three-way '*' rule.</p>",
    },
    "generate-parentheses": {
        "intuition": "<p>Build the string one character at a time while maintaining the prefix invariant: never place more closing brackets than opening brackets, and never use more than n of either.</p>",
        "steps": "<ol><li>Start with an empty builder and counts open=close=0.</li><li>Add '(' when open&lt;n.</li><li>Add ')' when close&lt;open.</li><li>When both counts reach n, emit the completed string.</li><li>Backtrack after each recursive choice.</li></ol>",
        "trace": "<p>For n=2, valid outputs are <code>(())</code> and <code>()()</code>. A prefix like <code>)(</code> is never generated because a close cannot be added before an unmatched open.</p>",
        "proof": "<p>Every generated prefix satisfies close≤open, so no prefix can become invalid. Every well-formed string must begin with an opening bracket and at each position obey the same count constraints; the recursion explores both legal next choices, so every valid string is generated.</p>",
        "complexity": "<p>The number of outputs is the nth Catalan number Cn; writing each string costs O(n), so time is O(n·Cn). Output storage is O(n·Cn), with O(n) recursion depth excluding results.</p>",
        "edge": "<p>n=0 conventionally produces one empty string; n=1 produces one pair. Ensure the mutable builder is restored after each recursive branch.</p>",
    },
    "permutations": {
        "intuition": "<p>A permutation is built by choosing one unused value for each next position. Backtracking explores every possible choice and undoes it before trying the next.</p>",
        "steps": "<ol><li>Maintain a current path and a used marker for each input index.</li><li>If path length equals n, copy it into the result.</li><li>Otherwise choose each unused index, mark it used and append its value.</li><li>Recurse, then remove the last value and clear its used marker.</li></ol>",
        "trace": "<p>For [1,2,3], start with 1, then explore 2→3 and 3→2; backtrack and repeat beginning with 2 and 3. There are six permutations.</p>",
        "proof": "<p>At each depth, every unused input index is considered exactly once. Each complete path uses every index once, so it is a permutation; every possible ordering corresponds to one unique sequence of choices and is therefore generated.</p>",
        "complexity": "<p>O(n·n!) time to construct/copy all permutations and O(n) auxiliary recursion/path/used space, excluding O(n·n!) output storage.</p>",
        "edge": "<p>Test empty input, one element, repeated values and large n. The source statement assumes distinct integers; duplicates require deduplication or a frequency-count backtracking strategy to avoid repeated permutations.</p>",
    },
    "subsets": {
        "intuition": "<p>For each element, a subset either includes it or excludes it. Recursion explores these two branches, producing every subset exactly once.</p>",
        "steps": "<ol><li>At index i, first recurse without including the current value.</li><li>Append the current value and recurse with it included.</li><li>Backtrack by removing the appended value.</li><li>When all indices are processed, copy the current subset into the result.</li></ol>",
        "trace": "<p>For [1,2], the branches produce [], [2], [1], [1,2] (ordering depends on branch order): four subsets.</p>",
        "proof": "<p>Each input element has exactly two independent choices. The recursion explores both for every index, so it covers all 2^n inclusion bitmasks. Each bitmask determines one unique subset of input positions.</p>",
        "complexity": "<p>O(n·2^n) time to copy all subsets, O(n) recursion/path space, and O(n·2^n) output storage.</p>",
        "edge": "<p>The empty subset must be included. Test empty input, one element and repeated values. If values repeat and subsets are defined by values rather than positions, clarify whether duplicate result sets should be removed.</p>",
    },
    "combination-sum1": {
        "intuition": "<p>Choose candidates in a fixed non-decreasing index order. Because a candidate may be reused, recurse from the same index after choosing it; move to the next index when skipping it.</p>",
        "steps": "<ol><li>Sort candidates if the implementation relies on early stopping.</li><li>At each index, try taking the current value if it does not exceed the remaining target.</li><li>After taking it, recurse with the same index to allow reuse.</li><li>Also explore skipping it by moving to the next index.</li><li>When remaining target is zero, copy the current combination.</li></ol>",
        "trace": "<p>For candidates [2,3,6,7] and target 7, the valid combinations are [2,2,3] and [7].</p>",
        "proof": "<p>Every combination has a unique representation by non-decreasing candidate indices. The take branch includes another copy of the current candidate; the skip branch excludes it permanently. These branches partition the solution space, preventing permutations of the same combination from being counted separately.</p>",
        "complexity": "<p>Exponential in the number of possible combinations; the search-tree bound depends on target and the smallest candidate. Auxiliary recursion/path space is O(target/minCandidate) in the deepest reuse path, excluding output.</p>",
        "edge": "<p>Test target zero, no solution, candidate larger than target and repeated values in the candidate list. Candidates must be positive to guarantee progress in unlimited-reuse recursion; zero/negative values can cause non-termination or invalidate pruning.</p>",
    },
    "n-queen-version2": {
        "intuition": "<p>Place one queen per row. For each row, try columns that are not attacked by an earlier queen; backtracking removes a placement when it leads to no complete board.</p>",
        "steps": "<ol><li>Process rows from top to bottom.</li><li>For each column, check column, main diagonal (row-col) and anti-diagonal (row+col) occupancy.</li><li>If safe, mark all three, record the queen and recurse to the next row.</li><li>When all rows are filled, copy the board/column placement to results.</li><li>Undo the marks during backtracking.</li></ol>",
        "trace": "<p>For n=4, one solution places queens in columns [2,4,1,3] using 1-based columns. Each new row avoids occupied columns and both diagonal directions.</p>",
        "proof": "<p>Every valid board has exactly one queen in each row, so its row-by-row column sequence is explored by the recursion. Safety checks reject exactly those placements sharing a column or diagonal with an earlier queen. Thus every emitted board is valid and every valid board is reachable.</p>",
        "complexity": "<p>Worst-case search is exponential (bounded by permutations of columns, O(n!)); safety checks are O(1) with occupancy arrays/sets. Auxiliary state is O(n) excluding board copies and output.</p>",
        "edge": "<p>n=1 has one solution; n=2 and n=3 have none. Ensure diagonal indexing is non-negative (offset row-col by n-1 if using arrays), and copy completed configurations rather than retaining a mutable path.</p>",
    },

    "bt24-right-view-of-binary-tree": {
        "intuition": "<p>The right view contains the last node at each depth when viewed from the right. BFS processes a level left-to-right, so the final node removed from each level is the rightmost.</p>",
        "steps": "<ol><li>Queue the root.</li><li>For each level, capture the queue size.</li><li>Process exactly that many nodes and record the final node in that level.</li><li>Enqueue children left then right.</li></ol>",
        "trace": "<p>For a root 1 with children 2 and 3, the right view starts [1,3]. At deeper levels, record the rightmost node present at each depth.</p>",
        "proof": "<p>BFS groups nodes by depth and preserves left-to-right order within each level. The last node at that level is exactly the node visible from the right.</p>",
        "complexity": "<p>O(n) time and O(w) queue space, where w is maximum width.</p>",
        "edge": "<p>Test empty tree, one node, left-only and right-only chains, and levels with missing right children. A left-only child may still be the visible right-view node.</p>",
    },
    "bt25-symmetric-tree": {
        "intuition": "<p>A tree is symmetric when its left subtree is the mirror image of its right subtree. Compare nodes in mirrored pairs: left-left against right-right and left-right against right-left.</p>",
        "steps": "<ol><li>Start with the root's left and right children.</li><li>If both are null, the pair matches; if only one is null or values differ, it does not.</li><li>Recursively compare left.left with right.right.</li><li>Compare left.right with right.left.</li><li>Both mirrored comparisons must succeed.</li></ol>",
        "trace": "<p>A root 5 with left child 1 and right child 1 is symmetric only if the descendants mirror in both shape and value, e.g. left's left child 2 mirrors right's right child 2.</p>",
        "proof": "<p>The recursive comparison checks equality of values and structure at every mirrored position. By induction, the two subtrees are mirror images iff both cross-child comparisons succeed.</p>",
        "complexity": "<p>O(n) time and O(h) recursion-stack space.</p>",
        "edge": "<p>Test empty, one node, asymmetric shape with equal values, mirrored values but wrong structure and duplicate values. Symmetry is structural as well as value-based.</p>",
    },
    "bt26-root-to-leaf-paths": {
        "intuition": "<p>Every root-to-leaf path is a traversal branch. Maintain a mutable path while doing DFS; when a leaf is reached, copy the path into the result.</p>",
        "steps": "<ol><li>Append the current node's value to the path.</li><li>If it is a leaf, store a copy of the current path.</li><li>Otherwise recurse into each non-null child.</li><li>Backtrack by removing the current node before returning.</li></ol>",
        "trace": "<p>For root 1 with leaf children 2 and 3, DFS records [1,2], backtracks, then records [1,3].</p>",
        "proof": "<p>DFS explores every root-to-leaf branch. The path contains exactly the ancestors from root to current node; copying it at a leaf records one complete path. Backtracking prevents one branch from contaminating another.</p>",
        "complexity": "<p>O(n + totalOutputSize) time and O(h) working path/recursion space, excluding stored results.</p>",
        "edge": "<p>Test empty tree, one node (one path), skewed tree, multiple leaves and repeated values. Store a copy, not the mutable path reference.</p>",
    },
    "bt27-root-given-node-path": {
        "intuition": "<p>Use DFS with backtracking. Append each visited node to the candidate path; if the target is not found in a subtree, remove that node before exploring another branch.</p>",
        "steps": "<ol><li>Append the current node.</li><li>If it is the target, return success.</li><li>Search the left subtree, then the right subtree.</li><li>If neither finds the target, remove the current node and return false.</li><li>Return the path on success or the source's “No Path” result when absent.</li></ol>",
        "trace": "<p>In a tree rooted at 1 with children 2 and 3, and 2 having child 5, searching for 5 records <code>1→2→5</code>.</p>",
        "proof": "<p>DFS explores every possible root-to-node route. A node remains in the path only when it is an ancestor of the target; failed branches are undone during backtracking. Thus a successful path contains exactly the root-to-target nodes.</p>",
        "complexity": "<p>O(n) time and O(h) recursion/path space.</p>",
        "edge": "<p>Test target at root, leaf, absent target, one node and skewed tree. The source assumes distinct node values; duplicate values require node identity or an explicit matching rule.</p>",
    },
    "bt29-maximum-width-of-tree": {
        "intuition": "<p>Maximum width is the largest number of nodes at any level. Level-order traversal counts the queue size at each level; this definition differs from positional width that includes gaps.</p>",
        "steps": "<ol><li>Queue the root.</li><li>At the start of each BFS level, record queue size.</li><li>Update maximum width with that size.</li><li>Process that level and enqueue non-null children.</li></ol>",
        "trace": "<p>For a complete tree with four nodes at its third level, the maximum node-count width is 4.</p>",
        "proof": "<p>The queue contains exactly the nodes of the current level before that level is processed. Its size is therefore the number of nodes at that depth; taking the maximum over all levels yields the required width.</p>",
        "complexity": "<p>O(n) time and O(w) queue space, where w is maximum level population.</p>",
        "edge": "<p>Test empty, one node, skewed tree (width 1), complete tree and uneven levels. Do not confuse node-count width with maximum positional span in a sparse tree.</p>",
    },
    "bt31-children-sum-property": {
        "intuition": "<p>For every non-leaf node, its value must equal the sum of its left and right child values, treating a missing child as zero. Leaves satisfy the property by definition.</p>",
        "steps": "<ol><li>Return true for null or leaf nodes.</li><li>Compute the sum of existing child values.</li><li>If it differs from the current node value, return false.</li><li>Recursively verify both child subtrees.</li></ol>",
        "trace": "<p>A node 35 with children 20 and 15 satisfies the property because 20+15=35. Its child nodes must independently satisfy the same rule.</p>",
        "proof": "<p>The property is local to each node. Checking the current equality and recursively checking both children verifies every internal node; leaves require no child-sum check.</p>",
        "complexity": "<p>O(n) time and O(h) recursion space.</p>",
        "edge": "<p>Test empty tree, one leaf, missing left/right child, a violation at root and a violation deep in a subtree. Use long if child sums can overflow int.</p>",
    },
    "bt33-nodes-at-distance-k": {
        "intuition": "<p>Distance in a tree can move downward to children or upward to the parent. Build parent references, then run BFS from the target, treating each node's parent and children as neighbours.</p>",
        "steps": "<ol><li>Traverse the tree to record each node's parent.</li><li>Start BFS from the target with distance zero and mark nodes visited.</li><li>For each level, expand left child, right child and parent if unvisited.</li><li>After k levels, collect nodes in the queue and sort if the contract requires sorted values.</li></ol>",
        "trace": "<p>For target 8 in a tree with children 4 and 12 and parent 20, nodes at distance 2 include 10, 14 and 22.</p>",
        "proof": "<p>Once parent links are added, the tree is an undirected graph. BFS visits nodes in non-decreasing shortest-path distance from the target, so the queue after k expansions contains exactly the nodes at distance k.</p>",
        "complexity": "<p>O(n) time and O(n) auxiliary space for parent mapping, visited state and BFS; sorting the answer adds O(a log a).</p>",
        "edge": "<p>Test k=0, k larger than tree height, target at root, target as leaf, absent target and nodes reachable through parent edges. Mark visited to avoid moving back and forth.</p>",
    },
    "bt34-burning-tree": {
        "intuition": "<p>Fire spreads one edge per time unit in all directions. The burn time is the maximum distance from the target node to any node. Parent references turn the tree into an undirected graph for BFS.</p>",
        "steps": "<ol><li>Find the target and record parent pointers for all nodes.</li><li>Start BFS at the target and mark it visited.</li><li>At each time step, expand left, right and parent neighbours.</li><li>Increment time when at least one new node is burned in that level.</li><li>Stop when no unvisited nodes remain.</li></ol>",
        "trace": "<p>Starting at target 8, nodes at distance 1 burn after one second, their unburned neighbours after the next, and so on. The answer is the greatest distance from 8 to any node.</p>",
        "proof": "<p>BFS explores the tree by increasing distance from the target. Since fire crosses exactly one edge per time unit, the level number is the burn time. The final non-empty level gives the time required to reach the farthest node.</p>",
        "complexity": "<p>O(n) time and O(n) auxiliary space for parent mapping and BFS.</p>",
        "edge": "<p>Test target at root, deepest leaf, one node, skewed tree and absent target. Count elapsed levels carefully: the target burns at time zero.</p>",
    },

    "g12-detect-cycle-in-undirected-graph-dfs": {
        "intuition": "<p>DFS explores one path deeply. In an undirected graph, an edge to a visited vertex other than the current node's parent indicates a cycle.</p>",
        "steps": "<ol><li>Start DFS from each unvisited vertex.</li><li>Mark the current vertex visited.</li><li>For each neighbour, recurse if unvisited.</li><li>If a neighbour is already visited and is not the parent, return true.</li><li>Return false if every component finishes without such an edge.</li></ol>",
        "trace": "<p>In a tree, every visited neighbour encountered from a node is its parent, so no cycle is reported. Adding an extra edge between two already connected non-parent vertices creates a cycle.</p>",
        "proof": "<p>The DFS tree contains exactly the edges used to discover vertices. An undirected edge to a visited non-parent vertex connects two vertices already joined by a tree path, closing a cycle.</p>",
        "complexity": "<p>O(V+E) time and O(V) visited/recursion space; recursion depth can reach O(V).</p>",
        "edge": "<p>Test disconnected graphs, isolated vertices, self-loops, parallel edges and a long chain. Parent handling and multigraph assumptions must match the input contract.</p>",
    },
    "g17-bipartite-graph-bfs": {
        "intuition": "<p>A graph is bipartite iff its vertices can be colored with two colors so every edge joins different colors. BFS assigns alternating colors along each edge.</p>",
        "steps": "<ol><li>Initialize all vertices uncolored.</li><li>For every uncolored component, assign its start vertex color 0 and run BFS.</li><li>For each edge u-v, assign v the opposite color if uncolored.</li><li>If v already has the same color as u, return false.</li><li>Return true after all components are processed.</li></ol>",
        "trace": "<p>A triangle cannot be two-colored: starting at 0, its two neighbours receive color 1, but the edge between them connects equal colors, so the graph is not bipartite.</p>",
        "proof": "<p>BFS colors vertices by parity of path length from the component root. If an edge joins equal colors, it forms an odd cycle and no valid two-coloring exists. If no conflict occurs, the produced coloring satisfies every edge.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space.</p>",
        "edge": "<p>Test disconnected components, isolated vertices, even cycles, odd cycles and empty graph. Do not process only the component containing vertex 0.</p>",
    },
    "g18-bipartite-graph-dfs": {
        "intuition": "<p>DFS can perform the same two-coloring as BFS. Every newly visited neighbour receives the opposite color; a same-color edge is a conflict.</p>",
        "steps": "<ol><li>Initialize every vertex as uncolored.</li><li>For each uncolored vertex, start DFS with one color.</li><li>For each neighbour, recursively assign the opposite color if uncolored.</li><li>If an already colored neighbour has the same color, return false.</li><li>Return true if all components are colored without conflict.</li></ol>",
        "trace": "<p>On a square cycle, colors alternate 0,1,0,1 and every edge connects different colors. On a triangle, the final edge connects two vertices both colored 1, revealing a conflict.</p>",
        "proof": "<p>DFS assigns colors so every discovery edge joins opposite colors. If all edges satisfy the condition, the coloring is a valid bipartition. A same-color edge proves no such coloring can exist under the assignments.</p>",
        "complexity": "<p>O(V+E) time and O(V) visited/color/recursion space. Deep graphs may overflow the Java call stack.</p>",
        "edge": "<p>Test disconnected components, isolated nodes, even and odd cycles and large-depth chains. For deep inputs, iterative BFS avoids recursion-depth risk.</p>",
    },
    "g20-eventual-safe-states-bfs": {
        "intuition": "<p>A node is safe when no path from it can enter a cycle. Reverse every edge and run Kahn's topological process from terminal nodes (outdegree zero); nodes removed by the process are safe.</p>",
        "steps": "<ol><li>Build the reverse adjacency list and record each original outdegree.</li><li>Queue all terminal nodes.</li><li>Remove a safe node and decrement the outdegree of its predecessors in the reverse graph.</li><li>When a predecessor's outdegree becomes zero, enqueue it.</li><li>Return all removed nodes in ascending order.</li></ol>",
        "trace": "<p>In <code>[[1,2],[2,3],[5],[0],[5],[],[]]</code>, terminal nodes 5 and 6 are safe; reverse propagation marks 2 and 4 safe as well. Nodes in or leading to the cycle remain.</p>",
        "proof": "<p>Terminal nodes are safe. A predecessor is safe once all of its outgoing neighbours are known safe. Kahn's algorithm removes exactly vertices whose outgoing paths can all terminate; vertices that remain are trapped in or can reach a directed cycle.</p>",
        "complexity": "<p>O(V+E) time and O(V+E) space for reverse adjacency, degrees and queue.</p>",
        "edge": "<p>Test all-terminal DAG, a pure cycle, a node leading into a cycle, disconnected components and self-loops. Sort the final list if the API requires ascending order.</p>",
    },
    "g20-eventual-safe-states-dfs": {
        "intuition": "<p>Use three states: unvisited, visiting (on the current DFS path), and safe/visited-complete. Reaching a visiting node reveals a cycle; a node is safe only when all outgoing neighbours are safe.</p>",
        "steps": "<ol><li>Start DFS from every unclassified vertex.</li><li>Mark a vertex visiting before exploring its neighbours.</li><li>If a neighbour is visiting, report unsafe due to a cycle.</li><li>If any neighbour is unsafe, the current vertex is unsafe.</li><li>After all neighbours are safe, mark the current vertex safe.</li></ol>",
        "trace": "<p>A terminal node has no outgoing edges and becomes safe immediately. A cycle such as 0→1→2→0 causes each active DFS call to be marked unsafe; any predecessor that reaches this cycle is also unsafe.</p>",
        "proof": "<p>A visiting-state edge identifies a directed cycle. A node can reach a terminal node along every possible path only if every outgoing neighbour is safe. Marking safe after all neighbours finish therefore matches the definition.</p>",
        "complexity": "<p>O(V+E) time and O(V) state/recursion space.</p>",
        "edge": "<p>Test terminal nodes, self-loops, DAG branches, multiple cycles, nodes leading into cycles and disconnected components. A single boolean visited flag is insufficient; distinguish active from completed nodes.</p>",
    },
    "g23-detect-cycle-in-directed-graph-bfs": {
        "intuition": "<p>Kahn's algorithm detects a directed cycle by counting how many vertices can be removed from the graph using indegree-zero vertices. A cycle has no first vertex with zero indegree within that cycle.</p>",
        "steps": "<ol><li>Compute indegrees.</li><li>Queue all zero-indegree vertices.</li><li>Remove vertices and decrement outgoing neighbours' indegrees.</li><li>Count removed vertices.</li><li>If the count is smaller than V, a directed cycle exists.</li></ol>",
        "trace": "<p>For a directed cycle 0→1→2→3→0, every vertex has indegree one, so the queue starts empty and no vertex is removed. The removed count is 0, less than V.</p>",
        "proof": "<p>Every DAG has at least one zero-indegree vertex and repeated removal yields a complete topological order. A directed cycle prevents all its vertices from being removed; therefore a removal count below V is equivalent to cycle existence.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space.</p>",
        "edge": "<p>Test a DAG, self-loop, cycle with an incoming tail, disconnected cyclic component and isolated vertices. Ensure all graph components are represented in the indegree calculation.</p>",
    },

    "g14-surrounded-regions-bfs": {
        "intuition": "<p>An O region is safe from capture if it is connected to the board boundary. Rather than search for enclosed regions, flood-fill all boundary-connected O cells and flip only the remaining O cells.</p>",
        "steps": "<ol><li>Scan the boundary and enqueue each O cell once.</li><li>Run BFS through four-directionally adjacent O cells, marking them as safe.</li><li>Scan the board: flip unmarked O to X and restore marked safe cells to O.</li></ol>",
        "trace": "<p>In the sample board, the bottom O touches the boundary and remains. The three interior O cells form a region disconnected from the boundary and are flipped to X.</p>",
        "proof": "<p>Every O connected to the boundary has a path to escape and must remain. Every O not reached by the boundary flood fill has no boundary path and is surrounded, so flipping exactly the unvisited O cells is correct.</p>",
        "complexity": "<p>O(mn) time and O(mn) worst-case queue/visited space.</p>",
        "edge": "<p>Test one-cell boards, all X, all O, boundary-connected winding paths, diagonal-only contact (not connected) and regions touching corners. Connectivity is four-directional.</p>",
    },
    "g15-number-of-enclaves-bfs": {
        "intuition": "<p>An enclave is land that cannot reach the boundary. Flood-fill all boundary-connected land, then count land cells that remain unvisited.</p>",
        "steps": "<ol><li>Queue all boundary cells containing 1 and mark them visited.</li><li>BFS through four-directionally adjacent land cells.</li><li>Count every grid cell that is 1 and was not reached.</li></ol>",
        "trace": "<p>For the sample grid, boundary-connected land is removed from consideration. Three interior land cells remain unreachable from the edge, so the answer is 3.</p>",
        "proof": "<p>A land cell can walk off the grid iff it is connected through land to a boundary cell. Multi-source BFS marks exactly this connected component set; the remaining land cells are precisely enclaves.</p>",
        "complexity": "<p>O(mn) time and O(mn) worst-case queue/visited space.</p>",
        "edge": "<p>Test no land, all land, one-row/one-column grids, isolated interior land and diagonal-only contact. Movement is four-directional.</p>",
    },
    "g16-distinct-islands-bfs": {
        "intuition": "<p>Two islands are considered the same when their shapes match under translation only. Record each island's cells relative to a fixed origin (for example, its first BFS cell); this removes absolute position while preserving orientation.</p>",
        "steps": "<ol><li>Scan for an unvisited land cell and use it as the island origin.</li><li>BFS/DFS through its four-directionally connected land cells.</li><li>For each cell, record relative coordinate (row-originRow, col-originCol).</li><li>Serialize the coordinate sequence consistently and insert it into a set of shapes.</li><li>Return the number of distinct shape encodings.</li></ol>",
        "trace": "<p>Two 2×2 islands at different grid positions both produce relative coordinates {(0,0),(0,1),(1,0),(1,1)}, so they count as one distinct shape.</p>",
        "proof": "<p>Subtracting the same origin from every cell removes translation and does not change relative geometry. Identical translated shapes produce the same normalized coordinate set; rotated or reflected shapes generally produce different encodings, as required.</p>",
        "complexity": "<p>O(mn) time to visit cells plus encoding work, and O(mn) space for visited cells and stored shape signatures.</p>",
        "edge": "<p>Test no islands, one island, translated copies, rotations/reflections (which should remain distinct), diagonal contact and different island sizes. Use an unambiguous coordinate serialization.</p>",
    },
    "g24-course-schedule1-bfs": {
        "intuition": "<p>Courses and prerequisites form a directed graph. A cycle means circular prerequisites, so courses cannot all be completed. Kahn's algorithm detects whether all vertices can be topologically removed.</p>",
        "steps": "<ol><li>Create an edge prerequisite→course for every pair.</li><li>Compute indegrees and queue all zero-indegree courses.</li><li>Remove courses and decrement indegrees of dependent courses.</li><li>Return true if the number removed equals numCourses; otherwise a cycle exists.</li></ol>",
        "trace": "<p>Prerequisite [1,0] creates edge 0→1, so course 0 is taken before 1 and both can be completed. Edges 0→1 and 1→0 form a cycle and make completion impossible.</p>",
        "proof": "<p>Zero-indegree courses have no unmet prerequisite and can be completed safely. Repeated removal is possible for all courses iff the dependency graph is acyclic.</p>",
        "complexity": "<p>O(V+E) time and O(V+E) space.</p>",
        "edge": "<p>Test no prerequisites, self-dependency, duplicate prerequisite edges if allowed, disconnected components and a cycle in a small subset of courses.</p>",
    },
    "g25-course-schedule2-bfs": {
        "intuition": "<p>Finding a valid course order is topological sorting. Kahn's algorithm repeatedly schedules courses whose prerequisites have already been completed.</p>",
        "steps": "<ol><li>Build prerequisite→course edges and indegrees.</li><li>Queue all zero-indegree courses.</li><li>Remove one, append it to the result, and decrement indegrees of its dependents.</li><li>Enqueue newly unlocked courses.</li><li>Return the order if it contains every course; otherwise return an empty array.</li></ol>",
        "trace": "<p>For prerequisites [1,0], [2,0], [3,1], [3,2], course 0 is first, courses 1 and 2 follow in either order, and 3 is last. One valid order is <code>[0,2,1,3]</code>.</p>",
        "proof": "<p>Every emitted vertex has indegree zero in the remaining graph, so no prerequisite edge points from a remaining course into it. Each emitted course is therefore valid at that position. Emitting all vertices proves a complete order; a leftover cycle makes this impossible.</p>",
        "complexity": "<p>O(V+E) time and O(V+E) space.</p>",
        "edge": "<p>Multiple valid orders are acceptable. Test no prerequisites, multiple independent courses, self-cycle, longer cycle and isolated courses. Return empty when not all vertices are emitted.</p>",
    },
    "g26-alien-dictionary": {
        "intuition": "<p>Adjacent words in a sorted alien dictionary reveal the first ordering constraint: at the first differing character, the earlier word's character must precede the later word's character. Topologically sort this character graph.</p>",
        "steps": "<ol><li>Compare each adjacent word pair and find the first differing position.</li><li>Add a directed edge from the character in the earlier word to the character in the later word.</li><li>Compute indegrees and topologically sort all K characters.</li><li>If a cycle exists, no valid order exists.</li><li>Also reject the invalid prefix case where a longer word precedes its own strict prefix.</li></ol>",
        "trace": "<p>For <code>[\"baa\",\"abcd\",\"abca\",\"cab\",\"cad\"]</code>, the first differing characters establish constraints such as b before a, d before a and a before c. A valid order is b,d,a,c.</p>",
        "proof": "<p>Lexicographic ordering is decided by the first differing character, so every adjacent word pair contributes a necessary precedence edge. A topological order satisfying all such edges respects every adjacent dictionary comparison; cycle detection identifies inconsistent constraints.</p>",
        "complexity": "<p>O(total characters + K + E) time and O(K+E) graph storage, where K is alphabet size and E inferred constraints.</p>",
        "edge": "<p>Test one word, identical words, prefix ordering, contradictory constraints, unused alphabet characters and multiple valid orders. Include all K characters even if no edge touches them.</p>",
    },
    "g27-shortest-path-in-un-directed-graph-unit-length": {
        "intuition": "<p>All edges have equal weight one, so BFS discovers vertices in non-decreasing number of edges from the source. The first discovery of a vertex is its shortest distance.</p>",
        "steps": "<ol><li>Initialize all distances to -1 and source distance to 0.</li><li>Queue the source.</li><li>For each dequeued vertex, visit unvisited neighbours, set distance to current distance plus one and enqueue them.</li><li>Leave unreachable vertices at -1.</li></ol>",
        "trace": "<p>For edges 0-1, 0-3, 1-2, source 0 has distances 0,1,2,1 for vertices 0,1,2,3 respectively.</p>",
        "proof": "<p>BFS explores all paths of length d before any path of length d+1. Therefore the first time a vertex is discovered, no shorter path can remain undiscovered; its assigned distance is minimal.</p>",
        "complexity": "<p>O(V+E) time and O(V) auxiliary space.</p>",
        "edge": "<p>Test source itself, disconnected vertices, multiple shortest paths, isolated vertices and cycles. The proof relies on unit/equal edge weights; use Dijkstra for arbitrary non-negative weights.</p>",
    },
    "g38-cheapest-flights-within-k-stops": {
        "intuition": "<p>The route is constrained by the number of stops, so ordinary Dijkstra with one best distance per city can discard a more expensive route that uses fewer edges. Track cost by edge count, or use Bellman–Ford-style bounded relaxations.</p>",
        "steps": "<ol><li>Initialize source cost to zero and all other costs to infinity.</li><li>Perform at most k+1 relaxation rounds, each using a snapshot of the previous round's distances.</li><li>For every flight u→v, update nextDist[v] with dist[u]+price.</li><li>After k+1 edges, return destination cost or -1 if unreachable.</li></ol>",
        "trace": "<p>For source 0 to destination 3 with at most one stop, route 0→1→3 costs 100+600=700. The cheaper route 0→1→2→3 uses two stops and is not allowed.</p>",
        "proof": "<p>After round i, dist[v] is the minimum cost to reach v using at most i edges. A route with at most k stops has at most k+1 edges, so k+1 rounds compute exactly the feasible search space.</p>",
        "complexity": "<p>O((k+1)E) time and O(V) distance space; snapshot arrays prevent a single round from accidentally using more than one additional edge.</p>",
        "edge": "<p>Test k=0 (direct flights only), source equals destination, unreachable destination, cheaper route with too many stops and multiple routes with different edge counts. Stops count intermediate cities, so at most k stops means at most k+1 flights.</p>",
    },

    "bt1-max-number-of-nodes-at-ith-level": {
        "intuition": "<p>A binary tree level can contain at most twice as many nodes as the previous level because every node has at most two children.</p>",
        "steps": "<ol><li>Clarify whether the root is level 0 or level 1.</li><li>For a maximum-width level i using root as level 1, compute <code>2^(i-1)</code>.</li><li>Use a wide integer type or detect overflow for large i.</li></ol>",
        "trace": "<p>With root at level 1, maximum node counts are 1, 2, 4, 8 for levels 1 through 4.</p>",
        "proof": "<p>Level 1 contains one root. If level i contains at most 2^(i-1) nodes, each has at most two children, so level i+1 contains at most 2^i nodes.</p>",
        "complexity": "<p>O(1) time and O(1) space for direct computation; arithmetic cost and overflow handling depend on the numeric type.</p>",
        "edge": "<p>Clarify level numbering. A sparse or skewed tree may contain fewer nodes; the formula is an upper bound for a binary tree, not its actual level size.</p>",
    },
    "bt2-binary-tree-representation": {
        "intuition": "<p>A binary tree node stores a value and references to its left and right children. A missing child is represented by null; links define structure rather than array positions.</p>",
        "steps": "<ol><li>Define a node with data, left and right references.</li><li>Create nodes for values.</li><li>Connect child references to represent the required shape.</li><li>Use null for absent children.</li></ol>",
        "trace": "<p>A root 1 with left child 2 and right child 3 is represented by node 1 whose left points to node 2 and right points to node 3.</p>",
        "proof": "<p>Each node reference explicitly identifies the root of a child subtree. Recursively following left and right references reaches every node in the tree exactly through its parent relationship.</p>",
        "complexity": "<p>Creating n nodes and assigning their links is O(n) time and O(n) storage.</p>",
        "edge": "<p>Test empty tree, single node, missing left/right child and ensure a node is not accidentally linked as a child of multiple parents in a tree structure.</p>",
    },
    "bt3-preorder-traversal-recursive": {
        "intuition": "<p>Preorder visits a node before its subtrees: Root, Left, Right. Recursion naturally follows this definition.</p>",
        "steps": "<ol><li>Return for a null node.</li><li>Visit the current node.</li><li>Recursively traverse the left subtree.</li><li>Recursively traverse the right subtree.</li></ol>",
        "trace": "<p>For root 1 with left subtree 2→(4,5) and right subtree 3, preorder is <code>1,2,4,5,3</code>.</p>",
        "proof": "<p>The algorithm emits the root first, then recursively emits every left-subtree node in preorder, followed by every right-subtree node. These disjoint sets cover all nodes once.</p>",
        "complexity": "<p>O(n) time and O(h) recursion-stack space.</p>",
        "edge": "<p>Test empty, one node, left-skewed, right-skewed and complete trees. Deep skewed trees can cause StackOverflowError.</p>",
    },
    "bt4-in-order-traversal-recursive": {
        "intuition": "<p>Inorder visits Left, Root, Right. For a binary search tree, this order produces values in non-decreasing order.</p>",
        "steps": "<ol><li>Return for null.</li><li>Recursively traverse the left subtree.</li><li>Visit the current node.</li><li>Recursively traverse the right subtree.</li></ol>",
        "trace": "<p>For root 2 with left child 1 and right child 3, inorder is <code>1,2,3</code>.</p>",
        "proof": "<p>The left subtree is fully emitted before the root, and the right subtree after it. Recursively applying the same rule visits every node exactly once in the required order.</p>",
        "complexity": "<p>O(n) time and O(h) recursion-stack space.</p>",
        "edge": "<p>Test empty, single node, skewed trees and duplicate values. Sorted output is guaranteed only when the input satisfies BST ordering.</p>",
    },
    "bt5-post-order-traversal-recursive": {
        "intuition": "<p>Postorder visits Left, Right, Root. It is useful when a parent operation depends on results computed for both child subtrees.</p>",
        "steps": "<ol><li>Return for null.</li><li>Recursively traverse the left subtree.</li><li>Recursively traverse the right subtree.</li><li>Visit the current node after both children.</li></ol>",
        "trace": "<p>For root 1 with left child 2 and right child 3, postorder is <code>2,3,1</code>.</p>",
        "proof": "<p>Each child subtree is completely emitted before the current root. Since left and right subtrees are disjoint and cover all descendants, every node appears exactly once after its descendants.</p>",
        "complexity": "<p>O(n) time and O(h) recursion-stack space.</p>",
        "edge": "<p>Test empty, leaf, skewed and complete trees. Postorder is commonly used for deletion and bottom-up subtree computations.</p>",
    },
    "bt6-level-order-traversal": {
        "intuition": "<p>Level order is breadth-first traversal. A queue ensures nodes are visited in increasing depth, with children added after their parents.</p>",
        "steps": "<ol><li>Return an empty result for a null root.</li><li>Enqueue the root.</li><li>While the queue is not empty, dequeue a node and record it.</li><li>Enqueue its non-null left and right children.</li></ol>",
        "trace": "<p>For root 1, children 2 and 3, and grandchildren 4 and 5 under 2, level order is <code>1,2,3,4,5</code>.</p>",
        "proof": "<p>FIFO order ensures all nodes at depth d are removed before nodes at depth d+1. Every node is enqueued once when its parent is processed, so all nodes are visited exactly once.</p>",
        "complexity": "<p>O(n) time and O(w) queue space, where w is maximum tree width.</p>",
        "edge": "<p>Test empty tree, one node, skewed tree and complete tree. Capture queue size at each level if the output must be grouped by depth.</p>",
    },
    "bt7-level-order-traversal2": {
        "intuition": "<p>When the result must be grouped by levels, capture the queue size before processing each level. This prevents children enqueued during the current pass from being mixed into that level.</p>",
        "steps": "<ol><li>Enqueue the root.</li><li>At each iteration, save the current queue size.</li><li>Process exactly that many nodes into one level list, enqueueing their children.</li><li>Append the level list to the result.</li></ol>",
        "trace": "<p>A root 1 with children 2 and 3 and grandchildren 4 and 5 produces <code>[[1],[2,3],[4,5]]</code>.</p>",
        "proof": "<p>The queue contains exactly one level at the start of the iteration. Processing the saved count removes all and only those nodes; newly enqueued children remain for the next iteration.</p>",
        "complexity": "<p>O(n) time and O(w) queue space, plus O(n) output storage.</p>",
        "edge": "<p>Test empty tree, one node, sparse levels and a right-only chain. Never use a changing queue size as the loop bound for one level.</p>",
    },
    "bt8-pre-order-traversal-iterative": {
        "intuition": "<p>Use a stack to simulate recursive preorder. Push the right child before the left child so the left child is popped and processed first.</p>",
        "steps": "<ol><li>Push the root.</li><li>Pop and visit the top node.</li><li>Push its right child if present.</li><li>Push its left child if present.</li><li>Repeat until the stack is empty.</li></ol>",
        "trace": "<p>For root 1 with children 2 and 3, pop 1, push 3 then 2, so 2 is visited before 3. The order is root-left-right.</p>",
        "proof": "<p>The stack is LIFO. Pushing right before left ensures the left subtree is fully processed before the right subtree, matching recursive preorder.</p>",
        "complexity": "<p>O(n) time and O(h) typical stack space, O(n) worst case depending on tree shape and push strategy.</p>",
        "edge": "<p>Test empty, one node, skewed trees and complete trees. Push only non-null children and preserve right-before-left push order.</p>",
    },
    "bt9-in-order-traversal-iterative": {
        "intuition": "<p>Simulate the recursive descent with a stack. Push the full left spine, visit the top node, then move into its right subtree.</p>",
        "steps": "<ol><li>Set current to root.</li><li>While current is non-null, push it and move left.</li><li>When current is null, pop and visit a node.</li><li>Set current to that node's right child and repeat until both current and stack are empty.</li></ol>",
        "trace": "<p>For root 2 with left 1 and right 3, push 2 then 1, visit 1, pop/visit 2, then visit 3. Output is <code>1,2,3</code>.</p>",
        "proof": "<p>The stack stores ancestors whose left subtrees are being completed. Popping visits the next node after its left subtree; moving right then processes its right subtree, exactly matching recursive inorder.</p>",
        "complexity": "<p>O(n) time and O(h) stack space.</p>",
        "edge": "<p>Test empty, one node, left/right chains and BST ordering. The loop must continue while either current is non-null or the stack is non-empty.</p>",
    },
    "bt10-post-order-traversal-iterative": {
        "intuition": "<p>Postorder is Left, Right, Root. An iterative solution can use two stacks: the first produces Root, Right, Left; reversing that order gives Left, Right, Root.</p>",
        "steps": "<ol><li>Push root to the first stack.</li><li>Pop a node, push it to the second stack.</li><li>Push its left child then right child onto the first stack.</li><li>When the first stack is empty, pop the second stack to obtain postorder.</li></ol>",
        "trace": "<p>For root 1 with children 2 and 3, the first stack produces 1,3,2 into the second stack; popping the second yields 2,3,1.</p>",
        "proof": "<p>The first stack's processing order is Root, Right, Left. The second stack reverses it, yielding Left, Right, Root, the required postorder sequence.</p>",
        "complexity": "<p>O(n) time and O(n) auxiliary space for the two stacks.</p>",
        "edge": "<p>Test empty, one node, skewed trees and complete trees. Confirm child push order because it determines the reversed sequence.</p>",
    },
    "bt11-post-order-traversal-iterative2": {
        "intuition": "<p>A single stack can implement postorder by tracking the last visited node. After returning from a left subtree, process the right subtree; after returning from the right subtree, visit the parent.</p>",
        "steps": "<ol><li>Descend left while pushing nodes.</li><li>Inspect the stack top without popping.</li><li>If its right child exists and was not just visited, move into that right subtree.</li><li>Otherwise pop and visit the node, recording it as last visited.</li><li>Repeat until the stack is empty.</li></ol>",
        "trace": "<p>For root 1 with children 2 and 3, the traversal visits 2, then 3, then 1. The last-visited pointer prevents re-entering a completed right subtree.</p>",
        "proof": "<p>A node is popped only after its left and right subtrees have been completed. The last-visited marker distinguishes returning from the left side from returning from the right side, preserving Left-Right-Root order.</p>",
        "complexity": "<p>O(n) time and O(h) stack space.</p>",
        "edge": "<p>Test nodes with only a left child, only a right child, both children and empty tree. Incorrect last-visited checks can cause repeated traversal or premature parent visits.</p>",
    },
    "bt12-pre-in-post-order-in-one-iteration": {
        "intuition": "<p>One stack can produce all three depth-first traversals by storing each node with a small state indicating which of its three visits is next.</p>",
        "steps": "<ol><li>Push root with state 1.</li><li>At state 1, record preorder and advance state; push the left child.</li><li>At state 2, record inorder and advance state; push the right child.</li><li>At state 3, record postorder and pop the node.</li><li>Continue until the stack is empty.</li></ol>",
        "trace": "<p>For root 1 with children 2 and 3, the same traversal yields preorder [1,2,3], inorder [2,1,3] and postorder [2,3,1].</p>",
        "proof": "<p>The state encodes the exact point at which recursive traversal would resume: before left, between left and right, and after right. Recording at those transitions reproduces the three recursive visitation orders.</p>",
        "complexity": "<p>O(n) time and O(h) stack space, plus O(n) output storage for each traversal list.</p>",
        "edge": "<p>Test empty, one node, skewed and complete trees. Ensure each state transition happens once and each node is appended to exactly one position in each traversal.</p>",
    },

    "bt30-maximum-width-of-binary-tree": {
        "intuition": "<p>This variant measures positional width, including null gaps between the leftmost and rightmost non-null nodes at a level. Assign complete-tree indices to nodes and subtract the first index at each level to keep numbers small.</p>",
        "steps": "<ol><li>Queue each node with a conceptual complete-tree index (root 0).</li><li>At each level, subtract the first index from all indices to normalize them.</li><li>For a node at normalized index i, assign left child 2i+1 and right child 2i+2.</li><li>The width of the level is last normalized index minus first normalized index plus one.</li><li>Track the maximum width.</li></ol>",
        "trace": "<p>For level positions containing nodes at conceptual indices 0 and 3 with two missing positions between, the width is 4, not 2. This is why a sparse level can be wider than its node count.</p>",
        "proof": "<p>Complete-tree indexing preserves the positional slots a node would occupy in a complete tree. The difference between the extreme non-null indices plus one counts every slot between them, including null gaps, exactly matching the definition.</p>",
        "complexity": "<p>O(n) time and O(w) queue space. Use long indices and normalize per level to reduce overflow risk.</p>",
        "edge": "<p>Test sparse trees with large gaps, skewed trees, complete trees and a level with only one node. This is not the same as node-count width in BT29.</p>",
    },
    "bt32-children-sum-property-ii": {
        "intuition": "<p>Convert the tree so every parent equals the sum of its children without decreasing any value. If the parent is larger, push its value down to a child; otherwise raise the parent to the child sum, then recurse.</p>",
        "steps": "<ol><li>At each node, compute the sum of existing child values.</li><li>If child sum is at least the node value, raise the node to that sum.</li><li>Otherwise raise one or both children so their sum equals the node value.</li><li>Recursively process left and right subtrees.</li><li>On the return path, recompute the parent as the sum of its children.</li></ol>",
        "trace": "<p>For a parent value 2 with children 35 and 10, the parent cannot be decremented; it is raised to 45. The property is then applied recursively to the child subtrees.</p>",
        "proof": "<p>Every update only increases a node. Before descending, the parent-child relation is made feasible by increasing the parent or children; recursive processing preserves child-subtree properties. Recomputing the parent after recursion establishes equality at the current node.</p>",
        "complexity": "<p>O(n) time and O(h) recursion space.</p>",
        "edge": "<p>Test leaf nodes, one missing child, parent greater than child sum, parent smaller than child sum and negative values if permitted. The exact distribution of increments may vary; structure must remain unchanged and no value may decrease.</p>",
    },
    "bt35-count-complete-tree-nodes": {
        "intuition": "<p>In a complete binary tree, if the leftmost and rightmost heights of a subtree are equal, that subtree is perfect and its node count is known directly. Otherwise recurse into its children.</p>",
        "steps": "<ol><li>Return 0 for null.</li><li>Compute the leftmost height and rightmost height.</li><li>If they are equal, return <code>2^height - 1</code>.</li><li>Otherwise return 1 plus counts of left and right subtrees.</li></ol>",
        "trace": "<p>A perfect tree of height 3 contains 7 nodes, so the method can count that subtree without visiting every node. A partially filled final level requires recursion into its children.</p>",
        "proof": "<p>A complete tree with equal extreme heights is perfect: all levels are full. The formula counts all nodes in a perfect tree. If heights differ, the root plus recursive counts partitions all nodes into disjoint left/right subtrees.</p>",
        "complexity": "<p>O(log² n) time for a complete tree: each level computes heights in O(log n), and only one or two subproblems remain along the height. O(log n) recursion space.</p>",
        "edge": "<p>Test empty, one node, perfect tree, last level partially filled on the left and a tree that is not complete. The optimized complexity depends on the complete-tree precondition.</p>",
    },
    "bt36-unique-binary-tree-requirements": {
        "intuition": "<p>For distinct node values, inorder combined with preorder or postorder uniquely determines a binary tree. Preorder and postorder alone do not generally determine whether a node with one child belongs on the left or right.</p>",
        "steps": "<ol><li>Check the two traversal types.</li><li>If one is inorder and the other is preorder or postorder, a unique tree can be reconstructed for distinct values.</li><li>If the pair is preorder and postorder, return false for the general case.</li></ol>",
        "trace": "<p>Preorder plus inorder uniquely identifies each root and partitions its left/right subtrees. Preorder plus postorder can describe both a single left child and a single right child with the same traversal sequences.</p>",
        "proof": "<p>Inorder locates the root's position and separates left and right subtree values. Preorder or postorder identifies the root and recursively supplies the subtree traversal order. Without inorder, a single-child orientation is ambiguous.</p>",
        "complexity": "<p>O(1) time for the traversal-type decision itself. Actual reconstruction costs O(n) with an index map under distinct values.</p>",
        "edge": "<p>Clarify whether node values are distinct. Duplicate values can make reconstruction ambiguous even when inorder is present. A full binary tree is a special case where preorder and postorder can be sufficient.</p>",
    },
    "bt37-binary-tree-from-in-order-pre-order-i": {
        "intuition": "<p>Preorder identifies the root first; inorder splits the remaining values into left and right subtrees. A value-to-index map avoids scanning inorder at every recursive call.</p>",
        "steps": "<ol><li>Build a map from each unique value to its inorder index.</li><li>Use a preorder pointer that advances from left to right.</li><li>Create the current root from the next preorder value.</li><li>Find its inorder split and recursively build the left range, then the right range.</li><li>Return null for an empty inorder range.</li></ol>",
        "trace": "<p>For preorder [3,9,20,15,7] and inorder [9,3,15,20,7], root is 3; inorder places 9 left and [15,20,7] right. The right subtree root is 20 with children 15 and 7.</p>",
        "proof": "<p>Preorder's first value in a subtree is its root. Inorder uniquely partitions that subtree into left and right values. Recursively applying the same rule reconstructs both subtrees, so the resulting tree matches both traversals.</p>",
        "complexity": "<p>O(n) time and O(n) map plus O(h) recursion space. Without the map, repeated inorder scans can degrade to O(n²).</p>",
        "edge": "<p>Test one node, skewed trees, negative values, mismatched traversal lengths and duplicate values. The source contract guarantees unique values and consistent traversals.</p>",
    },
    "bt38-binary-tree-from-in-order-pre-order-ii": {
        "intuition": "<p>With duplicate values, an inorder value may appear at multiple positions, so a simple value-to-index map is not enough. Reconstruction must select a root occurrence consistent with the current traversal ranges and the problem's duplicate policy.</p>",
        "steps": "<ol><li>Track the active inorder range and preorder cursor.</li><li>Choose the next preorder value as root.</li><li>Find a valid matching occurrence of that value within the current inorder range according to the source's policy.</li><li>Partition the range and recursively build left then right subtrees.</li><li>Verify the reconstructed postorder against the required output.</li></ol>",
        "trace": "<p>For preorder [0,1,3,4,2,5] and inorder [3,1,4,0,5,2], root 0 splits the inorder sequence into left [3,1,4] and right [5,2].</p>",
        "proof": "<p>The root occurrence divides the current inorder range into the values assigned to its left and right subtrees. Recursive construction follows the preorder root-left-right order. With duplicates, correctness depends on choosing an occurrence consistent with the input's intended tree; traversals may not uniquely identify one tree.</p>",
        "complexity": "<p>Depends on duplicate occurrence selection. A naive scan can be O(n²); an indexed occurrence structure can improve lookup but must still enforce valid range selection.</p>",
        "edge": "<p>Test repeated root values, duplicates in both subtrees, all-equal values and inconsistent traversals. Do not claim uniqueness for duplicate-valued traversals unless the source contract provides an additional disambiguation rule.</p>",
    },
    "bt40-morris-in-order-traversal": {
        "intuition": "<p>Morris inorder traversal temporarily threads each node's inorder predecessor back to the current node. These links replace the recursion stack and are removed when the traversal returns.</p>",
        "steps": "<ol><li>If current has no left child, visit it and move right.</li><li>Otherwise find the rightmost node in the left subtree (the inorder predecessor).</li><li>If its right link is null, create a temporary link to current and move left.</li><li>If its right link already points to current, remove the thread, visit current and move right.</li></ol>",
        "trace": "<p>For root 2 with left child 1 and right child 3, the predecessor 1 is temporarily threaded to 2. Visit 1, remove the thread and visit 2, then visit 3.</p>",
        "proof": "<p>The temporary predecessor link provides a return path after the left subtree is complete. Each thread is created once and removed once; nodes are visited when their left subtree has finished, which is inorder order.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space, excluding the output list. The tree structure is restored by removing every temporary thread.</p>",
        "edge": "<p>Test empty, one node, left/right chains and complete trees. Ensure every temporary link is removed, even when the traversal reaches a node with no right child. The source header comment says preorder, but the implementation method is explicitly Morris inorder.</p>",
    },
    "bt41-morris-pre-order-traversal": {
        "intuition": "<p>Morris preorder uses the same temporary predecessor threads as Morris inorder, but visits a node when its thread is first created—before descending into the left subtree.</p>",
        "steps": "<ol><li>If current has no left child, visit it and move right.</li><li>Otherwise find the rightmost node in the left subtree.</li><li>If its right link is null, visit current, create a temporary thread to current and move left.</li><li>If its right link already points to current, remove the thread and move right without visiting current again.</li></ol>",
        "trace": "<p>For root 1 with left child 2 and right child 3, visit 1 when creating the thread, then visit 2, remove the thread and finally visit 3. Output is <code>1,2,3</code>.</p>",
        "proof": "<p>Preorder visits the root before either subtree. Visiting on first encounter, before threading into the left subtree, preserves Root-Left-Right order. The second encounter only removes the thread and continues right.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space, excluding output. Every temporary thread is created and removed once.</p>",
        "edge": "<p>Test empty, one node, skewed trees and complete trees. Restore all predecessor links; a leftover thread corrupts the original tree. The traversal is preorder, unlike BT40.</p>",
    },
    "bt43-flatten-binary-tree-to-linked-list": {
        "intuition": "<p>Flattening must produce the preorder sequence using only right pointers. A stack can simulate preorder; an in-place alternative reconnects each left subtree between the current node and its original right subtree.</p>",
        "steps": "<ol><li>For each current node with a left child, find the rightmost node of its left subtree.</li><li>Attach the current node's original right subtree to that predecessor.</li><li>Move the left subtree to current.right and set current.left to null.</li><li>Advance along the right chain.</li></ol>",
        "trace": "<p>For root 1 with left subtree 2→(3,4) and right child 5→6, splice the original right subtree after the rightmost node 4. The flattened chain is <code>1→2→3→4→5→6</code>.</p>",
        "proof": "<p>Preorder visits the root, then the entire left subtree, then the original right subtree. Moving the left subtree to the right and attaching the original right subtree after its rightmost node preserves exactly that order; repeating at every node yields a right-only preorder chain.</p>",
        "complexity": "<p>The stack variant is O(n) time and O(n) space. The in-place predecessor-splicing variant uses O(1) extra space; worst-case time can be O(n²) if predecessor scans repeatedly traverse long right chains.</p>",
        "edge": "<p>Test empty, one node, left-only, right-only and balanced trees. Every left pointer must be null afterward, and the right chain must match preorder exactly.</p>",
    },

    "bst10-check-for-bst": {
        "intuition": "<p>A BST requires every node in the entire left subtree to be smaller and every node in the entire right subtree to be larger. Checking only immediate children is insufficient; propagate an allowed value range.</p>",
        "steps": "<ol><li>Start with the full range (-infinity,+infinity).</li><li>For a node, require its key to be strictly inside the range.</li><li>Recurse left with the upper bound set to the current key.</li><li>Recurse right with the lower bound set to the current key.</li><li>Return false on any violation.</li></ol>",
        "trace": "<p>A node 5 in the left subtree of root 10 violates the BST if it is greater than an ancestor's bound, even if it is smaller than its immediate parent.</p>",
        "proof": "<p>The recursive bounds encode every ancestor constraint. A node is accepted only if it satisfies all constraints inherited from the root-to-node path; both subtrees then receive the appropriate stricter bound.</p>",
        "complexity": "<p>O(n) time and O(h) recursion space.</p>",
        "edge": "<p>The source disallows duplicate keys, so use strict bounds. Test empty, one node, valid BST, a deep ancestor violation and duplicate values.</p>",
    },
    "bst12-predecessor-and-successor": {
        "intuition": "<p>The inorder predecessor is the greatest key smaller than the target; the successor is the smallest key greater than it. BST ordering lets us update candidates while descending from the root.</p>",
        "steps": "<ol><li>Search from the root.</li><li>If target is greater than current, current is a predecessor candidate; move right.</li><li>If target is smaller, current is a successor candidate; move left.</li><li>If target is found, the predecessor is the maximum of its left subtree and successor is the minimum of its right subtree, when those subtrees exist.</li></ol>",
        "trace": "<p>For the sample BST and key 8, the greatest smaller key is 4 and the smallest greater key is 9.</p>",
        "proof": "<p>When moving right from a smaller node, that node is a valid predecessor and any better predecessor must be farther right. When moving left from a larger node, that node is a valid successor and any better successor must be farther left. Subtree extrema complete the exact-match case.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space for iterative search, where h is tree height.</p>",
        "edge": "<p>Test target below minimum, above maximum, exact root match with missing subtrees, leaf match and absent target. Return null/-1 according to the API when no candidate exists.</p>",
    },
    "bst13-merge-two-bs-ts": {
        "intuition": "<p>Each BST's inorder traversal is sorted. Merge the two sorted traversals, or use two controlled inorder iterators to avoid storing both complete arrays.</p>",
        "steps": "<ol><li>Produce inorder sequences for both trees.</li><li>Use two pointers to merge them in ascending order.</li><li>Append remaining values from either sequence.</li><li>Return the merged sorted values.</li></ol>",
        "trace": "<p>For inorder sequences [2,3,4,5,6] and [1,2,3,6,7], merge to <code>[1,2,2,3,3,4,5,6,6,7]</code>.</p>",
        "proof": "<p>Inorder traversal produces sorted values for each BST. The standard merge procedure always selects the smallest unconsumed value from the two sequences, so the combined result is sorted and contains every node value.</p>",
        "complexity": "<p>O(n+m) time. Storing both traversals uses O(n+m) space; two stack-based iterators can reduce auxiliary storage to O(h1+h2), excluding output.</p>",
        "edge": "<p>Test empty tree, one empty tree, duplicate values across trees, skewed trees and identical trees. The result is a sorted multiset unless the problem explicitly requests unique values.</p>",
    },
    "bst15-pair-sum-in-bst": {
        "intuition": "<p>Two nodes sum to target when one value's complement exists in the tree. A hash set gives expected linear time; paired ascending/descending BST iterators provide an O(h) auxiliary-space two-pointer strategy.</p>",
        "steps": "<ol><li>For the hash-set method, traverse nodes and check whether target-current already exists.</li><li>If not, insert current and continue.</li><li>For the iterator method, produce smallest and largest remaining values.</li><li>Move the ascending iterator forward when the sum is too small and the descending iterator backward when too large; stop when they meet.</li></ol>",
        "trace": "<p>For a BST containing 1,2,3 and target 5, the values 2 and 3 form a valid pair.</p>",
        "proof": "<p>The hash-set method checks the exact complement before inserting the current node, preventing reuse of the same node. The iterator method follows the same safe pointer movement as two-sum on a sorted sequence.</p>",
        "complexity": "<p>Hash set: expected O(n) time and O(n) space. Two iterators: O(n) total traversal time and O(h) auxiliary stack space.</p>",
        "edge": "<p>Test no pair, target requiring the same value twice, duplicates if allowed and a single-node tree. Two distinct nodes must be used; the source BST may disallow duplicate keys.</p>",
    },
    "bst16-fixing-two-nodes-of-bst": {
        "intuition": "<p>Swapping two BST values disrupts the sorted inorder sequence. Inorder traversal should be increasing; the one or two inversions identify the misplaced nodes.</p>",
        "steps": "<ol><li>Perform inorder traversal while tracking the previous node.</li><li>When previous.value exceeds current.value, record the first misplaced node as previous on the first inversion.</li><li>Record the current node as the second misplaced node on every inversion.</li><li>After traversal, swap the two recorded values.</li></ol>",
        "trace": "<p>Inorder sequence <code>[1,5,3,4,2,6]</code> has inversions 5&gt;3 and 4&gt;2. The misplaced values are 5 and 2; swapping them restores sorted order.</p>",
        "proof": "<p>A BST's inorder sequence is sorted. Swapping two elements creates one inversion when they are adjacent in sorted order, or two when separated. The first inversion's previous node and the last inversion's current node are exactly the swapped values.</p>",
        "complexity": "<p>O(n) time and O(h) recursion/stack space. Morris traversal can reduce auxiliary traversal space to O(1) if threads are restored.</p>",
        "edge": "<p>Test swapped adjacent inorder values, non-adjacent values, root involvement and a tree already valid. The source guarantees exactly two nodes were swapped.</p>",
    },
    "bst17-largest-bst": {
        "intuition": "<p>For each subtree, return whether it is a BST, its size, minimum value and maximum value. A parent can combine two child results only when every left value is smaller than the root and every right value is larger.</p>",
        "steps": "<ol><li>For null, return a valid empty BST with size 0, min +infinity and max -infinity.</li><li>Recursively obtain summaries for left and right children.</li><li>If both are BSTs and left.max &lt; node.value &lt; right.min, the current subtree is a BST.</li><li>Return combined size and updated min/max.</li><li>Otherwise return the maximum BST size from either child.</li></ol>",
        "trace": "<p>If a node 10 has a valid left BST with maximum 8 and right BST with minimum 12, the whole subtree is a BST and its size is the sum of both sizes plus one.</p>",
        "proof": "<p>The summary contains exactly the information needed to test the BST ordering at the parent. By postorder induction, child summaries are correct; the parent either forms a valid BST or the largest valid BST must lie wholly in one child subtree.</p>",
        "complexity": "<p>O(n) time and O(h) recursion space; each node is processed once.</p>",
        "edge": "<p>Test empty, single node, fully valid BST, invalid root with valid child BSTs, duplicates and integer minimum/maximum keys. Use long sentinels to avoid colliding with valid int values.</p>",
    },
    "bst1-binary-search-trees": {
        "intuition": "<p>The inorder traversal of a BST with unique keys is strictly increasing. Therefore a proposed inorder sequence can represent a BST only if every adjacent pair is strictly increasing.</p>",
        "steps": "<ol><li>Scan the sequence from left to right.</li><li>If any value is less than or equal to its predecessor, return false.</li><li>Return true if the entire sequence is strictly increasing.</li></ol>",
        "trace": "<p><code>[8,14,45,64,100]</code> is strictly increasing and can be a BST inorder sequence. <code>[5,6,1,8,7]</code> contains a descent and cannot.</p>",
        "proof": "<p>Inorder traversal of a BST emits all left-subtree keys, then the root, then right-subtree keys; with unique keys, the result is strictly increasing. Conversely, any strictly increasing sequence can form a valid right-skewed BST.</p>",
        "complexity": "<p>O(n) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty/single sequence, duplicates (invalid under the unique-key contract), descending values and a sequence that is increasing except for one inversion.</p>",
    },
    "bst3-min-and-max-in-bst": {
        "intuition": "<p>The minimum key is the leftmost node and the maximum key is the rightmost node. BST ordering allows each to be found by following one pointer chain.</p>",
        "steps": "<ol><li>Start at the root.</li><li>Follow left pointers until no left child remains to find the minimum.</li><li>Follow right pointers until no right child remains to find the maximum.</li><li>Return both values.</li></ol>",
        "trace": "<p>For root 6 with left child 5 and right child 8, and 5's left child 2, the minimum is 2 and maximum is 8.</p>",
        "proof": "<p>Every left child is smaller than its parent, so no node outside the leftmost chain can be smaller than its terminal node. The symmetric argument identifies the maximum on the rightmost chain.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test empty tree, one node, left-skewed, right-skewed and balanced trees. Define the API's return value when root is null.</p>",
    },
    "bst4-ceil": {
        "intuition": "<p>The ceiling is the smallest key greater than or equal to x. During search, any node at least x is a candidate, but a smaller valid candidate may exist in its left subtree.</p>",
        "steps": "<ol><li>Initialize candidate as absent.</li><li>If current.value equals x, return it.</li><li>If current.value is greater than x, save it and move left.</li><li>If current.value is smaller than x, move right.</li><li>Return the best candidate or -1.</li></ol>",
        "trace": "<p>For a BST rooted at 5 with right child 7 and x=4, 5 is a candidate and searching left may find a closer value; the final candidate is the smallest key not below 4.</p>",
        "proof": "<p>When current is greater than x, current and its right subtree cannot contain a smaller ceiling, so only the left subtree can improve the candidate. When current is smaller, current and its left subtree are too small, so move right.</p>",
        "complexity": "<p>O(h) time and O(1) auxiliary space.</p>",
        "edge": "<p>Test exact match, x below minimum, x above maximum, empty tree and skewed trees. Return -1 when no ceiling exists.</p>",
    },
    "bst9-kth-largest-in-bst": {
        "intuition": "<p>Reverse inorder traversal (Right, Root, Left) visits BST values in descending order. The kth visited node is the kth largest.</p>",
        "steps": "<ol><li>Traverse the right subtree first.</li><li>Visit the current node and increment a counter.</li><li>If the counter reaches k, stop.</li><li>Otherwise traverse the left subtree.</li></ol>",
        "trace": "<p>For a BST with values 1,2,3, reverse inorder is 3,2,1. For k=2, the answer is 2.</p>",
        "proof": "<p>Inorder is ascending in a BST; reversing its traversal order yields descending keys. Counting visits therefore identifies the kth largest value.</p>",
        "complexity": "<p>O(h+k) time when traversal stops at the kth node (worst-case O(n)); O(h) stack/recursion space.</p>",
        "edge": "<p>Test k=1, k=n, k=0, k greater than node count and duplicate-key policy. The API should define behavior when k is invalid.</p>",
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
