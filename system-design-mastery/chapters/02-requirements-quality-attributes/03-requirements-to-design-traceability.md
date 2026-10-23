# Lesson 02.03 — Requirements-to-design traceability

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


---

**Chapter:** [Requirements and Quality Attributes](README.md) · **Previous:** [Quality attributes need operational definitions](02-quality-attributes-need-operational-definitions.md)
