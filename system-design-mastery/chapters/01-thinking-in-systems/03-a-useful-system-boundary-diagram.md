# Lesson 01.03 — A useful system boundary diagram

## 1.6 A useful system boundary diagram

~~~mermaid
flowchart LR
  U[Users and external clients] --> E[System boundary]
  E --> A[Application capabilities]
  A --> D[Owned data]
  A --> X[External dependencies]
  O[Operations and security] -. governs .-> E
  O -. observes .-> A
  O -. protects .-> D
~~~

The dotted relationships matter: security, observability, deployment, and operational ownership cross component boundaries rather than living in a single box.


## 1.7 Common errors

- Designing a solution before identifying the problem.
- Treating every quality attribute as equally important.
- Assuming a network call behaves like a local function call.
- Equating more services with better modularity.
- Hiding uncertainty behind precise-looking estimates.
- Describing only the happy path.
- Treating a diagram as evidence that an architecture is correct.


## Further reading
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework) — practitioner guidance for architecture quality.
- [Microsoft Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/) — patterns and their contexts.
- [Martin Fowler on microservices](https://martinfowler.com/articles/microservices.html) — trade-offs and organizational implications.


---

**Chapter:** [Thinking in Systems](README.md) · **Previous:** [Decompose by responsibility and change](02-decompose-by-responsibility-and-change.md)
