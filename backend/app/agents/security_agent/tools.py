
import re


def detect_sensitive_patterns(source_code: str) -> list[dict]:
    """
    Detect potentially sensitive credentials and dangerous code patterns.
    """

    patterns = {
        "Hardcoded credential": (
            r"""(?i)(password|api_key|secret|token)\s*=\s*["'][^"']+["']"""
        ),
        "Use of eval()": r"\beval\s*\(",
        "Use of exec()": r"\bexec\s*\(",
        "Potential SQL injection": (
            r"""(?i)(execute|executemany)\s*\(\s*f?["'][^"']*%s"""
        ),
        "Unsafe shell execution": (
            r"""(?i)subprocess\.(run|call|Popen)\s*\([^)]*shell\s*=\s*True"""
        ),
    }

    findings = []

    for title, pattern in patterns.items():
        for match in re.finditer(pattern, source_code):
            line_number = source_code.count("\n", 0, match.start()) + 1

            findings.append({
                "title": title,
                "line_number": line_number,
                "matched_code": match.group()
            })

    return findings


def detect_insecure_python_apis(source_code: str) -> list[dict]:
    """
    Detect additional potentially insecure Python APIs and configurations.
    """

    patterns = {
        "Unsafe pickle deserialization": r"\bpickle\.loads?\s*\(",
        "Potentially unsafe YAML loading": r"\byaml\.load\s*\(",
        "Weak MD5 hashing": r"\bhashlib\.md5\s*\(",
        "Weak SHA1 hashing": r"\bhashlib\.sha1\s*\(",
        "TLS certificate verification disabled": r"\bverify\s*=\s*False\b",
        "Debug mode enabled": r"\bdebug\s*=\s*True\b",
    }

    findings = []

    for title, pattern in patterns.items():
        for match in re.finditer(pattern, source_code):
            line_number = source_code.count("\n", 0, match.start()) + 1

            findings.append({
                "title": title,
                "line_number": line_number,
                "matched_code": match.group()
            })

    return findings
