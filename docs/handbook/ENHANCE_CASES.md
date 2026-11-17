# Enhancement brief: approach walkthrough and diagram explanations for case studies

You are EDITING existing, finished case-study pages in `C:\Users\kmangali\HLD\handbook\case-studies\`. Do not rewrite them. Add two things, keep everything else intact.

First read `..\AUTHORING.md` (CSS vocabulary, safe-JS rules, checker) and `..\CASE_AUTHORING.md`. Then read each assigned page fully before editing it.

## Addition 1: "How to approach this problem" section
Insert ONE new section before section 1 (right after the page intro/lead, before `<h2 id="problem">`):
`<h2 id="approach">How to approach this problem (read this first)</h2>`
Do not renumber the existing numbered sections. Write it for a learner who does not know how to START. About 700 to 1,100 words, plain words, specific to THIS problem, not generic. Cover, in this order:
1. **What the interviewer is really testing** in this problem (the 2 or 3 hard parts), in one short paragraph.
2. **The thinking order, step by step** as a numbered list (6 to 9 steps). Each step: what you do, what you SAY out loud (a short quoted sentence), and why that step comes at that point. Use this problem's real content: the first clarifying questions to ask, which number to estimate first and why, which API to draft first, which entity drives the data model, where the first bottleneck appears, what the first simple design is and how you decide to evolve it.
3. **The decision points**: 3 to 5 forks where a candidate must choose (for example SQL vs NoSQL, push vs pull, sync vs async), each with the question to ask yourself and how this problem's requirements decide it.
4. **A suggested time plan** for a 45 minute interview as a small table (minutes, what you cover, what to skip if short on time).
5. **Common mistakes** on this exact problem (4 to 6 bullets) and the one-line fix for each.
6. Add a pointer list "Sections of this page that match each step" linking to the existing section ids (`#requirements`, `#estimation`, ...). Only link ids that exist on the page.
Use one `callout` (Interview tip style from AUTHORING.md) for the single most important advice. Do not add a diagram here unless it clearly helps; if you add one, it counts toward the diagram rule below.

## Addition 2: explain every diagram
For EVERY `<figure>` with an SVG that currently has only a caption, add directly after the `</figure>` a block:
`<div class="callout"><b>Walkthrough.</b> ...</div>` (use the callout class variant that exists in AUTHORING.md; keep one consistent variant across the page).
Content, 80 to 200 words each, plain words:
- Say what each box, arrow and colour means in THIS diagram (name the actual boxes).
- Follow the main path in numbered order ("1. The client ... 2. ...") so a reader can trace the picture.
- Say WHY it is drawn this way: the design choice it shows and the alternative it avoids.
- Say what to point at when drawing it on a whiteboard, and what breaks if a box is removed.
Where the diagram is a sequence diagram, walk the messages in order. Where it is a chart or table-like figure, explain how to read it and the number that matters. Do not repeat the caption; add what the caption does not say. Skip hidden helper SVGs (display:none).

## Rules
- Do not remove or shorten existing content. Existing section ids must stay. Keep all current numbers consistent. If you must state a new number, derive it from the page's own estimation section.
- No new facts from memory that are risky: if unsure, say "assume" or explain the reasoning instead of quoting a figure.
- Safe-JS rule: add no script. Do not write the names of forbidden DOM APIs even in prose (see the checker in AUTHORING.md).
- No emoji, no em dashes in new text, plain words.
- After editing each page run from `C:\Users\kmangali\HLD\handbook`: `python -I tools/check.py case-studies/<file>` until it prints OK. Pages are checked for 4,000 words, 4 SVGs, 6 details, so you will pass; also confirm there are no broken ids by running `python -I C:\Users\kmangali\HLD\tools\check_site.py` at the end (it prints problems for the whole site; only fix problems in your pages, ignore others being edited by parallel agents).
- Edit only your assigned pages. Do not touch shared files (chapters.js, nav.js, css, tools).
- Do not run `build_site.py`, `build_search.py`, or copy into docs. The lead does that.
- Final reply: 4 lines at most: pages done, words added per page, anything you were unsure about (numbers assumed), any problem.
