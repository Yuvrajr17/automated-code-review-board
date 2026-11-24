
import re


def identify_test_files(diff_text: str) -> list[str]:
    """
    Identify test files included in a Git diff.
    """

    test_files = []

    for line in diff_text.splitlines():

        if line.startswith("diff --git "):

            match = re.match(
                r"diff --git a/(.*?) b/(.*)",
                line
            )

            if match:
                file_path = match.group(2)

                filename = file_path.split("/")[-1].lower()

                is_test_file = (
                    filename.startswith("test_")
                    or filename.endswith("_test.py")
                    or "/tests/" in file_path.lower()
                    or "/test/" in file_path.lower()
                )

                if is_test_file and file_path not in test_files:
                    test_files.append(file_path)

    return test_files


def analyze_test_changes(
    diff_text: str,
    test_files: list[str]
) -> dict:
    """
    Analyze whether the submitted diff contains test changes.
    """

    added_lines = 0
    deleted_lines = 0

    current_file = None

    for line in diff_text.splitlines():

        if line.startswith("diff --git "):
            parts = line.split(" b/", 1)

            current_file = parts[1] if len(parts) == 2 else None

        elif line.startswith(("+++", "---")):
            continue

        elif current_file in test_files:

            if line.startswith("+"):
                added_lines += 1

            elif line.startswith("-"):
                deleted_lines += 1

    return {
        "test_files_found": len(test_files),
        "test_files": test_files,
        "test_changes_detected": bool(test_files),
        "added_test_lines": added_lines,
        "deleted_test_lines": deleted_lines,
        "assessment": (
            "Test files were modified or added."
            if test_files
            else "No test-file changes detected in the submitted diff."
        )
    }
