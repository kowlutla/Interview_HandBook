# 7. Replication and Partitioning

Replication keeps copies of data on multiple nodes. Partitioning splits data across nodes. They solve different problems and are often used together.

## 7.1 Replication

Replication can improve availability, recovery, and read capacity. The exact benefits depend on how replicas are placed, updated, and promoted.

- **Primary/leader and replicas:** Writes go through a leader; replicas copy changes. This simplifies write ordering but can make the leader a bottleneck and replicas may lag.
- **Multi-leader:** Multiple nodes accept writes. This can help geographically distributed writes but requires conflict handling.
- **Leaderless/quorum-based designs:** Clients or coordinators interact with multiple replicas according to the database's protocol. Guarantees depend on read/write quorums, versioning, and conflict-resolution rules.

Do not assume replication automatically gives strong consistency or zero data loss. Understand the product's acknowledgement, durability, and failover semantics.

## 7.2 Synchronous versus asynchronous replication

**Synchronous replication** waits for one or more replicas to acknowledge before confirming a write. This can reduce the risk of losing acknowledged data, but increases latency and can reduce write availability when required replicas are unreachable.

**Asynchronous replication** acknowledges before all replicas catch up. It often lowers write latency and tolerates replica lag, but a failover may lose recent writes that had not reached the promoted replica.

Real systems often use intermediate policies, such as waiting for a configured subset of replicas. Always check what the acknowledgement actually guarantees.

## 7.3 Partitioning (sharding)

Partitioning divides a dataset into smaller pieces, often by a partition key. Each shard owns a subset of the data.

Common approaches:
- **Range-based:** Nearby key values live together. Range queries can be efficient, but skew or monotonically increasing keys can create hot partitions.
- **Hash-based:** A hash distributes keys more evenly, but range queries become harder.
- **Directory-based:** A lookup maps keys to shards, giving flexibility but introducing routing metadata and another dependency.

A good partition key distributes both data and traffic. Consider cardinality, skew, query patterns, growth, and whether common queries can be routed to a small number of shards.

## 7.4 Hot partitions and rebalancing

A shard can become hot if many requests target the same key or range. Adding more shards does not necessarily help when traffic is concentrated on one partition.

Possible mitigations include:
- Choosing a better partition key.
- Splitting a hot range or moving selected keys.
- Adding a controlled suffix/bucket for extreme hot keys, with more complex reads and writes.
- Caching very hot data.
- Applying per-tenant limits when one tenant dominates load.

Rebalancing moves data and load between nodes. It consumes network, disk, and CPU resources, so plans should account for migration, routing changes, rollback, and temporary capacity.

## 7.5 Cross-shard queries and transactions

Partitioning makes scale-out possible, but queries spanning many shards can require fan-out and aggregation. Cross-shard transactions may be more expensive or may not be supported by the selected system.

Try to align the partition key with common access patterns and transactional ownership. If a use case requires frequent global joins or atomic multi-entity updates, that is an important input to the data model and database choice.

## 7.6 Common interview questions

### What is the difference between replication and partitioning?

Replication creates multiple copies of the same data; partitioning divides the dataset into subsets. Replication is commonly used for availability, recovery, and reads. Partitioning is commonly used to distribute data and load beyond one node's capacity. A system may use both.

### Does a read replica guarantee fresh reads?

No. Asynchronous replicas can lag. If a user must read their own recent write, the system may route that read to the primary, wait for replication to catch up, or use a consistency mechanism supported by the database.

### How do you choose a shard key?

Choose a key with good distribution and cardinality that aligns with common queries and ownership boundaries. Avoid keys that concentrate traffic or data. Evaluate both storage balance and request distribution; they can differ.

### What is a hot shard?

A partition receiving disproportionate traffic or work. It can saturate even when the cluster has spare total capacity. Diagnose the key/range distribution and address the hotspot rather than simply adding nodes.

## Quick revision

- Replication copies data; partitioning divides it.
- Replication guarantees depend on acknowledgement and failover semantics.
- Synchronous replication trades latency/availability for stronger acknowledgement guarantees.
- Asynchronous replication can lose unreplicated recent writes during failover.
- A good shard key balances data and traffic while supporting important queries.
- Cross-shard operations and rebalancing add complexity.
