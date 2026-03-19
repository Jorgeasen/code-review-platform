from core.agent_base import AgentBase


class SecurityAgent(AgentBase):
    def run(self, context: dict) -> dict:
        file_paths = context.get("changed_files", [])
        diff = context.get("diff", "")

        sec_result = self.use_skill("bandit", file_paths=file_paths)
        ai_review = self.use_skill("claude_review", diff=diff, context="security review")

        return {
            "agent": self.name,
            "high_issues": sec_result.high,
            "medium_issues": sec_result.medium,
            "low_issues": sec_result.low,
            "bandit_issues": sec_result.issues,
            "ai_review": ai_review,
            "passed": sec_result.passed,
        }
