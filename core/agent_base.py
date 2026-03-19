from abc import ABC, abstractmethod

from core.skill_registry import SkillRegistry


class AgentBase(ABC):
    def __init__(self, name: str, registry: SkillRegistry):
        self.name = name
        self.registry = registry

    @abstractmethod
    def run(self, context: dict) -> dict:
        """Ejecuta el agente con el contexto dado y devuelve resultados."""
        ...

    def use_skill(self, skill_name: str, **kwargs):
        return self.registry.get(skill_name)(**kwargs)
