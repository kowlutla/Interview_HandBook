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

## Further reading
- [PostgreSQL storage documentation](https://www.postgresql.org/docs/current/storage.html).
- O'Neil et al., [The Log-Structured Merge-Tree](https://doi.org/10.1007/s002360050048).
- [Amazon S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) for product-specific semantics.
