# 17. Observability and Operating Production Systems

## Signals and their roles
- **Logs** record discrete events with context.
- **Metrics** aggregate numeric measurements over time.
- **Traces** connect spans across a request or workflow.

Structured logs make fields queryable. Correlation and trace IDs help connect events, but IDs should not contain secrets or unbounded user data. Context propagation must cross asynchronous boundaries and be handled safely at trust boundaries.

## RED and USE
RED focuses on Rate, Errors and Duration for request-driven services. USE focuses on Utilization, Saturation and Errors for resources. They are complementary heuristics, not complete observability strategies. A service may show normal CPU but be saturated on a connection pool or blocked on a remote dependency.

## Percentiles and cardinality
Latency percentiles describe distributions; averages can conceal slow requests. Histograms or equivalent aggregations are needed to estimate quantiles meaningfully across instances. Aggregating per-instance p99 values by taking their arithmetic mean is generally not the fleet-wide p99.

Metric cardinality grows when labels have many possible values. User IDs, request IDs and arbitrary URLs can make metrics expensive and noisy; put high-cardinality details in traces or logs when appropriate, with privacy controls.

## SLO-driven alerting
An SLI should represent user-visible success, such as successful eligible requests within a latency target. An SLO sets a target over a window. Error-budget burn rates can alert when a service consumes its allowed failure budget too quickly. Alert on actionable symptoms and user impact rather than every internal anomaly.

## Tracing and diagnosis
Distributed traces reveal the time spent in application spans and dependencies, but sampling can omit rare failures and clock differences complicate cross-host timing. Instrument retries and queue wait separately from service time. A span's duration is not necessarily CPU time.

A practical investigation flow:
1. Confirm user impact and affected scope.
2. Check error rate, latency percentiles and traffic changes.
3. Compare dependency and resource saturation signals.
4. Trace representative slow or failed requests.
5. Form a hypothesis and test it against evidence.
6. Mitigate safely, then verify recovery.
7. Preserve evidence and track corrective actions.

## Production readiness
A production-ready service needs ownership, dashboards, alerts, runbooks, capacity assumptions, deployment/rollback plans, security review, backup and restore evidence, dependency budgets and incident escalation. Operational readiness is not just a final checklist; it influences architecture.


## 17.1A Instrumentation boundaries and context propagation

Observability data should preserve enough context to connect an external request to its internal work without turning identifiers into high-cardinality metric labels. A trace context can flow through HTTP headers, message metadata, and asynchronous task boundaries. At trust boundaries, validate or replace untrusted context rather than blindly accepting arbitrary baggage.

A trace ID correlates work; it is not an authentication credential. Do not use trace context to make authorization decisions. Background jobs and message consumers should link their processing to the originating operation where appropriate, while also representing long delays and retries accurately.

## 17.1B Metrics: counters, gauges, histograms, and cardinality

- **Counter:** monotonically increasing event total, such as requests or failures.
- **Gauge:** current value that can rise or fall, such as queue depth or active connections.
- **Histogram:** observations bucketed by value, useful for latency and size distributions.
- **Summary:** a metric type that may calculate quantiles locally; aggregation behavior depends on the implementation.

Use counters for rates after calculating deltas over time; do not interpret a process-reset counter as a negative event. Gauges require clear semantics about when they are sampled. Histograms should have buckets appropriate to the target thresholds, and fleet-wide quantiles should be calculated from aggregatable distribution data rather than averaging instance p99 values.

Cardinality multiplies across labels. A metric with labels for tenant, user, URL, and request ID can create an unbounded series count. Keep labels bounded and use logs or traces for high-cardinality details with access and privacy controls.

## 17.1C Histograms, percentiles, and tail interpretation

Percentiles depend on sample size, aggregation, time window, and bucket resolution. A p99 over ten requests is a weak indicator of rare tail behavior. Aggregating per-instance quantiles by arithmetic mean does not produce the fleet quantile. Use histograms or a suitable mergeable distribution.

Latency should be measured at meaningful boundaries: client-visible end-to-end duration, service handler duration, queue wait, connection acquisition, and dependency duration answer different questions. Instrument retries separately so a successful final response does not conceal repeated failed attempts or excessive work.

## 17.1D Logs and traces are evidence with limitations

Structured logs should include stable event names and useful fields such as operation, result, dependency, duration, and correlation identifiers. Avoid logging secrets, full tokens, and unnecessary personal data. Sampling, buffering, and dropped telemetry mean absence of a log line is not proof that an event did not occur.

