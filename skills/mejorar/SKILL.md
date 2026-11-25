---
name: mejorar
description: Automejora del plugin. Analiza el historial de corridas de /orquestar y los aprendizajes de los proyectos, detecta patrones que se repiten y propone cambios con evidencia a las propias skills y agentes del plugin. Solo aplica lo que el usuario aprueba. Usar cuando el usuario pide /mejorar, "mejorá el plugin", "qué aprendió el orquestador".
---

# Mejorar

Tu trabajo es **mejorar el plugin a partir de evidencia**, no a partir de opiniones. Cada cambio que propongas tiene que apoyarse en corridas reales.

Entrada: $ARGUMENTS (opcional: `--min N` para cambiar el mínimo de corridas, o un foco como `implementer`, `presupuesto`, `entrevista`).

Formatos de memoria: leé `../orquestar/memoria.md`.

## 1. Ubicar el repo fuente

**Nunca edites la copia instalada** (`~/.claude/plugins/cache/...`): se pisa en cada update.

- Leé `~/.claude/orquestador/config.json` → campo `repo_fuente`.
- Si no existe, preguntale al usuario la ruta del repo del plugin, verificá que tenga `.claude-plugin/plugin.json` con `"name": "orquestador"` y guardala en `config.json`.

## 2. Juntar evidencia

- `~/.claude/orquestador/historial.jsonl` completo.
- `~/.claude/orquestador/eventos.jsonl` (un registro por subagente, escrito por el hook): modelo real, turnos, herramientas y tokens por agente.
- `~/.claude/orquestador/mejoras.md` (corridas anteriores de esta skill: qué se cambió y cuándo).
- Los `aprendizajes.md` de los proyectos del historial: buscá la ruta de cada `proyecto_id` en `config.json` → `proyectos` (`<ruta>/.claude/orquestador/aprendizajes.md`). Si no está en el índice, preguntale al usuario o seguí sin ese.

**Agrupá por `proyecto_id`, no por nombre**: dos carpetas con el mismo nombre pueden ser proyectos distintos, y la misma copia con otro nombre (`app`, `app-187`) es el mismo proyecto. Líneas viejas sin `proyecto_id` agrupalas por nombre y decilo.

**Mínimo de datos:** 5 corridas (o `--min N`). Con menos, mostrá un resumen de lo que hay y pará: con poca evidencia se sacan conclusiones de casos aislados.

## 3. Buscar patrones

Hacelo vos, sin agentes (es poco texto). Un patrón cuenta si aparece en **3+ corridas o en 2+ proyectos**:

| Señal | Posible cambio en el plugin |
|---|---|
| `bloqueos` altos en tareas con muchos archivos | regla de partición en Fase 3 de `orquestar` |
| `presupuesto_excedido` seguido | ajustar presupuesto por defecto o cómo se estima |
| el mismo **patrón evitable** del reviewer en varios proyectos | regla general en `agents/implementer.md` |
| la misma convención/trampa en `aprendizajes.md` de 2+ proyectos | promoverla al agente o skill correspondiente |
| `tamaño_estimado` sistemáticamente bajo | criterios de tamaño en `triage` |
| `hallazgos_reviewer` en 0 casi siempre | considerar un modelo más barato en `agents/reviewer.md` para tareas chicas (ahorro de quota) |
| en `eventos.jsonl`, un agente corre con un `modelo` distinto al de su archivo | algo pisa la configuración (prompt de una skill, env var): encontrarlo |
| explorers con muchos `turnos`/`tokens_in` | preguntas demasiado amplias: regla en Fase 2 de `orquestar` |
| `tests: sin_tests` frecuente | que `especificar` pregunte por verificación más temprano |

También compará con `mejoras.md`: si un cambio anterior no movió la métrica que buscaba, proponé revertirlo.

## 4. Proponer

Presentá **máximo 3 propuestas**, de mayor a menor impacto:

```
### 1. <título>
Evidencia: 4 de 9 corridas (proyectos: a, b) — <qué muestran los datos>
Cambio: <archivo> — diff
Métrica a mirar: <qué debería mejorar en el historial>
Riesgo: <qué podría empeorar>
```

Si no hay patrones con suficiente evidencia, decilo y no inventes propuestas.

## 5. Aplicar (solo lo aprobado)

1. Editá los archivos en el repo fuente.
2. Subí la versión *minor* en `.claude-plugin/plugin.json`.
3. Agregá la entrada en `CHANGELOG.md` del repo, con la evidencia resumida.
4. Agregá a `~/.claude/orquestador/mejoras.md`: fecha, versión, cambio, métrica a mirar, cantidad de corridas en el historial a esa fecha.
5. Decile al usuario que actualice con `/plugin marketplace update claude-orquestador`. No hagas commit ni push salvo que lo pida.
