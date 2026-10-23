# Lesson 03.03 — Concurrency and Little's Law

## 3.7 Concurrency and Little's Law

For a stable system, Little's Law states:

\[
L = \lambda W
\]

where L is average number of items in the system, λ is average arrival/completion rate, and W is average time in the system.

If a service completes 800 requests/s and average time in the system is 0.15 s, average in-flight requests are about 800 × 0.15 = 120. This is an average, not a maximum thread count or a safe pool size. Burstiness, queueing, service-time variance, and deadlines matter.

Little's Law applies to stable averages over a consistent boundary. If arrivals persistently exceed completions, backlog grows and the system is not in steady state.


## 3.8 Latency budgets and queueing

End-to-end latency includes network, queueing, application work, downstream calls, and response transfer. A budget might allocate 30 ms to edge/network, 40 ms to application work, 80 ms to data access, and 20 ms to serialization and response: total 170 ms. These are allocations, not guaranteed additive percentiles; correlated distributions and parallel branches make percentile composition subtle.

As utilization approaches a resource's effective capacity, queueing delay can rise sharply. Adding a queue does not create capacity; it can turn immediate rejection into delayed failure. Bound queues and deadlines, then decide which work to reject or shed.


---

**Chapter:** [Workload and Capacity Estimation](README.md) · **Previous:** [Bandwidth](02-bandwidth.md) · **Next:** [Sensitivity and sanity checks](04-sensitivity-and-sanity-checks.md)
