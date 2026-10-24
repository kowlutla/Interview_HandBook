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



## 8.2 Choosing among data-system families

A storage model should follow the shape of the data, access patterns, correctness constraints, and operational needs. “NoSQL” is not one model with one consistency or scaling behavior; key-value, document, wide-column, graph, search and time-series systems optimize different access paths.

| Family | Natural access pattern | Strengths | Main design costs |
|---|---|---|---|
| Relational | Predicate queries, joins, constraints, transactions | Rich query model and integrity enforcement | Schema/query/index tuning; distributed writes can be complex |
| Key-value | Lookup by known key | Simple, predictable access and horizontal distribution in some systems | Secondary queries and relationships may need application-managed indexes |
| Document | Retrieve/update aggregate-shaped documents | Flexible nested records and aggregate-oriented access | Cross-document invariants and joins may be limited or costly |
| Wide-column | Partition-key access over large distributed datasets | High write throughput and partitioned scale for designed queries | Query-first modeling, partition-key discipline and limited ad hoc joins |
| Graph | Relationship traversal and path queries | Traversal follows explicit edges and relationship semantics | Distributed traversals and graph partitioning can be expensive |
| Time-series | Time-bounded reads, rollups, retention | Time-oriented compression, downsampling and lifecycle features | High-cardinality labels, late events and retention/aggregation policy |
| Search engine | Full-text, relevance, filtering and faceting | Inverted indexes, analyzers, ranking and text retrieval | Usually a derived index with refresh lag and expensive index maintenance |
| Object storage/data lake | Large blobs, immutable files, datasets | Low-cost durable bulk storage and ecosystem integration | Object-level rather than general multi-object transactions; metadata/catalog and file-layout concerns |
| Analytical warehouse/columnar store | Large scans, aggregates, reporting | Column pruning, compression and analytical execution | Not automatically suitable for high-rate transactional point updates |

These are common tendencies, not guarantees for every product. Verify each candidate's transaction, consistency, partitioning, indexing, backup, restore and operational model.

## 8.3 Search indexes are usually derived data

A search engine often indexes data from an authoritative database through change data capture, an outbox/event stream, periodic bulk indexing or application dual writes. Direct dual writes create a partial-failure problem: the database update may succeed while the search update fails, or vice versa. Prefer a durable change path and an idempotent indexer where correctness matters.

Search results may be stale because indexing and refresh are asynchronous. Define whether the user can tolerate eventual visibility, how updates/deletes propagate, and how a full rebuild is performed. The index should be reconstructible from authoritative data or durable change history where feasible. Search ranking, analyzers, tokenization, language support and filters are product semantics, not just storage implementation details.

## 8.4 Row stores, columnar stores, lakehouses and warehouses

Row-oriented storage places fields for a record together, often helping point lookups and transactional updates. Columnar formats group values by column, enabling compression and reading only selected columns during analytical scans. These are workload tendencies rather than strict boundaries; many systems support mixed execution or storage modes.

A data lake commonly stores large datasets in object storage and relies on file formats, catalogs and processing engines. A warehouse offers managed analytical storage/query semantics. A lakehouse architecture attempts to add table metadata and transactional or governance capabilities over lake storage. These designs still need file-size management, partition pruning, schema evolution, late data handling, access controls, compaction, lineage and cost governance.

Small files can overwhelm metadata and scheduling; excessively large files can hurt parallelism and selective reads. Partitioning by a high-cardinality or poorly selective column can create too many tiny files or skew. Choose file layout from actual query predicates and write cadence.

## 8.5 Secondary indexes and materialized views

A secondary index creates an alternate access path at the cost of write amplification, storage and consistency maintenance. In distributed stores, a secondary query may scatter across partitions unless the index maps the predicate to a narrower set of locations. Indexing every field can turn writes into many independent updates and increase recovery complexity.

A materialized view precomputes a query or aggregation. It trades refresh work and storage for faster reads. The design must define freshness, refresh cadence, incremental update correctness, rebuild behavior, and what readers see during refresh. Materialized views can be derived from an authoritative source, but their lag should be visible to consumers when it affects decisions.

## 8.6 Storage selection checklist

- What are the dominant read/write/query shapes?
- Which invariants require transactions or constraints?
- Are relationships traversed by joins, graph paths, or precomputed views?
- Is the workload transactional, analytical, search-oriented, or mixed?
- What consistency and freshness do derived indexes provide?
- How are schema changes, backfills and full rebuilds performed?
- How are partition keys, hot keys and query fan-out controlled?
- What are retention, deletion, backup and point-in-time recovery requirements?
- Which index, compaction and file-layout costs appear under steady-state load?
- Can the team operate, restore and migrate the chosen system?



## 8.7 Distributed file systems and object, block, and file interfaces

