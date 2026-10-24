# 5. Networks and Request Journeys

A request rarely travels directly from a client to an application and back. It may pass through DNS, a transport connection, TLS, a proxy or load balancer, the application, and one or more dependencies. Each step has its own behavior and failure modes.

The useful mental model is to follow the request end to end. Networking concepts become easier to understand when you connect them to practical questions: Why did a connection fail? Why is the service slow even though the application CPU is low? Why did changing DNS not move all traffic? Why can a request time out even when the operation succeeded?

## A layered mental model: OSI and TCP/IP

The OSI model separates networking into seven conceptual layers: physical, data link, network, transport, session, presentation and application. The practical TCP/IP model groups responsibilities differently, commonly described as link, internet, transport and application. These models are maps for reasoning, not a claim that every production component fits neatly into one layer.

For architecture work, ask which layer owns the behavior. IP routing and subnets affect reachability; TCP or QUIC affect transport delivery and congestion; TLS protects the connection and authenticates identities; HTTP defines request semantics; proxies and gateways apply routing or policy; application code enforces business authorization and invariants. A symptom can cross layers, so use the models to organize evidence rather than guess a cause from the layer name alone.

## 5.1 Follow one request

A simplified request path looks like this:

~~~mermaid
sequenceDiagram
  participant C as Client
  participant D as DNS Resolver
  participant E as Edge or Proxy
  participant A as Application
  participant DB as Data Store
  C->>D: Resolve name if no usable cached answer
  D-->>C: Address record
  C->>E: Establish or reuse a protected connection
  E->>A: Forward request and relevant context
  A->>DB: Execute a bounded data operation
  DB-->>A: Result or error
  A-->>E: HTTP response
  E-->>C: Response
~~~

This is a model, not a mandatory sequence for every request. DNS may already be cached, TLS may terminate at the edge, and a persistent connection may avoid another handshake. Some requests never reach the database because a cache or application-level check can answer them.

The important point is that every hop adds a possible source of delay, failure, configuration mismatch, or trust boundary. A useful diagnosis follows the actual path and correlates evidence from the client, network edge, application, and dependencies.

## 5.2 IP addresses, routing, and NAT

IP addresses identify network interfaces within an addressing and routing system. Routers forward packets according to routing tables. CIDR notation expresses a network prefix: for example, `192.0.2.0/24` means the first 24 bits identify the prefix. IPv4 uses 32-bit addresses; IPv6 uses 128-bit addresses.

A packet's route can change, and its outbound and return paths need not be identical. Firewalls, network access controls, NAT, proxies, and service meshes operate at different points in the path. When a connection fails, identify which component sees the packet and which rule or route applies instead of treating “the network” as one box.

Network Address Translation (NAT) rewrites address or port information and maintains mappings. It commonly allows private-addressed hosts to share public addresses, but it is not a complete security boundary. Stateful network devices may also expire idle mappings, which can disrupt long-lived connections if the application does not detect and recover from the loss.

A subnet plan must account for routing, reserved addresses, future growth, and provider-specific rules. Do not assume every address in a prefix can be assigned to a workload.

## 5.3 TCP, UDP, and QUIC

TCP provides a reliable, ordered byte stream between endpoints. It retransmits lost data and uses congestion control to respond to network conditions. TCP does **not** preserve application message boundaries: two application writes can arrive in one read or be split across several reads. An application protocol must define its own framing.

TCP's ordered delivery also creates head-of-line blocking. If a segment is lost, later bytes on that same stream cannot be delivered to the application in order until the missing data is recovered. HTTP/2 multiplexes multiple streams over one TCP connection, so a TCP loss event can delay data for several HTTP/2 streams on that connection.

UDP sends datagrams without TCP's built-in reliability or ordering. Applications using UDP must decide what reliability, congestion control, and security behavior they need. QUIC, used by HTTP/3, runs over UDP and provides transport features including independently progressing streams. This avoids the specific cross-stream ordering dependency caused by TCP loss, but it does not eliminate congestion, packet loss, or shared connection-capacity limits.

Two different controls are worth separating:

- **Flow control** protects a receiver from being overwhelmed by a sender.
- **Congestion control** responds to conditions in the network path to avoid injecting traffic faster than the path can handle.

Application-level backpressure is a third concern. A TCP connection can be healthy while the service behind it is overloaded and accumulating work.

## 5.4 DNS: names, caching, and change propagation

DNS maps names to records. A typical lookup may use a local cache, recursive resolver, root server, top-level-domain server, and authoritative server. In practice, a cached answer often means not all these steps occur for every request.

Common records include A (IPv4 address), AAAA (IPv6 address), CNAME (alias), MX (mail exchanger), TXT (text data often used for verification and policy), NS (name-server information), and SRV (service location for protocols that use it).

TTL influences how long a record may be reused, but changing a record is not an instantaneous global traffic switch. Resolvers and applications may have their own caches, and clients can continue using existing connections after DNS changes. Plan migrations with overlap between old and new destinations, health checks, compatible backends, and a rollback path.

