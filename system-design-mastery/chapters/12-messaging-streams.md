# 12. Messaging, Streams, and Asynchronous Workflows

## Queue, pub-sub and event log
A queue distributes work among consumers, often with one consumer in a group handling each message. Publish-subscribe delivers an event to multiple subscribers. An event log retains an ordered sequence within a partition and permits consumers to read at their own pace or replay history. Products may combine these models but differ in retention, ordering and acknowledgment semantics.

Asynchrony reduces temporal coupling: producers need not wait for consumers to finish. It does not remove dependency; it changes when errors appear and how progress is observed.

## Kafka concepts
Kafka organizes records into topics and partitions. Offsets identify positions within a partition; order is defined within a partition, not globally across all partitions. A consumer group distributes partitions among members, and reassignment can cause pauses or duplicate processing depending on offset and effect coordination. Replication protects partitions according to configured policies. Consumer lag is a gap in progress, but a lag count alone does not show age or business impact. See [Kafka design documentation](https://kafka.apache.org/documentation/#design).

## Delivery semantics
- **At-most-once:** messages may be lost but are not redelivered under the stated semantics.
- **At-least-once:** retries/recovery avoid loss under assumptions but can create duplicates.
- **Exactly-once:** a scoped guarantee that a logical effect is reflected once within a defined protocol boundary.

A consumer that commits a database update then crashes before committing its offset will see replay. Committing the offset first can lose the effect. Correctness requires coordination or idempotent effects.

## Retry, poison events and replay
Retries help transient faults but can block progress or amplify load. Use bounded retry, backoff, jitter and a dead-letter/quarantine path for repeatedly failing events. A dead-letter queue needs monitoring, ownership, correction and replay procedures. Replay can repeat side effects, so event identity must be distinct from delivery attempt.

## Outbox, inbox and CDC
A service that updates a database and publishes an event faces a dual-write problem: the database can commit while publication fails, or publication can happen while the transaction rolls back. A transactional outbox writes business state and an outbox row in one local transaction; a relay publishes later. The relay may publish duplicates, so consumers still need idempotency.

An inbox/deduplication record can be committed atomically with local state changes. Change Data Capture (CDC) captures database changes, often from transaction logs, but introduces connector lag, schema evolution, snapshot and recovery considerations.

## Schema evolution and event sourcing
Event schemas need compatibility rules. Additive optional fields are often easier to evolve than changing a field's meaning or type. A schema registry supports governance but cannot ensure consumers interpret events correctly.

Event sourcing stores domain events as authoritative state history; current state is derived by replay or projections. It can support audit and rebuilds but adds event versioning, replay, retention, privacy deletion and debugging challenges. An event log is not automatically event sourcing.

CQRS separates command handling from query models. It can support asymmetric workloads but introduces projection lag and duplicated models. Use it when that trade-off is justified.

## Stream processing and backpressure
Stream processors handle continuous records, often using event time, processing time, windows, state and checkpoints. Late events complicate windows; watermarks estimate event-time progress and do not prove no earlier event can arrive. Recovery must coordinate input positions and operator state.

If producers outpace consumers, backlog grows. Define retention, admission control, prioritization and behavior when backlog age exceeds business usefulness.

## Further reading
- Apache Kafka [design](https://kafka.apache.org/documentation/#design) and [delivery semantics](https://kafka.apache.org/documentation/#semantics).
- Debezium [outbox event router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html).
- [CloudEvents specification](https://cloudevents.io/).
