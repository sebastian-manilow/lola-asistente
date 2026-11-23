"""Lola: escucha local (vosk, 0 tokens). Di "Lola" (+ frase) y la envia a la ventana de Claude."""
import json, queue, time, os, sys, re, traceback, winsound
import sounddevice as sd, vosk, win32gui, win32con, win32clipboard, pyautogui
vosk.SetLogLevel(-1)

D = os.path.dirname(os.path.abspath(__file__))
try: CFG = json.load(open(os.path.join(D, "..", "config.json"), encoding="utf-8"))
except Exception: CFG = {}
DEV = int(sys.argv[1]) if len(sys.argv) > 1 else int(CFG.get("microfono", 1))
SILENCIO = float(CFG.get("silencio_corte_s", 2.5))
ESPERA_MAX = float(CFG.get("espera_max_s", 300))
PALABRA = str(CFG.get("palabra_activacion", "lola")).lower()
DESPEDIDA = CFG.get("frase_despedida", "Hasta luego. Aquí estaré cuando me llames.")
LOG = open(os.path.join(D, f"escucha_{DEV}.log"), "a", encoding="utf-8")
FLAG = os.path.join(D, "hablando.flag")   # existe mientras Lola habla
DRY = os.path.join(D, "dry.flag")
if CFG.get("modo_seco"): open(DRY, "a").close()         # si existe: no envia, solo registra
def log(s): LOG.write(time.strftime("%H:%M:%S ") + s + "\n"); LOG.flush()

WAKE = re.compile(r"\b(lola|lolas|lo la|los la|hola la|ola la|y lo la|di lola|dilo la|el la|hola)\b")

def claude_win():
    r = []
    def e(h, _):
        if win32gui.IsWindowVisible(h) and win32gui.GetWindowText(h) == "Claude": r.append(h)
    win32gui.EnumWindows(e, None)
    return r[0] if r else None

PREV = [0]
def guardar_fg(h):
    f = win32gui.GetForegroundWindow()
    if f and f != h and win32gui.IsWindow(f): PREV[0] = f
def volver_fg():
    p = PREV[0]; PREV[0] = 0
    if p and win32gui.IsWindow(p):
        try:
            pyautogui.press("alt"); win32gui.SetForegroundWindow(p)
        except Exception: pass

def send(txt):
    txt = txt[:1].upper() + txt[1:]
    log("SEND " + txt)
    if os.path.exists(DRY): return
    import uiautomation as auto
    w = auto.WindowControl(searchDepth=1, Name="Claude")
    if not w.Exists(1): log("ERR sin ventana Claude"); return
    guardar_fg(w.NativeWindowHandle)
    if win32gui.IsIconic(w.NativeWindowHandle): win32gui.ShowWindow(w.NativeWindowHandle, win32con.SW_RESTORE)
    pyautogui.press("alt")
    try: win32gui.SetForegroundWindow(w.NativeWindowHandle)
    except Exception as ex: log("FG " + repr(ex))
    e = w.EditControl(Name="Prompt", searchDepth=40)
    if not e.Exists(2): log("ERR sin caja Prompt"); return
    e.Click(simulateMove=False); time.sleep(0.15)
    win32clipboard.OpenClipboard(); win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(txt, win32clipboard.CF_UNICODETEXT); win32clipboard.CloseClipboard()
    pyautogui.hotkey("ctrl", "v"); time.sleep(0.2); pyautogui.press("enter")
    log("OK enviado"); volver_fg()

def ui():
    import uiautomation as auto
    w = auto.WindowControl(searchDepth=1, Name="Claude")
    h = w.NativeWindowHandle
    guardar_fg(h)
    if win32gui.IsIconic(h): win32gui.ShowWindow(h, win32con.SW_RESTORE)
    pyautogui.press("alt")
    try: win32gui.SetForegroundWindow(h)
    except Exception: pass
    return w

BTN = None
def dictar(on):
    w = ui()
    import re as _r
    global BTN
    b = BTN
    try:
        ok = b is not None and b.Exists(0, 0)
    except Exception: ok = False
    if not ok:
        b = w.ButtonControl(searchDepth=40, RegexName="(?i)dicta|grab|detener dict|micr")
        if not b.Exists(2): log("ERR sin boton Dictar"); return False
        BTN = b
    log(("DICTAR ON " if on else "DICTAR OFF ") + b.Name)
    b.Click(simulateMove=False); return True

