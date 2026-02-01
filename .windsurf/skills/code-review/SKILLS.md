# Code Review Skills — Senior Python Developer & Application Architect

## Purpose
This document defines the expected **code review skills and responsibilities**
when working with AI-assisted development tools (e.g., Windsurf, Claude Code)
on Python applications with backend and frontend components.

The reviewer acts as:
- Architectural steward
- Quality gatekeeper
- Risk mitigator
- Mentor (to both humans and AI output)

---

## Core Review Principles

- Optimize for **long-term maintainability**, not short-term velocity
- Treat AI-generated code as **untrusted first drafts**
- Prefer clarity over cleverness
- Enforce consistency across backend and frontend layers
- Review for *system behavior*, not just local correctness

---

## Backend Review Skills (Python)

### Architecture & Design
- Validate clear separation of concerns:
  - API layer (FastAPI / Flask)
  - Domain / business logic
  - Persistence & integrations
- Ensure dependency direction is correct (no inverted imports)
- Identify unnecessary abstractions or premature generalization
- Verify service boundaries and module ownership

### Code Quality
- Enforce idiomatic Python (PEP 8, PEP 484, PEP 544 where applicable)
- Validate typing strategy:
  - Proper use of `typing`, `pydantic`, or dataclasses
  - Avoid misleading or overly generic types
- Identify hidden complexity introduced by AI (magic, indirection, callbacks)

### Error Handling & Resilience
- Validate consistent exception strategy
- Ensure errors are:
  - Logged with context
  - Mapped correctly to API responses
- Detect silent failures or swallowed exceptions

### Performance & Scalability
- Spot N+1 queries, inefficient loops, blocking I/O
- Validate async usage (no fake async)
- Ensure AI has not introduced unnecessary caching or optimization

---

## Frontend Review Skills (Python-based or API-facing)

### API Contracts
- Validate request/response schemas
- Ensure backward compatibility
- Detect leaky abstractions between frontend and backend

### State & Data Flow
- Confirm predictable data ownership
- Avoid over-fetching or under-fetching
- Validate pagination, filtering, and sorting patterns

---

## Security & Compliance
- Identify:
  - Injection risks
  - Unsafe deserialization
  - Secrets in code or config
- Validate authentication & authorization boundaries
- Ensure AI has not added insecure defaults

---

## AI-Specific Review Skills

### AI Output Evaluation
- Detect hallucinated libraries, APIs, or patterns
- Question copied patterns that do not fit project context
- Reduce verbosity and over-engineering common in AI output

### Prompt-Aware Reviewing
- Infer intent from prompts used
- Recommend prompt improvements when patterns repeat
- Flag areas where AI should *not* be used (critical logic, security)

---

## Documentation & Knowledge Transfer
- Ensure code explains *why*, not just *what*
- Validate README, docstrings, and inline comments
- Encourage architectural decision records (ADR-style notes)

---

## Reviewer Mindset
- Be precise, calm, and objective
- Comment on *impact*, not personal preference
- Leave the codebase better than you found it
