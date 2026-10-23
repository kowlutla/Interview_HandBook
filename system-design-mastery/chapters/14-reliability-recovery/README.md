# 14. Reliability, Recovery, and Service Objectives

## Redundancy is not recovery
Redundancy provides alternative resources when one fails; recovery restores service or data after disruption. A replica can reproduce corrupted writes, a backup can be unusable, and failover can route traffic to a region missing recent data. Reliable systems need failure containment, correct failover, recoverable state and tested procedures.

## Availability, reliability and durability
Availability measures whether a service is usable under a defined criterion. Reliability describes correct operation over time and conditions. Durability concerns persistence of acknowledged committed state. A service can be available while returning stale data, or durable while temporarily unavailable.

For a simple series system with independent required dependencies, end-to-end availability is approximately the product of component availabilities. Three required dependencies at 99.9% each yield 0.999^3 ≈ 99.7003%. Independence is often false, and caching/fallback can change the model, but the calculation shows how synchronous dependencies accumulate risk.

## Resilience mechanisms
- **Timeouts:** bound waiting; do not prove the remote operation failed.
- **Retries:** recover transient faults but can amplify load and duplicate effects.
- **Circuit breakers:** temporarily stop calls to a failing dependency.
- **Bulkheads:** isolate resource pools or workloads.
- **Fallbacks:** provide alternate behavior, which must remain correct and safe.
- **Load shedding:** preserve critical work during overload.
- **Health checks:** guide routing/restart decisions; poor probes can cause flapping or restart storms.

Patterns interact. Aggressive retries plus short timeouts and poorly tuned breakers can cause oscillation or suppress recoverable traffic.

## SLI, SLO, SLA and error budget
An SLI is a measured indicator, such as the fraction of eligible requests that succeed within a latency threshold. An SLO is a target over a defined window. An SLA is an external agreement that may include consequences if targets are missed.

For a 99.9% success SLO over a defined window, the error budget is 0.1% of eligible requests for that window. Request-based budgets depend on traffic volume; time-based availability budgets depend on the downtime definition. Objectives should shape release and reliability decisions, not merely appear on dashboards.

## Recovery objectives
- **RTO:** target time to restore service after disruption.
- **RPO:** acceptable data-loss window expressed in time.

Near-zero RPO may require synchronous remote replication or another durable remote-commit strategy, increasing latency and potentially reducing availability during network problems. Asynchronous replication can acknowledge sooner but may lose recent changes during regional failure depending on the acknowledgment contract.

Backups, replication and failover solve different problems. Replication can copy deletion or corruption; backups provide historical recovery points; failover redirects traffic but does not validate data integrity.

## Zones, regions and disaster recovery
Multiple zones can protect against some localized infrastructure failures. Multiple regions protect against broader outages but add global routing, replication, consistency, failover, cost and operational complexity. Active-active needs explicit ownership and conflict semantics; active-passive still needs tested promotion, data freshness and rollback procedures.

## Chaos engineering and incident learning
A controlled resilience experiment starts with a hypothesis, measurable steady state, bounded blast radius, abort criteria and a way to interpret results. Randomly killing production components without safety constraints is not chaos engineering.

Post-incident reviews should identify contributing conditions and systemic controls, not stop at individual actions. Track detection time, mitigation time, customer impact, recovery correctness and follow-up effectiveness.


## 14.1A Reliability is an end-to-end property

A service can be locally reliable while the user journey is unreliable. If a synchronous request requires several independent dependencies, each dependency adds a possible failure point. For a simple series model with availability values A1 through An, end-to-end availability is approximately the product of those values. This approximation assumes independence and that every dependency is required.

Fallbacks, caches, replicas and alternate paths can change the model, but only if they work under the same failure and load conditions. A fallback that calls the same failing dependency is not a real alternate path. A cache fallback may preserve reads but not writes, so the degraded contract must be explicit.

## 14.1B Timeouts, retries, circuit breakers, and bulkheads

A timeout bounds waiting. It should fit inside an end-to-end deadline and account for connection acquisition, remote processing, and cleanup. A timeout that is too short can reject healthy but slow work; one that is too long can retain resources and increase queueing.

Retries are useful for transient failures only when the operation is safe to repeat. Use bounded attempts, exponential backoff, jitter, deadlines, and retry budgets. Retrying a non-idempotent write after an uncertain timeout can duplicate effects.

