# Project Plan

## 1. Project Summary

AI Internship Copilot is a portfolio-focused application that compares an
AI/ML internship job description with a candidate's resume or current skills.
It identifies supported requirements, evidence gaps, and priority learning
needs, then creates a personalized preparation plan. The target user is a
student or early-career applicant preparing for AI/ML internships. The project
is useful for internship preparation because it demonstrates practical RAG,
LLM engineering, evaluation, API development, and responsible handling of
personal data in one focused workflow.

**Assumptions**

- The first version analyzes one job description and one resume at a time.
- The resume is supplied as text or a text-based PDF.
- A schema-only CLI is the first interface; FastAPI and Swagger are added only
  after the deterministic service works.
- One hosted LLM provider will be used initially, behind a provider-neutral
  interface.
- The project will not predict whether a candidate will be hired.

## 2. Project Type

- **Portfolio Project:** it must be easy to demonstrate, explain, test, and
  present in a GitHub repository and internship interview.
- **RAG Project:** conclusions about candidate fit must be grounded in
  retrieved resume evidence.
- **Agent Project, later:** a bounded clarification or report-revision loop can
  be added after the deterministic MVP works.
- **Web App / Demo Project:** FastAPI provides a small API and an interactive
  Swagger demo without requiring a separate frontend.

The MVP is primarily a portfolio and RAG project. It should not begin as a
multi-agent system because the core analysis can be implemented more clearly as
a testable pipeline.

## 3. Problem Statement

The goal is to build a system that helps AI/ML internship applicants understand
their fit for a role and prepare efficiently by using structured LLM
extraction, retrieval over resume evidence, transparent gap scoring, and
personalized plan generation.

## 4. Target User

### User profile

An undergraduate, master's student, recent graduate, or early-career candidate
applying for AI/ML, data science, NLP, computer vision, or ML engineering
internships.

### User pain points

- Job descriptions combine required, preferred, and vague qualifications.
- Candidates may not know which gaps matter most.
- Generic preparation plans do not use the candidate's actual experience.
- It is easy to overestimate a match or overlook transferable evidence.
- Preparing separately for every role is time-consuming.

### Expected user workflow

The user provides a job description, a resume, and an optional preparation
period such as two or four weeks. The system returns an evidence-grounded match
report, prioritized gaps, and a practical preparation plan. The user reviews
uncertain conclusions rather than treating the output as a hiring prediction.

## 5. MVP Scope

### Must Have

- Accept one job description as pasted text or a `.txt` file.
- Accept one resume as text or a text-based PDF.
- Extract required skills, preferred skills, responsibilities, and seniority
  signals from the job description.
- Split the resume into traceable evidence passages.
- Match each important requirement to relevant resume evidence.
- Classify each match as `supported`, `partial`, `unsupported`, or `uncertain`.
- Prioritize gaps as high, medium, or low.
- Generate a time-bounded learning, portfolio, and interview preparation plan.
- Return schema-valid JSON and readable Markdown.
- Expose the workflow through one FastAPI endpoint and Swagger.
- Include synthetic examples, tests, evaluation results, and limitations.

### Nice to Have

- Compare several jobs and rank them by fit.
- Ingest GitHub project descriptions, coursework, and personal notes.
- Add a simple frontend after the API is stable.
- Add local-model mode for privacy.
- Export the plan as PDF.
- Ask the user clarifying questions when evidence is ambiguous.
- Support multiple languages.

### Not Included Yet

- Job-board scraping.
- User accounts or authentication.
- Automated job applications.
- Automatic resume rewriting.
- Cloud deployment or a database server.
- Scanned-PDF OCR.
- Fine-tuning a model.
- A persistent vector database.
- A multi-agent architecture.
- Hiring-probability predictions.

## 6. Core User Workflow

1. The user submits a job description, resume, and preparation period.
2. The system validates the files and extracts normalized text.
3. The system extracts structured job requirements and resume experiences.
4. The system retrieves the most relevant resume passages for each important
   requirement.
5. The system classifies matches and records supporting evidence or
   uncertainty.
