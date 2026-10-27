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
- [x] Inspect the complete repository tree: the target now contains eight planning/reference Markdown files and 20 chapter README files, with no extra Markdown lesson fragments.
- [x] Compare commits from the first textbook creation through the latest edit; all paths in the checked comparison are under system-design-mastery/.

## Planning artifacts
- [x] Textbook landing page.
- [x] Roadmap and dependency sketch.
- [x] Curriculum and coverage matrix.
- [x] Create an explicit chapter-by-chapter coverage audit with Missing/Mentioned/Developing/Deep definitions, prioritized gaps, and a section-level map for the current expansion pass.
- [x] Refresh the coverage audit's remaining risks after closing multiple content gaps; separate content work from still-open source, schema, OpenAPI, Mermaid and cross-chapter verification.
- [x] Link the coverage audit from the textbook landing page.
- [x] Editorial and verification standard.
- [ ] Independent curriculum completeness and duplication review.
- [ ] Independently verify each mapped mandatory inventory row's coverage status and evidence; promote to Deep only after its acceptance criteria pass.
- [x] Draft a row-by-row map for all 21 mandatory curriculum topic families to exact teaching sections, with provisional statuses and explicit verification gaps; independent status verification remains open.
- [x] Add targeted curriculum-gap sections for service discovery/configuration (Chapter 15), OAuth/OIDC token roles (Chapter 16), RED/USE observability methods (Chapter 17), and cloud service models (Chapter 18).

## Research
- [x] Identified primary references for HTTP semantics, CAP, consensus, logical clocks, databases, Kafka, SRE, OAuth, cloud and runtime behavior.
- [x] Cross-checked the expanded topic inventory against current official architecture guidance from Azure, AWS, Google SRE, OWASP, and CNCF.
- [ ] Verify chapter claims against primary papers, standards and official documentation in a dedicated pass.
- [x] Add an evidence log for targeted checks of PostgreSQL isolation/write-skew claims, Kafka 4.3 delivery boundaries, OWASP injection guidance, SLSA v1.2, SPDX version wording, OpenAPI 3.1.0 syntax, NIST SSDF publication status, and core network RFC references.
- [x] Add a targeted evidence entry for Chapter 10's formal CAP framing and Lamport-clock causality distinction using the primary paper sources; full distributed-consistency claim review remains open.
- [x] Recalculate Chapter 17's request-based SLO example: a 99.9% target permits a 0.1% bad-event fraction, 10 million eligible requests imply 10,000 bad events of budget, and a 2% observed error rate is a 20× burn rate for that window.
- [x] Add the official OpenTelemetry documentation to the targeted evidence log for observability signals, context propagation and sampling; implementation-specific behavior remains version/language dependent.
- [x] Expand the reference library with official architecture-style, load-balancing, API-gateway throttling, CDN-cache-control, and API-security guidance.
- [x] At the original 19-chapter checkpoint, scan all Further reading blocks for duplicate URLs; remove duplicated RFC references in Chapter 05 and add an explicit RFC 9111 HTTP-caching link. Chapter 20 was added later and needs its own full source-link audit.
- [x] Scan the 73 URL occurrences in the reference catalog for duplicate destinations; all 73 were unique. Link liveness, redirect behavior, and claim-to-source alignment remain open.
- [ ] Recheck all source links during final audit.
- [x] Spot-check newly added protocol references against RFC Editor records and correct the RFC 9000 reference to the stable RFC information page; broader source-link verification remains open.
- [x] Validate the W3C WCAG 2.2 and C4 model references against their official pages, confirm AWS/Google sustainability guidance is provider-specific, and replace an inaccessible Java 21 structured-concurrency API URL with the official guide.
- [x] Remove duplicate entries from the research library and group newly added protocol/webhook/SBOM references with the existing source catalog.
- [x] Add C4 model, WCAG 2.2 and provider sustainability references to support the latest chapter expansions.
- [x] Add The Tail at Scale as a primary reference and update the OWASP API Security Top 10 link to its canonical current domain.
- [x] Add NIST SSDF, SLSA provenance and SPDX specification references to support cloud software-supply-chain guidance; check that SP 800-218 v1.1 is labeled as a final publication while later revision status is checked separately.
- [x] Add the July 2026 CISA SBOM minimum-elements guidance link to Chapter 18 and the reference catalog.
- [x] During the source spot-check, identify that SLSA v1.0 pages are retired and update chapter/reference links to the approved v1.2 specification and versioned build-provenance pages.
- [x] Replace generic Kafka documentation redirects with versioned Kafka 4.3 design and message-delivery-semantics links after checking the current official documentation.
- [x] Verify the OpenAPI example's declared 3.1.0 version against the official versioned specification and add matching reference links; a full OpenAPI parser/linter run remains open.
- [x] Parse the Chapter 6 OpenAPI YAML excerpt and manually verify its version field, path parameter, response and required schema fields; a dedicated OpenAPI validator/linter run remains open.

