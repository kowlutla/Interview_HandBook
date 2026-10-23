# 1. Thinking in Systems and Architecture

This chapter establishes the reasoning tools used throughout the textbook. System design is not primarily the act of drawing boxes; it is the disciplined process of deciding how responsibilities, state, communication, constraints, and failure should fit together.

## 1.1 What is a system?

A **system** is a set of interacting elements whose combined behavior produces outcomes. In software, the elements may include processes, services, databases, queues, users, external providers, operators, and deployment infrastructure.

A system has:
- **Inputs:** requests, events, files, commands, schedules, or environmental signals.
- **Transformations:** validation, computation, coordination, persistence, and routing.
- **State:** information that influences future behavior.
- **Outputs:** responses, events, side effects, reports, or externally visible changes.
- **Environment:** networks, hardware, identity providers, other systems, people, and operating conditions.
- **Constraints:** correctness, latency, throughput, cost, security, legal obligations, and team capacity.

A component cannot be understood entirely in isolation if its behavior depends on another component's latency, state, availability, or contract. System behavior emerges from interactions as well as from individual components.

### A simple example

An order service may validate an order, reserve inventory, charge a payment method, persist order state, and send a confirmation. Each operation can work correctly alone while the workflow still fails: inventory might be reserved but payment may time out; payment may succeed while the response is lost; a confirmation may be sent twice. System design reasons about the end-to-end outcome and the intermediate states—not only each API.

## 1.2 Architecture is a set of consequential decisions

**Software architecture** describes the important structures and decisions that shape system behavior: component boundaries, responsibilities, communication paths, state ownership, deployment units, trust boundaries, failure domains, and rules that allow the system to evolve.

A diagram is one representation of architecture, not the architecture itself. Two diagrams can look identical while differing radically in transaction boundaries, consistency guarantees, retry behavior, security boundaries, or recovery behavior. Those properties often determine whether the system works in production.

**System design** is the reasoning process used to choose a structure that satisfies requirements within constraints. **High-Level Design (HLD)** focuses on major components, their responsibilities, interfaces, data flows, state ownership, and deployment relationships. **Low-Level Design (LLD)** focuses on internal classes/modules, algorithms, schemas, and detailed implementation. The boundary is contextual: a database schema may be low-level in one discussion but central to HLD when it determines partitioning, consistency, or service ownership.

Architecture decisions differ from ordinary implementation details because they tend to have broad consequences, affect multiple teams or components, and become expensive to reverse after data, clients, and operational processes depend on them.

## 1.3 Define the system boundary

A **system boundary** states what is inside the system being designed and what is treated as an external dependency. Without a boundary, scope expands indefinitely and responsibility becomes unclear.

For each boundary, identify:
- Which behavior the system owns.
- Which data it owns and may change.
- Which guarantees it promises to clients.
- Which dependencies it calls or receives events from.
- Which identity and trust assumptions apply.
- Who operates it and responds to failures.
- Which failure modes are inside versus outside its control.

An external provider can fail even if your code is correct. The system must define whether to fail the request, use cached data, queue work, degrade functionality, or retry within a deadline.

~~~mermaid
flowchart LR
  U[Users and external clients] -->|requests| G[System boundary]
  G --> A[Application capabilities]
  A --> D[(Owned data)]
  A --> X[External dependencies]
  O[Operations and security] -. governs .-> G
  O -. observes .-> A
  O -. protects .-> D
~~~

The dotted relationships matter: security, observability, deployment, and operational ownership cross component boundaries rather than living in a single box.

## 1.4 Start with the problem, not a technology

A reliable reasoning sequence is:

1. State the user or business outcome.
2. Define scope and explicit exclusions.
3. Identify functional behavior and quality attributes.
4. Identify important data, invariants, and access patterns.
5. Describe workload shape and growth.
6. Identify constraints and assumptions.
7. Compare viable structures and their trade-offs.
8. Specify failure behavior and operational ownership.
9. Validate with measurements, experiments, and review.

Choosing a database, broker, cloud, or microservice boundary before clarifying access patterns and correctness needs reverses this order. Technology can make some choices easier, but it cannot rescue a misunderstood requirement.

### Separate facts, assumptions, and decisions