def enviar_dictado():
    time.sleep(0.8)
    w = ui()
    e = w.EditControl(Name="Prompt", searchDepth=40)
    if e.Exists(1):
        try: log("TEXTO " + e.GetValuePattern().Value[:200])
        except Exception: pass
        e.Click(simulateMove=False); time.sleep(0.1)
    if not os.path.exists(DRY): pyautogui.press("enter"); log("OK enviado"); volver_fg()

def limpiar():
    w = ui(); e = w.EditControl(Name="Prompt", searchDepth=40)
    if e.Exists(1): e.Click(simulateMove=False); pyautogui.hotkey("ctrl", "a"); pyautogui.press("delete")

import random, ctypes, glob
MUL = glob.glob(os.path.join(D, "muletillas", "*.mp3"))
def muletilla():
    if not MUL: return
    m = ctypes.windll.winmm.mciSendStringW
    m("close mu", None, 0, 0); m(f'open "{random.choice(MUL)}" type mpegvideo alias mu', None, 0, 0)
    m("play mu wait", None, 0, 0); m("close mu", None, 0, 0)
    while not q.empty(): q.get_nowait()

def relleno():
    m = ctypes.windll.winmm.mciSendStringW
    f = random.choice(glob.glob(os.path.join(D, "rellenos", "*.mp3")))
    m("close rl", None, 0, 0); m(f'open "{f}" type mpegvideo alias rl', None, 0, 0)
    m("play rl wait", None, 0, 0); m("close rl", None, 0, 0)

def beep():
    m = ctypes.windll.winmm.mciSendStringW
    try:
        m("close rg", None, 0, 0); m(f'open "{random.choice(glob.glob(os.path.join(D, "senales_*.mp3")))}" type mpegvideo alias rg', None, 0, 0)
        m("play rg wait", None, 0, 0); m("close rg", None, 0, 0)
    except Exception as ex: log("BEEP " + repr(ex))
    while not q.empty(): q.get_nowait()

MODEL = vosk.Model(os.path.join(D, "modelo_dl", "vosk-model-small-es-0.42"))
rec = vosk.KaldiRecognizer(MODEL, 16000)
wk = vosk.KaldiRecognizer(MODEL , 16000, json.dumps([PALABRA, "hola", "lo la", "[unk]"]))
q = queue.Queue()
dict_on = False; t0 = 0.0; last = 0.0; spoke = False
wait_reply = time.time() + 86400; saw_flag = False
pend = 0.0
long_on = False; long_buf = []; long_file = ""; long_last = 0.0
BYE = re.compile(r"cu[eé]lgate|adi[oó]s lola|lola adi[oó]s|hasta ma[nñ]ana|hasta luego|deja de escuchar|para de escuchar|c[aá]llate lola|lola c[aá]llate|buenas noches lola")
START_LONG = re.compile(r"escuchame todo|escúchame todo|escucha todo|modo largo|nota larga")
END_LONG = re.compile(r"(he terminado|ya he terminado|termin[eé]|fin de la nota|ya est[aá] lola|lola ya est[aá]|eso es todo)\s*$")
def start(silent=False):
    global dict_on, t0, last, spoke
    if not silent: beep()
    if dictar(True): dict_on = True; t0 = last = time.time(); spoke = False
