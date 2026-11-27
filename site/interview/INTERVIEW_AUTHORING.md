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

## ANSWER FORMAT v2 (the user rejected v1; this section overrides anything above that conflicts)
The user's feedback on v1: the "What the interviewer is testing" lines and "Likely follow-ups" boxes are not wanted; answers were not straight, did not sound like answering an interviewer, and the explanation was not up to the mark. They want answers that are detailed, easy to read AND easy to remember, with real technical depth and diagrams, but NOT tutorial length.

Every question is written like this:
1. **Direct answer first** (`<p class="ia">`): 2 to 4 spoken sentences that answer exactly what was asked, in first person where natural ("I would...", "It works like this..."). A candidate could say this out loud and stop, and it would already be a good answer. No preamble, no "it depends" opening, no restating the question. If the honest answer is "it depends", say the decision rule in the same breath ("use A when X, B when Y").
2. **Go deeper** (normal `<p>`, `<ul>`, small table or `<pre><code>`): the technical depth a senior would add if the interviewer keeps probing: the mechanism, the numbers/defaults, the trade-off, the failure mode, a tiny concrete example. 3 to 8 sentences or a short bullet list. Plain words, one idea per sentence, define jargon in a few words. Explain WHY before HOW.
3. **Diagram** (`<figure class="diagram">`) wherever a picture beats words: flows, lifecycles, comparisons, timelines, architectures, memory layouts. Keep it clear and uncluttered. Not every question needs one, but a page should have plenty (15+ for big topics).
4. **Remember line** (`<p class="rem"><b>Remember:</b> ...</p>`): ONE short line, a rule of thumb, mnemonic or contrast ("Merge keeps history, rebase rewrites it: never rebase what others have"). Every question has one.
5. Optional `<div class="mistake"><b>Watch out:</b> ...</div>` only when there is a real, common trap. Skip it otherwise.

Do NOT write: `class="why"` lines, `class="fu"` follow-up boxes, or "What the interviewer is testing". If a follow-up is worth knowing, make it its OWN question right after the parent (phrased as the interviewer would actually ask next, e.g. "And what happens to the old commits after a rebase?"), with its own id, badge, direct answer and remember line. Merge near-duplicate questions. Keep the question count high but each answer tight: typical answer 90 to 220 words including the deeper part (diagram questions can be more). Do not pad.

Scenario questions (`iq scn`) keep the shape Situation / Check first / Fix / Prevent, but still start with a `<p class="ia">` that states the one-sentence diagnosis and fix, and end with a `rem` line.

Keep ALL the existing sections: how to use, mental model, question sections, scenarios, rapid-fire table, one-hour list (links must resolve), cheat sheet, and the existing diagrams (reuse them in the right answers; fix any that are unclear). The review is also a CORRECTNESS pass: fix wrong or shaky facts you find, hedge version-specific ones, and list what you are unsure of in your final report.

## Question markup v2 (exact)
```html
<details class="iq" id="q-short-slug">
<summary>What is the difference between merge and rebase? <span class="lvl b">Basic</span></summary>
<div class="ans">
<p class="ia">Merge joins two branches with a merge commit and keeps history exactly as it happened. Rebase re-applies my commits on top of the new base, so history becomes a straight line but those commits get new hashes. I rebase my own private branches and merge shared ones.</p>
<p>Deeper: ...mechanism, numbers, trade-off...</p>
<figure class="diagram">...</figure>
<p class="rem"><b>Remember:</b> merge keeps history, rebase rewrites it. Never rebase what others already have.</p>
</div>
</details>
```
The level badge goes AFTER the question text; the Q-number comes from CSS, never typed. Level span: `lvl b` Basic, `lvl i` Intermediate, `lvl s` Senior. Scenario questions use `class="iq scn"`. Unique ids. The checker now requires one `ia` and (about) one `rem` per question and rejects `why`/`fu`. Minimums now: 2,500 words, 5 SVG, 25 questions, 4 scenarios.

When you rewrite a page, you may write it in parts (for example one file per section in the job temp dir) and join them, but the final file must be one complete HTML page with the skeleton below. Do NOT write the qnav/qfoot sidebar and pager markers (the build adds them; leave them out). Do not run build_site.py.

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

## CURATION RULE (the user asked for this explicitly, applies on top of v2)
Keep only the questions that are REALLY asked in interviews for a senior developer (5-10 yrs), and the follow-ups that interviewers genuinely ask next. Having a huge list does not help revision. Remove trivia, rarely-asked edge cases, tool-version minutiae and anything an ops/platform specialist would be asked instead of a developer. Do not cut drastically: keep as many as the topic truly needs, but not every question has to survive. Every surviving answer must be in depth (mechanism + trade-off + example) yet in natural, simple language. Each topic has a target question count given in your brief: land within about plus or minus 15 percent. Prefer cutting from the rapid-fire/cheat-sheet padding too; keep those compact. Keep ids stable for surviving questions.


## DSA topic pages

DSA pages are problem-centred, not conceptual Q&A pages. Preserve the Interview Book's typography, navigation, responsive layout and plain-English teaching style, but use a structure suited to solving coding problems.

For each problem, include:
- Clear problem statement and representative examples.
- The underlying pattern and intuition before showing code.
- Brute force when it teaches an important trade-off; do not add it mechanically.
- An optimized, compilable Java solution with required imports and explicit input assumptions.
- A meaningful dry run that traces the important state.
- Time and auxiliary-space complexity, explaining where each term comes from.
- Correctness reasoning or the invariant that makes the approach work.
- Common mistakes and edge cases worth testing.
- A short remember line with the central insight.

Use the Java source repository as the source of problem selection and initial implementations, not as an unquestionable source of truth. Review every implementation for correctness, boundary conditions, Java character/overflow behaviour, complexity and input constraints. Correct bugs and explain material deviations from the original. Do not copy misleading comments or unsupported complexity claims.

Group problems by learning topic and pattern. Avoid duplicate problem entries; keep genuinely different approaches only when the comparison is useful. Keep explanations detailed enough to teach the reasoning, but concise enough for interview revision. Use Java as the canonical language. DSA pages may use their own problem markup and validator; do not force algorithm problems into the conceptual `details.iq` Q&A format.