6. A transparent scoring rule prioritizes the gaps.
7. The LLM turns the structured gaps into a feasible preparation plan.
8. Validators check evidence references and output consistency.
9. The API returns JSON and a Markdown report for the user to review.

## 7. Technical Architecture

```text
User
  |
  v
CLI (Milestone 1A) / FastAPI and Swagger (Milestone 1B)
  |
  v
Input Validation and PDF/Text Parser
  |
  v
Structured Job and Resume Extraction
  |
  v
Resume Chunking -> Embeddings -> FAISS Retrieval
  |                                  |
  +----------------------------------+
  |
  v
Evidence-Based Match Classification
  |
  v
Deterministic Gap Prioritization
  |
  v
LLM Preparation-Plan Generation
  |
  v
Schema and Evidence Validation
  |
  v
JSON and Markdown Report
```

### Main components

- **Interface:** begin with a CLI, then add FastAPI Swagger as a thin wrapper.
- **Backend:** plain Python services shared by the CLI and FastAPI endpoint.
- **Data storage:** local sample/evaluation files; private uploads are processed
  per request and are not committed.
- **Model layer:** one LLM client hidden behind a small interface.
- **Retrieval layer:** sentence-transformer embeddings with an in-memory FAISS
  index for the submitted resume.
- **Agent/tool layer:** deferred. The MVP uses an explicit pipeline.
- **Evaluation layer:** labeled fixtures, automated metrics, prompt regression
  checks, and human review.

### Minimal technology stack

- Python 3.11
- FastAPI and Pydantic
- `pypdf`
- Hugging Face `sentence-transformers`
- FAISS
- One LLM provider SDK
- Pytest
- Ruff

LangChain may be used for a focused integration, but business logic should stay
in ordinary Python modules. LangGraph should be added only when branching,
retries, tool selection, or human approval becomes necessary.

## 8. Data Plan

### Input data

- AI/ML internship job descriptions.
- Candidate resumes or skill profiles.
- Optional preparation period.

### Initial sample data

- 10–20 public or manually written internship descriptions.
- 3–5 synthetic or fully anonymized resumes.
- 15–30 labeled resume–job pairs for evaluation.
- A small normalized skill vocabulary for common AI/ML competencies.

### Example evaluation record

```text
job_id
resume_id
job_text
resume_text
expected_requirements
expected_matches
expected_evidence
expected_priority_gaps
reviewer_notes
```

### Storage

- `data/samples/`: redistributable demo inputs.
- `data/evaluation/`: labeled evaluation records.
- `outputs/examples/`: selected anonymized reports.
- Private resumes and generated personal reports: local ignored directories,
  never committed.

### Privacy

- Remove names, email addresses, phone numbers, locations, IDs, and private
  employer details from repository examples.
- Record the source and usage rights for public data.
- Minimize personal information sent to a hosted model.
- Do not log full private resumes by default.
- Use synthetic data when redistribution rights are unclear.

## 9. AI / ML / LLM Design

### Structured extraction

Use separate prompts to extract:

- job requirements, importance, required/preferred status, and source text;
- resume experiences, skills, outcomes, and source text.

Require Pydantic-compatible structured output. Prompts should be versioned and
tested independently.

### RAG design

- **Document loading:** parse text and text-based PDF resumes.
- **Chunking:** split by resume sections and bullet boundaries, then apply a
  modest token limit while preserving section and passage IDs.
- **Embedding model:** begin with a small sentence-transformer suitable for
  semantic similarity.
- **Vector database:** use an in-memory FAISS index per analysis request.
- **Retrieval:** retrieve the top relevant resume passages for each important
  job requirement.
- **Reranking:** omit from the first baseline; add only if retrieval evaluation
  shows a clear need.
- **Generation:** provide each requirement and its retrieved evidence to the
  match classifier, then generate the final plan from validated gaps.
- **Evaluation:** measure requirement extraction, evidence precision, match
  classification, and top-gap ranking.

### Match and gap design

Each requirement receives:

- one of four match labels;
- supporting evidence IDs, if available;
- a short rationale;
- a confidence or uncertainty note.

