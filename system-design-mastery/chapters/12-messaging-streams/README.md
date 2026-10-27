# 12. Messaging, Streams, and Asynchronous Workflows

Messaging lets one part of a system hand work or information to another without requiring both to complete the same request together. This reduces temporal coupling and can absorb bursts, but it changes when failures appear: a request may be accepted now and fail later, messages may be delivered more than once, and consumers may fall behind.

The key is to understand the contract the messaging system provides—and the parts your application must still handle.

## 12.1 Queue, pub/sub, and event log

These models solve related but different problems:

- A **work queue** distributes tasks among workers. A task is generally handled by one worker in the relevant consumer group.
- **Publish-subscribe** lets multiple independent subscribers receive an event.
- A **durable event log** retains records in an ordered sequence within each partition. Consumers track their own positions and may replay retained history.

Products can combine these models, so compare their actual persistence, routing, acknowledgement, retention, ordering, and recovery behavior rather than relying on the product category.

Use a queue when work needs to be completed, pub/sub when independent components need the same notification, and a durable log when replay and consumer-controlled progress matter. None of these choices automatically makes a business operation happen exactly once.

## 12.2 Partitions, ordering, and consumer progress

Kafka organizes records into topics and partitions. Order is defined within a partition, not across every partition in a topic. A consumer group distributes partitions among its members; adding consumers helps only when enough partitions and downstream capacity allow more parallel work.

Choose the partition key around the entity whose events must remain ordered—for example, an order or account. A poor key can concentrate traffic on a small number of partitions. Adding partitions may also change key-to-partition mapping for some partitioning strategies, so consider how that affects ordering and stateful consumers.

A consumer's committed offset records its progress through a partition. Be precise about what the offset represents: a record has an offset, while the committed consumer position typically points to the next record to read. For example, after processing record offset 812, a consumer commonly commits position 813 as the next offset to consume. Consumer restarts and group rebalances can cause records to be processed again if the external side effect and progress update are not coordinated.

**Consumer lag** is the gap between the latest available data and a consumer's progress. Count alone is not enough: a thousand expensive events may take longer than a million tiny ones. Monitor lag age, arrival and processing rates, failures, batch size, and estimated drain time. If events arrive faster than the system can process them for a sustained period, the backlog will keep growing.

