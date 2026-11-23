# Instalador de Lola (Windows, sin administrador). Uso: powershell -ExecutionPolicy Bypass -File install.ps1
$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "[1/4] Comprobando Python..."
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { Write-Host "No se encuentra Python 3. Instalalo desde https://www.python.org/downloads/ (marca 'Add to PATH') y vuelve a ejecutar."; exit 1 }
& python -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)"
if ($LASTEXITCODE -ne 0) { Write-Host "Se necesita Python 3.9 o superior."; exit 1 }
Write-Host "[2/4] Instalando dependencias (solo para tu usuario)..."
& python -m pip install --user --upgrade vosk sounddevice edge-tts pyautogui pywin32 uiautomation
if ($LASTEXITCODE -ne 0) { Write-Host "Fallo pip. Revisa tu conexion."; exit 1 }
Write-Host "[3/4] Modelo de voz espanol pequeno de Vosk..."
$dl = Join-Path $raiz "voz\modelo_dl"
$modelo = Join-Path $dl "vosk-model-small-es-0.42"
if (Test-Path $modelo) { Write-Host "Ya existe, se omite." } else {
  New-Item -ItemType Directory -Force $dl | Out-Null
  $zip = Join-Path $dl "modelo.zip"
  Invoke-WebRequest "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip" -OutFile $zip
  Expand-Archive $zip -DestinationPath $dl -Force
  Remove-Item $zip
}
Write-Host "[4/4] Configuracion..."
$cfg = Join-Path $raiz "config.json"
if (-not (Test-Path $cfg)) { Copy-Item (Join-Path $raiz "config.example.json") $cfg; Write-Host "Creado config.json (editalo a tu gusto)." } else { Write-Host "config.json ya existe, no se toca." }
Write-Host "Microfonos disponibles (usa el indice en config.json):"
& python -c "import sounddevice as sd; print(sd.query_devices())"
Write-Host "Listo. Prueba: python voz\hablar.py Hola   y luego: python voz\escucha.py"
