# Independent Curriculum and Coverage Matrix

## Curriculum design principles

This curriculum starts from the work an architect must do: define the problem, reason quantitatively, understand execution and communication, choose data semantics, reason about distribution and failure, then compose and operate the system. Technology names are included where they illuminate a general mechanism; they do not determine the chapter order.

The existing repository was consulted only to understand the separation between fundamentals and future real-world examples. Its numbering, chapter names, and sequence are not the organizing basis for this curriculum.

## Coverage matrix

| Module | Essential coverage | Dependencies | Validation target |
|---|---|---|---|
| 01 — Thinking in systems | HLD vs LLD; boundaries and decomposition; architecture as constrained decision-making; assumptions, invariants, trade-offs, ADRs; monolith and distributed-system implications | Basic programming concepts | Explain why architecture is a set of decisions and constraints, not a diagram |
| 02 — Requirements and quality | Functional/non-functional requirements; scope; workload and user journeys; measurable quality attributes; latency, throughput, availability, reliability, durability, consistency, security, maintainability; constraints and priorities | M01 | Convert vague wishes into measurable targets and explicit trade-offs |
| 03 — Workload and capacity | Units, rates, powers of two; average/peak and burst traffic; read/write mix; concurrency; bandwidth; storage growth and overhead; memory/cache sizing; latency budgets; Little's Law; queueing and saturation; sensitivity, forecasting, cost | M02 | Worked estimates include assumptions, units, intermediate arithmetic and sanity checks |
| 04 — Execution and concurrency | Processes/threads; concurrency vs parallelism; scheduling/context switching; memory and resource limits; blocking/nonblocking; sync/async; CPU vs I/O bound; pools; locks, races, deadlocks; serialization | M03 | Explain how execution models alter throughput, latency and failure isolation |
| 05 — Networking | Layer models; IP/routing/subnets/NAT; TCP/UDP; handshakes, retransmission and congestion; DNS; TLS/certificates; HTTP/1.1, HTTP/2, HTTP/3; keep-alive/pooling/timeouts; packet loss and partitions; proxy/LB/CDN/edge/firewalls | M04 | Trace request and response path; distinguish protocol guarantees from deployment behavior |
| 06 — Interfaces and communication | REST/resource modeling; RPC/gRPC; GraphQL; WebSockets/SSE/long polling; sync/async and request/event; contracts, schemas, versioning, pagination, errors; gateway/discovery; timeout/retry/backoff/jitter; idempotency, throttling, compatibility | M05 | Explain how communication choice changes coupling, latency and retry safety |
| 07 — Data and relational systems | Data modeling, SQL, keys/constraints, normalization/denormalization, indexes and query plans, B-tree/hash alternatives, ACID, isolation, locks/deadlocks, pools, replicas/lag, partitioning/sharding, key choice/rebalancing, migration, backup/restore, retention | M03, M06 | Relate query patterns and correctness requirements to schema and index choices |
| 08 — Storage engines and models | Key-value, document, wide-column, graph, time-series, distributed SQL; object/block/file storage; distributed files; LSM and B-tree; compaction, amplification, durability and integrity; lifecycle | M07 | Compare by access pattern, data model, consistency and operational constraints |
| 09 — Caching and locality | Hierarchy, local/distributed, cache-aside/read-through/write-through/write-behind/write-around, keys/TTL, LRU/LFU, invalidation, stale data, stampede/penetration/avalanche/hot keys, sizing/hit rate, negative cache, coalescing, CDN, fallback | M03, M07 | Trace cache misses, stale reads and cache failure without hand-waving |
| 10 — Distribution and consistency | Partial failures, unreliable networks, partitions and detection, fault models, CAP/PACELC, strong/eventual/causal consistency, linearizability/sequential consistency, replication, quorum intuition, logical/vector clocks, clock skew, CRDTs, multi-region behavior | M05–M09 | State assumptions and client-visible guarantees; avoid CAP slogans |
| 11 — Replication and coordination | Leader election, Raft/Paxos concepts, safety/liveness, leases/fencing/split brain, distributed locks, 2PC, sagas/compensation, idempotency/deduplication, conflict resolution, exactly-once limitations | M10 | Describe safety conditions and failure cases for each mechanism |
| 12 — Messaging and streams | Queue/pub-sub/log; Kafka topics/partitions/offsets/producers/consumers/groups/lag/retention/replication; ordering; delivery semantics; retries/DLQ/poison/replay; idempotent consumer; outbox/inbox; CDC; event schema evolution; event sourcing/CQRS; windows and backpressure | M06, M10–M11 | Trace duplicate, reordered, delayed, replayed and poison events |
| 13 — Scaling and overload | Vertical/horizontal; statelessness/shared state; load-balancing; consistent hashing/virtual nodes; partitioning/skew/hot keys; locality; throughput/tail latency; saturation/queues/connection limits; backpressure/admission/load shedding/rate limits/autoscaling/degradation | M03, M09–M12 | Diagnose bottlenecks and second-order effects after a component scales |
| 14 — Reliability and recovery | Fault containment, redundancy/failover, health checks, circuit breakers/bulkheads/retry storms, graceful degradation, backup/restore, RTO/RPO, zones/regions, disaster recovery, chaos engineering, SLI/SLO/SLA/error budgets and incidents | M10–M13 | Derive recovery strategy from objectives and testable failure assumptions |
| 15 — Architecture and evolution | Monolith/modular monolith/SOA/microservices; DDD and bounded contexts; coupling and service boundaries; database per service; composition/orchestration; EDA; CQRS/event sourcing; saga/outbox; strangler; service discovery/config; sidecar/service mesh; control/data plane; multi-tenancy; debt and migration | M01, M06, M10–M14 | Explain prerequisites, fit, operational costs and when a pattern is unnecessary |
| 16 — Security and privacy | Authentication/authorization; sessions/cookies; OAuth 2.0/OIDC/JWT distinctions; IAM, RBAC/ABAC; TLS/encryption at rest; key/secrets management; least privilege/zero trust; threat modeling/trust boundaries; service identity; API abuse; tenant isolation, privacy, audit and retention | M05, M15 | Map threats to trust boundaries and controls; avoid confusing tokens with protocols |
| 17 — Observability and operations | Logs/metrics/traces; structured logs/correlation IDs/context propagation; RED/USE; percentiles; monitoring/alerts; SLI/SLO/SLA/error budgets; capacity diagnosis; incident analysis; readiness and ownership | M02, M14–M16 | Connect technical signals to user impact; discuss cardinality and sampling |
| 18 — Cloud and delivery | Cloud service models; compute/network/storage; regions/zones; ingress/LB/routing; containers/Docker; Kubernetes architecture, requests/limits/probes/autoscaling; managed vs self-hosted; IaC/config; CI/CD; rolling/blue-green/canary/flags/rollback; cost drivers | M04, M13–M17 | Relate deployment choices to failure domains, operability and cost |
| 19 — Advanced synthesis | Queueing/tail latency; storage amplification; serialization/schema compatibility; distributed scheduling; noisy neighbors; multi-region consistency/global routing; cost-performance-reliability-complexity frontier; architecture migration/evolution | M03–M18 | Integrate concepts into coherent, assumption-aware architectural reasoning |

## Completion checks

- [ ] All 19 modules have substantive chapters, not placeholder summaries.
- [ ] Each module includes mechanism, examples, trade-offs and failure modes appropriate to its topic.
- [ ] Technical claims have nearby citations to relevant primary sources where available.
- [ ] Worked calculations include units, assumptions and sanity checks.
- [ ] Distributed-systems claims distinguish safety, liveness, timing assumptions and implementation behavior.
- [ ] Diagrams are valid Mermaid and are explained in surrounding prose.
- [ ] Internal links resolve.
- [ ] Glossary terms match chapter usage.
- [ ] No interview Q&A bank or complete end-to-end HLD case studies have been introduced.
- [ ] A final path audit confirms all changes are inside this directory.
