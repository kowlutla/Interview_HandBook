# Curriculum

The target is a compact set of connected notes, not a fixed chapter count. Merge topics when that makes the concepts easier to learn; split them only when a topic genuinely needs independent treatment.

## Core learning path

| # | Chapter | What you should be able to explain |
|---:|---|---|
| 1 | [System Design Foundations](chapters/01-foundations/README.md) | Clarify requirements, define scope, identify constraints, and sketch a high-level architecture. |
| 2 | Capacity Estimation | Estimate request rates, storage, bandwidth, and rough capacity; state assumptions clearly. |
| 3 | APIs and System Boundaries | Define responsibilities, API contracts, synchronous calls, and service boundaries. |
| 4 | Data Modeling and Databases | Choose data models and storage systems based on access patterns and constraints. |
| 5 | Caching | Explain cache-aside and related patterns, invalidation, TTLs, stampedes, and failure behavior. |
| 6 | Scaling Traffic | Explain load balancing, stateless services, horizontal scaling, and bottlenecks. |
| 7 | Replication and Partitioning | Explain why they are used, their trade-offs, and common operational challenges. |
| 8 | Consistency and Transactions | Reason about stale reads, concurrent writes, transactions, and consistency requirements. |
| 9 | Asynchronous Processing | Choose queues, streams, and background jobs; explain retries, ordering, and idempotency. |
| 10 | Reliability and Resilience | Design timeouts, retries, backoff, circuit breakers, rate limits, and graceful degradation. |
| 11 | Security and Multi-Tenancy | Cover authentication, authorization, isolation, secrets, and abuse controls at architecture level. |
| 12 | Observability and Design Trade-offs | Use logs, metrics, traces, SLIs/SLOs, and a repeatable method to compare designs. |

## Scope rules

- These chapters are a learning path, not a requirement to create twelve equally long chapters.
- Keep foundational ideas in the core notes. Put specialized details in short callouts or a future advanced supplement.
- Do not duplicate a full explanation across chapters; link back to the original explanation and focus on the new relationship.
- Add diagrams only when they clarify flow, ownership, or failure behavior.
- Include interview questions with explanatory answers, but avoid turning every chapter into an enormous question bank.
- End-to-end case studies (for example, URL shortener, chat, feed, or ride-hailing) are a separate future phase.

## Completion criteria

A chapter is ready when:
- Its core concepts are accurate and explained in plain language.
- The reader can identify when to use the technique and its major trade-offs.
- Important failure modes are covered without drowning the reader in rare edge cases.
- Interview questions have direct, technically sound answers.
- Examples, diagrams, and internal links add value and work correctly.
