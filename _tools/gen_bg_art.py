#!/usr/bin/env python
"""
Procedural "folded paper / ribbon" background art for BookSaga.

Layered curved sheets with:
  - structured shading across the width (lit roll -> crease -> shadow)
  - curvature darkening where the sheet bends (reads as a fold)
  - crisp specular line on the lit cut edge + blurred tinted glow
  - soft ambient-occlusion shadow cast onto everything behind
  - depth-of-field blur per sheet, film grain, vignette

Usage:
    python gen_bg_art.py <scene> [out.png]
    python gen_bg_art.py all
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2
OUT_W, OUT_H = 1774, 887
W, H = OUT_W * SS, OUT_H * SS

U_STEPS = 46
T_STEPS = 240

LIGHT = np.array([0.40, -0.92])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64) / 255.0


def mix(a, b, t):
    return a + (b - a) * t


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a + 1e-12), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def noise1(x, seed=0, octaves=4, base=2.5):
    rng = np.random.default_rng(seed)
    v = np.zeros_like(x, dtype=np.float64)
    amp, freq, norm = 1.0, base, 0.0
    for _ in range(octaves):
        ph = rng.uniform(0, 2 * math.pi)
        v += amp * np.sin(x * freq * 2 * math.pi + ph)
        norm += amp
        amp *= 0.5
        freq *= 2.0
    return v / norm


def catmull_rom(pts, per_seg=80):
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = (np.array(P[i + k], dtype=np.float64) for k in range(4))
        for j in range(per_seg):
            t = j / per_seg
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1)
                              + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(np.array(pts[-1], dtype=np.float64))
    return np.array(out)


def resample(pts, n):
    d = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(d)])
    s /= s[-1] + 1e-12
    u = np.linspace(0, 1, n)
    return np.stack([np.interp(u, s, pts[:, 0]), np.interp(u, s, pts[:, 1])], axis=1)


def normals_of(pts):
    d = np.gradient(pts, axis=0)
    d /= (np.linalg.norm(d, axis=1, keepdims=True) + 1e-12)
    return np.stack([-d[:, 1], d[:, 0]], axis=1)


def curvature(pts):
    d1 = np.gradient(pts, axis=0)
    d2 = np.gradient(d1, axis=0)
    num = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0])
    den = (d1[:, 0] ** 2 + d1[:, 1] ** 2) ** 1.5 + 1e-9
    k = num / den
    k = np.convolve(np.pad(k, 6, mode="edge"), np.ones(13) / 13, mode="valid")
    return k / (k.max() + 1e-12)


def width_curve(t, wpts):
    ks = np.array(wpts, dtype=np.float64)
    w = np.interp(t, ks[:, 0], ks[:, 1])
    w = np.convolve(np.pad(w, 5, mode="edge"), np.ones(11) / 11.0, mode="valid")
    return w * H


# --------------------------------------------------------------------------- #
# shading
# --------------------------------------------------------------------------- #
def band_colors(spec, t, s, kn):
    """
    t, s, kn: (N, U) arrays.  s: 0 = lit edge, 1 = far edge.

    Edge-lit sheet model: brightness is highest right at the lit edge and falls
    away fast into shadow, with an optional soft crease ridge just inside the
    edge.  This is what makes a sheet read as paper seen nearly edge-on.
    """
    amb = spec.get("amb", 0.02)
    peak = spec.get("peak", 1.0)
    fall = spec.get("fall", 0.30)
    fall_exp = spec.get("fall_exp", 1.25)
    tg = spec.get("t_gain", (1.0, 0.0))
    tex = spec.get("texture", 0.035)
    seed = spec.get("seed", 1)

    b = amb + peak * np.exp(-((s / fall) ** fall_exp))

    # soft crease ridge just inside the lit edge
    cr = spec.get("crease_ridge", 0.0)
    if cr:
        b = b + cr * np.exp(-(((s - spec.get("crease_pos", 0.19))
                               / spec.get("crease_w", 0.055)) ** 2))

    # bounce light at the far edge
    b = b + spec.get("bounce", 0.05) * np.exp(-(((s - 1.0) / 0.06) ** 2))

    # bend darkening along the length + length falloff
    b = b * (1.0 - spec.get("fold", 0.40) * (kn ** 1.5))
    b = b * (tg[0] + tg[1] * t)

    if tex:
        b = b + tex * noise1(t * 3.0 + s * 0.4, seed=seed, octaves=3, base=2.2)

    shadow, light = spec["shadow"], spec["light"]
    col = shadow + (light - shadow) * np.clip(b, 0.0, 1.35)[..., None]

    # tight specular right on the lit edge
    spec_amt = np.exp(-(((s - 0.015) / 0.045) ** 2)) * spec.get("spec", 0.35)
    col = col + (np.array([1.0, 1.0, 1.0]) - col) * spec_amt[..., None]

    # tinted rim hugging the lit edge
    rim = np.exp(-(((s - spec.get("rim_pos", 0.0)) / spec.get("rim_w", 0.045)) ** 2))
    rim = rim * spec.get("rim_strength", 0.85) * (0.45 + 0.55 * t ** 0.6)
    col = col + (spec["rim"] - col) * np.clip(rim, 0.0, 1.0)[..., None]

    return np.clip(col, 0.0, 1.0), np.clip(rim, 0.0, 1.0)


# --------------------------------------------------------------------------- #
# one sheet
# --------------------------------------------------------------------------- #
def draw_band(canvas, spec):
    pts = resample(catmull_rom(spec["pts"], spec.get("per_seg", 80)), T_STEPS)
    pts = pts * np.array([W, H], dtype=np.float64)
    nrm = normals_of(pts)
    if spec.get("flip"):
        nrm = -nrm
    kn = curvature(pts)
    t = np.linspace(0.0, 1.0, T_STEPS)

    w = width_curve(t, spec["wpts"])
    # paper wobble: drift the centreline and breathe the width
    wob = spec.get("wobble", 0.004) * H * noise1(t * 1.6, seed=spec.get("seed", 1) + 7, octaves=3)
    pts = pts + nrm * wob[:, None]
    w = w * (1.0 + spec.get("width_jitter", 0.05)
             * noise1(t * 2.3, seed=spec.get("seed", 1) + 19, octaves=3))

    s_axis = np.linspace(0.0, 1.0, U_STEPS + 1)
    off = s_axis * 2.0 - 1.0
    grid = pts[:, None, :] + nrm[:, None, :] * (off[None, :, None] * w[:, None, None])

    tt = np.repeat(t[:, None], U_STEPS + 1, axis=1)
    ss = np.repeat(s_axis[None, :], T_STEPS, axis=0)
    kk = np.repeat(kn[:, None], U_STEPS + 1, axis=1)
    col, rim = band_colors(spec, tt, ss, kk)

    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fill)
    for i in range(T_STEPS - 1):
        for j in range(U_STEPS):
            q = np.array([grid[i, j], grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]])
            c = q.mean(axis=0)
            q = c + (q - c) * 1.07
            rgb = (col[i, j] * 0.5 + col[i + 1, j] * 0.5)
            fd.polygon([(float(p[0]), float(p[1])) for p in q],
                       fill=(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), 255))

    fill = fill.filter(ImageFilter.GaussianBlur(0.55 * SS))

    # ---- crisp edges (brightness varies along the edge) --------------------
    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    seed = spec.get("seed", 1)
    fade = spec.get("edge_fade", 0.20)
    prof = smoothstep(0.0, fade, t) * (1.0 - smoothstep(1.0 - fade, 1.0, t))
    prof = prof * np.clip(0.28 + 0.90 * np.abs(noise1(t * 2.7, seed=seed + 31, octaves=3, base=3.7)),
                          0.0, 1.0)
    prof = prof * (0.80 + 0.35 * t)

    lit = spec.get("edge_col", mix(spec["rim"], np.array([1.0, 1.0, 1.0]), 0.55))
    ep = grid[:, 0, :]
    ew = spec.get("edge_w", 1.9)
    for i in range(T_STEPS - 1):
        a = float(prof[i]) * spec.get("edge_gain", 1.0)
        if a < 0.02:
            continue
        c = np.clip(mix(lit, np.array([1.0, 1.0, 1.0]), 0.30 * a), 0, 1)
        w_ = max(1, int(ew * SS * (0.65 + 0.6 * a)))
        seg = [tuple(ep[i]), tuple(ep[i + 1])]
        ed.line(seg, fill=tuple(int(v * 255) for v in c) + (int(255 * min(1.0, a)),), width=w_)
        rc = np.clip(mix(spec["rim"], np.array([1.0, 1.0, 1.0]), 0.25), 0, 1)
        gd.line(seg, fill=tuple(int(v * 255) for v in rc) + (int(255 * min(1.0, a)),), width=w_)

    far = spec.get("far_edge", 0.30)
    if far > 0:
        fc = np.clip(mix(spec["shadow"], spec["rim"], 0.30) * 0.60, 0, 1)
        fp = grid[:, -1, :]
        for i in range(T_STEPS - 1):
            a = float(prof[i]) * far
            if a < 0.02:
                continue
            ed.line([tuple(fp[i]), tuple(fp[i + 1])],
                    fill=tuple(int(v * 255) for v in fc) + (int(255 * min(1.0, a)),),
                    width=max(1, int(1.4 * SS)))

    edge = edge.filter(ImageFilter.GaussianBlur(0.35 * SS))

    band = Image.alpha_composite(fill, edge)
    alpha = band.getchannel("A")

    # ---- shadow on everything behind --------------------------------------
    sstr = spec.get("shadow_strength", 1.0)
    if sstr > 0:
        sh = alpha.filter(ImageFilter.GaussianBlur(spec.get("shadow_blur", 22) * SS))
        ox = -LIGHT[0] * spec.get("shadow_dist", 12) * SS
        oy = -LIGHT[1] * spec.get("shadow_dist", 12) * SS
        sh = sh.transform(sh.size, Image.AFFINE, (1, 0, -ox, 0, 1, -oy), resample=Image.BILINEAR)
        shf = np.asarray(sh, dtype=np.float64) / 255.0
        canvas = canvas * (1.0 - shf[..., None] * sstr * 0.9)

    # ---- depth of field ----------------------------------------------------
    blur = spec.get("blur", 0.0)
    if blur > 0:
        band = band.filter(ImageFilter.GaussianBlur(blur * SS))

    ba = np.asarray(band, dtype=np.float64) / 255.0
    a = ba[..., 3:4] * spec.get("alpha", 1.0)
    canvas = canvas * (1 - a) + ba[..., :3] * a
    return canvas, glow


# --------------------------------------------------------------------------- #
# scene plumbing
# --------------------------------------------------------------------------- #
def background(kind):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    x, y = xx / W, yy / H

    if kind == "dark":
        top, bot = hexc("#06091F"), hexc("#140A31")
        img = top + (bot - top) * (y[..., None] ** 0.85)
        blooms = [(0.08, 0.95, 0.52, "#F121A5", 0.10),
                  (0.88, 0.14, 0.46, "#7B32FF", 0.11),
                  (0.52, 1.08, 0.40, "#FF7A1A", 0.05)]
    elif kind == "light":
        top, bot = hexc("#FBF3ED"), hexc("#FFF9FE")
        img = top + (bot - top) * (y[..., None] ** 0.8)
        blooms = [(0.90, 0.08, 0.55, "#F6D9EE", 0.62),
                  (0.06, 0.98, 0.52, "#EDE3FF", 0.55),
                  (0.55, 0.02, 0.45, "#FFE9D4", 0.42)]
    else:
        raise ValueError(kind)

    for (cx, cy, r, c, a) in blooms:
        d = np.sqrt((x - cx) ** 2 + ((y - cy) * (H / W)) ** 2)
        img = img + (hexc(c) - img) * (np.exp(-((d / r) ** 2) * 2.1)[..., None] * a)
    return np.clip(img, 0, 1)


def bloom(img, threshold=0.66, radius=40, amount=0.45):
    lum = img.mean(axis=2)
    mask = np.clip((lum - threshold) / (1.0 - threshold), 0.0, 1.0)[..., None]
    p = Image.fromarray((np.clip(img * mask, 0, 1) * 255).astype(np.uint8), "RGB")
    p = p.filter(ImageFilter.GaussianBlur(radius * SS))
    return np.clip(img + np.asarray(p, dtype=np.float64) / 255.0 * amount, 0, 1)


def dust(img, n=380, seed=3, colour="#FFA8DC", strength=0.75, region=None):
    rng = np.random.default_rng(seed)
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = tuple(int(v * 255) for v in hexc(colour))
    x0, y0, x1, y1 = region if region else (0, 0, 1, 1)
    for _ in range(n):
        px, py = rng.uniform(x0, x1) * W, rng.uniform(y0, y1) * H
        r = rng.gamma(1.6, 1.0) * 0.85 * SS
        a = rng.uniform(0.08, 0.5) * strength
        d.ellipse([px - r, py - r, px + r, py + r], fill=tuple(int(v * a) for v in c))
    layer = layer.filter(ImageFilter.GaussianBlur(0.45 * SS))
    return np.clip(img + np.asarray(layer, dtype=np.float64) / 255.0, 0, 1)


def finish(img, vignette=0.18):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    x = (xx / W - 0.5) * 2
    y = (yy / H - 0.5) * 2
    v = np.sqrt(x * x * 0.7 + y * y) / 1.2
    return np.clip(img * (1.0 - vignette * np.clip(v, 0, 1) ** 2.2)[..., None], 0, 1)


def save(img, path, grain=0.014):
    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), "RGB")
    out = out.resize((OUT_W, OUT_H), Image.LANCZOS)
    arr = np.asarray(out, dtype=np.float64) / 255.0
    arr = arr + np.random.default_rng(11).normal(0, grain, (OUT_H, OUT_W, 1))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGB").save(path)
    print("wrote", path)


def render(scene):
    canvas = background(scene["bg"])
    glows = []
    for band in scene["bands"]:
        canvas, g = draw_band(canvas, band)
        glows.append(g)

    if glows and scene.get("glow", 0.5) > 0:
        acc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for g in glows:
            acc = Image.alpha_composite(acc, g)
        acc = acc.filter(ImageFilter.GaussianBlur(scene.get("glow_blur", 16) * SS))
        a = np.asarray(acc, dtype=np.float64) / 255.0
        canvas = np.clip(canvas + a[..., :3] * a[..., 3:4] * scene["glow"], 0, 1)

    canvas = bloom(canvas, threshold=scene.get("bloom_thr", 0.66),
                   radius=scene.get("bloom_rad", 38), amount=scene.get("bloom_amt", 0.45))
    if scene.get("dust"):
        canvas = dust(canvas, **scene["dust"])
    return finish(canvas, vignette=scene.get("vignette", 0.18))


# --------------------------------------------------------------------------- #
# scenes
# --------------------------------------------------------------------------- #
MAGENTA = hexc("#FF3FA8")
HOTPINK = hexc("#F121A5")
ORANGE = hexc("#FF7A1A")
VIOLET = hexc("#9B44F2")
PEACH = hexc("#FFC59A")

DARKP = dict(shadow=hexc("#0C0C2B"), light=hexc("#6E5CBA"))
DEEPP = dict(shadow=hexc("#090A24"), light=hexc("#4A3C88"))
LITP = dict(shadow=hexc("#DCCDEA"), light=hexc("#FFFDFB"))


def radial_fan(origin, angles, radii, curve, wpts, base, **kw):
    out = []
    for k, ang in enumerate(angles):
        pts = []
        for r in radii:
            a = ang + curve * (r / radii[-1]) ** 1.7
            pts.append((origin[0] + math.cos(a) * r, origin[1] + math.sin(a) * r))
        b = dict(base)
        b.update(pts=pts, wpts=wpts, seed=200 + k, **kw)
        out.append(b)
    return out


SCENES = {}

# ---------------------------------------------------------------- 1. dark hero
SCENES["pages-dark"] = dict(
    bg="dark", glow=0.50, glow_blur=13, bloom_thr=0.62, bloom_amt=0.45,
    bands=[
        # A · big back sheet: bottom-left -> off the right edge
        dict(pts=[(-0.16, 1.16), (0.18, 0.80), (0.50, 0.62), (0.82, 0.58), (1.12, 0.62)],
             wpts=[(0, 0.05), (0.30, 0.17), (0.68, 0.15), (1, 0.13)],
             shadow=hexc("#090A24"), light=hexc("#3E3379"), rim=VIOLET,
             peak=0.95, fall=0.24, rim_strength=0.50, spec=0.22,
             edge_gain=0.45, edge_w=1.5, edge_fade=0.30,
             blur=3.6, shadow_blur=38, shadow_dist=24, flip=True, seed=11),
        # B · main sheet: left edge -> off the bottom-right corner
        dict(pts=[(-0.16, 0.60), (0.14, 0.52), (0.42, 0.58), (0.70, 0.72), (0.94, 0.94), (1.12, 1.14)],
             wpts=[(0, 0.04), (0.28, 0.15), (0.62, 0.14), (1, 0.12)],
             shadow=hexc("#0C0C2B"), light=hexc("#6B57B8"), rim=MAGENTA,
             peak=1.0, fall=0.21, rim_strength=0.90, spec=0.38,
             crease_ridge=0.24, crease_pos=0.17, crease_w=0.045,
             edge_gain=1.0, edge_w=2.0, edge_fade=0.18,
             blur=0.7, shadow_blur=26, shadow_dist=16, flip=True, seed=13),
        # C · thin bright sliver: left -> off the top-right corner
        dict(pts=[(-0.12, 0.34), (0.18, 0.26), (0.48, 0.22), (0.76, 0.15), (1.06, 0.00)],
             wpts=[(0, 0.02), (0.35, 0.065), (0.75, 0.055), (1, 0.035)],
             shadow=hexc("#0F0D2C"), light=hexc("#8E77CE"), rim=PEACH,
             peak=1.05, fall=0.19, rim_strength=1.0, spec=0.45,
             edge_gain=1.15, edge_w=1.7, edge_fade=0.22,
             blur=0.4, shadow_blur=22, shadow_dist=12, flip=True, seed=14),
        # D · small fan peeling in from the right edge, tapering inside frame
        dict(pts=[(1.12, 0.84), (0.96, 0.88), (0.84, 0.95), (0.76, 1.04)],
             wpts=[(0, 0.025), (0.45, 0.075), (1, 0.008)],
             shadow=hexc("#0B0B28"), light=hexc("#5B4AA2"), rim=HOTPINK,
             peak=1.0, fall=0.20, rim_strength=0.85, spec=0.3,
             edge_gain=0.85, edge_w=1.6, edge_fade=0.22,
             blur=1.4, shadow_blur=26, shadow_dist=14, seed=15),
        # E · corner peel, top-right
        dict(pts=[(1.12, 0.04), (0.96, 0.09), (0.86, 0.16), (0.80, 0.25)],
             wpts=[(0, 0.02), (0.42, 0.062), (1, 0.008)],
             shadow=hexc("#0B0B28"), light=hexc("#6C58B4"), rim=ORANGE,
             peak=1.1, fall=0.19, rim_strength=0.95, spec=0.45,
             edge_gain=0.9, edge_w=1.5, edge_fade=0.2,
             blur=2.4, shadow_blur=26, shadow_dist=15, seed=17),
    ],
    dust=dict(n=380, seed=5, colour="#FF9AD8", strength=0.65),
)

# --------------------------------------------------------------- 2. light sweep
SCENES["sweep-light"] = dict(
    bg="light", glow=0.05, glow_blur=30, bloom_thr=0.96, bloom_amt=0.12, vignette=0.08,
    bands=[
        dict(pts=[(-0.20, 1.14), (0.06, 0.80), (0.34, 0.66), (0.70, 0.66), (1.10, 0.72)],
             wpts=[(0, 0.03), (0.32, 0.16), (0.7, 0.14), (1, 0.10)],
             shadow=hexc("#DCCFE8"), light=hexc("#FFFFFF"), rim=hexc("#FFD3EC"),
             amb=0.45, peak=0.60, fall=0.72, spec=0.10, bounce=0.18,
             rim_strength=0.22, edge_gain=0.10, edge_w=1.2, edge_fade=0.34,
             shadow_strength=0.50, shadow_blur=52, shadow_dist=26,
             blur=4.5, flip=True, seed=21),
        dict(pts=[(-0.18, 0.98), (0.10, 0.62), (0.40, 0.46), (0.76, 0.44), (1.10, 0.48)],
             wpts=[(0, 0.035), (0.34, 0.17), (0.72, 0.14), (1, 0.09)],
             shadow=hexc("#D8C9E6"), light=hexc("#FFFFFF"), rim=hexc("#FFC6E4"),
             amb=0.45, peak=0.62, fall=0.68, spec=0.12, bounce=0.20,
             rim_strength=0.26, edge_gain=0.12, edge_w=1.4, edge_fade=0.28,
             shadow_strength=0.55, shadow_blur=42, shadow_dist=20,
             blur=2.2, flip=True, seed=22),
        dict(pts=[(-0.16, 0.82), (0.14, 0.46), (0.44, 0.32), (0.80, 0.30), (1.10, 0.34)],
             wpts=[(0, 0.04), (0.30, 0.18), (0.66, 0.15), (1, 0.10)],
             shadow=hexc("#E2D6EE"), light=hexc("#FFFFFF"), rim=hexc("#FFDCC0"),
             amb=0.48, peak=0.62, fall=0.62, spec=0.16, bounce=0.22,
             rim_strength=0.30, edge_gain=0.16, edge_w=1.6, edge_fade=0.24,
             shadow_strength=0.60, shadow_blur=34, shadow_dist=15,
             blur=0.6, flip=True, seed=23),
        dict(pts=[(1.16, 0.68), (0.94, 0.60), (0.78, 0.64), (0.66, 0.76)],
             wpts=[(0, 0.025), (0.45, 0.10), (1, 0.006)],
             shadow=hexc("#DCCFEA"), light=hexc("#FFFFFF"), rim=hexc("#E9C6F5"),
             amb=0.46, peak=0.60, fall=0.66, spec=0.12, bounce=0.20,
             rim_strength=0.26, edge_gain=0.12, edge_w=1.3, edge_fade=0.26,
             shadow_strength=0.50, shadow_blur=38, shadow_dist=17,
             blur=1.8, seed=24),
        dict(pts=[(1.14, 1.06), (0.90, 0.96), (0.72, 0.98), (0.58, 1.12)],
             wpts=[(0, 0.035), (0.45, 0.12), (1, 0.01)],
             shadow=hexc("#D6C7E3"), light=hexc("#FFFFFF"), rim=hexc("#F7C3DD"),
             amb=0.44, peak=0.58, fall=0.70, spec=0.10, bounce=0.18,
             rim_strength=0.20, edge_gain=0.08, edge_w=1.2, edge_fade=0.34,
             shadow_strength=0.45, shadow_blur=46, shadow_dist=20,
             blur=3.8, seed=25),
    ],
)

# ------------------------------------------------------------ 3. radial bloom
SCENES["bloom-dark"] = dict(
    bg="dark", glow=0.65, glow_blur=15, bloom_thr=0.60, bloom_amt=0.55,
    bands=radial_fan(
        origin=(1.10, 0.52),
        angles=[math.radians(a) for a in (196, 172, 148, 126, 106, 88, 70)],
        radii=[0.02, 0.22, 0.45, 0.72, 1.05, 1.45],
        curve=0.30,
        wpts=[(0, 0.006), (0.22, 0.055), (0.6, 0.045), (1, 0.006)],
        base=dict(shadow=hexc("#0B0B29"), light=hexc("#6A57B6"), rim=MAGENTA,
                  rim_strength=0.85, edge_gain=0.95, edge_w=1.7, edge_fade=0.22,
                  shadow_blur=26, shadow_dist=15),
    ),
    dust=dict(n=380, seed=9, colour="#FFA6DA", strength=0.75),
)
# vary depth + colour per petal
for _i, _b in enumerate(SCENES["bloom-dark"]["bands"]):
    _b["blur"] = 0.3 + _i * 0.55
    _b["alpha"] = 1.0 - _i * 0.04
    if _i % 3 == 1:
        _b["rim"] = ORANGE
    elif _i % 3 == 2:
        _b["rim"] = VIOLET

# ------------------------------------------------------------- 4. light curl
SCENES["curl-light"] = dict(
    bg="light", glow=0.06, glow_blur=28, bloom_thr=0.96, bloom_amt=0.12, vignette=0.08,
    bands=[
        dict(pts=[(-0.20, 0.80), (0.16, 0.56), (0.52, 0.44), (0.80, 0.42),
                  (0.98, 0.54), (0.94, 0.74), (0.74, 0.80), (0.56, 0.70)],
             wpts=[(0, 0.03), (0.22, 0.14), (0.52, 0.12), (0.78, 0.10), (1, 0.02)],
             shadow=hexc("#D9CAE6"), light=hexc("#FFFFFF"), rim=hexc("#FFC0DF"),
             amb=0.46, peak=0.62, fall=0.66, spec=0.14, bounce=0.20,
             rim_strength=0.30, edge_gain=0.16, edge_w=1.6, edge_fade=0.20,
             shadow_strength=0.58, shadow_blur=36, shadow_dist=16,
             blur=0.6, seed=31),
        dict(pts=[(-0.18, 1.12), (0.14, 0.86), (0.48, 0.76), (0.86, 0.80)],
             wpts=[(0, 0.03), (0.35, 0.13), (0.8, 0.10), (1, 0.05)],
             shadow=hexc("#D5C6E2"), light=hexc("#FFFFFF"), rim=hexc("#F0C4F0"),
             amb=0.44, peak=0.58, fall=0.70, spec=0.10, bounce=0.18,
             rim_strength=0.22, edge_gain=0.10, edge_w=1.2, edge_fade=0.32,
             shadow_strength=0.45, shadow_blur=48, shadow_dist=22,
             blur=4.2, flip=True, seed=32),
        dict(pts=[(1.12, 0.20), (0.92, 0.24), (0.78, 0.33), (0.70, 0.46)],
             wpts=[(0, 0.025), (0.45, 0.09), (1, 0.006)],
             shadow=hexc("#DDCFEA"), light=hexc("#FFFFFF"), rim=hexc("#FFD8B8"),
             amb=0.46, peak=0.60, fall=0.64, spec=0.12, bounce=0.20,
             rim_strength=0.28, edge_gain=0.12, edge_w=1.4, edge_fade=0.26,
             shadow_strength=0.48, shadow_blur=34, shadow_dist=15,
             blur=1.8, seed=33),
    ],
)


SCENES["test"] = SCENES["pages-dark"]

SCENES["test"] = dict(
    bg="dark", glow=0.5, glow_blur=12,
    bands=[
        # far, blurry sheet bottom-left
        dict(pts=[(-0.18, 1.10), (0.16, 0.90), (0.52, 0.86), (0.92, 0.98)],
             wpts=[(0, 0.03), (0.35, 0.13), (0.8, 0.10), (1, 0.02)],
             shadow=hexc("#0C0C2A"), light=hexc("#4C3E86"), rim=hexc("#B33A9E"),
             rim_strength=0.5, rim_w=0.03, edge_w=1.4, edge_gain=0.8,
             blur=3.0, shadow_blur=34, shadow_dist=20, seed=2),
        dict(pts=[(-0.16, 0.98), (0.18, 0.80), (0.50, 0.74), (0.86, 0.84)],
             wpts=[(0, 0.04), (0.4, 0.12), (0.85, 0.08), (1, 0.02)],
             shadow=hexc("#0D0D2C"), light=hexc("#58489A"), rim=hexc("#D8328F"),
             rim_strength=0.6, rim_w=0.03, edge_w=1.5, edge_gain=0.9,
             blur=1.8, shadow_blur=28, shadow_dist=18, seed=3),
        # main foreground page
        dict(pts=[(-0.14, 0.86), (0.14, 0.66), (0.44, 0.56), (0.74, 0.58), (1.06, 0.70)],
             wpts=[(0, 0.05), (0.28, 0.17), (0.62, 0.15), (0.88, 0.09), (1, 0.02)],
             shadow=hexc("#100E30"), light=hexc("#7A66C6"), rim=hexc("#FF3FA8"),
             rim_strength=0.75, rim_w=0.028, edge_w=1.8, edge_gain=1.05,
             blur=0.6, shadow_blur=24, shadow_dist=15, seed=4),
        # small peeling sliver top-right
        dict(pts=[(0.62, -0.08), (0.76, 0.02), (0.90, 0.14), (1.06, 0.20)],
             wpts=[(0, 0.01), (0.35, 0.06), (0.8, 0.04), (1, 0.01)],
             shadow=hexc("#0D0C2C"), light=hexc("#6C58B4"), rim=hexc("#FF7A1A"),
             rim_strength=0.9, rim_w=0.035, edge_w=1.5, edge_gain=1.0,
             blur=2.2, shadow_blur=26, shadow_dist=16, seed=5),
        dict(pts=[(1.12, 0.44), (0.94, 0.40), (0.80, 0.42), (0.70, 0.50)],
             wpts=[(0, 0.02), (0.4, 0.07), (1, 0.01)],
             shadow=hexc("#0D0C2C"), light=hexc("#5E4CA6"), rim=hexc("#FF3FA8"),
             rim_strength=0.85, rim_w=0.035, edge_w=1.5, edge_gain=1.0,
             blur=1.4, shadow_blur=24, shadow_dist=14, seed=6),
    ],
    dust=dict(n=300, region=(0, 0, 1, 1)),
)


if __name__ == "__main__":
    args = sys.argv[1:]
    names = list(SCENES) if (not args or args[0] == "all") else [args[0]]
    for name in names:
        out = args[1] if (len(args) > 1 and len(names) == 1) else os.path.join("_shots", f"art_{name}.png")
        save(render(SCENES[name]), out)
