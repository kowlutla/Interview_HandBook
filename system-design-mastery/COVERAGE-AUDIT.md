# System Design Mastery — Curriculum Coverage Audit

Status definitions:
- **Missing** — no meaningful explanation found in the current chapter.
- **Mentioned** — named or briefly described; not enough to teach design decisions.
- **Developing** — a substantive explanation exists, but depth, examples, edge cases, or verification remain.
- **Deep** — mechanisms, variants, selection criteria, trade-offs, failure modes, security/operations where relevant, diagrams, and worked reasoning have been reviewed.

Do not infer “Deep” from a heading or keyword match. This is an initial audit based on chapter structure and targeted content inspection; statuses must be upgraded only after reading and validating the relevant sections.

## Initial coverage map

| Topic family | Primary chapter(s) | Initial status | Gap to close |
|---|---|---|---|
| Systems thinking, boundaries, architecture decisions | 01 — 1.15 Architecture views, 1.16 worked architecture evaluation | Developing | Section 1.16 compares modular monolith, microservices and serverless against an invariant, team constraints, workload assumptions and explicit revisit triggers. Validate the scenario's assumptions and check consistency with later architecture-style guidance. |
| Requirements and quality attributes | 02 — 2.1–2.18, including 2.15 quality scenarios, 2.16 accessibility/usability/internationalization, 2.17 operability/portability/cost/sustainability, and 2.18 quality-attribute interactions | Developing | The expanded quality-scenario table now pairs observable criteria with verification evidence and accountable roles for accessibility, operability, portability, cost and sustainability. Still validate standard-specific claims and add project-specific numerical targets during real design work. |
| Workload estimation and capacity | 03 — 3.17 test methodology, 3.18 worked capacity test plan | Developing | Section 3.18 adds an illustrative workload mix, explicit latency/error/queue criteria, ramp/steady/spike/failure/soak sequence, and evidence to preserve. Validate thresholds against an actual product SLO and run the plan in a representative environment. |
| Execution, concurrency, runtime resources | 04 — 4.1–4.15, 4.16 cancellation/structured concurrency, 4.17 deadline-propagation scenario | Developing | Section 4.17 traces required and optional fan-out work under a shared deadline and distinguishes best-effort cancellation from durable jobs and unknown side-effect outcomes. Still verify runtime-specific API caveats and thread/task/pool limits. |
| Network fundamentals: IP, routing, TCP/UDP, DNS, TLS, HTTP | 05 — sections 5.1–5.11 | Developing | Section 5.10 consolidates symptom/evidence-based troubleshooting and common failure hypotheses; section 5.11 provides a concise architecture review checklist. Still verify protocol details against cited RFCs and test the troubleshooting guidance against real traces or a lab. |
| Load balancing, reverse proxies, ingress, global traffic management | 05 — 5.7; 13 — Load balancing and consistent hashing, 13.1B; 18 — Cloud primitives | Developing | Dedicated mechanism-level coverage: L4/L7, algorithms, health, draining, affinity, locality, TLS, failure modes, metrics. |
| CDN, edge delivery, origin shielding and invalidation | 05 — 5.7; 09 — Local, distributed and CDN caches, 9.1F, 9.1G | Developing | Dedicated edge-cache behavior, cache-key correctness, stale content, purge, origin failover, security and cost. |
| API gateways and API management | 06 — 6.11 API gateways and API management | Developing | Dedicated gateway responsibilities, limits, auth boundary, routing, transformation, high availability and failure policy. |
| API styles, contracts, retries, idempotency, streaming | 06 — includes 6.13 worked OpenAPI evolution | Developing | Section 6.13 demonstrates an OpenAPI response contract, additive-field rollout, breaking-change risks, consumer/provider contract tests and deprecation gates. Still validate syntax with a real OpenAPI linter and check client-specific compatibility behavior. |
| Architectural styles and patterns | 01, 15, 19 | Developing | A systematic comparison of layered/N-tier, client-server, modular monolith, SOA, microservices, event-driven, hexagonal, pipe/filter, serverless, CQRS/event sourcing and hybrids. |
| Relational modeling, SQL, indexes, transactions | 07 — includes 7.2 sharding/resharding and 7.3 worked write-skew lab | Developing | Section 7.3 traces concurrent transactions that each pass a local check but violate a global invariant, compares protection strategies, and defines a retry/test matrix. Continue validating isolation/query-plan examples and database-specific guarantees. |
| NoSQL models, search, analytics, data lakes | 08, 19 | Developing | Chapter 08, section 8.7's comparative access-pattern example distinguishes transactional records, derived search indexes, object assets, analytical datasets and caches, with authority/freshness/rebuild caveats. Verify product-specific guarantees and test the chosen architecture's recovery paths. |
| Storage engines, WAL, B-tree, LSM, compaction | 08 | Developing | Add recovery/write-path examples and compare amplification and workload implications. |
| Caching at client, CDN, application and data layers | 09 — 9.1A–9.1H, 9.2, 9.3 cache security/tenant isolation/freshness | Developing | Verify HTTP cache directives and provider-specific behavior; add a worked cache-key and invalidation scenario across user/tenant boundaries. |
| Distributed failure, consistency, clocks, CAP/PACELC | 10 | Developing | Section 10.18 now adds a write-timeout/read-replica timeline and explains why quorum arithmetic alone does not prove linearizability. Verify the consistency claims against primary literature and implementation contracts. |
| Replication, consensus, leases, locks, fencing, transactions | 11 — includes 11.6 worked stale-lease/fencing timeline | Developing | Section 11.6 traces a paused lease holder resuming after takeover and explains why the protected resource must atomically enforce monotonically increasing fencing tokens. Continue verifying protocol-specific recovery and consensus claims. |
| Queues, pub/sub, logs, Kafka, CDC and stream processing | 12 — 12.1–12.8, including delivery semantics, idempotency, outbox/inbox/CDC, stream processing, schema evolution, CQRS/event sourcing and projection rebuilds | Developing | Section 12.3 explains duplicate/lost-effect crash windows and scopes exactly-once claims; section 12.5 covers outbox/inbox/CDC; sections 12.7–12.8 cover schema evolution, projection rebuilds and event-data privacy. Verify compatibility assumptions against a chosen serialization format and registry. |
| Scaling, hashing, partitioning, hotspots, overload | 13 — 13.1A–13.1G, 13.2, 13.3 hedged requests/adaptive concurrency, 13.4 worked concurrency-limit decision | Developing | Section 13.4 compares illustrative throughput, p99, error and queue behavior across concurrency levels and derives a candidate limit below the observed knee. Validate with real workload data and test adaptive feedback stability. |
| Reliability, SLOs, redundancy, backup/restore, DR | 14 — includes 14.2–14.4 recovery engineering and rehearsal | Developing | Section 14.4 adds a timed restore/replay/cutover rehearsal with explicit RTO/RPO arithmetic, stale-writer fencing, data validation, dependency readiness and backlog drain. Continue checking recovery assumptions and testability. |
| Security, identity, privacy, tenant isolation | 16 — 16.1A–16.1J, 16.2 threat modeling, 16.3 API threats, 16.4 worked tenant-scoped export threat model | Developing | Section 16.4 maps trust boundaries and abuse cases across API, queue, worker, database, object storage and operations, with permission-revocation and negative-test cases. Verify controls against OWASP API-security and injection-prevention guidance and actual platform policies. |
| Observability and production operations | 17 — including 17.2 practical observability and 17.3 worked SLO alert design | Developing | Section 17.3 now derives a request-based error budget and burn-rate example, then maps signals to response policies and validation steps. Still verify alert behavior against historical traffic/incidents and review sampling/cardinality trade-offs across the full chapter. |
| Cloud, containers, Kubernetes, IaC and delivery | 18 | Developing | Sections 18.1F and 18.2–18.5 now cover CI/CD lifecycle and pipeline trust boundaries, Kubernetes, service mesh, IaC state/drift, SBOM, provenance, signing and build/deployment trust. Still verify supply-chain guidance against primary standards and test examples. |
| Cross-cutting patterns, cost, multi-tenancy and multi-region | 19 — 19.1A–19.1F, 19.2 pattern catalog, 19.3 worked multi-tenant fairness scenario, 19.4 pattern interactions | Developing | Section 19.3 tests tenant-aware admission, replica-multiplied local limits, reserved capacity and noisy-neighbor behavior; 19.4 maps interactions among retries, hedging, breakers, scaling, caches, replicas, outbox/inbox, failover and replay. Verify approximation assumptions and validate combinations against chapter guarantees. |
| Client-side, offline-first, and real-time architecture | 20 — sections 20.1–20.13, including new replay-to-live handoff guidance in 20.6 | Developing | Section 20.6 now explains the replay/subscription race, overlap or buffering, deduplication, durable checkpoints, retention gaps and snapshot recovery. Independently validate the protocol against a concrete event source and test disconnect/replay boundary cases; verify WebRTC topology/security and real rendering. |


## Mandatory inventory: row-by-row provisional mapping

This table mirrors the 21 topic-family rows in `CURRICULUM.md`. The status is deliberately provisional: exact section presence is mapped, but each row still needs independent depth and technical review before it can be called Deep.