These categories should not be mixed:
- **Fact:** confirmed by observation, a contract, a standard, or an authoritative source.
- **Assumption:** believed to be true for planning but not yet verified.
- **Constraint:** a condition the design must obey, such as a legal retention rule or fixed platform.
- **Decision:** a choice made among alternatives.
- **Risk:** an uncertain event or condition that could harm an objective.
- **Open question:** information needed before a consequential choice can be made.

For example, “the service receives 10,000 requests/s” is a fact only if supported by measurements or a binding requirement. Otherwise it is an assumption. A good design records how important assumptions will be tested.

## 1.5 Model behavior with responsibilities, state, and contracts

A component should have a clear responsibility and a contract with its callers. A useful contract specifies inputs, outputs, errors, side effects, timing expectations, authorization, and the meaning of success.

State ownership is especially important. Ask:
- Which component is authoritative for this fact?
- Which component is allowed to change it?
- What invariants must always hold?
- Can copies become stale?
- How are changes propagated?
- What happens if propagation is delayed or duplicated?

If two components both believe they own the same invariant, they can make conflicting decisions. A common design is to assign one authoritative owner and expose controlled commands or events to other components. Replicas and caches may hold copies, but copies need explicit freshness and reconciliation rules.

### Invariants versus workflow steps

An **invariant** is a condition that must remain true across all valid states. Examples include “an order identifier is unique” or “the same inventory unit cannot be sold twice.” A workflow is a sequence of actions intended to move the system between states. Workflows can fail halfway; invariants must still be protected.

This distinction helps identify which operations require atomic transactions, serialization, conditional updates, uniqueness constraints, idempotency, or reconciliation.

## 1.6 Decompose by responsibility and change

A component boundary should make some kind of change easier or isolate a meaningful concern. Useful signals include distinct domain rules, ownership of data invariants, different scaling needs, security boundaries, independent release cadence, and separate failure containment.

Two useful design qualities are:
- **Cohesion:** how strongly the elements inside a component belong together.
- **Coupling:** how much one component depends on the details or behavior of another.

High cohesion and manageable coupling generally make change safer. Coupling is not automatically bad: components must cooperate to deliver behavior. The goal is to make dependencies explicit, stable, and proportionate to the benefit of separation.

Over-fragmentation creates network calls, distributed transactions, duplicated operational work, and unclear ownership. Under-fragmentation creates entangled code, shared release risk, and competing responsibilities. There is no universal optimal number of components.

A **monolith** is deployed as one application unit; it can still have clear internal modules. A **modular monolith** enforces boundaries inside a shared deployment. **Microservices** split capabilities into independently deployable services and introduce network and operational failure modes. A **distributed system** has components that communicate across a network and must handle independent execution and partial failure. These categories overlap but are not synonyms.

### A boundary decision checklist

Before splitting a component into a separate service, ask:
1. Is there a clear capability or invariant it owns?
2. Is independent deployment or scaling genuinely valuable?
3. Is the interface stable enough to cross a network boundary?
4. Can its data ownership be defined without constant cross-service writes?
5. What happens when the network call times out or returns late?
6. Who owns alerts, on-call response, capacity, upgrades, and security?
7. Is the added operational cost justified by a measurable benefit?

If the answers are weak, a module inside one deployment may be the better boundary for now.

## 1.7 Architecture is multi-objective optimization

Typical objectives conflict:
- Lower latency can require more replicas, locality, or duplicated data.
- Stronger consistency can require coordination and increase write latency or reduce availability during partitions.
- Higher availability can require redundancy, graceful degradation, and careful dependency design.
- More isolation can reduce blast radius but increase cost and operational complexity.
- More abstraction can enable change but obscure behavior and add indirection.
- Longer retention can improve auditability and recovery but increase storage cost and privacy exposure.

A decision is meaningful only relative to a requirement and context. “Microservices scale better” is incomplete: a service can scale independently only if its bottlenecks and state boundaries allow it, and the organization can operate the resulting distributed system.

### Hard constraints, objectives, and trade-off frontiers

A **hard constraint** must be satisfied: for example, a legal data residency rule. An **objective** is something to optimize: for example, reduce p99 latency or infrastructure cost. A design that violates a hard constraint is not rescued by being excellent on another dimension.

