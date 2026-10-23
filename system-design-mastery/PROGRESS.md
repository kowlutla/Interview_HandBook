# Build and Quality Progress

Check items only when the work has actually been performed.

## Repository audit and scope
- [x] Repository access and push permission confirmed from GitHub metadata.
- [x] Read root README.
- [x] Read existing tutorials index in read-only mode.
- [x] Read existing real-world examples index in read-only mode.
- [x] Confirmed destination README was absent at the checked path before creation.
- [x] Established strict write boundary: system-design-mastery/.
- [x] Designed an independent curriculum around learning dependencies rather than existing numbering.
- [x] Inspect the complete repository tree: the target contains eight planning/reference Markdown files and 19 chapter README files, with no extra Markdown lesson fragments.
- [x] Compare commits from the first textbook creation through the latest edit; all paths in the checked comparison are under system-design-mastery/.

## Planning artifacts
- [x] Textbook landing page.
- [x] Roadmap and dependency sketch.
- [x] Curriculum and coverage matrix.
- [x] Create an explicit chapter-by-chapter coverage audit with Missing/Mentioned/Developing/Deep definitions, prioritized gaps, and a section-level map for the current expansion pass.
- [x] Link the coverage audit from the textbook landing page.
- [x] Editorial and verification standard.
- [ ] Independent curriculum completeness and duplication review.
- [ ] Complete evidence-based mapping of every mandatory inventory row to exact chapter sections and verify each status.
- [x] Add targeted curriculum-gap sections for service discovery/configuration (Chapter 15), OAuth/OIDC token roles (Chapter 16), RED/USE observability methods (Chapter 17), and cloud service models (Chapter 18).

## Research
- [x] Identified primary references for HTTP semantics, CAP, consensus, logical clocks, databases, Kafka, SRE, OAuth, cloud and runtime behavior.
- [x] Cross-checked the expanded topic inventory against current official architecture guidance from Azure, AWS, Google SRE, OWASP, and CNCF.
- [ ] Verify chapter claims against primary papers, standards and official documentation in a dedicated pass.
- [x] Expand the reference library with official architecture-style, load-balancing, API-gateway throttling, CDN-cache-control, and API-security guidance.
- [ ] Recheck all source links during final audit.
- [x] Spot-check newly added protocol references against RFC Editor records and correct the RFC 9000 reference to the stable RFC information page; broader source-link verification remains open.

## Textbook implementation
- [x] Draft all 19 chapter files.
- [x] Reorganize the textbook into 19 chapter folders, each with one coherent README.md chapter page.
- [x] Avoid over-fragmentation: consolidate chapters into a single reading file per folder rather than many tiny lesson files.
- [x] Add Mermaid diagrams where request flows, data paths, decision loops, or recovery sequences benefit from visualization.
- [x] Create glossary.
- [x] Create reference library.
- [ ] Review each module for accuracy, clarity, depth and prerequisite coverage.
- [x] Expand chapters 1–5 with additional first-principles explanations, mechanisms, edge cases, failure modes, operational checklists, and worked reasoning where appropriate.
- [x] Add a Chapter 5 protocol deep dive covering IPv6, DNSSEC versus encrypted DNS, TLS/mTLS, HTTP/2 versus HTTP/3, and DDoS/resource exhaustion, with relevant RFC references.
- [x] Add a worked Chapter 7 sharding/resharding example, Chapter 10 consistency timeline, and Chapter 14 SLO/error-budget calculation.
- [x] Expand chapters 11–19 with deeper protocol mechanics, operational edge cases, security controls, recovery workflows, IaC state/drift, SBOM and build provenance, and review checklists.
- [x] Deepen chapters 6–10 with additional API contract semantics, secure webhook delivery, relational concurrency/query planning, storage-engine internals including distributed file/object/block storage, cache correctness, and distributed consistency reasoning.
- [ ] Cross-chapter terminology and consistency review.
- [x] Fix Chapter 11 supplemental consensus sections appearing after the Further reading heading.
- [x] Reorder Chapter 11's consensus, fencing, transaction and review sections into a coherent reading sequence.
- [x] Consolidate duplicate deep-dive sections and repeated Further reading headings found in Chapters 10–11.
- [x] Add deep-dive sections on load balancers/CDNs (Chapter 5), API gateways (Chapter 6), architecture styles (Chapter 15), storage-model selection and search/analytics (Chapter 8), messaging delivery semantics (Chapter 12), overload/admission/backpressure (Chapter 13), Kubernetes runtime behavior (Chapter 18), recovery engineering (Chapter 14), threat modeling and tenant isolation (Chapter 16), practical observability (Chapter 17), and architecture patterns/anti-patterns (Chapter 19).
- [ ] Expand any chapter whose coverage remains too compressed for textbook-level mastery.

