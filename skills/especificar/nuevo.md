# Especificar — proyecto nuevo

No hay código que mirar: todo sale de la entrevista. No generes código ni scaffolding; eso lo hace `/orquestar` con la primera spec.

## 1. Entrevista de proyecto (estilo grill)

Mismas reglas que la entrevista normal: una pregunta por vez, con tu respuesta recomendada; si hay `grill-me` disponible, usala. Ramas a recorrer:

- **Problema y usuarios**: qué resuelve, para quién, cómo lo resuelven hoy.
- **Primera versión**: lo mínimo que tiene que hacer para ser útil. Qué queda explícitamente para después.
- **Stack**: lenguaje, framework, base de datos. Recomendá en base a lo que el usuario ya usa y justificá en una línea.
- **Arquitectura**: piezas principales y cómo se hablan.
- **Datos**: entidades principales y de dónde vienen.
- **Entorno**: dónde corre, cómo se despliega, integraciones externas.
- **Verificación**: cómo se prueba (tests, datos de prueba, pasos manuales).

Cortá cuando puedas describir la primera versión sin adivinar. Mostrá un resumen y pedí confirmación antes de escribir.

## 2. Escribir

Si el usuario no está parado en la carpeta del proyecto, preguntá dónde crearla. Archivos:

**`.claude/specs/proyecto.md`** — visión, no tareas:

```markdown
# <Proyecto>
Fecha: <YYYY-MM-DD>
## Problema y usuarios
## Primera versión (entra / queda para después)
## Stack (con el porqué)
## Arquitectura
## Datos
## Entorno y despliegue
## Decisiones tomadas
- <pregunta> → <decisión>
## Preguntas abiertas
## Hitos
1. `01-<slug>.md` — <una línea>
2. ...
```

**Una spec por hito**, `.claude/specs/NN-<slug>.md`, con el mismo formato de spec normal (sección 3 de SKILL.md) más una línea `Depende de: NN`.

Reglas para los hitos:
- 3 a 7 hitos para la primera versión. Si salen más, la primera versión es demasiado grande: proponé recortar.
- El `01` es siempre el esqueleto: proyecto que compila/corre, estructura de carpetas, un test que pasa.
- Cada hito deja algo que funciona y se puede probar, no capas a medias.

## 3. Cerrar

Mostrá la lista de hitos y proponé arrancar con `/orquestar .claude/specs/01-<slug>.md`.
