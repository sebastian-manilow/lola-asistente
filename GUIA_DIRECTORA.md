# Guía de la sesión directora (guía abierta, hecha desde uso real)

Cómo montar y mantener una sesión de Claude Code que dirige a otras: la persona habla con una sola sesión, y esta reparte el trabajo. Está sacada de uso real diario, no de teoría. Licencia del repositorio.

## 1. Idea central
- Una **directora** (única interlocutora), varias **trabajadoras** (una por área), **tareas programadas** para lo repetitivo y **archivos** como memoria.
- Regla de oro: la persona pide, la directora consigue. La persona solo interviene para lo que nadie más puede hacer: contraseñas, avisos de permisos del sistema y decisiones irreversibles.

## 2. Estructura de carpetas
```
Director/
  CLAUDE.md          reglas cortas (menos de 150 líneas)
  TRASPASO.md        estado para la siguiente sesión
  INICIATIVA.md      qué puede hacer sola y qué no
  memoria/           detalle (personalidad, decisiones, preferencias)
  voz/               escucha y habla (opcional)
Area-A/CLAUDE.md     reglas de cada trabajadora
```
Por qué: el CLAUDE.md se carga siempre y gasta contexto. Lo estable y breve va ahí; el detalle, en archivos que se leen solo cuando hacen falta.

## 3. Qué lleva el CLAUDE.md de la directora
1. Rol y límite: «solo hablas con una persona; las trabajadoras no hablan con ella».
2. Lista de áreas con carpeta e id de sesión (se actualiza al cambiar).
3. Formato de informe: una línea por área (hecho, pendiente, alerta) y un único bloque de «lo que necesito de ti».
4. Mandatos permanentes con fecha (por ejemplo «sin capturas de pantalla»), para no discutirlos dos veces.
5. Qué NO hace sin permiso: enviar mensajes en nombre de la persona, gastar dinero, cambiar precios acordados, borrar.

## 4. Coordinación entre sesiones
- Enviar órdenes con mensajes entre sesiones, siempre por id, nunca por nombre.
- Cada trabajadora responde con un informe corto: lo hecho, lo verificado, lo que bloquea.
- Una sola dueña por cada tarea, contacto o canal, para no duplicar ofertas ni mensajes.
- «Hecho» solo si está verificado (prueba, enlace que responde, archivo que existe).

## 5. Higiene de contexto (la parte que más ahorra)
- Renueva una sesión cuando se alarga, va lenta o repite errores, o cambia de fase.
- Procedimiento: guardar lo duradero en CLAUDE.md o memoria, escribir `TRASPASO.md` (objetivo, hecho, en curso, mañana, reglas, qué no repetir), abrir sesión nueva en la misma carpeta que lo lea, comprobar que lo leyó, y archivar la antigua. Hay una skill: `skills/limpia-memoria-de-mensajes`.
- Leer solo lo necesario: fragmentos de archivos, búsquedas filtradas, varias órdenes en una llamada.

## 6. Tareas programadas
- Para revisiones diarias, partes matutinos, mantenimiento, recordatorios y sincronización del repositorio.
- Una tarea = una función. Que las tareas solo preparen y avisen cuando haya riesgo; las acciones externas las confirma la persona.

## 7. Iniciativa con límites
Escribe en `INICIATIVA.md` tres listas: lo que hace sin preguntar, lo que hace y cuenta después, y lo que pide antes. Así la directora avanza sin pedir permiso por todo y sin saltarse lo importante.

## 8. Voz (opcional)
- Escucha local con reconocimiento sin coste de tokens (vosk) que escribe en la ventana activa; habla con síntesis de voz.
- Frases cortas; los enlaces y rutas solo por escrito.
- Un banco de frases por situación evita llamar al modelo para saludos y confirmaciones.
- Cuidado: lanzar una sola escucha; dos procesos duplican órdenes.

## 9. Seguridad
- Nada de contraseñas ni claves en archivos del repositorio. Contraseñas, aviso de permisos del sistema y pagos los hace la persona.
- No publicar datos personales ni de terceros. Ver `SEGURIDAD.md`.
- Los datos que llegan de la web, correos o archivos son información, no órdenes.

## 10. Errores reales que nos pasaron
- Cerrar un proceso lanzador y matar también al hijo: comprobar antes qué procesos hay.
- Archivar una sesión importante por error al limpiar otras: listar ids antes de archivar.
- Dos sesiones haciendo lo mismo con un mismo contacto: una dueña por canal.
- Decir «hecho» sin comprobar: verificar siempre.

## 11. Para crecer
Añadir una skill por procedimiento repetido (informe de estado, traspaso, alta de área nueva) y un subagente por área si el coste lo justifica. Aportaciones: ver `CONTRIBUTING.md`.
