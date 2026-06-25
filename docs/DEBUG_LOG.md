# Debug Log

## 2026-06-25 — Milestone 1A test-first implementation

### Bug

The planned schema and CLI behavior did not exist yet.

### Expected Behavior

The project should construct and serialize a valid report, reject blank resume
input, reject unknown evidence references, and return schema-valid JSON from a
plain-text CLI.

### Actual Behavior

The initial test run failed during collection because the
`internship_copilot` package did not exist.

### Failing Tests Added

- `tests/unit/test_schemas.py::test_valid_report_can_be_constructed_and_serialized`
- `tests/unit/test_schemas.py::test_empty_resume_input_is_rejected`
- `tests/unit/test_schemas.py::test_match_with_nonexistent_evidence_id_fails_validation`
- `tests/unit/test_cli.py::test_cli_returns_schema_valid_json_for_plain_text_inputs`

### Root Cause

Milestone 1A had only been planned; there were no schemas, fixture service, or
CLI modules.

### Fix

Added strict Pydantic schemas, cross-reference validation, a deterministic
fixture analysis service, and an `argparse` CLI that reads plain-text files and
prints JSON.

### Verification

- Initial `PYTHONPATH=src python3 -m pytest tests/unit -q` — failed during
  collection because `internship_copilot` did not exist.
- Final `PYTHONPATH=src python3 -m pytest -q` — passed: 4 tests.
- `PYTHONPATH=src python3 -m internship_copilot.cli --job-file tests/fixtures/job_description.txt --resume-file tests/fixtures/resume.txt`
  — succeeded and printed schema-valid JSON.
- `python3 -m ruff --version` — could not run because Ruff is not installed.

### Notes

- The available local interpreter is Python 3.10.11; the project target remains
  Python 3.11.
- FastAPI, PDF parsing, embeddings, vector stores, agents, and live LLM calls
  remain outside Milestone 1A.

## 2026-06-25 — Minimal project planner module

### Bug

The project had a preparation-action schema but no module that could turn
prioritized skill gaps into a preparation plan.

### Expected Behavior

The planner should order gaps by priority, create one schema-valid action per
gap, keep actions inside the requested time window, and reject invalid
durations.

### Actual Behavior

The first planner test failed during collection because
`internship_copilot.planning` did not exist.

### Failing Test Added

- `tests/unit/test_planning.py::test_create_preparation_plan_prioritizes_gaps_and_fits_time_window`
- `tests/unit/test_planning.py::test_create_preparation_plan_rejects_invalid_duration`

### Root Cause

The planner module had not been implemented.

### Fix

Added a small deterministic `create_preparation_plan` function that uses the
existing `SkillGap`, `Priority`, and `PreparationAction` schemas.

### Verification

- `PYTHONPATH=src python3 -m pytest tests/unit/test_planning.py -q` — passed: 2
  tests.
- `PYTHONPATH=src python3 -m pytest -q` — passed: 6 tests.
- `python3 -m compileall -q src tests` — passed.

### Notes

- The module does not use an LLM and does not infer or rank gaps itself.