## Textbook implementation
- [x] Draft all 20 chapter files, including the new client-side/offline-first/real-time architecture chapter.
- [x] Reorganize the textbook into 20 chapter folders, each with one coherent README.md chapter page.
- [x] Avoid over-fragmentation: consolidate chapters into a single reading file per folder rather than many tiny lesson files.
- [x] Add Mermaid diagrams where request flows, data paths, decision loops, or recovery sequences benefit from visualization.
- [x] Create glossary.
- [x] Create reference library.
- [x] Perform a scoped manual review of Chapter 01's worked architecture decision and Chapter 02's quality-attribute scenarios/interactions; clarify provider-specific payment idempotency-key scope and retention, and record review limits in COVERAGE-AUDIT.md.
- [x] Perform a scoped review of Chapter 03 capacity arithmetic, Chapter 04 deadline/cancellation semantics, Chapter 10 consistency claims, and Chapter 12 consumer-offset crash timelines; correct Kafka's record-offset versus next-position wording and record the review limits in COVERAGE-AUDIT.md.
- [x] Perform a scoped review of Chapter 05 timeout troubleshooting, Chapter 06 OpenAPI evolution, Chapter 07 write-skew reasoning, and Chapter 11 fencing; record inspected claims and remaining implementation/source-verification limits in COVERAGE-AUDIT.md.
- [x] Recalculate Chapter 13 concurrency-limit deltas, Chapter 14 SLO/recovery arithmetic, Chapter 17 error-budget math, and Chapter 19 Bloom-filter sizing; record remaining technical/source-review boundaries in COVERAGE-AUDIT.md.
- [x] Expand the curriculum from 19 to 20 chapters after the independent gap scan identified missing client-side, offline-first and real-time architecture coverage.
- [x] Add Chapter 20 covering rendering/delivery, client/server state ownership, offline persistence, synchronization/conflict resolution, realtime transports, WebRTC, collaboration, micro-frontends, interactive sessions, security and operations.
- [x] Add Chapter 20 to the textbook index, learning roadmap, curriculum matrix, mandatory inventory, coverage audit and glossary.
- [x] Extend the editorial standard with client/server state ownership, offline durability, synchronization checkpoints, conflict/deletion policy, reconnect/replay, backpressure and WebRTC trust-boundary requirements.
- [x] Extend the row-by-row mandatory inventory map to 21 topic families; all statuses remain provisional.
- [x] Perform a targeted source review of Chapter 20 browser-storage durability and WebRTC TURN/SFU encryption boundaries; record the official/provider references and remaining verification scope in COVERAGE-AUDIT.md.
- [ ] Review Chapter 20's technical claims against primary/official sources; verify rendering/security details and all external references.
- [x] Perform a targeted structural check of Chapter 20: balanced fences, no duplicate headings, Further reading order, two recognized Mermaid declarations, and valid textbook footer links.
- [x] Perform a current structural and relative-link check across all 28 Markdown files after adding Chapter 20; all local relative targets resolve, fences are balanced, headings are unique, and no instructional headings follow Further reading.
- [ ] Validate the two new Mermaid diagrams with a renderer; currently they have only been manually inspected.
- [ ] Review each module for accuracy, clarity, depth and prerequisite coverage.
- [x] Expand chapters 1–5 with additional first-principles explanations, mechanisms, edge cases, failure modes, operational checklists, and worked reasoning where appropriate.
- [x] Add a Chapter 5 protocol deep dive covering IPv6, DNSSEC versus encrypted DNS, TLS/mTLS, HTTP/2 versus HTTP/3, and DDoS/resource exhaustion, with relevant RFC references.
- [x] Add a Chapter 5 practical troubleshooting lab with phase-based symptoms, evidence and hypotheses, a disciplined investigation sequence, and a timeout-after-deployment worked example.
- [x] Add a Chapter 17 worked request-based SLO alert example connecting good-event definitions, error-budget arithmetic, burn rate, alert response policy and validation.
- [x] Add a Chapter 7 concurrent write-skew lab showing invariant violation and comparing database protection strategies.
- [x] Add a Chapter 12 consumer-crash timeline comparing database/offset commit ordering and the limits of exactly-once guarantees.
- [x] Add a Chapter 11 stale-lease failure timeline showing why fencing must be enforced atomically by the protected resource.
- [x] Add a Chapter 14 recovery rehearsal with timed restore, RTO/RPO measurement, data-integrity validation, stale-writer fencing and backlog drain.
- [x] Add a Chapter 12 producer/consumer schema-change risk matrix with compatibility caveats, deployment order and historical replay considerations.
- [x] Add a Chapter 12 projection rebuild/catch-up/cutover protocol with replay idempotency, partition offsets, validation and rollback criteria.
- [x] Clarify the Chapter 12 projection-rebuild boundary as a per-partition high-watermark/cutover point captured before historical replay, so live-event catch-up has an explicit boundary.
- [x] Add a Chapter 3 worked capacity-test plan with an illustrative workload mix, explicit acceptance thresholds, ramp/steady/spike/failure/soak phases and reproducibility requirements.
- [x] Add a Chapter 1 worked architecture evaluation comparing modular monolith, microservices and serverless using invariants, team constraints, validation evidence and revisit triggers.
- [x] Pair quality-attribute scenario examples in Chapter 2 with verification evidence and accountable roles.
- [x] Add a comparative storage access-pattern example distinguishing transactional, search, object, analytical and cached data.
- [x] Add a worked Chapter 19 noisy-neighbor scenario covering tenant fairness, replica-multiplied limits, reserved capacity and failure-topology testing.
- [x] Add a Chapter 16 tenant-scoped document-export threat model covering API, queue, worker, database, object-storage and operational trust boundaries.
- [x] Add explicit Chapter 16 injection guidance (parameterized queries, allow-listed identifiers, safe command execution, context-aware template/output handling) and a verification case; update the inventory map.
- [x] Add the OWASP Injection Prevention and SQL Injection Prevention Cheat Sheets to the reference library and link them from Chapter 16.
- [x] Spot-check OWASP injection-prevention URLs against the live Cheat Sheet pages; correct the SQL injection link to the verified HTML endpoint and make the SPDX reference version-neutral where the official index and spec redirect differ.
- [x] Spot-check the current OWASP Webhook Security Cheat Sheet and Debezium stable Outbox Event Router pages; implementation-specific validation remains required.
- [x] At the original 19-chapter checkpoint, inventory external URLs in the chapter pages and reference catalog; standardize the remaining Chapter 6 OWASP API Security link and replace the dated AWS Well-Architected curriculum link with the current framework entry point. Chapter 20 received a targeted source check, not a full link audit.
- [x] Add an explicit idempotent-receiver pattern explanation in Chapter 19 and define it in the glossary to match the mandatory cross-cutting pattern inventory.
- [x] Make powers-of-two binary capacity units explicit in Chapter 3 and map the concept to the capacity/performance inventory.
- [x] Make the CI/CD lifecycle and pipeline trust boundary explicit in Chapter 18, with guidance on isolated builds, least-privilege credentials, untrusted contributions, artifact provenance and release promotion; add the OWASP CI/CD security source.
- [x] Add Chapter 17 coverage for synthetic user-journey checks, deployment/configuration markers, and explicit incident-command roles; document the limits of synthetic checks versus real-user SLIs.
- [x] Clarify database buffer/page caches versus application-level object caches in Chapter 9, including the operational signals needed to evaluate each layer.
- [x] Add an explicit batch-versus-stream processing comparison in Chapter 12, including micro-batch, replay/output correctness and hybrid reconciliation trade-offs.
- [x] Explicitly define identity and access management (IAM) as a lifecycle and dependency boundary in Chapter 16, covering human/workload identities, revocation, audit and identity-provider availability.
- [x] Extend the glossary with batch processing, micro-batch, stream processing, CI/CD, IAM and synthetic-check definitions introduced or deepened during the coverage pass.
- [x] Make separation of concerns and logical-versus-physical architecture explicit in Chapter 1, including why logical components do not map one-to-one to deployed instances.
- [x] Clarify the database-per-service pattern in Chapter 15, including that it means data ownership/isolation rather than necessarily one physical server per service, and add anti-corruption-layer selection trade-offs.
- [x] Add glossary definitions for database-per-service and anti-corruption layer to align shared terminology with Chapter 15.
- [x] Recheck Chapter 1 after the architecture-foundations clarification; code fences, heading uniqueness, Further reading order and navigation footer remain valid.
- [x] Recheck Chapter 15 after the database-per-service and anti-corruption-layer additions; code fences, heading uniqueness, Further reading order and navigation footer remain valid.
- [x] Add a Chapter 9 cross-tenant/cache-poisoning test matrix covering tenant and role variation, header/key poisoning, revocation, stale-fill races and cache failure.
- [x] Add a Chapter 19 cross-pattern review of retry/hedge/breaker interactions, aggregate pool limits, cache/replica freshness, outbox/inbox, failover fencing and replay side effects.
- [x] Add a Chapter 6 worked OpenAPI evolution example covering additive fields, breaking changes, contract tests and deprecation gates.
- [x] Add a Chapter 13 worked concurrency-limit decision using illustrative throughput, p99 latency, error rate and queue-growth measurements.
- [x] Add a Chapter 4 deadline/cancellation scenario distinguishing required and optional fan-out work from durable background jobs.
- [x] Add write-skew and inbox-pattern terms to the glossary.
- [x] Add a worked Chapter 7 sharding/resharding example, Chapter 10 consistency timeline, and Chapter 14 SLO/error-budget calculation.
- [x] Deepen Chapter 1 with architecture viewpoints and diagram selection; Chapter 2 with accessibility, usability, internationalization, operability, portability, cost and sustainability; Chapter 3 with load-test methodology; and Chapter 4 with cancellation and structured concurrency.
- [x] Deepen Chapter 9 with cache-key security, cache poisoning, tenant isolation, stale-serving policies, permission revocation and deletion; deepen Chapter 12 with event sourcing/CQRS distinctions, projection rebuilds, schema compatibility and event-data privacy.
- [x] Add Chapter 13 guidance on hedged requests and adaptive concurrency, Chapter 16 API threat patterns aligned to OWASP categories, and a worked Bloom-filter sizing example in Chapter 19.
- [x] Expand chapters 11–19 with deeper protocol mechanics, operational edge cases, security controls, recovery workflows, IaC state/drift, SBOM and build provenance, and review checklists.
- [x] Deepen chapters 6–10 with additional API contract semantics, secure webhook delivery, relational concurrency/query planning, storage-engine internals including distributed file/object/block storage, cache correctness, and distributed consistency reasoning.
- [ ] Cross-chapter terminology and consistency review.
- [x] Perform a targeted conceptual consistency review of Chapters 10–15: consistency/isolation terminology, quorum assumptions, stale-writer fencing, 2PC versus saga boundaries, messaging offset/effect crash windows, RTO/RPO arithmetic, retry/hedge amplification, delayed autoscaling, and architecture-style selection. Record only scoped findings; full claim-by-claim verification remains open.
- [x] Fix Chapter 11 supplemental consensus sections appearing after the Further reading heading.
- [x] Reorder Chapter 11's consensus, fencing, transaction and review sections into a coherent reading sequence.
- [x] Consolidate duplicate deep-dive sections and repeated Further reading headings found in Chapters 10–11.
- [x] Add deep-dive sections on load balancers/CDNs (Chapter 5), API gateways (Chapter 6), architecture styles (Chapter 15), storage-model selection and search/analytics (Chapter 8), messaging delivery semantics (Chapter 12), overload/admission/backpressure (Chapter 13), Kubernetes runtime behavior (Chapter 18), recovery engineering (Chapter 14), threat modeling and tenant isolation (Chapter 16), practical observability (Chapter 17), and architecture patterns/anti-patterns (Chapter 19).
- [ ] Expand any chapter whose coverage remains too compressed for textbook-level mastery.

