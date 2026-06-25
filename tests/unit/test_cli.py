from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from internship_copilot.schemas import AnalysisReport


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = PROJECT_ROOT / "tests" / "fixtures"


def test_cli_returns_schema_valid_json_for_plain_text_inputs() -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "internship_copilot.cli",
            "--job-file",
            str(FIXTURES / "job_description.txt"),
            "--resume-file",
            str(FIXTURES / "resume.txt"),
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    report = AnalysisReport.model_validate_json(result.stdout)
    assert report.summary
    assert report.matches
