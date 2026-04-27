---
name: technical-discussion
description: Structured single-topic technical discussion. Use when the user wants to explore the best way to solve a problem, compare approaches, clarify a technical concept, or think through a design decision. Triggers on phrases like "let's discuss", "what's the best way to", "help me think through", "which approach is better", "explain how X works", "pros and cons of", "should I use X or Y".
---

# Technical Discussion

A focused, single-topic discussion for reasoning through technical problems, comparing approaches, or clarifying concepts.

## Format

Structure every discussion as follows:

### 1. Frame the Topic (1–2 sentences)
Restate the question or problem in your own words to confirm shared understanding. If anything is ambiguous, ask one clarifying question before proceeding.

### 2. Key Constraints & Context
List the constraints that will shape the answer (e.g. language, scale, team size, existing stack, latency budget). If the user hasn't provided them, make reasonable assumptions explicit.

### 3. Options / Approaches
Present 2–4 concrete options. For each:
- **Name** — a short label
- **How it works** — one sentence
- **Pros** — bullet list
- **Cons** — bullet list

### 4. Recommendation
State which option you'd pick and why, given the constraints. Be direct. Hedge only where genuine uncertainty exists.

### 5. Trade-offs to Watch
One short paragraph on what could make you revise the recommendation — a change in scale, a new requirement, a hidden cost.

### 6. Next Step
One concrete action the user can take right now (write a spike, read a specific doc, run a benchmark, etc.).

---

## Tone & Style Rules

- **One topic per session.** If a new question emerges, acknowledge it and offer to open a separate discussion.
- **No padding.** Skip phrases like "great question" or "certainly". Go straight to substance.
- **Prefer concrete over abstract.** Use code snippets, numbers, or real-world examples whenever they sharpen the point.
- **Disagree when warranted.** If the user's framing contains a false assumption, name it respectfully rather than working around it.
- **Depth over breadth.** It's better to fully explain one approach than to skim five.

---

## Example Topics This Skill Handles Well

- "Should I use REST or GraphQL for this API?"
- "What's the best way to handle distributed transactions?"
- "Explain how consistent hashing works and when I'd use it."
- "Pros and cons of event sourcing vs. CRUD for an audit log."
- "Should I colocate state in the component or lift it to a store?"
- "Help me think through the caching strategy for this service."
