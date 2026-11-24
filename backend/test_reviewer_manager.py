
from app.agents.reviewer_manager.tools import (
    remove_duplicate_findings,
    prioritize_findings
)

findings = [
    {
        "agent_name": "SecurityAgent",
        "file_path": "app.py",
        "line_number": 10,
        "severity": "high",
        "title": "Hardcoded password"
    },
    {
        "agent_name": "StyleAgent",
        "file_path": "app.py",
        "line_number": 5,
        "severity": "low",
        "title": "Unused variable"
    },
    {
        "agent_name": "SecurityAgent",
        "file_path": "app.py",
        "line_number": 10,
        "severity": "high",
        "title": "Hardcoded password"
    }
]

unique = remove_duplicate_findings(findings)
prioritized = prioritize_findings(unique)

print("Unique findings:", len(unique))
print("Prioritized findings:")

for finding in prioritized:
    print(finding["severity"], "-", finding["title"])
