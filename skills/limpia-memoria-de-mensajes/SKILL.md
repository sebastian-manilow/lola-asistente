---
name: limpia-memoria-de-mensajes
description: Cuando el usuario diga "Limpia la memoria de mensajes", crea un traspaso a una sesión nueva y limpia del mismo proyecto para seguir más ligero sin perder estado.
---

# Limpia la memoria de mensajes (traspaso a sesión nueva)

Disparador: el usuario dice "Limpia la memoria de mensajes" (o parecido: "limpia el contexto", "sesión nueva"). Hazlo todo sin pedirle nada ni explicar pasos.

## Procedimiento
1. **Guardar lo duradero**: si en la sesión hay reglas, decisiones o datos nuevos que no estén ya en `CLAUDE.md` del proyecto o en la memoria (`memory/`), escríbelos ahí ahora (un archivo por hecho + línea en `MEMORY.md`).
2. **Escribir `TRASPASO.md`** en la raíz del proyecto (sobrescribir, máx. ~40 líneas, sin datos que ya estén en CLAUDE.md):
   - Objetivo actual y qué se estaba haciendo (1-3 líneas).
   - Estado: hecho / en curso / pendiente (con rutas, ids, enlaces y fechas límite).
   - Decisiones recientes del usuario y reglas nuevas (referenciando dónde quedaron anotadas).
   - Sesiones o tareas programadas relacionadas (ids) y qué esperan del usuario.
   - Primer paso exacto para continuar.
   - Qué NO repetir (comprobaciones ya hechas).
3. **Comprobar que no quedan cosas a medias** (formularios abiertos, ediciones sin guardar, tareas en segundo plano) y anotarlas en el traspaso.
4. **Abrir la sesión nueva** con `start_session` (initiation "user_asked", context "fresh", `cwd` = carpeta del proyecto, `use_worktree` false, `name` corto, título "<proyecto> (sesión limpia)"). El prompt: "Lee `TRASPASO.md` y `CLAUDE.md` y continúa desde el primer paso indicado; al empezar confirma en una línea qué retomas." El background (≥80 caracteres): resumen de 2-3 líneas del proyecto y la ruta de `TRASPASO.md`.
5. **Responder en una o dos líneas**: enlace a la sesión nueva ([título](#id)) y que la actual se puede dejar. No archivar la antigua salvo que el usuario lo pida.
6. Cuando la sesión nueva termine su primer turno, resumirlo al usuario en una línea.

## Mejoras ya incorporadas
- El traspaso vive en un archivo (`TRASPASO.md`), no solo en el prompt: sobrevive a reinicios y sirve a futuras sesiones.
- Nada se pierde: lo duradero va a CLAUDE.md/memoria antes de abrir la sesión.
- Mismo `cwd` del proyecto para que se carguen sus instrucciones y memoria automáticamente.
- Si el proyecto tiene tareas programadas, el traspaso las lista para no duplicarlas.
