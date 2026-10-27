# Curriculum

The target is a compact set of connected notes, not a fixed chapter count. Merge topics when that makes the concepts easier to learn; split them only when a topic genuinely needs independent treatment.

## Core learning path

| # | Chapter | What you should be able to explain |
|---:|---|---|
| 1 | [System Design Foundations](chapters/01-foundations/README.md) | Clarify requirements, define scope, identify constraints, and sketch a high-level architecture. |
| 2 | [Capacity Estimation](chapters/02-capacity-estimation/README.md) | Estimate request rates, storage, bandwidth, and rough capacity; state assumptions clearly. |
| 3 | [APIs and System Boundaries](chapters/03-apis-and-boundaries/README.md) | Define responsibilities, API contracts, synchronous calls, and service boundaries. |
| 4 | [Data Modeling and Databases](chapters/04-data-modeling-and-databases/README.md) | Choose data models and storage systems based on access patterns and constraints. |
| 5 | [Caching](chapters/05-caching/README.md) | Explain cache-aside and related patterns, invalidation, TTLs, stampedes, and failure behavior. |
| 6 | [Scaling Traffic](chapters/06-scaling-traffic/README.md) | Explain load balancing, stateless services, horizontal scaling, and bottlenecks. |
| 7 | [Replication and Partitioning](chapters/07-replication-and-partitioning/README.md) | Explain replication lag, shard-key selection, hot partitions, consistent hashing, and safe rebalancing. |
| 8 | [Consistency and Transactions](chapters/08-consistency-and-transactions/README.md) | Reason about stale reads, concurrent writes, transactions, and consistency requirements. |
| 9 | [Asynchronous Processing](chapters/09-asynchronous-processing/README.md) | Choose queues, streams, and background jobs; explain retries, ordering, and idempotency. |
| 10 | [Reliability and Resilience](chapters/10-reliability-and-resilience/README.md) | Design bounded retries, isolation, graceful degradation, RTO/RPO, and multi-region failover without split brain. |
| 11 | [Security and Multi-Tenancy](chapters/11-security-and-multi-tenancy/README.md) | Cover authentication, authorization, isolation, secrets, and abuse controls at architecture level. |
| 12 | [Observability and Design Trade-offs](chapters/12-observability-and-trade-offs/README.md) | Use logs, metrics, traces, SLIs/SLOs, and a repeatable method to compare designs. |
| 13 | [Distributed Systems and Business Correctness](chapters/13-distributed-systems-and-correctness/README.md) | Reason about partial failure, CAP, quorums, delivery semantics, consensus, clocks, fencing, and business invariants. |
| 14 | [Networking, Request Routing, and Real-Time Systems](chapters/14-networking-and-real-time-systems/README.md) | Trace requests through DNS, edge, proxies, application dependencies, and real-time transports. |
| 15 | [Specialized Infrastructure](chapters/15-specialized-infrastructure-and-search/README.md) | Choose search, object storage, analytics, probabilistic structures, schedulers, CDC, and storage engines when justified. |
| 16 | [Interview Method and Estimation Workshop](chapters/16-interview-method-and-estimation-workshop/README.md) | Run a timed interview, estimate workload with units, and diagnose bottlenecks using observable signals. |
| 17 | [Senior Trade-offs and Case-Study Practice](chapters/17-senior-tradeoffs-and-case-study-path/README.md) | Defend conditional design choices, plan safe migrations, and practise canonical end-to-end problems. |

## Scope rules

- These chapters are a learning path, not a requirement to create twelve equally long chapters.
- Keep foundational ideas in the core notes. Put specialized details in short callouts or a future advanced supplement.
- Do not duplicate a full explanation across chapters; link back to the original explanation and focus on the new relationship.
- Add diagrams only when they clarify flow, ownership, or failure behavior.
- Include interview questions with explanatory answers, but avoid turning every chapter into an enormous question bank.
- Full end-to-end designs remain in [`../real-world-examples/README.md`](../real-world-examples/README.md); Chapter 17 provides a curated practice order without duplicating them.
- Networking, specialized infrastructure, real-time communication, and interview execution are covered in dedicated chapters 14–16; related tutorials remain deeper references.

## Completion criteria

A chapter is ready when:
- Its core concepts are accurate and explained in plain language.
- The reader can identify when to use the technique and its major trade-offs.
- Important failure modes are covered without drowning the reader in rare edge cases.
- Interview questions have direct, technically sound answers.
- Examples, diagrams, and internal links add value and work correctly.