log(f"INICIO micro {DEV}")
with sd.RawInputStream(device=DEV, samplerate=16000, blocksize=4000, dtype="int16", channels=1,
                       callback=lambda d, f, t, s: q.put(bytes(d))):
    while True:
        try:
            d = q.get(); now = time.time()
            if os.path.exists(os.path.join(D, "pausa.flag")):
                if dict_on: dictar(False); time.sleep(0.8); limpiar(); dict_on = False; log("PAUSA: dictado cerrado")
                wait_reply = 0; pend = 0.0
                if not dict_on and not os.path.exists(FLAG):
                    wf = wk.AcceptWaveform(d)
                    wt = json.loads(wk.Result()).get("text", "") if wf else json.loads(wk.PartialResult()).get("partial", "")
                    if re.search(r"(lola|lo la)", wt) and wf:
                        try: os.remove(os.path.join(D, "pausa.flag"))
                        except Exception: pass
                        wk.Reset(); rec.Reset(); log("PAUSA terminada por Lola"); start()
                continue
            if False and pend and not os.path.exists(FLAG) and now - pend > 8 and not saw_flag:
                relleno(); pend = time.time(); continue
            if os.path.exists(FLAG):            # Lola esta hablando
                pend = 0.0
                if dict_on:                     # cerrar dictado y borrar lo que haya captado de mi voz
                    dictar(False); time.sleep(1.5); limpiar(); dict_on = False; log("DICTAR cancelado: hablo yo")
                saw_flag = True; rec.Reset(); wk.Reset(); continue
            if wait_reply:                      # conversacion: esperar a que Lola responda
                if saw_flag:                    # solo escucho tras responder Lola; mientras trabaja, no
                    wait_reply = 0; saw_flag = False; log("SIGUE conversacion"); time.sleep(0.6); rec.Reset(); start(True); continue
                if now > wait_reply: wait_reply = 0; log("FIN espera respuesta")
            if long_on:
                if now - long_last > SILENCIO:
                    long_on = False; log("NOTA LARGA fin por silencio")
                    if long_buf: send("Nota de voz larga guardada en " + long_file + ". Léela entera, haz lo que te pido en ella y respóndeme por voz.")
                    wait_reply = time.time() + 600; saw_flag = False; continue
                if rec.AcceptWaveform(d):
                    t = json.loads(rec.Result()).get("text", "").strip()
                    if t:
                        long_buf.append(t); long_last = now; open(long_file, "a", encoding="utf-8").write(t + chr(10))
                        if END_LONG.search(t):
                            long_on = False; log("NOTA LARGA fin " + str(len(long_buf)) + " frases")
                            send("Nota de voz larga guardada en " + long_file + ". Léela entera, haz lo que te pido en ella y respóndeme por voz.")
                            wait_reply = time.time() + 600; saw_flag = False
                continue
            if dict_on:
                fin = rec.AcceptWaveform(d)
                txt = json.loads(rec.Result()).get("text", "") if fin else json.loads(rec.PartialResult()).get("partial", "")
                if txt.strip(): last = now; spoke = True
                if BYE.search(txt):
                    dictar(False); time.sleep(0.8); limpiar(); dict_on = False; wait_reply = 0; rec.Reset()
                    log("ADIOS: " + txt); open(os.path.join(D, "hablando.flag"), "w").close()
                    import subprocess; subprocess.Popen([sys.executable.replace("pythonw", "python"), os.path.join(D, "hablar.py"), DESPEDIDA], creationflags=0x08000000)
                    continue
                if fin and START_LONG.search(txt):
                    dictar(False); time.sleep(0.8); limpiar(); dict_on = False; long_on = True; long_buf = []; long_last = time.time()
                    long_file = os.path.join(D, "notas", time.strftime("%Y%m%d_%H%M%S") + ".txt")
                    log("NOTA LARGA inicio " + long_file); beep(); rec.Reset(); continue
                if spoke and now - last > SILENCIO:          # silencio tras hablar -> enviar
                    dictar(False); enviar_dictado(); dict_on = False; muletilla(); rec.Reset()
                    wait_reply = time.time() + 86400; saw_flag = False; pend = time.time()
                elif not spoke and now - t0 > ESPERA_MAX:        # no dijo nada -> salir de conversacion
                    dictar(False); dict_on = False; rec.Reset(); log("SIN voz, en espera de Lola")
                continue
            wf = wk.AcceptWaveform(d)
            wt = json.loads(wk.Result()).get("text", "") if wf else json.loads(wk.PartialResult()).get("partial", "")
            if re.search(r"(lola|lo la)", wt):
                wk.Reset(); rec.Reset(); log("WAKE " + wt); start(); continue
            if rec.AcceptWaveform(d):
                t = json.loads(rec.Result()).get("text", "").strip()
                if not t: continue
                log("OIDO " + t); w = t.split()
                if len(w) <= 2 and set(w) & {"lola","lolas","lo","la","los","hola","ola","dola"}:
                    log("WAKE corto " + t); start()
        except Exception:
            log("EXC " + traceback.format_exc().replace(chr(10), " | "))
