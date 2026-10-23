# 3. Workload Models and Capacity Reasoning

Capacity estimation is a way to expose scale and bottlenecks before choosing infrastructure. It is not a promise of production performance. The output is a model whose assumptions can be measured and revised.

## 3.1 Units and rates

Use consistent units. One byte is 8 bits. Decimal storage units commonly use KB = 1,000 bytes, MB = 10^6 bytes, GB = 10^9 bytes; binary units use KiB = 1,024 bytes, MiB = 2^20 bytes, GiB = 2^30 bytes. State which convention is used.

A rate is quantity divided by time. Requests/s, MB/s, and events/s are not interchangeable; each event may have a different payload size and processing cost.

## 3.2 Average traffic and peak traffic

Suppose a service receives 30 million requests per day.

- Seconds/day = 86,400.
- Average rate = 30,000,000 / 86,400 ≈ 347 requests/s.
- If a measured peak-to-average factor is 5, peak estimate ≈ 1,735 requests/s.

The factor 5 is an explicit assumption, not a universal property. Traffic may be more bursty around releases, notifications, or daily batch jobs. Use time-series data when available.

Averages hide synchronized bursts. Capacity must be sized against the workload interval that matters, not just the daily mean.

## 3.3 Read/write mix

If 70% of 1,735 requests/s are reads:
- Reads ≈ 1,214.5/s.
- Writes ≈ 520.5/s.

This arithmetic does not imply equal resource cost. One write may update several indexes and replicas; one read may scan millions of rows. Request mix is a starting point, and operation-weighted CPU, I/O and lock demand matter more.

## 3.4 Bandwidth

Assume peak traffic is 1,735 requests/s and average response payload is 24 KiB = 24 × 1,024 = 24,576 bytes.

Payload egress ≈ 1,735 × 24,576 = 42,639,360 bytes/s ≈ 40.7 MiB/s ≈ 341 Mbit/s.

This excludes request payloads, protocol headers, TLS overhead, retransmissions, replication, and traffic between internal services. A network estimate that ignores response size can be wrong by orders of magnitude.

## 3.5 Storage growth

Assume 2 million new records/day, with 1.2 KiB of logical record data each.

Daily logical growth = 2,000,000 × 1.2 KiB = 2,400,000 KiB ≈ 2.29 GiB/day.
Annual logical growth ≈ 2.29 × 365 ≈ 835 GiB/year.

If a planning model uses a 2.5× multiplier for indexes, metadata, and operational overhead, one year's primary footprint is roughly 2.04 TiB before replicas and backups. The multiplier is a placeholder to be replaced by measurements from the selected schema and engine. If three full copies are retained, replicated capacity may approach 6.1 TiB, before backup retention and free-space requirements. Do not apply a replica multiplier twice if the original estimate already includes replicas.

## 3.6 Memory and cache sizing

If 5 million hot keys average 600 bytes of value data, raw values occupy 3,000,000,000 bytes, about 2.79 GiB. Real cache memory also includes key bytes, object/allocator overhead, hash-table slack, metadata, replication buffers, and fragmentation. The usable value capacity is therefore lower than physical RAM.

A cache hit ratio must specify what counts as a lookup. If 90% of 1,000 lookups/s hit, the backing store receives about 100 misses/s for that lookup class—unless misses trigger multiple backend operations or requests coalesce.

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
