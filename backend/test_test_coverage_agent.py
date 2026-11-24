
import asyncio

from app.agents.test_coverage_agent.agent import (
    create_test_coverage_agent
)


sample_diff = """
diff --git a/app.py b/app.py
index 1234567..abcdefg 100644
--- a/app.py
+++ b/app.py
@@ -1,2 +1,3 @@
 def add(a, b):
+    return a + b

diff --git a/tests/test_app.py b/tests/test_app.py
new file mode 100644
--- /dev/null
+++ b/tests/test_app.py
@@ -0,0 +1,3 @@
+def test_add():
+    assert add(2, 3) == 5
"""


async def main():

    agent = create_test_coverage_agent()

    response = await agent.run(
        f"Analyze test coverage changes in this Git diff:\n{sample_diff}"
    )

    print("\n===== TEST-COVERAGE AGENT REPORT =====\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
