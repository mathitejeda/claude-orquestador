# Changelog

## 0.5.0 — 2026-11-24

Métricas confiables y modelos configurables en un solo lugar.

- **Modelos**: las skills ya no pasan `model` a los agentes del plugin; manda el `model:` de `agents/*.md`. Antes la tabla de `orquestar` lo pisaba y cambiar el archivo no tenía efecto. `model` explícito solo en el fallback a agentes genéricos.
- **Hook `SubagentStop`** (`hooks/registrar.py`): registra cada subagente del plugin en `~/.claude/orquestador/eventos.jsonl` con el modelo real, turnos, herramientas y tokens. La retro cuenta agentes desde ahí en lugar de estimarlos.
- **`proyecto_id`**: hash del remote `origin` (o de la ruta si no hay remote). Distingue carpetas con el mismo nombre y une copias del mismo repo. `triage` y `mejorar` agrupan por id.
- **Índice local** `config.json` → `proyectos`: `/mejorar` encuentra los `aprendizajes.md` sin asumir `~/dev/<proyecto>`.
- `/mejorar` detecta agentes que corren con un modelo distinto al configurado y explorers demasiado caros.

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
