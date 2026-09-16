#!/usr/bin/env python3
"""
Portal kalejdoskopowy - fraktalne pogiecie wspolrzednych obrazu.

Ta sama matematyka co Kaliset/Mandelbox (skladanie abs + obrot + skala),
ale zamiast renderowac geometrie, gnie WSPOLRZEDNE i probkuje nimi zdjecie.
Efekt: komorki wypelnione odbitym lustrzanie obrazem zrodlowym, obrysowane
szklistymi krawedziami - jak sufit-portal z referencji.

Uzycie:
    python3 portal_kalejdoskop.py                      # zrodlo proceduralne
    python3 portal_kalejdoskop.py --plate las.jpg      # wlasne zdjecie
    python3 portal_kalejdoskop.py --iter 14 --scale 1.32 --rot 0.38
"""
import argparse, math
import numpy as np
from PIL import Image


def noise2d(h, w, oktawy=6, seed=0):
    """Fraktalny szum - suma oktaw interpolowanych bikubicznie."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    rozm = 4
    for _ in range(oktawy):
        g = rng.random((rozm, rozm)).astype(np.float32)
        warstwa = np.asarray(
            Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
            np.float32) / 255.0
        out += warstwa * amp
        tot += amp
        amp *= 0.5
        rozm *= 2
    return out / tot


def las_proceduralny(h, w, seed=3):
    """Zastepcze zrodlo wzorowane na swierkowym lesie: proste pnie,
    jasny mech na dole, mgla pod swiatlo w glebi."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = xx / w, yy / h
    img = np.zeros((h, w, 3), np.float32)

    # 1. glebia: jasna, mglista luka miedzy drzewami w gornej polowie
    mgla = np.exp(-(((u - 0.52) / 0.42) ** 2 + ((v - 0.34) / 0.30) ** 2))
    img += mgla[..., None] * np.array([0.78, 0.82, 0.72], np.float32)
    img += np.array([0.10, 0.14, 0.11], np.float32)

    # 2. korony: ciemna zielen u gory
    korona = np.clip(1.0 - v * 3.0, 0, 1) ** 1.3
    n_kor = noise2d(h, w, oktawy=6, seed=seed + 2)
    img *= (1 - (korona * np.clip((n_kor - 0.40) * 2.6, 0, 1))[..., None] * 0.80)
    img += (korona * np.clip((n_kor - 0.45) * 2.0, 0, 1))[..., None] * np.array([0.06, 0.20, 0.09], np.float32)

    # 3. runo: jasny mech w dolnej trzeciej, z kepami
    runo = np.clip((v - 0.52) * 3.4, 0, 1) ** 0.8
    n_mech = noise2d(h, w, oktawy=5, seed=seed + 11)
    mech = np.array([0.20, 0.44, 0.17], np.float32) * (0.55 + 0.75 * n_mech)[..., None]
    img = img * (1 - runo[..., None]) + mech * runo[..., None]
    # przeswity slonca na mchu
    plamy = np.clip((noise2d(h, w, oktawy=4, seed=seed + 19) - 0.55) * 4.0, 0, 1)
    img += (plamy * runo)[..., None] * np.array([0.26, 0.38, 0.12], np.float32)

    # 4. pnie: proste, pionowe, zbiegajace sie lekko ku gorze
    rng = np.random.default_rng(seed + 31)
    for _ in range(26):
        x0 = rng.random() * 1.2 - 0.1
        glebia = rng.random()                      # 0 = blisko, 1 = daleko
        szer = (0.004 + 0.020 * (1 - glebia)) * (0.85 + 0.3 * rng.random())
        zbieg = (x0 - 0.5) * 0.10 * (1 - glebia)   # perspektywa
        d = np.abs((u + zbieg * (1 - v)) - x0)
        pien = np.exp(-(d / szer) ** 2)
        wys = np.clip(1.0 - (v - (0.55 + 0.35 * glebia)) * 6.0, 0, 1)
        maska = pien * wys * (0.92 - 0.55 * glebia)
        kora = np.array([0.20, 0.17, 0.13], np.float32) * (0.5 + 0.9 * glebia)
        img = img * (1 - maska[..., None]) + kora * maska[..., None]
        # mokre swiatlo na lewej krawedzi pnia
        krawedz = np.exp(-(((u + zbieg * (1 - v)) - (x0 - szer * 0.75)) / (szer * 0.45)) ** 2)
        img += (krawedz * wys * (1 - glebia))[..., None] * np.array([0.16, 0.18, 0.14], np.float32)

    # 5. mgla powietrzna narastajaca w glebi kadru
    dal = np.clip(1.0 - np.abs(v - 0.40) * 2.2, 0, 1)
    img = img * (1 - 0.34 * dal[..., None]) + np.array([0.62, 0.68, 0.60], np.float32) * 0.34 * dal[..., None]

    return np.clip(img, 0, 1)


