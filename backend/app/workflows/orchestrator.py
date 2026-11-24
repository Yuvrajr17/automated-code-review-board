from app.agents.test_coverage_agent.tools import (
    identify_test_files,
    analyze_test_changes
)

from app.agents.security_agent.tools import (
    detect_sensitive_patterns,
    detect_insecure_python_apis
)

from app.agents.style_agent.tools import (
    extract_python_source,
    run_ruff_analysis
)

from app.agents.diff_agent.agent import create_diff_agent
from app.agents.diff_agent.tools import (
    extract_changed_files,
    count_diff_changes
)

from app.agents.style_agent.agent import create_style_agent
from app.agents.security_agent.agent import create_security_agent
from app.agents.test_coverage_agent.agent import create_test_coverage_agent
from app.agents.reviewer_manager.agent import create_reviewer_manager


async def run_code_review(diff_text: str, repository_name: str):
    """
    Run the complete multi-agent code review workflow.

    1. Execute deterministic diff analysis using Python tools.
    2. Diff Agent summarizes the changes.
    3. Run specialist agents sequentially.
    4. Reviewer Manager consolidates all reports.
    """

    # Step 1: Execute Python tools directly
    changed_files = extract_changed_files(diff_text)
    change_counts = count_diff_changes(diff_text)

    print("Python tools executed successfully.")
    print("Changed files:", changed_files)
    print("Change counts:", change_counts)

    # Step 2: Create agents
    diff_agent = create_diff_agent()
    style_agent = create_style_agent()
    security_agent = create_security_agent()
    test_agent = create_test_coverage_agent()
    reviewer_manager = create_reviewer_manager()

    # Step 3: Run Diff Agent
    diff_response = await diff_agent.run(
        f"""
        Analyze the following Git diff.

        Repository: {repository_name}

        Results from Python analysis tools:

        Modified files:
        {changed_files}

        Added lines:
        {change_counts["added_lines"]}

        Deleted lines:
        {change_counts["deleted_lines"]}

        Git diff:
        {diff_text}
        """
    )

    diff_report = (
        diff_response.text
        or "Diff Agent did not generate a text report."
    )

    
    # Step 4: Execute Style Agent Python tools directly
    python_source = extract_python_source(diff_text)
    ruff_findings = run_ruff_analysis(python_source)

    print("Style Agent Python tools executed.")
    print("Python source extracted:", bool(python_source))
    print("Ruff findings:", ruff_findings)

        # Run Style Agent using the Python tool results

    if python_source.strip():
        style_analysis = f"""
        Python source was extracted.

        Ruff analysis results:
        {ruff_findings}

        Explain the detected style and code-quality issues.
        Do not invent issues beyond the supplied results.
        """
    else:
        style_analysis = """
        No Python source was found in the changed files.
        Ruff analysis was skipped.
        Explain that Python-specific style analysis was not applicable.
        """

    style_response = await style_agent.run(
        f"""
        Review the coding style and readability of this repository change.

        Repository: {repository_name}

        Static analysis results:
        {style_analysis}
        """
    )

    style_report = (
        style_response.text or "No style report generated."
    )

    print("Style Agent completed successfully.")

    
    # Step 5: Execute Security Agent Python tools directly

    # Analyze only newly added lines, not diff metadata or removed code.
    added_code_lines = []

    for line in diff_text.splitlines():
        if line.startswith(("+++", "---", "@@", "diff ", "index ")):
            continue

        if line.startswith("+"):
            added_code_lines.append(line[1:])

    added_source_code = "\n".join(added_code_lines)

    sensitive_findings = detect_sensitive_patterns(added_source_code)
    insecure_api_findings = detect_insecure_python_apis(added_source_code)

    security_findings = sensitive_findings + insecure_api_findings

    print("Security Agent Python tools executed.")
    print("Sensitive pattern findings:", sensitive_findings)
    print("Insecure API findings:", insecure_api_findings)

    # Step 6: Run Security Agent using compact tool results

    security_response = await security_agent.run(
        f"""
        Review the following results from the Python security tools.

        Repository: {repository_name}

        Security findings:
        {security_findings}

        If findings exist, explain their risks and recommend fixes.
        If no findings exist, clearly state that no matching patterns
        were detected.

        Do not invent findings.
        """
    )

    security_report = (
        security_response.text or "No security report generated."
    )


    # Step 6: Run Test-Coverage Agent
    
    # Step 7: Execute Test-Coverage Python tools directly

    test_files = identify_test_files(diff_text)

    test_analysis = analyze_test_changes(
        diff_text,
        test_files
    )

    print("Test-Coverage Python tools executed.")
    print("Identified test files:", test_files)
    print("Test analysis:", test_analysis)



    # Step 8: Run Test-Coverage Agent using compact results

    test_response = await test_agent.run(
        f"""
        Analyze the following test-coverage analysis.

        Repository: {repository_name}

        Identified test files:
        {test_files}

        Test change analysis:
        {test_analysis}

        Explain the testing changes and potential gaps.
        Do not invent findings or claim tests were executed.
        """
    )

    test_report = (
        test_response.text or "No test coverage report generated."
    )


    # Step 7: Consolidate all reports
    final_response = await reviewer_manager.run(
        f"""
        You are reviewing repository: {repository_name}

        DIFF AGENT REPORT:
        {diff_report}

        STYLE AGENT REPORT:
        {style_report}

        SECURITY AGENT REPORT:
        {security_report}

        TEST-COVERAGE AGENT REPORT:
        {test_report}

        Consolidate these reports.

        Remove duplicate findings.
        Prioritize issues by severity.
        Provide a final recommendation:
        approve or request_changes.

        Do not invent findings.
        """
    )

    return {
        "repository_name": repository_name,
        "diff_report": diff_report,
        "style_report": style_report,
        "security_report": security_report,
        "test_report": test_report,
        "final_report": final_response.text
    }
