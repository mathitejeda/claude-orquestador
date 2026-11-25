---
name: triage
description: Ordena una pila de issues o pendientes poco claros. Los lee, estima tamaño y claridad mirando el código con agentes baratos, detecta solapamientos y propone un orden y qué hacer con cada uno (resolver directo, especificar u orquestar). No implementa nada. Usar cuando el usuario pide /triage, "tengo varios issues", "no sé por dónde empezar".
---

# Triage

Tu trabajo es **ordenar y recomendar**, no implementar. No edites código ni modifiques issues (labels, comentarios, cierres) sin permiso explícito.

Entrada: $ARGUMENTS. Puede ser:
- vacío o `github` → issues abiertos del repo actual,
- filtros (`label:bug`, `milestone:x`, números `#3 #7 #12`),
- un archivo con pendientes, o una lista pegada.

## 1. Juntar los pendientes

- GitHub: `gh issue list --state open --limit 50 --json number,title,body,labels,comments` (aplicá filtros si los hay). Si son más de ~25, preguntá si filtrar antes de seguir.
- Otro origen: parsealo en una lista numerada.

## 2. Estimar contra el código

**Calibración con memoria** (si existe):
- `.claude/orquestador/aprendizajes.md` del repo → sección `Calibración` y `Trampas`.
- `~/.claude/orquestador/historial.jsonl` → filtrá por `proyecto` igual al nombre de la carpeta del repo. Compará `tamaño_estimado` con lo que costó de verdad (`agentes`, `bloqueos`). Si las tareas "chicas" de este repo suelen necesitar más, ajustá tus estimaciones y decilo en una línea en la presentación.

- Agrupá los pendientes por zona del código (por título/cuerpo).
- Por cada grupo con zona incierta, un `orquestador:explorer` con **model: haiku**, en paralelo, máximo **3 explorers en total**. Pedile por issue: archivos probablemente afectados, tamaño estimado y si el código ya resuelve parte o lo contradice.
- Lo obvio, resolvelo vos con un grep. Nunca uses sonnet ni opus en esta fase.

## 3. Clasificar

Para cada pendiente:
- **Tamaño**: trivial (≤ ~20 líneas, 1 archivo) · chico · grande.
- **Claridad**: clara (se podría implementar ya) · ambigua (faltan decisiones) · dudosa (quizás ya resuelto, duplicado o no vale la pena).
- **Toca**: módulos/archivos principales.
- **Siguiente paso**:
  - trivial y clara → resolver directo en una sesión normal (sonnet), o agrupar varios triviales en una sola tarea;
  - chica/grande y clara → `/orquestar`;
  - ambigua → `/especificar`;
  - dudosa → preguntarle al usuario / proponer cerrar.

Detectá **solapamientos**: issues que tocan los mismos archivos (conviene hacerlos juntos o en secuencia) y dependencias (uno bloquea a otro).

## 4. Presentar

```
| # | Issue | Tamaño | Claridad | Toca | Siguiente paso |
|---|-------|--------|----------|------|----------------|

Solapamientos / dependencias:
- #3 y #7 tocan exportador/csv.go → hacerlos juntos.

Orden sugerido:
1. Lote de triviales: #4, #9 (una sesión sonnet)
2. #3 + #7 → /orquestar
3. #12 → /especificar primero (falta decidir X)

Dudosos: #15 parece resuelto en <ruta:línea> — ¿cerrar?
```

Después, **preguntá**: ¿qué orden querés? ¿alguno afuera? Para los ambiguos, ofrecé arrancar `/especificar` con el primero.

Opcional: si el usuario quiere, guardá la tabla en `.claude/specs/triage-<YYYY-MM-DD>.md` para retomarla en otra sesión.
