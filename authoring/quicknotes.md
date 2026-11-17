# Authoring guide for System Design Quick Notes pages

The reader is a senior engineer revising 1 to 2 days before a system design interview. These pages are a LOOKUP and REVISION layer on top of the full Handbook at `C:/Users/kmangali/HLD/handbook` (read its chapters for facts; do not invent). Pages must be fast to scan, but complete enough that nothing an interviewer commonly asks is missing.

## The reference page
Read `notes/q04-caching.html` first (and `assets/quick.css`). Copy its structure and CSS classes. It shows: jump links, definitions table, `tl` one-liner boxes, `cols` + `card` grids, tables, `say` (say-this), `trap`, `nums` boxes, and a long Q&A of `<details><summary>question</summary><p>answer</p></details>` blocks grouped under `<h3>` headings.

## Writing style (very important)
- **Plain, everyday words.** Short sentences. Explain every technical term the first time in simple words ("a cache is a small fast store that keeps copies of data so we do not ask the slow database every time"). No jargon without a one-line meaning. Prefer "slow down" to "degrade throughput", "copy" to "replica" first, then introduce the proper term. A smart friend who has not studied this should follow it.
- Dense but not terse: tables, short bullets, one-line definitions, numbers, "say this" lines. No filler.
- Accurate: use only well-known facts. When unsure, write "about" or "typically", or leave it out.
- Q&A answers are DETAILED (4 to 8 sentences), real interview questions: concept questions, design scenarios, real-time production-incident questions ("hit rate suddenly drops, what do you do?"), and trade-off ("why X instead of Y?") questions. Answer like a strong candidate speaking aloud.

## Required content for a MODULE page (`notes/qNN-slug.html`)
1. Jump links under the title.
2. `0. Key definitions`: a table of 12 to 25 terms in simple words for everything in the module.
3. One numbered `<h2 id=...>` section per topic/chapter covered (see the "Chapters to cover" list in your task). Each section: a one-line `tl` summary, then the way it works in simple words, tables comparing options (when to use / when not), key numbers in a `nums` box, common mistakes in a `trap` box, and what to say in an interview in a `say` box. Each section has a small tag linking to the owning handbook chapter: `<span class="tag"><a href="../../handbook/chapters/NN-slug.html">Ch NN</a></span>`.
4. At least **4 inline SVG diagrams** (aim 6 or more) placed where they make the idea easy: flows, request paths, before/after, comparison pictures, timelines, small architectures. Use the vocabulary below. Keep text inside the shapes with generous box sizes.
5. A `say-aloud script` section (30 to 60 seconds of what to say for this topic area).
6. `Interview Q&A`: **25 to 35** `details` blocks grouped under `<h3>` headings (A concepts, B design scenarios, C failures and real-time production scenarios, D trade-offs and why-questions). Cover every question commonly asked on these topics, with detailed plain-language answers.
7. `Dig deeper`: links to the handbook chapters and relevant case study pages.
- Length: at least 4,500 words (aim 5,000 to 7,000). At least 20 details blocks.

## Required content for a CASE SHEET (`cases/cNN-slug.html`)
One-page "cheat sheet" for the case study in the Handbook (read `C:/Users/kmangali/HLD/handbook\case-studies\cNN-slug.html` first and condense it faithfully, same numbers). Use `../assets/style.css`, `../assets/quick.css`, and a back link `<a href="../index.html">`.
Sections (all short and scannable): 1 Problem in 3 lines and the clarifying questions to ask; 2 Requirements (functional, non-functional, out of scope); 3 Estimation with the numbers worked out; 4 API (a few lines); 5 Data model and store choices with a reason each; 6 Architecture diagram (SVG) and the main request flow(s) as numbered steps or a small sequence SVG; 7 The 2 to 3 deep dives, each as a comparison table plus the choice and why; 8 Scaling and bottlenecks; 9 Failure modes table (what fails, what happens, fix); 10 Things to say to impress (senior/lead level); 11 **Q&A: 8 to 14 `details` blocks** of follow-up questions an interviewer asks, with detailed plain answers; 12 Links to the handbook case study and chapters.
- At least 1,800 words (aim 2,200 to 3,000), at least 2 SVG diagrams (aim 3 to 4), at least 6 details blocks.

## Page skeleton
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quick Notes: TITLE | System Design Quick Notes</title>
<link rel="stylesheet" href="../assets/style.css">
<link rel="stylesheet" href="../assets/quick.css">
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--fg)"/></marker>
  <marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--good)"/></marker>
  <marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--bad)"/></marker>
</defs></svg>
<div class="qn">
<p class="back"><a href="../index.html">← Quick Notes index</a></p>
<h1>Title</h1>
<p class="sub">One line about what this sheet covers.</p>
...content...
</div>
</body>
</html>
```
No script tags at all (quick notes use no JavaScript). No external URLs, fonts, images. Do not write the names of unsafe DOM APIs in prose (the checker greps).

## Diagrams
`<figure class="diagram"><svg viewBox="0 0 W H" role="img" aria-label="..."> ... </svg><figcaption>how to read it, in one or two plain sentences</figcaption></figure>`. Two side by side: `<div class="two">` with two figures (each viewBox about 400 wide).
Shape classes: `box` (blue, services), `cache` (amber), `db` (green), `ext` (purple, users/outside), `hit` (soft green), `miss` (soft red). Lines: `arrow`, `arrow-g`, `arrow-r`, add `dash` for dashed; `life` for sequence lifelines. Text: `t-sm` (small, muted), `t-b` (bold), `t-c` (centered; set x to the center). Arrow heads: `marker-end="url(#ah)"` (also `#ahg`, `#ahr`). Use `rx="8"` on rounded rects. Plain `<text>` is 13px: allow about 8 px per character; 6 px per character for t-sm. Make boxes wide enough, never let labels overflow or overlap, and keep a clear left-to-right or top-to-bottom flow.

## Links
- To the handbook chapter: `../../handbook/chapters/NN-slug.html`; to a handbook case study: `../../handbook/case-studies/cNN-slug.html`; to a cheat sheet: `../../handbook/cheatsheets/cs-*.html`. Use real file names (list `C:/Users/kmangali/HLD/handbook\chapters`).
- To another quick note: `qNN-slug.html` (same folder) or `../cases/cNN-slug.html`.

## Procedure
1. Read this file, `notes/q04-caching.html`, and the handbook chapters/case study you are condensing (read them; condense faithfully, do not contradict them).
2. Write the page with the Write tool to the exact path given in your task (if too long, write the first part and then append with Edit while keeping the file valid HTML).
3. From `C:/Users/kmangali/HLD/quicknotes` run `python -I tools/check_quick.py <your file>` and fix every reported problem until it prints OK. (Links to quick-note pages that another agent has not written yet may be reported as missing; avoid linking to other quick notes except `../index.html` and, for the module pages, the case sheet file names listed in your task.)
4. Re-read once for plain wording, accuracy, and SVG text fitting inside shapes.
5. Do NOT edit any other file (including the handbook, `index.html`, CSS, or other pages).
6. Final reply: 3 lines maximum: file path, checker counts, facts you were unsure of.
