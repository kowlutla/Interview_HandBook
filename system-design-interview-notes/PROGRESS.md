# Progress Tracker

## Current direction

The interview notes are the primary learn-and-revise path. The tutorials remain focused concept references, `real-world-examples/` remains the canonical home for complete design walkthroughs, and `system-design-mastery/` remains a separate first-principles textbook. No content in those three directories was intentionally changed as part of this notes expansion.

## Content inventory

- [x] Landing page, curriculum, editorial standard, and progress tracker inspected on the default branch.
- [x] Existing 12 chapter pages inspected.
- [x] Tutorials and real-world-example indexes inspected.
- [x] Mastery landing page inspected to preserve scope boundaries.
- [x] Chapters 13–17 added for distributed correctness, networking/real-time, specialized infrastructure, interview methodology/estimation, and senior trade-offs/case-study practice.
- [x] README and curriculum navigation updated for 17 chapters.
- [x] Case-study pathways linked to canonical examples rather than copied.

## Verification status — do not infer completion from chapter existence

- [ ] Full topic-by-topic audit against every requirement in the execution brief.
- [ ] Independent technical review of all 17 chapters and all claims.
- [x] All 15 case-study destination paths in Chapter 17 fetched successfully from the current repository.
- [ ] All relative Markdown links checked mechanically.
- [ ] All Mermaid blocks rendered with a Mermaid renderer.
- [ ] Numerical examples independently rechecked across every chapter.
- [ ] Final editorial review for duplication, terminology, and answer length.
- [ ] Repository diff reviewed to confirm protected directories are unchanged.

## Known review findings and limitations

- The new chapters include worked estimates, failure paths, trade-off tables, and Mermaid diagrams, but diagram syntax has not yet been rendered by a dedicated Mermaid renderer.
- The 15 curated case-study links in Chapter 17 were checked by fetching each exact destination. The wider set of relative links across all existing chapters has not yet been mechanically checked.
- The existing 12 chapters have been inspected for scope and content, but a complete line-by-line technical correction pass across all 17 chapters is not claimed here.
- No claim is made that the full 23-module inventory has passed acceptance. This tracker should only be updated after each outstanding check is actually performed.

## Quality rules

- Prefer explanations over keyword lists.
- Include interview questions with clear, technically sound answers.
- Keep examples purposeful and avoid repetition.
- State assumptions and units in calculations.
- Distinguish protocol/vendor guarantees from general patterns.
- Drafting a chapter does not mean it has passed technical review.
- Mark checks complete only after they have actually been performed.