DNS success also proves very little beyond resolution: the destination may still be unreachable, the TLS identity may be wrong, or the application may be unhealthy.

## 5.5 TLS protects a connection; it does not authorize an action

TLS provides confidentiality and integrity and can authenticate the server through certificates. Mutual TLS can also authenticate a client. Correct authentication depends on validating the certificate chain and the intended hostname or identity—not merely checking that a certificate exists.

Certificate expiry, renewal failures, incorrect trust roots, hostname mismatches, and protocol configuration can all cause production failures. Disabling certificate validation to work around an error removes a key protection. Private keys need appropriate access controls and rotation procedures.

TLS termination at a proxy changes the trust path. If the connection from the proxy to the application crosses an untrusted network, that hop needs its own protection. Similarly, forwarded client-identity headers should be trusted only when they are inserted or sanitized by known proxies. A securely encrypted request can still be unauthorized; authentication and authorization remain separate decisions.

## 5.6 HTTP versions and request semantics

HTTP defines application-level request and response semantics. The main versions differ in framing and transport:

| Version | What matters architecturally |
|---|---|
| HTTP/1.1 | Persistent connections are supported; parallelism commonly uses multiple connections. |
| HTTP/2 | Binary framing and multiplexed streams share a TCP connection. TCP-level loss can affect multiple streams on that connection. |
| HTTP/3 | HTTP runs over QUIC, which uses UDP and avoids TCP's cross-stream ordering dependency. |

A newer version is not automatically faster in every deployment. Handshake behavior, network conditions, server support, proxies, and client mix all matter.

Connection reuse avoids repeated setup costs, but connection pools need limits, idle lifetimes, stale-connection handling, and acquisition timeouts. An unbounded wait for a pool slot can tie up request threads and contribute to cascading timeouts.

HTTP method semantics also matter for retries. A transport connection can acknowledge bytes without proving that the application operation completed. A request may reach the server and commit successfully while the response is lost. For non-idempotent business operations, application-level idempotency keys, durable deduplication, or a status lookup may be needed to resolve uncertain outcomes.

## 5.7 Proxies, load balancers, and CDNs

These components are often combined in one product, but their responsibilities are different.

A **forward proxy** acts on behalf of clients. A **reverse proxy** receives traffic on behalf of origin services. A **load balancer** distributes connections or requests among backends. A **CDN** serves cacheable content from edge locations, often reducing latency and origin load.

Layer 4 load balancing primarily uses transport-level information. Layer 7 load balancing can route using application details such as host, path, or headers. Common balancing strategies include round robin, weighted routing, and least-connections-style approaches. The best choice depends on request duration, instance capacity, and the implementation's behavior.

Health checks are imperfect observations. A process can respond to a simple health endpoint while still being unable to serve real requests. Readiness should indicate whether an instance can accept traffic; liveness should be used carefully because aggressive restart loops can worsen overload. Draining matters during deployment so existing work has time to finish where the protocol and application allow it.

A CDN's cache key must represent every request dimension that changes the response. If tenant identity, authorization, or a relevant query parameter is accidentally omitted, one user's content can be served to another. Cache freshness, stale serving, origin shielding, purge behavior, and origin failover should be chosen deliberately—not assumed from the word “CDN.”

For traffic spanning regions, global traffic management may use DNS-based routing, anycast, provider routing services, or combinations of these. Health signals, routing policy, client/resolver caching and existing connections mean a traffic shift is not necessarily immediate. A regional failover plan must also account for warm capacity, data consistency, dependency availability and the risk of sending all traffic to a cold or under-sized destination.

Session affinity (sticky routing) sends a client's requests to the same target when possible. It can simplify some in-memory session designs, but it may create uneven load and complicate failover; it does not guarantee that a session survives target loss. Prefer explicit shared or client-carried session state when appropriate, and use affinity only when its trade-offs are understood.

## 5.8 Firewalls, WAFs, and private connectivity

Network security controls serve different purposes:

- A **firewall** or cloud security rule controls permitted network flows.
- A **Web Application Firewall (WAF)** evaluates application-layer traffic against configured rules.
- **Network segmentation** limits which components can reach one another.
- **Private endpoints** and private routing can reduce exposure of service traffic to public networks.
- **Egress controls** restrict where workloads may initiate connections.

These controls are complementary, not interchangeable. A WAF does not replace application authorization, and a private network does not make every workload trustworthy. Use the minimum required connectivity and verify the real path through routing, NAT, proxies, and policy enforcement.

### A few protocol details that change design decisions

IPv4 and IPv6 may coexist in the same deployment. A service that works over IPv4 is not necessarily configured correctly for IPv6: DNS records, firewall rules, listeners, routing, monitoring, and dependency access all need to match the intended address families. Test the actual client-to-service path rather than assuming dual-stack support from one successful request.

