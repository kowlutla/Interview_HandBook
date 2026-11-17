/* Builds the sidebar, in-page contents, previous/next links, search, theme toggle and visited marks
   from window.HLD (assets/chapters.js). Uses DOM APIs only. */
(function () {
  'use strict';
  var H = window.HLD;
  if (!H) return;
  var me = document.currentScript;
  var base = me.src.replace(/assets\/nav\.js.*$/, '');
  var pageId = document.body.getAttribute('data-page') || '';

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function url(item, mod) { return base + (item.dir || mod.dir) + '/' + item.id + '.html'; }

  // ---- theme ----
  var root = document.documentElement;
  try { var saved = localStorage.getItem('hld-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  // ---- flatten + numbering ----
  var flat = [], n = 0, current = -1;
  H.modules.forEach(function (m) {
    m.items.forEach(function (it) {
      var isCase = (it.id.indexOf('c') === 0 && /^c\d\d-/.test(it.id));
      var isCheat = it.id.indexOf('cs-') === 0;
      var label;
      if (isCase) label = it.id.slice(1, 3);
      else if (isCheat) label = '★';
      else if (it.id.indexOf('ref-') === 0) label = 'A–Z';
      else label = it.id.slice(0, 2);
      var rec = { it: it, mod: m, label: label, href: url(it, m) };
      if (it.id === pageId) current = flat.length;
      flat.push(rec);
    });
  });
  var visited = {};
  try { visited = JSON.parse(localStorage.getItem('hld-visited') || '{}'); } catch (e) {}
  if (pageId && pageId !== 'index') {
    visited[pageId] = 1;
    try { localStorage.setItem('hld-visited', JSON.stringify(visited)); } catch (e) {}
  }

  // ---- headings on this page -> ids ----
  var main = document.querySelector('main');
  var heads = [];
  if (main) {
    var used = {};
    Array.prototype.forEach.call(main.querySelectorAll('h2'), function (h) {
      if (h.closest('.recap') && !h.id) h.id = 'recap';
      if (!h.id) {
        var s = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
        while (used[s]) s += '-x';
        h.id = s;
      }
      used[h.id] = 1;
      heads.push(h);
    });
  }

  if (pageId.indexOf('ref-') === 0) heads = [];  // glossary: letter bar and filter replace the in-page list

  // accessibility: skip link, labelled landmark, main target
  (function () {
    var mm = document.querySelector('main'); if (mm && !mm.id) mm.id = 'main';
    var sk = document.createElement('a'); sk.className = 'skip'; sk.href = '#main'; sk.textContent = 'Skip to content';
    document.body.insertBefore(sk, document.body.firstChild);
  })();

  // ---- sidebar ----
  var nav = document.getElementById('toc');
  if (!nav) {
    nav = el('nav', 'toc'); nav.id = 'toc';
    var layout = document.querySelector('.layout');
    if (layout) layout.insertBefore(nav, layout.firstChild);
  }
  nav.setAttribute('aria-label', 'Site contents');
  nav.textContent = '';
  var brand = el('a', 'brand', 'System Design Handbook');
  brand.href = base + 'index.html';
  nav.appendChild(brand);
  nav.appendChild(el('div', 'tagline', 'System design, explained from the ground up'));

  // ---- link to the matching Quick Notes sheet (kept in sync by mapping chapter numbers to sheets) ----
  var qbase = base + '../quicknotes/';
  var QMAP = [[1, 2, 'q01-framework-estimation'], [3, 7, 'q02-networking-api'], [8, 12, 'q03-stateless-tier'],
    [13, 15, 'q04-caching'], [16, 16, 'q03-stateless-tier'], [17, 23, 'q05-data-stores'], [24, 26, 'q06-replication-sharding'],
    [27, 33, 'q07-distributed-theory'], [34, 38, 'q08-async'], [39, 43, 'q09-resilience-ha'], [44, 53, 'q10-microservices'],
    [54, 56, 'q11-crosscutting'], [57, 59, 'q12-algorithms'], [60, 61, 'q13-delivery-playbook']];
  var qhref = qbase + 'index.html', qlabel = 'Open Quick Notes';
  if (/^c\d\d-/.test(pageId)) { qhref = qbase + 'cases/' + pageId + '.html'; qlabel = 'Quick sheet for this case'; }
  else if (pageId.indexOf('cs-') === 0) { qhref = qbase + 'notes/q13-delivery-playbook.html'; qlabel = 'Quick sheet for this page'; }
  else if (/^\d\d-/.test(pageId)) {
    var cn = parseInt(pageId.slice(0, 2), 10);
    QMAP.forEach(function (r) { if (cn >= r[0] && cn <= r[1]) { qhref = qbase + 'notes/' + r[2] + '.html'; qlabel = 'Quick sheet for this chapter'; } });
  }
  var qlinks = el('div', 'qlinks');
  if (qlabel !== 'Open Quick Notes') { var ql = el('a', 'ctx', '⚡ ' + qlabel); ql.href = qhref; qlinks.appendChild(ql); }
  [['🏠 Home', base + '../index.html'], ['🔍 Search the whole site', base + '../search.html']].forEach(function (r) {
    var a2 = el('a', null, r[0]); a2.href = r[1]; qlinks.appendChild(a2);
  });
  nav.appendChild(qlinks);

  var tools = el('div', 'tools');
  var search = el('input'); search.type = 'search'; search.placeholder = 'Filter chapters…'; search.setAttribute('aria-label', 'Filter chapters');
  tools.appendChild(search);
  nav.appendChild(tools);

  var openSet = null;
  try { openSet = JSON.parse(localStorage.getItem('hld-open') || 'null'); } catch (e) {}
  function saveOpen() {
    var o = {};
    groups.forEach(function (g) { if (g.d.open) o[g.m.id] = 1; });
    try { localStorage.setItem('hld-open', JSON.stringify(o)); } catch (e) {}
  }
  var groups = [];
  var bulk = el('div', 'bulk');
  var bExp = el('button', null, 'Expand all'); bExp.type = 'button';
  var bCol = el('button', null, 'Collapse all'); bCol.type = 'button';
  bulk.appendChild(bExp); bulk.appendChild(bCol);
  nav.appendChild(bulk);
  var list = el('div');
  H.modules.forEach(function (m, mi) {
    var d = el('details');
    var inMod = current >= 0 && flat[current].mod === m;
    if (inMod || (openSet && openSet[m.id])) d.open = true;
    d.appendChild(el('summary', null, m.title));
    var rows = [];
    flat.forEach(function (r, idx) {
      if (r.mod !== m) return;
      var done = !!r.it.done;
      var a = el(done ? 'a' : 'span', 'ch' + (done ? '' : ' soon') + (idx === current ? ' current' : '') + (visited[r.it.id] ? ' visited' : ''));
      if (done) a.href = r.href;
      a.appendChild(el('span', 'num', r.label));
      a.appendChild(el('span', null, r.it.t));
      if (!done) a.title = 'Coming soon';
      d.appendChild(a);
      rows.push({ node: a, text: (r.it.t + ' ' + (r.it.d || '')).toLowerCase() });
      if (idx === current && heads.length) {
        var op = el('div', 'onpage');
        var tg = el('button', 'twist', '▾'); tg.type = 'button'; tg.title = 'Collapse or expand sections of this chapter';
        tg.addEventListener('click', function (ev) { ev.preventDefault(); ev.stopPropagation(); var c = op.classList.toggle('closed'); tg.textContent = c ? '▸' : '▾'; });
        a.appendChild(tg);
        heads.forEach(function (h) {
          var l = el('a', null, h.textContent.replace(/^\s*\d+[a-z]?\.\s*/, ''));
          l.href = '#' + h.id; l.setAttribute('data-target', h.id);
          op.appendChild(l);
        });
        d.appendChild(op);
        rows.push({ node: op, text: '' , keep: true });
      }
    });
    groups.push({ d: d, m: m, rows: rows, wasOpen: d.open });
    d.addEventListener('toggle', function () { if (!search.value.trim()) { saveOpen(); } });
    list.appendChild(d);
  });
  nav.appendChild(list);
  bExp.addEventListener('click', function () { groups.forEach(function (g) { g.d.open = true; g.wasOpen = true; }); saveOpen(); });
  bCol.addEventListener('click', function () { groups.forEach(function (g) { g.d.open = false; g.wasOpen = false; }); saveOpen(); });
  var nomatch = el('div', 'nomatch', 'No chapter matches.'); nomatch.style.display = 'none';
  nav.appendChild(nomatch);

  search.addEventListener('input', function () {
    var q = search.value.trim().toLowerCase(), any = false;
    groups.forEach(function (g) {
      var shown = 0;
      g.rows.forEach(function (r) {
        if (r.keep) { r.node.style.display = q ? 'none' : ''; return; }
        var ok = !q || r.text.indexOf(q) >= 0;
        r.node.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      g.d.style.display = shown ? '' : 'none';
      g.d.open = q ? shown > 0 : g.wasOpen;
      if (shown) any = true;
    });
    nomatch.style.display = any ? 'none' : '';
  });

  // keep the current chapter in view in the sidebar
  var cur = nav.querySelector('.ch.current');
  if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'center' });

  // ---- mobile top bar ----
  var layoutEl = document.querySelector('.layout');
  if (layoutEl) {
    var bar = el('div', 'topbar');
    var btn = el('button', null, '☰ Contents'); btn.type = 'button'; btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () { var o = document.body.classList.toggle('nav-open'); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); });
    bar.appendChild(btn);
    bar.appendChild(el('span', null, current >= 0 ? flat[current].it.t : 'System Design Handbook'));
    layoutEl.parentNode.insertBefore(bar, layoutEl);
    main && main.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
  }

  // ---- previous / next (only pages that exist) ----
  if (main && current >= 0) {
    var prev = null, next = null, i;
    for (i = current - 1; i >= 0; i--) if (flat[i].it.done) { prev = flat[i]; break; }
    for (i = current + 1; i < flat.length; i++) if (flat[i].it.done) { next = flat[i]; break; }
    var pager = el('div', 'pager');
    if (prev) {
      var pa = el('a', 'prev'); pa.href = prev.href;
      pa.appendChild(el('span', 'lbl', '← Previous'));
      pa.appendChild(document.createTextNode(prev.label + '. ' + prev.it.t));
      pager.appendChild(pa);
    }
    if (next) {
      var na = el('a', 'next'); na.href = next.href;
      na.appendChild(el('span', 'lbl', 'Next →'));
      na.appendChild(document.createTextNode(next.label + '. ' + next.it.t));
      pager.appendChild(na);
    }
    main.appendChild(pager);
  }

  // ---- scroll spy ----
  if (heads.length) {
    var links = {};
    Array.prototype.forEach.call(nav.querySelectorAll('.onpage a'), function (a) { links[a.getAttribute('data-target')] = a; });
    var ticking = false;
    function spy() {
      ticking = false;
      var y = window.scrollY + 120, active = heads[0].id;
      heads.forEach(function (h) { if (h.offsetTop <= y) active = h.id; });
      Object.keys(links).forEach(function (k) { links[k].classList.toggle('active', k === active); });
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(spy); } });
    spy();
  }
})();
