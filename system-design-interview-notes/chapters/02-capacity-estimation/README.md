# 2. Capacity Estimation

Capacity estimation helps you check whether a proposed architecture is plausible. Early design estimates do not need to be exact; they need clear assumptions, correct units, and enough accuracy to guide decisions.

## 2.1 Estimation targets

Start with only the quantities that affect the design:

- Requests per second (average and peak).
- Read/write ratio.
- Data stored per day and over the retention period.
- Approximate bandwidth.
- Rough concurrency or number of active connections.
- Replication and redundancy overhead, when relevant.

Do not calculate every quantity by default. Estimate what helps you choose or size components.

## 2.2 Convert daily requests to requests per second

`Average RPS = Requests per day ÷ 86,400`

Example: assume a service receives 100 million requests per day.

`100,000,000 ÷ 86,400 ≈ 1,157 average requests/second`

If peak traffic is assumed to be 3 times the average:

`Peak RPS ≈ 1,157 × 3 ≈ 3,471`

The peak multiplier is an assumption, not a universal constant. Real traffic can be much more bursty, so state the assumption and revise it if the workload suggests otherwise.

## 2.3 Estimate storage

A useful first approximation is:

`Daily storage = Records per day × Average stored size per record`

Example: 5 million records/day at an average of 2 KB each:

`5,000,000 × 2 KB ≈ 10 GB/day`

For 90 days, raw retained data is approximately 900 GB, before indexes, metadata, replication, compression, and storage-system overhead.

Be explicit about units:
- Decimal: 1 GB = 1,000 MB.
- Binary: 1 GiB = 1,024 MiB.

For rough design estimates, approximate values are fine when the unit convention is consistent.

## 2.4 Estimate bandwidth

`Bandwidth ≈ Requests per second × Average bytes transferred per request`

If a service handles 2,000 responses/second averaging 50 KB each:

`2,000 × 50 KB = 100,000 KB/s ≈ 100 MB/s`

This is an approximate payload rate. Real network usage includes request bodies, headers, protocol overhead, retries, and traffic in both directions. If requests and responses differ greatly in size, estimate ingress and egress separately.

## 2.5 Estimate concurrency with Little’s Law

Little’s Law states:

`L = λ × W`

Where:
- `L` is the average number of items in the system.
- `λ` is the average arrival rate.
- `W` is the average time an item spends in the system.

If a service receives 1,000 requests/second and average response time is 0.2 seconds:

`Average in-flight requests ≈ 1,000 × 0.2 = 200`

This estimates average concurrency under stable conditions. It is not by itself a thread-pool size or server-count formula; resource usage and tail latency must also be considered.

## 2.6 Turn estimates into design decisions

Use the estimates to test the design:
- Whether one database instance can plausibly handle the write rate and data size.
- Whether read volume justifies caching.
- Whether payloads make bandwidth or object storage a dominant concern.
- Whether traffic peaks require buffering or autoscaling.
- Whether retained data calls for partitioning, archival, or expiration.
- Whether the latency budget makes synchronous fan-out risky.

Avoid pretending rough estimates produce exact infrastructure sizing. Actual capacity depends on workload shape, data distribution, query complexity, hardware, implementation, and performance testing.

## 2.7 Common mistakes

- Confusing average RPS with peak RPS.
- Forgetting the number of seconds in a day (86,400).
- Ignoring read/write ratios and request payload sizes.
- Treating KB, MB, GB and KiB, MiB, GiB as interchangeable without stating assumptions.
- Multiplying raw data size by an arbitrary overhead factor without explaining why.
- Assuming a single benchmark translates directly to production capacity.
- Giving a number without showing the assumptions or arithmetic.

## Quick revision

- Average RPS = daily requests ÷ 86,400.
- Peak RPS = average RPS × an explicitly stated peak factor.
- Daily storage = records/day × average record size.
- Bandwidth ≈ RPS × bytes/request.
- Little’s Law: average concurrency = arrival rate × average time in system.
- Estimates guide architecture; measurements validate capacity.

## Further reading

- [Little's Law (overview)](https://en.wikipedia.org/wiki/Little%27s_law)
- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/)

## Worked concurrency example

Little's Law is (L = \lambda W): average work in the system equals throughput multiplied by average time in the system, when the system is stable and units match. At 600 requests/second and 0.2 seconds average response time, average in-flight requests are approximately (600 \times 0.2 = 120). This is not a thread-pool sizing rule: tail latency, bursts, queueing, and time spent holding scarce resources matter.

```mermaid
flowchart LR
    A[Daily volume] --> B[Divide by 86,400]
    B --> C[Average RPS]
    C --> D[Apply stated peak factor]
    D --> E[Peak RPS estimate]
    E --> F[Load test and identify bottleneck]
```

## Scenario analysis

**Case:** A service averages 1,000 requests/second but experiences short spikes to 5,000 requests/second; capacity has been planned using only average traffic.

**Reasoning:** Not if the latency/availability objective must hold during the spike. Estimate the duration and burst shape, determine whether queues are acceptable, and measure per-instance capacity under realistic dependencies. Keep headroom or autoscale early enough; autoscaling cannot react instantly to every spike. If the database saturates first, adding API instances can worsen the incident.

## Further reading

- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/) — overload behavior and graceful protection.
