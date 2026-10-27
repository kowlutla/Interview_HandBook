# System Design HLD Notes

A practical, concept-focused guide to the fundamentals of High-Level Design (HLD).

The goal is not to document every distributed-systems topic. It is to build the mental models needed to clarify requirements, choose suitable components, reason about trade-offs, and understand how an architecture behaves.

> **Editorial rule:** These are reference notes, not a question bank. Every section should explain a concept, design decision, mechanism, trade-off, failure mode, or worked example.

## How to use these notes

1. Learn the concept and the problem it solves.
2. Understand the basic flow before memorizing terminology.
3. Focus on when to use a technique, when not to use it, and its trade-offs.
4. Apply the concepts to the worked scenarios and end-to-end case studies.
5. Use the quick-revision section to revisit the core concepts.

## Chapter format

Most topics use this structure, adapting it when a section would add no value:

- **What and why** — definition and problem being solved.
- **How it works** — plain-language explanation and a simple diagram when useful.
- **Key choices** — patterns or options and when each fits.
- **Trade-offs and failure modes** — the most important costs, limitations, and risks.
- **Example** — one realistic example, only where it improves understanding.
- **Quick revision** — a compact recap.

## Chapters

1. [System Design Foundations](chapters/01-foundations/README.md)
2. [Capacity Estimation](chapters/02-capacity-estimation/README.md)
3. [APIs and System Boundaries](chapters/03-apis-and-boundaries/README.md)
4. [Data Modeling and Databases](chapters/04-data-modeling-and-databases/README.md)
5. [Caching](chapters/05-caching/README.md)
6. [Scaling Traffic](chapters/06-scaling-traffic/README.md)
7. [Replication and Partitioning](chapters/07-replication-and-partitioning/README.md)
8. [Consistency and Transactions](chapters/08-consistency-and-transactions/README.md)
9. [Asynchronous Processing](chapters/09-asynchronous-processing/README.md)
10. [Reliability and Resilience](chapters/10-reliability-and-resilience/README.md)
11. [Security and Multi-Tenancy](chapters/11-security-and-multi-tenancy/README.md)
12. [Observability and Design Trade-offs](chapters/12-observability-and-trade-offs/README.md)
13. [Distributed Systems and Business Correctness](chapters/13-distributed-systems-and-correctness/README.md)
14. [Networking, Request Routing, and Real-Time Systems](chapters/14-networking-and-real-time-systems/README.md)
15. [Specialized Infrastructure: Search, Files, Analytics, and Coordination](chapters/15-specialized-infrastructure-and-search/README.md)
16. [HLD Design Workflow and Estimation Workshop](chapters/16-interview-method-and-estimation-workshop/README.md)
17. [Senior Design Trade-offs and Case-Study Reference](chapters/17-senior-tradeoffs-and-case-study-path/README.md)

## Case-study learning path

Use the [curated case-study pathway in Chapter 17](chapters/17-senior-tradeoffs-and-case-study-path/README.md#173-curated-case-study-learning-path) alongside the canonical [45-case-study index](../real-world-examples/README.md). Attempt each design before reading the example; the notes teach the method while the examples remain the source for full walkthroughs.

## Supporting documents

- [Curriculum](CURRICULUM.md)
- [Editorial Standard](EDITORIAL-STANDARD.md)
- [Progress Tracker](PROGRESS.md)

## Scope boundaries

This guide focuses on HLD fundamentals. Deep implementation tutorials, exhaustive protocol specifications, niche specialist architectures, and large end-to-end case studies are intentionally out of scope for the core notes. They can be developed separately when needed.

## Status

Seventeen chapters now form the learning path, including dedicated material on distributed correctness, networking and real-time flows, specialized infrastructure, design workflow, estimation, and senior trade-offs. Content expansion is not the same as complete verification: consult [PROGRESS.md](PROGRESS.md) for checks actually performed. The existing `system-design-mastery/`, `tutorials/`, and `real-world-examples/` content remains a separate resource.
