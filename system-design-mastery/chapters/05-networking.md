# 5. Networks and Request Journeys

## 5.1 Layering is a diagnostic model

The OSI model separates physical, link, network, transport, session, presentation, and application concerns. The Internet protocol suite is commonly described with link, internet, transport, and application layers. These are conceptual models, not exact diagrams of every implementation.

Layering helps locate responsibilities: IP routes packets; TCP provides an ordered byte stream; TLS protects a communication channel; HTTP defines application semantics. A failure at one layer can appear as a symptom at another, so diagnostics need correlation across layers.

## 5.2 IP, routing, subnetting, and NAT

IP addresses identify network interfaces within a routing system. Prefix length describes which bits identify a network. Routers forward packets based on routing tables; the path can change and is not necessarily symmetric. Network Address Translation (NAT) rewrites address/port information and maintains mappings, often allowing private-addressed hosts to share public addresses. NAT is not, by itself, a complete security boundary.

A network partition means some communicating components cannot exchange messages reliably within the relevant time assumptions. It does not require every packet to be permanently lost; delay and one-way reachability can be enough to make participants disagree about availability.

## 5.3 TCP and UDP

TCP provides a reliable, ordered byte stream between endpoints, with retransmission and congestion control. It does not preserve application message boundaries, and it does not guarantee that an application-level operation completed merely because bytes were acknowledged by the transport.

UDP sends datagrams without TCP's built-in reliability and ordering. Applications using UDP must decide what reliability, congestion control, and security behavior they need. QUIC, used by HTTP/3, implements transport features over UDP rather than relying on TCP's stream behavior.

TCP retransmissions can cause delay. Loss of a packet can affect delivery of later bytes on the same TCP stream until missing data is recovered. HTTP/2 multiplexes streams over a TCP connection, so TCP-level loss can delay multiple streams on that connection. HTTP/3 uses QUIC streams to reduce this cross-stream transport head-of-line blocking, though congestion and path problems can still affect traffic.

## 5.4 DNS is a distributed naming system

A typical DNS lookup may use a local cache, recursive resolver, root server, top-level-domain server, and authoritative server. Caching reduces lookup latency and load; TTL influences how long records may be reused. TTL expiry does not instantly guarantee global propagation, because resolvers and applications may have their own caches or stale-serving policies.

DNS provides name-to-record resolution, not instantaneous global traffic switching. A client may continue using an existing connection or cached address after DNS changes.

## 5.5 TLS and HTTPS

TLS provides confidentiality and integrity and can authenticate the server through certificates; mutual TLS can also authenticate clients. Correct deployment depends on certificate validation, trust roots, hostname checks, protocol configuration, key protection, and renewal. Encryption does not replace authorization: a securely encrypted request can still be unauthorized.

HTTPS identifies a secure HTTP origin. The HTTP semantics are described in [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html); TLS 1.3 is specified in [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).

## 5.6 HTTP versions

- **HTTP/1.1** uses textual message syntax and supports persistent connections; parallelism often uses multiple connections.
- **HTTP/2** uses binary framing and multiplexed streams on a connection, with header compression.
- **HTTP/3** maps HTTP semantics onto QUIC, which uses UDP and provides independently progressing streams.

The versions share core HTTP semantics; the transport and framing differ. Newer does not mean every deployment is faster: handshake setup, network conditions, server support, proxy behavior, and client mix matter. See [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) and [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html).

## 5.7 Proxies, load balancers, and CDNs

A forward proxy acts on behalf of clients; a reverse proxy receives traffic on behalf of origin services. A load balancer distributes work among backends. A CDN serves content from edge locations, often using cache policies and origin shielding. These roles may be combined in one product, but the responsibilities remain distinct.

Health checks are imperfect observations. A process responding to a health endpoint may still be unable to serve a real request. Readiness should reflect whether the instance can accept traffic; liveness should be used carefully because aggressive restart loops can worsen overload.

## 5.8 Trace a request

~~~mermaid
sequenceDiagram
  participant C as Client
  participant D as DNS Resolver
  participant E as Edge/Proxy
  participant A as Application
  participant DB as Data Store
  C->>D: Resolve service name if cache misses
  D-->>C: Address record
  C->>E: Establish transport and TLS as needed
  E->>A: Forward request with deadline/context
  A->>DB: Query using bounded connection
  DB-->>A: Result or error
  A-->>E: HTTP response
  E-->>C: Response
~~~

This is a simplified journey: DNS may be resolved by a local stub or proxy, TLS may terminate at the edge, and persistent connections may avoid repeating handshakes. Each hop adds potential queueing, timeouts, retries, and trust boundaries.

## 5.9 Timeouts and connection reuse

A connect timeout, TLS handshake timeout, request deadline, idle timeout, and downstream read timeout govern different phases. A total deadline should be propagated so downstream work does not continue indefinitely after the caller has abandoned the request. Connection pooling reduces handshake and setup costs but requires stale-connection handling, pool limits, and safe reuse.

## Further reading
- IETF [RFC 9293 — TCP](https://www.rfc-editor.org/rfc/rfc9293.html).
- IETF [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html).
- IETF [RFC 9000 — QUIC](https://www.rfc-editor.org/rfc/rfc9000.html).
- IETF [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html).
