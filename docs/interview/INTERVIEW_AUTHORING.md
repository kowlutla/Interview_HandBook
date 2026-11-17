# Authoring guide for Interview Book topic pages

One page per topic: `C:/Users/kmangali/HLD/interview/topics/<slug>.html`. The reader is a senior engineer (about 8+ years) preparing for interviews. The page must contain the questions that are REALLY asked, with answers a strong candidate would say aloud, in plain words.

Do NOT copy the old Q&A in `C:/Users/kmangali/Personal Repos/Interview-Preparation/<Topic>`. That repo is only a topic checklist: read it to see what is covered, then write fresh, better, deeper content from your own knowledge. Where the repo is wrong or shallow, correct it.

## Audience and depth (the user asked for this explicitly)
The reader is a SENIOR SOFTWARE ENGINEER with 5 to 10 years of experience, interviewing for developer roles. Write at the depth such a developer is expected to have: what they use daily, how it works well enough to debug and design with it, and the trade-offs they must be able to explain. Do NOT go to DevOps/SRE/platform-specialist depth (for example for CI/CD: pipelines, deployment strategies, rollbacks, secrets, common failures yes; Jenkins plugin internals, cluster operations, capacity planning, kernel-level tuning no). If a topic is a specialist area, cover what an application developer must know and mention in one line where the specialist depth begins. Remove any question that only a dedicated ops or infrastructure engineer would be asked.

## Quality bar (the user asked for this explicitly)
- Answers must be DETAILED yet SIMPLE: written the way a friendly senior colleague explains it out loud. Natural, conversational English. Short sentences, everyday words, one idea at a time. Explain the "why" before the "how". Use a small concrete example or analogy in most answers.
- Never leave a term unexplained. If you must use jargon, define it in a few plain words right there.
- A model answer is 6 to 12 sentences for normal questions (more with code or a diagram). Not a bullet dump of keywords: bullets only for lists of options or steps.
- Questions are the ones really asked in interviews for senior engineers (8+ years): mix "what and why", "how does it work inside", "compare X and Y", "what happens when...", debugging, design, and production incidents.
- Accuracy over volume. For anything version-specific say which version. If unsure, say "typically" or leave it out. Review your own facts at the end.
- Use `interview/topics/git.html` as the exemplar for depth, tone, structure, markup and diagram quality. Read at least its first 400 lines before writing.

## Reference pages (read first)
- `quicknotes/notes/q04-caching.html` for tone, `tl`/`say`/`trap`/`nums` boxes, tables, diagram style.
- `quicknotes/assets/quick.css`, `interview/assets/interview.css` for classes.

## Writing style
- Plain everyday words, short sentences, explain each term the first time. No filler.
- Answers are spoken-style, 5 to 10 sentences for normal questions, longer with code or a diagram for deep ones.
- Accurate. Where behaviour depends on version (for example default branch name, new commands), say which version. If unsure, say "about" or leave it out.
- Prefer questions that are asked in real interviews: concept, "why/how does it work internally", trade-off, "what happens when you run X", debugging, and real-life production scenarios ("a teammate force-pushed over main, what do you do?"). No hard limit on the number of questions; cover the topic completely.

## Page structure
1. Title, one-line `sub`, jump links to the sections.
2. `How to use this page` short box and a legend of the three levels.
3. `Mental model` section: the 5 to 8 ideas everything else hangs on, with a diagram.
4. Question sections, each an `<h2 id="...">` grouped by sub-topic (for example for Git: object model, branching and merging, rebase and history, remotes and workflows, undoing things, finding bugs and recovery, collaboration and release practice, internals and performance).
5. `Real-life scenarios` section: at least 8 incident/situation questions, each `details class="iq scn"`, answered as: situation, what you check first, commands/steps, how you prevent it next time.
6. `Rapid-fire round` table (30+ one-line question and answer pairs).
7. `If you only have an hour` list: the 12 questions to read first (link with `<a href="#qid">`).
8. `Cheat sheet`: command/decision tables.

## Question markup (exact)
```html
<details class="iq" id="q-short-slug">
<summary>What is the difference between merge and rebase? <span class="lvl b">Basic</span></summary>
<div class="ans">
<p class="why"><b>What the interviewer is testing:</b> one sentence.</p>
<p>Model answer paragraph(s)...</p>
<pre><code>git rebase main</code></pre>
<figure class="diagram">...</figure>   <!-- when a picture helps -->
<div class="fu"><b>Likely follow-ups</b><ul><li>question? short answer.</li></ul></div>
<div class="mistake"><b>Common mistakes:</b> ...</div>
</div>
</details>
```
The level badge goes AFTER the question text. The question number (Q1, Q2...) is added automatically by CSS, never write it by hand. Level span: `lvl b` + text Basic, `lvl i` + Intermediate, `lvl s` + Senior. Scenario questions use `class="iq scn"`. Every question needs a unique id. Not every question needs follow-ups or mistakes boxes, but most should have follow-ups, and every non-trivial one a why line.

## Diagrams
At least 10 inline SVG diagrams for a big topic, placed where they teach: object model, branch/merge/rebase pictures (commit dots and arrows), reset modes, remote flows, workflows, recovery timelines. Same vocabulary as the Quick Notes: `<figure class="diagram"><svg viewBox="0 0 W H" role="img" aria-label="...">...</svg><figcaption>how to read it</figcaption></figure>`; classes `box cache db ext hit miss`, lines `arrow arrow-g arrow-r dash`, text `t-sm t-b t-c`. Marker defs `ah`, `ahg`, `ahr` go in the hidden svg at the top of the body (copy from q04). Roomy boxes, no overlapping labels (about 8 px per character at 13px).

## Skeleton
```html
<!DOCTYPE html>
<html lang="en">
<head>
<script src="../../theme.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interview Book: TOPIC | Interview Book</title>
<link rel="stylesheet" href="../../handbook/assets/style.css">
<link rel="stylesheet" href="../../quicknotes/assets/quick.css">
<link rel="stylesheet" href="../assets/interview.css">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs> ...markers... </defs></svg>
<div class="qn">
<h1>TOPIC interview questions</h1>
<p class="sub">...</p>
...
</div>
</body>
</html>
```
The sidebar and pager are generated by `tools/build_site.py` (between qnav/qfoot markers); do not write them. The `<script src="../../theme.js">` line is the only script allowed. No external URLs/fonts/images. Never write the names of unsafe DOM APIs in text (the checker greps). Every `<h2>` must have an id.

## Checking
From `C:/Users/kmangali/HLD/interview`: `python -I tools/check_interview.py topics/<slug>.html`. Minimums: 6,000 words, 6 SVG, 40 questions, a badge per question, 6 scenario questions. Aim far above (Git: 80+ questions, 12+ diagrams, 15+ scenarios). Fix every PROBLEMS line. Do not run build_site.py or edit files other than your topic page.
