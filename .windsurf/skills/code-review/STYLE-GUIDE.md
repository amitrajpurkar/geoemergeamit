# Python Application Style Guide (AI-Assisted Development)

## Purpose
This style guide defines the coding and design standards for Python applications
developed with the assistance of AI code tools such as Windsurf or Claude Code.

The goal is to ensure that all code—human or AI-generated—is:
- Readable
- Maintainable
- Secure
- Architecturally consistent

AI is treated as a productivity tool, not a source of authority.

---

## Guiding Principles
- Readability over cleverness
- Explicit over implicit
- Simplicity over over-engineering
- Consistency over personal preference
- Humans must understand this code first, AI second

---

## Project Structure

A typical application layout:

app/
api/            # HTTP / RPC interfaces (FastAPI, Flask, etc.)
domain/         # Core business logic and rules
services/       # Application services and orchestration
repositories/   # Data access and persistence
models/         # Domain and API models
config/         # Configuration and settings
tests/

Rules:
- No business logic in API route handlers
- No framework imports inside domain logic
- One clear responsibility per module
- Dependencies must flow inward (API → domain, never the reverse)

---

## Naming Conventions

- Modules: `snake_case.py`
- Packages: `snake_case`
- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

Avoid vague or AI-style names such as:
- `data_handler_v2`
- `process_data_enhanced`
- `final_result`
- `helper_utils`

Names must communicate intent, not implementation history.

---

## Typing Standards

- All public functions and methods **must** be typed
- Avoid `Any` unless explicitly justified and documented
- Prefer explicit models over unstructured dictionaries
- Use `dataclasses` or `pydantic` models for structured data

### Preferred:
```python
def create_user(request: CreateUserRequest) -> User:
```

### Avoid:
```python
def create_user(data: dict):
```

Types are part of the public contract and must remain stable.

---

## Function & Method Design
	•	Functions should do one thing
	•	Prefer small, composable functions
	•	Avoid deeply nested conditionals
	•	Prefer early returns over complex branching

Default to clarity over abstraction. If an abstraction does not reduce cognitive
load, it should not exist.

---

## Error Handling
	•	Never silently ignore exceptions
	•	Catch exceptions only when adding context or translating layers
	•	Use domain-specific exceptions where possible
	•	Do not use exceptions for normal control flow

API layers may translate domain errors into HTTP responses; domain layers must not
know about transport concerns.

---

## Logging
	•	Use structured, contextual logging
	•	Never use print() in application code
	•	Logs should answer: what happened, where, and why
	•	Never log secrets, credentials, or PII

Log levels must be meaningful and consistent.

---

## Security Practices
	•	Validate all external inputs
	•	Avoid unsafe deserialization
	•	Never embed secrets in code or config files
	•	Authentication and authorization boundaries must be explicit

Assume AI-generated code may introduce insecure defaults—verify carefully.

---

## Performance & Concurrency
	•	Avoid premature optimization
	•	Watch for N+1 queries and inefficient loops
	•	Ensure async code is truly non-blocking
	•	Do not mix sync and async patterns casually

Performance changes must be justified and measurable.

---

## AI-Generated Code Rules

All AI-generated code must be treated as a first draft and:
	•	Reviewed line-by-line
	•	Simplified where possible
	•	Refactored to match project conventions
	•	Stripped of unused helpers, abstractions, and comments

Remove AI-generated filler comments and “explanatory noise.”
If the code is complex, rewrite it—do not annotate around it.

---

## Testing Standards
	•	Business logic must be testable without framework bootstrapping
	•	Tests should focus on behavior, not implementation details
	•	Avoid excessive mocking
	•	Prefer clear, descriptive test names

Tests are part of the system’s documentation.

---

## Documentation & Comments
	•	Explain why something exists, not what the code does
	•	Keep docstrings concise and accurate
	•	Update documentation when behavior changes
	•	Delete outdated comments immediately

Comments that restate the code are worse than no comments.

---

## Style Enforcement
	•	Automated linters and formatters are mandatory
	•	Code reviews enforce architectural and semantic consistency
	•	Style deviations must be justified, not habitual

Consistency across the codebase outweighs local elegance.

---


## Final Rule

If code cannot be easily understood by a senior engineer unfamiliar with the
change, it is not ready to merge—regardless of whether it was written by a human
or an AI.

----