A trace shows spans and causal relationships as instrumented, but instrumentation gaps, sampling, asynchronous work, and clock differences can complicate interpretation. A long span may include waiting rather than CPU execution. Correlate traces with resource metrics and application-level state transitions.

## 17.1E SLOs, alerting, and burn rate

An SLI needs an explicit good-event definition and eligible-event denominator. An SLO needs a target and window. Alerting should focus on user impact or rapid loss of error budget rather than every threshold crossing.

A burn rate compares the observed error rate with the allowed error rate implied by the SLO. Multi-window alerting can detect both fast severe incidents and slower sustained degradation. The right windows depend on traffic volume, service criticality, and response expectations; avoid alerts so sensitive that routine variation pages the team constantly.

A dashboard is not an alerting strategy. Each page should have an owner, an actionable next step, and enough context to assess impact. Alerts without a response path create noise rather than reliability.

## 17.1F Capacity and saturation observability

Monitor the constrained resource, not only CPU. Useful signals include queue depth and age, worker utilization, thread-pool rejection, connection acquisition latency, database lock waits, cache miss load, consumer lag, disk latency, network retransmissions, and rate-limit rejection.

A growing queue can indicate the system is accepting more work than it can complete. Queue depth alone is insufficient if arrival rate is low; queue age and drain rate provide context. A system may have low CPU while waiting on exhausted connections or a slow dependency.

## 17.1G Incident diagnosis and runbooks

A practical incident sequence is:
1. Establish customer impact, scope, and start time.
2. Check traffic, success rate, latency percentiles, and saturation.
3. Identify the first failing or slowing dependency in traces and logs.
4. Compare current behavior with a known baseline and recent changes.
5. Form a falsifiable hypothesis and test it with evidence.
6. Mitigate using a reversible, bounded action where possible.
7. Verify customer-facing recovery and data correctness.
8. Preserve evidence, communicate status, and track follow-up work.

Runbooks should state symptoms, safe checks, mitigation steps, expected signals, abort conditions, escalation paths, and verification criteria. Avoid blindly restarting components when doing so may destroy evidence, worsen a thundering herd, or interrupt recovery.

## 17.1H Operational readiness checklist

- Service owner and escalation path are known.
- SLIs/SLOs and error-budget policy are defined.
- Dashboards show user impact and constrained resources.
- Alerts are actionable and tested.
- Traces and logs carry safe correlation context.
- Capacity and dependency limits are documented.
- Rollout and rollback steps are rehearsed.
- Backup restore and disaster recovery have evidence.
- Secrets and access are controlled.
- Runbooks define verification and safe abort conditions.



## 17.1I RED and USE methods: choose signals by component

The **RED method** is useful for request-driven services:
- **Rate:** requests or operations per unit time.
- **Errors:** failed or incorrect requests under a defined denominator.
- **Duration:** latency distribution, usually including tail percentiles.

The **USE method** is useful for resources:
- **Utilization:** how busy the resource is.
- **Saturation:** queued or delayed work beyond immediate service capacity.
- **Errors:** resource-level errors, such as device or connection failures.

These methods complement rather than replace domain-specific indicators. A database may need lock waits, query duration, connection acquisition latency and replication lag. A message consumer may need lag age, processing rate and retry rate. A user journey may need a business success rate that cannot be inferred from HTTP status alone.

Avoid dashboards that show only averages. Pair rates with p95/p99 duration, queue depth and queue age, and annotate deployments or configuration changes. Use bounded metric labels for service, route template, status class and dependency; put high-cardinality identifiers in controlled logs or traces instead.



## 17.2 Observability in practice: from symptom to cause

Observability is the ability to infer system behavior from emitted evidence. Logs, metrics and traces are complementary views, not interchangeable storage formats. A dashboard can show that latency rose; traces may reveal which dependency consumed time; structured logs may explain a particular rejected operation. None guarantees that the system emitted enough context or that sampling retained the relevant event.

### Metrics: dimensions, cardinality and histograms

A metric time series is identified by its metric name and label set. Labels such as route template, status class, service and region are usually bounded. User IDs, request IDs, raw URLs, search terms and arbitrary tenant names can create unbounded cardinality, increasing memory, storage, query cost and alert complexity. Put per-request identifiers in logs or traces where access and retention can be controlled.

