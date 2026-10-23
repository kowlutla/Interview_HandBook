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
| Network fundamentals: IP, routing, TCP/UDP, DNS, TLS, HTTP | 05 | Developing | Expand practical protocols and troubleshooting; validate HTTP/2/3, QUIC, connection reuse, certificates, IPv6 and NAT details. |
| Load balancing, reverse proxies, ingress, global traffic management | 05, 13, 18 | Mentioned / Developing | Dedicated mechanism-level coverage: L4/L7, algorithms, health, draining, affinity, locality, TLS, failure modes, metrics. |
| CDN, edge delivery, origin shielding and invalidation | 05, 09 | Mentioned / Developing | Dedicated edge-cache behavior, cache-key correctness, stale content, purge, origin failover, security and cost. |
| API gateways and API management | 06 | Mentioned / Developing | Dedicated gateway responsibilities, limits, auth boundary, routing, transformation, high availability and failure policy. |
| API styles, contracts, retries, idempotency, streaming | 06 | Developing | Compare REST/RPC/gRPC/GraphQL/webhooks/WebSockets/SSE; deepen contract evolution and end-to-end deadlines. |
| Architectural styles and patterns | 01, 15, 19 | Developing | A systematic comparison of layered/N-tier, client-server, modular monolith, SOA, microservices, event-driven, hexagonal, pipe/filter, serverless, CQRS/event sourcing and hybrids. |
| Relational modeling, SQL, indexes, transactions | 07 | Developing | Validate examples; deepen query plans, isolation, constraints, migrations, operations and workload-based index selection. |
| NoSQL models, search, analytics, data lakes | 08, 19 | Mentioned / Developing | Give separate model-by-model comparison and explain search/indexing, analytical versus operational workloads, and selection boundaries. |
| Storage engines, WAL, B-tree, LSM, compaction | 08 | Developing | Add recovery/write-path examples and compare amplification and workload implications. |
| Caching at client, CDN, application and data layers | 09, 05 | Developing | Deepen strategies, stampede/penetration/avalanche, coherence, freshness contracts and outage protection. |
| Distributed failure, consistency, clocks, CAP/PACELC | 10 | Developing | Validate formal distinctions, add timelines/counterexamples, and make assumptions explicit. |
| Replication, consensus, leases, locks, fencing, transactions | 11 | Developing | Compare Raft/Paxos concepts, failover safety, 2PC/Saga and distributed lock limits with examples. |
| Queues, pub/sub, logs, Kafka, CDC and stream processing | 12 | Developing | Expand ordering, delivery, consumer recovery, event time, retention, schema evolution and replay examples. |
| Scaling, hashing, partitioning, hotspots, overload | 13 | Developing | Add worked algorithms, failure-domain capacity, admission control, load shedding and autoscaling pitfalls. |
| Reliability, SLOs, redundancy, backup/restore, DR | 14 | Developing | Add quantitative availability/recovery examples, restore testing, multi-region failure modes and incident workflows. |
| Security, identity, privacy, tenant isolation | 16 | Developing | Threat-model examples, authorization boundaries, secrets/key lifecycle, abuse controls and privacy lifecycle. |
| Observability and production operations | 17 | Developing | Deepen alert design, cardinality, sampling, tracing limitations, burn-rate alerts and runbooks. |
| Cloud, containers, Kubernetes, IaC and delivery | 18 | Developing | Expand scheduler/controller behavior, networking/storage, resource limits, deployment rollback and supply-chain security. |
| Cross-cutting patterns, cost, multi-tenancy and multi-region | 19 | Developing | Build a pattern catalog with context, forces, consequences, anti-patterns and interactions. |

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