Missing resume evidence means `unsupported` or `uncertain`; it does not prove
that the user lacks the skill. Gap priority should combine requirement
importance, match status, repetition in the job description, transferability,
and estimated preparation effort. The scoring rule should be visible and
mostly deterministic.

### Agent design for a later version

- **Agent goal:** improve an analysis by resolving missing evidence or revising
  an invalid report.
- **Tools:** resume retriever, project/coursework retriever, clarification
  request, match validator, and plan generator.
- **Planning strategy:** a small state graph with explicit allowed transitions,
  not unrestricted autonomous planning.
- **Memory:** request-scoped structured state; no long-term personal memory in
  the first agent version.
- **Stopping condition:** stop when required fields are valid and evidence
  checks pass, or after a fixed retry limit.
- **Error handling:** return partial results and a clear error when parsing,
  retrieval, model calls, or validation fail.
- **Safety boundaries:** never invent experience, submit applications, edit a
  resume without approval, or expose private inputs.

### LLM controls

- Use low-temperature settings where supported.
- Give each prompt one task.
- Require structured output.
- Validate all evidence references.
- Store prompt version and model settings with evaluation results.
- Mock paid API calls in normal tests.

## 10. File Structure

This is the target structure. Create files only when their milestone requires
them.

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
│   ├── fixtures/
│   ├── unit/
│   └── integration/
└── outputs/
    └── examples/
