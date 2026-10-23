# 13. Scaling, Load Distribution, and Overload

## Scaling follows the constrained resource
Vertical scaling adds resources to a node; horizontal scaling adds nodes. Neither guarantees linear improvement. Shared locks, serial work, network traffic, hot keys, coordination and fixed-size dependencies limit gains. Amdahl's law captures one limit: accelerating only part of a workload cannot eliminate the serial fraction.

Stateless application instances are easier to scale because any healthy instance can serve a request. State still exists and needs deliberate shared or partitioned ownership.

## Load balancing and consistent hashing
Round-robin, least-connections, weighted routing, locality-aware routing and consistent hashing solve different problems. Health checks are imperfect observations: a process can answer a health endpoint but fail real requests.

Consistent hashing maps keys and nodes into a hash space; virtual nodes can improve distribution when nodes have unequal capacity. Rebalancing changes ownership and may trigger data movement. Hot keys remain hot even when the hash function distributes keys uniformly.

## Partitioning and skew
A useful partition key balances load while preserving locality for common queries. Tenant ID can be convenient, but one very large tenant may dominate a shard. Time-based keys can make recent writes hot. Salting spreads writes but complicates reads and aggregation. Uniform key count is not uniform work: one frequently updated record can dominate millions of rarely accessed records.

## Tail latency and fan-out
Latency is a distribution. p50 is the median; p95 and p99 reveal slow experiences. A request that depends on many independent calls can have poor tail behavior even if each dependency is usually fast. If all 20 calls must finish and each has a 99% chance of meeting a threshold, the chance all 20 meet it is approximately 0.99^20 = 81.8%. Independence is an assumption; correlated failure can be worse.

## Saturation and queue buildup
When arrivals exceed service capacity persistently, backlog grows. Even below nominal capacity, high utilization and variable service times can create large waiting times. A queue absorbs short bursts but adds latency and memory use. Bound queues and define rejection or load-shedding behavior.

## Overload controls
- **Admission control:** accept work only when capacity or policy allows.
- **Rate limiting:** cap work by client, tenant, resource or time window.
- **Backpressure:** signal upstream to slow down.
- **Load shedding:** reject lower-priority work to preserve critical paths.
- **Graceful degradation:** preserve core behavior while dropping optional work.
- **Bulkheads:** isolate pools so one workload cannot consume all resources.
- **Autoscaling:** add capacity based on signals, accounting for startup and warm-up delay.

Retries can worsen overload. Use bounded attempts and retry budgets, and avoid independent retry loops at every layer.

## Autoscaling and bottleneck diagnosis
Autoscaling depends on metrics, decision intervals, provisioning, startup and readiness. It cannot protect against every sudden burst and may overwhelm a fixed-capacity database as application replicas grow. Observe CPU, memory, I/O, network, queue depth, connection waits, lock waits, cache misses, query plans, errors and tail latency together.

A CPU-bound bottleneck may need algorithmic improvement; a lock bottleneck can worsen with more threads; a downstream cap may need admission control rather than more application instances.

## Further reading
- Google SRE [Handling Overload](https://sre.google/sre-book/handling-overload/).
- Google SRE [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
