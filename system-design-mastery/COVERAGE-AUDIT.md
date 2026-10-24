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
| Requirements and quality attributes | 02 — 2.1–2.18, 2.19 accessibility/usability/internationalization, 2.20 operability/portability/cost/sustainability, 2.21 quality-attribute interactions | Developing | Validate examples against standards and make sure each quality attribute has measurable acceptance scenarios and explicit verification ownership. |
| Workload estimation and capacity | 03 — 3.17 test methodology, 3.18 worked capacity test plan | Developing | Section 3.18 adds an illustrative workload mix, explicit latency/error/queue criteria, ramp/steady/spike/failure/soak sequence, and evidence to preserve. Validate thresholds against an actual product SLO and run the plan in a representative environment. |
| Execution, concurrency, runtime resources | 04 — 4.1–4.15, 4.16 cancellation and structured task lifetime | Developing | Verify runtime-specific examples, add cancellation propagation scenarios, and ensure thread/task/pool limits are distinguished. |
| Network fundamentals: IP, routing, TCP/UDP, DNS, TLS, HTTP | 05 — sections 5.1–5.18, 5.22–5.23 | Developing | Section 5.23 adds a symptom/evidence/hypothesis matrix, phased investigation sequence, and a timeout-after-deployment worked example. Still verify protocol details against cited RFCs and test the troubleshooting guidance against real traces or a lab. |
| Load balancing, reverse proxies, ingress, global traffic management | 05 — 5.19; 13 — Load balancing and consistent hashing, 13.1B; 18 — Cloud primitives | Developing | Dedicated mechanism-level coverage: L4/L7, algorithms, health, draining, affinity, locality, TLS, failure modes, metrics. |
| CDN, edge delivery, origin shielding and invalidation | 05 — 5.20; 09 — Local, distributed and CDN caches, 9.1F, 9.1G | Developing | Dedicated edge-cache behavior, cache-key correctness, stale content, purge, origin failover, security and cost. |
| API gateways and API management | 06 — 6.11 API gateways and API management | Developing | Dedicated gateway responsibilities, limits, auth boundary, routing, transformation, high availability and failure policy. |
| API styles, contracts, retries, idempotency, streaming | 06 — includes 6.13 worked OpenAPI evolution | Developing | Section 6.13 demonstrates an OpenAPI response contract, additive-field rollout, breaking-change risks, consumer/provider contract tests and deprecation gates. Still validate syntax with a real OpenAPI linter and check client-specific compatibility behavior. |
| Architectural styles and patterns | 01, 15, 19 | Developing | A systematic comparison of layered/N-tier, client-server, modular monolith, SOA, microservices, event-driven, hexagonal, pipe/filter, serverless, CQRS/event sourcing and hybrids. |
| Relational modeling, SQL, indexes, transactions | 07 — includes 7.2 sharding/resharding and 7.3 worked write-skew lab | Developing | Section 7.3 traces concurrent transactions that each pass a local check but violate a global invariant, compares protection strategies, and defines a retry/test matrix. Continue validating isolation/query-plan examples and database-specific guarantees. |
| NoSQL models, search, analytics, data lakes | 08, 19 | Mentioned / Developing | Sections 8.2–8.7 now compare major storage families, derived search indexes, row/columnar and lakehouse workloads, materialized views, and distributed file/object/block semantics. Verify product-specific guarantees and add a comparative access-pattern example. |
| Storage engines, WAL, B-tree, LSM, compaction | 08 | Developing | Add recovery/write-path examples and compare amplification and workload implications. |
| Caching at client, CDN, application and data layers | 09 — 9.1A–9.1H, 9.2, 9.3 cache security/tenant isolation/freshness | Developing | Verify HTTP cache directives and provider-specific behavior; add a worked cache-key and invalidation scenario across user/tenant boundaries. |
| Distributed failure, consistency, clocks, CAP/PACELC | 10 | Developing | Section 10.18 now adds a write-timeout/read-replica timeline and explains why quorum arithmetic alone does not prove linearizability. Verify the consistency claims against primary literature and implementation contracts. |
| Replication, consensus, leases, locks, fencing, transactions | 11 — includes 11.6 worked stale-lease/fencing timeline | Developing | Section 11.6 traces a paused lease holder resuming after takeover and explains why the protected resource must atomically enforce monotonically increasing fencing tokens. Continue verifying protocol-specific recovery and consensus claims. |
| Queues, pub/sub, logs, Kafka, CDC and stream processing | 12 — 12.1A–12.1H, 12.2, 12.3 event sourcing/CQRS/schema governance, 12.4 crash timeline | Developing | Section 12.4 traces both database-before-offset and offset-before-database crash windows, compares inbox/idempotency/broker transactions/outbox, and states the exactly-once boundary. Section 12.3 now includes a producer/consumer schema-change risk matrix and rollout guidance. Section 12.3 now includes a stepwise projection rebuild/catch-up/cutover protocol with partition-scoped offsets, idempotent replay, validation and rollback criteria. Still verify the schema matrix against one chosen serialization format and registry. |
| Scaling, hashing, partitioning, hotspots, overload | 13 — 13.1A–13.1G, 13.2, 13.3 hedged requests/adaptive concurrency | Developing | Verify hedging safety and load amplification; add a measured decision example and check adaptive-concurrency stability claims. |
| Reliability, SLOs, redundancy, backup/restore, DR | 14 — includes 14.2–14.4 recovery engineering and rehearsal | Developing | Section 14.4 adds a timed restore/replay/cutover rehearsal with explicit RTO/RPO arithmetic, stale-writer fencing, data validation, dependency readiness and backlog drain. Continue checking recovery assumptions and testability. |
| Security, identity, privacy, tenant isolation | 16 — 16.1A–16.1J, 16.2, 16.3 API threat patterns | Developing | Validate controls against OWASP guidance and add a worked multi-tenant authorization threat model with explicit trust boundaries. |
| Observability and production operations | 17 — including 17.2 practical observability and 17.3 worked SLO alert design | Developing | Section 17.3 now derives a request-based error budget and burn-rate example, then maps signals to response policies and validation steps. Still verify alert behavior against historical traffic/incidents and review sampling/cardinality trade-offs across the full chapter. |
| Cloud, containers, Kubernetes, IaC and delivery | 18 | Developing | Sections 18.2–18.5 now deepen Kubernetes, service mesh, IaC state/drift, SBOM, provenance, signing and build/deployment trust. Still verify supply-chain guidance against primary standards and test examples. |
| Cross-cutting patterns, cost, multi-tenancy and multi-region | 19 — 19.1A–19.1F, 19.2 pattern catalog, Bloom-filter sizing example | Developing | Verify approximation assumptions, add a worked multi-tenant fairness scenario, and review pattern interactions across chapters. |


