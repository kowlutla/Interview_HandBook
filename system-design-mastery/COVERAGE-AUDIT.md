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
| Systems thinking, boundaries, architecture decisions | 01 | Developing | Add worked boundary/decomposition examples and architecture evaluation techniques; verify all key concepts. |
| Requirements and quality attributes | 02 | Developing | Add concrete measurable scenarios, prioritization, and requirement-to-design examples. |
| Workload estimation and capacity | 03 | Developing | Add worked end-to-end sizing examples, queueing intuition, uncertainty ranges, and validation. |
| Execution, concurrency, runtime resources | 04 | Developing | Expand memory/GC, file descriptors, worker models, async/event loops, and resource isolation as needed. |
| Network fundamentals: IP, routing, TCP/UDP, DNS, TLS, HTTP | 05 — sections 5.1–5.18 | Developing | Sections 5.22 now add IPv6 coexistence, DNSSEC versus encrypted DNS, TLS/mTLS, HTTP/2 versus HTTP/3, and DDoS/resource-exhaustion distinctions. Still verify protocol details against the cited RFCs and add practical troubleshooting exercises. |
| Load balancing, reverse proxies, ingress, global traffic management | 05 — 5.19; 13 — Load balancing and consistent hashing, 13.1B; 18 — Cloud primitives | Developing | Dedicated mechanism-level coverage: L4/L7, algorithms, health, draining, affinity, locality, TLS, failure modes, metrics. |
| CDN, edge delivery, origin shielding and invalidation | 05 — 5.20; 09 — Local, distributed and CDN caches, 9.1F, 9.1G | Developing | Dedicated edge-cache behavior, cache-key correctness, stale content, purge, origin failover, security and cost. |
| API gateways and API management | 06 — 6.11 API gateways and API management | Developing | Dedicated gateway responsibilities, limits, auth boundary, routing, transformation, high availability and failure policy. |
| API styles, contracts, retries, idempotency, streaming | 06 | Developing | Section 6.12 now covers webhook signing, replay, idempotency, ordering, schema evolution, and SSRF. Continue verifying provider-specific contract caveats and add a worked OpenAPI/versioning example. |
| Architectural styles and patterns | 01, 15, 19 | Developing | A systematic comparison of layered/N-tier, client-server, modular monolith, SOA, microservices, event-driven, hexagonal, pipe/filter, serverless, CQRS/event sourcing and hybrids. |
| Relational modeling, SQL, indexes, transactions | 07 | Developing | Sections 7.2 now adds shard-key trade-offs, cross-shard operations and a safe resharding sequence. Continue validating isolation/query-plan examples and database-specific guarantees. |
| NoSQL models, search, analytics, data lakes | 08, 19 | Mentioned / Developing | Sections 8.2–8.7 now compare major storage families, derived search indexes, row/columnar and lakehouse workloads, materialized views, and distributed file/object/block semantics. Verify product-specific guarantees and add a comparative access-pattern example. |
| Storage engines, WAL, B-tree, LSM, compaction | 08 | Developing | Add recovery/write-path examples and compare amplification and workload implications. |
| Caching at client, CDN, application and data layers | 09, 05 | Developing | Deepen strategies, stampede/penetration/avalanche, coherence, freshness contracts and outage protection. |
| Distributed failure, consistency, clocks, CAP/PACELC | 10 | Developing | Section 10.18 now adds a write-timeout/read-replica timeline and explains why quorum arithmetic alone does not prove linearizability. Verify the consistency claims against primary literature and implementation contracts. |
| Replication, consensus, leases, locks, fencing, transactions | 11 | Developing | Compare Raft/Paxos concepts, failover safety, 2PC/Saga and distributed lock limits with examples. |
| Queues, pub/sub, logs, Kafka, CDC and stream processing | 12 | Developing | Expand ordering, delivery, consumer recovery, event time, retention, schema evolution and replay examples. |
| Scaling, hashing, partitioning, hotspots, overload | 13 | Developing | Add worked algorithms, failure-domain capacity, admission control, load shedding and autoscaling pitfalls. |
| Reliability, SLOs, redundancy, backup/restore, DR | 14 | Developing | Sections 14.2–14.3 now include availability composition, RTO/RPO, restore validation, and a worked request-based SLO/error-budget/burn-rate example. Continue checking measurement definitions and recovery assumptions. |
| Security, identity, privacy, tenant isolation | 16 | Developing | Threat-model examples, authorization boundaries, secrets/key lifecycle, abuse controls and privacy lifecycle. |
| Observability and production operations | 17 | Developing | Deepen alert design, cardinality, sampling, tracing limitations, burn-rate alerts and runbooks. |
| Cloud, containers, Kubernetes, IaC and delivery | 18 | Developing | Sections 18.2–18.5 now deepen Kubernetes, service mesh, IaC state/drift, SBOM, provenance, signing and build/deployment trust. Still verify supply-chain guidance against primary standards and test examples. |
| Cross-cutting patterns, cost, multi-tenancy and multi-region | 19 | Developing | Build a pattern catalog with context, forces, consequences, anti-patterns and interactions. |


