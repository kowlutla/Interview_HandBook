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
