import subprocess
import json
from dataclasses import dataclass


@dataclass
class LintResult:
    score: float
    issues: list[str]
    passed: bool


def run_pylint(file_paths: list[str]) -> LintResult:
    """Ejecuta pylint sobre los ficheros indicados."""
    result = subprocess.run(
        ["pylint", "--output-format=json", *file_paths],
        capture_output=True,
        text=True,
    )
    try:
        issues_data = json.loads(result.stdout)
        issues = [
            f"{i['path']}:{i['line']} - {i['message']}" for i in issues_data
        ]
    except (json.JSONDecodeError, KeyError):
        issues = []

    score = 0.0
    for line in result.stderr.splitlines():
        if "Your code has been rated at" in line:
            try:
                score = float(line.split("at ")[1].split("/")[0])
            except (IndexError, ValueError):
                pass

    return LintResult(score=score, issues=issues, passed=score >= 7.0)


def run_black_check(file_paths: list[str]) -> bool:
    """Devuelve True si el código ya está formateado con black."""
    result = subprocess.run(
        ["black", "--check", *file_paths], capture_output=True
    )
    return result.returncode == 0