def probkuj(tex, sx, sy):
    """Probkowanie bilinearne z odbiciem na brzegach."""
    h, w = tex.shape[:2]
    sx = np.abs(sx) % (2 * w)
    sx = np.where(sx >= w, 2 * w - sx - 1, sx)
    sy = np.abs(sy) % (2 * h)
    sy = np.where(sy >= h, 2 * h - sy - 1, sy)
    x0 = np.floor(sx).astype(np.int32); y0 = np.floor(sy).astype(np.int32)
    x1 = np.clip(x0 + 1, 0, w - 1);     y1 = np.clip(y0 + 1, 0, h - 1)
    x0 = np.clip(x0, 0, w - 1);         y0 = np.clip(y0, 0, h - 1)
    fx = (sx - x0)[..., None];          fy = (sy - y0)[..., None]
    return ((tex[y0, x0] * (1 - fx) + tex[y0, x1] * fx) * (1 - fy) +
            (tex[y1, x0] * (1 - fx) + tex[y1, x1] * fx) * fy)


def zloz(px, py, iteracje, skala, rot, offx, offy, min_r=0.30):
    """Fraktalne skladanie wspolrzednych + pulapka orbitalna (trap)."""
    ca, sa = math.cos(rot), math.sin(rot)
    trap = np.full(px.shape, 1e9, np.float32)
    for _ in range(iteracje):
        px, py = np.abs(px), np.abs(py)              # skladanie lustrzane
        px, py = px * ca - py * sa, px * sa + py * ca  # obrot
        r2 = px * px + py * py                        # inwersja sferyczna
        f = np.clip(min_r / np.maximum(r2, 1e-6), 1.0, 1.0 / min_r)
        px, py = px * f, py * f
        px = px * skala - offx
        py = py * skala - offy
        trap = np.minimum(trap, np.sqrt(px * px + py * py))
    return px, py, trap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", help="zdjecie zrodlowe (np. klatka lasu); brak = las proceduralny")
    ap.add_argument("--out", default="portal.png")
    ap.add_argument("-W", type=int, default=1280)
    ap.add_argument("-H", type=int, default=720)
    ap.add_argument("--iter", type=int, default=12)
    ap.add_argument("--scale", type=float, default=1.32)
    ap.add_argument("--rot", type=float, default=0.38)
    ap.add_argument("--offx", type=float, default=0.62)
    ap.add_argument("--offy", type=float, default=0.48)
    ap.add_argument("--zoom", type=float, default=1.15)
    ap.add_argument("--szklo", type=float, default=1.0, help="sila szklanych krawedzi")
    ap.add_argument("--pasy", type=float, default=12.0, help="gestosc warstwic na szkle")
    ap.add_argument("--miekkosc", type=float, default=1.0, help="rozmycie zrodla (0=ostre)")
    ap.add_argument("--texskala", type=float, default=0.22, help="ile zrodla widac w komorce (male=wiecej drzew)")
    ap.add_argument("--inwersja", type=float, default=0.30, help="sila inwersji sferycznej (0=wylaczona)")
    ap.add_argument("--winieta", type=float, default=0.25, help="sila przyciemnienia brzegow")
    a = ap.parse_args()

    W, H = a.W, a.H
    tex = (np.asarray(Image.open(a.plate).convert("RGB").resize((W, H), Image.LANCZOS), np.float32) / 255.0
           if a.plate else las_proceduralny(H, W))
    if a.miekkosc > 0:
        from PIL import ImageFilter
        tex = np.asarray(Image.fromarray((tex * 255).astype(np.uint8))
                         .filter(ImageFilter.GaussianBlur(a.miekkosc * 2.5)), np.float32) / 255.0

    # siatka wspolrzednych, srodek kadru, korekta proporcji
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px = (xx / W - 0.5) * 2.0 * (W / H) / a.zoom
    py = (yy / H - 0.5) * 2.0 / a.zoom

    fx, fy, trap = zloz(px, py, a.iter, a.scale, a.rot, a.offx, a.offy,
                        min_r=(a.inwersja if a.inwersja > 0 else 1.0))

    # pogiete wspolrzedne -> probkowanie zrodla (to daje las w komorkach)
    obraz = probkuj(tex, (fx * a.texskala + 0.5) * W, (fy * a.texskala + 0.5) * H)

    # --- szklane krawedzie z pola trap ---
    t = np.log(np.maximum(trap, 1e-6))
    t = (t - t.min()) / max(t.max() - t.min(), 1e-6)
    gy, gx = np.gradient(t)
    nachylenie = np.sqrt(gx * gx + gy * gy)
    nachylenie /= max(nachylenie.max(), 1e-6)

    # warstwice: jasne obrysy komorek
    pasy = np.abs(np.sin(t * a.pasy)) ** 6
    # specular: swiatlo z gory-prawej po normalnej powierzchni szkla
    spec = np.clip(-gx * 0.7 + gy * 0.7, 0, None)
    spec = (spec / max(spec.max(), 1e-6)) ** 1.6

    krawedz = np.clip(nachylenie * 5.0, 0, 1)
    obraz = obraz * (1.0 - 0.45 * krawedz[..., None])                                  # przyciemnienie rowkow
    zapas = np.clip(1.0 - obraz.mean(axis=2), 0, 1)[..., None]  # nie przepalaj jasnych miejsc
    obraz += (pasy * a.szklo * 0.55)[..., None] * np.array([0.62, 0.80, 0.95], np.float32) * zapas
    obraz += (spec * krawedz * a.szklo * 0.9)[..., None] * np.array([0.75, 0.88, 1.0], np.float32) * zapas

    # aberracja chromatyczna na krawedziach
    prz = (krawedz * 2.2).astype(np.float32)
    obraz[..., 0] = np.roll(obraz[..., 0], 1, axis=1) * 0.5 + obraz[..., 0] * 0.5
    obraz[..., 2] = np.roll(obraz[..., 2], -1, axis=1) * 0.5 + obraz[..., 2] * 0.5

    # --- grade: zimno, kontrast, winieta, ziarno ---
    obraz = np.clip(obraz, 0, 1) ** 1.05
    obraz[..., 0] *= 0.82
    obraz[..., 1] *= 0.95
    obraz[..., 2] *= 1.12
    sr = obraz.mean(axis=2, keepdims=True)
    obraz = sr + (obraz - sr) * 0.78
    obraz = np.clip((obraz - 0.5) * 1.22 + 0.5, 0, 1)

    vy, vx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((vx / W - 0.5) * 1.9) ** 2 + ((vy / H - 0.5) * 1.9) ** 2)
    obraz *= np.clip(1.0 - (r - 0.45) * a.winieta * 2.2, 0.15, 1)[..., None]
    obraz += np.random.default_rng(1).normal(0, 0.012, (H, W, 1)).astype(np.float32)

    Image.fromarray((np.clip(obraz, 0, 1) * 255).astype(np.uint8)).save(a.out)
    print("zapisano:", a.out)


if __name__ == "__main__":
    main()
