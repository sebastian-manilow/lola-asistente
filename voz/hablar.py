import sys, os, hashlib, shutil
D=os.path.dirname(os.path.abspath(__file__))
FL=os.path.join(D,"hablando.flag")
open(FL,"w").close()
import asyncio, tempfile
import json
try: CFG=json.load(open(os.path.join(D,"..","config.json"),encoding="utf-8"))
except Exception: CFG={}
VOZ=os.environ.get("VOZ") or CFG.get("voz_tts","es-ES-XimenaNeural")
txt = " ".join(sys.argv[1:])
CD=os.path.join(D,"cache"); os.makedirs(CD,exist_ok=True)
cf=os.path.join(CD,hashlib.md5((VOZ+txt).encode()).hexdigest()+".mp3")
f = os.path.join(tempfile.gettempdir(), f"dv_{os.getpid()}.mp3")
if os.path.exists(cf):
    shutil.copyfile(cf,f)
else:
    import edge_tts
    async def main():
        await edge_tts.Communicate(txt, VOZ, **(dict(rate="+8%", pitch="-2Hz", volume="+40%") if VOZ.startswith("es-") else dict(volume="+40%"))).save(f)
    asyncio.run(main())
    if len(txt)<=120:
        try: shutil.copyfile(f,cf)
        except: pass
import ctypes, time
m=ctypes.windll.winmm.mciSendStringW
m('close dv',None,0,0)
m(f'open "{f}" type mpegvideo alias dv',None,0,0)
m('play dv wait',None,0,0)
m('close dv',None,0,0)
time.sleep(0.1)
try: os.remove(FL)
except: pass
try: os.remove(f)
except: pass