| Inventory row | Exact teaching locations | Provisional status | What remains before acceptance |
|---|---|---|---|
| Architecture foundations | Ch. 01: 1.1–1.16, especially 1.14 cohesion/coupling/separation of concerns, 1.15 logical versus physical architecture views, and 1.16 worked evaluation | Developing | Verify terminology and viewpoint taxonomy; check that the worked decision's assumptions and revisit triggers align with Chapter 15. |
| Requirements and quality | Ch. 02: 2.1–2.18, especially 2.15 quality scenarios, 2.16 accessibility/usability/internationalization, 2.17 operability/cost/sustainability attributes, and 2.18 interactions | Developing | Validate measurement examples and standards-specific accessibility/security claims; check that every quality attribute has a meaningful test method and owner. |
| Capacity and performance | Ch. 03: 3.1–3.18, including explicit binary powers-of-two unit conversions and especially 3.16 worked estimate, 3.17 test methodology, 3.18 acceptance plan | Developing | Recheck all arithmetic and unit conversions; verify workload assumptions, open/closed-loop testing distinctions, and illustrative thresholds. |
| Runtime and execution | Ch. 04: 4.1–4.17, especially 4.15 runtime limits, 4.16 cancellation/structured concurrency, 4.17 deadline scenario | Developing | Check runtime-specific caveats, shutdown semantics, cancellation propagation, and interactions among thread/task, connection, and worker pools. |
| Network fundamentals | Ch. 05: 5.1–5.11 | Developing | Verify protocol claims against RFCs, particularly DNS security, TLS/mTLS, QUIC/HTTP/3, IPv6, flow/congestion control, and troubleshooting evidence. |
| Traffic entry and delivery | Ch. 05: 5.7–5.8; Ch. 06: 6.11; Ch. 18: 18.2–18.3 | Developing | Check differences among L4/L7 balancers, reverse proxies, gateways, ingress, CDN and global routing; verify provider-specific claims and failure behavior. |
| API and service communication | Ch. 06: 6.1–6.13, especially 6.10A–6.10H, 6.11 gateways, 6.12 webhooks, 6.13 OpenAPI evolution | Developing | Run a dedicated OpenAPI validator; verify HTTP status/conditional-request semantics, retry safety, schema compatibility, webhook SSRF/signature/replay protections, and streaming reconnect behavior. |
| Architecture styles | Ch. 01: 1.6, 1.14–1.16; Ch. 15: 15.1A–15.1I (including anti-corruption-layer decisions and the architecture-style comparison); Ch. 19: 19.2 | Developing | Compare all listed styles with consistent decision criteria and ensure the costs and prerequisites are concrete rather than labels-only. |
| Databases and transactions | Ch. 07: 7.1A–7.1L, relational practice section, 7.2 sharding/resharding, 7.3 write-skew lab | Developing | Verify isolation claims against named database implementations; test migration/resharding steps, retry behavior, query-plan interpretation, backup/PITR and replica-lag caveats. |
| Storage and search | Ch. 08: 8.1A–8.1I, new 8.2A specialized-system selection, and 8.2–8.7 | Developing | Verify query-shaped comparisons for graph, wide-column, time-series, inverted-index and lakehouse systems against real workloads; review B-tree/LSM, WAL/checkpoint, compaction/amplification and object/block/file recovery behavior. |
| Caching and locality | Ch. 09: 9.1A–9.1H, new 9.1C.1 hot-key treatment, 9.2, 9.3 (cache layers, invalidation, HTTP behavior, failure modes and tenant isolation); database buffer/page cache distinction added alongside application and edge caches | Developing | Validate the new hot-key section against a skewed-load test; check eviction/admission, negative caching, invalidation races, HTTP/CDN directive behavior, cache poisoning, tenant isolation and revocation/deletion propagation. |
| Distributed systems | Ch. 10: 10.7–10.18 | Developing | Verify consistency definitions and CAP/PACELC wording against primary literature; test quorum assumptions, failure-detector limits, clock uncertainty, CRDT invariants and multi-region failover claims. |
| Coordination and distributed transactions | Ch. 11: 11.1A–11.1C, 11.5A–11.5I, 11.6 | Developing | Verify Raft/Paxos and membership-change summaries against primary sources; make 2PC blocking/recovery assumptions, fencing enforcement and saga compensation boundaries explicit. |
| Messaging and data movement | Ch. 12: 12.1–12.8, including new 12.3A Kafka exactly-once boundary | Developing | Validate idempotent producer and transaction claims against deployed Kafka/client settings; keep external database/payment/email effects separate from broker transaction guarantees; choose a concrete serialization/registry compatibility model and verify replay, watermarks, retention and projection cutover assumptions. |
| Scaling and traffic management | Ch. 13: 13.1A–13.1G, 13.2–13.4; Ch. 19: 19.3 | Developing | Recalculate examples and validate the concurrency-knee assumptions; review autoscaling feedback delay, aggregate per-replica limits, consistent hashing/skew, hedge amplification and overload priorities. |
| Reliability and recovery | Ch. 14: 14.1A–14.1G, 14.2–14.4 | Developing | Recheck availability math and SLO/error-budget calculations; validate RTO/RPO definitions, backup/restore evidence, failback fencing, chaos-test safety and incident-response roles. |
| Security and privacy | Ch. 16: 16.1A–16.1J (including IAM lifecycle), 16.2–16.4, including the API injection guidance in 16.3 | Developing | Verify threat/control mappings against primary security guidance; expand any missing implementation examples for IAM, key rotation, encryption at rest, injection, browser/session threats and data deletion. |
| Observability and operations | Ch. 17: 17.1A–17.1J (including synthetic checks, deployment markers and incident command), 17.2–17.3 | Developing | Recheck SLI/error-budget arithmetic and alert windows; verify cardinality/sampling trade-offs, synthetic checks, incident command, deployment markers, ownership and postmortem guidance. |
| Cloud and delivery | Ch. 18: Delivery strategies; 18.1A–18.1I, 18.2–18.5 | Developing | Verify cloud responsibility models and Kubernetes behavior against current official docs; validate CI/CD, progressive delivery, IaC state/drift, cost/quota and supply-chain standards claims. |
| Cross-cutting patterns | Ch. 19: 19.1A–19.1F, 19.2 (including idempotent receiver), 19.3–19.4; cross-links to Chapters 06, 09, 11–15 | Developing | Audit each pattern's intent, preconditions and failure modes; check cross-pattern combinations, scheduler correctness, claim-check/materialized-view behavior, multi-tenancy and cost/complexity reasoning. |
| Client-side and real-time architecture | Ch. 20: 20.1–20.13 | Developing | Verify rendering trade-offs, local durability and synchronization guarantees, conflict strategies, transport/replay boundaries, WebRTC topology/security, and client-side operational metrics against primary sources and realistic failure scenarios. |

## Exact section map for the current expansion pass

The following sections are present and are the starting points for the deeper review. “Present” does not mean technically verified or complete.

| Area | Exact chapter section(s) to review |
|---|---|
| Architecture reasoning | Chapter 01: 1.4, 1.6, 1.7, 1.9, 1.13, 1.14, 1.15 architecture views and diagram selection, 1.16 worked architecture evaluation |
| Measurable quality attributes | Chapter 02: 2.5–2.12 and 2.15–2.18, including accessibility, usability, internationalization, operability, portability, cost, sustainability and attribute interactions |
| Workload and capacity | Chapter 03: 3.1–3.15, 3.16 worked capacity example, 3.17 testing methodology, 3.18 worked capacity test plan |
| Runtime and resource limits | Chapter 04: 4.1–4.14, 4.15 Runtime resource limits, 4.16 Cancellation and structured concurrency, 4.17 worked cancellation scenario |
| Networking and request path | Chapter 05: 5.1–5.11, covering the request path, network protocols, traffic entry, security boundaries, timeouts and evidence-led troubleshooting |
| API contracts and gateway | Chapter 06: 6.1–6.10H, 6.11 API gateways and API management, 6.12 Webhooks, 6.13 worked OpenAPI evolution |
| Relational data and transactions | Chapter 07: Isolation anomalies, Optimistic versus pessimistic concurrency, Query planning, Safe schema migration, Relational systems in practice, 7.2 Sharding and resharding, 7.3 Write-skew concurrency lab |
| Storage families and engines | Chapter 08: B-trees and LSM trees, 8.1A–8.1I, 8.2–8.6 data-system families/search/analytics/indexes, 8.7 Distributed file systems and object/block/file interfaces plus comparative access-pattern example |
| Cache behavior | Chapter 09: Common patterns, TTL and invalidation, Failure modes, 9.1A–9.1H, 9.2 Cache patterns and failure modes, 9.3 Cache security/tenant isolation/freshness |
| Distributed consistency | Chapter 10: Consistency models, CAP and PACELC, 10.7–10.18 including worked consistency timeline |
| Replication and coordination | Chapter 11: Leader election, Leases and fencing tokens, Two-phase commit, Sagas and compensation, 11.5A–11.5I, 11.6 Worked stale-lease/fencing timeline |
| Messaging and stream processing | Chapter 12: sections 12.1–12.8, covering messaging models, partitioning, delivery/idempotency, retries/backpressure, outbox/inbox/CDC, stream processing, schema evolution, event sourcing/CQRS, projection rebuilds and privacy |
| Scaling and overload | Chapter 13: Load balancing and consistent hashing, Overload controls, 13.1A–13.1G, 13.2 Admission control/load shedding/backpressure, 13.3 Hedged requests/adaptive concurrency, 13.4 worked concurrency-limit decision |
| Reliability and recovery | Chapter 14: SLI, SLO, SLA and error budget, Recovery objectives, Zones, regions and disaster recovery, 14.1A–14.1G, 14.2 Recovery engineering, 14.3 worked SLO/error-budget example, 14.4 recovery rehearsal |
| Architectural styles and evolution | Chapter 15: Monolith, modular monolith and microservices, Sidecars and service meshes, 15.1A–15.1H, 15.1I Architectural styles |
| Security and privacy | Chapter 16: Threat modeling, Authorization models, Tenant isolation, OAuth 2.0 and OpenID Connect, 16.2 Threat modeling a system architecture, 16.3 API threat patterns, 16.4 tenant-scoped export threat model |
| Observability and operations | Chapter 17: RED and USE, Percentiles and cardinality, SLO-driven alerting, 17.1A–17.1I, 17.2 Observability in practice, 17.3 worked SLO alert design |
| Cloud and Kubernetes | Chapter 18: Containers and Kubernetes, 18.1A–18.1I, 18.2 Kubernetes architecture, 18.3 Service mesh, 18.4 IaC state and drift, 18.5 software supply-chain security |
| Client-side and real-time architecture | Chapter 20: 20.1–20.13 — rendering/delivery, state ownership, offline persistence, synchronization/conflicts, real-time transport, WebRTC, collaboration, micro-frontends, interactive sessions, security and operations |
| Patterns and anti-patterns | Chapter 19: Probabilistic data structures including Bloom-filter sizing, Distributed scheduling, Multi-tenancy, Multi-region consistency and routing, 19.2 Architecture pattern catalog, 19.3 worked multi-tenant fairness scenario, 19.4 pattern interactions |

