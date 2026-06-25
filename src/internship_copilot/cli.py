from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError

from internship_copilot.schemas import AnalysisRequest
from internship_copilot.service import create_fixture_analysis


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run fixture internship analysis.")
    parser.add_argument("--job-file", type=Path, required=True)
    parser.add_argument("--resume-file", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        request = AnalysisRequest(
            job_description=args.job_file.read_text(encoding="utf-8"),
            resume=args.resume_file.read_text(encoding="utf-8"),
        )
    except (OSError, ValidationError) as error:
        raise SystemExit(str(error)) from error

    report = create_fixture_analysis(request)
    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