## Validation
- [x] Audit section ordering across all chapter pages and move supplemental worked diagrams/guidance ahead of each chapter's Further reading section; keep navigation footer at the end.
- [x] Re-run chapter-level structural checks after the section-order correction: all 19 pages have balanced fenced blocks, no exact duplicate headings, no instructional headings after Further reading, and the navigation footer at the end.
- [x] Revalidate relative Markdown targets across all 27 Markdown files in the textbook tree after section reordering; no missing local targets found.
- [x] Recheck Chapters 12 and 16 after the versioned Kafka-link and injection-guidance edits; their fences, headings, Further reading order, and navigation footers remain structurally valid.
- [x] Recheck Chapters 6, 16 and 19 after the final source-link and pattern edits; chapter fences, duplicate headings, Further reading order and navigation footers remain valid.
- [x] Recheck every chapter modified during the latest coverage-gap pass (03, 09, 12, 16, 17, 18, 19): balanced fences, no exact duplicate headings, no instructional headings after Further reading, and footer at end.
- [x] Validate relative internal Markdown links in all created Markdown files against the expected file set; no broken internal targets found.
- [x] Recheck all 27 Markdown paths in the target tree and the relative links in the landing page and all chapter pages.
- [x] Re-run relative-link validation across all 27 Markdown files after the latest Chapter 05 and Chapter 12 edits; no broken local targets were found.
- [ ] Validate Mermaid diagrams with a renderer; currently added diagrams have only been manually reviewed.
- [x] Perform a static Mermaid inventory check across all 19 chapters: 24 non-empty Mermaid blocks have recognized diagram declarations; actual Mermaid rendering remains unverified because no renderer is available.
- [x] Check all 19 chapter pages for balanced fenced code blocks and exact duplicate Markdown headings; none were found.
- [x] Re-run structural and relative-link checks across all 19 chapter pages after the latest content edits; no broken relative file targets, unbalanced code fences, or duplicate headings were found.
- [x] Recheck all 19 chapter pages and the textbook landing page after the latest worked labs; relative Markdown links resolve, fenced blocks are balanced, and no duplicate headings were found.
- [x] Independently recalculate the chapter's traffic, bandwidth, storage, Little's Law and fan-out examples; results match within rounding.
- [x] Recheck the Chapter 19 Bloom-filter sizing arithmetic and cross-check the illustrative 99.9% request SLO/error-budget arithmetic against the stated definitions; detailed service-specific assumptions remain illustrative.
- [x] Perform a scoped review of Chapters 9 and 16–18 covering cache isolation and revocation, asynchronous authorization, API threat boundaries, telemetry cardinality/context trust, and supply-chain artifact evidence. Record remaining implementation-specific verification in COVERAGE-AUDIT.md; full review remains open.
- [ ] Review assumptions, caveats and implementation-specific claims.
- [ ] Audit for missing topics, duplication and out-of-scope content.
- [x] Verify final repository path boundary against the original textbook baseline; the checked comparison contains no paths outside system-design-mastery/.
- [x] Original 19-chapter baseline comparison: 45 changed paths, all under `system-design-mastery/`; the target then contained 27 Markdown files and 19 chapter README pages. This is historical; the expanded current tree contains 28 Markdown files and 20 chapter README pages.
- [ ] Report limitations honestly; do not claim the textbook complete until all acceptance checks pass.

## Current status
The textbook now has 20 substantive chapter pages in chapter folders, supported by the landing page, roadmap, curriculum, coverage audit, editorial standard, glossary and research library. A curriculum gap scan identified that client-side rendering/delivery, offline-first persistence, synchronization/conflict resolution, realtime transports, WebRTC, collaborative editing, micro-frontends and interactive-session architecture were not taught in depth; Chapter 20 was added rather than treating scattered mentions as sufficient coverage. The mandatory inventory now contains 21 topic families and all statuses remain provisional until independent acceptance checks pass.

The textbook currently contains 28 Markdown files and 26 Mermaid blocks by inventory. A current static check across all 28 files found balanced fenced blocks, no exact duplicate headings, no instructional headings after Further reading, and no broken local relative Markdown targets. Mermaid rendering remains unverified. Scoped technical reviews and corrections are recorded in COVERAGE-AUDIT.md, including payment idempotency-key retention boundaries and Kafka record-offset versus next-position terminology. The human-readable consolidation pass now covers all 20 chapters. Chapters 02, 05, 12 and 19 received earlier focused edits; the latest pass reviewed Chapters 01, 03, 04, 06–11 and 13–18, and Chapter 20 was reviewed for flow and unnecessary repetition.

Still open: independent curriculum/duplication review; claim-by-claim source verification; exhaustive external-link audit; verification of all 21 mandatory inventory rows; review of Chapter 20's client/offline/realtime claims; Mermaid rendering; OpenAPI parser/linter validation; and cross-chapter consistency review. The current 28-file structural and relative-link pass has now completed successfully. Do not mark the textbook complete or promote a row to Deep until the relevant acceptance criteria have actually passed.