A circuit breaker tracks failures or slow calls and temporarily prevents new calls to a dependency. Common states are closed, open and half-open, but thresholds and behavior vary by implementation. A breaker can prevent resource waste; it cannot repair the dependency or determine whether a timed-out write committed.

Bulkheads isolate resource pools or workload classes so one failing dependency or tenant cannot consume every worker, connection, or queue slot. Isolation needs capacity planning: overly small pools can reject useful work, while shared downstream dependencies can still be overwhelmed.

## 14.1C Graceful degradation and criticality

Define which capabilities are essential and which can be reduced during an incident. A commerce system might preserve checkout and order status while temporarily disabling recommendations or expensive personalization. Degradation should be deliberate, visible where appropriate, and safe for business invariants.

Prioritization requires bounded queues and resource reservations. If optional background work can consume all database connections, the critical path is not actually protected. Separate concurrency limits, priorities, quotas and dependency budgets can help.

Fallback data must be safe for the operation. Serving a stale public product description may be acceptable; serving stale authorization or inventory data can create security or correctness failures. Each fallback needs a freshness and correctness contract.

## 14.1D Redundancy, replication, backup, and restore

These mechanisms protect against different failures:
- Redundancy provides alternate capacity.
- Replication maintains copies, often for availability or data-loss reduction.
- Backups preserve recoverable historical state.
- Point-in-time recovery reconstructs state to a chosen time using base backups and logs where supported.
- Integrity checks detect corruption.
- Restore exercises prove that the recovery procedure works.

Replication can immediately propagate accidental deletion or corrupted writes. A backup can be useless if it shares the compromised credentials or failure domain. Protect backup credentials separately, test restoration regularly, and verify application-level invariants after recovery.

## 14.1E Recovery objectives and runbooks

RTO and RPO must be attached to a defined scenario and scope. “Recover within one hour” should specify whether that means the first health response, core writes restored, all regions restored, or the entire backlog drained. RPO should state which writes count as acknowledged and what data loss is acceptable.

A recovery runbook should define:
- Trigger and decision authority.
- Preconditions and safety checks.
- Steps to promote, restore or redirect.
- How to prevent old writers from returning.
- How to validate data freshness and integrity.
- How to handle in-flight or uncertain operations.
- Communication and escalation.
- Rollback or failback criteria.
- Evidence that recovery is complete.

Runbooks should be exercised under realistic constraints. A procedure that depends on one unavailable administrator, expired credentials, or undocumented manual knowledge is a reliability risk.

## 14.1F Incident response and learning

During an incident, separate detection, diagnosis, mitigation, recovery and prevention. Mitigation reduces current harm; root-cause analysis explains contributing conditions; prevention changes the system so the same class of failure is less likely or less damaging.

Useful measures include time to detect, time to mitigate, time to recover, affected users/operations, data integrity impact, and follow-up completion. Avoid treating mean time metrics as complete summaries: distributions and severe outliers matter.

A blameless review does not mean no accountability. It means understanding why actions appeared reasonable given the information and controls available, then improving detection, guardrails, architecture and procedures.

## 14.1G Chaos experiments and game days

A safe experiment defines a hypothesis, expected steady state, target failure, scope, monitoring, abort conditions, and recovery plan. Begin in a controlled environment and expand blast radius only when evidence supports it. Test dependency latency, connection exhaustion, zone loss, process restart, stale credentials, backup restore, and failover where appropriate.

A successful experiment is not simply “the service stayed up.” It should verify correctness, error budgets, recovery objectives, and whether alerts and runbooks led to the expected response. Experiments should not create uncontrolled risk for customers.


## Further reading
- Google [Site Reliability Engineering book](https://sre.google/sre-book/table-of-contents/).
- Google [SRE Workbook: Error Budget Policy](https://sre.google/workbook/error-budget-policy/).
- AWS [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html).


## Recovery is a chain, not a single failover switch

```mermaid
flowchart TD
  A[Detect incident] --> B[Contain blast radius]
  B --> C[Fail over or restore]
  C --> D[Validate data and service correctness]
  D --> E{Objectives met?}
  E -- No --> F[Continue recovery and communicate impact]
  F --> D
  E -- Yes --> G[Monitor stability]
  G --> H[Review and prevent recurrence]
```

A service is not recovered merely because a health endpoint turns green. Verify that data is sufficiently current, critical operations work, dependencies are healthy, and the system can sustain expected traffic.


---

[Back to textbook contents](../../README.md) · [Curriculum](../../CURRICULUM.md) · [Roadmap](../../ROADMAP.md)
