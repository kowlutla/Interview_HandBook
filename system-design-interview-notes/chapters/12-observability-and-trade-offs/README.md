# 12. Observability and Design Trade-offs

Observability helps teams understand what a system is doing from its outputs. Design trade-off analysis helps explain why an architecture is appropriate for its requirements. Both are essential: a design should be measurable in production and defensible before it is built.

## 12.1 Logs, metrics, and traces

- **Logs** describe individual events and often provide detailed diagnostic context.
- **Metrics** aggregate measurements over time, such as request rate, error rate, latency, queue depth, and resource utilization.
- **Distributed traces** connect spans across a request path to show where time was spent and which dependencies were called.

Use correlation or trace identifiers to connect relevant signals. Avoid putting high-cardinality values such as arbitrary user IDs into every metric label; this can make monitoring expensive and hard to operate. Sensitive values should not be copied into logs or traces without a clear need and appropriate controls.

## 12.2 The four golden signals

A practical starting point for service monitoring is:
- **Latency:** How long requests take, including tail percentiles.
- **Traffic:** How much demand the system receives.
- **Errors:** Failed or incorrect outcomes, including relevant timeouts.
- **Saturation:** How close resources are to their effective limits.

Averages can hide poor experiences for a minority of users. Percentiles such as p95 or p99 can help reveal tail latency, but interpret them alongside request volume and the service's actual objective.

## 12.3 SLIs, SLOs, and error budgets

- **SLI (Service Level Indicator):** A measured property, such as the fraction of eligible requests that succeed within a latency target.
- **SLO (Service Level Objective):** The target for that indicator over a defined window.
- **SLA (Service Level Agreement):** A formal commitment, often with consequences if it is missed.

An error budget is the tolerated unreliability implied by an SLO. For a 99.9% success target over a suitable request population, the allowed failure fraction is 0.1%. The exact budget depends on the SLI definition and measurement window.

SLOs should represent user experience, not merely an infrastructure metric. A server can be “up” while requests fail or become too slow.

## 12.4 A repeatable trade-off framework

When comparing designs, state:
1. **Requirement:** What must the system achieve?
2. **Options:** Which plausible approaches meet the basic need?
3. **Benefits:** What does each option improve?
4. **Costs and risks:** What becomes slower, less available, harder to operate, or more expensive?
5. **Failure behavior:** What happens when a component or dependency fails?
6. **Decision and assumptions:** Why is one option best under current constraints?
7. **Revisit trigger:** What measurement or change would justify a different choice?

For example, a read replica may improve read capacity but introduce lag. If a use case requires read-your-writes, route those reads appropriately or choose a stronger mechanism. The right answer depends on the user-visible guarantee, not on a generic preference for replicas.

## 12.5 Common interview questions

### What is the difference between logs, metrics, and traces?

Logs capture individual events, metrics show aggregated behavior over time, and traces show how a request flows through components. They complement one another: metrics often detect an issue, traces locate a slow or failing dependency, and logs provide event details.

### Why monitor tail latency?

An average can look healthy while a meaningful fraction of users experience very slow requests. Tail percentiles help expose queueing, uneven load, garbage collection, or slow dependencies. They should be interpreted with traffic volume and the SLO.

### How do you choose between two architectures?

Compare each against the stated requirements and assumptions. Explain the important gains, costs, failure modes, and operational burden. A good decision includes a reason to revisit it, such as traffic growth, stricter consistency needs, or measured saturation.

### What is an error budget used for?

It expresses how much unreliability is acceptable under an SLO. Teams can use it to balance feature delivery and reliability work, investigate repeated incidents, and decide when risky changes should slow down. It is meaningful only if the SLI reflects real user outcomes.

## Quick revision

- Logs explain events; metrics reveal trends; traces connect request paths.
- Monitor latency, traffic, errors, and saturation.
- Define user-centered SLIs and realistic SLOs.
- Compare designs using requirements, benefits, costs, failure modes, and assumptions.
- State what evidence would cause you to revisit an architectural choice.
