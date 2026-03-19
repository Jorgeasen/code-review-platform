from core.agent_base import AgentBase


class StyleAgent(AgentBase):
    def run(self, context: dict) -> dict:
        file_paths = context.get("changed_files", [])
        lint_result = self.use_skill("pylint", file_paths=file_paths)
        format_ok = self.use_skill("black_check", file_paths=file_paths)
        complexity_result = self.use_skill("complexity_check", file_paths=file_paths)

        return {
            "agent": self.name,
            "lint_score": lint_result.score,
            "lint_issues": lint_result.issues,
            "formatting_ok": format_ok,
            "avg_complexity": complexity_result.average_complexity,
            "complex_fns": complexity_result.complex_functions,
            "passed": (
                lint_result.passed
                and format_ok
                and complexity_result.passed
            ),
        }
