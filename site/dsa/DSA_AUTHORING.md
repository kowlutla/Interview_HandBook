# DSA Authoring Standards

DSA pages are problem-centred, not conceptual Q&A pages. Preserve the Interview Book's typography, navigation, responsive layout and plain-English teaching style, but use a structure suited to solving coding problems.

For each problem, include:
- Clear problem statement and representative examples.
- The underlying pattern and intuition before showing code.
- Brute force when it teaches an important trade-off; do not add it mechanically.
- An optimized, compilable Java solution with required imports and explicit input assumptions.
- A meaningful dry run that traces the important state.
- Time and auxiliary-space complexity, explaining where each term comes from.
- Correctness reasoning or the invariant that makes the approach work.
- Common mistakes and edge cases worth testing.
- A short remember line with the central insight.

Use the Java source repository as the source of problem selection and initial implementations, not as an unquestionable source of truth. Review every implementation for correctness, boundary conditions, Java character/overflow behaviour, complexity and input constraints. Correct bugs and explain material deviations from the original. Do not copy misleading comments or unsupported complexity claims.

Group problems by learning topic and pattern. Avoid duplicate problem entries; keep genuinely different approaches only when the comparison is useful. Keep explanations detailed enough to teach the reasoning, but concise enough for interview revision. Use Java as the canonical language. DSA pages may use their own problem markup and validator; do not force algorithm problems into the conceptual `details.iq` Q&A format.