## Exact section map for the current expansion pass

The following sections are present and are the starting points for the deeper review. “Present” does not mean technically verified or complete.

| Area | Exact chapter section(s) to review |
|---|---|
| Architecture reasoning | Chapter 01: 1.4, 1.6, 1.7, 1.9, 1.13, 1.14, 1.15 architecture views and diagram selection |
| Measurable quality attributes | Chapter 02: 2.5–2.12, 2.15–2.21 including accessibility, usability, internationalization, operability, portability, cost, sustainability and attribute interactions |
| Workload and capacity | Chapter 03: 3.1–3.15, 3.16 Worked capacity example, 3.17 Workload testing methodology |
| Runtime and resource limits | Chapter 04: 4.1–4.14, 4.15 Runtime resource limits, 4.16 Cancellation and structured concurrency |
| Networking and request path | Chapter 05: 5.1–5.18, 5.19 Load balancers, 5.20 CDNs, 5.21 Network boundaries, 5.22 Protocol details and operational edge cases, 5.23 Practical network troubleshooting |
| API contracts and gateway | Chapter 06: 6.1–6.10H, 6.11 API gateways and API management, 6.12 Webhooks |
| Relational data and transactions | Chapter 07: Isolation anomalies, Optimistic versus pessimistic concurrency, Query planning, Safe schema migration, Relational systems in practice, 7.2 Sharding and resharding, 7.3 Write-skew concurrency lab |
| Storage families and engines | Chapter 08: B-trees and LSM trees, 8.1A–8.1I, 8.2–8.6 data-system families/search/analytics/indexes, 8.7 Distributed file systems and object/block/file interfaces |
| Cache behavior | Chapter 09: Common patterns, TTL and invalidation, Failure modes, 9.1A–9.1H, 9.2 Cache patterns and failure modes, 9.3 Cache security/tenant isolation/freshness |
| Distributed consistency | Chapter 10: Consistency models, CAP and PACELC, 10.7–10.18 including worked consistency timeline |
| Replication and coordination | Chapter 11: Leader election, Leases and fencing tokens, Two-phase commit, Sagas and compensation, 11.5A–11.5I, 11.6 Worked stale-lease/fencing timeline |
| Messaging and stream processing | Chapter 12: Queue, pub-sub and event log, Delivery semantics, Outbox, inbox and CDC, 12.1A–12.1H, 12.2 Message brokers and delivery semantics, 12.3 Event sourcing/CQRS/schema governance, 12.4 Consumer crash timeline |
| Scaling and overload | Chapter 13: Load balancing and consistent hashing, Overload controls, 13.1A–13.1G, 13.2 Admission control/load shedding/backpressure, 13.3 Hedged requests/adaptive concurrency |
| Reliability and recovery | Chapter 14: SLI, SLO, SLA and error budget, Recovery objectives, Zones, regions and disaster recovery, 14.1A–14.1G, 14.2 Recovery engineering, 14.3 Worked SLO and error-budget example |
| Architectural styles and evolution | Chapter 15: Monolith, modular monolith and microservices, Sidecars and service meshes, 15.1A–15.1H, 15.1I Architectural styles |
| Security and privacy | Chapter 16: Threat modeling, Authorization models, Tenant isolation, OAuth 2.0 and OpenID Connect, 16.2 Threat modeling a system architecture, 16.3 API threat patterns |
| Observability and operations | Chapter 17: RED and USE, Percentiles and cardinality, SLO-driven alerting, 17.1A–17.1I, 17.2 Observability in practice |
| Cloud and Kubernetes | Chapter 18: Containers and Kubernetes, 18.1A–18.1I, 18.2 Kubernetes architecture, 18.3 Service mesh, 18.4 IaC state and drift, 18.5 software supply-chain security |
| Patterns and anti-patterns | Chapter 19: Probabilistic data structures including Bloom-filter sizing, Distributed scheduling, Multi-tenancy, Multi-region consistency and routing, 19.2 Architecture pattern catalog |