DNS security mechanisms solve different problems. DNSSEC lets validating resolvers verify the authenticity and integrity of DNS data; it does not encrypt the lookup. DNS over HTTPS (DoH) and DNS over TLS (DoT) encrypt the client-to-resolver channel, but encryption alone does not prove that the returned DNS data is authentic. Choose based on the threat model and operational environment.

Mutual TLS adds client-certificate authentication to TLS, but the application still needs authorization. Likewise, HTTP caching directives and CDN-specific controls must agree: a shared cache must not reuse personalized or tenant-specific responses across users, and a purge request is only useful if it reaches the relevant cache layers.

Finally, denial-of-service protection is a capacity and trust-boundary problem as well as a filtering problem. Volumetric traffic can saturate links or upstream capacity before an application firewall sees the request. Lower-volume attacks can exhaust connection slots, TLS handshakes, request workers, queues, or expensive application operations. Use layered controls—upstream mitigation where needed, bounded connections and queues, rate limits, request-size and execution limits, and graceful overload behavior. No single WAF rule or autoscaling policy protects every layer.

## 5.9 Timeouts and connection lifecycles

Different timeouts protect different stages: DNS lookup, TCP connection establishment, TLS handshake, connection-pool acquisition, request processing, downstream reads and writes, and idle connections. They should fit within an overall request deadline.

For example, if an incoming request has 500 ms remaining, starting a downstream call with a fresh two-second timeout allows work to continue after the caller has given up. Propagate the remaining budget, cancel work that is no longer useful, and leave time for cleanup and response generation.

Connection pools improve efficiency but are finite resources. A small pool may queue requests; a large pool may overwhelm the database or downstream service. Monitor pool wait time, active connections, connection errors, request latency, and downstream saturation together.

A timeout means the expected result was not observed within the configured interval. It does not prove that the remote operation did not execute. For writes, use idempotency or reconciliation to handle uncertain outcomes.

## 5.10 Troubleshoot from evidence, not guesses

When a request fails, investigate in the order of the actual path. The following table is a starting point, not a substitute for telemetry.

| Symptom | Evidence to gather | Possible explanations |
|---|---|---|
| Name lookup fails | Resolver response, TTL, configured resolver, client cache | Incorrect record, resolver outage, stale local configuration |
| Connection cannot be established | Route, firewall decision, SYN/SYN-ACK behavior, NAT state | Unreachable endpoint, blocked port, exhausted mapping or backlog |
| TLS handshake fails | Certificate chain, hostname, expiry, negotiated protocol | Certificate/configuration mismatch, trust issue, incompatible settings |
| Requests stall before reaching the app | Load-balancer logs, connection counts, queue/pool wait | Routing, health-check, connection-pool or edge saturation |
| Latency rises but CPU stays low | Distributed trace, downstream timings, pool waits, queue depth | Network wait, lock contention, slow dependency, connection starvation |
| Clients time out after a deployment | Per-hop deadlines, rollout timing, error rates, connection reuse | Slow startup, readiness error, pool exhaustion, dependency regression |
| DNS change has no immediate effect | Resolver answers, client cache, open connections | Cached records, runtime-level caching, reused connections |

A disciplined investigation compares timestamps and request identifiers across client, edge, application, and dependency telemetry. Check one hypothesis at a time. Increasing timeouts may hide the symptom while increasing the number of requests waiting in the system.

## 5.11 A practical review checklist

Before approving a network-facing design, be able to answer:

- Where does DNS resolution happen, and how are changes rolled out?
- Where does TLS terminate, and which identities are validated at each hop?
- Which layer routes traffic, checks health, and drains connections?
- What is the cache key, freshness policy, and invalidation path?
- Are timeouts bounded by one end-to-end deadline?
- What happens when a pool, network path, resolver, or downstream service is saturated?
- Which forwarded headers are trusted, and from which proxies?
- How can operators distinguish a network failure from an application or dependency failure?

These questions connect the protocol details to architectural decisions. You do not need to memorize every packet field to design a good system, but you do need to know which layer owns a behavior and what evidence can confirm it.

## Further reading

- IETF, [RFC 8200 — IPv6 Specification](https://www.rfc-editor.org/rfc/rfc8200.html).
- IETF, [RFC 4033 — DNS Security Introduction and Requirements](https://www.rfc-editor.org/rfc/rfc4033.html).
- IETF, [RFC 9293 — TCP](https://www.rfc-editor.org/rfc/rfc9293.html).
- IETF, [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html).
- IETF, [RFC 9000 — QUIC Transport](https://www.rfc-editor.org/info/rfc9000/).
- IETF, [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html), and [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html).
- AWS, [Elastic Load Balancing overview](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html) for provider-specific behavior.
- Cloudflare, [Origin Cache Control](https://developers.cloudflare.com/cache/concepts/cache-control/) and [CDN-Cache-Control](https://developers.cloudflare.com/cache/concepts/cdn-cache-control/) for CDN-specific behavior.

---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
