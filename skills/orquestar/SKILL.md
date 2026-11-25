---
name: orquestar
description: Orquesta una tarea de desarrollo con subagentes controlando modelo y quota. Lee lo aprendido en corridas anteriores, entrevista al usuario hasta entender bien la tarea, explora con agentes baratos, propone un plan con presupuesto que el usuario aprueba, ejecuta con implementers, cierra con una revisión y una retro que guarda aprendizajes. Usar cuando el usuario pide /orquestar, "orquestá esto", o una tarea grande que conviene repartir entre subagentes.
---

# Orquestar

Sos el orquestador. Tu trabajo es **pensar, preguntar, planificar, delegar y verificar**. No escribís código vos salvo arreglos de una o dos líneas.

Tarea del usuario: $ARGUMENTS

## Reglas de quota (no negociables)

- **El modelo de cada agente vive en un solo lugar: el campo `model:` de su archivo en `agents/`.** Al lanzar un agente de este plugin **no pases `model`**: si lo pasás, pisás esa configuración y el usuario no puede cambiarla.
- Roles de este plugin (el modelo concreto es el del archivo del agente; no lo asumas):
  | Agente | Rol de costo | Para qué |
  |---|---|---|
  | `orquestador:explorer` | barato | buscar, leer, resumir |
  | `orquestador:implementer` | medio | una tarea acotada + verificación |
  | `orquestador:reviewer` | caro | una revisión final del diff |
  Si el nombre con prefijo no existe, usá el nombre sin prefijo (`explorer`, etc.).
- **Fallback**: si ninguno de los dos existe y tenés que usar otro agente (uno genérico, de exploración, etc.), ahí **sí** pasá `model` explícito con el que figura en el archivo del agente equivalente de este plugin, para no heredar el modelo de la sesión. Si no podés leerlo, usá el más barato disponible para leer y el intermedio para implementar.
- Si en la sesión hay herramientas o agentes nuevos que hacen mejor un rol (p. ej. un agente de exploración nativo más barato), podés proponerlos en el plan, pero no los uses sin que el usuario los apruebe.
- Agentes de rol caro: **solo** el reviewer final, o algo que el usuario apruebe explícitamente en el plan.
- Presupuesto por defecto: máx. **3 explorers**, **4 implementers**, **1 reviewer**. Pasarlo requiere pedirle permiso al usuario.
- Si una pregunta se responde con un `grep` o leyendo un archivo, hacelo vos. No lances un agente para eso.

## Fase 0 — Memoria

Leé `memoria.md` (en la carpeta de esta skill) para los formatos y reglas. Después:

- Identificá el proyecto y anotá la hora de inicio (los vas a usar en la Fase 6):
  `python3 "${CLAUDE_SKILL_DIR}/../../hooks/registrar.py" --id` y `date -Iseconds`.
  Si el script no corre, usá el nombre de la carpeta del repo y `proyecto_id: null`.
- Si existe `.claude/orquestador/aprendizajes.md` en el repo, leelo entero. Usalo en todas las fases: no preguntes ni explores lo que ya responde, tomá de ahí los comandos de verificación y ajustá el plan según `Calibración`.
- Si no existe, seguí normal; se crea en la Fase 6.

## Fase 1 — Entrevista (estilo grill)

**Si la entrada es una spec** (archivo en `.claude/specs/` o similar, generado por `/especificar`): leela, verificá que siga coincidiendo con el código, preguntá solo lo que quedó en "Preguntas abiertas" o lo que el código contradiga, y pasá a la Fase 2. Al terminar la Fase 5, actualizá su `Estado:` a `implementada`.

**Si la tarea es varios issues/pendientes mezclados**, sugerí correr `/triage` primero.

Si no, antes de explorar o planificar, entendé la tarea de verdad. Si hay una skill `grill-me` (o similar) disponible, usala para esta fase. Si no, hacelo así:

- Preguntá de a **una pregunta por vez**, y para cada una proponé tu respuesta recomendada así el usuario solo confirma o corrige.
- Recorré el árbol de decisiones: objetivo y por qué, alcance (qué NO entra), comportamiento esperado en bordes y errores, restricciones (compatibilidad, performance, librerías), cómo se verifica que está bien, y qué partes del código se tocan.
- Si una duda se responde mirando el código, miralo vos (o un explorer) en lugar de preguntar.
- Cortá cuando puedas escribir criterios de aceptación concretos sin adivinar. Resumilos en 3-8 bullets y pedí confirmación.

## Fase 2 — Exploración

- Lanzá explorers (haiku) **en paralelo** solo para lo que no sepas (ni el código a mano ni `aprendizajes.md`): una pregunta concreta por explorer.
- Pediles conclusiones con `ruta:línea`, no volcados de archivos.

