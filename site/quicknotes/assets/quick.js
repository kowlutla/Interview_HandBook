/* Quick Notes sidebar behaviour, matching the Handbook sidebar: filter box, expand/collapse all,
   remembered open sections, and a mobile Contents button. DOM APIs only. */
(function () {
  var layout = document.querySelector('.layout'), nav = document.getElementById('toc');
  if (!layout || !nav) return;
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }

  // accessibility: skip link, labelled landmark, main target
  (function () {
    var mm = document.querySelector('main'); if (mm && !mm.id) mm.id = 'main';
    var sk = document.createElement('a'); sk.className = 'skip'; sk.href = '#main'; sk.textContent = 'Skip to content';
    document.body.insertBefore(sk, document.body.firstChild);
  })();
  nav.setAttribute('aria-label', 'Site contents');

  // mobile top bar
  var bar = el('div', 'topbar');
  var btn = el('button', null, '☰ Contents'); btn.type = 'button'; btn.setAttribute('aria-expanded', 'false');
  btn.addEventListener('click', function () { var o = document.body.classList.toggle('nav-open'); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); });
  var h = document.querySelector('h1');
  bar.appendChild(btn); bar.appendChild(el('span', null, h ? h.textContent : 'System Design Quick Notes'));
  layout.parentNode.insertBefore(bar, layout);
  var m = document.querySelector('main');
  if (m) m.addEventListener('click', function () { document.body.classList.remove('nav-open'); });

  // filter + bulk buttons, inserted after the link row
  var groups = Array.prototype.slice.call(nav.querySelectorAll(':scope > details'));
  var KEY = 'qn-open', saved = null;
  try { saved = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) {}
  groups.forEach(function (d, i) {
    var t = d.querySelector('summary').textContent;
    if (saved && saved[t]) d.open = true;
    d.addEventListener('toggle', function () { if (!search.value.trim()) save(); });
    d._wasOpen = d.open;
  });
  function save() {
    var o = {};
    groups.forEach(function (d) { if (d.open) o[d.querySelector('summary').textContent] = 1; });
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }
  var tools = el('div', 'tools');
  var search = el('input'); search.type = 'search'; search.placeholder = 'Filter sheets…'; search.setAttribute('aria-label', 'Filter sheets');
  tools.appendChild(search);
  var bulk = el('div', 'bulk');
  var bE = el('button', null, 'Expand all'); bE.type = 'button';
  var bC = el('button', null, 'Collapse all'); bC.type = 'button';
  bulk.appendChild(bE); bulk.appendChild(bC);
  var ql = nav.querySelector('.qlinks');
  if (ql) { ql.parentNode.insertBefore(tools, ql.nextSibling); tools.parentNode.insertBefore(bulk, tools.nextSibling); }
  bE.addEventListener('click', function () { groups.forEach(function (d) { d.open = true; d._wasOpen = true; }); save(); });
  bC.addEventListener('click', function () { groups.forEach(function (d) { d.open = false; d._wasOpen = false; }); save(); });
  var none = el('div', 'nomatch', 'No sheet matches.'); none.style.display = 'none'; nav.appendChild(none);
  search.addEventListener('input', function () {
    var q = search.value.trim().toLowerCase(), any = false;
    groups.forEach(function (d) {
      var shown = 0;
      Array.prototype.forEach.call(d.querySelectorAll('a.ch'), function (a) {
        var ok = !q || a.textContent.toLowerCase().indexOf(q) >= 0;
        a.style.display = ok ? '' : 'none'; if (ok) shown++;
      });
      Array.prototype.forEach.call(d.querySelectorAll('.onpage'), function (o) { o.style.display = q ? 'none' : ''; });
      d.style.display = shown ? '' : 'none';
      d.open = q ? shown > 0 : d._wasOpen;
      if (shown) any = true;
    });
    none.style.display = any ? 'none' : '';
  });
  var cur = nav.querySelector('.ch.current');
  if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'center' });
})();
