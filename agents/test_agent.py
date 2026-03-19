from core.agent_base import AgentBase


class TestAgent(AgentBase):
    def run(self, context: dict) -> dict:
        test_result = self.use_skill("pytest")
        return {
            "agent": self.name,
            "passed": test_result.passed,
            "failed": test_result.failed,
            "errors": test_result.errors,
            "output": test_result.output,
            "success": test_result.success,
        }
