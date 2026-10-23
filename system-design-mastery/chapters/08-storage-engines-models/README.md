# 8. Storage Engines and Data-System Choices

## Logical model versus storage engine
A logical data model describes how applications represent and query information. A storage engine determines how it is organized on media, indexed, replicated and recovered. Two systems in the same category can have different transaction guarantees, write paths and operational limits.

| Model | Natural strengths | Costs and questions |
|---|---|---|
| Relational | Constraints, joins, transactions, flexible SQL | Distribution and very large scale require careful design |
| Key-value | Direct lookup by key | Secondary queries and relationships need deliberate modeling |
| Document | Related attributes grouped into flexible records | Cross-document constraints and schema drift |
| Wide-column | Large sparse datasets and partition-oriented access | Query-driven modeling, hot partitions |
| Graph | Traversal across relationships | High-degree graph distribution and traversal costs |
| Time-series | Time-oriented ingestion, retention and aggregation | Cardinality, late data and downsampling |
| Distributed SQL | Relational semantics with distribution mechanisms | Coordination, transaction latency and topology |
| Object storage | Large blobs, media, backups and archives | Not a replacement for low-latency transactional lookups |
| Block storage | Raw blocks for filesystems and databases | Filesystem, replication and backup layers remain your responsibility |
| File storage | Hierarchical shared access | Metadata scaling, locking and network filesystem semantics |

These are broad families; verify the selected product's actual behavior.

## B-trees and LSM trees
B-trees maintain a balanced ordered structure, supporting lookup and range scans. Updates can require page writes and splits. Log-structured merge trees buffer writes, flush sorted runs and merge them through compaction. This can make ingestion efficient, but reads may consult multiple structures and compaction creates background I/O. Bloom filters can reduce unnecessary reads.

- **Write amplification:** physical bytes written divided by logical bytes written.
- **Read amplification:** storage work per logical read.
- **Space amplification:** physical storage relative to live logical data.
- **Compaction:** merging/reorganizing files to control read cost and reclaim obsolete versions.

These costs interact. Compaction can compete with foreground traffic; a write-heavy workload may benefit from an LSM design, while read-heavy range scans may favor another structure. Benchmark representative data sizes and distributions.

## Object, block and file storage
Object storage exposes objects through identifiers and APIs; it suits media, backups, archives and data lakes. Block storage exposes addressable blocks. File storage exposes paths and filesystem operations. Object durability does not ensure the application wrote the correct object, retained the right version, or preserved encryption keys.

## Integrity and lifecycle
Replication can protect against some hardware failures; checksums detect corruption; versioning and immutable retention can help recover from deletion or malicious changes. None replaces a tested restore process. Lifecycle rules may tier, expire, archive or compact data; they must respect query requirements, retention obligations, deletion policy and recovery objectives.

## Choose with workload evidence
Ask about dominant access patterns, atomic invariants, joins, distribution key, skew, freshness, growth, retention, restoration, operational ownership and migration cost. Do not choose by a universal SQL-versus-NoSQL ranking.


## 8.1A Storage-model selection starts with access patterns

Describe operations before choosing a database family:
- Key lookup, range scan, prefix search, graph traversal, aggregation, or full-text retrieval.
- Read/write ratio, payload size, update frequency, and hot-key distribution.
- Required atomicity and uniqueness constraints.
- Data growth, retention, deletion, backup, and restore needs.
- Freshness, consistency, latency, and geographic distribution.
- Operational skills, query flexibility, and migration cost.

A database optimized for one access pattern may perform poorly when forced into another. A key-value store can be excellent for direct lookup but require application-managed secondary indexes. A graph engine can simplify traversals but may struggle when graph partitions force remote hops. A relational engine can support many patterns but still needs deliberate indexing and distribution.

## 8.1B B-tree page behavior and locality

B-trees keep keys ordered in pages, allowing logarithmic lookup and efficient range traversal. Internal nodes direct the search; leaf pages contain or reference row data depending on the engine. Page splits and updates can create write amplification, and random key insertion may have different locality from monotonically increasing keys.

A B-tree is not simply slow for writes. Its behavior depends on page size, fill factor, cache residency, key distribution, concurrency, WAL behavior, and storage. Sequential key patterns can improve locality but may create a hot rightmost page under high concurrency. Measure the actual engine rather than infer performance from the data structure alone.

## 8.1C LSM write path and compaction trade-offs

An LSM engine commonly records changes in a write-ahead log, updates an in-memory structure, flushes sorted immutable files, and merges files during compaction. The log supports recovery; the memtable absorbs writes; immutable files organize data for reads; compaction controls the number and overlap of files.

