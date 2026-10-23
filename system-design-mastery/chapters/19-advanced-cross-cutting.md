# 19. Advanced Cross-Cutting Reasoning

This final chapter connects mechanisms that are often taught separately but interact in production.

## Queueing and tail behavior
Little's Law relates average work in a stable system to arrival rate and average time: L = λW. It does not predict tail latency by itself. High utilization, bursty arrivals and variable service times can make waiting time rise nonlinearly. A queue buys time, not throughput; if arrivals persistently exceed service capacity, backlog grows without bound unless work is rejected, shed or capacity changes.

## Storage amplification and write paths
An LSM engine may reduce random in-place writes but create compaction work; a B-tree may maintain ordered pages but perform page splits and write amplification. Read, write and space amplification affect SSD endurance, latency and cost. The correct comparison uses realistic write sizes, update patterns, data sizes, cache state and read distributions rather than a single benchmark headline.

## Serialization and schema evolution
Serialization affects CPU, payload size, memory allocation, compatibility and observability. Schema evolution must account for producers and consumers deployed at different times. Additive fields can be compatible only if readers handle absent or unknown values safely. A field whose meaning changes is a breaking change even if its type remains identical.

## Probabilistic data structures
Bloom filters answer set-membership questions with possible false positives but no false negatives under standard assumptions and correct operation. A positive result means “possibly present,” not “definitely present.” They are useful when the cost of a false positive is an extra lookup and the cost of storing an exact set is high. Cardinality sketches and other approximate structures similarly trade exactness for bounded memory; their error properties and merge rules must be understood before use.

## Distributed scheduling
A distributed scheduler must consider ownership, duplicate execution, clock behavior, lease expiry, retries, missed runs and backfill. A scheduled job may run twice after a crash unless effects are idempotent or execution is coordinated. “Exactly once at the scheduled time” is generally not a realistic blanket guarantee; define whether the goal is at-least-once execution, at-most-once attempt, or one logical business effect.

## Multi-tenancy and noisy neighbors
Tenants share some combination of compute, connections, storage, caches, queues and control-plane resources. Isolation can be enforced through separate resources, quotas, workload pools, row-level policies or scheduling. Stronger isolation costs more; shared resources can be efficient but allow a noisy tenant to degrade others. Fairness policies need to define whether fairness means equal request count, CPU, latency or reserved capacity.

## Multi-region consistency and routing
Global traffic routing is only one part of multi-region architecture. Data placement, write ownership, replication lag, conflict resolution, regional failover, session guarantees and data residency all matter. DNS changes may not immediately affect existing connections or cached records. Active-active is not automatically more available if the write path requires global coordination or conflicting writes cannot be reconciled.

## Cost, complexity and evolution
A design should be evaluated on useful throughput, latency, correctness, availability, recovery, security, operating cost and change cost. A cheaper component can increase engineering burden; a managed service can reduce operational work while increasing provider dependence. Count failure modes and on-call complexity as real costs.

Prefer reversible decisions when uncertainty is high. Make irreversible or high-migration-cost choices only after validating the assumptions that drive them. Architecture should evolve from measured bottlenecks and changing requirements, not from novelty.

## Synthesis checklist
For any architectural decision, ask:
1. What requirement does it serve?
2. What workload and failure model are assumed?
3. What guarantee does it provide—and what does it not?
4. Where is the state of record?
5. What happens on timeout, duplicate, partition and recovery?
6. What is the effect on tail latency and overload?
7. How is correctness observed and tested?
8. What are the operational and financial costs?
9. How can the decision be rolled back or migrated?

## Further reading
- O'Neil et al., [LSM-tree paper](https://doi.org/10.1007/s002360050048).
- Google SRE [Handling Overload](https://sre.google/sre-book/handling-overload/).
- [Raft resources](https://raft.github.io/) for replicated coordination.
