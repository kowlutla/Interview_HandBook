# Editorial Standard

## The target reader

A software engineer preparing for HLD/System Design interviews who needs to understand the reasoning behind architectural choices and revise efficiently.

## Required writing style

- Use clear, direct English and explain unfamiliar terms on first use.
- Prefer a short explanation plus a concrete example over a long list of facts.
- Explain **why** a design choice works, not only what it is called.
- Keep paragraphs focused; use tables to compare real alternatives, not to fragment prose.
- Use diagrams where they explain a decision, request/data flow, state transition, or failure path; make arrows, actors, and data flow unambiguous.
- Use Mermaid with concise labels. Read the prose and diagram together to check that the ordering and guarantees agree.
- Include enough detail to understand mechanisms and trade-offs; avoid academic digressions and implementation trivia unless they change a design decision.
- Distinguish universal principles from technology-specific behavior.
- State assumptions in calculations and examples.

## Standard topic template

Use only sections that genuinely help for the topic:

1. **What is it?**
2. **Why is it needed?**
3. **How does it work?**
4. **When should you use it?**
5. **Trade-offs and failure modes**
6. **Example**
7. **Interview questions and answers**
8. **Quick revision**

Do not force all sections onto small concepts. Do not repeat the definition under multiple headings.

## Interview answer quality

Answers should:
- Start with the direct answer.
- Explain the mechanism or reasoning.
- Mention the most relevant trade-off or limitation.
- Add an example when it makes the answer clearer.
- Avoid unsupported absolutes such as “always,” “never,” or “guarantees” unless technically justified.

## Length discipline

- Keep a typical concept to a few focused paragraphs or a compact comparison table.
- Let foundational topics such as consistency or partitioning be longer when needed for real understanding.
- Remove repeated examples, redundant summaries, and edge cases that do not materially affect an architectural decision.
- Keep a chapter's quick revision genuinely short.
- Do not add a section merely to increase completeness metrics.

## Quality checklist

- [ ] The problem being solved is clear.
- [ ] The mechanism is explained accurately.
- [ ] Selection guidance and trade-offs are concrete.
- [ ] Important failure modes are included.
- [ ] Interview answers are understandable without reading another long section.
- [ ] No substantial duplication with other chapters.
- [ ] Relative Markdown links resolve against the current repository tree.
- [ ] Mermaid syntax is rendered and visually inspected when a renderer is available; manual inspection must not be reported as rendered validation.
