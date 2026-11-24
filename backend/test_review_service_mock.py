
import asyncio
from unittest.mock import patch

from app.workflows.review_service import execute_review
from app.database.connection import db_connection


async def fake_review_workflow(repository_name, diff_text):
    """Simulate reports from all five agents without Gemini."""

    return {
        "repository_name": repository_name,
        "diff_report": "Found 2 changed files.",
        "style_report": "One style issue detected.",
        "security_report": "No security issues detected.",
        "test_report": "No test-file changes detected.",
        "final_report": (
            "Final recommendation: request_changes. "
            "Please fix the style issue."
        )
    }


async def main():

    with patch(
        "app.workflows.review_service.run_code_review",
        side_effect=fake_review_workflow
    ):

        result = await execute_review(
            repository_name="Demo Repository",
            diff_text="Sample Git diff for testing"
        )

    print("\nReview creation result:")
    print(result)

    review_id = result["review_id"]

    # Verify review was saved
    with db_connection() as connection:

        review = connection.execute(
            "SELECT * FROM reviews WHERE id = ?",
            (review_id,)
        ).fetchone()

        logs = connection.execute(
            "SELECT * FROM agent_logs WHERE review_id = ?",
            (review_id,)
        ).fetchall()

    assert review is not None
    assert review["status"] == "completed"
    assert review["recommendation"] == "request_changes"
    assert len(logs) == 5

    print("\nSaved review:", dict(review))
    print("\nAgent logs saved:", len(logs))
    print("\nMock review persistence test passed!")


if __name__ == "__main__":
    asyncio.run(main())
