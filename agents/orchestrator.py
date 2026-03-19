import json
import os

import anthropic
from dotenv import load_dotenv

from core.skill_registry import SkillRegistry
from agents.style_agent import StyleAgent
from agents.security_agent import SecurityAgent
from agents.test_agent import TestAgent
from skills.linting import run_pylint, run_black_check
from skills.security_scan import run_bandit
from skills.test_runner import run_pytest
from skills.claude_review import review_code_with_claude
from skills.complexity_check import run_complexity_check

load_dotenv()


class Orchestrator:
    """Agente principal que coordina a los sub-agentes via Claude API."""

    def __init__(self):
        self.registry = SkillRegistry()
        self._register_skills()
        self.agents = {
            "style": StyleAgent("StyleAgent", self.registry),
            "security": SecurityAgent("SecurityAgent", self.registry),
            "tests": TestAgent("TestAgent", self.registry),
        }
        self.client = anthropic.Anthropic()

    def _register_skills(self):
        self.registry.register("pylint", run_pylint)
        self.registry.register("black_check", run_black_check)
        self.registry.register("bandit", run_bandit)
        self.registry.register("pytest", run_pytest)
        self.registry.register("claude_review", review_code_with_claude)
        self.registry.register("complexity_check", run_complexity_check)

    def decide_agents(self, pr_context: dict) -> list[str]:
        """Claude decide qué agentes son relevantes para este PR."""
        response = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""Dado este PR, decide qué agentes de revisión activar.

PR title: {pr_context.get('title', '')}
Files changed: {pr_context.get('changed_files', [])}
Labels: {pr_context.get('labels', [])}

Responde SOLO con una lista JSON de agentes a activar.
Agentes disponibles: ["style", "security", "tests"]
Ejemplo: ["style", "security"]""",
                }
            ],
        )
        return json.loads(response.content[0].text)

    def run(self, pr_context: dict) -> dict:
        agents_to_run = self.decide_agents(pr_context)
        results = {
            name: self.agents[name].run(pr_context)
            for name in agents_to_run
        }
        return self._aggregate_results(results)

    def _aggregate_results(self, results: dict) -> dict:
        summary_resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=600,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Genera un resumen ejecutivo en markdown de esta revisión de PR:\n"
                        + json.dumps(results, ensure_ascii=False, indent=2)
                    ),
                }
            ],
        )
        return {
            "individual_results": results,
            "summary": summary_resp.content[0].text,
            "overall_passed": all(
                r.get("passed", r.get("success", True))
                for r in results.values()
            ),
        }