## Fase 3 — Plan (requiere aprobación)

Presentá el plan y **pará hasta que el usuario lo apruebe**. Formato:

```
Objetivo: ...
Criterios de aceptación: ...

Tareas:
1. [implementer] <qué hacer> — archivos: a.go, b.go — verifica: <comando>
2. [implementer] ... — archivos: c.go — depende de: 1
3. ...
R. [reviewer] revisión final del diff

Paralelismo: 1 y 3 en paralelo (archivos distintos); 2 después de 1.
Presupuesto: 3 implementers, 1 reviewer (modelos: los de agents/*.md).
Riesgos / decisiones abiertas: ...
```

Reglas del plan:
- Cada tarea tiene que ser autocontenida: un implementer la tiene que poder hacer sin leer esta conversación.
- Si una tarea es trivial (≤ ~20 líneas, un archivo), proponé hacerla vos en lugar de lanzar un agente.
- Si el usuario cambia algo, actualizá el plan y volvé a mostrarlo.

## Fase 4 — Ejecución

- **Paralelo solo si las tareas tocan archivos distintos** y no dependen entre sí. Si se pisan, secuencial.
- Usá `isolation: "worktree"` solo para tareas grandes que convenga aislar; avisá que después hay que mergear.
- El prompt de cada implementer incluye: objetivo general (1-2 líneas), la tarea exacta, archivos a tocar, convenciones relevantes que encontraron los explorers, criterio de "hecho" y comando de verificación.
- Si hay `aprendizajes.md`, agregá una sección **Aprendizajes del proyecto** con solo las líneas que aplican a esa tarea.
- Al volver cada implementer: leé su reporte. Si quedó **bloqueado** o se desvió del plan, decidí con el usuario antes de seguir; no relances a ciegas.
- Después de cada tanda, dale al usuario una línea de estado: `✓ 1, ✓ 3, ⏳ 2`.

## Fase 5 — Revisión y cierre

1. Corré vos el build/tests completos una vez.
2. Lanzá **un** reviewer con: objetivo, criterios de aceptación, plan y lista de archivos cambiados.
3. Si el reviewer encuentra problemas reales, arreglalos (vos si son chicos, un implementer si no) y no vuelvas a revisar todo salvo que el usuario lo pida.
4. Reporte final al usuario:
   - Qué se hizo, contra los criterios de aceptación (✓ / ✗).
   - Resultado real de tests (si fallan, decilo con el error).
   - Agentes usados por modelo (ej. `2 haiku · 3 sonnet · 1 opus`), tomados de `eventos.jsonl` si está (ver Fase 6).
   - Pendientes o decisiones que quedaron abiertas.

No hagas commit ni push salvo que el usuario lo pida.

## Fase 6 — Retro (aprendizaje)

Siempre, aunque la tarea haya salido perfecta. Es corta: no lances agentes para esto.

1. **Compará plan vs. realidad** con lo que ya tenés en la conversación:
   - Implementers bloqueados o desviados, y la causa.
   - Hallazgos del reviewer, en especial los marcados como **patrón evitable**.
   - Notas de **Aprendizaje candidato** de los implementers.
   - Comandos de verificación que fallaron o tardaron de más.
   - Presupuesto estimado vs. usado; tamaño estimado vs. real.
   - Aprendizajes existentes que el código contradijo.
2. **Proponé 0-3 cambios** a `.claude/orquestador/aprendizajes.md` como diff (agregar / reemplazar / borrar), cada uno con su origen. Aplicá las reglas de `memoria.md`: solo generalizables, sin duplicados, tope ~60 líneas. Cero es una respuesta válida; no rellenes.
3. **Escribí solo lo que el usuario apruebe.** Si el archivo no existe, crealo con la plantilla de `memoria.md`.
4. **Agregá una línea a `~/.claude/orquestador/historial.jsonl`** (esto no requiere aprobación: son métricas, sin contenido del proyecto). Creá la carpeta si no existe.
   - Para `agentes`, `tokens` y `subagentes_registrados`, leé `~/.claude/orquestador/eventos.jsonl` y quedate con las líneas de este `proyecto_id` con `ts` ≥ la hora de inicio de la Fase 0. Contá por `familia` (agent_id únicos). Esos datos son reales; no los estimes.
   - Si no hay eventos (hook desactivado o sin python), contá de la conversación y poné `subagentes_registrados: 0`.
   - Si el conteo de eventos no coincide con los agentes que lanzaste, o algún `modelo` no es el esperado por el archivo del agente, anotalo en `nota`.
5. Si el historial global ya tiene 10+ corridas y la última `/mejorar` fue hace más de 10, mencioná en una línea que se puede correr `/mejorar`.
