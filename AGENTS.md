# AGENTS.md

## Project goal

Build AI Internship Copilot: a small, interview-ready system that compares one
AI/ML internship description with one resume, grounds match claims in resume
evidence, identifies skill gaps, and produces a focused preparation plan.

The intended MVP is a deterministic RAG pipeline. Agent behavior is optional
and belongs to a later milestone.

## Current stage

- Stage: working Milestone 1A prototype.
- Current milestone: **Milestone 1A — schema-only CLI prototype**, implemented
  and awaiting review before any Milestone 1B work.
- Treat `docs/PLAN.md` as the source of truth for scope and milestone order.
- Do not describe planned functionality as implemented.

## Milestone 1A scope

When implementation is explicitly requested, limit work to:

- core Pydantic schemas for inputs, requirements, evidence, matches, gaps,
  preparation actions, and the final report;
- plain-text job-description and resume input through a small CLI;
- a deterministic fixture service that returns fake but schema-valid analysis;
- synthetic or anonymized text fixtures;
- schema, CLI, and invalid-input tests.

Do **not** add yet:

- FastAPI, Swagger, or any frontend;
- PDF parsing or OCR;
- embeddings, FAISS, Chroma, or other retrieval infrastructure;
- LangChain, LangGraph, agents, tools, or memory;
- live LLM calls or provider SDKs;
- persistent databases, accounts, scraping, deployment, or cloud services.

## Environment and file guidance

- Target Python version: 3.11.
- Pydantic is the only required application dependency planned for Milestone
  1A; add other dependencies only when their milestone begins.
- Established commands:
  - Install: `python3 -m pip install -r requirements.txt`
  - Run CLI: `PYTHONPATH=src python3 -m internship_copilot.cli --job-file <job.txt> --resume-file <resume.txt>`
  - Test: `PYTHONPATH=src python3 -m pytest`
- No format or lint command is established until Ruff is added and configured.
- Create only files needed by the active milestone. Do not scaffold the full
  planned tree in advance.
- Keep interfaces thin and put reusable behavior in ordinary Python modules.

## Skill usage

- For planning or scope changes, use the project-planner guidance and update
  `docs/PLAN.md` first.
- For README work, use the README-builder guidance and keep status claims
  truthful.
- After a significant plan or milestone change, use the agents-updater guidance
  to realign this file.
- For debugging, follow test-first debugging: reproduce the failure with the
  smallest test before changing implementation.

## Testing and debugging

- Write tests with each implementation change; do not postpone all tests until
  the end of a milestone.
- For a bug, first add or identify a failing regression test, confirm the
  failure, make the smallest fix, then rerun the relevant tests.
- Milestone 1A tests must cover valid schema construction, rejected invalid
  data, CLI input handling, and schema-valid fixture output.
- Do not call external services in normal tests.
- After editing, run the relevant available checks. If checks cannot run,
  explain exactly what is missing; do not invent commands.

## AI grounding and anti-hallucination

These rules apply to schemas, fixtures, tests, and all later AI behavior:

- A skill absent from the resume must never be marked `supported`.
- Every positive match must reference valid resume evidence.
- A nonexistent evidence ID must fail validation.
- A claim without supporting evidence must become `uncertain` or
  `unsupported`.
- A vague requirement without specific evidence must be `uncertain`.
- Missing resume evidence does not prove that the candidate lacks a skill.
- Never invent candidate experience, metrics, evaluation results, or hiring
  predictions.

## Privacy

- Use only synthetic, anonymized, or clearly redistributable repository data.
- Never commit real resumes, personal reports, credentials, API keys, or
  private job data.
- Remove names, contact details, locations, IDs, and private employer details
  from examples.
- Do not log full private resumes or persist personal data.
- The system is a preparation assistant, not a hiring predictor or application
  submission tool.

## Decision logging

Update `docs/DECISIONS.md` whenever implementation introduces a meaningful
architecture choice. Record the date, context, options, decision, reasoning,
and consequences.

Required decisions include CLI before FastAPI, FastAPI instead of Streamlit,
deterministic pipeline before agent, FAISS instead of Chroma, request-scoped
retrieval, and no persistent personal data. Do not create the file merely to
pre-fill future decisions; add entries when the relevant choice is made.

## README rules

- Update `README.md` separately when implemented behavior, setup, commands,
  project status, or limitations change.
- Never document planned features as completed.
- Never invent commands, outputs, screenshots, metrics, or benchmark results.
- A documentation-only task does not require unrelated README edits.

## Definition of done

For Milestone 1A:

- the CLI accepts plain-text inputs and returns fixture-based, schema-valid
  output;
- relevant schema and CLI tests pass, or failures are clearly explained;
- no later-milestone technology has been introduced;
- privacy and anti-hallucination rules are covered by validation or tests;
- `docs/DECISIONS.md` and `README.md` are updated only when the change makes
  their current content inaccurate.
