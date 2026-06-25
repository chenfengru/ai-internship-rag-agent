# Architecture Decisions

## 2026-06-25 — CLI before FastAPI

### Context

Milestone 1A needs to prove the input and report schemas before adding a web
interface or AI dependencies.

### Options considered

- Start with a plain-text CLI.
- Start with FastAPI and Swagger.
- Start with Streamlit.

### Decision

Start with a small CLI that reads plain-text files and calls a deterministic
fixture service.

### Reasoning

The CLI keeps the first milestone focused on data contracts, validation, and
testability. It also ensures that later interfaces can wrap shared application
logic instead of containing that logic themselves.

### Consequences

- Milestone 1A has no web framework dependency.
- FastAPI remains planned for Milestone 1B as a thin wrapper.
- CLI and API behavior can later share the same schemas and service.
