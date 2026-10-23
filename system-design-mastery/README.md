# System Design Mastery
## A first-principles textbook for High-Level Design

This is an independent textbook for learning to reason about software systems: their requirements, workload, data, communication, failure modes, operational behavior, and evolution. It is not an index of interview questions and does not contain full end-to-end design case studies.

## Begin your journey
- **[Roadmap](ROADMAP.md)** — the learning sequence and prerequisites.
- **[Curriculum](CURRICULUM.md)** — the topic map, scope rationale, and coverage checks.
- **[Progress](PROGRESS.md)** — honest implementation and quality status.
- **[Glossary](GLOSSARY.md)** — precise shared terminology.
- **[Research library](references/README.md)** — standards, foundational papers, and technical documentation.
- **[Writing and verification standard](EDITORIAL-STANDARD.md)** — how claims, examples, diagrams, and reviews are handled.

## The textbook
1. [Thinking in systems and architecture](chapters/01-thinking-in-systems.md)
2. [Requirements and quality attributes](chapters/02-requirements-quality-attributes.md)
3. [Workload models and capacity reasoning](chapters/03-workload-capacity.md)
4. [Execution, concurrency, and resource limits](chapters/04-execution-concurrency.md)
5. [Networks and request journeys](chapters/05-networking.md)
6. [Interfaces and communication semantics](chapters/06-interfaces-communication.md)
7. [Data modeling and relational systems](chapters/07-data-relational.md)
8. [Storage engines and data-system choices](chapters/08-storage-engines-models.md)
9. [Caching and data locality](chapters/09-caching.md)
10. [Distribution, failure, and consistency](chapters/10-distributed-systems.md)
11. [Replication, coordination, and transactions](chapters/11-replication-coordination.md)
12. [Messaging, streams, and asynchronous workflows](chapters/12-messaging-streams.md)
13. [Scaling, load distribution, and overload](chapters/13-scaling-overload.md)
14. [Reliability, recovery, and service objectives](chapters/14-reliability-recovery.md)
15. [Architectural boundaries and evolution](chapters/15-architecture-evolution.md)
16. [Security, identity, and privacy](chapters/16-security-privacy.md)
17. [Observability and operating production systems](chapters/17-observability-operations.md)
18. [Cloud infrastructure and delivery](chapters/18-cloud-delivery.md)
19. [Cross-cutting advanced reasoning](chapters/19-advanced-cross-cutting.md)

## How to learn from this book
Read in order on the first pass. For each concept, ask: what problem does it solve, what assumptions does it require, what guarantee does it provide, how can it fail, and what trade-off does it introduce? Redraw diagrams from memory and recalculate examples after changing their assumptions.

The chapters intentionally distinguish abstract concepts from implementation-specific behavior. A protocol specification, a research result, a vendor's documentation, and a practitioner's recommendation are different kinds of evidence.

## Scope and repository boundary
This directory is the complete scope of the current learning phase: conceptual System Design and HLD fundamentals. Interview preparation and complete end-to-end system design exercises are future phases. Existing repository material is reference-only; this textbook has its own curriculum and editorial standards.
