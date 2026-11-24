
import re

from app.database.connection import db_connection
from app.workflows.orchestrator import run_code_review


async def execute_review(repository_name: str, diff_text: str):

    # Step 1: Create review record
    with db_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO reviews (
                repository_name,
                diff_text,
                status
            )
            VALUES (?, ?, ?)
            """,
            (repository_name, diff_text, "processing")
        )

        review_id = cursor.lastrowid

    try:
        # Step 2: Execute multi-agent workflow
        result = await run_code_review(
            repository_name=repository_name,
            diff_text=diff_text
        )

        # Step 3: Save individual agent reports
        reports = {
            "DiffAgent": result["diff_report"],
            "StyleAgent": result["style_report"],
            "SecurityAgent": result["security_report"],
            "TestCoverageAgent": result["test_report"],
            "ReviewerManager": result["final_report"]
        }

        with db_connection() as connection:

            for agent_name, output in reports.items():
                connection.execute(
                    """
                    INSERT INTO agent_logs (
                        review_id,
                        agent_name,
                        status,
                        output
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (review_id, agent_name, "completed", output)
                )

            # Step 4: Determine recommendation
            final_report = result["final_report"].lower()

            recommendation = (
                "request_changes"
                if re.search(r"\brequest_changes\b|\brequest changes\b", final_report)
                else "approve"
            )

            # Step 5: Update review
            connection.execute(
                """
                UPDATE reviews
                SET status = ?,
                    recommendation = ?,
                    summary = ?
                WHERE id = ?
                """,
                (
                    "completed",
                    recommendation,
                    result["final_report"],
                    review_id
                )
            )

        return {
            "review_id": review_id,
            "repository_name": repository_name,
            "status": "completed",
            "recommendation": recommendation,
            "final_report": result["final_report"]
        }

    except Exception:
        with db_connection() as connection:
            connection.execute(
                """
                UPDATE reviews
                SET status = ?
                WHERE id = ?
                """,
                ("failed", review_id)
            )

        raise
