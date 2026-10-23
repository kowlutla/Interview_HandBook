# Lesson 03.04 — Sensitivity and sanity checks

## 3.9 Sensitivity and sanity checks

Ask which assumptions dominate the result:
- If payload size doubles, bandwidth approximately doubles.
- If record count doubles, logical storage approximately doubles if record shape is stable.
- If peak-to-average ratio rises, average-based capacity may under-provision.
- If one operation causes ten database writes, request rate is not database operation rate.

Check units, orders of magnitude, and implied physical limits. Compare estimates with observed metrics and benchmark realistic workload mixes before committing to capacity or cost.


## Further reading
- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/).
- [Little's original law is often taught through queueing theory; a practical systems treatment appears in the SRE literature](https://sre.google/sre-book/table-of-contents/).


---

**Chapter:** [Workload and Capacity Estimation](README.md) · **Previous:** [Concurrency and Little's Law](03-concurrency-and-little-s-law.md)
