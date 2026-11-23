# Lola — asistente personal por voz sobre Claude Code

Lola es una "directora" personal: una sesión de Claude Code que coordina otras sesiones de trabajo (una por cada área que definas) y se maneja por voz, sin teclear.

## Cómo funciona
- **Escucha local (0 tokens):** `voz/escucha.py` usa Vosk (offline). Al oír la palabra de activación ("Lola") envía lo que sigue a la ventana de Claude.
- **Voz:** `voz/hablar.py` responde con voz neuronal (edge-tts, es-ES), en segundo plano.
- **Personalidad y reglas:** `PERSONALIDAD.md` (tono, protocolo de conversación, límites).
- **Dirección de sesiones:** ver `DIRECTOR.md` (patrón: un director + trabajadores por área).

## Índice
[Instalación](#instalación-en-3-pasos) · [Configuración](config.example.json) · [Autolimpieza de contexto](#autolimpieza-de-contexto) · [Seguridad](SEGURIDAD.md) · [Guía de sesiones](GUIA_SESIONES.md) · [Personalidad](PERSONALIDAD.md) · [Director](DIRECTOR.md) · [Contribuir](CONTRIBUTING.md) · [Licencia MIT](LICENSE)

## Requisitos
Windows, Python 3.9+, Claude Code (app de escritorio). No requiere administrador.

## Instalación en 3 pasos
1. Clona el repositorio: `git clone https://github.com/sebastian-manilow/lola-asistente.git`
2. Ejecuta `powershell -ExecutionPolicy Bypass -File install.ps1` (instala dependencias, descarga el modelo Vosk y crea `config.json`).
3. Ajusta `config.json` (palabra de activación, voz, micrófono) y arranca `python voz\escucha.py`.

## Autolimpieza de contexto
Cuando una sesión se hace pesada, di "Limpia la memoria de mensajes": la skill `skills/limpia-memoria-de-mensajes/SKILL.md` guarda lo duradero, escribe `TRASPASO.md` y abre una sesión limpia que continúa. Cópiala a `~/.claude/skills/`. Más en [GUIA_SESIONES.md](GUIA_SESIONES.md).

Sin datos personales: contraseñas, claves y datos de la persona usuaria no forman parte del repositorio. Ver [SEGURIDAD.md](SEGURIDAD.md).
- Guía detallada de la sesión directora: [GUIA_DIRECTORA.md](GUIA_DIRECTORA.md)
