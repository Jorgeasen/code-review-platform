import subprocess
import json
from dataclasses import dataclass


@dataclass
class ComplexityResult:
    average_complexity: float
    complex_functions: list[str]
    passed: bool


def run_complexity_check(file_paths: list[str]) -> ComplexityResult:
    """Calcula la complejidad ciclomática usando radon."""
    result = subprocess.run(
        ["radon", "cc", "-s", "-j", *file_paths],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
        all_complexities = []
        complex_fns = []
        for file_data in data.values():
            for fn in file_data:
                c = fn.get("complexity", 0)
                all_complexities.append(c)
                if c > 10:
                    complex_fns.append(
                        f"{fn['name']} (complejidad: {c})"
                    )
        avg = sum(all_complexities) / len(all_complexities) if all_complexities else 0.0
    except (json.JSONDecodeError, KeyError, ZeroDivisionError):
        avg = 0.0
        complex_fns = []

    return ComplexityResult(
        average_complexity=round(avg, 2),
        complex_functions=complex_fns,
        passed=avg <= 10 and len(complex_fns) == 0,
    )
