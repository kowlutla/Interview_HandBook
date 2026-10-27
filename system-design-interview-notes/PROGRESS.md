# Progress Tracker

## Current direction

The HLD notes are the primary learn-and-revise path. The tutorials remain focused concept references, `real-world-examples/` remains the canonical home for complete design walkthroughs, and `system-design-mastery/` remains a separate first-principles textbook. No content in those three directories was intentionally changed as part of this notes expansion.

## Content inventory

- [x] Landing page, curriculum, editorial standard, and progress tracker inspected on the default branch.
- [x] Existing 12 chapter pages inspected.
- [x] Tutorials and real-world-example indexes inspected.
- [x] Mastery landing page inspected to preserve scope boundaries.
- [x] Chapters 13–17 added for distributed correctness, networking/real-time, specialized infrastructure, design workflow/estimation, and senior trade-offs/case-study practice.
- [x] Chapters 1–12 strengthened with scenario analysis, diagrams where useful, and targeted authoritative references.
- [x] README and curriculum navigation updated for 17 chapters.
- [x] Case-study pathways linked to canonical examples rather than copied.
- [x] Added focused coverage for consistent hashing/rebalancing, multi-region failover, consensus/clocks/fencing, B-tree versus LSM trade-offs, CDC projections, and safe architecture migration.
- [x] Removed interview-question/Q&A sections from the notes, converted scenario prompts to declarative cases, and updated the README, curriculum, and editorial standard to enforce a notes-only format.

## Verification status — do not infer completion from chapter existence

- [ ] Full topic-by-topic audit against every requirement in the execution brief.
- [ ] Review the new addenda against neighboring chapter material to remove any duplication and align all terminology.
- [ ] Independent technical review of all 17 chapters and all claims.
- [x] All 15 case-study destination paths in Chapter 17 fetched successfully from the current repository.
- [x] Relative Markdown links in all 21 Markdown files under `system-design-interview-notes/` checked mechanically against the current repository tree; 56 local links resolved and no missing targets were found. (This is not a whole-repository link audit.)
- [ ] All Mermaid blocks rendered with a Mermaid renderer.
- [x] Markdown code-fence counts checked for balance across the 17 chapter pages (this does not validate Mermaid syntax or rendering).
- [ ] Numerical examples independently rechecked across every chapter.
- [ ] Final editorial review for duplication, terminology, and answer length.
- [ ] Repository diff reviewed to confirm protected directories are unchanged.

## Known review findings and limitations

- The expanded chapters now focus on concepts, design reasoning, worked scenarios, diagrams, and revision summaries, including request, replication, cache, outbox, resilience, security, observability, and design-workflow diagrams. Mermaid syntax has not yet been rendered by a dedicated Mermaid renderer; a balanced Markdown code-fence check is not a rendering test. The estimation arithmetic in Chapters 2 and 16 was manually rechecked, but a complete numerical audit of every chapter is still pending.
- The 15 curated case-study links in Chapter 17 were checked by fetching each exact destination. Relative Markdown links in the entire `system-design-interview-notes/` subtree were also checked against the repository tree: 56 local links resolved with no missing targets. The rest of the repository has not yet had a full mechanical link audit.
- The existing 12 chapters have now received targeted addenda and the new chapters have been expanded. A full line-by-line technical correction pass across all 17 chapters is still not claimed here.
- Coverage has been strengthened in several high-value gaps, but no claim is made that the full 23-module inventory has passed acceptance. The whole-repository link audit, Mermaid rendering, and full technical review remain outstanding. This tracker should only be updated after each outstanding check is actually performed.

## Quality rules

- Prefer explanations over keyword lists.
- Keep the notes concept-first; do not add interview-question or Q&A sections.
- Keep examples purposeful and avoid repetition.
- State assumptions and units in calculations.
- Distinguish protocol/vendor guarantees from general patterns.
- Drafting a chapter does not mean it has passed technical review.
- Mark checks complete only after they have actually been performed.