Latest editorial correction and verification: a whole-book heading-order audit found supplemental worked diagrams/guidance placed after Further reading in multiple chapters. Those sections were moved into the instructional body before Further reading. A fresh check of all 19 chapter pages then confirmed balanced fenced blocks, no exact duplicate headings, no instructional headings after Further reading, and navigation footers at the end. Relative Markdown targets were also checked across all 27 Markdown files in the target tree; no missing local targets were found. This structural pass does not validate Mermaid rendering or prove technical claims; the full claim-by-claim and source-link audits remain open.


## Scope extension — 2026-10-24
The independent curriculum review found that the 19-chapter draft did not meaningfully cover client-side rendering/delivery, offline-first persistence, synchronization and conflict resolution, persistent real-time transports, WebRTC, collaborative editing, or micro-frontends. Rather than mark those topics as covered by passing mentions in API/network chapters, a dedicated Chapter 20 was added and linked from the landing page, roadmap, curriculum, coverage audit and glossary. The mandatory inventory now contains 21 topic families (the original 20 plus client-side/real-time architecture). Chapter 20 is substantive but remains **Developing** until its sources, assumptions, examples and diagrams receive the same independent verification as the other chapters.


## Human-readable consolidation pass — 2026-10-24

The user emphasized that the textbook must read like a human-written, readable explanation. The editorial standard now explicitly requires natural transitions, clear motivation before jargon, connected prose, purposeful examples, selective use of bullets/tables, and removal of repeated explanations and mechanical checklists.

- [x] Add explicit human-written readability criteria to EDITORIAL-STANDARD.md.
- [x] Consolidate Chapter 05 (Networking): remove repeated introductory/deep-dive treatment and combine related protocol, edge, security, timeout and troubleshooting guidance into a coherent request-journey explanation. Word count reduced from approximately 6,133 to 2,423 while retaining the main networking fundamentals.
- [x] Consolidate Chapter 12 (Messaging): merge repeated summaries and detailed sections into one learning path covering delivery semantics, partitions, retries, outbox/inbox, stream processing, schema evolution, CQRS/event sourcing, projection rebuilds, and privacy. Word count reduced from approximately 5,334 to 2,139 after retaining a compact schema-compatibility matrix and event-identity guidance.
- [x] Recheck relative Markdown targets across all 28 Markdown files in system-design-mastery/ after these edits; no missing local targets found.
- [x] Run static structure checks across all 28 Markdown files: balanced fenced blocks, no exact duplicate headings, and no instructional headings after Further reading.
- [x] Complete the first human-readability and duplication pass across all 20 chapters, prioritizing repeated summaries, overlapping explanations and checklist/table overload without shortening merely to reduce word count.
- [ ] Validate Mermaid diagrams with a renderer; static declaration and fence checks are not rendering validation.
- [ ] Run an OpenAPI parser/linter on the Chapter 06 example.
- [ ] Complete the claim-by-claim source and external-link audit.


## Additional human-readable review — 2026-10-24

- [x] Consolidate Chapter 02: remove repeated availability/reliability/durability/correctness definitions, repeated prioritization guidance, and a redundant review checklist. Retain the accessibility, operability, portability, cost, sustainability and quality-interaction content. Word count reduced from approximately 3,939 to 3,684.
- [x] Refresh coverage-audit section references after consolidating Chapters 02, 05 and 12.
- [x] Complete the same review across the remaining chapters; focus on overlapping explanations and checklist/table overload rather than reducing length arbitrarily.

- [x] Consolidate Chapter 19 (Advanced Cross-Cutting Reasoning): remove short summary sections that repeated the later worked explanations, preserve the queueing/tail-latency concept as a coherent section, and link back to the chapters that teach storage engines and messaging in depth. Word count reduced from approximately 3,890 to 3,499.

- [x] Recheck relative links, fenced blocks and duplicate headings in the changed chapters (02, 05, 12, 19) and their progress/audit/editorial documents after the consolidation edits; no issues found.
- [x] Open the canonical IETF RFC pages for TCP, TLS 1.3, HTTP semantics and HTTP/3, the versioned Kafka 4.3 design documentation, and the W3C WCAG 2.2 Recommendation; checked URLs resolve to the intended official sources. Claim-by-claim verification remains open.


## Remaining-chapter readability pass — 2026-10-24

- [x] Chapter 01: reduced repeated architecture-decision and decomposition explanations while retaining reversible/irreversible decision guidance and the distinct architecture-view and worked-evaluation sections.
- [x] Chapter 03: made the latency-budget section focus on budget composition and linked queueing detail to the dedicated saturation/tail-latency section.
- [x] Chapter 04: reduced repetition between the pool introduction, pool-sizing discussion and runtime-resource section.
- [x] Chapter 06: removed the repeated idempotent-retry sequence diagram while retaining the contract, retry, idempotency and failure-path explanations.
- [x] Chapter 07: replaced repeated introductory summaries with a short chapter orientation and removed duplicated isolation, query-plan, migration and checklist explanations; retained the overselling example, connection-pool admission-control guidance, sharding example and write-skew lab.
- [x] Chapters 08–11 and 13–18: consolidated repeated overview sections where later sections already teach the same mechanism in depth. Unique material was retained or folded into the detailed treatment, including the cache-benefit calculation, 2PC-versus-saga trade-offs, idempotency boundaries, and orchestration-versus-choreography choices.
- [x] Chapter 20: reviewed the full chapter for flow and repetition. Its sections address distinct client/offline/synchronization/realtime domains, so no broad shortening was warranted.
- [x] Rechecked the edited chapter pages (01, 03, 04, 06–11, 13–18) and Chapter 20 for balanced code fences, duplicate headings, instructional headings after Further reading, and navigation footer placement; all checks passed.
- [x] Run a fresh repository-wide relative-link check after these edits across all 28 Markdown files; no missing local relative targets found.
- [ ] Continue technical/source verification, Mermaid rendering and OpenAPI validation; readability completion does not imply technical certification.


## Rapid verification sprint — 2026-10-24

- [x] Fetch the current default-branch version of all 20 chapter README files and run a fresh structural sweep: all 20 have balanced fenced blocks, unique exact Markdown headings, a Further reading section, and the expected textbook navigation footer.
- [x] Inventory chapter Mermaid declarations: 22 Mermaid blocks across the 20 chapter pages. This is a static inventory only; it does not establish that the diagrams render successfully.
- [x] Confirm the current chapter file paths and current blob SHAs before recording this pass; no chapter content changes were needed from the structural scan alone.
- [ ] Render Mermaid diagrams using an actual Mermaid renderer.
- [ ] Validate the Chapter 06 OpenAPI 3.1.0 example using a parser/linter.
- [ ] Complete source-to-claim verification, external-link audit, independent mandatory-inventory review, and cross-chapter consistency review.

The sprint improves confidence in repository structure but does not certify technical correctness or complete the textbook. The acceptance criteria above remain open until executed and recorded.


## Targeted technical verification sprint — 2026-10-24

