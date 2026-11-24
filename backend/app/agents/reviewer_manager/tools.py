
def get_value(finding, key, default=None):
    """Read a field from either a dictionary or an object."""
    if isinstance(finding, dict):
        return finding.get(key, default)

    return getattr(finding, key, default)


def remove_duplicate_findings(findings: list) -> list:
    """
    Remove duplicate findings based on agent, file,
    line number and title.
    """

    unique_findings = []
    seen = set()

    for finding in findings:
        key = (
            get_value(finding, "agent_name"),
            get_value(finding, "file_path"),
            get_value(finding, "line_number"),
            get_value(finding, "title")
        )

        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)

    return unique_findings


def prioritize_findings(findings: list) -> list:
    """Sort findings from highest to lowest severity."""

    severity_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
        "info": 4
    }

    return sorted(
        findings,
        key=lambda finding: severity_order.get(
            get_value(finding, "severity", "info"),
            5
        )
    )