## Exact section map for the current expansion pass

The following sections are present and are the starting points for the deeper review. “Present” does not mean technically verified or complete.

| Area | Exact chapter section(s) to review |
|---|---|
| Architecture reasoning | Chapter 01: 1.4, 1.6, 1.7, 1.9, 1.13, 1.14 |
| Measurable quality attributes | Chapter 02: 2.5–2.12, 2.15–2.18 |
| Workload and capacity | Chapter 03: 3.1–3.15, 3.16 Worked capacity example |
| Runtime and resource limits | Chapter 04: 4.1–4.14, 4.15 Runtime resource limits |
| Networking and request path | Chapter 05: 5.1–5.18, 5.19 Load balancers, 5.20 CDNs, 5.21 Network boundaries, 5.22 Protocol details and operational edge cases |
| API contracts and gateway | Chapter 06: 6.1–6.10H, 6.11 API gateways and API management, 6.12 Webhooks |
| Relational data and transactions | Chapter 07: Isolation anomalies, Optimistic versus pessimistic concurrency, Query planning, Safe schema migration, Relational systems in practice, 7.2 Sharding and resharding |
| Storage families and engines | Chapter 08: B-trees and LSM trees, 8.1A–8.1I, 8.2–8.6 data-system families/search/analytics/indexes, 8.7 Distributed file systems and object/block/file interfaces |
| Cache behavior | Chapter 09: Common patterns, TTL and invalidation, Failure modes, 9.1A–9.1H, 9.2 Cache patterns and failure modes |
| Distributed consistency | Chapter 10: Consistency models, CAP and PACELC, 10.7–10.18 including worked consistency timeline |
| Replication and coordination | Chapter 11: Leader election, Leases and fencing tokens, Two-phase commit, Sagas and compensation, 11.5A–11.5G, 11.6 Consensus and transaction boundaries |
| Messaging and stream processing | Chapter 12: Queue, pub-sub and event log, Delivery semantics, Outbox, inbox and CDC, 12.1A–12.1H, 12.2 Message brokers and delivery semantics |
| Scaling and overload | Chapter 13: Load balancing and consistent hashing, Overload controls, 13.1A–13.1G, 13.2 Admission control, load shedding, and backpressure |
| Reliability and recovery | Chapter 14: SLI, SLO, SLA and error budget, Recovery objectives, Zones, regions and disaster recovery, 14.1A–14.1G, 14.2 Recovery engineering, 14.3 Worked SLO and error-budget example |
| Architectural styles and evolution | Chapter 15: Monolith, modular monolith and microservices, Sidecars and service meshes, 15.1A–15.1H, 15.1I Architectural styles |
| Security and privacy | Chapter 16: Threat modeling, Authorization models, Tenant isolation, OAuth 2.0 and OpenID Connect, 16.2 Threat modeling a system architecture |
| Observability and operations | Chapter 17: RED and USE, Percentiles and cardinality, SLO-driven alerting, 17.1A–17.1I, 17.2 Observability in practice |
| Cloud and Kubernetes | Chapter 18: Containers and Kubernetes, 18.1A–18.1I, 18.2 Kubernetes architecture, 18.3 Service mesh, 18.4 IaC state and drift, 18.5 software supply-chain security |
| Patterns and anti-patterns | Chapter 19: Probabilistic data structures, Distributed scheduling, Multi-tenancy, Multi-region consistency and routing, 19.2 Architecture pattern catalog |

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