- [x] Independently recalculate Chapter 03 worked capacity example: 300 million requests/day = 3,472.22 average requests/s; 4x peak = 13,888.89 requests/s; 13 KiB combined request/response payload ≈ 176.32 MiB/s (before overhead); Little's Law at 120 ms ≈ 1,667 average in-flight requests; instance estimate under the stated 25% loss assumption = 23.15, rounded up to 24 before further validation.
- [x] Recalculate Chapter 19 Bloom-filter approximation for one million items at 1% target false-positive probability: approximately 9.585 million bits, 1.20 MB decimal / 1.14 MiB, and 6.64 optimal hash functions (about 7 in an implementation). The chapter correctly labels the result as approximate and states the assumptions.
- [x] Recheck Chapter 14 request-based SLO arithmetic: 99.9% SLO gives a 0.1% budget; 50 million eligible requests imply 50,000 bad events; 1% observed failures imply a 10x burn rate against a 0.1% target. Confirm the chapter distinguishes request-based from time-based SLOs.
- [x] Review scoped consistency claims in Chapters 10–11: quorum intersection is explicitly not presented as a complete linearizability proof; CAP availability is qualified; saga compensation is distinguished from atomic rollback; fencing is enforced at the protected resource; membership changes are qualified by protocol.
- [x] Parse the Chapter 06 OpenAPI YAML example with PyYAML and verify key invariants: OpenAPI 3.1.0 declaration, templated path parameter, required path parameter, response, and required schema fields. Cross-check path templating and required: true against the official OpenAPI 3.1.0 specification. This is a YAML parse plus targeted invariant check, not a full OpenAPI validator/linter.
- [x] Cross-check the Chapter 14 error-budget definition against Google's SRE Workbook: error budget is 1 minus the SLO, with request-count budgets dependent on the request-based SLI definition.
- [ ] Run a full OpenAPI 3.1 parser/linter. Attempting to launch the Mermaid CLI with npx timed out before the package could be obtained; no renderer result is claimed.
- [ ] Continue claim-by-claim source review, exhaustive external-link validation, independent verification of all 21 inventory rows, and cross-chapter consistency review. The scoped checks above do not complete these book-wide acceptance criteria.


## Chapter 20 source verification — 2026-10-24

- [x] Opened the current MDN browser-storage guidance and confirmed that browser-origin storage is best-effort by default, quota/eviction behavior varies by browser, and persistent-storage requests have browser-specific approval behavior.
- [x] Opened MDN's WebRTC protocol guidance and Cloudflare's TURN FAQ; checked the ICE/STUN/TURN distinction, TURN relay role, and the difference between point-to-point relay and SFU fan-out. The chapter's wording remains qualified and explicitly identifies Cloudflare's description as provider-specific.
- [x] Opened the W3C Indexed Database API 3.0 and Service Workers publications; updated Chapter 20's Further reading notes to identify the IndexedDB 3.0 document as a Working Draft and the Service Workers page as an evolving Candidate Recommendation Draft, rather than implying both are finalized Recommendations.
- [x] Added MDN's WebRTC protocol reference for ICE/STUN/TURN/SFU context.
- [ ] Continue checking all Chapter 20 references and source-to-claim alignment; the opened subset is not an exhaustive external-link audit.
- [ ] Validate Mermaid diagrams using a real renderer and run a full OpenAPI validator. Network/package retrieval is not available in the current execution environment; do not report these checks as passed.


## Final structural and focused source pass — 2026-10-24

- [x] Re-run the structural sweep across all 20 chapter pages after the Chapter 09 and Chapter 20 edits: all have balanced fences, no exact duplicate headings, a Further reading section, and the textbook navigation footer at the end.
- [x] Re-inventory chapter Mermaid blocks after removing a second, redundant Cache-aside read-path diagram from Chapter 09. Current chapter-page inventory is 29 non-empty Mermaid blocks with recognized diagram declarations across the 20 chapter pages; actual rendering remains unverified.
- [x] Remove the duplicate Chapter 09 cache-aside sequence diagram because the same read path is already explained and illustrated near the start of the chapter.
- [x] Add explicit draft-status qualifiers for the W3C Service Workers and IndexedDB 3.0 references in Chapter 20 and add MDN's WebRTC protocol guide.
- [x] Spot-check the current official MDN browser-storage and WebRTC protocol pages, Cloudflare's provider-specific TURN FAQ, and the W3C publication status pages. Results and limits are recorded in COVERAGE-AUDIT.md.
- [ ] Complete the full repository-wide external-link audit and source-to-claim review. A subset of Chapter 20 links and several foundational standards have been opened; this is not exhaustive.
- [ ] Run a Mermaid renderer and full OpenAPI 3.1 validator. Package retrieval failed in the current execution environment, so only static Mermaid checks and YAML parsing/targeted OpenAPI checks are confirmed.
- [ ] Complete the independent 21-family coverage acceptance and cross-chapter consistency review. Do not label the textbook fully technically accepted until these checks are performed.


## Additional validation pass — 2026-10-24

- [x] Re-parse the Chapter 06 Orders API example with PyYAML and rerun targeted OpenAPI invariants: OpenAPI version, non-empty paths, path-template/path-parameter correspondence, required path parameter, operationId, and response definition all pass.
- [x] Re-open foundational primary references used by the textbook: RFC 9110 (HTTP semantics), RFC 9293 (TCP), RFC 8446 (TLS 1.3), RFC 9114 (HTTP/3), OpenAPI 3.1.0, Google's SRE Workbook error-budget policy, WCAG 2.2, MDN browser storage guidance, MDN WebRTC protocols, and the W3C IndexedDB 3.0 publication.
- [x] Confirm the current source pages resolve in the web retrieval environment and confirm the published status of WCAG 2.2 (Recommendation) versus IndexedDB 3.0 (Working Draft).
- [x] At this checkpoint, local full OpenAPI validation was blocked by package/network constraints. This was subsequently completed in CI: run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824) passed `openapi-spec-validator` for the embedded Chapter 06 OpenAPI 3.1 document; see the CI acceptance confirmation below.
- [x] At this checkpoint, local Mermaid rendering was blocked by package/network constraints. This was subsequently completed in CI: run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824) rendered all 29 diagrams to SVG and uploaded the artifact; see the CI acceptance confirmation below.
- [ ] This reference spot-check does not validate every external URL in all chapters or prove every claim is supported by its cited source. Complete the remaining claim-by-claim and inventory acceptance review before declaring technical acceptance.


## Curriculum-gap corrections — 2026-10-24

- [x] Chapter 05: added an explicit OSI/TCP-IP layered mental model, including how to assign failures to the responsible layer without assuming a one-to-one mapping; expanded global traffic-management and session-affinity trade-offs.
- [x] Chapter 18: added feature-flag rollout guidance covering separation of deploy from exposure, ownership/lifetime, safe defaults, testing both paths, authorization, and stale-flag removal.
- [x] Glossary: added definitions for feature flags, last-write-wins (LWW), point-in-time recovery (PITR), QUIC and event-time watermarks after comparing glossary entries with the mandatory inventory.
- [x] Rechecked changed files for balanced fenced blocks, Further reading placement where applicable, and navigation footer in the two edited chapters.
- [ ] The corrections address explicit curriculum/glossary omissions found during the independent pass, but do not close the full 21-family depth review or technical acceptance.


## Final verification checkpoint — 2026-10-24

This checkpoint separates checks supported by evidence from validation that could not be completed in the current environment.