Often there is no single design that is best on every dimension. A design is **Pareto-dominated** if another feasible design is at least as good on every considered objective and strictly better on at least one. The **Pareto frontier** contains feasible designs for which improving one objective requires sacrificing another. This is a useful way to compare options without pretending that every trade-off can be reduced to one universal score.

## 1.8 Reason about failure before implementation

A local function call often returns a result or throws an error within one process. A remote call has additional outcomes:
- The request never reaches the server.
- The server receives it but does not finish.
- The server commits the change but the response is lost.
- The response arrives after the caller's deadline.
- A dependency is slow rather than fully unavailable.
- A retry overlaps with the original operation.

Therefore, a timeout does **not** prove that an operation failed. It means the caller stopped waiting within a specified time. The result may be unknown. Safe recovery depends on operation semantics, idempotency, deduplication, status lookup, and transaction boundaries.

Design the failure contract for every critical dependency: timeout, retry policy, deadline, fallback, error mapping, and whether the caller can safely repeat the operation.

## 1.9 Use explicit decision records

An architecture decision record (ADR) should briefly capture:
- **Context:** the problem, constraints, and forces driving the choice.
- **Decision:** what was chosen and the scope of the choice.
- **Alternatives:** credible options considered and why they were not selected.
- **Consequences:** expected benefits, costs, and risks.
- **Assumptions:** what must remain true for the decision to be sound.
- **Validation:** measurements, experiments, or signals that will test it.
- **Revisit triggers:** changes in scale, requirements, team structure, or operational evidence that could invalidate it.

An ADR protects against hindsight bias and makes trade-offs visible. It is not a substitute for design detail, code, runbooks, or experiments. Record decisions at the level where they affect future choices; do not create paperwork for every trivial implementation detail.

## 1.10 A practical architecture reasoning loop

Architecture is not a one-time diagram. Requirements and constraints shape candidate designs; the design is validated against realistic workloads and failure modes; production evidence then informs the next decision.

~~~mermaid
flowchart TD
  A[Understand goals and constraints] --> B[Identify invariants and quality targets]
  B --> C[Model workload and dependencies]
  C --> D[Compare candidate designs]
  D --> E[Make trade-offs explicit]
  E --> F[Build and validate assumptions]
  F --> G[Operate and measure]
  G --> H{Assumptions still hold?}
  H -- Yes --> I[Continue and refine]
  H -- No --> A
~~~

The loop may be iterative rather than strictly sequential. A workload estimate may reveal that a requirement is too expensive; a security review may force a new boundary; a failure test may invalidate an availability assumption.

## 1.11 Common errors and how to detect them

- **Designing before understanding the problem:** requirements cannot be traced to design decisions.
- **Treating every quality attribute as equally important:** no explicit priorities or acceptable compromises exist.
- **Equating a diagram with correctness:** state transitions, retries, failure paths, and trust boundaries are missing.
- **Assuming remote calls behave like local calls:** timeouts, partial failure, and duplicate effects are not modeled.
- **Equating more services with better modularity:** ownership and operational costs are unclear.
- **Ignoring state ownership:** multiple components can mutate the same business fact without conflict rules.
- **Hiding uncertainty behind precise estimates:** assumptions are not written down and sensitivity is not checked.
- **Designing only the happy path:** no behavior is defined for timeouts, overload, partial completion, or recovery.
- **Failing to revisit decisions:** observed production behavior no longer matches the original model.

## 1.12 Self-check

You should be able to explain, in your own words:
1. Why architecture is more than a component diagram.
2. The difference between a requirement, constraint, assumption, decision, and risk.
3. Why state ownership and invariants affect component boundaries.
4. Why a modular monolith can have strong modularity without distributed-system overhead.
5. Why a remote timeout does not establish whether a write committed.
6. How a Pareto frontier helps compare feasible designs.
7. What evidence would cause you to revisit an architecture decision.

## Further reading

- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework) — practitioner guidance for architecture quality.
- [Microsoft Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/) — patterns and their contexts.
- [Martin Fowler on microservices](https://martinfowler.com/articles/microservices.html) — trade-offs and organizational implications.
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — reliability, service operation, and production feedback.

---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