## New additions in the current review pass
| Tail latency and duplicate work | Chapter 13, 13.3 | Explains hedged requests, cancellation, idempotency, shared bottlenecks and adaptive concurrency feedback | Validate against The Tail at Scale and verify workload-specific trade-offs |
| API threat patterns | Chapter 16, 16.3 | Adds object/function/property-level authorization, sensitive business flows, resource abuse, SSRF, unsafe upstream APIs and API inventory | Build a threat model and verify controls against the OWASP API Security Top 10 |
| Probabilistic structure sizing | Chapter 19, Bloom filter sizing subsection | Adds standard approximate false-positive and bit-budget formulas plus a million-item worked example | Independently recalculate formula and label assumptions clearly |
| Cache security and data lifecycle | Chapter 09, 9.3 | Covers tenant-aware cache keys, cache poisoning/deception, stale-serving, permission revocation and deletion; a cross-tenant/cache-poisoning test matrix now specifies scenarios and expected outcomes | Verify against HTTP caching semantics and execute the matrix against the actual proxy/cache configuration |
| Event sourcing, CQRS and schema governance | Chapter 12, 12.7 | Distinguishes commands/events, event sourcing/notification, CQRS/read-model lag, projection rebuild/cutover, schema-change risk and event-data privacy | Verify the schema risk matrix against a chosen serialization format/registry and test the rebuild protocol under live traffic |

| Addition | Location | Why it matters | Remaining verification |
|---|---|---|---|
| Architecture viewpoints and diagram selection | Chapter 01, 1.15 | Separates context, logical structure, runtime behavior, deployment, data ownership and trust boundaries instead of relying on one overloaded diagram | Validate diagram terminology and review the logical-versus-deployment example |
| Accessibility, usability and internationalization | Chapter 02, 2.16 | Makes critical user journeys, assistive technology, locale/time handling and accessible error behavior explicit quality attributes | Confirm conformance language against WCAG 2.2 and define project-specific targets |
| Operability, portability, cost and sustainability | Chapter 02, 2.17–2.18 | Adds lifecycle qualities and explains interactions between performance, cost, retention, resilience and environmental impact | Provider guidance is illustrative; validate measurable targets and avoid implying a single universal sustainability metric |
| Load, stress, spike, soak and scalability testing | Chapter 03, 3.17 | Connects estimates to reproducible evidence and explains open-loop/closed-loop traffic and coordinated omission | Review benchmark method and ensure a future worked test plan is concrete |
| Cancellation and structured task lifetime | Chapter 04, 4.16 | Distinguishes timeout from cancellation, rollback, and durable background work; covers deadline propagation and orphaned work | Verify runtime-specific examples and clearly label version-specific APIs |

## High-priority remaining verification risks

The recent expansions address several previously identified content gaps. The remaining work is now primarily evidence-backed verification and ensuring that the examples' assumptions are explicit:

1. **Claim-by-claim technical review:** check protocol, consistency, recovery, security and runtime claims against primary standards, papers or official documentation. Keep product-specific behavior clearly labeled.
2. **Schema compatibility:** verify the Chapter 12 change matrix against one selected serialization format and schema registry; compatibility labels and behavior vary by tooling and format.
3. **Executable document validation:** run the Chapter 6 OpenAPI excerpt through a real parser/linter and validate every Mermaid block with a renderer. These checks have not been performed yet.
4. **Source-link audit:** validate every external reference, replace stale or redirected links where needed, and confirm the source supports the adjacent claim.
5. **Cross-chapter consistency:** review shared terminology and guarantees for retries, idempotency, timeouts, consistency/isolation, event delivery, RTO/RPO, tenant scope and architecture views.
6. **Worked-example evidence:** recalculate arithmetic and inspect reasoning; where an example uses illustrative performance numbers or thresholds, label them as examples and do not imply they are measured production results.
7. **Mandatory inventory closure:** independently verify each mapped inventory row and upgrade a status to Deep only after mechanisms, variants, selection criteria, failure modes, security/operations, examples and sources have actually been reviewed.

Do not treat a section's presence as evidence that these checks are complete.

## Review rules

- A topic may have one primary home and several cross-links; avoid repeating the same textbook section in multiple chapters.
- Use standards and primary papers for protocol/theory claims, and official product documentation only for implementation-specific behavior.
- For every major component, teach purpose, internal mechanism, variants, selection criteria, trade-offs, failure modes, security, observability, scaling, and interactions.
- Add a diagram when it clarifies sequence, topology, state ownership, or failure behavior.
- Do not mark the textbook complete until every mandatory inventory row has an evidence-backed coverage status and technical verification.

## Targeted technical and source checks completed

These checks validate specific claims or source destinations; they do not constitute a full chapter-by-chapter technical sign-off.