See the versioned [Kafka 4.3 design documentation](https://kafka.apache.org/43/design/design/) and [message delivery semantics](https://kafka.apache.org/43/design/design/#message-delivery-semantics) for Kafka-specific behavior; verify details against the broker and client versions actually deployed.

### Producer acknowledgements, replication, and durability

A successful producer send means only what the broker and producer configuration define. In Kafka, `acks=0` does not wait for a broker acknowledgement; `acks=1` waits for the leader to acknowledge the record; and `acks=all` waits for the current in-sync replica set to acknowledge it. For `acks=all`, `min.insync.replicas` can require a minimum number of in-sync replicas for the write to be accepted. If that minimum cannot be met, the write may fail rather than silently weakening the configured acknowledgement policy.

These settings are not interchangeable with a blanket durability guarantee. The effective risk also depends on replication factor, in-sync replica health, leader-election policy, broker/storage behavior, producer retries and idempotence, and whether the application treats an ambiguous timeout as a possible successful append. Acknowledgement from the leader is not the same as every replica being current, and replication is not a backup against accidental deletion or application-level corruption.

Idempotent producer support can suppress duplicate appends caused by supported producer retries, but it does not deduplicate two separately issued application commands that represent the same business operation. Use a stable operation/event identity when application retries must refer to the same logical action. Define how the producer recovers from a timeout where the append may have succeeded, and test broker failover while writes are in flight.

### Dead-letter queues, ordering, and replay safety

A dead-letter queue (DLQ) isolates records that cannot currently be processed, but moving a failed record aside can change observable ordering. If events for one aggregate must be applied in order, processing later events while an earlier event is quarantined may leave the aggregate in an invalid state. Decide whether to pause that partition/key, route later events to a holding area, or permit out-of-order progress under an explicit domain rule.

A DLQ record should retain enough safe diagnostic context to investigate and replay it: original topic/queue, partition and offset or message ID, event type/schema version, failure category, attempt history, and relevant correlation identifiers. Avoid copying secrets or unnecessary personal data into the DLQ. Give the queue an owner, retention policy, alerting threshold and documented remediation process.

Replay is a new execution attempt, not merely moving bytes back to the original queue. Confirm whether downstream effects already happened, preserve the original event identity when deduplicating the same logical event, and use a deliberate replay strategy that avoids overwhelming consumers or violating ordering. If a corrected event is a genuinely new business fact, assign a new identity and maintain a traceable relationship to the original. Test duplicate replay, partial prior success, poison records and per-key ordering.
### Consumer-group rebalances, lag and offset correctness

A partitioned log assigns each partition to a consumer within a consumer group, so one partition is normally processed by only one active member of that group at a time. Membership changes, slow processing, session timeouts and deployments can trigger a rebalance. Rebalances are not merely a throughput event: they change which worker is allowed to advance progress for a partition and can expose duplicate work or stalled partitions if application processing is not designed for ownership changes.

Treat the committed offset as a recovery checkpoint, not as proof that a business effect happened exactly once. If a worker commits an offset before the corresponding effect is durable, a crash can skip the effect on restart. If it commits after the effect, a crash between the effect and offset commit can repeat the effect. The downstream operation must therefore be idempotent or transactionally coupled to the checkpoint where the chosen platform supports that coupling.

Operationally, distinguish **consumer lag** (how far behind the group is) from **time to drain** (how long the current backlog will take to process at sustainable net throughput). Lag alone does not identify whether the cause is a traffic spike, a hot partition, slow dependency, repeated failures, an oversized batch, or insufficient partition-level parallelism. Alert on lag age and growth, processing latency, rebalance frequency, failed/retried records, and estimated drain time—not only one absolute lag threshold.

A safe consumer should:
- stop accepting new work when partition ownership is being revoked, and finish or safely abandon in-flight work within a bounded shutdown budget;
- commit only progress that matches the application's durable processing boundary;
- tolerate replay after process loss, rebalance, timeout, or uncertain commit response;
- bound work per poll/batch so slow downstream calls do not cause avoidable membership churn;
- test rolling deployment, long processing pauses, partition reassignment, consumer crash after effect-before-commit, and commit-response loss.

These are general design principles; exact rebalance protocols, offset APIs, and timeout interactions vary by broker and client version. Verify them against the deployed client documentation instead of assuming all Kafka clients behave identically.

## 12.3 Delivery guarantees and idempotent effects

Messaging systems commonly describe delivery as at-most-once, at-least-once, or exactly-once within a defined boundary.

- **At-most-once** avoids redelivery under the chosen acknowledgement contract, but a failure may lose work.
- **At-least-once** retries or redelivers work under the system's assumptions, so duplicates are possible.
- **Exactly-once** is a scoped guarantee, not a blanket promise that every downstream side effect happens once.

The central question is: *what happens if the consumer performs the work but crashes before recording its progress?*

If a consumer writes to a database and then acknowledges the message, a crash between those actions may cause the write to be repeated. If it acknowledges first and crashes before the write, the work may be lost.

~~~mermaid
sequenceDiagram
  participant B as Broker
  participant C as Consumer
  participant D as Database
  B->>C: Deliver event
  C->>D: Commit business change
  D-->>C: Commit succeeds
  Note over C,B: Consumer crashes before acknowledging
  B->>C: Redeliver event after restart
  C->>D: Process same event again
~~~

A robust consumer makes repeated delivery safe. Common approaches include a stable event or operation ID, a deduplication record committed in the same transaction as the business change, conditional updates, or an idempotent state transition. The deduplication record must be retained for the relevant replay/redelivery horizon, and concurrent deliveries must not race past the check.

Broker-level transactions can coordinate particular broker operations, such as consuming records and producing new records. They do not automatically include an external payment provider, email system, or arbitrary database transaction. Always name the boundary of an exactly-once claim.

### Kafka's exactly-once boundary

Kafka-specific delivery claims need to name both the producer/consumer settings and the boundary of the effect. Kafka provides an idempotent producer mode that uses producer identity and sequence information to suppress duplicate writes caused by producer retries within the protocol's supported scope. This does not mean an application can retry an entire business command indefinitely without creating a second logical event: the application still needs stable command/event identity and a policy for uncertain outcomes.

Kafka transactions can atomically commit records across multiple Kafka partitions and coordinate consumed offsets with produced Kafka records. A downstream consumer that must hide aborted transactional output needs a compatible read-committed isolation setting. This supports Kafka-to-Kafka processing patterns, but an arbitrary SQL transaction, payment API call, email send or third-party side effect is not automatically part of the Kafka transaction.

Consider a consumer that reads an order event, writes a payment row to PostgreSQL, and then commits the Kafka offset. If the database commit succeeds and the process crashes before the offset is committed, Kafka can deliver the event again. A Kafka transaction cannot roll back that already committed PostgreSQL row. Use a database transaction with a unique event/operation key, a conditional state transition, an inbox/deduplication record, or a purpose-built connector/sink that explicitly coordinates the supported boundary.

Before describing a pipeline as exactly-once, write down:
1. Which records and offsets participate in the atomic transaction.
2. Which consumer isolation level exposes transactional output.
3. How application-level retries are assigned stable identities.
4. Which external effects occur outside the broker transaction.
5. How a crash after an external commit but before offset progress is recovered.
6. Which broker/client versions and settings the guarantee assumes.

See the versioned [Kafka 4.3 message delivery semantics](https://kafka.apache.org/43/design/design/#message-delivery-semantics) and [transaction design](https://kafka.apache.org/43/design/design/#using-transactions); verify the behavior against the deployed client and broker configuration.

## 12.4 Retries, poison messages, and backpressure

Retries help with transient problems such as temporary network failures or rate limits. They do not fix invalid data or a permanently impossible business state. Use bounded attempts, exponential backoff and jitter, and distinguish retryable from terminal errors.

A message that repeatedly fails is often called a poison message. A dead-letter queue or quarantine store can preserve it for investigation, but it is not a repair strategy by itself. Someone must own the failure, understand the cause, correct the data or code, and decide whether replay is safe. Replaying a message may repeat external side effects.

Backpressure and concurrency limits protect consumers and their dependencies. Bound in-flight messages, batch size, database connections, and worker concurrency. A larger prefetch window may improve throughput, but it consumes more memory and can increase the amount of work repeated after a crash.

If arrival rate remains above processing capacity, adding a queue only delays the overload. Track backlog age and drain time, then increase safe capacity, limit producers, shed nonessential work, or change the processing design.

## 12.5 The dual-write problem: outbox, inbox, and CDC

A service may need to update its database and publish an event. These are two separate operations, so either can succeed while the other fails. Publishing before the database commit can announce a change that never happened; committing the database first can leave other services unaware of the change.

The **transactional outbox** pattern records the business change and an outbox row in the same local database transaction. A relay or Change Data Capture (CDC) connector publishes the outbox event later. If the relay publishes successfully but crashes before marking the row complete, it may publish the event again. Consumers still need idempotency.

~~~mermaid
flowchart LR
  A[Business command] --> B[One local database transaction]
  B --> C[Update business state]
  B --> D[Insert outbox row]
  D --> E[Relay or CDC connector]
  E --> F[Message broker]
  F --> G[Idempotent consumer]
  G --> H[Consumer state change]
~~~

An **inbox** or deduplication record can be committed atomically with the consumer's local state change. CDC can also capture changes from database logs, but brings its own considerations: connector lag, initial snapshots, schema evolution, restart behavior, and recovery from retained log positions.

These patterns reduce gaps between database state and event publication; they do not remove the need to define retries, event identity, retention, and recovery.

## 12.6 Event time, stream processing, and batch work

Stream processors distinguish **event time** (when an event happened) from **processing time** (when the processor handled it). Events may arrive late or out of order because of retries, network delays, or source behavior.

Windows aggregate events over a time interval. A watermark represents the processor's estimate of how far event time has progressed; it is not proof that no older event can ever arrive. The design must define what happens to late events: update an earlier result, emit a correction, or drop events after a stated horizon.

Stateful stream processors need checkpoints and a recovery plan for both operator state and input positions. Their sinks must also tolerate replay or coordinate writes with progress. “Streaming” does not mean every event is processed instantly or in a strict global order.

Batch processing handles a bounded collection of data, while stream processing handles ongoing input. Batch is often simpler for periodic jobs and large historical computations; streams are useful when results must update continuously. Many architectures combine them, but the two paths need consistent definitions and a way to compare or reconcile results.

## 12.7 Schema evolution, event sourcing, and CQRS

A schema registry can store message schemas and enforce configured compatibility rules, but it cannot guarantee that a consumer interprets the data correctly. Compatibility depends on the serialization format, reader/writer behavior, defaults, deployment order, and the registry policy.

The common compatibility labels describe different promises. **Backward compatibility** generally means a newer reader can read older data; **forward compatibility** means an older reader can read data written by a newer version; **full compatibility** aims to support both directions. Some registries also offer **transitive** modes that compare a new schema with a broader history, not only the immediately previous version. Exact definitions depend on the registry and serialization format, so check the policy you actually configure.

| Schema change | Typical risk | Safer approach |
|---|---|---|
| Add an optional field | Often low, but defaults and unknown-field handling matter | Make consumers tolerant before producers start sending it. |
| Add a required field or remove a field | Older events or consumers may not satisfy the new contract | Use a transition period, defaults/backfill, or a versioned event. |
| Change a field's type, units, or meaning | Data may fail to parse or be silently misinterpreted | Prefer a new field or event version and test the conversion explicitly. |
| Add an enum value | Older consumers may reject a value they do not recognize | Make unknown values safe or coordinate the rollout. |

An event should also carry a stable identity, event type, schema/version information, and the domain identifiers needed to process it safely. Include only metadata and payload fields consumers actually need; an event may be copied into many systems and retained for a long time.

Before a rollout, test old and new payloads against old and new consumers—including missing fields, unknown enum values, defaults, malformed records, and replay from retained history. Make sure active consumers can tolerate the next producer output before the producer starts emitting it.

Keep three related ideas distinct:

- **Event notification** tells other components that something changed. The producer's database usually remains the source of truth.
- **Event sourcing** makes the event history the authoritative record from which current state is derived. It requires version-aware replay, correction procedures, retention and privacy decisions, and often snapshots or projections.
- **CQRS** separates command handling from query handling, sometimes with a read-optimized projection. It can help when reads and writes have different needs, but it introduces projection lag, rebuilds, and additional operational work.

Do not adopt event sourcing simply because a broker is already present. It is most useful when the business history itself matters. Similarly, CQRS should solve a real read/write or ownership problem rather than exist as a default pattern.

### A safe projection rebuild

Suppose a bug corrupted an order read model, while the retained event log still contains the events needed to rebuild it. Keep the current projection serving reads while you build a replacement separately.

1. **Define the source and invariants.** Record the source topic/partitions, retention horizon, projection version, and the business checks that the new projection must satisfy.
2. **Create an isolated replacement.** Write to a new table, index, or namespace so incomplete replay cannot corrupt the live view.
3. **Capture the replay boundary.** Record a high-watermark per source partition or establish an appropriate consistent snapshot. A single offset is not a global ordering across partitions.
4. **Replay safely.** Make projection writes idempotent or guard them with event IDs or aggregate versions.
5. **Catch up with live events.** Continue processing events after the replay boundary and measure lag per partition.
6. **Validate and cut over.** Compare meaningful counts, aggregates, representative records, and invariants. Define the exact applied offsets or versions that form the cutover barrier; do not switch merely because the replay job has ended.
7. **Keep a rollback path.** Switch readers in a controlled way and retain the old projection for a bounded period if it remains trustworthy.

The precise procedure depends on the broker, database, and deployment model. The important properties are a known replay boundary, safe reprocessing, an explicit catch-up barrier, validation, and a reversible cutover.

## 12.8 Event data is replicated data

Once a sensitive value enters an event log, it may be copied into consumer databases, analytics, dead-letter queues, backups, and exports. Minimize event payloads, restrict consumer access, define retention, and avoid including secrets or personal information that downstream consumers do not need.

If a system must support deletion or correction, decide in advance how that requirement applies to retained events and derived data. Immutable history, backups, legal retention, and erasure requirements can conflict; this is an architectural decision, not a cleanup detail to postpone.

## Further reading

- Apache Kafka 4.3 [design](https://kafka.apache.org/43/design/design/) and [message delivery semantics](https://kafka.apache.org/43/design/design/#message-delivery-semantics).
- Debezium [outbox event router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html).
- [CloudEvents specification](https://cloudevents.io/).

---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
