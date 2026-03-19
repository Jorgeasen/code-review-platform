import subprocess
from dataclasses import dataclass


@dataclass
class TestResult:
    passed: int
    failed: int
    errors: int
    output: str
    success: bool


def run_pytest(test_paths: list[str] | None = None) -> TestResult:
    """Ejecuta pytest y devuelve un resumen de resultados."""
    cmd = ["pytest", "--tb=short", "-q", *(test_paths or [])]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    passed = failed = errors = 0
    for line in output.splitlines():
        if " passed" in line:
            try:
                passed = int(line.strip().split()[0])
            except (IndexError, ValueError):
                pass
        if " failed" in line:
            try:
                failed = int(line.strip().split()[0])
            except (IndexError, ValueError):
                pass
        if " error" in line:
            try:
                errors = int(line.strip().split()[0])
            except (IndexError, ValueError):
                pass

    return TestResult(
        passed=passed,
        failed=failed,
        errors=errors,
        output=output[:2000],
        success=failed == 0 and errors == 0,
    )
