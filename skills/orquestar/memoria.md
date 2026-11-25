# Memoria del orquestador

Referencia compartida por `orquestar`, `especificar`, `triage` y `mejorar`. Define qué se guarda, dónde y con qué reglas.

## Dos niveles

| Archivo | Alcance | Quién escribe | Quién lee |
|---|---|---|---|
| `<repo>/.claude/orquestador/aprendizajes.md` | un proyecto | `orquestar` (Fase 6), con aprobación | todas las skills |
| `~/.claude/orquestador/historial.jsonl` | todos los proyectos | `orquestar` (Fase 6), automático | `triage`, `mejorar` |
| `~/.claude/orquestador/mejoras.md` | el plugin | `mejorar` | `mejorar` |

Los aprendizajes viven en el repo para que se versionen y los aproveche cualquiera que trabaje ahí. El historial es global para poder ver patrones entre proyectos.

## `aprendizajes.md`

```markdown
# Aprendizajes del proyecto
<!-- Mantenido por /orquestar. Máx. ~60 líneas. Editable a mano. -->

## Verificación
- Build: `<comando>` · Tests rápidos: `<comando>` · Lento/evitar por tarea: `<comando>`

## Convenciones
- <regla> — origen: <de dónde salió, ej. "reviewer 2026-11-20">

## Trampas
- <qué pasa si tocás X> → <qué hacer>

## Calibración
- <observación sobre tamaño/presupuesto, ej. "tareas de >3 archivos se bloquean: partirlas">
```

Reglas:
- **Generalizable o nada.** Un aprendizaje tiene que servir para la *próxima* tarea, no describir esta. "El parser de fechas está en util/time.go" no va (eso lo encuentra un grep); "las fechas siempre en UTC, el reviewer lo marcó" sí.
- **Con origen.** Cada línea dice de dónde salió, así se puede auditar o borrar.
- **Sin duplicados ni contradicciones.** Si uno nuevo contradice uno existente, reemplazalo.
- **Tope ~60 líneas.** Si se pasa, consolidá antes de agregar.
- **Nunca** secretos, tokens, datos de clientes ni rutas personales.

## `historial.jsonl`

Una línea JSON por corrida de `/orquestar`:

```json
{"fecha":"2026-11-20","proyecto":"<nombre de la carpeta del repo>","tarea":"<5-8 palabras>","origen":"spec|directa","tamaño_estimado":"trivial|chico|grande","tareas_plan":3,"agentes":{"haiku":2,"sonnet":3,"opus":1},"presupuesto_excedido":false,"bloqueos":1,"desvios":0,"hallazgos_reviewer":2,"tests":"ok|fallan|sin_tests","aprendizajes_nuevos":1,"nota":"<una línea opcional: qué salió distinto de lo esperado>"}
```

- `proyecto` es solo el nombre de la carpeta, nunca la ruta completa.
- Creá `~/.claude/orquestador/` si no existe. Agregá al final; nunca reescribas líneas viejas.

## Cómo usar la memoria al leerla

- Antes de preguntarle algo al usuario o lanzar un explorer, fijate si `aprendizajes.md` ya lo responde.
- Pasale a cada implementer **solo** las líneas relevantes a su tarea (verificación + convenciones/trampas de los archivos que toca), no el archivo entero.
- Si el código contradice un aprendizaje, el código manda: avisá y proponé corregirlo en la retro.
