
import asyncio
from app.workflows.orchestrator import run_code_review


sample_diff = """
diff --git a/app.py b/app.py
index 1234567..abcdefg 100644
--- a/app.py
+++ b/app.py
@@ -1,3 +1,7 @@
+password = "admin123"
+
+def process_input(user_input):
+    return eval(user_input)
+
"""

async def main():
    print("\\nStarting Automated Code Review...\\n")

    result = await run_code_review(
        diff_text=sample_diff,
        repository_name="Demo Repository"
    )

    print("\\n========== DIFF AGENT ==========")
    print(result["diff_report"])

    print("\\n========== STYLE AGENT ==========")
    print(result["style_report"])

    print("\\n========== SECURITY AGENT ==========")
    print(result["security_report"])

    print("\\n========== TEST-COVERAGE AGENT ==========")
    print(result["test_report"])

    print("\\n========== FINAL REVIEW ==========")
    print(result["final_report"])


if __name__ == "__main__":
    asyncio.run(main())
