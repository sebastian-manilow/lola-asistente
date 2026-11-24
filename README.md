# Lola — asistente personal por voz sobre Claude Code

Lola es un asistente de voz que actúa como **directora**: una sesión de Claude Code que recibe órdenes habladas, las reparte entre otras sesiones de trabajo (una por área: empleo, vídeo, administración…) y responde en voz alta. Proyecto personal, pensado para Windows, con el objetivo de hacer más con menos tokens.

## Qué demuestra
- **Orquestación multi-agente:** un director y varios trabajadores con contexto aislado por área, coordinados con mensajes entre sesiones.
- **Voz sin coste de tokens:** la detección de la palabra de activación corre en local (Vosk, offline); solo el texto reconocido llega al modelo.
- **Respuesta hablada:** síntesis de voz neuronal (edge-tts, es-ES) en segundo plano, para no bloquear la conversación.
- **Ahorro de contexto:** una skill de "autolimpieza" guarda lo duradero, escribe un traspaso y abre una sesión nueva que continúa el trabajo.
- **Seguridad por diseño:** la asistente nunca escribe contraseñas ni códigos; esas acciones quedan siempre en manos de la persona usuaria.

## Cómo funciona
| Pieza | Archivo | Función |
|---|---|---|
| Escucha local | `voz/escucha.py` | Vosk offline; al oír "Lola" envía la frase a la ventana de Claude. |
| Voz | `voz/hablar.py` | Lee las respuestas con edge-tts, en segundo plano. |
| Personalidad y límites | `PERSONALIDAD.md` | Tono, protocolo de conversación y reglas de seguridad. |
| Dirección de sesiones | `DIRECTOR.md`, `GUIA_DIRECTORA.md` | Cómo organizar un director y sus trabajadores. |
| Autolimpieza | `skills/limpia-memoria-de-mensajes/SKILL.md` | Traspaso a sesión limpia sin perder estado. |
| Instalador | `install.ps1` | Instala dependencias, descarga el modelo Vosk y crea `config.json`. |

## Requisitos
- Windows 10/11, Python 3.9 o superior.
- Claude Code (app de escritorio).
- Micrófono y altavoces. No requiere permisos de administrador.

## Uso
1. Clona el repositorio:
   ```powershell
   git clone https://github.com/sebastian-manilow/lola-asistente.git
   ```
2. Instala todo desde la carpeta del proyecto:
   ```powershell
   powershell -ExecutionPolicy Bypass -File install.ps1
   ```
3. Revisa `config.json` (palabra de activación, voz, micrófono; plantilla en [config.example.json](config.example.json)) y arranca la escucha:
   ```powershell
   python voz\escucha.py
   ```
4. Di "Lola" seguido de la orden, por ejemplo: *"Lola, revisa el estado de las sesiones"*.

## Documentación
- [Guía de la sesión directora](GUIA_DIRECTORA.md) y [guía de sesiones](GUIA_SESIONES.md)
- [Personalidad y voz](PERSONALIDAD.md)
- [Seguridad](SEGURIDAD.md)
- [Contribuir](CONTRIBUTING.md)

## Limitaciones
- Solo Windows (la escucha usa el micrófono y la ventana activa del sistema).
- Requiere una cuenta de Claude Code con uso activo; el coste de tokens depende de las sesiones que se abran.
- Proyecto personal y en evolución: úsalo como punto de partida, no como producto cerrado.

## Privacidad
El repositorio no contiene contraseñas, claves, rutas personales ni datos de la persona usuaria: todo eso se configura en local. Detalles en [SEGURIDAD.md](SEGURIDAD.md).

## Licencia
MIT. Ver [LICENSE](LICENSE).
