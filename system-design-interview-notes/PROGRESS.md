# Progress Tracker

## Current direction

The interview notes are the primary learn-and-revise path. The tutorials remain focused concept references, `real-world-examples/` remains the canonical home for complete design walkthroughs, and `system-design-mastery/` remains a separate first-principles textbook. No content in those three directories was intentionally changed as part of this notes expansion.

## Content inventory

- [x] Landing page, curriculum, editorial standard, and progress tracker inspected on the default branch.
- [x] Existing 12 chapter pages inspected.
- [x] Tutorials and real-world-example indexes inspected.
- [x] Mastery landing page inspected to preserve scope boundaries.
- [x] Chapters 13–17 added for distributed correctness, networking/real-time, specialized infrastructure, interview methodology/estimation, and senior trade-offs/case-study practice.
- [x] Chapters 1–12 strengthened with scenario practice, interview Q&A, diagrams where useful, and targeted authoritative references.
- [x] README and curriculum navigation updated for 17 chapters.
- [x] Case-study pathways linked to canonical examples rather than copied.

## Verification status — do not infer completion from chapter existence

- [ ] Full topic-by-topic audit against every requirement in the execution brief.
- [ ] Review the new addenda against neighboring chapter material to remove any duplication and align all terminology.
- [ ] Independent technical review of all 17 chapters and all claims.
- [x] All 15 case-study destination paths in Chapter 17 fetched successfully from the current repository.
- [ ] All relative Markdown links checked mechanically.
- [ ] All Mermaid blocks rendered with a Mermaid renderer.
- [ ] Numerical examples independently rechecked across every chapter.
- [ ] Final editorial review for duplication, terminology, and answer length.
- [ ] Repository diff reviewed to confirm protected directories are unchanged.

## Known review findings and limitations

- The expanded chapters now include scenarios and interview Q&A across the core topics, plus additional request, replication, cache, outbox, resilience, security, observability, and interview-method diagrams. Mermaid syntax has not yet been rendered by a dedicated Mermaid renderer; a balanced Markdown code-fence check is not a rendering test.
- The 15 curated case-study links in Chapter 17 were checked by fetching each exact destination. The wider set of relative links across all existing chapters has not yet been mechanically checked.
- The existing 12 chapters have now received targeted addenda and the new chapters have been expanded. A full line-by-line technical correction pass across all 17 chapters is still not claimed here.
- No claim is made that the full 23-module inventory has passed acceptance. This tracker should only be updated after each outstanding check is actually performed.

## Quality rules

- Prefer explanations over keyword lists.
- Include interview questions with clear, technically sound answers.
- Keep examples purposeful and avoid repetition.
- State assumptions and units in calculations.
- Distinguish protocol/vendor guarantees from general patterns.
- Drafting a chapter does not mean it has passed technical review.
- Mark checks complete only after they have actually been performed.
