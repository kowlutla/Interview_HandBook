# System Design Interview Notes

A practical, interview-focused guide to the fundamentals of High-Level Design (HLD).

The goal is not to document every distributed-systems topic. It is to build the mental models needed to clarify requirements, choose suitable components, reason about trade-offs, and explain an architecture clearly in an interview.

> **Editorial rule:** Every section must help the reader understand a concept, make a design decision, or answer an interview question. Keep the explanation detailed enough to build understanding, but short enough to revise.

## How to use these notes

1. Learn the concept and the problem it solves.
2. Understand the basic flow before memorizing terminology.
3. Focus on when to use a technique, when not to use it, and its trade-offs.
4. Practise answering the interview questions aloud.
5. Use the quick revision section before interviews.

## Chapter format

Most topics use this structure, adapting it when a section would add no value:

- **What and why** — definition and problem being solved.
- **How it works** — plain-language explanation and a simple diagram when useful.
- **Key choices** — patterns or options and when each fits.
- **Trade-offs and failure modes** — the most important costs, limitations, and risks.
- **Example** — one realistic example, only where it improves understanding.
- **Interview questions** — direct questions with explanatory answers.
- **Quick revision** — a compact recap.

## Core curriculum

See [Curriculum](CURRICULUM.md) for the planned learning path and scope.

## Scope boundaries

This guide focuses on HLD fundamentals. Deep implementation tutorials, exhaustive protocol specifications, niche specialist architectures, and large end-to-end case studies are intentionally out of scope for the core notes. They can be developed separately when needed.

## Status

This is a new, separate guide. The existing `system-design-mastery/` folder is intentionally left unchanged. Chapters will be marked complete only after their content and links have been reviewed.
