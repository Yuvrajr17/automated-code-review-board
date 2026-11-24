
import asyncio

from app.agents.security_agent.agent import create_security_agent


async def main():
    agent = create_security_agent()

    sample_code = """
password = "admin123"
result = eval(user_input)
data = pickle.loads(user_data)
response = requests.get(url, verify=False)
hash_value = hashlib.md5(data)
"""

    response = await agent.run(
        f"""
        Review the following Python code for security issues.

        Code:
        {sample_code}
        """
    )

    print("\nSECURITY AGENT REPORT:\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
