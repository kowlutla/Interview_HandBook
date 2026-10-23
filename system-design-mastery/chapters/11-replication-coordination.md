# 11. Replication, Coordination, and Distributed Transactions

## Leader election is not enough
A leader coordinates writes or a replicated state machine. Election chooses a candidate, but the complete protocol must prevent stale leaders from committing conflicting state. A paused process may resume after its lease expired; believing it is leader does not make that belief valid.

Consensus algorithms such as Raft and Paxos coordinate agreement despite specified failures. Guarantees depend on assumptions including non-Byzantine participants, durable state, quorum membership and correct implementation. Raft separates leader election, log replication and safety; it is not simply the node with the most votes. See [Raft resources](https://raft.github.io/).

## Leases and fencing tokens
A lease grants ownership for a bounded interval under a clock or coordination model. A paused process can outlive its lease from its own perspective. Fencing tokens address stale ownership by attaching an ordered token to operations; the protected resource rejects tokens older than the latest accepted token. The resource must enforce fencing—having a lock service issue tokens is insufficient if the database accepts stale writes.

## Distributed locks
A distributed lock is useful only when ownership and expiry semantics match the protected operation. A lock alone may not prevent stale writes during partitions, pauses or lease expiry. Prefer idempotent operations and resource-enforced version checks where possible.

## Two-phase commit
Two-phase commit coordinates a transaction across participants:
1. **Prepare:** participants prepare and record enough state to commit or abort.
2. **Decision:** the coordinator records and communicates commit or abort.

2PC can preserve atomic commit under its assumptions, but a participant may block while coordinator or communication is unavailable. Logging, recovery, timeouts and coordinator failover matter.

## Sagas and compensation
A saga decomposes a business workflow into local transactions with compensating actions. Compensation is not always a perfect inverse: a shipped parcel cannot literally be unshipped, and a refund is a new business event rather than erasure of a charge. Sagas trade one global atomic commit for explicit workflow state, retries, idempotency and compensation.

Orchestration centralizes workflow decisions; choreography distributes reactions through events. Both need explicit timeouts, duplicate handling, terminal states and observability.

## Idempotency and deduplication
At-least-once delivery can produce duplicates. Deduplication stores a message ID or business idempotency key with the effect. To close crash windows, the deduplication record and business state change should be atomic in one transactional boundary or coordinated by an equivalent protocol.

A broker's exactly-once feature generally applies to a defined scope. It does not automatically make arbitrary external side effects exactly once. Always name the boundary and failure model.

## Reconfiguration and split brain
Membership changes alter which nodes form a quorum. Safe protocols constrain how old and new configurations overlap. Independently changing replica membership can create two groups that each believe they have authority. Split brain is conflicting authority that permits divergent commits, not merely duplicate leader processes.

## Further reading
- [Raft paper and resources](https://raft.github.io/).
- Fischer, Lynch and Paterson, [consensus impossibility result](https://doi.org/10.1145/3149.214121).
