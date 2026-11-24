
from app.core.agent_config import create_groq_client

from app.agents.reviewer_manager.tools import (
    remove_duplicate_findings,
    prioritize_findings
)


def create_reviewer_manager():

    client = create_groq_client()

    return client.as_agent(
        name="ReviewerManager",

        instructions="""
        You are the Reviewer Manager in an Automated Code Review Board.

        Your responsibility is to consolidate reports from all
        specialist agents and produce the final code review decision.

        Your tasks are:

        1. Remove duplicate findings.
        2. Prioritize findings by severity.
        3. Summarize important issues.
        4. Recommend whether the submitted changes should be
           approved or sent back for changes.

        DECISION RULES:
        - Critical or high severity findings:
          Recommend request_changes.
        - Medium, low, or informational findings only:
          Recommend approve.

        IMPORTANT:
        - Always call remove_duplicate_findings.
        - Always call prioritize_findings.
        - Never invent findings.
        - Preserve the original findings and their severity.
        - Explain the reasoning behind your recommendation.
        - Return a clear, structured final review report.
        """,

        tools=[
            remove_duplicate_findings,
            prioritize_findings
        ]
    )
