import asyncio
from app.core.agent_config import create_groq_client


async def main():
    client = create_groq_client()

    response = await client.get_response(
        "Reply with exactly: Groq connection successful."
    )

    print("Groq response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())