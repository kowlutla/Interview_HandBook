# Depth pass: make every answer a real explanation (final review round)

The user reviewed the Interview Book and said: the answers are too short and "direct, what-to-what". They are hard to STUDY and UNDERSTAND from. Re-work every answer on your page so that a reader who half-knows the topic can learn it from the answer alone. Do this for ALL questions on your page, one final time, so do it properly.

## What a good enriched answer looks like (typical 250 to 450 words, more for hard topics; never padded)
Write like a patient senior colleague teaching one person at a whiteboard. Plain, natural English. Define every term the first time. In most answers include, in whatever order reads best:
1. **What it is, from scratch** in one or two plain sentences (assume the reader has met the word but is fuzzy).
2. **Why it exists**: the problem it solves, what goes wrong without it. Explain WHY before HOW.
3. **How it works, step by step**: the actual mechanism, a numbered flow or a short timeline of what happens, with a SMALL CONCRETE EXAMPLE (real numbers, a tiny code/config/SQL snippet, a request walked through, before/after). Examples teach more than abstractions.
4. **Analogy** only when it genuinely helps (one line, not forced).
5. **Trade-offs and when to choose which**, with a clear decision rule.
6. **Pitfalls / what goes wrong in production / what an interviewer probes next**, in a sentence or two.
7. Where a picture helps, keep or add a clear inline SVG diagram.
8. For comparisons ("X vs Y"), add a small table AND explain the difference in words.
Keep it easy to read: short paragraphs, one idea per paragraph, occasional bullet list or table, bold the key term, but no wall of text and no keyword dumps.

## Keep the interview usefulness
Keep a short "what to say" opening so the candidate can answer aloud in 20 seconds, then go deeper. On pages that already use the v2 markup (`<p class="ia">` direct answer first, `<p class="rem"><b>Remember:</b> ...</p>` last), KEEP both: the `ia` stays 2 to 4 sentences, but add the explanatory body between them (several `<p>`, lists, tables, snippets, diagrams). On HLD pages (`hld-*.html`, free-form) keep whatever structure the answer already has but enrich it the same way; a short bold "In one line:" or "Say this:" opening followed by the explanation works well. Do not remove the quick revision/rapid-fire/cheat-sheet sections; you may leave them compact.

## Rules
- Do NOT change question ids, summaries (you may fix wording), the badge/level spans, the `iq`/`iq scn` classes or the page skeleton. Do NOT reduce the number of questions. You MAY add a missing question that a senior interviewer would genuinely ask, with a new unique id, and you MAY fix a wrong or misleading question. Do not add case studies (URL shortener, etc).
- Accuracy matters more than length. Fix any wrong, outdated or shaky fact you meet; hedge version-specific facts ("typically", "since version X") and never invent numbers. List unsure facts in your final report.
- Do not copy-paste filler to reach a word count. Every added sentence must teach something.
- Keep the page-level checks passing: balanced HTML, unique ids, only `<script src="../../theme.js">` in head, no external URLs, no unsafe DOM API names written in text, every `<h2>` has an id, every `<a href="#...">` resolves. Do not touch the `<!--qnav:start-->...<!--qnav:end-->` and `<!--qfoot:start-->...<!--qfoot:end-->` blocks if present (the build regenerates them). Do not run `tools/build_site.py`, and edit ONLY your own page.
- Existing diagrams: keep them (fix unclear ones). Add a diagram where a flow, lifecycle, comparison or architecture is easier to see than to read.

## Method (the pages are big: work in chunks, never in one giant write)
1. Copy your page into your own directory `C:/Users/kmangali/.claude/jobs/4820a254/tmp/depth-<slug>/` and split it into parts at each `<h2` (a small `python -I` script is fine; use the Write tool for any file containing backslashes, `python3` does not exist, use `python -I`; never share scripts or directories with other agents).
2. Enrich part by part (each part of roughly 8 to 15 questions), writing the new part file, then join all parts back into the final page at `C:/Users/kmangali/HLD/interview/topics/<slug>.html`. Keep the original page backed up in your directory.
3. Check from `C:/Users/kmangali/HLD/interview`: `python -I tools/check_interview.py topics/<slug>.html` and fix every PROBLEMS line. Question count must stay the same or increase.
4. Final report (short): file path, question count before and after, words before and after, and any facts you are unsure of or changed.
