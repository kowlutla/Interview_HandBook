# Editorial and Verification Standard

## Teach mechanisms, not vocabulary lists
Explain why a concept exists, the problem it addresses, how it works, what it guarantees, what it does not guarantee, when it is useful, alternatives, failure modes, and connections to other chapters. Introduce jargon before relying on it. Avoid forcing every chapter into identical headings.

## Evidence and claim types
Distinguish:
- **Formal guarantee:** supported by a standard, proof, or primary research.
- **Implementation behavior:** tied to a named product and version/documentation.
- **Operational guidance:** a recommendation dependent on workload and organizational context.
- **Illustrative assumption:** introduced for a worked example, not a sourced benchmark.
- **Estimate:** approximate result whose assumptions and uncertainty are explicit.

Cite primary references close to the claim. Do not invent source details or benchmarks. When sources differ, explain whether they use different models, versions, workloads, or definitions.

## Quantitative examples
Show the model, assumptions, units, arithmetic, result, and sanity check. Keep bits and bytes distinct. Label averages, percentiles, peaks and time windows. Do not imply that an estimate replaces measurement.

## Distributed systems
Name the fault model and timing assumptions. Separate safety (nothing forbidden happens) from liveness (something good eventually happens). State what a client can observe. Explain the boundary of guarantees, especially for partitions, retries, clocks, quorum operations and exactly-once claims.

## Diagrams
Use Mermaid when it clarifies relationships, sequence, state or failure. Keep nodes and edges readable, explain what the diagram shows, and do not treat a diagram as proof of correctness.

## Scope
Focused examples are encouraged. Complete end-to-end system architectures and interview question collections are excluded from this phase.

## Review checklist
- [ ] Is the problem being solved clear?
- [ ] Are terms defined and used consistently?
- [ ] Are prerequisites explained or linked?
- [ ] Are claims supported and appropriately qualified?
- [ ] Are examples technically correct and useful?
- [ ] Are failure modes and trade-offs explicit?
- [ ] Are diagrams valid and explained?
- [ ] Are internal links correct?
- [ ] Is there duplication that should be consolidated?
