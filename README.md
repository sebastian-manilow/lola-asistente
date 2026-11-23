# Lola — asistente personal por voz sobre Claude Code

Lola es una "directora" personal: una sesión de Claude Code que coordina otras sesiones de trabajo (búsqueda de empleo, vídeos, prospección de clientes) y se maneja por voz, sin teclear.

## Cómo funciona
- **Escucha local (0 tokens):** `voz/escucha.py` usa Vosk (offline). Al oír la palabra de activación ("Lola") envía lo que sigue a la ventana de Claude.
- **Voz:** `voz/hablar.py` responde con voz neuronal (edge-tts, es-ES), en segundo plano.
- **Personalidad y reglas:** [PERSONALIDAD.md](PERSONALIDAD.md) (tono, protocolo de conversación, límites).
- **Dirección de sesiones:** [DIRECTOR.md](DIRECTOR.md) (patrón: un director + trabajadoras por área).

## Requisitos
Windows, Python 3, `pip install vosk sounddevice edge-tts`, modelo Vosk español, Claude Code (app de escritorio).

Sin datos personales: contraseñas, claves y datos de la persona usuaria no forman parte del repositorio.
