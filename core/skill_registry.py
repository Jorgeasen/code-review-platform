from typing import Callable


class SkillRegistry:
    """Registro central de skills disponibles en el sistema."""

    def __init__(self):
        self._skills: dict[str, Callable] = {}

    def register(self, name: str, fn: Callable):
        self._skills[name] = fn

    def get(self, name: str) -> Callable:
        if name not in self._skills:
            raise ValueError(f"Skill '{name}' no registrada")
        return self._skills[name]

    def list_skills(self) -> list[str]:
        return list(self._skills.keys())


registry = SkillRegistry()
