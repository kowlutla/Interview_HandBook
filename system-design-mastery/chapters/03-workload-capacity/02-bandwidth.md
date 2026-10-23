# Lesson 03.02 — Bandwidth

## 3.4 Bandwidth

Assume peak traffic is approximately 1,736 requests/s and average response payload is 24 KiB = 24 × 1,024 = 24,576 bytes.

Payload egress ≈ 1,736 × 24,576 = 42,663,936 bytes/s ≈ 40.7 MiB/s ≈ 341.3 Mbit/s.

This excludes request payloads, protocol headers, TLS overhead, retransmissions, replication, and traffic between internal services. A network estimate that ignores response size can be wrong by orders of magnitude.


## 3.5 Storage growth

Assume 2 million new records/day, with 1.2 KiB of logical record data each.

Daily logical growth = 2,000,000 × 1.2 KiB = 2,400,000 KiB ≈ 2.29 GiB/day.
Annual logical growth ≈ 2.29 × 365 ≈ 835 GiB/year.

If a planning model uses a 2.5× multiplier for indexes, metadata, and operational overhead, one year's primary footprint is roughly 2.04 TiB before replicas and backups. The multiplier is a placeholder to be replaced by measurements from the selected schema and engine. If three full copies are retained, replicated capacity may approach 6.1 TiB, before backup retention and free-space requirements. Do not apply a replica multiplier twice if the original estimate already includes replicas.


## 3.6 Memory and cache sizing

If 5 million hot keys average 600 bytes of value data, raw values occupy 3,000,000,000 bytes, about 2.79 GiB. Real cache memory also includes key bytes, object/allocator overhead, hash-table slack, metadata, replication buffers, and fragmentation. The usable value capacity is therefore lower than physical RAM.

A cache hit ratio must specify what counts as a lookup. If 90% of 1,000 lookups/s hit, the backing store receives about 100 misses/s for that lookup class—unless misses trigger multiple backend operations or requests coalesce.


---

**Chapter:** [Workload and Capacity Estimation](README.md) · **Previous:** [Units and rates](01-units-and-rates.md) · **Next:** [Concurrency and Little's Law](03-concurrency-and-little-s-law.md)