## Validation
- [x] Validate relative internal Markdown links in all created Markdown files against the expected file set; no broken internal targets found.
- [x] Recheck all 27 Markdown paths in the target tree and the relative links in the landing page and all chapter pages.
- [ ] Validate Mermaid diagrams with a renderer; currently added diagrams have only been manually reviewed.
- [x] Check all 19 chapter pages for balanced fenced code blocks and exact duplicate Markdown headings; none were found.
- [x] Re-run structural and relative-link checks across all 19 chapter pages after the latest content edits; no broken relative file targets, unbalanced code fences, or duplicate headings were found.
- [x] Independently recalculate the chapter's traffic, bandwidth, storage, Little's Law and fan-out examples; results match within rounding.
- [ ] Review assumptions, caveats and implementation-specific claims.
- [ ] Audit for missing topics, duplication and out-of-scope content.
- [x] Verify final repository path boundary against the original textbook baseline; the checked comparison contains no paths outside system-design-mastery/.
- [ ] Report limitations honestly; do not claim the textbook complete until all acceptance checks pass.

## Current status
The independent curriculum and all 19 chapter drafts have been reorganized into chapter folders with one full-length README.md per chapter. The mandatory topic inventory has been expanded and cross-checked against current official architecture and operations references; this is a coverage checklist, not evidence that every topic is already deeply taught. Chapters 1–5 and 11–19 have received deeper content passes adding conceptual distinctions, internal mechanics, examples, trade-offs, failure modes, and practical review/troubleshooting checklists. Chapters 6–10 have now received a deeper content pass. All 19 chapters have had at least one expansion pass, but chapter depth is not yet uniformly exhaustive and needs a comparative review. The current structure is intentionally not split into many tiny files. Mermaid diagrams are present across all 19 chapters. All 19 chapter pages passed a fresh structural and relative-file-link check after the latest edits: no broken relative file targets, unbalanced code fences, or duplicate headings were found. Actual Mermaid renderer validation remains open because no Mermaid rendering tool is available in the current environment. Relative internal links were rechecked across the landing page, all 19 chapter pages, and the target's Markdown inventory; all relative targets reviewed resolve within the intended tree. Chapter 10's overlapping deep-dive material has been consolidated into a sequential section set. Chapter 11's consensus deep dives were moved before its references after a structural audit found they had been appended after the Further reading heading; related sections were then reordered and overlapping review material consolidated. A targeted coverage pass also expanded service discovery/configuration, OAuth/OIDC token roles, RED/USE observability, and cloud service models in Chapters 15–18. A first coverage audit now exists, and additional deep-dive sections were added to Chapters 1–8, 10–19, including network security boundaries, service mesh, multi-region consistency, and worked capacity and database examples. The audit statuses are provisional and do not claim those chapters are fully verified. The audit now maps major topic families to concrete sections and identifies remaining high-priority depth risks. A full claim-by-claim technical review, topic-by-topic coverage mapping, Mermaid renderer validation, and source-link audit remain open. Recent targeted examples now cover resharding, consistency after uncertain writes, and request-based SLO budgets; their assumptions still require primary-source review. Actual animated media is not used: GitHub Markdown is best served by clear Mermaid diagrams and stepwise sequence/flow diagrams, which remain readable and version-controlled.
