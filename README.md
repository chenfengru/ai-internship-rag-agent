# AI Internship Copilot

A developing evidence-grounded RAG application for comparing AI/ML internship
requirements with a candidate's resume and creating a focused preparation plan.

## Project Status

**Current stage: Milestone 1A working prototype**

The repository now contains a schema-only CLI and deterministic fixture
analysis. It does not yet perform RAG or LLM analysis.

**Implemented**

- Core Pydantic schemas and evidence-reference validation.
- Plain-text CLI input.
- Deterministic fixture analysis with schema-valid JSON output.
- Deterministic preparation planning from prioritized skill gaps.
- Schema, invalid-input, evidence-reference, and CLI tests.

**Planned**

- Milestone 1B: FastAPI wrapper around the deterministic service.
- Evidence-grounded resume and job-description matching.
- Skill-gap prioritization and a two-week preparation plan.
- Evaluation using labeled, anonymized examples.

**Not included yet**

- Live LLM calls, embeddings, or FAISS retrieval.
- PDF parsing.
- API endpoints or a frontend.
- Evaluation results, metrics, screenshots, or demo output.
- Agent behavior.

See [docs/PLAN.md](docs/PLAN.md) for the complete project plan.

## Problem

AI/ML internship descriptions often mix required skills, preferred skills,
responsibilities, and vague expectations. Applicants may struggle to identify
which requirements their resume supports, where evidence is weak, and which
gaps deserve attention first.

AI Internship Copilot is planned to turn one job description and one resume
into an evidence-grounded analysis. It will distinguish supported experience
from missing or uncertain evidence and use the resulting gaps to propose a
practical preparation plan. It will not predict hiring outcomes.

## Target User

The intended user is an undergraduate, master's student, recent graduate, or
early-career applicant preparing for AI/ML, data science, NLP, computer vision,
or ML engineering internships.

The project is designed for applicants who want to:

- interpret a job description more systematically;
- connect requirements to specific resume evidence;
- avoid overstating their experience;
- prioritize learning and portfolio work;
- prepare interview topics for a particular role.

## Planned Demo Workflow

The intended end-to-end demo will use one anonymized resume and one AI
internship job description:

1. The user provides the job description.
2. The user provides a resume or skill profile.
3. The system extracts important job requirements.
4. The system retrieves relevant resume passages.
5. Each requirement receives a `supported`, `partial`, `unsupported`, or
   `uncertain` label.
6. The system identifies the top three preparation gaps.
7. The system creates a two-week preparation plan.
8. The report includes limitations and uncertainty notes.

This workflow is planned and does not run yet.

## Features

| Feature | Status | Notes |
| --- | --- | --- |
| Core Pydantic schemas | Implemented — Milestone 1A | Define inputs, evidence, matches, gaps, actions, and report structure. |
| Plain-text CLI | Implemented — Milestone 1A | Accept one job description and one resume file. |
| Fixture analysis | Implemented — Milestone 1A | Return deterministic schema-valid data without AI dependencies. |
| FastAPI `/analyze` endpoint | Planned — Milestone 1B | Wrap the same deterministic service used by the CLI. |
| PDF resume parsing | Planned — Milestone 2 | Limited to text-based PDFs initially. |
| Structured LLM extraction | Planned — Milestone 2 | Extract requirements and resume experiences into validated schemas. |
| Resume chunking and embeddings | Planned — Milestone 2 | Preserve traceable passage IDs. |
| FAISS evidence retrieval | Planned — Milestone 2 | Use a request-scoped in-memory index. |
| Evidence-based match labels | Planned — Milestone 2 | Prevent unsupported positive claims. |
| Gap prioritization | Planned — Milestone 2 | Use visible, mostly deterministic scoring. |
| Deterministic preparation planner | Implemented | Convert prioritized gaps into time-bounded actions. |
| Personalized preparation plan | Planned — Milestone 3 | Generate time-bounded learning, project, and interview actions. |
| Evaluation and portfolio demo | Planned — Milestone 3 | Publish actual results and failure cases after evaluation. |
| Bounded agent workflow | Optional — Milestone 4 | Consider only if evaluation demonstrates a need. |

## Planned Architecture

```text
Job Description + Resume
          |
          v
CLI (Milestone 1A)
FastAPI Wrapper (Milestone 1B)
          |
          v
Input Validation and Parsing
          |
          v
Structured Requirement and Experience Extraction
          |
          v
Resume Chunking -> Embeddings -> Request-Scoped FAISS Retrieval
          |
          v
Evidence-Based Match Classification
          |
          v
Deterministic Gap Prioritization
          |
          v
Preparation-Plan Generation
          |
          v
Schema and Evidence Validation
          |
          v
JSON and Markdown Report
```

The MVP is planned as a deterministic pipeline rather than an autonomous
agent. Plain Python services will contain the core logic so that the CLI and
later FastAPI endpoint can share the same behavior. Retrieval will be scoped to
the submitted resume, and every positive match should reference a valid
evidence passage.

## Tech Stack

### Currently Used

- Python
- Pydantic
- `argparse`
- Pytest

### Planned

- Python 3.11
- Pydantic
- FastAPI
- `pypdf`
- Hugging Face `sentence-transformers`
- FAISS
- One LLM provider behind a small provider-neutral interface
- Pytest
- Ruff

LangChain may be used for a focused integration. LangGraph is deferred unless a
later clarification or validation-retry workflow requires explicit state and
branching.

## Project Structure

### Current

