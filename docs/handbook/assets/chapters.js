/* Single source of truth for the handbook structure.
   dir: folder holding the page. id: file name without .html.
   done:true means the page exists. Only the maintainer flips this flag. */
window.HLD = {
  title: "System Design Handbook",
  modules: [
    { id: "m0", title: "Orientation", dir: "chapters", items: [
      { id: "01-interview-framework", t: "How to Approach a Design Interview", d: "Requirement types, scoping, assumptions, API then data then design then deep dive, time budget", done: true },
      { id: "02-estimation", t: "Estimation and Metrics", d: "Powers of two, latency numbers, QPS/storage/bandwidth, peak vs average, percentiles, nines, Little's Law", done: true }
    ]},
    { id: "m1", title: "Networking and Communication", dir: "chapters", items: [
      { id: "03-networking-essentials", t: "Networking Essentials", d: "OSI/TCP-IP layers, TCP vs UDP, HTTP/1.1, 2, 3 and QUIC, keep-alive, TLS handshake, NAT, firewalls", done: true },
      { id: "04-dns", t: "DNS in Depth", d: "Resolution path, record types, TTL and caching, DNS load balancing, GeoDNS, failure modes", done: true },
      { id: "05-api-design", t: "API Design", d: "REST, HTTP semantics, idempotency, gRPC, GraphQL, pagination, versioning, errors, async APIs, webhooks", done: true },
      { id: "06-realtime", t: "Real-Time Communication", d: "Polling, long polling, SSE, WebSockets, connection management at scale, presence", done: true },
      { id: "07-serialization", t: "Serialization, Compression and Batching", d: "JSON vs Protobuf/Avro, schema evolution, compression tradeoffs, batching and latency", done: true }
    ]},
    { id: "m2", title: "Scaling the Stateless Tier", dir: "chapters", items: [
      { id: "08-scalability-concurrency", t: "Scalability and Concurrency", d: "Vertical vs horizontal, stateless design, sessions, threads vs event loops, pools, backpressure", done: true },
      { id: "09-load-balancing", t: "Load Balancers", d: "L4 vs L7, algorithms, health checks, sticky sessions, TLS termination, global LB, HA of the LB itself", done: true },
      { id: "10-proxies", t: "Forward and Reverse Proxies", d: "Forward vs reverse proxy, uses, Nginx/Envoy/HAProxy, buffering, connection pooling, caching proxy", done: true },
      { id: "11-api-gateway", t: "API Gateway and BFF", d: "Gateway responsibilities, auth offload, routing, aggregation, rate limiting, BFF, gateway failure modes", done: true },
      { id: "12-cdn", t: "Content Delivery Networks (CDN)", d: "Edge, routing, cache keys, tiering, invalidation, video, signed URLs, security", done: true },
      { id: "13-caching-patterns", t: "Caching I: Patterns", d: "Cache levels, cache-aside, read/write-through, write-back, eviction, invalidation", done: true },
      { id: "14-caching-failures", t: "Caching II: Failure Modes and Distributed Caches", d: "Stampede, penetration, avalanche, hot keys, consistency, local vs distributed caches", done: true },
      { id: "15-redis", t: "Redis Deep Dive", d: "Data structures, single-threaded model, persistence, replication, cluster, eviction, use cases, pitfalls", done: true },
      { id: "16-rate-limiting", t: "Rate Limiting and Load Shedding", d: "Token bucket, leaky bucket, windows, distributed limiters, shedding, admission control", done: true }
    ]},
    { id: "m3", title: "The Data Layer", dir: "chapters", items: [
      { id: "17-data-modeling", t: "Data Modeling", d: "Access-pattern-first design, normalization vs denormalization, deletes, TTL and retention", done: true },
      { id: "18-relational-internals", t: "Relational Databases In Depth", d: "Indexes, query plans, ACID, isolation levels, MVCC, locking", done: true },
      { id: "19-storage-engines", t: "Storage Engines", d: "B-tree vs LSM, WAL, SSTable, compaction, read/write amplification", done: true },
      { id: "20-nosql", t: "NoSQL Families and Choosing a Store", d: "Key-value, document, wide-column, graph, time-series, decision framework", done: true },
      { id: "21-object-storage", t: "Object Storage (S3-style)", d: "Buckets and objects, durability and erasure coding, consistency, multipart upload, tiers, design internals", done: true },
      { id: "22-search-engines", t: "Search Engines (Elasticsearch)", d: "Inverted index, analyzers, relevance, shards and replicas, indexing pipeline, near-real-time, pitfalls", done: true },
      { id: "23-other-stores", t: "Other Specialized Stores", d: "Distributed file systems, data warehouses and OLAP, time-series DBs, vector databases", done: true },
      { id: "24-replication", t: "Replication", d: "Leader-follower, multi-leader, leaderless, sync vs async, lag, failover, quorums, conflicts", done: true },
      { id: "25-sharding", t: "Sharding and Partitioning", d: "Range, hash, shard keys, consistent hashing, hot partitions, rebalancing, cross-shard queries", done: true },
      { id: "26-multi-region-migrations", t: "Multi-Region Data and Migrations", d: "Active-active vs passive, geo-replication, online schema change, dual write, backfills", done: true }
    ]},
    { id: "m4", title: "Distributed Systems Theory", dir: "chapters", items: [
      { id: "27-failure-time-ordering", t: "Failure, Time and Ordering", d: "Partial failure, partitions, clock skew, Lamport and vector clocks, hybrid logical clocks", done: true },
      { id: "28-cap-consistency", t: "CAP, PACELC and Consistency Models", d: "Linearizable, sequential, causal, eventual, session guarantees, choosing per feature", done: true },
      { id: "29-consensus", t: "Consensus and Leader Election", d: "Quorums, Raft and Paxos concepts, split-brain, leases", done: true },
      { id: "30-coordination-locks", t: "Coordination Services and Distributed Locks", d: "ZooKeeper/etcd, leases, fencing tokens, lock pitfalls, config and membership", done: true },
      { id: "31-distributed-transactions", t: "Distributed Transactions", d: "2PC and its limits, saga overview, TCC, outbox and inbox", done: true },
      { id: "32-idempotency-ids", t: "Idempotency, Delivery Semantics and ID Generation", d: "Idempotency keys, at-most/at-least/exactly-once, UUID, Snowflake, ULID", done: true },
      { id: "33-gossip-merkle", t: "Gossip, Failure Detection and Merkle Trees", d: "Gossip protocols, phi-accrual detection, anti-entropy, Merkle trees", done: true }
    ]},
    { id: "m5", title: "Asynchronous Architecture", dir: "chapters", items: [
      { id: "34-queues-kafka", t: "Message Queues, Logs and Kafka", d: "Queue vs log vs pub/sub, partitions, offsets, consumer groups, ISR, retention, SQS/RabbitMQ", done: true },
      { id: "35-messaging-patterns", t: "Messaging Patterns", d: "Fan-out, competing consumers, ordering, retries, DLQ, poison messages, replay", done: true },
      { id: "36-event-driven", t: "Event-Driven Design", d: "Event notification vs state transfer, CQRS, event sourcing, change data capture", done: true },
      { id: "37-batch-stream", t: "Batch and Stream Processing", d: "MapReduce, Spark, Flink, windowing, watermarks, Lambda vs Kappa", done: true },
      { id: "38-scheduling-workflows", t: "Scheduling and Workflows", d: "Distributed cron, delayed jobs, orchestration engines", done: true }
    ]},
    { id: "m6", title: "Architecture and Resilience", dir: "chapters", items: [
      { id: "39-architecture-styles", t: "Architecture Styles and DDD", d: "Layered, hexagonal, modular monolith, bounded contexts, serverless", done: true },
      { id: "40-resilience", t: "Resilience Patterns and Tail Latency", d: "Timeouts, retries with jitter, circuit breaker, bulkhead, hedging, graceful degradation", done: true },
      { id: "41-ha-dr", t: "High Availability and Disaster Recovery", d: "Redundancy, failover, multi-AZ/region, RPO/RTO, backups", done: true },
      { id: "42-multitenancy-cells", t: "Multi-Tenancy and Cell-Based Architecture", d: "Isolation models, noisy neighbors, quotas, blast radius", done: true },
      { id: "43-deployment-autoscaling", t: "Deployment and Autoscaling", d: "Rolling, blue/green, canary, feature flags, containers, Kubernetes concepts, autoscaling", done: true }
    ]},
    { id: "m7", title: "Microservices in Depth", dir: "chapters", items: [
      { id: "44-monolith-to-microservices", t: "Monolith to Microservices", d: "When to split, cost of distribution, Conway's Law, strangler fig, distributed monolith", done: true },
      { id: "45-decomposition", t: "Service Decomposition", d: "By capability, subdomain, data ownership, granularity, boundary smells", done: true },
      { id: "46-microservice-data", t: "Data Management in Microservices", d: "Database per service, shared DB tradeoffs, API composition, CQRS views, data sync", done: true },
      { id: "47-service-communication", t: "Service Communication and Contracts", d: "REST vs gRPC vs messaging, sync vs async, contracts, consumer-driven tests, compatibility", done: true },
      { id: "48-sagas", t: "Sagas in Depth", d: "Choreography vs orchestration, compensation, timeouts, outbox/inbox, idempotent consumers", done: true },
      { id: "49-discovery-config", t: "Service Discovery and Configuration", d: "Client vs server discovery, registries, central config, secrets", done: true },
      { id: "50-service-mesh", t: "Service Mesh", d: "Sidecars, control vs data plane, mTLS, traffic shifting, tradeoffs", done: true },
      { id: "51-microservice-resilience", t: "Resilience Between Services", d: "Cascading failure, retry storms, timeout budgets, isolation in practice", done: true },
      { id: "52-microservice-observability", t: "Observability for Microservices", d: "Correlation IDs, distributed tracing, log aggregation, per-service SLOs", done: true },
      { id: "53-operating-microservices", t: "Operating Microservices", d: "Independent deployment, versioning, testing pyramid, zero trust, ownership and on-call", done: true }
    ]},
    { id: "m8", title: "Cross-Cutting Concerns", dir: "chapters", items: [
      { id: "54-observability-slos", t: "Observability and SLOs", d: "Logs, metrics, traces, RED/USE, alerting, SLI/SLO/SLA, error budgets", done: true },
      { id: "55-security", t: "Security for System Design", d: "AuthN vs authZ, OAuth2/OIDC/JWT, RBAC/ABAC, encryption, secrets, API security, DDoS/WAF", done: true },
      { id: "56-privacy-cost-mobile", t: "Privacy, Cost and Client/Mobile Concerns", d: "PII and GDPR, data residency, tiering, offline sync, push notifications", done: true }
    ]},
    { id: "m9", title: "Algorithms and Data Structures", dir: "chapters", items: [
      { id: "57-hashing-probabilistic", t: "Hashing and Probabilistic Structures", d: "Consistent hashing, Bloom filter, HyperLogLog, Count-Min Sketch", done: true },
      { id: "58-geospatial-text", t: "Geospatial and Text Structures", d: "Geohash, quadtree, S2, trie, inverted index", done: true },
      { id: "59-sorted-sets-crdt", t: "Sorted Sets, Top-K, CRDTs and OT", d: "Skip list, top-K, Merkle tree, CRDTs, Operational Transform", done: true }
    ]},
    { id: "m10", title: "Patterns and Interview Delivery", dir: "chapters", items: [
      { id: "60-pattern-playbook", t: "Recurring Design Patterns", d: "Read vs write heavy, fan-out, hot keys, contention control, large files, counting, ledgers, ML serving", done: true },
      { id: "61-delivery-playbook", t: "Interview Delivery Playbook", d: "Clarifying, structuring, tradeoff language, failure walkthroughs, senior/lead expectations", done: true }
    ]},
    { id: "m11", title: "Worked Case Studies", dir: "case-studies", items: [
      { id: "c01-url-shortener", t: "Design a URL Shortener", d: "ID generation, redirects, caching, analytics", done: true },
      { id: "c02-pastebin", t: "Design Pastebin", d: "Object storage, expiry, read-heavy caching", done: true },
      { id: "c03-rate-limiter", t: "Design a Rate Limiter", d: "Algorithms, distributed counters, placement", done: true },
      { id: "c04-key-value-store", t: "Design a Key-Value Store", d: "Partitioning, replication, quorums, LSM storage", done: true },
      { id: "c05-distributed-cache", t: "Design a Distributed Cache", d: "Sharding, eviction, hot keys, consistency", done: true },
      { id: "c06-news-feed", t: "Design a News Feed", d: "Fan-out on write vs read, ranking, celebrities", done: true },
      { id: "c07-chat", t: "Design a Chat System", d: "WebSockets, ordering, delivery, presence, storage", done: true },
      { id: "c08-notification-system", t: "Design a Notification System", d: "Channels, queues, retries, preferences, dedup", done: true },
      { id: "c09-file-sync", t: "Design Dropbox / Google Drive", d: "Chunking, sync, dedup, metadata, conflicts", done: true },
      { id: "c10-video-streaming", t: "Design YouTube / Netflix", d: "Upload, transcoding, CDN, adaptive streaming", done: true },
      { id: "c11-autocomplete", t: "Design Search Autocomplete", d: "Trie, top-K, freshness, serving", done: true },
      { id: "c12-web-crawler", t: "Design a Web Crawler", d: "Frontier, politeness, dedup, scale", done: true },
      { id: "c13-nearby-search", t: "Design Uber / Nearby Search", d: "Geospatial indexing, matching, location updates", done: true },
      { id: "c14-payment-system", t: "Design a Payment System", d: "Idempotency, ledger, reconciliation, sagas", done: true },
      { id: "c15-ticket-booking", t: "Design Ticket Booking / Flash Sale", d: "Contention, reservations, queues, fairness", done: true },
      { id: "c16-collaborative-editor", t: "Design a Collaborative Editor", d: "OT vs CRDT, sync, presence", done: true },
      { id: "c17-message-queue", t: "Design a Message Queue", d: "Log storage, partitions, consumers, durability", done: true },
      { id: "c18-job-scheduler", t: "Design a Job Scheduler", d: "Timers, leader election, retries, exactly-once effects", done: true },
      { id: "c19-metrics-logging", t: "Design Metrics and Log Aggregation", d: "Ingest, time-series storage, rollups, alerting", done: true },
      { id: "c20-ad-click-aggregation", t: "Design Ad Click Aggregation", d: "Stream processing, windows, exactly-once, reconciliation", done: true },
      { id: "c21-lock-service", t: "Design a Distributed Lock Service", d: "Consensus, leases, fencing, failure cases", done: true },
      { id: "c22-ecommerce-decomposition", t: "Decompose an E-commerce Monolith", d: "Boundaries, strangler fig, data split, sagas", done: true },
      { id: "c23-ride-sharing", t: "Design a Ride-Sharing Service", d: "Matching, live location, ETA, surge pricing", done: true },
      { id: "c24-hotel-booking", t: "Design a Hotel Booking System", d: "Inventory by date, overbooking, reservation holds, payments", done: true },
      { id: "c25-digital-wallet-ledger", t: "Design a Digital Wallet and Ledger", d: "Double-entry ledger, transfers, idempotency, reconciliation", done: true },
      { id: "c26-stock-exchange", t: "Design a Stock Exchange", d: "Order book, matching engine, sequencer, low latency, recovery", done: true },
      { id: "c27-object-storage-s3", t: "Design Object Storage (S3-like)", d: "Metadata vs data, erasure coding, durability, multipart upload", done: true },
      { id: "c28-unique-id-generator", t: "Design a Distributed Unique ID Generator", d: "Snowflake, clock issues, ordering, ranges, tradeoffs", done: true },
      { id: "c29-maps-routing", t: "Design Maps and Routing", d: "Tiles, geocoding, graph partitioning, shortest path, live traffic", done: true },
      { id: "c30-social-graph", t: "Design a Social Graph (Friends and Followers)", d: "Edge storage, mutual friends, recommendations, sharding", done: true },
      { id: "c31-twitter-search-trending", t: "Design Tweet Search and Trending Topics", d: "Indexing a firehose, real-time search, trending with sketches", done: true },
      { id: "c32-gaming-leaderboard", t: "Design a Gaming Leaderboard", d: "Sorted sets, ranking at scale, sharded leaderboards, time windows", done: true }
    ]},
    { id: "m12", title: "Cheat Sheets", dir: "chapters", items: [
      { id: "cs-numbers", t: "Cheat Sheet: Numbers to Remember", d: "Latency and capacity numbers", done: true, dir: "cheatsheets" },
      { id: "cs-decision-tables", t: "Cheat Sheet: Decision Tables", d: "Which DB, queue, cache strategy, consistency level", done: true, dir: "cheatsheets" },
      { id: "cs-failure-checklist", t: "Cheat Sheet: Failure Handling Checklist", d: "What to say about failures for any design", done: true, dir: "cheatsheets" },
      { id: "cs-microservices-checklist", t: "Cheat Sheet: Microservices Checklist", d: "Review checklist for a microservice design", done: true, dir: "cheatsheets" }
    ]},
    { id: "m13", title: "Reference", dir: "reference", items: [
      { id: "ref-glossary", t: "Glossary: A to Z", d: "Every term in one place, each linked to its chapter", done: true }
    ]}
  ]
};
