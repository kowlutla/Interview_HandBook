# Authoring guide for HLD Handbook pages

You are writing ONE page of a system design (HLD) interview handbook. General interview audience (senior engineers), not company-specific. Read this whole file, then read the reference page `chapters/12-cdn.html` (and skim `chapters/13-caching-patterns.html`) before writing. Match their depth, tone, structure quality and visual vocabulary.

## Non-negotiable quality bar
- **Detailed prose, not terse bullets.** Explain every idea step by step: what it is, why it exists, how it works internally, what goes wrong, what the tradeoffs are. Define a term before using it. No "A -> B -> C" shorthand without a sentence-level explanation. Plain language first, then precision.
- **Complete for the topic.** If the page is about a system design component (load balancer, queue, search engine...), cover everything an interviewer could probe: purpose, internal architecture, request flow, scaling, configuration that matters, failure modes and mitigations, alternatives/products, when to use and not use, cost/operations, a worked example with real numbers, and interview Q&A.
- **Accurate.** Use well-known facts only. When unsure of an exact number or vendor behaviour, say "typically" or leave it out. Never invent product features. Double-check protocol and algorithm details.
- **Length:** chapters at least 6,000 words of visible text (aim 6,500-9,000), case studies at least 4,500, cheat sheets at least 900. The minimums enforced by `tools/check.py` are 5,500 / 4,000 / 800.
- **Diagrams:** at least 6 inline SVG diagrams per chapter (4 minimum enforced), each with a `<figcaption>` explaining how to read it. Use sequence diagrams, flows, architecture boxes, timelines, state tables, as the topic needs. Each diagram must be clear and uncluttered, with text that fits inside its shapes (leave generous box sizes; check that labels do not overlap or run off the viewBox).
- **Interactivity:** include 1 small widget only where it genuinely teaches (calculator, simulator, stepper). Optional.
- **Q&A:** at least 8 `<details><summary>question</summary><p>answer</p></details>` blocks with substantive answers (3+ sentences each), the way a strong candidate would answer.
- Chapters need not follow one rigid outline. Shape sections to the topic. But always include: a lead paragraph, numbered `<h2 id="...">` sections, a worked example with numbers where relevant, "Connects to", and a recap.

## Page skeleton (copy exactly; change only title, kicker, h1, lead, content, data-page, and script content)
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chapter NN: Title | HLD Handbook</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="NN-slug">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--fg)"/></marker>
  <marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--good)"/></marker>
  <marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--bad)"/></marker>
</defs></svg>
<div class="layout">
<nav class="toc" id="toc"></nav>
<main>
<div class="kicker">Chapter NN · Module name</div>
<h1>Title</h1>
<p class="lead">One or two sentence promise of what the reader will understand.</p>
<h2 id="short-id">1. First section</h2>
... content ...
<div class="recap" id="recap"><h2 style="border:none;margin-top:14px">N. Recap</h2><ul>...</ul></div>
<p class="connects"><b>Connects to:</b> builds on <a href="02-estimation.html">Chapter 2</a> ... Leads to ...</p>
</main>
</div>
<script src="../assets/chapters.js"></script>
<script src="../assets/nav.js"></script>
<!-- optional widget script after these -->
</body>
</html>
```
Rules: `data-page` equals the file name without `.html` and the id in `assets/chapters.js`. Do NOT write your own sidebar or prev/next links: `nav.js` generates the sidebar (from your `<h2>` elements), the previous/next pager and the page list. Every `<h2>` needs a unique `id`. Number h2 titles ("1. ...") like the reference pages. Case studies live in `case-studies/` (use `../assets/...` too); cheat sheets in `cheatsheets/`.

## Page vocabulary (CSS already exists in assets/style.css; do not add CSS files; avoid `<style>` blocks)
- Headings: `h2` sections, `h3` subsections (numbered like 3.1), `h4` minor.
- Callouts: `<div class="callout key"><b>Key idea</b> text</div>`; also `watch` (Watch out), `tip` (Interview tip), `good`.
- Tables: plain `<table>` with a `<tr><th>` header row; cells are padded and styled by CSS.
- Code and headers: `<pre>` and `<code>`.
- Diagrams: `<figure class="diagram"><svg viewBox="0 0 W H" role="img" aria-label="..."> ... </svg><figcaption>...</figcaption></figure>`. Two side by side: wrap two figures in `<div class="two">` (each viewBox about 400 wide).
- SVG classes: shapes `box` (blue, app/service), `cache` (amber), `db` (green), `ext` (purple, users/external), `hit` (green soft), `miss` (red soft); lines `arrow`, `arrow-g`, `arrow-r`, add `dash` for dashed; `life` for sequence lifelines; text `t-sm` (small muted), `t-b` (bold), `t-c` (centered; set x to the center). Arrow heads use the markers defined in the skeleton. Plain `<text>` is 13px. Use `rx="8"` on rounded rects. Give rectangles room (about 7-8 px per character at 13px; 6 px per character for t-sm).
- Widgets: `<div class="widget"><h4>Try it</h4>...</div>`, rows in `<div class="row">`, output in `<div class="log">`.
- Cross-links to other chapters: relative `<a href="NN-slug.html">Chapter N</a>` using ids from `assets/chapters.js` (from a chapter to a case study: `../case-studies/c01-url-shortener.html`; from a case study to a chapter: `../chapters/NN-slug.html`). Link only to ids that exist in `assets/chapters.js` (the target page may not be written yet; that is fine).

## Safe JavaScript only (a security hook blocks unsafe patterns and the checker fails them)
Never assign HTML strings to elements, never write to the document stream, never evaluate strings as code. Build DOM with `document.createElement` and `textContent`. Use these helpers in any widget script:
```js
function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
function setParts(node, parts) { node.textContent = ''; parts.forEach(function (p) { if (typeof p === 'string') node.appendChild(document.createTextNode(p)); else node.appendChild(el('b', null, p.b)); }); }
```
No external URLs, fonts, CDNs or images. The site must work offline from `file://`. In prose, do not write the literal names of the forbidden APIs (the checker greps for them).

## Numbering used in cross-references
Chapter numbers are the two-digit prefixes in `assets/chapters.js` (09-load-balancing is Chapter 9, 12-cdn is Chapter 12, 13-caching-patterns is Chapter 13). Refer to other chapters by that number and link them. Keep your scope to your manifest entry (the `d` field is a scope hint; extend it sensibly) and do not duplicate content another chapter owns; link instead, with a one-sentence recap.

## Procedure
1. Read `chapters/12-cdn.html` (structure, SVG style, depth) and this file.
2. Plan sections for your topic. Write the page to its path with the Write tool (one file; if too long for one call, write the first part, then append with edits, keeping the file valid).
3. Run `python -I tools/check.py <your file>` from `C:\Users\kmangali\HLD\handbook`. Fix every reported problem (length, diagrams, Q&A count, broken anchors/links, forbidden patterns). Re-run until it prints OK.
4. Re-read your page once for correctness, clarity, overlapping SVG text, and unexplained jargon.
5. Do NOT edit `assets/chapters.js`, `assets/*.css`, `assets/nav.js`, `index.html` or any other chapter. The maintainer flips the `done` flags.
6. Final reply, 3 lines max: file path, the checker's counts, and any facts you were unsure about.
