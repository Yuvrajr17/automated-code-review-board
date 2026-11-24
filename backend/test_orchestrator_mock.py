
import asyncio
from types import SimpleNamespace
from unittest.mock import patch

import app.workflows.orchestrator as workflow


execution_order = []


class FakeAgent:
    def __init__(self, name):
        self.name = name

    async def run(self, prompt):
        execution_order.append(self.name)
        return SimpleNamespace(
            text=f"{self.name} mock report generated successfully."
        )


async def main():
    with (
        patch.object(
            workflow, "create_diff_agent",
            return_value=FakeAgent("DiffAgent")
        ),
        patch.object(
            workflow, "create_style_agent",
            return_value=FakeAgent("StyleAgent")
        ),
        patch.object(
            workflow, "create_security_agent",
            return_value=FakeAgent("SecurityAgent")
        ),
        patch.object(
            workflow, "create_test_coverage_agent",
            return_value=FakeAgent("TestCoverageAgent")
        ),
        patch.object(
            workflow, "create_reviewer_manager",
            return_value=FakeAgent("ReviewerManager")
        )
    ):
        result = await workflow.run_code_review(
            diff_text="Sample Git diff",
            repository_name="Demo Repository"
        )

    print("Execution order:", execution_order)
    print("\nFinal report:")
    print(result["final_report"])

    assert execution_order[0] == "DiffAgent"
    assert execution_order[-1] == "ReviewerManager"
    assert len(execution_order) == 5

    print("\nOrchestration test passed!")


if __name__ == "__main__":
    asyncio.run(main())
