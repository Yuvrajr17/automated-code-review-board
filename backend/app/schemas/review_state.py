
from typing import Literal

from pydantic import BaseModel, Field


class Finding(BaseModel):
    agent_name: str

    file_path: str | None = None
    line_number: int | None = None

    severity: Literal[
        "critical",
        "high",
        "medium",
        "low",
        "info"
    ]

    title: str
    description: str
    suggestion: str | None = None


class ChangeState(BaseModel):
    review_id: int | None = None

    repository_name: str
    diff_text: str

    changed_files: list[str] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)

    agent_status: dict[str, str] = Field(default_factory=dict)

    final_summary: str | None = None

    recommendation: Literal[
        "approve",
        "request_changes"
    ] | None = None
