# Lesson 02.02 — Quality attributes need operational definitions

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


---

**Chapter:** [Requirements and Quality Attributes](README.md) · **Previous:** [Requirements define success](01-requirements-define-success.md) · **Next:** [Requirements-to-design traceability](03-requirements-to-design-traceability.md)
