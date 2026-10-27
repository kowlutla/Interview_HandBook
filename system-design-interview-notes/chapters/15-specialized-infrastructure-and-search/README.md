# 15. Specialized Infrastructure: Search, Files, Analytics, and Coordination

Specialized components are justified by a workload or product requirement. Start with the data's authoritative owner and access patterns; add a search engine, object store, stream processor, or coordination system only when its distinct capability is needed.

## 15.1 Search indexes are derived data

A relational database can support exact lookups and many filters, but full-text relevance, tokenization, stemming, and ranked retrieval often justify a search engine. The index is commonly asynchronous and therefore can lag behind the source of truth.

```mermaid
flowchart LR
    API[Write API] --> DB[(Authoritative database)]
    DB --> OUT[Outbox / CDC]
    OUT --> IDX[Indexer]
    IDX --> SEARCH[(Search index)]
    CLIENT[Search client] --> SEARCH
    CLIENT -. authoritative detail or validation .-> API
```

The write path should not pretend that the search index is immediately current unless the system synchronously coordinates that guarantee. For critical updates, expose indexing status, use version-aware indexing, or read the authoritative store for final validation. Rebuild indexes from source data/events when necessary. Search results are often suitable for discovery, not as the authority for inventory, payment state, or access control.

## 15.2 Object storage and file transfer

Store large binary objects in object storage and metadata (owner, permissions, size, checksum, object key, lifecycle state) in a transactional database. This avoids pushing large payloads through application servers and keeps metadata queries efficient.

Typical upload flow:
1. Authenticate and authorize the upload request.
2. Create an upload record and issue a short-lived, scoped presigned URL when supported.
3. Client uploads directly to object storage, possibly using multipart upload for large files.
4. Verify object existence, size, checksum, and policy before marking the upload complete.
5. Publish an event for scanning, thumbnailing, or indexing.
6. Deliver downloads through signed access or a CDN with cache policy appropriate to the data's privacy.

A presigned URL is a bearer capability: anyone holding it may use it within its scope and expiry. Do not log it or make it broader/longer-lived than necessary. Handle abandoned multipart uploads, malware scanning, retention, and deletion from replicas/derived indexes according to policy.

## 15.3 OLTP versus OLAP and batch versus streaming

| Workload | Typical shape | Suitable starting point |
|---|---|---|
| OLTP | Many short transactions, selective reads/writes, invariants | Transactional database |
| OLAP | Large scans, aggregations, historical analysis | Warehouse/lakehouse or analytical store |
| Batch | Process a bounded dataset on a schedule | Scheduled jobs over durable inputs |
| Streaming | Continuously process arriving events with freshness goals | Stream processor plus durable event log |

Do not run expensive analytical scans on the same transactional database without understanding contention. A warehouse is not automatically real-time; ingestion and transformation add lag. Streaming is not automatically better than batch: it introduces state, replay, late-event, and operational complexity.

## 15.4 Bloom filters and probabilistic structures

A Bloom filter can say “definitely not present” or “possibly present,” with false positives but no false negatives under its normal assumptions. It is useful as a cheap pre-check before an expensive lookup, such as reducing unnecessary disk reads. A positive result must still be verified against the authoritative structure. Size it for the expected number of elements and acceptable false-positive probability; account for rebuilds and deletions (ordinary Bloom filters do not support deletion without a variant).

## 15.5 Unique IDs, schedulers, and rate limiting

- **Unique IDs:** choose based on uniqueness scope, sortability, coordination, and exposure of internal information. Central sequences are simple but can bottleneck or leak volume; random IDs reduce coordination but require collision probability analysis; time/worker-based IDs require clock and worker-ID management.
- **Job schedulers:** persist scheduled work, claim it with bounded leases/visibility timeouts, retry transient failures, and make handlers idempotent. A scheduler firing twice must not duplicate a business effect.
- **Distributed rate limiting:** a local token bucket is cheap but only limits each instance. A shared counter/script or dedicated limiter can enforce a global quota at the cost of network latency and a new dependency. Define whether limits are approximate or strict and what happens when the limiter is unavailable.

## 15.6 When not to add a specialized component

Do not add Kafka, a graph database, a distributed lock manager, or a separate search cluster just because the technology is common in design discussions. First establish the need: replay/fan-out, graph traversal, coordination, or relevance search. Every additional component adds deployment, monitoring, security, capacity, and failure-handling work.

## Quick revision

- Search is commonly a derived, eventually updated index.
- Keep large blobs in object storage and ownership/permissions in a metadata store.
- Separate OLTP and OLAP when their workloads interfere.
- Bloom filters trade memory for probabilistic pre-checks.
- Add specialized infrastructure only when a clear workload justifies its operational cost.

## Further reading

- [Amazon S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) — provider-specific bearer-capability behavior and expiry.
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) — event-log, consumer, and delivery semantics.
- [Apache Spark Structured Streaming guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) — stateful streaming, event time, and processing model.

## Scenario analysis

**Case:** A small application is proposed with a search cluster, event stream, cache, and analytics warehouse before launch, despite modest initial requirements.

**Reasoning:** Start from user-visible requirements and query patterns. A relational database may be enough for transactional CRUD and modest filtering. Add a search index when full-text relevance or query latency justifies its derived-data lifecycle; add a stream when durable fan-out/replay or decoupled processing is needed; add a warehouse when analytical scans materially interfere with OLTP. For each component, name the owner of authoritative data, the freshness contract, and the failure behavior. Avoid introducing infrastructure without a workload that needs it.

## 15.7 B-tree and LSM-tree storage trade-offs

Storage-engine choice is about the workload and implementation, not a universal ranking.

- **B-tree-family indexes** keep keys in an ordered structure and support efficient point lookups and range scans. They are common in relational databases. Updates may cause page writes and page splits, and secondary indexes add write and storage cost.
- **Log-structured merge (LSM) trees** typically buffer writes in memory and flush sorted runs to disk, then compact those runs in the background. They can provide high write throughput, but compaction consumes I/O and space, and read amplification may require checking multiple structures unless filters and indexes narrow the search.
- **Write amplification** is the amount of physical data written relative to the logical data changed. **Read amplification** is the extra work needed to serve a read. **Space amplification** is the additional storage consumed by indexes, obsolete versions, or compaction overlap.

A write-heavy workload with sequential ingestion may favor an LSM-oriented engine, while a workload requiring efficient ordered access and predictable range queries may favor a B-tree-oriented design. Real systems include caching, compression, compaction policies, concurrency control, and other details, so benchmark representative operations before choosing.

### Read amplification in write-optimized engines

An LSM-based engine may need to consult multiple sorted runs and merge results; compaction and tombstones can add work. Bloom filters and indexes reduce unnecessary reads, while compaction policy trades background I/O and space for read efficiency. Measure the actual workload rather than assuming the storage-engine family determines performance by itself.

## 15.8 Change data capture and derived projections

Change data capture (CDC) publishes committed database changes to downstream consumers. It can maintain search indexes, analytics projections, or caches without putting every downstream update in the synchronous request path. A log-based CDC pipeline still introduces lag, schema compatibility concerns, duplicate/replayed events, and ordering constraints.

Treat the projection as rebuildable derived state where possible. Include a stable event identity or source position, make consumers idempotent, define how schema changes are rolled out, and monitor the age of the latest processed change. A successful database commit does not mean every projection has already caught up.