## New additions in the current review pass
| Tail latency and duplicate work | Chapter 13, 13.3 | Explains hedged requests, cancellation, idempotency, shared bottlenecks and adaptive concurrency feedback | Validate against The Tail at Scale and verify workload-specific trade-offs |
| API threat patterns | Chapter 16, 16.3 | Adds object/function/property-level authorization, sensitive business flows, resource abuse, SSRF, unsafe upstream APIs and API inventory | Build a threat model and verify controls against the OWASP API Security Top 10 |
| Probabilistic structure sizing | Chapter 19, Bloom filter sizing subsection | Adds standard approximate false-positive and bit-budget formulas plus a million-item worked example | Independently recalculate formula and label assumptions clearly |
| Cache security and data lifecycle | Chapter 09, 9.3 | Covers tenant-aware cache keys, cache poisoning/deception, stale-while-revalidate/stale-if-error, permission revocation, deletion and privacy propagation | Verify against HTTP caching semantics and add a concrete cross-tenant test matrix |
| Event sourcing, CQRS and schema governance | Chapter 12, 12.3 | Distinguishes commands/events, event sourcing/notification, CQRS/read-model lag, projection rebuilds, schema compatibility and event-data privacy | Verify broker/registry-specific semantics and add a worked projection rebuild example |

| Addition | Location | Why it matters | Remaining verification |
|---|---|---|---|
| Architecture viewpoints and diagram selection | Chapter 01, 1.15 | Separates context, logical structure, runtime behavior, deployment, data ownership and trust boundaries instead of relying on one overloaded diagram | Validate diagram terminology and review the logical-versus-deployment example |
| Accessibility, usability and internationalization | Chapter 02, 2.19 | Makes critical user journeys, assistive technology, locale/time handling and accessible error behavior explicit quality attributes | Confirm conformance language against WCAG 2.2 and define project-specific targets |
| Operability, portability, cost and sustainability | Chapter 02, 2.20–2.21 | Adds lifecycle qualities and explains interactions between performance, cost, retention, resilience and environmental impact | Provider guidance is illustrative; validate measurable targets and avoid implying a single universal sustainability metric |
| Load, stress, spike, soak and scalability testing | Chapter 03, 3.17 | Connects estimates to reproducible evidence and explains open-loop/closed-loop traffic and coordinated omission | Review benchmark method and ensure a future worked test plan is concrete |
| Cancellation and structured task lifetime | Chapter 04, 4.16 | Distinguishes timeout from cancellation, rollback, and durable background work; covers deadline propagation and orphaned work | Verify runtime-specific examples and clearly label version-specific APIs |

## High-priority missing/depth risks

1. **Traffic-entry architecture:** load balancer, reverse proxy, API gateway, ingress, service mesh and CDN must be differentiated by responsibility and trust boundary.
2. **Architecture styles:** explain how to choose styles based on state ownership, deployment independence, consistency, team ownership and operational cost—not by trend.
3. **Data-model breadth:** explicitly compare relational, key-value, document, wide-column, graph, time-series, search, object, analytical and lake/warehouse choices.
4. **Failure and overload:** connect queues, timeouts, retries, circuit breakers, bulkheads, load shedding and autoscaling into one causal model.
5. **Security by design:** identity, authorization, tenant isolation, API abuse, secrets, network trust, data lifecycle and audit must appear throughout the system journey.
6. **Cloud-native delivery:** connect containers, orchestration, service discovery, configuration, health probes, rollout strategy, capacity and rollback.
7. **Worked examples:** each chapter should include at least one example that changes an assumption and shows how the design decision changes.

## Review rules

- A topic may have one primary home and several cross-links; avoid repeating the same textbook section in multiple chapters.
- Use standards and primary papers for protocol/theory claims, and official product documentation only for implementation-specific behavior.
- For every major component, teach purpose, internal mechanism, variants, selection criteria, trade-offs, failure modes, security, observability, scaling, and interactions.
- Add a diagram when it clarifies sequence, topology, state ownership, or failure behavior.
- Do not mark the textbook complete until every mandatory inventory row has an evidence-backed coverage status and technical verification.
