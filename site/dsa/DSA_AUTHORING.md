# DSA Authoring Standards

DSA is an independent problem-solving handbook, not a subsection of Interview Book. Its pages may use a distinct visual language, but must retain the site's shared navigation, responsive behaviour, accessible markup and theme support.

## Teaching objective

A reader should be able to solve the problem after studying the explanation—not merely understand code after it has been shown. Teach the reasoning in the order a strong candidate should discover it:

1. Understand the requirement and constraints.
2. Build intuition from examples and identify the important observation.
3. Consider a straightforward approach or a tempting incorrect approach when that comparison teaches something useful.
4. Choose the data structure or algorithm and explain why it fits.
5. Present the optimized Java implementation.
6. Trace the important state in a meaningful dry run.
7. Establish correctness using an invariant or a clear argument.
8. Derive time and auxiliary-space complexity.
9. Test edge cases, identify common mistakes and practise explaining the solution aloud.

Do not add a brute-force section mechanically. Include it when it helps explain the trade-off or why the optimized insight matters. Distinguish an intentionally incorrect/insufficient approach from a valid brute-force solution.

## Required problem content

For each problem, include:
- A concise problem statement in original wording, with constraints and input assumptions made explicit.
- Representative examples, including at least one case that exposes the central difficulty.
- Pattern classification and intuition before code.
- Relevant approaches and the reason the selected approach is preferred.
- An optimized, compilable Java solution with required imports and explicit input assumptions.
- A dry run that traces variables, data structures or decisions—not merely repeats the output.
- Correctness reasoning or the invariant that makes the approach work.
- Time and auxiliary-space complexity, explaining where each term comes from. State whether output space is excluded.
- Common mistakes, meaningful edge cases and small practice tests.
- A concise interview-ready explanation and one memorable takeaway.

## Writing and presentation

- Write as a clear, experienced engineer teaching another engineer. Use natural language, short paragraphs and concrete examples.
- Explain the observation before naming the pattern. Avoid unexplained jargon and generic statements such as "use hashing for efficiency."
- Every code sample must be complete enough to compile in the stated context. Include imports, method signatures, types and validation when required by the problem contract.
- Use tables for traces and comparisons only when they make state easier to follow. Use diagrams for relationships or state transitions that are difficult to explain in prose.
- Keep problem sections visually distinct and easy to scan. A reader should be able to find the intuition, code, dry run and complexity quickly.
- Keep the explanation substantial enough to teach, but avoid padding, repeated explanations and textbook digressions.
- Keep Java as the canonical language unless the user explicitly asks otherwise.

## Correctness and source review

Use the Java source repository as the source of problem selection and initial implementations, not as an unquestionable source of truth. Review every implementation for correctness, boundary conditions, Java character/overflow behaviour, complexity and input constraints. Correct bugs and explain material deviations from the original. Do not copy misleading comments or unsupported complexity claims.

For every claimed optimal solution, verify:
- It satisfies every stated constraint.
- The data structure supports the claimed operations and complexity.
- The invariant is maintained at every iteration.
- The dry run matches the code exactly.
- Complexity includes initialization and auxiliary data structures where relevant.
- Unicode, integer overflow, nullability and mutation assumptions are stated when they matter.

## Topic organization

Group problems by learning topic and pattern. Avoid duplicate problem entries; keep genuinely different approaches only when the comparison is useful. Build topic landing pages that explain the learning path and group related problems. Do not force algorithm problems into the conceptual `details.iq` Q&A format.

## Visual and navigation standards

DSA may have its own problem-card and article styling. It must continue to provide:
- Independent DSA landing page and DSA-only topic navigation.
- Shared Home and global Search access.
- Clear topic and problem navigation with working anchors.
- Responsive code blocks and tables on mobile.
- Accessible heading hierarchy, labels and semantic HTML.
- Shared theme tokens; avoid hard-coded page backgrounds that break light/dark themes.

## Review checklist

Before considering a topic complete, verify that a reader can answer:
- What exactly is the problem asking?
- What is the key observation?
- Why does this data structure or algorithm solve it?
- What does the state look like during execution?
- Why is the algorithm correct?
- Where do the time and space bounds come from?
- Which edge case is most likely to break a careless implementation?
- How would I explain the solution in one minute?
