---
name: especificar
description: Convierte una idea, issue o pedido vago en una spec concreta mediante una entrevista estilo grill, y la guarda en un archivo listo para /orquestar. No implementa nada. Usar cuando el usuario pide /especificar, "especifiquemos X", "armemos la tarea de X", o trae algo que todavía no está claro.
---

# Especificar

Tu trabajo es **entender y escribir**, no implementar. No edites código del proyecto.

Entrada: $ARGUMENTS (puede ser una idea suelta, un número de issue `#12`, una URL de issue o un archivo).

**Si la entrada empieza con `nuevo`, o es claramente un proyecto desde cero**: leé `nuevo.md` (en la carpeta de esta skill) y seguí ese flujo en lugar del de abajo.

## 1. Contexto

- Si existe `.claude/orquestador/aprendizajes.md` en el repo, leelo primero: convenciones y trampas que la spec debería respetar o mencionar.
- Si es un issue de GitHub: `gh issue view <n> --comments`.
- Mirá el código relevante vos mismo con grep/lectura. Lanzá a lo sumo 1-2 `orquestador:explorer` (model: haiku) solo si la zona es grande o desconocida. Nunca otros modelos.
- Objetivo: llegar a la entrevista sabiendo cómo funciona hoy lo que se va a cambiar, para no preguntar cosas que el código responde.

## 2. Entrevista (estilo grill)

Si hay una skill `grill-me` (o similar) disponible, usala para esta fase. Si no:

- **Una pregunta por vez.** Cada una con tu respuesta recomendada, así el usuario confirma o corrige.
- Recorré el árbol de decisiones, rama por rama, hasta que no queden dudas:
  - Problema y por qué importa ahora.
  - Comportamiento esperado: caso feliz, bordes, errores.
  - Alcance: qué entra y, explícitamente, qué NO.
  - Restricciones: compatibilidad, datos existentes, performance, dependencias.
  - Diseño: dónde va el cambio, qué se reutiliza, alternativas descartadas y por qué.
  - Verificación: cómo se prueba que está bien (tests, pasos manuales).
- Si detectás que en realidad son varias tareas independientes, decilo y proponé partirla.
- Cortá cuando puedas escribir criterios de aceptación verificables sin adivinar.

## 3. Escribir la spec

Guardala en `.claude/specs/<slug>.md` dentro del proyecto (creá la carpeta si no existe), salvo que el usuario pida otro lugar. Formato:

```markdown
# <Título>

Origen: <issue #n / pedido del usuario> · Fecha: <YYYY-MM-DD>
Estado: lista para orquestar

## Problema
## Objetivo
## Alcance
- Entra: ...
- No entra: ...
## Comportamiento esperado
## Diseño propuesto
- Archivos / módulos afectados: `ruta` — qué cambia
- Alternativas descartadas: ...
## Criterios de aceptación
- [ ] ...
## Verificación
## Decisiones tomadas en la entrevista
- <pregunta> → <decisión>
## Preguntas abiertas
```

Mostrale al usuario un resumen de 5-10 líneas y la ruta del archivo. Proponé el siguiente paso: `/orquestar .claude/specs/<slug>.md` (o hacerlo directo en una sesión normal si es chica).

Si el origen era un issue de GitHub, ofrecé (no hagas sin permiso) comentar la spec en el issue.
