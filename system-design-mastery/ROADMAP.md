# Learning Roadmap

The curriculum is arranged around dependencies, not around technology popularity. First learn how to define and measure a problem; then understand execution and communication; then data; then distribution and failure; finally architectural composition and production operation.

## Pass 1 — Reason from requirements
**Read:** Chapters 1–3.

Learn to separate requirements from proposed solutions, identify constraints, describe quality attributes measurably, and estimate workload without false precision.

**Checkpoint:** Given a service description, state its important user-visible outcomes, assumptions, workload shape, bottlenecks to investigate, and unresolved questions.

## Pass 2 — Understand the machine and the network
**Read:** Chapters 4–6.

Understand concurrency, resource contention, network uncertainty, request lifecycles, interface contracts, timeouts, retries, and idempotency.

**Checkpoint:** Trace one request across client, DNS, transport, proxy, application, and data store. Explain why a timeout does not prove that the remote operation failed.

## Pass 3 — Understand data behavior
**Read:** Chapters 7–9.

Learn data modeling, transaction semantics, indexes, storage-engine trade-offs, and cache freshness before relying on distributed data systems.

**Checkpoint:** Choose a data model from access patterns and correctness needs; explain what happens when a cache is stale or a replica lags.

## Pass 4 — Understand distribution as uncertainty
**Read:** Chapters 10–12.

Start with partial failure and consistency models, then study replication and coordination, then asynchronous messaging and stream processing.

**Checkpoint:** Explain safety and liveness separately. Trace duplicate delivery, a partition, a leader change, and replay without assuming a single global clock or perfect failure detector.

## Pass 5 — Scale and survive
**Read:** Chapters 13–14.

Connect workload models to bottlenecks, queueing, overload, redundancy, recovery objectives, and service-level objectives.

**Checkpoint:** Identify where a system saturates first, why tail latency can rise before average latency looks alarming, and how overload controls preserve critical work.

## Pass 6 — Compose and operate
**Read:** Chapters 15–19.

Study boundaries, evolution, security, observability, deployment, and advanced cross-cutting concerns as parts of one operating system—not isolated checklists.

**Checkpoint:** Defend an architectural decision by stating its context, alternatives, assumptions, failure modes, operational cost, and migration path.

## Dependency sketch

~~~mermaid
flowchart TD
  A[Systems thinking] --> B[Requirements and quality]
  B --> C[Workload and capacity]
  C --> D[Execution and concurrency]
  D --> E[Networking]
  E --> F[Interfaces and communication]
  F --> G[Data modeling]
  G --> H[Storage engines]
  G --> I[Caching]
  H --> J[Distribution and consistency]
  I --> J
  J --> K[Replication and coordination]
  F --> L[Messaging and streams]
  K --> L
  C --> M[Scaling and overload]
  J --> M
  M --> N[Reliability and recovery]
  K --> N
  N --> O[Architecture and evolution]
  O --> P[Security and privacy]
  P --> Q[Observability and operations]
  Q --> R[Cloud delivery]
  R --> S[Advanced synthesis]
~~~

The diagram captures dominant prerequisites rather than every relationship. Security and observability should be considered from the beginning; their later chapters consolidate and deepen those concerns.

## Study routine
1. Read the chapter's motivation and mechanism.
2. Recreate its important diagram without looking.
3. Change one assumption in each worked example and recompute.
4. Describe one failure mode and the exact guarantee that is lost.
5. Follow at least one primary reference.
6. Mark a chapter complete only after its review checklist has been checked.