Counters measure cumulative events; gauges represent current values; histograms capture distributions or buckets of observations. Averages hide tail behavior and can improve while a small fraction of requests become catastrophically slow. Percentiles must be calculated with a method appropriate to the telemetry system; averaging per-instance p99 values does not generally yield the fleet-wide p99.

### RED and USE are starting frameworks

RED focuses on request-driven services: rate, errors and duration. USE focuses on resources: utilization, saturation and errors. Neither is a complete dashboard. Add domain success rates, queue age, retry volume, connection acquisition latency, cache freshness, replication lag and dependency-specific signals where they explain the user journey.

A high CPU percentage is not itself an incident; a growing queue, rising tail latency and falling successful throughput may show that CPU is the constrained resource. Interpret signals together and compare them to a known baseline and service objective.

### Distributed tracing and context propagation

A trace connects spans across a request path. Context propagation must survive HTTP/RPC calls, message headers, async task boundaries and scheduled work. If a consumer starts a new trace without linking the producer context, the causal chain is lost. Sampling reduces cost but may discard rare failures; tail-based sampling or targeted error retention can help when supported and appropriately bounded.

Tracing can add overhead and can expose sensitive attributes if instrumentation is careless. Do not place secrets, raw tokens or unnecessary personal data in span attributes. A trace ID is correlation metadata, not an authentication credential.

### Alerting on user impact and error-budget burn

An alert should prompt a defined action. Page on conditions that require immediate human intervention; route lower urgency issues to tickets or dashboards. Avoid paging on every transient internal error when user-visible SLOs remain healthy, but ensure that a fast-burn outage is detected before the budget is exhausted.

A multi-window, multi-burn-rate approach compares recent error-budget consumption over different windows to balance fast detection with noise. Exact thresholds depend on the SLO period, service criticality and response process. Alert on symptoms first, then use component signals for diagnosis.

### Incident diagnosis as hypothesis testing

Start with impact and timeline: which user journeys, regions, tenants or operations are affected, and when did the change begin? Compare recent deployments, configuration changes, traffic shifts, dependency health, saturation, error rates and queue age. Form hypotheses, choose a signal that can falsify each hypothesis, and avoid changing many variables at once.

During mitigation, prefer reversible changes that reduce impact: rollback a bad release, disable a risky feature, shed optional work, or route around a proven failure. Verify that the user-visible SLI recovers and that the mitigation did not violate data correctness. A green process health check is not sufficient evidence of recovery.

### Runbooks and postmortems

A useful runbook includes symptoms, scope, diagnostic commands or dashboards, safe mitigations, escalation contacts, rollback criteria, and verification steps. Keep it versioned with the service and test it during exercises. A postmortem should document impact, contributing conditions, detection gaps, response timeline and follow-up actions without blaming individuals.

Actions should change the system or its operating environment: add a guardrail, improve capacity, make a dangerous state unrepresentable, add a missing signal, automate a safe recovery step, or clarify ownership. “Be more careful” is not a reliable corrective action.

### Observability checklist

- Can user-visible success, latency and availability be measured?
- Are labels bounded and sensitive data excluded?
- Do metrics expose saturation, queue age and tail latency?
- Does trace context survive async boundaries and messages?
- Is sampling appropriate for rare failures?
- Are alerts tied to actionable user impact or error-budget burn?
- Can on-call staff identify recent deployments and configuration changes?
- Are runbooks executable and recovery steps verified?
- Do postmortems produce measurable engineering changes?
- Is telemetry itself bounded, available and protected?


## Further reading
- [OpenTelemetry documentation](https://opentelemetry.io/docs/).
- Google [Site Reliability Engineering book](https://sre.google/sre-book/table-of-contents/).


## Observability is a feedback loop

```mermaid
flowchart TD
  A[Instrument requests and dependencies] --> B[Collect metrics, logs, and traces]
  B --> C[Compare user-visible SLIs with SLOs]
  C --> D{Impact or error-budget burn?}
  D -- Yes --> E[Alert and investigate]
  E --> F[Mitigate and verify recovery]
  F --> G[Learn and update design or runbook]
  G --> A
  D -- No --> H[Continue trend and capacity analysis]
  H --> A
```

Metrics reveal patterns, logs add event context, and traces connect work across services. None is sufficient alone for every incident; correlation and low-cardinality labels matter.


---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
