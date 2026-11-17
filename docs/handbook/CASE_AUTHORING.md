# Authoring guide for System Design Handbook case studies and cheat sheets

First read `AUTHORING.md` completely (quality bar, skeleton, CSS/SVG vocabulary, safe-JS rules, procedure). Everything there applies, with the differences below. Read `chapters/12-cdn.html` for visual style and `chapters/01-interview-framework.html` for the interview framework this page follows.

## Case study pages (`case-studies/cNN-slug.html`)
- Location: `case-studies/`. Asset paths start with `../assets/`. Links to chapters: `../chapters/NN-slug.html`; to other case studies: `cNN-slug.html`; cheat sheets: `../cheatsheets/cs-*.html`.
- Kicker: `Case study NN · Worked solutions`. Title: "Design ...". `data-page` equals the file name without `.html`.
- Length: at least 4,500 words (checker minimum 4,000), at least 6 SVG diagrams, at least 8 Q&A blocks (follow-up questions an interviewer would ask, with strong answers).
- Write it as a worked interview solution, shaped to the problem (not a rigid template), but cover these in order unless a better order exists:
  1. Problem statement and clarifying questions (list the questions and the answers you assume).
  2. Functional and non-functional requirements; explicit out-of-scope.
  3. Estimation with real arithmetic: users, QPS average and peak, read:write ratio, storage per day/year, bandwidth, memory for caches. Show the numbers.
  4. API design (endpoints/messages with fields).
  5. Data model and storage choice, with the reason for each store (link the chapter that owns the technology).
  6. A first simple design (single box or two), then the scaled high-level architecture diagram, then a numbered request-flow walkthrough for each core operation (sequence diagrams).
  7. Deep dives (2 to 4) on the hardest parts: the part an interviewer would probe. Compare at least two options with a tradeoff table and justify the choice.
  8. Scaling, bottlenecks, hot spots, caching, sharding strategy.
  9. Failure modes: for each major component say what happens when it fails, slows, or returns wrong data, and the mitigation. Consistency and idempotency decisions. Multi-region if relevant.
  10. Security/abuse, monitoring and SLOs (brief, specific to this system), cost notes.
  11. Evolution: what changes at 10x scale, what you would build first (phasing), alternatives not chosen.
  12. Interview Q&A, "Connects to" (link the chapters used, with chapter numbers) and a recap.
- Link generously to the chapters that own each technique (do not re-teach them; one-sentence recap, then link).
- Numbers must be internally consistent with the estimation section.

## Cheat sheet pages (`cheatsheets/cs-*.html`)
- Location `cheatsheets/`, same `../assets/` paths. At least 900 words of dense, scannable content: tables, short rules, numbers, decision flows. At least 3 diagrams or large tables; Q&A not required. Each row/item links to the owning chapter. Prose may be terse here (this is the one place terse is correct), but every number must be defensible; use "about"/"typically" when unsure.
- Kicker: `Cheat sheet`.

## Everything else
Same procedure as `AUTHORING.md`: run `python -I tools/check.py <file>` from `C:\Users\kmangali\HLD\handbook` until it prints OK, do not edit shared files or other pages, final reply in 3 lines (path, checker counts, facts you were unsure of).
