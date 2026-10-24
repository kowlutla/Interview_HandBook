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

## Client-side, offline-first, and real-time systems

For client-facing systems, distinguish authoritative server state, client-local state, cached/replicated state, and pending operations. Do not equate optimistic presentation with commit, transport delivery with durable processing, or browser storage with unconditional durability. State retry identity, synchronization checkpoints, conflict/deletion policy, cursor expiry and resynchronization behavior. For persistent connections and WebRTC, define reconnect/replay, ordering, backpressure, authorization revocation, privacy metadata, and relay/media-server trust boundaries. Treat implementation and browser behavior as version/platform dependent where appropriate.

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


## Human-written, readable teaching style

The textbook should read like an experienced engineer patiently explaining a difficult idea to another engineer—not like generated documentation, a compliance checklist, or a collection of search-result summaries.

- Begin each section with the central idea in plain language. Explain why the reader should care before introducing terminology.
- Prefer connected prose that develops one thought at a time. Use bullets for genuinely parallel items, steps, or concise checklists—not as the default form for every explanation.
- Use natural transitions to show how one idea leads to the next. Vary sentence structure and paragraph length; avoid repetitive “Definition / Benefits / Drawbacks / Use cases” templates when they make the writing mechanical.
- Explain technical terms when they first become necessary. Do not stack several unexplained terms in one sentence.
- Use one purposeful example to make an abstract mechanism concrete. Walk through what happens and why; do not add examples merely to increase length.
- Use tables only when comparison is easier to understand side by side. Keep table cells short and explain the important conclusion in prose nearby.
- Avoid repeating the same idea in an introduction, a detailed section, a checklist, and a summary. A short signpost may preview a later section, but it should not teach the same material twice.
- Keep checklists at the end of a major decision or review process, not after every small subsection. Remove checklist items that merely restate the headings.
- Avoid inflated phrasing, generic filler, artificial enthusiasm, and overuse of bold text. Be precise and approachable rather than chatty.
- Do not simplify away important nuance. If a guarantee depends on a protocol, database engine, provider, or configuration, explain that dependency in plain language.
- Keep the main learning path focused. Move specialist details to a clearly labeled optional note or appendix when they interrupt the core explanation.

### Readability review questions

When revising a chapter, ask:
1. Could a reader explain the idea after reading the section once?
2. Does each paragraph move the explanation forward?
3. Is the reason behind the mechanism clear, not just the terminology?
4. Could a repeated table, list, heading, or checklist be removed without losing understanding?
5. Does the chapter feel like one coherent explanation rather than several notes stitched together?
6. Is the depth justified by the concept's importance to HLD fundamentals?
