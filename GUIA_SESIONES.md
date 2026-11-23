# Guía de sesiones: director + trabajadoras

## Patrón
Una sesión **directora** (la única con la que hablas) y varias **trabajadoras**, una por área (empleo, vídeo, administración...). La directora reparte órdenes, vigila el estado y te da un informe corto.

## Montaje
1. Crea una carpeta por área con su propio `CLAUDE.md`.
2. Crea la carpeta de la directora con un `CLAUDE.md` que liste las áreas y los ids de sus sesiones.
3. Abre cada trabajadora en su carpeta; la directora les da órdenes con mensajes entre sesiones.
4. Las tareas repetitivas (revisiones diarias, mantenimiento) se programan en segundo plano; la directora solo mira el resultado.

## CLAUDE.md genérico de la directora
```markdown
# Directora
Eres la directora. La persona usuaria solo habla contigo.
## Qué haces
- Al abrir o al decir "estado": un informe corto por área (hecho, pendiente, alertas).
- Reenvía las órdenes a la trabajadora adecuada; nunca hagas hablar a la persona con ellas.
- Agrupa lo que necesita de la persona (contraseñas, aprobaciones) en un único resumen.
## Áreas
- Área A: carpeta `A/`, sesión `id_A`
- Área B: carpeta `B/`, sesión `id_B`
## Límites
Ver SEGURIDAD.md.
```

## TRASPASO.md de ejemplo
```markdown
# Traspaso
Objetivo: terminar el informe mensual del área A.
Hecho: datos recogidos (`datos/mes.csv`). En curso: gráficos. Pendiente: revisión y envío (requiere aprobación).
Decisiones: formato PDF, tono breve.
Tareas programadas relacionadas: revisión diaria 09:00.
Primer paso: abrir `informe/borrador.md` y completar la sección 3.
No repetir: la descarga de datos ya está hecha.
```

## Cuándo renovar una sesión
Cuando tenga muchísimos mensajes, el contexto pase de la mitad, vaya lenta, repita errores o cambie de fase. Di "Limpia la memoria de mensajes" (skill en `skills/limpia-memoria-de-mensajes/`): guarda lo duradero, escribe `TRASPASO.md` y abre una sesión limpia que lo lee y sigue. Copia la skill a `~/.claude/skills/`.

## Repartir tareas en segundo plano
- Tareas largas o repetitivas: una trabajadora o una tarea programada, no la directora.
- Una tarea, un responsable; el resultado vuelve como informe breve.
- Lo que requiera tu aprobación (mensajes a terceros) espera en el chat de la sesión que lo ejecuta.
