import asyncio
from app.agents.diff_agent.agent import create_diff_agent


sample_diff = """
diff --git a/main.py b/main.py
index 1234567..abcdefg 100644
--- a/main.py
+++ b/main.py
@@ -1,3 +1,4 @@
 def hello():
-    print("Hello")
+    print("Hello World")
+    print("Welcome")
"""


async def main():

    agent = create_diff_agent()

    response = await agent.run(
        f"Analyze this Git diff:\n{sample_diff}"
    )

    print("\n===== DIFF AGENT REPORT =====\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())