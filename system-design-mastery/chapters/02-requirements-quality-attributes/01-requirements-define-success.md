# Lesson 02.01 — Requirements define success

## 2.1 Requirements define success

A functional requirement states what the system must do: create an order, retrieve a profile, or publish a notification. A non-functional requirement (NFR) describes a property of that behavior, such as latency, availability, privacy, durability, or accessibility. The distinction is useful but not absolute: “a user can export data within 30 seconds” combines a function and a performance target.

Requirements should be testable. “Fast” is not testable until the operation, workload, percentile, and measurement boundary are stated. “Highly available” needs a success definition and time window. “Secure” needs assets, threats, trust boundaries, and controls.


## 2.2 Define scope and assumptions

Write down:
- Users, clients, and important workflows.
- In-scope and explicitly out-of-scope behavior.
- Data created, read, updated, deleted, retained, and exported.
- Expected traffic, burstiness, geography, and growth.
- Compliance, budget, team, technology, and migration constraints.
- Dependencies and the behavior expected when each is unavailable.

An assumption is not a fact. Record it with a validation path. If an assumption strongly affects the architecture, model alternative values instead of silently committing to one.


---

**Chapter:** [Requirements and Quality Attributes](README.md) · **Next:** [Quality attributes need operational definitions](02-quality-attributes-need-operational-definitions.md)
