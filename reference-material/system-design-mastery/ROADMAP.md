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
**Read:** Chapters 15–20.

Study boundaries, evolution, security, observability, deployment, advanced cross-cutting concerns, and client-side/offline/real-time behavior as parts of one operating system—not isolated checklists.

**Checkpoint:** Defend an architectural decision by stating its context, alternatives, assumptions, failure modes, operational cost, and migration path. For a client-facing system, also explain which state is authoritative, how offline edits and reconnects are reconciled, and what delivery guarantees each real-time transport actually provides.

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


## Textbook completion workflow (quality gates)

The six learning passes above describe the reading order. They do not imply that the chapters are already complete. Before calling this a dependable reference, use the following editorial sequence:

### Gate A — Inventory-to-chapter audit

For every row in the mandatory topic inventory in `CURRICULUM.md`, record the exact chapter section that teaches it and classify coverage as:
- **Missing:** no meaningful explanation exists.
- **Mentioned:** named or briefly described, without enough mechanism or design reasoning.
- **Developing:** mechanism and trade-offs exist, but examples, edge cases, failure behavior, or operational guidance are missing.
- **Deep:** purpose, internals, variants, selection criteria, trade-offs, failure modes, security/operations where relevant, diagrams, and worked reasoning are present.

Do not mark a topic Deep merely because the phrase appears in a paragraph. Maintain an evidence-based gap list and resolve it chapter by chapter.

### Gate B — Expand by dependency order

Address foundational gaps before advanced topics: requirements and capacity; runtime and networking; traffic entry and APIs; data and storage; caching; distributed systems and coordination; messaging; scaling and resilience; architecture styles; security; operations; cloud delivery; cross-cutting patterns. This reduces duplicated explanations and avoids teaching a mechanism before its prerequisites.

### Gate C — Technical verification

For claims about protocols, consistency, security, or database behavior, use primary standards, papers, or official documentation. Label implementation-specific behavior and assumptions. Recalculate every numeric example and distinguish a protocol guarantee from a common implementation choice.

### Gate D — Pedagogical verification

For each major concept, check for: motivation, vocabulary, mechanism, a diagram, a concrete example, alternatives, when/when-not to use, failure modes, bottlenecks, observability, security implications where applicable, and a short self-check. Split a chapter into more Markdown files only when the coherent chapter page becomes unwieldy; do not fragment merely to create more files.

### Gate E — Repository and rendering verification

Check internal links, source links, heading structure, code fences, and Mermaid rendering. Verify that changes stay under `system-design-mastery/`. Keep the progress tracker honest: distinguish content drafted from content independently reviewed.

## Study routine
1. Read the chapter's motivation and mechanism.
2. Recreate its important diagram without looking.
3. Change one assumption in each worked example and recompute.
4. Describe one failure mode and the exact guarantee that is lost.
5. Follow at least one primary reference.
6. Mark a chapter complete only after its review checklist has been checked.
