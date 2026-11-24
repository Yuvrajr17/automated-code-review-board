
import subprocess
import tempfile
import json
import re
from pathlib import Path


def extract_python_source(diff_text: str) -> str:
    """
    Extract newly added source lines only from Python files in a Git diff.
    """

    source_lines = []
    current_file_is_python = False

    for line in diff_text.splitlines():

        if line.startswith("diff --git "):
            match = re.match(r"diff --git a/(.*?) b/(.*)", line)

            if match:
                file_path = match.group(2)
                current_file_is_python = file_path.endswith(".py")
            else:
                current_file_is_python = False

            continue

        if line.startswith(
            ("+++", "---", "@@", "index ")
        ):
            continue

        if current_file_is_python and line.startswith("+"):
            source_lines.append(line[1:])

    return "\n".join(source_lines)


def run_ruff_analysis(source_code: str) -> list[dict]:
    """
    Run Ruff static analysis on extracted Python source.
    Return detected style and code-quality issues.
    """

    if not source_code.strip():
        return []

    with tempfile.TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "reviewed_code.py"
        file_path.write_text(source_code, encoding="utf-8")

        result = subprocess.run(
            [
                "ruff",
                "check",
                str(file_path),
                "--output-format",
                "json"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode not in (0, 1):
            raise RuntimeError(
                f"Ruff execution failed: {result.stderr}"
            )

        return json.loads(result.stdout)
