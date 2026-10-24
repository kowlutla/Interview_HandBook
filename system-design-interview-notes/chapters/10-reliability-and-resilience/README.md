# 10. Reliability and Resilience

Reliability is the ability to provide the required behavior over time. Resilience is the ability to continue or recover when components fail. A reliable architecture does not assume failures can be eliminated; it limits their impact and makes recovery predictable.

## 10.1 Timeouts and deadlines

Every remote call should have a bounded wait. A timeout prevents a caller from waiting forever, but it does not prove that the remote operation failed. The operation may have completed while the response was delayed or lost.

A **deadline** is the total time budget for a request. Downstream calls should fit within the remaining budget rather than each receiving a fresh full timeout. Propagate cancellation when the caller no longer needs the result.

## 10.2 Retries, backoff, and jitter

Retry only failures likely to be transient. Use bounded exponential backoff and jitter to avoid synchronized retry waves.

Retries are dangerous when:
- The operation is not idempotent.
- The dependency is already overloaded.
- Multiple layers retry independently, multiplying attempts.
- A retry exceeds the caller's deadline.
- A timeout is mistaken for proof that no side effect occurred.

Set retry budgets and prefer one clearly owned retry policy per operation. State-changing requests need idempotency or reconciliation.

## 10.3 Circuit breakers and bulkheads

A **circuit breaker** temporarily stops calls to a failing dependency after a configured failure pattern, then allows limited probes to test recovery. It can prevent repeated calls from consuming resources, but thresholds and half-open behavior need careful tuning.

A **bulkhead** isolates resources so one workload or dependency cannot consume all threads, connections, or concurrency slots. Separate pools, per-tenant limits, and bounded queues are examples.

Neither technique fixes a broken dependency. They limit cascading failure and should be paired with timeouts, monitoring, and a fallback or clear failure response.

## 10.4 Rate limiting and graceful degradation

Rate limiting protects capacity and fairness by bounding work per identity, tenant, or resource. Common algorithms include token bucket and leaky bucket; fixed and sliding windows are also used.

Graceful degradation preserves the most important behavior when full service is impossible. For example, a product might temporarily disable recommendations while preserving checkout. Define which features are essential and ensure degraded modes do not violate security or data correctness.

## 10.5 Redundancy and failure domains

Redundancy helps only when replicas do not share the same failure cause. Two instances in one failure domain may both be lost to a host, rack, zone, credential, or network problem.

Identify the failure domains that matter and place replicas accordingly. More regions can improve disaster resilience but add cost, replication lag, data residency constraints, and more complex failover.

## 10.6 Recovery and disaster recovery

- **RTO (Recovery Time Objective):** How long recovery may take.
- **RPO (Recovery Point Objective):** How much data loss, measured in time, can be tolerated.

Backups are useful only if they can be restored within the required objectives. Test restoration, failover, and failback; verify dependencies such as keys, configuration, credentials, and DNS. A backup that has never been restored is an assumption, not demonstrated recovery capability.

## 10.7 Common interview questions

### Why are retries sometimes harmful?

They increase load and can duplicate side effects. When a dependency is overloaded, retries may make recovery harder. Use bounded attempts, backoff, jitter, idempotency, and a total deadline.

### What is a circuit breaker?

A mechanism that stops sending normal traffic to a dependency after a configured failure pattern, then tests whether it has recovered. It limits cascading failures but does not replace timeouts or fix the underlying cause.

### What is the difference between RTO and RPO?

RTO is the target time to restore service; RPO is the tolerated amount of data loss. They drive different decisions about failover automation, backups, replication, and recovery testing.

### Does running multiple instances guarantee high availability?

No. Instances may share a database, network, zone, credentials, or configuration that becomes a common failure point. Availability depends on the full request path and independent failure domains, not just replica count.

## Quick revision

- Bound waits with timeouts and end-to-end deadlines.
- Retry transient failures carefully, with backoff, jitter, and idempotency.
- Use circuit breakers and bulkheads to limit cascading failures.
- Define degraded behavior for overload and dependency failures.
- Design redundancy across relevant failure domains.
- Set RTO/RPO and test actual restoration.