- [x] Re-opened the live curriculum, coverage audit, progress tracker, editorial standard, and representative chapters for networking, distribution/consistency, replication/coordination, messaging/streams, scaling/overload, reliability/recovery, API design, and cloud delivery.
- [x] Confirmed that recent targeted content fixes are present in the live repository: OSI/TCP-IP and global traffic/session-affinity guidance in Chapter 05; feature-flag rollout guidance in Chapter 18; and feature flags, LWW, PITR, QUIC, and event-time watermarks in the glossary.
- [x] Confirmed that the coverage audit retains provisional statuses and explicitly documents outstanding acceptance work; no topic family was promoted to Deep without the required evidence.
- [x] Confirmed earlier recorded structural checks, targeted arithmetic checks, and Chapter 06 OpenAPI YAML checks are scoped as targeted checks rather than full standards validation.
- [ ] Full independent mechanism/example/trade-off/failure-mode review of all 21 curriculum families remains open.
- [ ] Repository-wide external-link liveness and claim-to-source audit remains open.
- [ ] Mermaid rendering remains unverified for all 29 chapter-page diagrams; package acquisition is blocked by the current environment's network/DNS restrictions. Static checks do not establish successful rendering.
- [ ] Full OpenAPI 3.1 validator/linter run remains unverified; package acquisition is blocked by the current environment's network/DNS restrictions. Targeted YAML checks do not establish full conformance.
- [ ] Final whole-book contradiction, duplication, terminology, and prerequisite review remains open.

**Closure decision:** The content-build/readability pass is in a review-ready state, but formal technical acceptance is not complete. Keep this distinction visible; do not describe the textbook as fully validated until the remaining checks are performed in an environment with the required validators and the full coverage/source reviews are completed.


## Inventory reconciliation — 2026-10-24

- [x] Re-fetched all 20 current chapter pages and counted Mermaid opening declarations directly from their Markdown content. The current total is **29 chapter-page Mermaid blocks** (16 across Chapters 01–10 and 13 across Chapters 11–20). This supersedes older checkpoint counts of 21/22; the diagrams have not been rendered.
- [x] Compared the Chapter 11 section headings with the coverage-audit row and found a stale reference to section 11.2A, which does not exist in the current chapter. Correct the audit mapping to the sections actually present.
- [ ] Mermaid rendering remains a blocker; declaration counts do not establish syntactic or visual validity.

- [x] Static diagram declaration check: reviewed all 29 Mermaid blocks in the 20 chapter pages. Each begins with a recognized flowchart or sequence-diagram declaration; rendering is still unverified.
- [x] Checked the numbered section endpoints listed in the 21-row mandatory inventory against current chapter headings. All referenced endpoints exist after correcting the stale Chapter 11 mapping. This validates the map, not the depth or technical accuracy of each section.



## Independent depth review and final structural recheck — 2026-10-24

- [x] Re-fetched all 20 current chapter pages and reviewed the chapter structure against the 21-family curriculum, with focused mechanism-level reads in storage-model selection, cache correctness/security, consistency/quorums, consensus/fencing/transactions, messaging/replay/schema evolution, IAM/injection/tenant isolation, Kubernetes/cloud delivery, and offline/realtime/WebRTC architecture.
- [x] Found and closed a specific depth gap in Chapter 09: hot keys were mentioned in checklists but lacked a standalone explanation of diagnosis and safe mitigation. Added a dedicated section distinguishing read-hotspot remedies from write-hotspot correctness, including local caches, coalescing, replication, safe partitioning, quotas/admission control, and a skew-focused validation test.
- [x] Added AWS caching best practices and OWASP Web Cache Security Cheat Sheet as further reading for cache stampedes/TTL behavior and shared-cache security/tenant isolation. The official pages were opened during this pass.
- [x] Re-ran the structural check across all 20 chapter pages, correctly accounting for both backtick and tilde Markdown fences: all fenced blocks are balanced; all exact headings are unique; each chapter has Further reading; navigation footer placement is correct; no instructional headings appear after Further reading.
- [x] Re-inventoried Mermaid blocks using both supported fence styles: **29 blocks** across the 20 chapter pages. All first non-comment lines use recognized Mermaid diagram declarations. This is a static syntax-screen only; no renderer result is claimed.
- [ ] Full independent mechanism/example/trade-off/failure-mode acceptance for each of the 21 mandatory topic families remains open. The focused review found and corrected a real gap, but a sampled/targeted read is not a substitute for a complete claim-by-claim review.
- [ ] Full external-link liveness and claim-to-source audit remains open. Newly added Chapter 09 sources were checked; that does not establish that every URL across the book resolves or supports the adjacent claim.
- [ ] Mermaid rendering and full OpenAPI 3.1 validation remain blocked by the current execution environment's package/network constraints. Static declarations and YAML parsing are not equivalent to those checks.
- [ ] Whole-book contradiction/prerequisite review remains open beyond the targeted consistency checks already recorded.

**Acceptance state:** Structural checks are passing and the identified Chapter 09 hot-key gap is closed. The textbook remains review-ready, not formally technically accepted, until the remaining source, renderer, schema and full-depth checks are completed.



## Reference-link availability pass — 2026-10-24

- [x] Re-opened all **74 unique URL destinations** in the current reference catalog through the web retrieval environment, including RFC Editor standards, primary papers, versioned Kafka/OpenAPI/SLSA specifications, PostgreSQL documentation, cloud-provider architecture guidance, Kubernetes, OpenTelemetry, OWASP, WCAG and CISA/NIST materials.
- [x] Reconfirmed the newly added Chapter 09 references: AWS Caching Best Practices and the OWASP Web Cache Security Cheat Sheet both resolve to the intended pages.
- [x] Followed up on two DOI URLs that the page reader could not fetch directly: search results confirmed the cited FLP consensus paper DOI (10.1145/3149.214121) and the O'Neil et al. LSM-tree paper DOI (10.1007/s002360050048). These are reader limitations, not evidence of dead links.
- [x] Confirmed the CISA 2026 SBOM bulletin URL resolves and describes the updated minimum-elements guidance. The generic CISA SBOM landing page returned HTTP 403 in the retrieval environment, so its availability cannot be confirmed by that direct fetch.
- [ ] This pass covers the reference catalog and the two new Chapter 09 URLs, not every external URL repeated or added within all chapter pages. Chapter-specific link liveness and claim-to-source alignment remain open.
- [ ] The link check establishes page availability and basic topical match for the sources inspected; it does not prove that every claim throughout the textbook is fully supported by its cited source.



## Cross-chapter consistency pass — 2026-10-24

- [x] Compare high-risk concept boundaries across Chapters 03/13/19 (capacity, replica-multiplied limits and retry/hedge amplification); Chapters 07/10/11 (isolation, distributed consistency, consensus, 2PC/saga and fencing); Chapters 09/16/20 (cache authorization, revocation, deletion and offline tombstones); Chapters 06/12/19 (idempotency, outbox/inbox, duplicate publication, schema compatibility and replay); and Chapters 14/18 (recovery objectives, failover, stale writers and progressive delivery compatibility).
- [x] Record the scoped findings and limitations in COVERAGE-AUDIT.md. Key terminology remains aligned across the inspected boundaries; this pass does not prove that no contradiction or duplication exists anywhere in the book.
- [x] Update the Chapter 09 inventory row to include the newly added hot-key section and a skewed-load validation requirement.
- [ ] Full chapter-by-chapter contradiction, prerequisite and residual-duplication review remains open; do not mark the 21-family inventory Deep on the basis of this focused pass.



## CI validation route added — 2026-10-24

