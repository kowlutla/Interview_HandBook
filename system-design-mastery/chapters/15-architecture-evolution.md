# 15. Architectural Boundaries and Evolution

## Boundaries around change and invariants
A module or service boundary should make responsibility, ownership and invariants clearer. Domain-driven design uses bounded contexts to identify where a model and its language are consistent. “Customer” can mean different things in identity, billing and support; forcing all domains to share one model may create coupling.

Service boundaries should consider data ownership, transaction boundaries, team ownership, scaling profile, security, deployment cadence and failure containment. If two services constantly need synchronous round trips or distributed transactions to preserve one invariant, the boundary may be wrong or the workflow needs a different contract.

## Monolith, modular monolith and microservices
A monolith deploys as one unit. A modular monolith keeps internal boundaries within that deployment. Microservices permit independent deployment and scaling but require discovery, network resilience, versioned contracts, data ownership, observability and operational maturity.

Microservices are not an automatic scalability strategy. If boundaries are unstable or the team cannot operate distributed infrastructure, a modular monolith may provide better change velocity and reliability. Explicit module boundaries make later extraction easier.

## Data ownership and composition
Private data stores support service ownership and reduce accidental cross-service writes, but complicate cross-domain queries. API composition or materialized read models can combine information at the cost of extra calls or eventual consistency. A shared database can be a pragmatic transition, but ungoverned cross-service schema access creates hidden coupling.

## Orchestration and choreography
Orchestration centralizes workflow progression in a coordinator. Choreography lets services react to events. Orchestration makes transitions visible but can create a complex coordinator; choreography avoids central control but can obscure end-to-end behavior. Both need timeouts, retries, duplicate handling, terminal states, compensation and observability.

## CQRS, event sourcing and outbox
CQRS separates command handling from query models. Event sourcing stores domain events as authoritative history. The outbox pattern atomically records a business update and an event to publish in one local transaction. They solve different problems and should not be bundled automatically.

Use CQRS when read/write models materially differ; event sourcing when history is central; outbox when dual-write reliability matters. Each adds operational and cognitive cost.

## Sidecars, service meshes, control and data planes
A sidecar places supporting behavior next to an application. A service mesh may provide traffic policy, service identity and telemetry, but adds control-plane dependencies and configuration complexity. Do not move business semantics into infrastructure merely because it can intercept traffic.

The data plane handles ordinary production traffic. The control plane configures, schedules or changes the data plane. A control-plane outage need not stop existing traffic if the system is designed to retain safe configuration, but the desired behavior must be explicit.

## Migration and technical debt
The strangler pattern gradually routes selected functionality from a legacy system to a replacement. It needs a routing boundary, data synchronization strategy, rollback plan, observability and retirement criteria. Dual writes and dual reads create consistency risks; migration phases should be explicit and measurable.

Technical debt is the future cost created by constraints, shortcuts, unclear ownership and deferred maintenance. Record why a compromise was made, what conditions make it harmful, and what signal should trigger revisiting it.

## Further reading
- Fowler, [Microservices](https://martinfowler.com/articles/microservices.html).
- Fowler, [Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html).
- Microsoft [Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/).
