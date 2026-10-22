"""Capture un aperçu de chaque site lié depuis index.html.

Les images vont dans assets/apercus/<domaine>.webp et servent à l'aperçu
qui s'affiche au survol des cartes. Relancer ce script quand un site change :

    python scripts/apercus.py            # tous les sites
    python scripts/apercus.py py e3c     # seulement py.nsi.xyz et e3c.nsi.xyz

Nécessite Google Chrome et Pillow (pip install pillow).
"""
import concurrent.futures, pathlib, re, subprocess, sys, tempfile
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "apercus"
CHROME = next((p for p in [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
] if pathlib.Path(p).exists()), None)


def hosts():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    found = re.findall(r'href="https://([a-z0-9.-]+\.nsi\.xyz)/"[^>]*data-site', html)
    return list(dict.fromkeys(found))


# Sites qui chargent un gros programme (interpréteur Python, émulateur) : on attend en temps réel.
SLOW = {"pyweb": 16000, "webos": 12000, "epsilon": 10000, "omega": 10000, "psi": 10000}

# Captures faites à la main (le site ne finit pas de charger sans fenêtre visible) :
# ignorées lors d'une mise à jour générale, refaites seulement si on les nomme.
MANUAL = {"pyweb"}


def capture(host):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        png = pathlib.Path(tmp) / "shot.png"
        slow = SLOW.get(host.split(".nsi.xyz")[0])
        # Le temps virtuel accélère le chargement ; certains émulateurs le bloquent,
        # on retente alors avec un simple délai réel.
        waits = [f"--timeout={slow}"] if slow else ["--virtual-time-budget=8000", "--timeout=10000"]
        for wait in waits:
            try:
                subprocess.run([
                    CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                    "--ignore-certificate-errors", f"--user-data-dir={tmp}/profil",
                    "--window-size=1280,800", "--force-device-scale-factor=2", wait,
                    f"--screenshot={png}", f"https://{host}/",
                ], capture_output=True, timeout=90)
            except subprocess.TimeoutExpired:
                continue
            if png.exists():
                break
        if not png.exists():
            return f"ÉCHEC  {host}"
        # Capture en résolution rétina (2560×1600), réduite à 1280×800 : net sur tous les écrans
        Image.open(png).convert("RGB").resize((1280, 800), Image.LANCZOS).save(
            OUT / f"{host}.webp", quality=84, method=6)
        return f"ok     {host}"


if __name__ == "__main__":
    if not CHROME:
        sys.exit("Google Chrome est introuvable.")
    OUT.mkdir(parents=True, exist_ok=True)
    todo = hosts()
    if sys.argv[1:]:
        todo = [h for h in todo if h.split(".nsi.xyz")[0] in sys.argv[1:]]
    else:
        todo = [h for h in todo if h.split(".nsi.xyz")[0] not in MANUAL]
    with concurrent.futures.ThreadPoolExecutor(4) as ex:
        for line in ex.map(capture, todo):
            print(line, flush=True)
