# Lesson 01.01 — Architecture is a set of consequential decisions

## 1.1 Architecture is a set of consequential decisions

A software system is a collection of interacting parts that transforms inputs into outcomes under constraints. Architecture describes the important structures and decisions that shape those interactions: component boundaries, responsibilities, communication paths, state ownership, deployment units, failure domains, and rules that allow the system to evolve.

A diagram is one representation of architecture, not the architecture itself. Two diagrams can look identical while differing radically in consistency guarantees, retry behavior, security boundaries, data ownership, or recovery behavior. Those properties often determine whether the system works in production.

**System design** is the reasoning process used to choose a system structure that satisfies requirements within constraints. **High-Level Design (HLD)** focuses on major components, their responsibilities, interfaces, data flows, and deployment relationships. **Low-Level Design (LLD)** focuses on internal class/module structures, algorithms, schemas, and detailed implementation. The boundary is contextual: a database schema may be low-level for one discussion but central to HLD when it determines partitioning or consistency.


## 1.2 Start with the problem, not a technology

A reliable reasoning sequence is:

1. State the user or business outcome.
2. Define scope and explicit exclusions.
3. Identify functional behavior and quality attributes.
4. Describe workload shape and important data.
5. Identify constraints and assumptions.
6. Compare viable structures and their trade-offs.
7. Specify failure behavior and operational ownership.
8. Validate with measurements, experiments, and review.

Choosing a database, broker, cloud, or microservice boundary before clarifying access patterns and correctness needs reverses this order. Technology can make some choices easier, but it cannot rescue a misunderstood requirement.


---

**Chapter:** [Thinking in Systems](README.md) · **Next:** [Decompose by responsibility and change](02-decompose-by-responsibility-and-change.md)
