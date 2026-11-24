import asyncio
from app.agents.style_agent.agent import create_style_agent


sample_diff = """
diff --git a/main.py b/main.py
index 1234567..abcdefg 100644
--- a/main.py
+++ b/main.py
@@ -1,2 +1,3 @@
+import os
+x=10
+print("Hello")
"""


async def main():

    agent = create_style_agent()

    response = await agent.run(
        f"Analyze the coding style of this Git diff:\n{sample_diff}"
    )

    print("\n===== STYLE AGENT REPORT =====\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())