| Area | Evidence checked | Result and remaining boundary |
|---|---|---|
| Distributed consistency and causal clocks | Gilbert and Lynch [CAP paper](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf) and Lamport [Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) | Supports the formal CAP framing and the distinction between Lamport-clock order and causality. A full review of every consistency-model example and multi-region implementation caveat remains open. |
| Relational isolation and write skew | PostgreSQL [transaction isolation documentation](https://www.postgresql.org/docs/current/transaction-iso.html) | Supports the distinction between snapshot-style repeatable-read behavior and serializable protection against serialization anomalies. Engine-specific guarantees and retry behavior still need to be stated when examples name a database. |
| Messaging delivery guarantees | Versioned Apache Kafka 4.3 [design documentation](https://kafka.apache.org/43/design/design/) and [message delivery semantics](https://kafka.apache.org/43/design/design/#message-delivery-semantics) | Sources are versioned and reinforce that delivery guarantees depend on producer, broker and consumer boundaries. The textbook avoids treating broker transactions as automatic exactly-once effects in arbitrary external databases. |
| Injection prevention | OWASP [Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) and [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) Cheat Sheets | The Chapter 16 addition covers parameterized queries, allow-listed query identifiers, safe command invocation and context-aware output handling. It is architectural guidance, not an exhaustive secure-coding manual. |
| Software supply-chain provenance | Approved [SLSA v1.2 specification](https://slsa.dev/spec/v1.2/) and versioned build-provenance pages | References use approved v1.2 destinations rather than retired v1.0 pages. Verify requirements against the selected build platform and standard version. |
| Observability signals and context propagation | Official [OpenTelemetry documentation](https://opentelemetry.io/docs/) | The official documentation exposes the core signals, context propagation and sampling topics used by Chapter 17. SDK/exporter behavior and instrumentation details still depend on the language and deployment. |
| CI/CD pipeline security | OWASP [CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html) | Supports treating build/deployment automation as privileged infrastructure and protecting credentials, source control, build execution, artifact integrity and monitoring. Tool-specific hardening still depends on the selected CI/CD platform. |
| SPDX version references | Official [SPDX specifications index](https://spdx.dev/use/specifications/) and [specification source](https://spdx.github.io/spdx-spec/) | The published index and source redirect present version information differently, so the catalog now avoids an overly specific version claim. Check the version required by the SBOM toolchain. |
| OpenAPI example | Official [OpenAPI 3.1.0 specification](https://spec.openapis.org/oas/v3.1.0.html); YAML parsed with PyYAML and key fields manually checked | Syntax and selected contract fields were checked. A dedicated OpenAPI parser/linter and generated-client compatibility test remain open. |
| Secure software development guidance | NIST [SP 800-218 final publication page](https://csrc.nist.gov/pubs/sp/800/218/final) | The catalog identifies v1.1 as a final publication and notes that later revision/draft status should be checked; do not silently treat a draft as final. |
| Coordination and distributed transactions | Official [Raft resources](https://raft.github.io/) and the Raft paper landing page; Chapter 11 sections 11.1A–11.6 | The chapter distinguishes leader election from replicated-state-machine safety, describes durable protocol state and quorum membership as assumptions, and states that stale-owner protection requires resource-enforced fencing. Its 2PC discussion distinguishes atomic commit from non-blocking recovery; saga compensation is described as a new business action rather than a perfect inverse. Implementation-specific membership-change and failure-recovery behavior still needs checking against the chosen consensus/transaction implementation. |
| Messaging crash windows and exactly-once scope | Versioned [Kafka 4.3 design docs](https://kafka.apache.org/43/design/design/) and [delivery semantics](https://kafka.apache.org/43/design/design/#message-delivery-semantics); Chapter 12 sections 12.1–12.8 | The textbook's offset-before-effect versus effect-before-offset timelines match the documented failure boundaries, and it does not extend Kafka's internal transaction guarantee to arbitrary external side effects. Validate the schema-compatibility matrix against a concrete serialization format/registry and the target connector/sink. | The Chapter 12 projection-rebuild procedure was clarified to capture a per-partition high-watermark/cutover boundary before historical replay, separating replayed history from events arriving during the rebuild.
| Recovery objectives and availability arithmetic | Chapter 14 sections 14.2–14.4; dependency composition and RTO/RPO definitions inspected | The illustrative dependency calculation is arithmetically consistent (0.999³ ≈ 0.997); the worked recovery timeline distinguishes time to service restoration from the recovered data point and conditions both conclusions on explicit measurement boundaries. The assumptions remain illustrative and must be replaced with service-specific failure scenarios and evidence. |
| Scaling and architecture-style trade-offs | Chapters 13–15 sections 13.2–13.4 and 15.1A–15.1I | The reviewed guidance consistently treats retries/hedges as load amplification, notes that cancellation may not stop remote work, and treats autoscaling as delayed feedback. The style comparison avoids presenting microservices, serverless, CQRS or event sourcing as universally superior. Validate thresholds and operational choices with workload-specific measurements. |
| Cache security and derived-data lifecycle | Chapter 09 section 9.3; RFC 5861 and HTTP caching references in the source catalog | The chapter treats cache keys as response/authorization contracts, avoids raw bearer tokens in keys, distinguishes bounded stale-serving from immediate revocation, and covers deletion across derived copies. The test matrix includes cross-tenant collisions, role variation, poisoning, revocation and stale-fill races. Run these tests against the actual CDN/proxy/cache configuration; HTTP directive behavior can differ by cache implementation. |
| API security and asynchronous authorization | OWASP [API Security Top 10 (2023)](https://api-security.owasp.org/editions/2023/en/0x00-header/) and Chapter 16 sections 16.3–16.4 | The worked export threat model rechecks authorization at asynchronous execution time, treats queue messages and internal networks as untrusted boundaries, and includes object/property/function authorization, SSRF, business-flow abuse and resource exhaustion. Validate each control against the actual identity, queue and object-storage configuration; threat-model coverage is not a substitute for implementation tests. |
| Observability and alert arithmetic | Official [OpenTelemetry documentation](https://opentelemetry.io/docs/) and Chapter 17 sections 17.1–17.3 | The review confirms bounded metric-label guidance, separates trace correlation from authorization, and checks the illustrative request-based budget arithmetic (0.1% of 10 million eligible requests = 10,000 bad events; 2% error rate is 20× the 0.1% budget fraction for the same window). Alert thresholds still require historical traffic and incident validation. |
| Cloud delivery and supply-chain claims | Approved [SLSA v1.2 specification](https://slsa.dev/spec/v1.2/), [SPDX specifications index](https://spdx.dev/use/specifications/), and Chapter 18 section 18.5 | The chapter distinguishes SBOM inventory, provenance, artifact signatures and deployment policy, and explicitly avoids treating a signature or green pipeline as proof of benign code. Confirm required attestations, signing identities and verification policy against the actual build platform and selected standard versions. | The reference catalog and Chapter 18 also now link the CISA/international-partner July 2026 SBOM minimum-elements guidance; the general CISA SBOM resource page is retained for broader context.
| Foundational worked calculations and assumptions | Chapters 01–04, 17 and 19; Bloom-filter sizing in Chapter 19 section 19.1A | Rechecked that the architecture example ties seat allocation to one authoritative transaction boundary, the capacity plan labels its workload and thresholds illustrative, the 99.9% request SLO uses a 0.1% error budget, and the Bloom-filter sizing formula gives approximately 9.59 million bits and 6.64 optimal hash functions for one million items at 1% false-positive probability. Arithmetic and internal reasoning are consistent at the stated precision. These checks do not validate every formula, workload assumption or implementation. |
| Webhooks and outbox implementation references | Current [OWASP Webhook Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html) and [Debezium stable Outbox Event Router documentation](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html) | The current pages cover the expected source topics: signature/replay protection, SSRF and duplicate handling for webhooks, and CDC-based outbox publication. These sources support the textbook's architectural boundaries but do not establish that any particular deployment is secure without configuration-specific testing. |
| Network protocol references | RFC Editor pages for HTTP semantics (9110), TCP (9293), QUIC (9000), HTTP/3 (9114), HTTP caching (9111), cache extensions (5861), TLS 1.3 (8446), IPv6 (8200), DNSSEC requirements (4033) | Targeted protocol-source spot checks were performed. This does not replace line-by-line claim/source alignment across all networking content. |


## Editorial and consistency review findings

A fresh relative-Markdown-link pass after the Chapter 05 reference cleanup and Chapter 12 projection-boundary clarification scanned all 27 Markdown files in the target tree (with fenced code removed before link extraction); every local target resolved. This still does not validate external URL liveness or Mermaid rendering.

A duplicate-URL scan of the reference catalog found 73 URL occurrences and 73 unique URLs; no duplicate destinations were found. This is a local catalog hygiene check only—external URL liveness, redirects, and claim-to-source alignment remain part of the open source audit.

A follow-up scan of the Further reading blocks in all 19 chapters found duplicate RFC links in Chapter 05; the duplicates were removed and RFC 9111 (HTTP Caching) was added explicitly. The same scan found no duplicate URLs in the other 18 chapter reference blocks. This checks duplication only, not whether every external URL is live or every citation supports its adjacent claim.

A whole-book heading-order pass found supplemental worked diagrams/guidance positioned after the `Further reading` heading in multiple chapters. The affected sections have been moved before `Further reading` so the teaching flow, references, and navigation footer are consistently ordered. This is an editorial correction, not evidence that the underlying technical claims have been fully verified. A fresh post-correction check of all 19 chapter pages confirmed balanced fenced blocks, no exact duplicate headings, no instructional headings after Further reading, and navigation footers at the end. Relative Markdown targets were checked across all 27 Markdown files in the target tree; no missing local targets were found. A static diagram scan also found 24 non-empty Mermaid blocks across the 19 chapters, each beginning with a recognized diagram declaration; actual renderer validation remains open. A targeted post-edit structural check of Chapters 03, 09, 12, 16, 17, 18 and 19 also passed after the latest content additions. These structural/link checks are separate from technical claim verification. A targeted source pass checked the OWASP injection-prevention pages and made the SPDX version reference neutral because the official index and spec redirect present version details differently. Continue the claim-by-claim technical review, exhaustive source-link audit, Mermaid rendering validation, and independent status verification/closure for the mandatory inventory.


## Scoped technical review log — 2026-10-24

### Chapters 01–02: targeted architecture and quality-attribute review

- **Chapter 01, section 1.16 — payment idempotency boundary:** the worked architecture example correctly treats a provider timeout as an uncertain outcome and includes a reconciliation path. A precision gap remained: a stable idempotency key is not an unlimited guarantee because key scope, retention, and same-key/different-payload behavior are provider-specific. The chapter now explicitly requires those properties to be checked, the logical operation/key association to be persisted, and reconciliation or manual recovery when retries may outlive the provider's key-retention window. This is a targeted correction, not a complete review of all Chapter 01 claims.
- **Chapter 02, sections 2.15–2.18 — quality-attribute scenarios and lifecycle trade-offs:** the reviewed sections distinguish availability, reliability, durability and correctness; require workload-specific measurable targets; caution against treating automated accessibility scans as proof of WCAG conformance; and qualify provider-specific sustainability guidance. No definite technical defect was identified in these inspected sections. Standards/source alignment and the rest of Chapter 02 remain open for the dedicated claim-by-claim pass.
- **Evidence boundary:** this pass inspected the cited sections and their reasoning. It did not validate all external links, independently verify every nearby citation, render Mermaid diagrams, or certify either chapter as complete. Keep both curriculum inventory rows at **Developing** until their acceptance criteria are independently satisfied.


### Chapters 03–04, 10 and 12: worked examples and protocol boundaries

- **Chapter 03, sections 3.16 and 3.18:** independently recalculated the illustrative daily request rate (300 million/day ≈ 3,472 requests/s), peak rate at 4× (≈13,889 requests/s), read/write split, payload bandwidth (about 176 MiB/s before overhead), Little's Law concurrency (about 1,667), cache-miss/database amplification, and 25%-capacity-loss sizing (24 instances under the stated linear-scaling assumption). The arithmetic is consistent at the stated precision. Inputs and scaling assumptions remain illustrative, and the chapter correctly requires representative measurement.
- **Chapter 04, section 4.17:** the reviewed fan-out example correctly shares one end-to-end deadline, accounts for queue/pool waits, distinguishes best-effort cancellation from stopping remote work, and separates accepted durable jobs from request-scoped work. Runtime-specific cancellation/shutdown behavior remains implementation-dependent and is not certified by this scoped read.
- **Chapter 10, section 10.18:** the reviewed consistency example correctly states that a timeout does not establish whether a write committed, that read-your-writes needs an enforcement mechanism, and that quorum intersection arithmetic alone does not prove linearizability. Full primary-source claim alignment remains open.
- **Chapter 12, section 12.3:** found and corrected a terminology precision issue in the crash timeline. The example now distinguishes processing record offset 812 from the committed consumer position, which in Kafka is conventionally the next offset to consume (typically 813 after processing 812). Both duplicate-delivery and lost-effect crash windows remain intact.
- **Evidence boundary:** this was a targeted review of named worked sections, not a full claim-by-claim review of these chapters, a live link audit, or rendered-diagram validation. Keep the inventory rows at **Developing**.


### Chapters 05–07 and 11: targeted networking, API, database and fencing review

- **Chapter 05, timeout troubleshooting example:** the reviewed sequence correctly distinguishes a client-visible timeout from the remote operation's commit outcome, recommends inspecting per-hop deadlines and queue/pool waits, and warns that indiscriminately increasing timeouts can increase in-flight work and queueing. No definite defect found in this excerpt; protocol claims and cited RFC alignment remain for the source pass.
- **Chapter 06, section 6.13:** the OpenAPI 3.1.0 excerpt includes a required path parameter, response schema and required fields. The compatibility discussion correctly qualifies optional-field additions by actual client/serializer behavior, calls out enum expansion and semantic changes, and requires parser/linter plus consumer/provider tests. The key/replay diagram also explicitly binds deduplication state to the mutation's transactional boundary. The full document still needs the already-planned dedicated OpenAPI lint and broad claim/source review.
- **Chapter 07, section 7.3:** the write-skew interleaving is logically consistent: two snapshot transactions read the same aggregate condition and update different rows, so row-level write conflicts need not protect the global invariant. The section appropriately qualifies serializable retries and warns against blind retries. Engine-specific isolation and constraint behavior still require source/configuration checks.
- **Chapter 11, section 11.6:** the stale-lease timeline correctly demonstrates why a worker-side lease belief is insufficient and why fencing must be enforced atomically at the protected resource. The token ordering, resource scope and recovery assumptions are called out. Implementation-specific token durability and coordination semantics remain open.
- **Evidence boundary:** no additional content correction was justified by these excerpts. This is a scoped inspection, not certification of the full chapters or their external references. Maintain **Developing** statuses until the complete acceptance checks pass.


### Additional scoped review — 2026-10-24

- Chapter 13 section 13.4: recalculated throughput changes in the illustrative table. The 40-to-60 concurrency step is about +14.3%; 60-to-80 is about +2.7%. The interpretation is consistent with the worsening p99, error rate, and queue behavior shown.
- Chapter 14 sections 14.3–14.4: recalculated the request-based error budget (0.1% of 50 million = 50,000 bad requests) and the recovery example (35 minutes elapsed; eight minutes of data-point lag in the stated example). The prose appropriately qualifies conclusions by the SLI and RTO/RPO definitions.
- Chapter 17 section 17.3: the 99.9% SLO permits a 0.1% bad-event fraction; 10 million eligible requests imply a 10,000-event budget; 2% bad events is 20x the allowed fraction for the same window. The text correctly treats burn rate as a ratio rather than a guaranteed forecast.
- Chapter 19 Bloom-filter example: recalculation confirms approximately 9.59 million bits, 1.20 MB decimal (about 1.14 MiB), and 6.64 optimal hash functions for one million items at a 1% target false-positive rate. The chapter appropriately qualifies this as an approximation.
- Chapter 16's tenant-scoped export example remains subject to full claim/source verification. Chapter 18's Kubernetes, IaC, delivery and supply-chain claims also remain open for version-specific verification.
- These focused checks do not complete the full technical review, source-link audit, or Mermaid renderer validation. Keep the relevant inventory rows at Developing.


### Chapter 20 — targeted source and structural review (2026-10-24)

- Added the missing client-side/offline-first/real-time curriculum area as a dedicated chapter rather than counting brief mentions in networking/API chapters as deep coverage. The chapter covers rendering choices, state ownership, optimistic mutation outcomes, local operation durability, sync cursors, conflict strategies/tombstones, realtime transports, reconnect/replay, WebRTC, collaboration, micro-frontends, interactive-session authority, security and operations.
- Checked browser-storage claims against MDN's current storage-quota/eviction guidance and IndexedDB documentation. The chapter correctly avoids promising that browser storage is unconditionally durable: best-effort storage may be evicted or cleared, storage limits vary, and synchronization is application responsibility. See [MDN Storage quotas and eviction criteria](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria) and [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API).
- Checked the WebRTC relay security distinction against provider documentation. The text now distinguishes a TURN relay that forwards encrypted WebRTC packets from an SFU/MCU that commonly terminates participant transport security and may access media unless additional end-to-end media encryption is used. Cloudflare's [TURN FAQ](https://developers.cloudflare.com/realtime/turn/faq/) is a provider-specific example; verify behavior against the selected media topology.
- A targeted static review of Chapter 20 found balanced fenced blocks, no duplicate headings, no instructional headings after Further reading, two Mermaid blocks with recognized `flowchart` and `sequenceDiagram` declarations, and the expected landing-page/roadmap/curriculum/audit/progress references. Its three footer links target existing files. Actual Mermaid rendering and the current all-28-file relative-link pass remain open.
- **Status: Developing.** The new chapter is substantive, but rendering trade-offs, synchronization algorithms, transport/replay semantics, WebRTC topologies, security controls, source alignment and operational failure cases still need full independent review. Do not mark the client-side inventory row Deep yet.


### Human-readable consolidation review — 2026-10-24

The editorial standard was extended to make the desired voice explicit: the textbook should read like an experienced engineer explaining a difficult idea to another engineer, not like a generated checklist or a set of stitched-together summaries. The standard now calls for clear motivation before jargon, connected prose, purposeful examples, selective bullets/tables, natural transitions, and removal of repeated explanations.

- **Chapter 05 — Networking:** The previous draft introduced core networking topics in short sections and then repeated much of the same material in later deep-dive sections. It has been consolidated into a request-journey narrative covering IP/routing/NAT, TCP/UDP/QUIC, DNS, TLS, HTTP versions, proxies/load balancing/CDNs, network security boundaries, timeouts, and evidence-led troubleshooting. Approximate word count changed from 6,133 to 2,423. The chapter retains its core HLD coverage but still needs a full protocol/source review; this edit is an editorial consolidation, not technical certification.
- **Chapter 12 — Messaging:** The previous draft repeated queue/pub-sub/log, delivery semantics, retries, lag, and outbox concepts across introductory summaries and subsequent detailed sections. It has been consolidated into a single progression: messaging models, partitions and consumer progress, delivery/idempotency, retries and backpressure, outbox/inbox/CDC, stream processing, schema evolution, CQRS/event sourcing, projection rebuilds, and event-data privacy. Approximate word count changed from 5,334 to 2,139. A compact compatibility matrix and event-identity guidance were retained to preserve useful depth without restoring repeated explanations. The chapter should be checked during the next technical pass to ensure the reduced treatment still gives enough depth for the intended textbook.
- Static checks after these edits found no broken local relative Markdown targets across the 28 Markdown files, no unbalanced fenced blocks, no exact duplicate headings, and no instructional headings after Further reading. This does not validate Mermaid rendering, external-link liveness, or technical claims.
- **Editorial status:** the first human-readable consolidation pass now covers all 20 chapters. The latest pass removed repeated summaries where detailed teaching already existed, while retaining unique examples and trade-off guidance. This is an editorial milestone, not technical/source certification. Continue checking whether each remaining chapter tells one coherent story, whether bullets and tables serve a real purpose, and whether a concept is explained once in the right place rather than repeated in several checklists.


### Chapter 02 — readability consolidation (2026-10-24)

The chapter previously repeated several concepts after the main explanation: availability/reliability/durability/correctness were defined in the quality-attribute table and then reintroduced; requirement prioritization appeared in multiple sections; and a second review checklist repeated the earlier self-check. These were consolidated into the main definitions, prioritization explanation and self-check. The distinct quality-scenario section and the later accessibility, operability, portability, cost, sustainability and lifecycle-interaction material remain.

Approximate word count decreased from 3,939 to 3,684. This was an editorial pass, not a complete technical/source certification. Section numbering was updated; the inventory now refers to Chapter 02 sections 2.15–2.18 for quality scenarios and lifecycle attributes.


### Chapter 19 — readability consolidation (2026-10-24)

The chapter opened with several short overview sections for topics that were then explained again in detail later in the same chapter or in their dedicated chapters. Those summaries and a repeated synthesis checklist were removed. Queueing and tail behavior was retained as a connected explanation because it contributes directly to cross-cutting reasoning; the introduction now points readers to Chapters 03, 08 and 12 for the underlying capacity, storage and messaging mechanics. Approximate word count decreased from 3,890 to 3,499. This is an editorial pass only; the chapter's technical/source review remains open.


### Source spot-check after readability edits — 2026-10-24

Opened the canonical source pages linked from the revised networking and messaging chapters and the existing accessibility discussion:
- IETF RFC 9293 (TCP), RFC 8446 (TLS 1.3), RFC 9110 (HTTP semantics), and RFC 9114 (HTTP/3) resolve to their official RFC Editor pages.
- Apache Kafka 4.3 design documentation resolves to the versioned official documentation.
- W3C WCAG 2.2 resolves to the W3C Recommendation.

This confirms the checked URLs are reachable and point to the intended authoritative documents. It does not complete a claim-by-claim verification of every protocol statement, all external links, or provider-specific details. Those checks remain open.


### Remaining-chapter readability pass — 2026-10-24

The first human-readable consolidation pass now covers all 20 chapters. Earlier focused edits covered Chapters 02, 05, 12 and 19. The latest pass reviewed Chapters 01, 03, 04, 06–11 and 13–18; Chapter 20 was read end-to-end and retained without broad shortening because its sections cover distinct client-side, offline-first, synchronization, realtime, WebRTC, collaboration and interactive-session concerns.

- **Chapter 01:** reduced repeated architecture-decision and decomposition guidance while retaining the reversible-decision discussion, architecture views and worked architecture evaluation.
- **Chapter 03:** narrowed the latency-budget section to budget composition and connected queueing detail to the dedicated saturation/tail-latency section.
- **Chapter 04:** reduced repetition across the pool introduction, pool-sizing section and runtime-resource discussion.
- **Chapter 06:** removed a second idempotent-retry diagram that repeated the earlier communication failure path; the contract, retry, idempotency and uncertain-outcome material remains.
- **Chapter 07:** replaced repeated overview summaries with a short orientation and removed duplicated isolation, query-plan, migration and checklist explanations. The overselling example, connection-pool admission-control discussion, sharding example and write-skew lab remain.
- **Chapters 08–11 and 13–18:** removed overlapping overview sections when later sections already explained the mechanism. Unique material was preserved or folded into detailed sections, including the Chapter 09 cache-benefit calculation, Chapter 11 2PC-versus-saga comparison and idempotency boundaries, and Chapter 15 orchestration-versus-choreography trade-offs.
- **Static structure check:** the edited chapter pages (01, 03, 04, 06–11, 13–18) and reviewed Chapter 20 have balanced fenced blocks, no exact duplicate headings, no instructional headings after Further reading, and the expected navigation footer. A fresh relative-link pass across all 28 Markdown files completed after these edits; no missing local relative targets were found.

**What this status means:** readability consolidation is complete for the first pass; the technical claim/source audit, external-link liveness, Mermaid rendering, OpenAPI validation and cross-chapter consistency review remain open. Do not promote coverage rows to Deep on the strength of editorial work alone.


## Rapid verification sprint — 2026-10-24

A fresh fetch and structural scan of the current default-branch versions of all 20 chapter pages found balanced fenced blocks, no exact duplicate Markdown headings, a Further reading section, and the expected navigation footer in every chapter. The scan counted 22 Mermaid declarations in chapter pages. These results support structural integrity only; they do not prove that Mermaid renders, that the OpenAPI example passes a parser, or that the technical claims and source links are fully verified. All 21 mandatory inventory rows therefore remain provisional, and no row is promoted to Deep on the basis of this scan.


## Targeted technical verification sprint — 2026-10-24

The following scoped checks were completed during the rapid closeout pass; they do not upgrade the corresponding inventory rows from Developing to Deep.

- **Chapter 03 capacity arithmetic:** recalculated average and peak request rates, payload bandwidth, Little's Law concurrency, and the simplified 25%-capacity-loss instance estimate. The arithmetic matches the stated assumptions and rounding.
- **Chapter 10 distributed consistency:** reviewed quorum-intersection caveats, the distinction between formal CAP availability and business usefulness, session consistency, and the statement that quorum arithmetic alone does not prove linearizability.
- **Chapter 11 coordination:** reviewed the distinction between saga compensation and atomic rollback, the scope limits of exactly-once claims, fencing at the protected resource, and protocol-safe membership changes.
- **Chapter 14 reliability:** recalculated the request-based 99.9% SLO example (50 million eligible requests yields 50,000 bad events of budget; a 1% observed error rate is a 10x burn rate against a 0.1% target). The chapter explicitly distinguishes request-based from time-based SLOs.
- **Chapter 19 Bloom filter:** recalculated the standard sizing approximation for one million items and a 1% target false-positive rate (about 9.585 million bits, 1.20 MB decimal / 1.14 MiB, and roughly seven hash functions). The text appropriately treats this as an estimate under stated assumptions.
- **Chapter 06 OpenAPI example:** parsed the YAML with PyYAML and checked core invariants; the path-template and required path-parameter rules were cross-checked against the official [OpenAPI 3.1.0 specification](https://spec.openapis.org/oas/v3.1.0.html). This is not a full specification validator.
- **SLO evidence:** checked Google's [SRE Workbook error-budget policy](https://sre.google/workbook/error-budget-policy/) for the definition of error budget as 1 minus the SLO and the dependence of request budgets on the chosen SLI.

**Still open:** no Mermaid renderer was obtained because the npx attempt timed out; no full OpenAPI linter was run. These checks are targeted, not a claim-by-claim source audit. All 21 curriculum inventory statuses remain provisional; the independent coverage, external-link, source alignment and cross-chapter consistency reviews are not complete.


## Chapter 20 source spot-check — 2026-10-24

A focused source spot-check was completed against the live official/vendor pages for browser storage, WebRTC protocol behavior, and the status of the cited W3C publications.

- MDN's storage guidance confirms that browser-origin data is best-effort by default; eviction, quotas, and persistent-storage approval vary by browser. Chapter 20's warning not to treat browser storage as a guaranteed server-side durable record is appropriate.
- MDN's WebRTC protocol guidance supports the chapter's distinction between ICE connectivity checks, STUN address discovery, and TURN relaying. Cloudflare's provider-specific TURN FAQ confirms that its TURN service relays WebRTC-encrypted packets and distinguishes TURN's point-to-point relay role from SFU media fan-out. The chapter correctly scopes the privacy claim to a TURN relay and separately warns that an SFU/MCU may access media unless a separate end-to-end media-encryption design prevents it.
- The cited W3C [Service Workers publication](https://www.w3.org/TR/service-workers/) is currently an evolving Candidate Recommendation Draft, and [Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB-3/) is a Working Draft. Chapter 20's Further reading section now explicitly identifies these statuses, so readers do not mistake them for finalized Recommendations.
- MDN WebRTC protocol guidance has been added alongside the existing general WebRTC API reference.

This is a targeted source spot-check, not a complete Chapter 20 claim-by-claim review. The chapter's full external-link audit and all other chapters' source verification remain open. Mermaid rendering and full OpenAPI validation also remain unverified.


## Final structural and focused source pass — 2026-10-24

- **Chapter 09 duplication correction:** removed a second cache-aside sequence diagram that repeated the read path already illustrated near the chapter's opening. The chapter now has one cache-aside read-path diagram.
- **Fresh structural check:** all 20 chapter pages still have balanced code fences, no exact duplicate Markdown headings, a Further reading section, and the navigation footer at the end. The current chapter-page Mermaid inventory is 29 blocks across the 20 chapters; static declaration checks pass, but rendering is not validated.
- **Chapter 20 source qualification:** checked current MDN browser-storage and WebRTC protocol guidance, Cloudflare's provider-specific TURN FAQ, and W3C publication statuses. The chapter now identifies the Service Workers publication as an evolving Candidate Recommendation Draft and Indexed Database API 3.0 as a Working Draft, and includes the MDN WebRTC protocols guide. These are targeted checks, not exhaustive claim/source verification.

The book-wide technical acceptance remains open: no Mermaid renderer or full OpenAPI validator was successfully run; external-link liveness and source-to-claim alignment are not exhaustive; and the 21 curriculum inventory families have not all received independent depth verification. Do not mark them Deep or claim the entire textbook technically certified until those checks are completed.


## Additional validation pass — 2026-10-24

### Chapter 06 OpenAPI example

The embedded Orders API YAML was re-parsed with PyYAML and passed targeted structural invariants: OpenAPI version is 3.1.0; the paths map is non-empty; the templated `{orderId}` path has exactly one matching `in: path` parameter; that parameter is `required: true`; and the operation has an `operationId` and response definition. This does **not** establish full OpenAPI 3.1 compliance. The environment lacks `openapi-spec-validator`, and package-host DNS/network access is unavailable, so the full validator remains pending.

### Primary-source availability and status spot-check

The following reference pages were opened successfully through the web retrieval environment:
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9293 — TCP](https://www.rfc-editor.org/rfc/rfc9293.html)
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html)
- [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0.html)
- [Google SRE Workbook — Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — W3C Recommendation
- [MDN — Storage quotas and eviction criteria](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)
- [MDN — WebRTC protocols](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols)
- [W3C — Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB-3/) — Working Draft

This establishes that these selected references resolve and that their document statuses were checked. It is not a repository-wide URL liveness audit and does not verify every technical claim against the nearest cited source.

### Remaining acceptance blockers — reference and tooling pass

- Mermaid rendering of all 29 chapter-page diagrams is still unverified. No local Mermaid CLI/standalone parser is available, and external package retrieval fails due network/DNS restrictions.
- Full OpenAPI 3.1 schema/spec validation is still unverified for the same package-access constraint.
- The full source-to-claim audit, repository-wide external-link audit, independent review of all 21 mandatory topic families, and cross-chapter consistency pass remain incomplete. Do not promote provisional coverage statuses to Deep based on these targeted checks.


## Curriculum-gap corrections from independent spot review — 2026-10-24

A focused comparison of curriculum requirements, Chapter 05/18 content, and glossary entries found several concepts that deserved explicit teaching rather than relying on implication.

- **Chapter 05:** added a concise OSI/TCP-IP mental model tied to concrete architecture responsibilities; expanded global traffic-management and session-affinity behavior, including caching/connection delay, failover capacity, and stickiness trade-offs.
- **Chapter 18:** added feature-flag design guidance covering deploy/exposure separation, safe defaults, ownership and expiry, enabled/disabled-path testing, authorization, and flag cleanup.
- **Glossary:** added definitions for feature flags, LWW, PITR, QUIC and stream-processing watermarks.

These are genuine coverage improvements. They are not enough to promote the associated inventory families to Deep: the full chapter-by-chapter mechanism/failure-mode review and standards/source verification still need completion.


## Final acceptance checkpoint — 2026-10-24

The latest verification re-opened the live curriculum, editorial standard, progress tracker and representative chapters across networking, distribution/consistency, coordination, messaging, scaling, reliability, API design and cloud delivery. Recent targeted fixes are present in the repository. The chapter content supports keeping the relevant topic families at **Developing** until the full acceptance criteria are independently checked; no status is upgraded on the basis of headings or keyword scans.

### What is supported by checks so far

- Twenty chapter pages and the supporting curriculum, roadmap, editorial standard, glossary, reference library, progress tracker and coverage audit are part of the textbook structure recorded in the progress tracker.
- Prior structural checks recorded in the tracker include balanced fences, unique headings, Further reading placement, navigation footers and resolving relative links across the 28 Markdown files at that checkpoint.
- Selected primary-source spot checks, targeted capacity/SLO/Bloom-filter arithmetic, and targeted Chapter 06 OpenAPI YAML invariants have been recorded. These are bounded checks, not a full source-to-claim audit or full standards validation.
- The current spot review identified and fixed explicit networking, feature-flag and glossary omissions; the changes do not by themselves establish deep coverage across all 21 topic families.

### Remaining acceptance blockers

1. Read every mandatory inventory row against the actual chapter text and verify mechanism, example, selection criteria, trade-offs, failure modes and operational/design implications before changing provisional coverage statuses.
2. Audit every external link for liveness/redirects and verify claim-to-source alignment, including the Chapter 20 links that received only targeted checks.
3. Render all 29 chapter-page Mermaid diagrams in a real renderer. This remains blocked in the current environment because no renderer is available and package retrieval fails under network/DNS restrictions.
4. Run a full OpenAPI 3.1 validator/linter against the Chapter 06 example. Targeted YAML parsing and invariant checks are not equivalent; package retrieval is blocked in the current environment.
5. Complete the cross-chapter review for terminology, contradictions, duplicate explanations, prerequisite gaps and numerical assumptions.

**Status:** review-ready content draft; **formal technical acceptance remains open**. Do not mark the textbook fully validated until the blockers above have evidence of completion.


## Inventory reconciliation — 2026-10-24

A fresh pass fetched all 20 current chapter pages and counted Mermaid declarations directly in their Markdown. The current chapter-page total is **29 blocks**: 16 in Chapters 01–10 and 13 in Chapters 11–20. Earlier checkpoints in this file recorded 21 or 22 blocks; those are historical counts from earlier content states and are superseded by this inventory. Rendering remains unverified, so this is a count of declared blocks only, not a syntax or visual acceptance result.

The row for coordination/distributed transactions previously referenced Chapter 11 section 11.2A, which is absent from the current chapter. The mapping now points only to the current sections 11.1A–11.1C, 11.5A–11.5I, and 11.6.

The latest mapping check compared every numbered section endpoint cited in the 21-row mandatory inventory with the current chapter headings. All referenced endpoints exist after correcting the stale Chapter 11 section reference. A separate static pass checked the first non-comment line of all 29 Mermaid blocks: each declares a recognized flowchart or sequence diagram. Neither check proves content depth or actual Mermaid rendering.



## Independent depth review and final structural recheck — 2026-10-24

### Focused review and correction

The current versions of all 20 chapter pages were re-fetched and checked against the curriculum map. A targeted mechanism-level read covered storage-model selection; cache correctness, security and invalidation; consistency and quorum assumptions; consensus, fencing, two-phase commit and sagas; messaging delivery, replay, schema evolution and event-time handling; OAuth/OIDC token roles, injection and tenant isolation; Kubernetes/cloud delivery; and offline synchronization, realtime transports and WebRTC.

One substantive gap was found in Chapter 09: hot keys appeared in review checklists but did not have their own mechanism-level treatment. A new section now explains how to diagnose skew and choose safe mitigations, distinguishes hot reads from hot writes, and warns that key salting/partitioning is only safe when the invariant and aggregation model permit it. It also adds a targeted validation scenario that keeps total load fixed while making one key disproportionately hot. The chapter's further reading now includes the official AWS Caching Best Practices and OWASP Web Cache Security Cheat Sheet. These official pages were opened during this review.

This correction is a concrete improvement, not evidence that every inventory row now qualifies as Deep. The mandatory inventory remains provisional until the full mechanism/example/selection/trade-off/failure-mode and source checks are completed row by row.

### Fresh structural check

A new check was run against all 20 current chapter pages, recognizing both backtick and tilde Markdown fence styles. Results:
- All 20 chapter pages have balanced fenced blocks.
- No exact duplicate Markdown headings were found.
- Each chapter has a Further reading section.
- Navigation footers are present at the end.
- No instructional headings appear after Further reading.
- The inventory contains 29 Mermaid blocks across the chapters. All 29 begin with recognized Mermaid diagram declarations after skipping blank/comment lines.

**Limit:** this is static Markdown/diagram-declaration validation. No actual Mermaid renderer was available, so successful rendering and visual layout are unverified.

### Acceptance status after this pass

- Structural Markdown checks: **passed** for all 20 chapters.
- Focused Chapter 09 hot-key depth gap: **corrected**.
- Selected Chapter 09 source pages: **opened and checked**.
- All 21 topic-family depth acceptance: **still open**; targeted inspection must not be presented as exhaustive independent acceptance.
- Repository-wide external-link liveness and claim-to-source alignment: **still open**; selected official references are verified, not every link/claim.
- Mermaid rendering: **still open**; the environment could not acquire the required renderer.
- Full OpenAPI 3.1 validation: **still open**; prior YAML parse and targeted invariants passed, but no full validator/linter ran.
- Whole-book contradictions, prerequisite flow and residual duplication: **still open beyond prior scoped checks**.

The textbook is structurally clean and review-ready, but formal technical acceptance is not yet justified. Do not promote coverage rows to Deep or label the book fully validated until the remaining checks have evidence.



## Reference-link availability pass — 2026-10-24

The current reference catalog was re-fetched and all **74 unique destinations** in `references/README.md` were opened or attempted in the web retrieval environment. This included foundational distributed-systems papers; IETF RFCs; PostgreSQL and SQLite; versioned Kafka 4.3 and OpenAPI 3.1.0 documentation; Google SRE; AWS, Google Cloud and Azure architecture material; Docker and Kubernetes; OpenTelemetry; C4; WCAG 2.2; OAuth/OIDC; OWASP; CISA/NIST; SLSA v1.2; and SPDX. The two Chapter 09 references added during the current pass (AWS caching best practices and the OWASP Web Cache Security Cheat Sheet) were also opened successfully.

Availability caveats:
- The page reader could not fetch the DOI destinations for the FLP consensus paper and the LSM-tree paper directly. Search results independently confirm both DOI identifiers and the cited publications.
- The generic CISA SBOM landing page returned HTTP 403 to the retrieval environment. The linked CISA 2026 SBOM bulletin resolves and describes the updated minimum elements.
- Some sites redirect to canonical trailing-slash URLs or versioned pages; the redirects led to the intended sources.

This is a **reference-catalog link-availability pass**, not a complete claim-by-claim source audit. It does not cover every chapter-only URL or verify every sentence against a source. Continue to keep source-to-claim alignment open until the remaining chapter-level review is complete.



## Cross-chapter consistency pass — 2026-10-24

A focused consistency pass compared the main concepts that are taught in one chapter and relied on by another. The following boundaries remain aligned in the current text:

- **Capacity and overload (Chapters 03, 13 and 19):** workload estimates are treated as assumptions to validate, not guaranteed production capacity; per-instance limits must be multiplied across replicas and other shared bottlenecks considered; retries and hedges can amplify demand.
- **Consistency, consensus and transactions (Chapters 07, 10 and 11):** database isolation is not conflated with distributed consistency; quorum intersection is not presented as a complete linearizability proof; consensus ordering does not make arbitrary external side effects transactional; 2PC blocking/recovery is distinguished from saga compensation; leases do not protect against stale owners unless fencing/conditional enforcement reaches the protected resource.
- **Caches, authorization and deletion (Chapters 09, 16 and 20):** a cache hit is not authorization; TTL does not imply immediate revocation; deleting an authoritative row does not automatically erase copies in caches, indexes, offline replicas, events or backups; offline clients may resurrect deleted records if tombstones are discarded too early.
- **Messaging and data correctness (Chapters 06, 12 and 19):** idempotency guarantees are scoped to a defined operation/effect boundary; a durable outbox avoids the database-plus-broker dual-write gap but does not remove duplicate publication; consumer deduplication must be atomic with local effects; schema compatibility and replay remain distinct concerns.
- **Recovery and deployment (Chapters 14 and 18):** recovery targets must be measured through restore exercises; region or cluster failover requires data-state and stale-writer handling, not only routing changes; progressive delivery must account for backward/forward compatibility of schemas and stored data.
- **Client and server ownership (Chapters 06, 16 and 20):** client state and local persistence improve experience but do not replace server-side authorization; a persistent realtime connection is not durable delivery; token expiry or membership revocation must affect long-lived subscriptions and offline operations.

The Chapter 09 hot-key gap found during the targeted review has been corrected with a dedicated section. The chapter's glossary and related concepts now align on LWW, PITR, QUIC, event-time watermarks, feature flags, idempotent receivers, database-per-service, and fencing tokens.

**Limit:** this is a focused consistency pass over high-risk concept boundaries, not a proof that no contradiction or duplicate remains anywhere in all 20 chapters. The 21-family inventory stays Developing; no row is promoted to Deep.



## CI validation path for blocked tooling — 2026-10-24

To avoid leaving renderer/spec validation as a purely environmental blocker, a repository-native route has been added:

- `.github/workflows/system-design-validation.yml` runs on textbook changes, pull requests and manual dispatch.
- `system-design-mastery/scripts/validate_artifacts.py` extracts fenced Mermaid diagrams and the embedded OpenAPI 3.1 example. It fails if the expected 20 chapters, 29 Mermaid diagrams or one OpenAPI document are not found, and screens diagram declaration lines.
- One CI job installs `openapi-spec-validator` and validates the extracted specification.
- A separate CI job installs the official Mermaid CLI, renders each diagram to SVG, checks that all 29 outputs exist, and uploads the rendered files as an artifact.

**Current status: configured, not yet proven passing.** The files were re-fetched after creation and the chapter-root path in the extraction script was corrected. A completed workflow result has not yet been retrieved; therefore neither real Mermaid rendering nor full OpenAPI validation is marked passed. Once the Actions run completes, inspect both job results and repair any failures before acceptance. If Mermaid CLI cannot install its browser/runtime on the hosted runner, use its documented container alternative or pin a compatible CLI/browser combination and rerun. If OpenAPI validation flags an issue, confirm against the versioned OpenAPI 3.1 specification and fix the actual contract rather than suppressing the error.


## Additional depth corrections — storage and Kafka guarantees — 2026-10-24

Two more targeted review gaps were found and corrected:

- **Chapter 08, new section 8.2A:** expands specialized storage selection beyond family labels. It compares wide-column, graph, time-series, inverted-index search, columnar warehouse/lakehouse and relational models by example workload, efficient access path, and operational/correctness costs. A commerce example distinguishes authoritative price/inventory from search, recommendation and analytics projections, including freshness, replay/rebuild, deletion and authorization obligations.
- **Chapter 12, new section 12.3A:** explains Kafka idempotent producer scope, transactional records/offsets and `read_committed` visibility, and demonstrates why a Kafka transaction does not automatically include a PostgreSQL commit or external payment/email side effect. It adds a six-question checklist for auditing an exactly-once claim and links to the versioned Kafka 4.3 delivery and transaction design docs.

Both changes are substantive depth corrections, not grounds to mark the inventory rows Deep. They require independent review and the CI validation pipeline's completed run. The repository validation workflow now has two artifact jobs configured, but actual Mermaid rendering and OpenAPI validation remain unconfirmed until a completed Actions run is inspected.


## All-chapter section map recheck — 2026-10-24

A fresh heading-level review re-fetched the current section structures for all 20 chapters. Chapters 01–07 and 13–19 have dedicated sections for the major curriculum areas shown in the mandatory inventory, including measurable quality attributes, capacity-test plans, concurrency/cancellation, networking layers, API contract/security/gateway semantics, relational anomalies and resharding, scaling/overload, SLO/recovery rehearsal, architecture styles, IAM/threat modeling, observability cardinality/incident response, Kubernetes/IaC/supply-chain security, and multi-tenant fairness/pattern interactions. Chapters 08, 09 and 12 were additionally checked after substantive edits; their fences/headings/footer structure remains intact.

This verifies that the expected teaching areas and named sections exist. It does **not** prove that every explanation in each area meets the Deep bar. In particular, the full 21-row acceptance still requires examples, selection criteria, trade-offs, failure modes, and source alignment to be independently checked row by row. The two newest additions (Chapter 08 section 8.2A and Chapter 12 section 12.3A) remain provisional improvements until that deeper review and automated validation finish.

### Validation workflow observability

The repository contains the CI workflow and artifact-extraction script. The workflow has now been inspected through the Actions REST endpoints rather than relying on the pull-request-only helper. See the later **CI evidence update** below for the verified OpenAPI pass, initial Mermaid sandbox failure, and corrected run status.


## Focused client real-time consistency review — 2026-10-24

A mechanism-level review of Chapter 20 found a concrete missing edge case in the already-described replayable real-time stream: a replay endpoint and a live subscription can each work correctly yet lose an event at the handoff boundary. Section 20.6 now describes the high-watermark/subscription-position requirement, overlap or buffering, merge and deduplication, durable checkpoint advancement, retention-gap detection and snapshot fallback. It also proposes boundary tests for publishes during subscription setup, disconnects during replay, duplicate delivery, cursor expiry and crashes between applying an event and persisting the checkpoint.

This is a substantive correction, not proof that all client/realtime topics are accepted. The exact handoff must be verified against the selected broker/change-feed API and its ordering/retention contract. The mandatory inventory row remains **Developing** until source alignment, operational assumptions and diagram rendering are independently verified.


## CI evidence update — 2026-10-24

The initial workflow run has now been inspected directly. Run [40103087271](https://github.com/kowlutla/System-Design/actions/runs/40103087271) extracted the expected 29 Mermaid diagrams and one OpenAPI 3.1 document. Its Structural and OpenAPI validation job **passed**, including the `openapi-spec-validator` command. Its Mermaid renderer job **failed before rendering the first SVG** because Chromium could not start under the runner's default sandbox policy (`No usable sandbox`). That failure indicates a CI browser-launch configuration problem, not a demonstrated syntax error in the diagrams.

The workflow was updated at commit `4d868540e7913b027acd3f43c58304586d80cb61` to pass Puppeteer a no-sandbox configuration and to treat missing rendered files as an upload failure. At the time of this earlier entry, corrected run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824) was still in progress. It has since completed successfully; see **Confirmed CI run** below.

This does not change the overall acceptance decision: all 21 inventory families remain Developing/provisional, source-to-claim review remains incomplete, and whole-book technical acceptance is open.


## Confirmed CI run — 2026-10-24

Corrected workflow run [40104445824](https://github.com/kowlutla/System-Design/actions/runs/40104445824) completed both jobs successfully:
- The extracted embedded OpenAPI 3.1 document passed `openapi-spec-validator`.
- The renderer processed all 29 Mermaid inputs; the job verified the count and uploaded [29 SVG files](https://github.com/kowlutla/System-Design/actions/runs/40104445824/artifacts/12563862191). The job log lists all rendering inputs and confirms artifact upload.

This is verified automated rendering, not a manual visual inspection of diagram clarity/layout. It also does not complete the separate 21-family depth acceptance or the exhaustive claim-to-source/whole-book consistency audit. All inventory rows remain Developing/provisional.
