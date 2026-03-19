import subprocess
import json
from dataclasses import dataclass


@dataclass
class SecurityResult:
    high: int
    medium: int
    low: int
    issues: list[str]
    passed: bool


def run_bandit(file_paths: list[str]) -> SecurityResult:
    """Ejecuta bandit para detectar vulnerabilidades de seguridad."""
    result = subprocess.run(
        ["bandit", "-r", "-f", "json", *file_paths],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
        results = data.get("results", [])
        high = sum(1 for r in results if r["issue_severity"] == "HIGH")
        medium = sum(1 for r in results if r["issue_severity"] == "MEDIUM")
        low = sum(1 for r in results if r["issue_severity"] == "LOW")
        issues = [
            f"{r['filename']}:{r['line_number']} [{r['issue_severity']}] {r['issue_text']}"
            for r in results
        ]
    except (json.JSONDecodeError, KeyError):
        high = medium = low = 0
        issues = []

    return SecurityResult(
        high=high,
        medium=medium,
        low=low,
        issues=issues,
        passed=high == 0 and medium == 0,
    )