Compaction consumes I/O and CPU, competes with foreground requests, and rewrites data. Different compaction strategies trade write amplification, space amplification, read amplification, and write stalls differently. A system that looks fast during a short ingest benchmark may degrade once compaction debt accumulates.

Tombstones represent deletions in many LSM designs. They cannot always be removed immediately because older versions or replicas may still contain the value. Retention and compaction rules must ensure deleted data is not accidentally resurrected during recovery or replica repair.

## 8.1D Write-ahead logs, checkpoints, and recovery

A write-ahead log records enough information to recover committed changes after a crash. The general rule is that the relevant log record must reach the required durability point before the data page is considered safely persisted under that protocol. Exact ordering and guarantees depend on the engine and configuration.

Checkpoints reduce how much log must be replayed during recovery, but aggressive checkpointing can create I/O spikes and insufficient checkpointing can increase recovery time. Group commit can amortize flush costs across transactions while changing latency and throughput characteristics. Understand what commit acknowledged means for local disk, replica acknowledgment, and failover.

## 8.1E Replication, durability, and acknowledged writes

Durability depends on the acknowledgment contract. A commit may mean data reached an in-memory buffer, local durable log, multiple replicas, or a quorum according to a specific protocol. These are different failure guarantees.

Synchronous replication can reduce the window of lost acknowledged writes but may make writes unavailable or slower when required replicas cannot be reached. Asynchronous replication can improve latency and availability while permitting a lag window. Even synchronous replication does not protect against every logical corruption or operator error; backup and point-in-time recovery remain important.

## 8.1F Object storage consistency and multipart uploads

Object storage is suitable for large immutable or versioned blobs, media, backups, and data lake files. It typically uses object keys and metadata rather than general database transactions across arbitrary objects. Application-level manifests or commit markers may be needed when publishing a multi-object dataset atomically from the reader's perspective.

Multipart upload improves transfer of large objects but introduces incomplete-upload cleanup, part retry, finalization, and integrity checks. Object versioning can aid recovery from overwrite or deletion but increases storage cost and does not automatically satisfy data deletion requirements.

## 8.1G Compression, checksums, and encoding

Compression reduces storage and network transfer but consumes CPU and can affect random access. The right choice depends on compressibility, block size, read/write mix, and latency budget. Columnar formats often benefit analytical scans by reading only needed columns; row-oriented formats can be better for retrieving a complete record.

Checksums detect certain corruption classes but do not identify the correct value if every copy contains the same logical error. End-to-end integrity may require checksums at multiple layers and validation of application invariants. Serialization format choices also affect schema evolution and cross-language compatibility.

## 8.1H Storage amplification and capacity estimates

Write amplification is physical bytes written divided by logical bytes written. Read amplification is storage work per logical read. Space amplification is physical storage relative to live data. These are workload- and engine-dependent, and should be measured over steady-state compaction and realistic update patterns.

Capacity planning must include indexes, replicas, logs, temporary compaction space, snapshots, backups, and growth. A database whose live records occupy 1 TB may require substantially more than 1 TB of physical capacity after indexes, replication, headroom, and recovery artifacts are included.

## 8.1I Storage engine benchmark checklist

- Use representative record sizes and key distributions.
- Include hot keys, skew, updates, deletes, and range scans.
- Run long enough to reach steady-state compaction/checkpoint behavior.
- Measure p50/p95/p99 latency, throughput, CPU, I/O, and stalls.
- Test cold and warm cache behavior.
- Include replication and recovery settings used in production.
- Measure storage amplification and recovery time.
- Verify correctness after crash/restart and restore.
- Include operational skill and migration cost in the decision.


## Further reading
- [PostgreSQL storage documentation](https://www.postgresql.org/docs/current/storage.html).
- O'Neil et al., [The Log-Structured Merge-Tree](https://doi.org/10.1007/s002360050048).
- [Amazon S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) for product-specific semantics.


## Conceptual write paths: B-tree and LSM

```mermaid
flowchart TD
  subgraph BTree[B-tree-oriented write]
    B1[Update key] --> B2[Find page]
    B2 --> B3[Modify page and log]
  end
  subgraph LSM[LSM-oriented write]
    L1[Write request] --> L2[Write-ahead log]
    L2 --> L3[Memtable]
    L3 --> L4[Sorted immutable files]
    L4 --> L5[Background compaction]
  end
```

This is a conceptual comparison, not a claim that all engines follow identical paths. Real products combine logs, caches, indexes and recovery mechanisms differently. Compare read, write and space amplification under your workload.


---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
