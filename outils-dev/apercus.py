"""Capture un aperçu de chaque site lié depuis index.html.

Les images vont dans assets/apercus/<domaine>.webp. Relancer ce script quand un site change :

    python scripts/apercus.py            # tous les sites (sauf les captures faites à la main)
    python scripts/apercus.py py e3c     # seulement py.nsi.xyz et e3c.nsi.xyz

- Les captures trop claires sont refaites avec le mode sombre automatique de Chrome,
  pour que tous les aperçus restent cohérents avec la page.
- Les simulateurs NumWorks sont recadrés sur la calculatrice seule, sur fond transparent.
- discover.nsi.xyz est capturé dans son style sombre « Glassmorphisme » (scripts/apercu-discover.mjs).
- Si un site répond par une erreur, sa capture précédente est conservée.

Nécessite Google Chrome et Pillow (pip install pillow), et Node 22 pour discover.
"""
import concurrent.futures, pathlib, re, ssl, subprocess, sys, tempfile, urllib.error, urllib.request
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "apercus"
CHROME = next((p for p in [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
] if pathlib.Path(p).exists()), None)

# Sites qui chargent un gros programme (interpréteur Python, émulateur) : on attend en temps réel.
SLOW = {"pyweb": 16000, "webos": 12000, "epsilon": 10000, "omega": 10000, "psi": 10000}

# Captures faites à la main (le site ne finit pas de charger sans fenêtre visible) :
# ignorées lors d'une mise à jour générale, refaites seulement si on les nomme.
MANUAL = {"pyweb"}

# Simulateurs NumWorks : on ne garde que la calculatrice
CALC = {"epsilon", "omega", "psi"}

# Au-delà de cette luminosité moyenne (0 à 255), la capture est refaite en mode sombre
LIGHT = 120
DARK_FLAGS = ["--force-dark-mode", "--enable-features=WebContentsForceDark"]


def short(host):
    return host.removesuffix(".nsi.xyz")


def hosts():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    found = re.findall(r'href="https://([a-z0-9.-]+\.[a-z]{2,})/"[^>]*data-site', html)
    return list(dict.fromkeys(found))


def shoot(host, png, tmp, scale=2, height=800, extra=()):
    slow = SLOW.get(short(host))
    # Le temps virtuel accélère le chargement ; certains émulateurs le bloquent,
    # on retente alors avec un simple délai réel.
    waits = [f"--timeout={slow}"] if slow else ["--virtual-time-budget=8000", "--timeout=10000"]
    png.unlink(missing_ok=True)
    for wait in waits:
        try:
            subprocess.run([
                CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                "--ignore-certificate-errors", f"--user-data-dir={tmp}/profil", *extra,
                f"--window-size=1280,{height}", f"--force-device-scale-factor={scale}", wait,
                f"--screenshot={png}", f"https://{host}/",
            ], capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            continue
        if png.exists():
            return Image.open(png).convert("RGB")
    return None


def isolate_calculator(im):
    """Retire le fond uni et l'en-tête du simulateur : reste la calculatrice, sur fond transparent."""
    sentinel = (255, 0, 255)
    w, h = im.size
    bg = im.getpixel((10, h - 10))
    top = next(y for y in range(h)
               if len(row := (im.crop((0, y, w, y + 1)).getcolors(w * 2) or [])) == 1
               and max(abs(a - b) for a, b in zip(row[0][1], bg)) < 4)
    work = im.crop((0, top, w, h))
    for seed in [(0, 0), (w - 1, 0), (0, work.height - 1), (w - 1, work.height - 1), (w // 2, work.height - 1)]:
        if work.getpixel(seed) != sentinel:
            ImageDraw.floodfill(work, seed, sentinel, thresh=14)
    mask = ImageChops.difference(work, Image.new("RGB", work.size, sentinel)).convert("L").point(lambda v: 255 if v > 30 else 0)
    # Cadre de la calculatrice : colonnes bien remplies, puis lignes couvrant au moins la moitié de sa largeur
    small = mask.resize((mask.width // 8, mask.height // 8))
    px = small.load()
    cols = [x for x in range(small.width) if sum(px[x, y] > 0 for y in range(small.height)) > small.height * .25]
    span = cols[-1] - cols[0] + 1
    rows = [y for y in range(small.height) if sum(px[x, y] > 0 for x in range(cols[0], cols[-1] + 1)) > span * .5]
    box = (cols[0] * 8, rows[0] * 8, (cols[-1] + 1) * 8, (rows[-1] + 1) * 8)
    calc = work.crop(box).convert("RGBA")
    calc.putalpha(mask.crop(box).filter(ImageFilter.GaussianBlur(.8)))
    calc = calc.crop(calc.getbbox())
    calc.thumbnail((900, 1500), Image.LANCZOS)
    return calc


def status(host):
    """Code HTTP renvoyé par le site (0 s'il est injoignable)."""
    try:
        req = urllib.request.Request(f"https://{host}/", headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(req, timeout=20, context=ssl._create_unverified_context()).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def capture(host):
    code = status(host)
    if not 200 <= code < 400:
        return f"GARDÉE {host}  (le site répond {code or 'rien'} : capture précédente conservée)"
    if short(host) == "discover":
        # La page retient son style dans le navigateur : capture dédiée, puis conversion en WebP
        subprocess.run(["node", str(ROOT / "scripts" / "apercu-discover.mjs")], capture_output=True, timeout=120)
        png = OUT / f"{host}.png"
        if not png.exists():
            return f"ÉCHEC  {host}"
        Image.open(png).convert("RGB").resize((1280, 800), Image.LANCZOS).save(OUT / f"{host}.webp", quality=84, method=6)
        png.unlink()
        return f"ok     {host}  (style Glassmorphisme)"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        png = pathlib.Path(tmp) / "shot.png"
        if short(host) in CALC:
            im = shoot(host, png, tmp, scale=3, height=900)
            if im is None:
                return f"ÉCHEC  {host}"
            isolate_calculator(im).save(OUT / f"{host}.webp", quality=88, method=6)
            return f"ok     {host}  (calculatrice seule)"
        im = shoot(host, png, tmp)
        if im is None:
            return f"ÉCHEC  {host}"
        note = ""
        if ImageStat.Stat(im.convert("L")).mean[0] > LIGHT:
            dark = shoot(host, png, tmp, extra=DARK_FLAGS)
            if dark is not None:
                im, note = dark, "  (mode sombre forcé)"
        # Capture en résolution rétina (2560×1600), réduite à 1280×800 : net sur tous les écrans
        im.resize((1280, 800), Image.LANCZOS).save(OUT / f"{host}.webp", quality=84, method=6)
        return f"ok     {host}{note}"


if __name__ == "__main__":
    if not CHROME:
        sys.exit("Google Chrome est introuvable.")
    OUT.mkdir(parents=True, exist_ok=True)
    todo = hosts()
    if sys.argv[1:]:
        todo = [h for h in todo if short(h) in sys.argv[1:]]
    else:
        todo = [h for h in todo if short(h) not in MANUAL]
    with concurrent.futures.ThreadPoolExecutor(4) as ex:
        for line in ex.map(capture, todo):
            print(line, flush=True)
