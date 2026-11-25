# claude-orquestador

Plugin de Claude Code para orquestar subagentes **sin quemar la quota**, y que **aprende de cada corrida**.

```
/triage  →  /especificar <issue confuso>  →  /orquestar <spec o tarea>  →  (cada tanto) /mejorar
```

## Qué resuelve

Delegar en subagentes es potente, pero por defecto heredan el modelo más caro, nadie controla cuántos se lanzan y cada sesión empieza de cero. Este plugin:

- **Controla costo**: cada agente tiene un modelo fijo (haiku para leer, sonnet para implementar, opus solo para la revisión final) y un presupuesto que se aprueba antes de ejecutar.
- **Entiende antes de hacer**: entrevista estilo *grill*, una pregunta por vez con respuesta recomendada, hasta tener criterios de aceptación verificables.
- **Aprende**: guarda convenciones, trampas y comandos de verificación por proyecto, y métricas de cada corrida.
- **Se mejora a sí mismo**: `/mejorar` detecta patrones entre corridas y propone cambios al propio plugin, con evidencia.

## Comandos

| Comando | Qué hace |
|---|---|
| `/triage [github \| #3 #7 \| label:bug \| archivo]` | Ordena issues: tamaño, claridad, solapamientos, orden sugerido. No implementa. |
| `/especificar <idea \| #issue>` | Entrevista y guarda la spec en `.claude/specs/<slug>.md`. No implementa. |
| `/especificar nuevo <idea>` | Proyecto desde cero: `proyecto.md` + una spec por hito. |
| `/orquestar <tarea \| spec>` | Memoria → entrevista → exploración → plan aprobado → ejecución → revisión → retro. |
| `/mejorar` | Analiza el historial y propone mejoras al plugin. |

Agentes: `explorer` (haiku, solo lectura) · `implementer` (sonnet) · `reviewer` (opus, solo lectura).

Hook: `SubagentStop` → `hooks/registrar.py` anota cada subagente del plugin (modelo real, turnos, tokens) en `~/.claude/orquestador/eventos.jsonl`. Requiere `python3`; sin él, el plugin funciona igual pero las métricas las estima la retro.

## Cómo aprende

```
           ┌──────────── lee ─────────────┐
           ▼                              │
  /orquestar ──► implementers ──► reviewer ──► Fase 6: retro
                    │ "aprendizaje        │ "patrón          │
                    │  candidato"         │  evitable"       │
                    └─────────────────────┴──────────────────┤
                                                             ▼
                          .claude/orquestador/aprendizajes.md   (por proyecto, aprobado por vos)
                          ~/.claude/orquestador/historial.jsonl (métricas, todos los proyectos)
                                                             │
                                          /mejorar ◄─────────┘
                                             │  patrones en 3+ corridas o 2+ proyectos
                                             ▼
                                   diffs a skills/ y agents/ del plugin (aprobados por vos)
```

Dos ciclos:

1. **Por proyecto (cada corrida).** La retro propone 0-3 aprendizajes *generalizables* (no detalles de la tarea), con su origen. Se escriben solo si los aprobás. Tope de ~60 líneas para que no se llene de ruido. La próxima corrida los lee antes de preguntar o explorar, y cada implementer recibe solo los que aplican a su tarea.
2. **Del plugin (cada ~10 corridas).** `/mejorar` cruza historial y aprendizajes de varios proyectos. Si el mismo error aparece en distintos repos, lo convierte en una regla del agente; si los presupuestos se exceden seguido, ajusta la estimación. Cada cambio queda registrado con la métrica que debería mover, y si no la mueve, se propone revertirlo.

Principios: **evidencia antes que opinión**, **humano en el loop** para todo lo que cambia comportamiento, y **olvidar es parte de aprender** (los aprendizajes se reemplazan o se borran cuando el código los contradice).

Detalle de formatos: [`skills/orquestar/memoria.md`](skills/orquestar/memoria.md).

## Instalar

```
/plugin marketplace add mathitejeda/claude-orquestador
/plugin install orquestador@claude-orquestador
```

Desde una carpeta local:

```
/plugin marketplace add <ruta>/claude-orquestador
/plugin install orquestador@claude-orquestador
```

Actualizar: `/plugin marketplace update claude-orquestador`.

### Red de seguridad recomendada

Para que cualquier subagente sin modelo explícito no herede Opus, en `~/.claude/settings.json`:

```json
"env": { "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet" }
```

## Ajustar

- Modelos por agente: campo `model:` en `agents/*.md`. Es el **único** lugar: las skills no pasan `model` a los agentes del plugin, así que cambiarlo ahí alcanza (p. ej. cuando sale un modelo nuevo).
- Presupuesto y flujo: `skills/orquestar/SKILL.md`.
- Memoria: `skills/orquestar/memoria.md`.

## Próximos pasos

- Evals con `claude plugin eval` para que `/mejorar` valide que un cambio no empeora nada antes de proponerlo.
- Arranque en frío de `/mejorar`: con 1-4 corridas, mostrar "qué aprendió" sin proponer cambios.

Ver [CHANGELOG](CHANGELOG.md).
