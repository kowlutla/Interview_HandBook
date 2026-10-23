# 9. Caching and Data Locality

## Why cache?
A cache stores reusable data closer to the consumer or in a faster access layer. It can reduce latency, repeated database work and network transfer. Benefit depends on reuse: caching rarely requested data may add complexity without meaningful savings. A cache is usually not the source of truth; if treated as authoritative, durability and consistency need explicit design.

## Common patterns
- **Cache-aside:** application checks cache, loads source on miss, then populates cache. Simple, but concurrent misses can stampede and invalidation belongs to the application.
- **Read-through:** cache abstraction loads from source on miss.
- **Write-through:** update cache and source in the write path; ordering and partial failure matter.
- **Write-behind:** acknowledge before asynchronously persisting. This can reduce latency but requires durable buffering and recovery.
- **Write-around:** writes bypass cache; subsequent reads populate it.

Pattern labels alone do not define atomicity; inspect the implementation contract.

## TTL and invalidation
A time-to-live limits how long an entry remains eligible. It does not guarantee freshness relative to every source update. Invalidation can be explicit, version-based, event-driven or time-based. A stale-fill race occurs when an older read finishes after invalidation and repopulates stale data. Version checks or ordering mechanisms may be needed.

## Eviction and sizing
LRU approximates recency; LFU approximates frequency. Scan-heavy workloads can pollute recency-based caches, while frequency-based policies can retain formerly popular entries. Usable cache capacity is lower than physical RAM because keys, values, object/allocator overhead, metadata, fragmentation and replication consume memory.

## Failure modes
- **Stampede:** many requests fetch/recompute one expired key.
- **Penetration:** absent keys repeatedly hit the backing store.
- **Avalanche:** many expirations or cache outage suddenly overloads the source.
- **Hot key:** one key receives disproportionate traffic.
- **Stale fill race:** old data repopulates after a newer update.
- **Cache outage:** fallback traffic overwhelms the backing system.

Mitigations include request coalescing, jittered TTLs, negative caching, bounded concurrency, stale-while-revalidate where safe, and rate limiting. Negative caching can hide a newly created record until expiry or invalidation.

## Local, distributed and CDN caches
Process-local caches avoid network latency but each instance has separate entries and invalidation state. Distributed caches share entries but add network and operational dependency. Multi-level caches reduce latency but complicate coherence.

CDNs cache near users. Keys must include every dimension that changes the representation, such as locale or authorization context; missing a dimension can serve incorrect or private content. HTTP caching behavior is defined by [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html); stale response extensions are described in [RFC 5861](https://www.rfc-editor.org/rfc/rfc5861.html).

## Quantifying benefit
If 90% of 2,000 lookups/s hit cache, about 200 lookups/s reach the source for that lookup class. If each miss causes three database queries, the source sees about 600 queries/s. Average hit ratio can hide correlated expiration bursts.

~~~mermaid
sequenceDiagram
  participant App
  participant Cache
  participant DB
  App->>Cache: Get key
  alt Hit
    Cache-->>App: Value
  else Miss
    Cache-->>App: Miss
    App->>DB: Read authoritative value
    DB-->>App: Value and version
    App->>Cache: Populate with bounded TTL
    App-->>App: Return value
  end
~~~

The diagram omits concurrent misses and invalidation races; real designs must address them.

## Further reading
- [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html).
- [Redis eviction documentation](https://redis.io/docs/latest/develop/reference/eviction/).
