# 3. APIs and System Boundaries

APIs define how components communicate. Service boundaries define which component owns a responsibility and its data. Good boundaries make systems easier to evolve; poor boundaries create tight coupling, duplicated logic, and fragile deployments.

## 3.1 Define responsibilities before services

Start by identifying the main capabilities and the data they own. Split a component when there is a meaningful reason—such as a separate scaling profile, security boundary, ownership, or independent lifecycle—not simply because the diagram looks more distributed.

A modular monolith can be a good starting point. Microservices add network calls, deployment coordination, observability needs, and partial failures. They are useful when their independent ownership and scaling benefits outweigh that complexity.

## 3.2 Design a clear API contract

An API contract should make clear:
- The operation and resource being addressed.
- Required inputs and validation rules.
- Success response and error behavior.
- Authentication and authorization requirements.
- Pagination, filtering, and sorting behavior where needed.
- Idempotency expectations for operations that may be retried.
- Compatibility expectations as the API evolves.

For HTTP APIs, use methods and status codes consistently. For example, a request to create an order should make clear whether it creates a new order on every call or can safely be retried with an idempotency key.

## 3.3 Synchronous versus asynchronous communication

**Synchronous request/response** is appropriate when the caller needs an immediate result and the dependency's latency and availability fit the request budget.

**Asynchronous messaging** is useful when work can finish later, bursts need buffering, consumers should be decoupled, or the caller should not wait for the whole workflow.

Asynchronous processing adds complexity: the caller may need a status resource, eventual completion notification, retries, deduplication, and a way to inspect or recover failed work.

Do not use a queue merely to make a diagram more scalable. Use one when its buffering or decoupling benefits solve a real requirement.

## 3.4 Keep remote calls within a latency budget

Every network hop adds latency and a possible failure point. A chain of dependent calls can be slower and less available than its individual services suggest.

For a request path:
- Set a deadline or timeout appropriate to the caller's total latency budget.
- Avoid unbounded fan-out.
- Propagate cancellation when work is no longer needed.
- Define behavior when a dependency is slow or unavailable.
- Do not retry every failure automatically; retries can amplify overload.

A timeout does not prove that the remote operation failed. The server may have completed the operation while the response was lost. For state-changing calls, use idempotency or reconciliation where appropriate.

## 3.5 API and boundary trade-offs

| Choice | Useful when | Main cost or risk |
|---|---|---|
| Modular monolith | One team or product can share deployment and scaling | Less independent deployment and scaling |
| Microservices | Clear ownership, independent evolution, or different scaling needs | Network failures, distributed data, operational overhead |
| Synchronous call | Immediate result is required | Caller depends on downstream latency and availability |
| Asynchronous message | Work can finish later or needs buffering | Eventual completion, duplicate delivery, and harder debugging |
| Coarse-grained API | One operation can satisfy a use case efficiently | May return data the caller does not need |
| Fine-grained API | Reusable operations and independent control matter | More round trips and orchestration |

## 3.6 Common interview questions

### When should you split a monolith into microservices?

Split when there is a clear benefit such as independent ownership, release cadence, scaling, or fault isolation. First check whether modular boundaries inside a single deployment would solve the problem. Microservices are not automatically more scalable or reliable.

### When should a request use a queue?

Use a queue when the caller does not need the full work result immediately, when bursts should be buffered, or when producers and consumers need decoupling. Keep synchronous processing for operations where immediate confirmation is required and the work fits the latency budget.

### Why are retries dangerous for state-changing APIs?

A timeout can occur after the server has performed the operation. Retrying a non-idempotent request may create duplicate effects. Use an idempotency key or another deduplication mechanism, define its scope and retention, and handle retries that occur after the deduplication window.

### What makes an API backward-compatible?

Existing clients should continue to work under the new contract. Additive optional fields are often safer than removing or changing existing fields, but compatibility depends on client behavior, validation rules, and serialization. Changes should be evaluated against actual consumers and tested with contract checks where appropriate.

## Quick revision

- Define ownership before splitting services.
- Prefer the simplest boundary that supports the requirements.
- Use synchronous calls for immediate results; asynchronous messaging for decoupling or buffering.
- Budget latency across the whole request path.
- A timeout does not prove a write failed.
- Make retries safe through idempotency or deduplication.

## Scenario practice

**Scenario:** A checkout API calls inventory, pricing, promotions, payment, and email services synchronously. Its p99 latency rises and one slow dependency causes broad failures. How would you reshape the flow?

**Reasoning:** Keep synchronous calls only where the user needs an immediate decision, bound each call by a propagated deadline, and isolate optional work. Email and other post-commit side effects are good asynchronous candidates. Use an explicit checkout state machine for long-running work; do not turn payment or inventory correctness into fire-and-forget tasks. Reduce unnecessary network hops before splitting more services.

## Interview questions

### Q1. When is a modular monolith better than microservices?
When one team can own the domain and a shared deployment does not block independent scaling or release needs. A modular monolith keeps in-process calls and local transactions simpler. Extract a service when a clear boundary, ownership need, scaling profile, or isolation requirement justifies network and operational complexity.

### Q2. When should an API operation be asynchronous?
When the work may take longer than a request budget, can finish later, or benefits from durable buffering/replay. Return a durable operation or resource identifier and expose status. Do not acknowledge work as accepted until the system has safely recorded enough state to recover it.

## Further reading

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — HTTP method and response semantics.
- [Google API Design Guide](https://cloud.google.com/apis/design) — API resource and compatibility guidance.