```text
.
├── .gitignore
├── AGENTS.md
├── README.md
├── requirements.txt
├── docs/
│   ├── DEBUG_LOG.md
│   ├── DECISIONS.md
│   └── PLAN.md
├── src/
│   └── internship_copilot/
│       ├── __init__.py
│       ├── cli.py
│       ├── planning.py
│       ├── schemas.py
│       └── service.py
└── tests/
    ├── fixtures/
    └── unit/
```

IDE configuration files are not part of the application design.

### Planned

```text
ai-internship-copilot/
├── README.md
├── AGENTS.md
├── app.py
├── requirements.txt
├── .env.example
├── docs/
│   ├── PLAN.md
│   ├── DECISIONS.md
│   └── EVALUATION.md
├── data/
│   ├── samples/
│   └── evaluation/
├── src/
│   └── internship_copilot/
│       ├── config.py
│       ├── schemas.py
│       ├── cli.py
│       ├── ingestion.py
│       ├── extraction.py
│       ├── retrieval.py
│       ├── matching.py
│       ├── planning.py
│       ├── prompts.py
│       ├── reporting.py
│       └── service.py
├── tests/
└── outputs/
    └── examples/
```

Files and directories will be added only when their milestone requires them.

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## How to Run

```bash
PYTHONPATH=src python3 -m internship_copilot.cli \
  --job-file tests/fixtures/job_description.txt \
  --resume-file tests/fixtures/resume.txt
```

## Example Input and Output

To be added after the first working demo.

The example will use synthetic or anonymized data and will show the input job
description, input resume, extracted requirements, matched evidence, four match
labels, top three gaps, a two-week plan, and uncertainty notes.

## Testing

Milestone 1A tests can be run with:

```bash
PYTHONPATH=src python3 -m pytest
```

The planned test strategy includes:

- Pydantic schema and validation tests;
- CLI and API contract tests;
- invalid and empty input tests;
- evidence-reference validation;
- retrieval and match-classification checks;
- mocked LLM failure tests;
- qualitative review of preparation-plan usefulness.

Planned anti-hallucination checks include:

- a skill absent from the resume must not be marked `supported`;
- a nonexistent evidence ID must fail validation;
- an unsupported LLM experience claim must be downgraded to `uncertain` or
  `unsupported`;
- a vague requirement without specific evidence must be marked `uncertain`.

## Evaluation

Evaluation is planned after the evidence-grounded RAG analysis milestone. No
results or benchmark metrics are available yet.

The planned evaluation will use synthetic or anonymized resume–job pairs with
human labels for:

- important job requirements;
- match classes;
- acceptable supporting evidence;
- top preparation gaps.

Planned measures include requirement-extraction precision and recall,
match-classification performance, evidence precision, top-gap overlap,
structured-output reliability, latency, cost, and a human usefulness rubric.
Actual results and known failure cases will be added after evaluation.

## Privacy and Safety

- Repository examples will use synthetic or anonymized resumes.
- Private resumes, personal reports, and credentials must not be committed.
- Personal identifiers should be removed before using hosted model services.
- The planned vector index is request-scoped and should not persist personal
  data.
- Full private resumes should not be logged by default.
- The system must not invent candidate experience.
- Missing evidence should produce `unsupported` or `uncertain`, not a positive
  match.
- The project is a preparation assistant, not a hiring-probability predictor.
- It will not submit applications or edit a resume without user approval.

## Limitations

- The current application is a fixture-based schema and CLI prototype, not a
  real internship analysis system.
- Retrieval quality and LLM behavior have not been evaluated.
- The current prototype supports plain-text files only.
- PDF parsing, embeddings, FAISS, and live LLM calls are later milestones.
- The planned analysis depends on the completeness and clarity of the supplied
  resume and job description.
- Absence of resume evidence does not prove that the candidate lacks a skill.
- The system will not predict interview selection or hiring outcomes.
- Agent behavior is optional and outside the initial MVP.

## Roadmap

- [x] **Milestone 1A:** schema-only CLI prototype with fixture analysis.
- [ ] **Milestone 1B:** FastAPI wrapper and API contract tests.
- [ ] **Milestone 2:** evidence-grounded RAG analysis.
- [ ] **Milestone 3:** personalized plan, evaluation, and portfolio demo.
- [ ] **Milestone 4:** optional bounded clarification or validation workflow.

Meaningful architecture choices will be recorded in the planned
`docs/DECISIONS.md`, including CLI before FastAPI, deterministic pipeline before
agent, FAISS instead of Chroma, request-scoped retrieval, and no persistent
personal data.

## What I Plan to Learn

Current and intended learning outcomes include:

- designing stable Pydantic contracts before adding model dependencies;
- separating interfaces from reusable application services;
- grounding LLM conclusions in traceable resume evidence;
- testing failure and hallucination cases rather than only happy paths;
- evaluating retrieval and generated recommendations;
- documenting architecture trade-offs clearly;
- handling personal application data responsibly.

## Interview Talking Points

After implementation and evaluation, the project is intended to support
discussion of:

- why the first version begins with a CLI and schemas;
- why FastAPI is planned as a thin wrapper rather than the core application;
- why the MVP is a deterministic pipeline rather than an agent;
- how Pydantic validation controls structured model output;
- how evidence references reduce unsupported experience claims;
- why FAISS is sufficient for a small request-scoped resume index;
- how anti-hallucination behavior will be tested;
- how evaluation and failure analysis guide later architecture choices;
- how private resume data is kept out of persistent storage.

## License

License to be decided.