- [x] Added `.github/workflows/system-design-validation.yml`, triggered by relevant pushes, pull requests and manual dispatch. It has separate jobs for OpenAPI validation and real Mermaid rendering.
- [x] Added `system-design-mastery/scripts/validate_artifacts.py` to extract the embedded OpenAPI 3.1 YAML and all Mermaid blocks from the 20 chapter pages. It enforces the expected counts (one OpenAPI document and 29 Mermaid diagrams) before tool validation.
- [x] Re-fetched both new files after commit and inspected their contents. The script's chapter-root path was corrected and re-fetched.
- [ ] **Not yet verified:** no completed GitHub Actions run result has been retrieved in this pass. Do not treat the workflow definition as proof that rendering or OpenAPI validation passed. Check the Actions run after GitHub executes it; investigate and fix any install, browser, renderer, schema or script errors.
- [ ] The validator checks the embedded OpenAPI example and Mermaid syntax/renderability, but does not replace full topic-depth or claim-to-source acceptance.


## Additional depth corrections — storage and Kafka guarantees — 2026-10-24

- [x] Chapter 08: added section 8.2A comparing wide-column, graph, time-series, inverted-index search, warehouse/lakehouse and relational choices by representative query shape, efficient access path, and failure/operational cost. Added a commerce example separating transactional authority from search, recommendation and analytics projections.
- [x] Chapter 12: added section 12.3A distinguishing Kafka idempotent producer behavior and Kafka transactional records/offsets from arbitrary external side effects. It includes the database-commit/offset-commit crash window, `read_committed` visibility, and a checklist for bounding exactly-once claims. The linked Kafka 4.3 delivery and transaction design documentation was opened.
- [x] Updated the coverage audit's storage and messaging rows to point to the new sections and to keep acceptance criteria explicit.
- [ ] The changes are not yet full acceptance for either topic family. Review them against representative workloads and deployed product contracts; keep statuses Developing until independent review is complete.
- [ ] The CI workflow is configured, but no completed GitHub Actions result has yet been verified in this session. Mermaid rendering and full OpenAPI 3.1 validation remain unconfirmed pending those results.


## All-chapter section map recheck — 2026-10-24

- [x] Re-fetched the current heading structure for all 20 chapters and reviewed the teaching sequence/section coverage for Chapters 01–07 and 13–19, alongside the previously focused mechanism-level review of Chapters 08–12 and 16/18/20.
- [x] Confirmed that the current chapters contain dedicated treatment for requirements and quality attributes, capacity testing, runtime/concurrency limits, networking layers, API semantics and gateways, relational isolation/sharding, scaling and overload, SLO/recovery rehearsal, architecture styles, IAM/threat modeling, metrics/cardinality/incident response, Kubernetes/IaC/supply chain, and cross-cutting fairness/pattern interactions.
- [x] Added two substantive gaps found during deeper reading: Chapter 08 specialized storage selection (8.2A) and Chapter 12 Kafka exactly-once boundary (12.3A). Rechecked the three changed chapter pages (08, 09, 12): no duplicate headings or unclosed fences; each retains Further reading and the navigation footer.
- [ ] This section-map pass is not an exhaustive sentence-by-sentence acceptance of all 21 families. The inventory remains Developing until examples, failure modes, source alignment and selection criteria have been independently confirmed for every row.
- [x] At this earlier checkpoint the helper only surfaced pull-request-triggered workflow runs; subsequent inspection of the Actions REST endpoint verified push run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824). Both OpenAPI validation and all 29 Mermaid renders passed. See the CI acceptance confirmation below.


## Focused client real-time depth correction — 2026-10-24

- [x] Reviewed Chapter 20's synchronization and durable real-time delivery sections at mechanism level.
- [x] Added a replay-to-live handoff subsection to Chapter 20.6: high-watermark/subscription-position requirements, overlap or buffering, deduplication, durable checkpoints, retention gaps and snapshot recovery.
- [x] Added concrete boundary tests for publishes during subscription setup, disconnects during replay, duplicate delivery, cursor expiry and a crash between applying an event and persisting the checkpoint.
- [x] Updated COVERAGE-AUDIT.md to record the correction and preserve the Developing status.
- [ ] Independently verify the exact handoff against a chosen broker/change-feed API and ordering contract; the generic design guidance does not establish product-specific guarantees.
- [ ] CI remains unverified: repository helper available in this session only returns pull-request-triggered runs; it returned no run for the workflow commit. A local clone attempt also failed because this environment could not resolve github.com. Do not claim the Mermaid renderer or full OpenAPI validator passed.


## Tracker and change verification — 2026-10-24

- [x] Re-fetched the updated Chapter 20, progress tracker, coverage audit, artifact extractor and CI workflow from the default branch after the latest commits.
- [x] Rechecked Chapter 20's changed page for duplicate headings, balanced fenced blocks, Further reading and navigation footer; these structural checks passed for that page.
- [x] Found and disambiguated a duplicate “Remaining acceptance blockers” heading in COVERAGE-AUDIT.md so Markdown section anchors are unique for that pair of sections.
- [ ] Repository-wide structural validation after the latest edits has not been rerun as a single automated suite. The CI workflow remains the intended route, but its completed run cannot be inspected through the available Actions helper in this session.
- [ ] Full acceptance remains open: no inventory family has been promoted to Deep; no claim-to-source audit or real Mermaid/OpenAPI validation is being represented as complete.


## CI validation results and renderer fix — 2026-10-24

- [x] Inspected GitHub Actions run [40103087271](https://github.com/kowlutla/System-Design/actions/runs/40103087271) from commit `f8e75f9e22a13dbcae5f60f69581ad76d81c7ccf`, including both jobs and the Mermaid job log.
- [x] Confirmed the extractor ran successfully and extracted exactly 29 Mermaid blocks and one OpenAPI 3.1 document.
- [x] Confirmed the `openapi-spec-validator` step completed successfully against the extracted OpenAPI document. This is a verified full validator run for that embedded specification, not a claim that every API design in the textbook has been audited.
- [x] Diagnosed the Mermaid job failure from its logs: Mermaid CLI installed, but Chromium failed to launch with `No usable sandbox`; rendering stopped on the first diagram and produced no rendered artifact.
- [x] Updated the workflow at commit `4d868540e7913b027acd3f43c58304586d80cb61` to pass Puppeteer a config enabling `--no-sandbox` and `--disable-setuid-sandbox`, and made the render artifact upload fail if no files are found.
- [x] Corrected run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824) subsequently completed successfully; see the **CI acceptance confirmation** entry below for exact job and artifact evidence.
- [ ] The full 21-family depth/source acceptance, whole-book contradiction review and all chapter-local source verification remain open; statuses must remain provisional.


## CI acceptance confirmation — 2026-10-24

