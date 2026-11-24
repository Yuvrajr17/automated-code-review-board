import re


def extract_changed_files(diff_text: str) -> list[str]:
    """
    Extract unique file paths modified in the submitted Git diff.
    """

    changed_files = []

    for line in diff_text.splitlines():

        if line.startswith("diff --git "):

            match = re.match(r"diff --git a/(.*?) b/(.*)", line)

            if match:
                file_path = match.group(2)

                if file_path not in changed_files:
                    changed_files.append(file_path)

    return changed_files


def count_diff_changes(diff_text: str) -> dict:
    """
    Count the number of added and deleted lines in a Git diff.
    """

    added_lines = 0
    deleted_lines = 0

    for line in diff_text.splitlines():

        if line.startswith("+++") or line.startswith("---"):
            continue

        if line.startswith("+"):
            added_lines += 1

        elif line.startswith("-"):
            deleted_lines += 1

    return {
        "added_lines": added_lines,
        "deleted_lines": deleted_lines
    }