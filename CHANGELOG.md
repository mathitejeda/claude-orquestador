# Changelog

## 0.4.0 — 2026-11-20

Memoria y automejora.

- **Memoria por proyecto**: `/orquestar`, `/especificar` y `/triage` leen `.claude/orquestador/aprendizajes.md` (comandos de verificación, convenciones, trampas, calibración) antes de preguntar o explorar.
- **Fase 6 — Retro** en `/orquestar`: compara plan vs. realidad, propone 0-3 aprendizajes que el usuario aprueba y registra métricas en `~/.claude/orquestador/historial.jsonl`.
- **Implementer** respeta los aprendizajes que recibe y reporta *aprendizajes candidatos*.
- **Reviewer** marca *patrones evitables* con la regla que los habría prevenido.
- **`/triage`** calibra estimaciones de tamaño con el historial del proyecto.
- **Nueva skill `/mejorar`**: detecta patrones entre corridas y proyectos y propone cambios con evidencia al propio plugin.

## 0.3.0

- `/triage`, `/especificar` (incluye `nuevo` para proyectos desde cero) y `/orquestar`.
- Agentes `explorer` (haiku), `implementer` (sonnet), `reviewer` (opus).
