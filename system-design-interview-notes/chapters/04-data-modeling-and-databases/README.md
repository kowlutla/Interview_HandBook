# 4. Data Modeling and Databases

Database choice should follow the data model, access patterns, consistency needs, and operational constraints—not popularity. Start by asking what data must be stored and how the system reads and writes it.

## 4.1 Model the access patterns

Before choosing a database, identify:
- The main entities and their relationships.
- The most common reads and writes.
- Query filters, sorting, and pagination requirements.
- Transaction boundaries and invariants.
- Data volume, growth, and retention.
- Consistency, latency, and availability expectations.

A schema that fits the data conceptually may still perform poorly if it does not support the application's access patterns.

## 4.2 Relational versus non-relational databases

| Database family | Often a good fit | Important trade-offs |
|---|---|---|
| Relational (SQL) | Relationships, joins, constraints, and multi-row transactions | Schema changes and horizontal scaling may require planning |
| Document | Aggregate-shaped records and flexible attributes | Cross-document transactions and joins may be less natural or more costly |
| Key-value | Simple lookup by key, sessions, counters, and cache-like access | Limited querying beyond the key model |
| Wide-column | Large distributed datasets with known query patterns and high write throughput | Data modeling is query-driven; ad hoc queries can be difficult |
| Graph | Relationship traversals and connected-data queries | Specialized operations and ecosystem may be unnecessary for simple relationships |
| Search engine | Full-text search, relevance ranking, and faceted search | Often an index/projection rather than the authoritative transactional store |

These are tendencies, not hard rules. Modern products overlap, so evaluate actual guarantees and workload behavior.

## 4.3 Normalize and denormalize

**Normalization** reduces duplicated facts and helps preserve consistency. It is often useful for transactional data with relationships and frequent updates.

**Denormalization** duplicates or precomputes data to make reads simpler or faster. It can be valuable for read-heavy access patterns, but updates must keep duplicated representations sufficiently current.

Do not denormalize merely because it sounds scalable. First identify the expensive query or consistency requirement that motivates it.

## 4.4 Indexes and query patterns

An index helps the database locate rows or documents without scanning all data, but indexes consume storage and make writes more expensive.

Design indexes around real query patterns:
- Filter columns and sort order matter.
- Composite-index column order matters.
- An index may not help a query if its predicates or ordering do not align with the index.
- Too many indexes increase write amplification and maintenance work.

For large datasets, pagination should be designed deliberately. Offset pagination is easy but can become expensive at high offsets and may shift under concurrent writes. Keyset/cursor pagination can be more efficient and stable when the sort key and tie-breaking rules are well defined.

## 4.5 Transactions and ownership

A transaction groups changes that must satisfy a set of invariants atomically within the database's transaction model. Keep related data together when strong transactional invariants require it.

When a workflow crosses independent services or databases, one local transaction generally cannot atomically commit every participant. Options include redesigning ownership, using an orchestration/saga workflow, or accepting and managing eventual consistency.

## 4.6 Choosing a database: practical method

1. List the access patterns and consistency requirements.
2. Identify which database capabilities are essential (transactions, joins, full-text search, graph traversal, etc.).
3. Estimate data size and read/write rates.
4. Consider operational expertise, backups, recovery, scaling, and cost.
5. Validate the choice with representative queries and load tests.

A relational database is a strong default for many business applications, but not a universal answer. Specialized storage is justified when it materially improves a required workload.

## 4.7 Common interview questions

### When would you choose SQL over NoSQL?

Choose SQL when relationships, joins, constraints, and transactional invariants are central. Consider a non-relational model when its data shape and access patterns fit a specialized workload better. “NoSQL scales, SQL does not” is an oversimplification; scalability depends on the product, schema, workload, and operating model.

### What is the difference between normalization and denormalization?

Normalization reduces duplicated facts and update anomalies. Denormalization deliberately duplicates or precomputes information to improve particular reads. Denormalization trades simpler/faster reads for additional storage and consistency work.

### Why are indexes not always beneficial?

Indexes speed up suitable queries but consume memory and storage and add work to inserts, updates, and deletes. Indexes should be based on observed query patterns and verified with query plans and realistic load.

### When is cursor pagination better than offset pagination?

Cursor pagination is often preferable for large or frequently changing datasets because it can avoid scanning and skipping many rows. It requires a deterministic ordering and a cursor that captures the position, usually with a unique tie-breaker. Offset pagination can be perfectly adequate for small, stable result sets.

### Should every service have its own database?

Independent ownership can reduce coupling, but separate databases increase operational and cross-service consistency complexity. The principle is that each service should own its data contract and writes; physical database separation is an architectural choice, not a rule that must be applied without considering the system.

## Quick revision

- Start with access patterns and invariants.
- SQL and NoSQL are different modeling options, not a scalability ranking.
- Normalize for consistency; denormalize for justified read needs.
- Indexes trade faster reads for storage and write overhead.
- Use cursor pagination when deep offsets or concurrent changes matter.
- Cross-service transactions require explicit workflow and consistency design.
