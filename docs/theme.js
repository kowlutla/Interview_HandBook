/* Site-wide light/dark theme. One saved choice (localStorage key hld-theme) is applied on every page,
   and one floating toggle is added to every page. DOM APIs only. */
(function () {
  'use strict';
  var KEY = 'hld-theme', root = document.documentElement;
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply() { var t = saved(); if (t) root.setAttribute('data-theme', t); else root.removeAttribute('data-theme'); }
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }
  apply();
  var btn;
  function label() { if (btn) { btn.textContent = isDark() ? '\u2600' : '\u263E'; btn.title = isDark() ? 'Switch to light theme' : 'Switch to dark theme'; btn.setAttribute('aria-label', btn.title); } }
  function build() {
    if (document.getElementById('theme-fab')) return;
    btn = document.createElement('button');
    btn.id = 'theme-fab'; btn.type = 'button';
    var s = btn.style;
    s.position = 'fixed'; s.right = '14px'; s.top = '10px'; s.zIndex = '60';
    s.width = '36px'; s.height = '36px'; s.borderRadius = '50%'; s.fontSize = '18px'; s.lineHeight = '1';
    s.cursor = 'pointer'; s.border = '1px solid rgba(128,128,128,.5)'; s.background = 'rgba(128,128,128,.18)';
    s.color = 'inherit'; s.boxShadow = '0 2px 8px rgba(0,0,0,.2)'; s.backdropFilter = 'blur(4px)';
    btn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      try { localStorage.setItem(KEY, next); } catch (e) {}
      root.setAttribute('data-theme', next); label();
    });
    document.body.appendChild(btn); label();
  }
  window.addEventListener('storage', function (e) { if (e.key === KEY) { apply(); label(); } });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
