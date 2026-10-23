# System Design Mastery
## A first-principles textbook for High-Level Design

This is an independent textbook for learning to reason about software systems: their requirements, workload, data, communication, failure modes, operational behavior, and evolution. It is not an index of interview questions and does not contain full end-to-end design case studies.

## Begin your journey
- **[Roadmap](ROADMAP.md)** — the learning sequence and prerequisites.
- **[Curriculum](CURRICULUM.md)** — the topic map, scope rationale, and coverage checks.
- **[Coverage audit](COVERAGE-AUDIT.md)** — initial chapter-by-chapter gap map and the standard for marking a topic deeply covered.
- **[Progress](PROGRESS.md)** — honest implementation and quality status.
- **[Glossary](GLOSSARY.md)** — precise shared terminology.
- **[Research library](references/README.md)** — standards, foundational papers, and technical documentation.
- **[Writing and verification standard](EDITORIAL-STANDARD.md)** — how claims, examples, diagrams, and reviews are handled.

## The textbook

Each chapter is a folder with a single, full-length Markdown chapter page (README.md). Chapters stay as one coherent reading experience unless a future chapter becomes too long to navigate comfortably. Diagrams use Mermaid where a sequence, boundary, or decision flow is clearer visually; animated behavior is represented with stepwise diagrams rather than decorative motion.

1. [Thinking in systems and architecture](chapters/01-thinking-in-systems/README.md)
2. [Requirements and quality attributes](chapters/02-requirements-quality-attributes/README.md)
3. [Workload models and capacity reasoning](chapters/03-workload-capacity/README.md)
4. [Execution, concurrency, and resource limits](chapters/04-execution-concurrency/README.md)
5. [Networks and request journeys](chapters/05-networking/README.md)
6. [Interfaces and communication semantics](chapters/06-interfaces-communication/README.md)
7. [Data modeling and relational systems](chapters/07-data-relational/README.md)
8. [Storage engines and data-system choices](chapters/08-storage-engines-models/README.md)
9. [Caching and data locality](chapters/09-caching/README.md)
10. [Distribution, failure, and consistency](chapters/10-distributed-systems/README.md)
11. [Replication, coordination, and transactions](chapters/11-replication-coordination/README.md)
12. [Messaging, streams, and asynchronous workflows](chapters/12-messaging-streams/README.md)
13. [Scaling, load distribution, and overload](chapters/13-scaling-overload/README.md)
14. [Reliability, recovery, and service objectives](chapters/14-reliability-recovery/README.md)
15. [Architectural boundaries and evolution](chapters/15-architecture-evolution/README.md)
16. [Security, identity, and privacy](chapters/16-security-privacy/README.md)
17. [Observability and operating production systems](chapters/17-observability-operations/README.md)
18. [Cloud infrastructure and delivery](chapters/18-cloud-delivery/README.md)
19. [Cross-cutting advanced reasoning](chapters/19-advanced-cross-cutting/README.md)


## Core building blocks covered

The curriculum explicitly covers the path from user to data and back: DNS, TLS, firewalls/WAF, reverse proxies, L4/L7 load balancers, API gateways, ingress, CDNs and edge caches; application runtimes and architecture styles; synchronous APIs and asynchronous messaging; relational and non-relational data stores; storage engines, caches, search and analytics; service discovery and configuration; service meshes; identity and authorization; observability; deployment, scaling, failover and disaster recovery.

A component's name appearing in a chapter is not considered sufficient coverage. Each important building block must be explained through its purpose, how it works, variants, when to use it, trade-offs, failure modes, security boundaries, metrics, and interactions with neighboring components. See the [mandatory topic inventory](CURRICULUM.md#mandatory-topic-inventory-coverage-audit).

## How to learn from this book
Read in order on the first pass. For each concept, ask: what problem does it solve, what assumptions does it require, what guarantee does it provide, how can it fail, and what trade-off does it introduce? Redraw diagrams from memory and recalculate examples after changing their assumptions.

The chapters intentionally distinguish abstract concepts from implementation-specific behavior. A protocol specification, a research result, a vendor's documentation, and a practitioner's recommendation are different kinds of evidence.

## Scope and repository boundary
This directory is the complete scope of the current learning phase: conceptual System Design and HLD fundamentals. Interview preparation and complete end-to-end system design exercises are future phases. Existing repository material is reference-only; this textbook has its own curriculum and editorial standards.
