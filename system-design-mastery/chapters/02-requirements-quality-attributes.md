# 2. Requirements and Quality Attributes

## 2.1 Requirements define success

A functional requirement states what the system must do: create an order, retrieve a profile, or publish a notification. A non-functional requirement (NFR) describes a property of that behavior, such as latency, availability, privacy, durability, or accessibility. The distinction is useful but not absolute: “a user can export data within 30 seconds” combines a function and a performance target.

Requirements should be testable. “Fast” is not testable until the operation, workload, percentile, and measurement boundary are stated. “Highly available” needs a success definition and time window. “Secure” needs assets, threats, trust boundaries, and controls.

## 2.2 Define scope and assumptions

Write down:
- Users, clients, and important workflows.
- In-scope and explicitly out-of-scope behavior.
- Data created, read, updated, deleted, retained, and exported.
- Expected traffic, burstiness, geography, and growth.
- Compliance, budget, team, technology, and migration constraints.
- Dependencies and the behavior expected when each is unavailable.

An assumption is not a fact. Record it with a validation path. If an assumption strongly affects the architecture, model alternative values instead of silently committing to one.

## 2.3 Quality attributes need operational definitions

| Attribute | Working meaning | Useful question |
|---|---|---|
| Latency | Elapsed time for a defined operation | Which percentile and end-to-end boundary? |
| Throughput | Useful work completed per unit time | At what workload and error rate? |
| Availability | Fraction of time or requests meeting a success criterion | What counts as success, and over which window? |
| Reliability | Ability to perform correctly over time and under stated conditions | Which failure modes and correctness properties? |
| Durability | Persistence of acknowledged committed state under a defined failure model | What failures must acknowledged data survive? |
| Scalability | Ability to handle growth in workload/resources while preserving targets | What grows, and how does cost change? |
| Consistency | Rules governing values and operation order visible to clients | Which reads may observe which writes? |
| Maintainability | Ease and safety of understanding, changing, testing, and operating the system | How costly is a typical change? |
| Security | Protection against defined threats and unauthorized actions | Which actors can do what to which assets? |
| Recoverability | Ability to restore service/data after disruption | What are RTO and RPO? |

These terms are related but not interchangeable. A database may be durable but temporarily unavailable. A service can be available while returning stale results. A system can have high throughput but poor tail latency.

## 2.4 Make objectives measurable

A performance objective might state: “For authenticated profile reads at the public API boundary, p99 latency is below 250 ms at 2,000 requests/s under the defined mix, excluding client-network time.” This identifies operation, percentile, load, and boundary. It still needs a measurement window, error budget, and test environment.

For availability, define both success and denominator. Counting only server 5xx responses can conceal timeouts, incorrect responses, or failed client-visible workflows. A service-level indicator (SLI) should approximate what users experience.

## 2.5 Understand trade-offs explicitly

Quality attributes often conflict:
- Stronger synchronous validation may increase latency and couple availability to more dependencies.
- More replicas can improve read capacity and failure tolerance but create replication lag or write coordination costs.
- Encryption and authorization checks add work but are requirements, not optional optimizations; performance must be engineered around them.
- Longer retention improves auditability and replay but increases storage, privacy exposure, and deletion obligations.

Use priorities and thresholds. Not every attribute must be maximized; some are constraints, while others are optimization goals.

## 2.6 Requirements-to-design traceability

For each critical requirement, document:
1. Metric and threshold.
2. Architecture mechanism intended to satisfy it.
3. Assumptions and dependencies.
4. Validation method.
5. Failure mode if the mechanism does not hold.

Example: a p99 latency target might motivate a bounded database connection pool, cache for repeated reads, and an end-to-end deadline. Each mechanism needs tests: cache-miss behavior, pool saturation, dependency timeout, and cold-start behavior.

## 2.7 Questions that expose ambiguity

- Is the read allowed to be stale? If so, by how much?
- Does a successful response mean data is durably committed?
- What happens if a request times out after the server commits it?
- Are workloads steady, bursty, seasonal, or synchronized?
- What is the impact of losing one zone, one region, or a dependency?
- How are deletion, audit, retention, and recovery reconciled?
- Which failure is acceptable, and which must be prevented?

## Further reading
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — reliability objectives and operational practice.
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — quality attribute trade-offs.
