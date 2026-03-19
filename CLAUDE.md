# Code Review Platform

## Proyecto
Sistema de revisión automática de PRs usando agentes IA orquestados.

## Arquitectura
- agents/   → lógica de cada agente (orquestador + especializados)
- skills/   → herramientas atómicas reutilizables sin estado
- hooks/    → manejadores de eventos del sistema
- core/     → infraestructura base (bus de eventos, registro de skills)
- .github/  → workflows de CI/CD

## Comandos útiles
- `uv run python -m agents.orchestrator`  → lanza el orquestador
- `uv run pytest`                          → ejecuta los tests
- `uv run black .`                         → formatea el código
- `uv run pylint agents/ skills/ hooks/`   → análisis estático

## Convenciones
- Cada agente hereda de AgentBase (core/agent_base.py)
- Las skills son funciones puras sin estado, registradas en SkillRegistry
- Los hooks se suscriben al EventBus mediante bus.subscribe()
- Variables de entorno cargadas desde .env (nunca hardcodear claves)
