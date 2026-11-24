import asyncio
from app.core.agent_config import create_gemini_client


# A simple Python function exposed as an agent tool
def get_project_status() -> str:
    """Return the current development status of the project."""
    return "Automated Code Review Board backend setup is complete."


async def main():
    client = create_gemini_client()

    agent = client.as_agent(
        name="GeminiTestAgent",
        instructions=(
            "You are a helpful assistant. "
            "Use the available Python tool when asked about project status."
        ),
        tools=[get_project_status]
    )

    response = await agent.run(
        "Call the project status tool and tell me its result."
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())