# Lesson 01.02 — Decompose by responsibility and change

## 1.3 Decompose by responsibility and change

A component boundary should make some kind of change easier or isolate a meaningful concern. Useful signals include distinct domain rules, ownership of data invariants, different scaling needs, security boundaries, independent release cadence, and separate failure containment.

Over-fragmentation creates network calls, distributed transactions, duplicated operational work, and unclear ownership. Under-fragmentation creates entangled code, shared release risk, and competing responsibilities. There is no universal optimal number of components.

A **monolith** is deployed as one application unit; it can still have clear internal modules. A **modular monolith** enforces boundaries inside a shared deployment. **Microservices** split capabilities into independently deployable services and introduce network and operational failure modes. A **distributed system** has components that communicate across a network and must handle independent execution and partial failure. These categories overlap but are not synonyms.


## 1.4 Architecture is multi-objective optimization

Typical objectives conflict:
- Lower latency can require more replicas, locality, or duplicated data.
- Stronger consistency can require coordination and increase write latency or reduce availability during partitions.
- Higher availability can require redundancy, graceful degradation, and careful dependency design.
- More isolation can reduce blast radius but increase cost and operational complexity.
- More abstraction can enable change but obscure behavior and add indirection.

A decision is meaningful only relative to a requirement and context. “Microservices scale better” is incomplete: a service can scale independently only if its bottlenecks and state boundaries allow it, and the organization can operate the resulting distributed system.


## 1.5 Record assumptions and decisions

An architecture decision record (ADR) should briefly capture:
- Context and forces driving the decision.
- Decision and considered alternatives.
- Expected consequences and known risks.
- Assumptions that would invalidate the choice.
- How the decision will be evaluated or revisited.

This protects against hindsight bias and makes trade-offs visible. It is not a substitute for design detail or experiments.


---

**Chapter:** [Thinking in Systems](README.md) · **Previous:** [Architecture is a set of consequential decisions](01-architecture-is-a-set-of-consequential-decisions.md) · **Next:** [A useful system boundary diagram](03-a-useful-system-boundary-diagram.md)