```

### Decision Log Rule

Update `docs/DECISIONS.md` whenever making a meaningful architecture choice.
Each entry should record the context, options considered, selected option,
reasoning, consequences, and date. At minimum, document:

- why CLI before FastAPI;
- why FastAPI instead of Streamlit;
- why a deterministic pipeline before an agent;
- why FAISS instead of Chroma;
- why the vector index is request-scoped;
- why the system stores no persistent personal data.

The decision log should explain choices in interview-ready language without
pretending that deferred alternatives are inherently bad.

## 11. Milestones

### Milestone 1A: Schema-only CLI prototype

- **Goal:** prove the core data contract and input-to-report flow with the
  smallest possible CLI prototype.
- **Files to create/edit:** `requirements.txt`, `schemas.py`, a small CLI entry
  point, fixture analysis service, sample text fixtures, and schema tests.
- **Expected output:** the CLI accepts a plain-text job description and resume,
  then returns a fake but schema-valid analysis report.
- **How to verify:** run the CLI with valid and invalid text inputs, validate the
  full output against the Pydantic schemas, run Pytest, and check Ruff.
- **Estimated difficulty:** beginner.
- **Common mistakes:** adding FastAPI, PDF parsing, embeddings, FAISS, or live
  LLM calls; using vague schemas; and hardcoding only one successful input.

### Milestone 1B: FastAPI wrapper

- **Goal:** expose the deterministic schema-based service through a minimal API
  without changing its core behavior.
- **Files to create/edit:** `app.py`, API request/response adapters, API
  contract tests, and `docs/DECISIONS.md`.
- **Expected output:** `POST /analyze` accepts plain-text job description and
  resume fields and returns the same schema-valid fixture analysis as the CLI.
- **How to verify:** call `/analyze` with valid and invalid requests, compare API
  output with the deterministic service output, and run API contract tests.
- **Estimated difficulty:** beginner to intermediate.
- **Common mistakes:** placing analysis logic in the route handler, changing
  schemas only for the API, adding PDF support too early, and skipping error
  response tests.

### Milestone 2: Evidence-grounded RAG analysis

- **Goal:** produce useful requirement matches and skill gaps grounded in
  resume passages.
- **Files to create/edit:** `extraction.py`, `retrieval.py`, `matching.py`,
  `prompts.py`, `service.py`, integration tests, and anonymized samples.
- **Expected output:** each important requirement has a valid label, rationale,
  and evidence reference or an explicit uncertainty.
- **How to verify:** run the labeled examples, inspect evidence precision,
  confirm unsupported requirements receive no invented evidence, and test model
  failures with mocks.
- **Estimated difficulty:** intermediate.
- **Common mistakes:** oversized chunks, treating semantic similarity as proof,
  mixing extraction and generation prompts, and trusting malformed model output.

### Milestone 3: Personalized plan and portfolio evaluation

- **Goal:** generate a time-bounded preparation plan and publish credible
  evaluation evidence.
- **Files to create/edit:** `planning.py`, `docs/EVALUATION.md`, evaluation
  records, README, example outputs, CI configuration, and expanded tests.
- **Expected output:** a complete Markdown/JSON report plus documented metrics,
  limitations, demo flow, and failure analysis.
- **How to verify:** run automated metrics, complete the human rubric, reproduce
  the demo from a clean setup, and run all quality checks.
- **Estimated difficulty:** intermediate.
- **Common mistakes:** generic recommendations, invented metrics, evaluating
  only easy examples, and polishing the UI before analysis quality.

### Milestone 4: Optional bounded agent workflow

- **Goal:** add clarification or validation-retry behavior only if evaluation
  shows it improves results.
- **Files to create/edit:** a small workflow module, agent-state schemas,
  agent-specific tests, and `docs/DECISIONS.md`.
- **Expected output:** the system can request missing information or retry one
  invalid stage within strict limits.
- **How to verify:** test all state transitions, retry limits, stopping
  conditions, and partial-failure behavior.
- **Estimated difficulty:** intermediate to advanced.
- **Common mistakes:** adding tools without a measurable need, infinite loops,
  hidden state, and calling a fixed pipeline an agent.

## 12. Implementation Steps

1. Define Pydantic schemas for the input, requirement, evidence passage, match
   result, gap, preparation action, and final report.
2. Create one synthetic resume and two sample job descriptions.
3. Create a CLI that accepts plain-text job and resume inputs.
4. Return a fake but schema-valid analysis report from a deterministic fixture
   service.
5. Add schema, CLI, and invalid-input tests without adding FastAPI, PDF parsing,
   embeddings, FAISS, or live LLM calls.
6. Record the CLI-first decision in `docs/DECISIONS.md`.
7. Add the FastAPI `/analyze` wrapper around the same deterministic service.
8. Add API contract and error-response tests.
9. Render the same report as JSON and Markdown.
10. Add text-based PDF extraction with clear unsupported-file errors.
11. Implement job-requirement and resume-experience extraction behind the LLM
   interface.
12. Chunk resume evidence and build a request-scoped FAISS index.
13. Retrieve passages for each requirement and assign stable evidence IDs.
14. Implement match classification and validate all cited IDs.
15. Implement deterministic gap priority scoring.
16. Generate preparation actions from validated gaps and the selected time
    period.
17. Build the labeled evaluation set and calculate baseline metrics.
18. Review failure cases before changing prompts, retrieval, or architecture.
19. Update the README with setup, architecture, demo output, evaluation,
    privacy, limitations, and interview talking points.
20. Consider an agent workflow only after the deterministic MVP meets its
    acceptance criteria.

## 13. Testing Plan

### Unit tests

- Text normalization and PDF parsing.
- Empty, oversized, and unsupported inputs.
- Resume chunk boundaries and evidence IDs.
- Gap scoring and priority ordering.
- Structured model-output parsing.
- Evidence-reference validation.
- Markdown rendering.

### Integration and contract tests

- `/analyze` follows the published request and response schemas.
- A text resume and job description produce a complete report.
- A PDF fixture produces the expected normalized text.
- Retrieved passages belong to the submitted resume.
- Unsupported requirements do not receive positive evidence claims.
- Timeout, malformed JSON, missing configuration, and provider failures return
  understandable errors.

### Manual and qualitative tests

- Does each positive match have relevant evidence?
- Are uncertain cases labeled honestly?
- Are the top gaps important for the job?
- Can the proposed actions fit the selected preparation period?
- Is the report specific to the supplied inputs rather than generic?
- Can a reviewer trace recommendations back to job requirements?

### Quality commands

```text
pytest
ruff format --check .
ruff check .
```

Live-model tests should be optional and marked separately. Normal tests should
use mocked provider responses.

### Anti-hallucination Tests

- If the resume does not mention a skill, the system must not mark that skill as
  `supported`.
- If a match cites an evidence ID that does not exist, validation must fail.
- If the LLM claims experience without supporting evidence, validation must
  downgrade the match to `uncertain` or `unsupported`.
- If a job requirement is vague or cannot be tested against specific resume
  evidence, the system must label the match `uncertain`.

These checks should be automated regression tests, not only prompt
instructions.

## 14. Evaluation Plan

Create a gold set of 15–30 resume–job pairs and manually label important
requirements, match classes, acceptable evidence, and top gaps. Double-review a
small subset to identify ambiguous labels.

### Metrics

- Requirement extraction precision, recall, and F1.
- Match-classification accuracy and macro F1.
- Retrieval or evidence precision.
- Top-three gap overlap or Precision@3.
- Structured-output success rate.
- Median latency and approximate cost per analysis.

### Human rubric

Rate reports from 1 to 5 for correctness, evidence grounding, prioritization,
plan feasibility, clarity, and honesty about uncertainty.

### Initial acceptance targets

These are targets, not claimed results:

- At least 95% schema-valid responses.
- At least 90% of match claims have valid evidence or an explicit
  unsupported/uncertain label.
- At least 80% overlap with reviewer-selected top-three gaps.
- At least 4/5 average human usefulness.
- Under 30 seconds median latency for the hosted-model MVP.

Publish actual results, weak cases, and limitations. Do not replace failed
evaluation with handpicked demo examples.

### Demo Scenario

Use one anonymized resume and one representative AI internship job description
as the stable end-to-end portfolio demo. Show:

1. the input job description;
2. the input resume;
3. extracted job requirements;
4. evidence-matched resume passages;
5. `supported`, `partial`, `unsupported`, and `uncertain` labels;
6. the top three preparation gaps;
7. a two-week preparation plan;
8. limitations and uncertainty notes.

The demo should be reproducible from repository-safe inputs and should expose
weak or uncertain results rather than presenting a hand-edited perfect output.

## 15. Risks and Things to Avoid

- Scope expanding into scraping, authentication, deployment, or multiple agents.
- Treating embedding similarity as proof of experience.
- Invented skills, achievements, metrics, or hiring predictions.
- Generic preparation plans unrelated to the detected gaps.
- Sending or committing private resume data.
- Too many frameworks obscuring the core logic.
- No labeled test data or formal evaluation.
- Testing only the happy path.
- Hardcoded examples presented as a functioning system.
- Adding reranking, memory, or a vector server before evaluation justifies it.
- A polished frontend with weak evidence grounding.
- A README that describes features the repository cannot reproduce.

## 16. Portfolio Value

### Skills demonstrated

- FastAPI and typed API design.
- LLM structured outputs and prompt versioning.
- RAG with embeddings, retrieval, and evidence grounding.
- Transparent ranking and uncertainty handling.
- Automated testing and AI-specific evaluation.
- Privacy-aware data design.
- Modular software architecture and CI.
- Product scoping and technical communication.

### Resume bullet ideas

Use actual measured results when available:

- Built an evidence-grounded AI Internship Copilot that maps job requirements
  to resume passages and generates prioritized preparation plans using FastAPI,
  structured LLM outputs, and FAISS retrieval.
- Designed a labeled evaluation set and measured requirement extraction, match
  classification, evidence precision, latency, and report usefulness.
- Added schema validation and evidence checks to prevent unsupported claims
  about candidate experience.

### Interview talking points

- Why the MVP is a deterministic pipeline rather than an agent.
- Why the vector index is request-scoped.
- How unsupported experience claims are prevented.
- How match labels and gap priorities are defined.
- What the evaluation revealed and what changed afterward.
- How the design protects personal resume data.
- When LangGraph, reranking, or a persistent vector store would be justified.

### GitHub README highlights

- One-sentence problem statement.
- Architecture diagram.
- Reproducible quick start.
- Anonymized input and output example.
- Evaluation table with real results.
- Privacy and limitations.
- Short demo video or animation.
- Design decisions and roadmap.

## 17. Next Codex Action

Next, implement Milestone 1A only: define the core Pydantic schemas and create a
CLI-based fixture analysis flow. Do not add FastAPI, PDF parsing, embeddings,
FAISS, or live LLM calls yet.
