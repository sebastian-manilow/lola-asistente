# Patrón Director + trabajadoras
Una sesión "Director" habla con la persona; el resto son trabajadoras por área (empleo, vídeos, ventas). El Director reenvía órdenes, vigila el estado, archiva sesiones terminadas y renueva (traspaso a sesión limpia) las que se alargan. Las aprobaciones sensibles (mensajes a terceros, pagos) las da siempre la persona en el chat de la sesión que las ejecuta.

Multitarea: cada petición se lanza en segundo plano (sesiones o subagentes) y el Director va respondiendo según llegan los resultados.
