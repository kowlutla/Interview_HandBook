# Research and Reference Library

Prefer primary sources for formal guarantees. Product documentation describes a particular implementation and should not automatically be generalized. Chapter authors should cite sources close to the claims they support and recheck exact sections during final audit.

## Distributed systems and theory
- Gilbert and Lynch, *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services* (2002): [MIT-hosted paper](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf).
- Gilbert and Lynch, *Perspectives on the CAP Theorem* (2012): [MIT DSpace record](https://dspace.mit.edu/entities/publication/dfcb6512-af44-4fc9-8e8b-1a8f28f1b53a).
- Ongaro and Ousterhout, *In Search of an Understandable Consensus Algorithm (Raft)*: [USENIX paper PDF](https://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf) and [paper/dissertation resources](https://raft.github.io/).
- Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System* (1978): [original paper](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).
- Fischer, Lynch and Paterson, *Impossibility of Distributed Consensus with One Faulty Process* (1985): [DOI](https://doi.org/10.1145/3149.214121).
- Brewer, *CAP Twelve Years Later: How the Rules Have Changed* (2012): [DOI](https://doi.org/10.1109/MC.2012.37).

## Network and identity standards
- IETF, [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
- IETF, [RFC 9293 — TCP](https://www.rfc-editor.org/rfc/rfc9293.html).
- IETF, [RFC 9000 — QUIC](https://www.rfc-editor.org/info/rfc9000/).
- IETF, [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html).
- IETF, [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html).
- IETF, [RFC 5861 — HTTP cache-control extensions](https://www.rfc-editor.org/rfc/rfc5861.html).
- IETF, [RFC 9700 — OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html).
- IETF, [RFC 6749 — OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749.html).
- OpenID Foundation, [OpenID Connect specifications](https://openid.net/developers/specs/).

## Databases and storage
- PostgreSQL, [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [indexes](https://www.postgresql.org/docs/current/indexes.html), [EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), [point-in-time recovery](https://www.postgresql.org/docs/current/continuous-archiving.html).
- SQLite, [atomic commit](https://www.sqlite.org/atomiccommit.html).
- O'Neil et al., *The Log-Structured Merge-Tree (LSM-Tree)* (1996): [DOI](https://doi.org/10.1007/s002360050048).

## Messaging and events
- Apache Kafka, [design](https://kafka.apache.org/documentation/#design), [delivery semantics](https://kafka.apache.org/documentation/#semantics), and [documentation](https://kafka.apache.org/documentation/).
- Debezium, [outbox event router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html).
- [CloudEvents specification](https://cloudevents.io/).

## Reliability and operations
- Dean and Barroso, [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/) — tail-latency variability, fan-out and hedged requests.
- Google, [Site Reliability Engineering book](https://sre.google/sre-book/table-of-contents/).
- Google, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) and [Service Best Practices / Error Budgets](https://sre.google/sre-book/service-best-practices/).
- Google, [SRE Workbook: Error Budget Policy](https://sre.google/workbook/error-budget-policy/).
- Google Cloud, [Well-Architected Reliability pillar](https://docs.cloud.google.com/architecture/framework/reliability).
- AWS, [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html).
- NIST, [Cybersecurity Framework](https://www.nist.gov/cyberframework).

## Runtime, cloud and architecture
- Docker, [container fundamentals](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).
- Kubernetes, [cluster architecture](https://kubernetes.io/docs/concepts/architecture/), [resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), [probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).
- OpenTelemetry, [documentation](https://opentelemetry.io/docs/).
- Fowler, [Microservices](https://martinfowler.com/articles/microservices.html) and [Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html).
- Microsoft, [Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/).
- Google, [Cloud Architecture Framework](https://cloud.google.com/architecture/framework).


## Architecture documentation, accessibility and sustainability
- C4 model, [Diagrams](https://c4model.com/diagrams), [Introduction](https://c4model.com/introduction), and [Abstractions](https://c4model.com/abstractions). Use the model to communicate different levels of static structure; add dynamic and deployment views when those questions matter.
- W3C, [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/wcag/).
- AWS, [Sustainability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html).
- Google Cloud, [Sustainability pillar](https://docs.cloud.google.com/architecture/framework/sustainability). These cloud sources are provider guidance, not universal environmental accounting standards.

## Architecture styles, traffic management and security
- Microsoft Azure Architecture Center, [Architecture styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles) and [Microservices architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices).
- AWS, [Elastic Load Balancing documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html).
- AWS API Gateway, [HTTP API throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-throttling.html). Treat documented throttles as implementation behavior, not universal API gateway semantics.
- Cloudflare, [Origin Cache Control](https://developers.cloudflare.com/cache/concepts/cache-control/) and [CDN-Cache-Control](https://developers.cloudflare.com/cache/concepts/cdn-cache-control/). These describe Cloudflare-specific behavior; use RFC 9111 for general HTTP caching semantics.
- OWASP, [API Security Top 10](https://api-security.owasp.org/editions/2023/en/0x00-header/).


## Protocol standards and secure integrations
- IETF, [RFC 8200 — IPv6 Specification](https://www.rfc-editor.org/rfc/rfc8200.html).
- IETF, [RFC 4033 — DNS Security Introduction and Requirements](https://www.rfc-editor.org/rfc/rfc4033.html).
- IETF, [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html).
- OWASP, [Webhook Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html).
- CISA and international partners, [Software Bill of Materials (SBOM) guidance](https://www.cisa.gov/sbom).

## Evidence labels
In chapter prose, distinguish formal specification/research, implementation documentation, practitioner guidance, and illustrative assumptions. Avoid copying source wording; synthesize it into an original explanation.


## Software supply-chain security
- NIST, [Secure Software Development Framework SP 800-218 v1.1](https://csrc.nist.gov/pubs/sp/800/218/final); the NIST page also lists later draft/revision status.
- SLSA, [Build track basics](https://slsa.dev/spec/v1.0/), [build provenance](https://slsa.dev/spec/v1.0/provenance), and [current provenance specification](https://slsa.dev/spec/build-provenance).
- SPDX, [specifications](https://spdx.dev/use/specifications/) and the [SPDX 3.0.1 specification](https://spdx.github.io/spdx-spec/).