The phrase “storage” covers different interfaces and failure models. **Block storage** exposes addressable blocks or volumes to a host, leaving the filesystem and many data-layout decisions to the consumer. **File storage** exposes a shared directory/file namespace with filesystem semantics. **Object storage** exposes objects addressed by keys, usually with metadata and API operations rather than arbitrary in-place byte updates.

A distributed file system presents file-like operations across multiple machines. Depending on its design, it may distribute metadata separately from file contents, replicate blocks, use erasure coding, cache client data, or provide different consistency guarantees. It should not be assumed to behave exactly like a local disk under concurrent access, network partition or server restart.

### Metadata, data placement and failure recovery

Distributed file systems must locate files and blocks, track replicas or erasure-coded fragments, recover failed nodes, detect corruption and rebalance placement. Metadata availability can become a bottleneck even when bulk data is distributed. A design may use a metadata service, partitioned namespace, decentralized placement, or a combination; the recovery and consistency model depends on that choice.

Replication stores multiple copies and can improve availability at the cost of storage and write traffic. Erasure coding stores data and parity fragments and can reduce storage overhead for large durable datasets, but reconstruction consumes network and CPU and may be slower during degraded operation. Neither approach removes the need for integrity checks, failure-domain-aware placement and tested recovery.

### Object storage is not a general POSIX filesystem

Object stores are well suited to large immutable or versioned objects, backups, media, data lakes and durable artifacts. They commonly support multipart upload, metadata and lifecycle policies, but do not necessarily provide arbitrary in-place updates, atomic rename or filesystem locking semantics. Applications should use the documented API consistency contract and avoid assuming local-filesystem behavior.

When writing a large object, multipart upload can improve parallelism and allow retries by part, but incomplete uploads need cleanup. Object versioning can help recover from accidental overwrite or deletion, yet retention and deletion policies must account for versions, replication and legal requirements. Access policy should include both the object and the mechanism used to issue temporary access URLs.

### Storage selection example

A low-latency database volume may favor block storage with predictable IOPS and a supported filesystem/database configuration. A shared team directory may need file semantics and coordinated access. Large media objects or backups may favor object storage with lifecycle and versioning. An analytical data lake may combine object storage with columnar files, a catalog and compute engines.

The cheapest per-gigabyte option may not be cheapest overall. Include request charges, retrieval tiers, cross-zone/region transfer, replication, metadata operations, recovery speed and engineering effort. A restore path that takes several days can violate a recovery objective even when the storage is durable.

### Comparative access-pattern example: one product, several workloads

Suppose a commerce application must support transactional order updates, full-text product search, image delivery and historical sales analysis. These are different access patterns and do not necessarily belong in one storage engine. The table shows a possible division of responsibility, not a requirement to adopt every store.

| Workload | Candidate storage/read model | Authority and consistency question | Main caveat |
|---|---|---|---|
| Create an order and enforce business constraints | Relational database with transactions and indexes | Which transaction commits the order and its invariants? | Cross-service side effects still need an explicit workflow/outbox protocol |
| Search products by text, facets and relevance | Derived search index | How quickly does a committed product change become searchable, and how is the index rebuilt? | Search results may be stale; index availability does not make it the source of truth |
| Store product images and downloadable assets | Object storage, optionally fronted by a CDN | Who may read/write each object, and how are versions, deletion and cache invalidation handled? | Object APIs do not automatically provide database transactions or arbitrary filesystem semantics |
| Analyze months of sales by region/product/time | Columnar warehouse or lakehouse over governed data | What is the freshness and lineage of the analytical dataset? | Batch/stream ingestion, schema evolution and late corrections require governance |
| Repeatedly read a hot product summary | Cache or materialized view | What staleness is acceptable, and how is invalidation/rebuild performed? | Cached values are derived copies; authorization and tenant scope must be reflected in keys/policies |

Keep the authoritative write path small and explicit. Search indexes, analytical tables and caches should have a rebuild or reconciliation strategy. Add a separate store only when its access pattern, scale, latency, isolation or operational benefit justifies the extra consistency and recovery work. A single well-operated relational system may be the better choice when it already meets the requirements.

### Distributed storage review checklist

- Does the application need block, file, or object semantics?
- What consistency and atomicity does the storage interface guarantee?
- How are metadata and data placement scaled and recovered?
- Is durability provided by replication, erasure coding, or another mechanism?
- Are replicas placed across independent failure domains?
- How is silent corruption detected and repaired?
- Are multipart uploads, versions, incomplete uploads and deletion handled?
- What are the restore throughput and cost under failure conditions?
- Do lifecycle and retention policies match recovery and compliance needs?
- Have application assumptions been checked against the actual storage API contract?


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

## Further reading
- [PostgreSQL storage documentation](https://www.postgresql.org/docs/current/storage.html).
- O'Neil et al., [The Log-Structured Merge-Tree](https://doi.org/10.1007/s002360050048).
- [Amazon S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) for product-specific semantics.



---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
