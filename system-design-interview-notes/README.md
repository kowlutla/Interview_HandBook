# System Design Interview Notes

A practical, interview-focused guide to the fundamentals of High-Level Design (HLD).

The goal is not to document every distributed-systems topic. It is to build the mental models needed to clarify requirements, choose suitable components, reason about trade-offs, and explain an architecture clearly in an interview.

> **Editorial rule:** Every section must help the reader understand a concept, make a design decision, or answer an interview question. Keep the explanation detailed enough to build understanding, but short enough to revise.

## How to use these notes

1. Learn the concept and the problem it solves.
2. Understand the basic flow before memorizing terminology.
3. Focus on when to use a technique, when not to use it, and its trade-offs.
4. Practise answering the interview questions aloud.
5. Use the quick revision section before interviews.

## Chapter format

Most topics use this structure, adapting it when a section would add no value:

- **What and why** — definition and problem being solved.
- **How it works** — plain-language explanation and a simple diagram when useful.
- **Key choices** — patterns or options and when each fits.
- **Trade-offs and failure modes** — the most important costs, limitations, and risks.
- **Example** — one realistic example, only where it improves understanding.
- **Interview questions** — direct questions with explanatory answers.
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

## Supporting documents

- [Curriculum](CURRICULUM.md)
- [Editorial Standard](EDITORIAL-STANDARD.md)
- [Progress Tracker](PROGRESS.md)

## Scope boundaries

This guide focuses on HLD fundamentals. Deep implementation tutorials, exhaustive protocol specifications, niche specialist architectures, and large end-to-end case studies are intentionally out of scope for the core notes. They can be developed separately when needed.

## Status

The initial twelve chapter drafts now exist. Focused technical and link reviews are still required before calling the guide complete. The existing `system-design-mastery/` folder is intentionally left unchanged.