- [x] Verified corrected GitHub Actions run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824): both jobs completed successfully.
- [x] OpenAPI job: extractor produced exactly one embedded OpenAPI 3.1 specification; `openapi-spec-validator` completed successfully.
- [x] Mermaid job: extracted 29 diagrams, rendered each to SVG after applying the Puppeteer no-sandbox configuration, verified the expected output count, and uploaded artifact [system-design-mermaid-rendered](https://github.com/kowlutla/System-Design/actions/runs/40104445824/artifacts/12563862191) containing 29 files.
- [x] Inspected the Mermaid job log; it names all 29 rendering inputs and confirms that 29 files were uploaded. This confirms renderer execution, not a human visual inspection of every resulting diagram.
- [ ] Full 21-family mechanism/example/trade-off/failure-mode and source acceptance remains open. No row is promoted to Deep.
- [ ] Whole-book contradiction/prerequisite/duplication review and exhaustive chapter-local claim-to-source audit remain open. The textbook is not yet formally accepted solely because structural/render/schema validation passed.


## Focused Kafka consumer correctness correction — 2026-10-24

- [x] Added a new mechanism-focused section to Chapter 12 on consumer-group rebalances, offset correctness, lag versus drain time, ownership revocation, bounded shutdown, durable-effect/offset crash windows, and tests for reassignment and uncertain commit responses.
- [x] Updated the mandatory messaging/data-movement audit row to reflect the new material and retain the explicit remaining verification work.
- [ ] The messaging family remains Developing: this addition is not evidence that all Kafka version/configuration claims, schema-registry choices, replay semantics, or external side-effect boundaries have passed independent source review.
- [ ] Continue the remaining 21-family depth/source review and whole-book consistency review; do not mark the textbook accepted on the strength of this focused correction.


## Focused security and cloud rollback corrections — 2026-10-24

- [x] Added Chapter 16 guidance distinguishing cached authorization decisions from cached HTTP responses, including decision-context dimensions, bounded revocation delay, invalidation failure, fail-open trade-offs, and targeted revocation/cache-path tests.
- [x] Cited OWASP Authorization and Web Cache Security Cheat Sheets for the new Chapter 16 material.
- [x] Added Chapter 18 guidance that Kubernetes Deployment rollback restores the Pod template and does not undo database migrations, emitted events, external side effects, or every related resource; cited official Kubernetes Deployment documentation.
- [x] Updated COVERAGE-AUDIT.md with both focused changes while retaining Developing statuses.
- [ ] Recheck changed chapters structurally and verify the latest CI result after these commits; the earlier green run predates these edits.
- [ ] Continue full 21-family depth review, whole-book contradiction/prerequisite/duplication review, and claim-to-source verification. These focused additions do not constitute final acceptance.


## Focused search-index safety correction — 2026-10-24

- [x] Added Chapter 08 section 8.3A on stale authorization attributes, tenant filtering before pagination, side channels through facets/counts/highlights/autocomplete, durable deletion/tombstone ordering, and safe snapshot-plus-stream index rebuild/cutover.
- [x] Updated COVERAGE-AUDIT.md to record the additional search-index depth while retaining Developing status.
- [ ] Verify the snapshot/CDC handoff and deletion semantics against the actual database, connector, and search product selected for any concrete design; this chapter intentionally states the generic mechanism, not vendor guarantees.
- [ ] Re-run the full repository validation workflow after the recent Chapter 08/16/18 edits; the last verified green run predates these commits and the current Actions helper does not expose push-triggered runs.


## Focused cache correctness correction — 2026-10-24

- [x] Added a worked tenant-safe cache-key and authorization-revocation scenario to Chapter 09, including representation dimensions, current-policy enforcement, invalidation loss, and CDN/proxy/pagination/ETag test cases.
- [x] Updated COVERAGE-AUDIT.md to record the scenario while retaining Developing status.
- [ ] Validate cache behavior against the chosen CDN/proxy/cache product and execute skewed-load, invalidation-loss and cross-tenant tests in a representative environment.
- [ ] Continue the 21-family acceptance review; current changes are focused corrections, not full-book sign-off.


## Repository-wide chapter structure recheck — 2026-10-24

- [x] Re-fetched all 20 current chapter pages from the default branch after the latest edits.
- [x] Checked every chapter for balanced fenced-code markers, duplicate heading text, and the expected navigation footer. All 20 pages passed these specific structural checks.
- [ ] This is not a Markdown renderer, link resolver, Mermaid renderer, or technical claim audit; those checks remain distinct. The prior green OpenAPI/Mermaid workflow predates the latest content commits, and a post-edit workflow run has not been verified.


## Textbook v1 closure checkpoint — 2026-10-24

- [x] Froze the current 20-chapter conceptual HLD textbook scope; no further broad expansion is planned for this phase.
- [x] Recorded the closure decision and verification boundaries in COVERAGE-AUDIT.md.
- [x] Confirmed the latest fetched versions of all 20 chapter pages passed the scoped structural checks (balanced fences, unique heading text, expected navigation footer).
- [x] Preserved the verified historical CI evidence: run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824) passed OpenAPI validation and rendered 29 Mermaid diagrams.
- [ ] **Post-edit CI is not verified.** The successful run predates the latest chapter edits; do not imply those changes were validated by that run.
- [ ] Full 21-family source/depth acceptance and exhaustive link/claim audit are not complete. Inventory statuses remain Developing/provisional.

**Stopping rule:** Treat the textbook content as v1-complete for learning use, with technical acceptance explicitly provisional. Reopen only for a concrete defect or missing prerequisite. Interview Q&A and end-to-end case studies remain separate future phases.

## Finalization audit — 2026-10-28

A fresh recursive Git tree inspection was performed against the repository's published `main` head (commit `9d2a8dc3f7bf136a113a1517c24761fff8546f6c`). The tree response was complete (not truncated).

- [x] Confirm the scope boundary: all changes for this work remain limited to `system-design-mastery/`; `tutorials/`, `real-world-examples/` and other root paths are outside the cleanup scope.
- [x] Inventory all 52 entries under `system-design-mastery/`: 28 Markdown files (20 chapter `README.md` pages and eight intentional landing/planning/reference pages) plus the existing validation script.
- [x] Review the complete Markdown path inventory for extra lesson fragments, duplicate chapter pages, empty-looking planning-file names, or misplaced Markdown files. No unexpected Markdown paths were found; **no Markdown deletion is justified** by the tree audit.
- [x] Confirm that the chapter structure remains one canonical Markdown page per chapter and that the index lists Chapters 01–20.
- [ ] Do not mark whole-book technical acceptance complete based on this structural inventory. The existing 21-family matrix remains Developing/provisional until every family passes its mechanism, example, selection, trade-off, failure-mode and source-alignment criteria.
- [ ] Run post-edit validation after substantive chapter changes: the known successful Mermaid/OpenAPI workflow run predates later content edits and is historical evidence only.
- [ ] Finish complete local-link resolution and claim-to-source review, including Chapter 20 and any chapter-only URLs. No exhaustive link-liveness or claim-by-claim source pass is claimed by this tree audit.

**Decision:** the current file structure is already clean and appropriately consolidated. Preserve the eight support pages because they serve distinct navigation, learning-sequence, terminology, source, editorial, coverage, and status purposes. Do not delete files merely to reduce the count. The remaining work is verification and any concrete correctness corrections discovered by it—not further structural reorganization.

## Targeted capacity-estimation correction — 2026-10-28

A targeted read of Chapter 03 found that capacity estimation covered average/peak rates, storage, bandwidth and cache sizing, but did not explicitly connect DAU to backend request volume. Added a worked section that converts DAU × actions/user/day × requests/action into daily requests, active-period average RPS, assumed peak RPS, read/write rates, response bandwidth and retained raw storage. The example states its assumptions and distinguishes estimates from measured capacity. Arithmetic was checked: 60 million requests/day over 10 hours is about 1,667 RPS; a 3× peak is about 5,000 RPS; 12 KiB × 5,000 is about 59 MiB/s; and one million 2 KiB records/day is about 2 GiB/day before overhead.

- [x] Add explicit DAU-to-RPS, fan-out, read/write split, bandwidth and retention calculations to Chapter 03.
- [ ] Run the post-edit artifact validation workflow and check relative links after all changes.
