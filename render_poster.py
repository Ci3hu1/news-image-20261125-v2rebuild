#!/usr/bin/env python3
"""Render the NI25 v2 poster: 46 verified stories from Wednesday
25 November 2026, one image, 1024x1024.

Daylight wire desk: paper-white ground, ink-black masthead band,
signal-red rules and square number chips, teal accents, linocut
scenes with heavy black outlines. Byte-deterministic: fixed fonts,
no randomness, no timestamps, no network.
"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
MARGIN = 20

PAPER = (250, 248, 242)
CARD = (255, 253, 248)
INK = (16, 16, 16)
RED = (201, 29, 29)
TEAL = (14, 122, 120)
GREY = (110, 108, 100)
LIGHT = (232, 228, 218)
LAND = (226, 222, 210)
SEA = (238, 240, 236)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_font_cache = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _font_cache:
        name = "DejaVuSerif-Bold.ttf" if serif else (
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _font_cache[key]


# ---------------------------------------------------------------- data
# (n, region, city, lon, lat, poster title, scene kind)
HEROES = [
    (1, "OCEANIA", "Canberra", 149.13, -35.28,
     "CPI jumps to 4.9%, jobless 4.9%",
     "Australia — stagflation fears", "chart"),
    (2, "MIDDLE EAST", "Gaza City", 34.47, 31.50,
     "Israel launches ground offensive in central Gaza",
     "First major push beyond the Yellow Line", "ground"),
    (3, "AMERICAS", "Langley", -77.14, 38.95,
     "CIA hit by cyberattack",
     "Unclassified system breached — AP", "lock"),
]

FEATURED = [
    (4, "ASIA", "Mumbai", 72.88, 19.08,
     "Sooryavanshi, 15, hits 204 off 53", "bat"),
    (5, "OCEANIA", "Canberra", 149.13, -35.28,
     "Australia says sorry to LGBTQ veterans", "sorry"),
    (6, "ASIA", "New Delhi", 77.21, 28.61,
     "Modi, Merz talk up partnership", "handshake"),
    (7, "MIDDLE EAST", "Sanaa", 44.19, 15.35,
     "Houthis threaten Saudi ports", "flame"),
    (8, "MIDDLE EAST", "Doha", 51.53, 25.29,
     "Qatar urges restraint on Iran", "speech"),
    (9, "EUROPE", "London", -0.13, 51.51,
     "Two held over William home break-in", "home"),
    (10, "AFRICA", "Ituri", 30.25, 1.57,
     "WHO pulls staff from Ebola hospital", "cross"),
    (11, "ASIA", "Chandigarh", 76.78, 30.73,
     "Akalis & BJP reunite for Punjab polls", "ballot"),
    (12, "OCEANIA", "Wellington", 174.78, -41.29,
     "Flavell slams ACT Maori seats vote", "gavel"),
    (13, "GLOBAL", "New York", -74.00, 40.71,
     "Gold slips as US inflation looms", "coin"),
]

ALSO_ON = [
    (14, "Gukesh holds Sindarov in title Game 1", 80.27, 13.08),
    (15, "Sensex drops 1,484; Nifty below 25,400", 72.88, 19.08),
    (16, "Houthis report deaths after Saudi strikes", 44.50, 14.50),
    (17, "Ras Al Khaimah crash kills 11", 55.98, 25.67),
    (18, "Nepal FM hails PM Shah's India visit", 85.32, 27.72),
    (19, "India space economy to hit $40-45bn", 77.21, 28.61),
    (20, "APEDA ships first frozen peas to Qatar", 51.53, 25.29),
    (21, "Ben Stokes signs up for IPL 2027 auction", 72.88, 19.08),
    (22, "Nvidia's Huang admitted code breach", -121.96, 37.35),
    (23, "Putin: retaliation 'inevitable' after oil hits", 37.62, 55.76),
    (24, "Russia calls Ukraine drone hits 'terrorism'", 20.00, 58.00),
    (25, "Saudi coalition condemns Riyadh tower attack", 46.68, 24.71),
    (26, "Iraqi PM orders Baghdad to run Kurdish oilfields", 44.37, 33.31),
    (27, "Israeli drones kill seven in central Gaza", 34.47, 31.50),
    (28, "Gaza's displaced children mark Children's Day", 34.39, 31.45),
    (29, "Zimbabwean convicted in SA over Ukraine bid", 28.05, -26.20),
    (30, "Gaza toll 74,746, WAFA says", 34.47, 31.50),
    (31, "Anthropic shares fall below $83 IPO price", -122.42, 37.77),
    (32, "Rahul Gandhi backs strong India-Israel ties", 77.21, 28.61),
    (33, "Pacific states step up El Nino response", 178.44, -17.71),
    (34, "Outrage in PNG after five women buried alive", 147.15, -9.44),
    (35, "Probe call after West Papuan leader dies", 140.72, -2.53),
    (36, "NZ dollar hits 17-year low", 174.78, -41.29),
    (37, "Waddington flies NZ flag at Miss Universe", -66.07, 18.47),
    (38, "AI blamed as cyber breaches surge", 174.78, -41.29),
    (39, "World's deepest volcanic blast found", 145.20, 11.35),
    (40, "Star system 'should not exist' found", 0.00, 0.00),
    (41, "One third of attacks on children in Palestine", 34.47, 31.50),
    (42, "German GDP +0.1%, revised down - Destatis", 13.40, 52.52),
    (43, "Houthis claim refinery, Riyadh strikes", 50.06, 26.64),
    (44, "China probes Politburo member Chen Jining", 116.41, 39.90),
    (45, "Puigdemont to return to Spain on Dec 12", 2.17, 41.39),
    (46, "Asian stocks slide on tariff threats", 126.98, 37.57),
]

KPIS = [
    ("4.9%", "AU CPI"),
    ("4.9%", "AU JOBLESS"),
    ("204", "OFF 53 BALLS - AGE 15"),
    ("1,484", "SENSEX PTS LOST"),
    ("11", "RAK CRASH DEAD"),
    ("7", "KILLED IN GAZA"),
]

TIMELINE = [
    ("00:30 GMT", "Australia CPI 4.9% lands"),
    ("MORNING", "Canberra apologises to LGBTQ veterans"),
    ("MIDDAY", "Sooryavanshi hits 204 off 53 balls"),
    ("AFTERNOON", "German GDP +0.1%"),
    ("19:45 CET", "ESA unveils Hera Dimorphos close-ups"),
    ("NIGHT", "CIA breach reported"),
]

DATE_CHECK = ("DATE CHECK - NOT IN THIS EDITION",
              "Nepal 5.6 quake (Tue 24 Nov)  -  Huawei guilty verdict (Tue 24 Nov)")

FOOTER_LINES = [
    "Every story first reported Wednesday 25 November 2026 - verified on the outlet's own page.",
    "Sources: Reuters - AP - Destatis - Al Jazeera - BBC - RNZ - AFP  |  46 stories - 7 regions - Daylight wire desk",
]

# Simplified continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-70, 42),
     (-75, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 29), (-97, 26),
     (-105, 23), (-110, 24), (-115, 30), (-125, 40), (-125, 49),
     (-135, 58), (-155, 58), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-55, 76), (-58, 70)],
    # South America
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41),
     (-70, -50), (-73, -54), (-70, -40), (-72, -20), (-77, -12), (-80, -3)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 70),
     (40, 68), (45, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40),
     (19, 42), (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36)],
    # Africa
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -26),
     (26, -34), (19, -35), (15, -27), (12, -18), (9, -1), (9, 4),
     (-8, 4), (-13, 8)],
    # Asia
    [(30, 62), (40, 68), (60, 69), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (155, 50), (142, 45), (140, 40), (135, 35), (130, 32), (127, 35),
     (122, 38), (120, 32), (115, 25), (110, 20), (108, 12), (105, 8),
     (100, 7), (98, 12), (95, 16), (90, 22), (85, 20), (80, 15), (77, 8),
     (75, 12), (70, 20), (65, 25), (60, 25), (55, 26), (52, 28), (50, 30),
     (48, 30), (45, 30), (42, 35), (38, 36), (36, 36), (33, 38), (30, 40),
     (28, 42), (30, 46), (32, 50), (30, 55)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -22),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
]

# ---------------------------------------------------------------- helpers
AUDIT = []  # (text, text_bbox, container_bbox) for the clearance check


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def fit_text(draw, s, fnt, max_w):
    """Word-aware truncation with an ellipsis so text never overflows."""
    if text_w(draw, s, fnt) <= max_w:
        return s
    words = s.split(" ")
    out = ""
    for w_ in words:
        trial = (out + " " + w_).strip()
        if text_w(draw, trial + " ...", fnt) <= max_w:
            out = trial
        else:
            break
    if not out:
        # Single long word: cut characters.
        while out == "" and s:
            s = s[:-1]
            if text_w(draw, s + "...", fnt) <= max_w:
                out = s
        return (out + "...") if out else "..."
    return out + " ..."


def wrap_lines(draw, s, fnt, max_w, max_lines):
    """Greedy word wrap; ellipsis on the last line if it still overflows."""
    words = s.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit_text(draw, lines[-1], fnt, max_w)
    return lines


def draw_checked(draw, xy, s, fnt, fill, container):
    """Draw text and record its bbox against its container for clearance."""
    draw.text(xy, s, font=fnt, fill=fill)
    bbox = draw.textbbox(xy, s, font=fnt)
    AUDIT.append((s, bbox, container))


def clearance_violations():
    """Count recorded texts whose bbox touches or escapes its container."""
    bad = 0
    for _s, (x0, y0, x1, y1), (cx0, cy0, cx1, cy1) in AUDIT:
        if x0 < cx0 + 1 or y0 < cy0 + 1 or x1 > cx1 - 1 or y1 > cy1 - 1:
            bad += 1
    return bad


def chip(draw, x, y, size, number, fnt=None):
    """Signal-red square number chip with a white centred number."""
    fnt = fnt or font(10, bold=True)
    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=RED)
    draw.rectangle([x, y, x + size - 1, y + size - 1], outline=INK, width=1)
    label = str(number)
    tw = draw.textlength(label, font=fnt)
    th = fnt.getbbox(label)[3] - fnt.getbbox(label)[1]
    draw.text((x + (size - tw) / 2, y + (size - th) / 2 - 1),
              label, font=fnt, fill=(255, 255, 255))

# ---------------------------------------------------------------- scenes
def draw_motif(draw, box, kind, label=None):
    """Linocut motif inside box (x0, y0, x1, y1): heavy black outlines,
    flat red/teal/paper fills. label is drawn only in hero-size scenes."""
    x0, y0, x1, y1 = box
    w_, h_ = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    o = 3  # outline width
    if kind == "chart":
        base = y1 - 8
        bars = [(0.12, 0.35), (0.32, 0.55), (0.52, 0.45), (0.72, 0.80)]
        for fx, fh in bars:
            bx = x0 + fx * w_
            bw = w_ * 0.14
            draw.rectangle([bx, base - fh * (h_ - 16), bx + bw, base],
                           fill=TEAL, outline=INK, width=o)
        draw.line([(x0 + 4, base), (x1 - 4, base)], fill=INK, width=o)
        draw.line([(x0 + 4, base), (x0 + w_ * 0.86, y0 + 8)],
                  fill=RED, width=3)
    elif kind == "ground":
        draw.rectangle([x0, y0 + h_ * 0.55, x1, y1], fill=INK)
        for fx, fw, fh in [(0.08, 0.16, 0.34), (0.30, 0.12, 0.46),
                           (0.48, 0.18, 0.28), (0.70, 0.14, 0.40)]:
            bx = x0 + fx * w_
            draw.rectangle([bx, y0 + h_ * 0.55 - fh * h_ * 0.55,
                            bx + fw * w_, y0 + h_ * 0.55],
                           fill=PAPER, outline=INK, width=o)
        draw.line([(x0 + 6, y0 + h_ * 0.30), (x1 - w_ * 0.18, y0 + h_ * 0.30)],
                  fill=RED, width=4)
        draw.polygon([(x1 - w_ * 0.18, y0 + h_ * 0.30 - 7),
                      (x1 - w_ * 0.18, y0 + h_ * 0.30 + 7),
                      (x1 - 4, y0 + h_ * 0.30)], fill=RED)
    elif kind == "lock":
        bw, bh = w_ * 0.42, h_ * 0.46
        bx0, by0 = cx - bw / 2, cy - bh * 0.28
        draw.arc([cx - bw * 0.32, by0 - bh * 0.55, cx + bw * 0.32,
                  by0 + bh * 0.10], 180, 360, fill=INK, width=4)
        draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=4,
                               fill=RED, outline=INK, width=o)
        draw.ellipse([cx - 4, by0 + bh * 0.30, cx + 4, by0 + bh * 0.30 + 8],
                     fill=PAPER)
        draw.line([(cx, by0 + bh * 0.36), (cx, by0 + bh * 0.62)],
                  fill=PAPER, width=3)
        draw.line([(bx0 - 8, by0 + bh + 8), (bx0 + bw + 8, by0 - 6)],
                  fill=INK, width=2)
    elif kind == "bat":
        draw.line([(x0 + w_ * 0.18, y1 - 8), (x0 + w_ * 0.78, y0 + 10)],
                  fill=INK, width=5)
        draw.ellipse([x0 + w_ * 0.62, y0 + 4, x0 + w_ * 0.92, y0 + h_ * 0.42],
                     fill=RED, outline=INK, width=o)
        draw.ellipse([x0 + w_ * 0.08, y0 + h_ * 0.45, x0 + w_ * 0.30,
                      y0 + h_ * 0.72], fill=TEAL, outline=INK, width=o)
    elif kind == "sorry":
        draw.rectangle([x0 + w_ * 0.10, y0 + h_ * 0.18,
                        x1 - w_ * 0.10, y0 + h_ * 0.72],
                       fill=PAPER, outline=INK, width=o)
        draw.line([(x0 + w_ * 0.22, y0 + h_ * 0.36),
                   (x1 - w_ * 0.22, y0 + h_ * 0.36)], fill=TEAL, width=3)
        draw.line([(x0 + w_ * 0.22, y0 + h_ * 0.52),
                   (x1 - w_ * 0.32, y0 + h_ * 0.52)], fill=TEAL, width=3)
    elif kind == "handshake":
        draw.ellipse([x0 + w_ * 0.12, cy - h_ * 0.22, x0 + w_ * 0.42,
                      cy + h_ * 0.22], fill=TEAL, outline=INK, width=o)
        draw.ellipse([x1 - w_ * 0.42, cy - h_ * 0.22, x1 - w_ * 0.12,
                      cy + h_ * 0.22], fill=RED, outline=INK, width=o)
        draw.line([(x0 + w_ * 0.38, cy), (x1 - w_ * 0.38, cy)],
                  fill=INK, width=3)
    elif kind == "flame":
        draw.polygon([(cx, y0 + 4), (cx + w_ * 0.22, cy),
                      (cx + w_ * 0.10, cy + h_ * 0.18),
                      (cx + w_ * 0.30, y1 - 6), (cx - w_ * 0.30, y1 - 6),
                      (cx - w_ * 0.10, cy + h_ * 0.18),
                      (cx - w_ * 0.22, cy)], fill=RED, outline=INK)
        draw.ellipse([cx - w_ * 0.08, cy, cx + w_ * 0.08, cy + h_ * 0.22],
                     fill=(255, 210, 60))
    elif kind == "speech":
        draw.rectangle([x0 + w_ * 0.10, y0 + h_ * 0.14,
                        x1 - w_ * 0.10, y0 + h_ * 0.66],
                       fill=PAPER, outline=INK, width=o)
        draw.polygon([(x0 + w_ * 0.28, y0 + h_ * 0.66),
                      (x0 + w_ * 0.44, y0 + h_ * 0.66),
                      (x0 + w_ * 0.30, y1 - 4)], fill=PAPER, outline=INK)
        draw.line([(x0 + w_ * 0.24, y0 + h_ * 0.34),
                   (x1 - w_ * 0.24, y0 + h_ * 0.34)], fill=TEAL, width=3)
        draw.line([(x0 + w_ * 0.24, y0 + h_ * 0.50),
                   (x1 - w_ * 0.36, y0 + h_ * 0.50)], fill=TEAL, width=3)
    elif kind == "home":
        draw.polygon([(x0 + 4, cy), (cx, y0 + 4), (x1 - 4, cy)],
                     fill=RED, outline=INK)
        draw.rectangle([x0 + w_ * 0.18, cy, x1 - w_ * 0.18, y1 - 4],
                       fill=PAPER, outline=INK, width=o)
        draw.rectangle([cx - 5, y1 - h_ * 0.34, cx + 5, y1 - 4],
                       fill=INK)
    elif kind == "cross":
        draw.rectangle([cx - 5, y0 + 4, cx + 5, y1 - 4], fill=TEAL,
                       outline=INK, width=2)
        draw.rectangle([x0 + 6, cy - 5, x1 - 6, cy + 5], fill=TEAL,
                       outline=INK, width=2)
    elif kind == "ballot":
        draw.rectangle([x0 + w_ * 0.14, y0 + h_ * 0.30, x1 - w_ * 0.14,
                        y1 - 4], fill=PAPER, outline=INK, width=o)
        draw.line([(x0 + w_ * 0.30, y0 + 4), (x1 - w_ * 0.30, y0 + 4)],
                  fill=INK, width=3)
        draw.line([(cx - 6, y0 + h_ * 0.52), (cx - 1, y0 + h_ * 0.66),
                   (cx + 7, y0 + h_ * 0.40)], fill=RED, width=3)
    elif kind == "gavel":
        draw.line([(x0 + w_ * 0.16, y1 - 8), (x1 - w_ * 0.16, y0 + 10)],
                  fill=INK, width=4)
        draw.rectangle([x0 + w_ * 0.52, y0 + 4, x1 - w_ * 0.08,
                        y0 + h_ * 0.34], fill=RED, outline=INK, width=o)
    elif kind == "coin":
        draw.ellipse([cx - h_ * 0.30, cy - h_ * 0.30, cx + h_ * 0.30,
                      cy + h_ * 0.30], fill=(255, 210, 60), outline=INK,
                     width=o)
        draw.text((cx - 5, cy - 10), "$", font=font(16, bold=True), fill=INK)
    if label and h_ >= 60:
        lf = font(15, bold=True)
        tw = draw.textlength(label, font=lf)
        tx0, ty0 = cx - tw / 2 - 5, y0 + h_ - 22
        draw.rectangle([tx0, ty0, tx0 + tw + 10, ty0 + 18],
                       fill=PAPER, outline=INK, width=2)
        draw.text((cx - tw / 2, ty0 + 1), label, font=lf, fill=INK)


# ---------------------------------------------------------------- cards
def draw_hero(draw, box, story):
    n, _region, _city, _lon, _lat, title, sub, kind = story
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 4], fill=RED)
    scene = (x0 + 8, y0 + 12, x1 - 8, y0 + 92)
    draw.rectangle(scene, fill=SEA, outline=INK, width=2)
    label = {1: "4.9%", 2: "GAZA", 3: "CIA"}.get(n)
    draw_motif(draw, scene, kind, label=label)
    chip(draw, x0 + 8, y0 + 100, 20, n)
    tx = x0 + 34
    lines = wrap_lines(draw, title, font(16, bold=True), x1 - tx - 8, 2)
    ly = y0 + 98
    for ln in lines:
        draw_checked(draw, (tx, ly), ln, font(16, bold=True), INK,
                     (x0 + 8, y0 + 96, x1 - 8, y0 + 146))
        ly += 19
    draw_checked(draw, (tx, y0 + 150), fit_text(draw, sub, font(11), x1 - tx - 8),
                 font(11), GREY, (x0 + 8, y0 + 148, x1 - 8, y0 + 168))


def draw_featured(draw, box, story):
    n, _region, _city, _lon, _lat, title, kind = story
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=1)
    scene = (x0 + 1, y0 + 1, x1 - 1, y0 + 27)
    draw.rectangle(scene, fill=SEA)
    draw_motif(draw, scene, kind)
    chip(draw, x0 + 5, y0 + 31, 16, n, fnt=font(9, bold=True))
    tx = x0 + 26
    lines = wrap_lines(draw, title, font(11, bold=True), x1 - tx - 6, 2)
    ly = y0 + 30
    for ln in lines:
        draw_checked(draw, (tx, ly), ln, font(11, bold=True), INK,
                     (x0 + 4, y0 + 29, x1 - 6, y0 + 60))
        ly += 14
    draw_checked(draw, (tx, y0 + 62),
                 fit_text(draw, _region, font(9), x1 - tx - 6),
                 font(9), GREY, (x0 + 4, y0 + 61, x1 - 6, y0 + 80))

# ---------------------------------------------------------------- sections
def draw_masthead(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    draw.rectangle([x0, y, x1, y + 76], fill=INK)
    draw_checked(draw, (x0 + 14, y + 10), "THE DAYLIGHT WIRE",
                 font(38, bold=True, serif=True), (255, 255, 255),
                 (x0 + 10, y + 6, x0 + 560, y + 56))
    draw_checked(draw, (x0 + 16, y + 54), "WEDNESDAY 25 NOVEMBER 2026",
                 font(15, bold=True), (255, 255, 255),
                 (x0 + 12, y + 50, x0 + 560, y + 74))
    right = "46 STORIES"
    tw = draw.textlength(right, font=font(24, bold=True))
    draw_checked(draw, (x1 - 14 - tw, y + 8), right, font(24, bold=True),
                 RED, (x1 - 200, y + 4, x1 - 10, y + 40))
    sub = "ALL FROM WEDNESDAY"
    tw2 = draw.textlength(sub, font=font(12, bold=True))
    draw_checked(draw, (x1 - 14 - tw2, y + 44), sub, font(12, bold=True),
                 (255, 255, 255), (x1 - 200, y + 40, x1 - 10, y + 62))
    draw.rectangle([x0, y + 76, x1, y + 79], fill=RED)
    return y + 84


def draw_timeline(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    col_w = (x1 - x0) / 6
    draw.line([(x0, y + 16), (x1, y + 16)], fill=RED, width=2)
    for i, (when, what) in enumerate(TIMELINE):
        cx = x0 + i * col_w
        draw.ellipse([cx + 2, y + 11, cx + 12, y + 21], fill=RED,
                     outline=INK, width=1)
        draw_checked(draw, (cx + 16, y), when, font(11, bold=True), RED,
                     (cx + 14, y - 2, cx + col_w - 4, y + 14))
        lines = wrap_lines(draw, what, font(10), col_w - 18, 2)
        ly = y + 24
        for ln in lines:
            draw_checked(draw, (cx + 2, ly), ln, font(10), INK,
                         (cx, y + 22, cx + col_w - 4, y + 50))
            ly += 12
    return y + 54


def draw_kpi(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    draw.rectangle([x0, y, x1, y + 62], fill=CARD, outline=INK, width=2)
    cell = (x1 - x0) / 6
    for i, (num, label) in enumerate(KPIS):
        cx = x0 + i * cell
        if i:
            draw.line([(cx, y + 8), (cx, y + 54)], fill=LIGHT, width=1)
        draw_checked(draw, (cx + 12, y + 6), num, font(24, bold=True),
                     RED if i % 2 == 0 else INK,
                     (cx + 8, y + 2, cx + cell - 8, y + 36))
        draw_checked(draw, (cx + 12, y + 38),
                     fit_text(draw, label, font(9, bold=True), cell - 24),
                     font(9, bold=True), GREY,
                     (cx + 8, y + 36, cx + cell - 8, y + 56))
    return y + 68


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (83.0 - lat) / 138.0 * (y1 - y0)
    return px, py


def draw_map(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    draw_checked(draw, (x0 + 2, y), "WHERE IT HAPPENED - 46 STORIES ON THE MAP",
                 font(12, bold=True), INK, (x0, y - 2, x0 + 420, y + 16))
    box = (x0, y + 20, x1, y + 146)
    draw.rectangle(box, fill=SEA, outline=INK, width=2)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=INK)
    # Stagger pins/dots that share a city so numbers never collide.
    seen = {}

    def place(lon, lat):
        key = (round(lon, 1), round(lat, 1))
        k = seen.get(key, 0)
        seen[key] = k + 1
        px, py = project(lon, lat, box)
        return px + (k % 3) * 8 - 8, py + (k // 3) * 8 - 4

    for n, _r, _c, lon, lat, _t, _s, _k in HEROES:
        px, py = place(lon, lat)
        s = 15
        draw.rectangle([px - s / 2, py - s / 2, px + s / 2, py + s / 2],
                       fill=RED, outline=INK, width=1)
        label = str(n)
        fnt = font(9, bold=True)
        tw = draw.textlength(label, font=fnt)
        draw.text((px - tw / 2, py - 6), label, font=fnt,
                  fill=(255, 255, 255))
    for n, _r, _c, lon, lat, _t, _k in FEATURED:
        px, py = place(lon, lat)
        s = 15
        draw.rectangle([px - s / 2, py - s / 2, px + s / 2, py + s / 2],
                       fill=RED, outline=INK, width=1)
        label = str(n)
        fnt = font(9, bold=True)
        tw = draw.textlength(label, font=fnt)
        draw.text((px - tw / 2, py - 6), label, font=fnt,
                  fill=(255, 255, 255))
    for n, _t, lon, lat in ALSO_ON:
        px, py = place(lon, lat)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=TEAL,
                     outline=INK, width=1)
    draw_checked(draw, (x0 + 2, y + 150),
                 "RED SQUARES 1-13 FEATURED  -  TEAL DOTS 14-46 ALSO ON  -  7 REGIONS",
                 font(10, bold=True), GREY,
                 (x0, y + 148, x1, y + 164))
    return y + 168


def draw_also_on(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    draw_checked(draw, (x0 + 2, y), "ALSO ON WEDNESDAY",
                 font(13, bold=True), INK, (x0, y - 2, x0 + 240, y + 16))
    draw.rectangle([x0, y + 18, x1, y + 20], fill=RED)
    col_w = (x1 - x0) / 3
    rows = 11
    for col in range(3):
        items = ALSO_ON[col * rows:(col + 1) * rows]
        cx = x0 + col * col_w
        for r, (n, title, _lon, _lat) in enumerate(items):
            ry = y + 26 + r * 12
            chip(draw, cx, ry, 11, n, fnt=font(8, bold=True))
            draw_checked(draw, (cx + 15, ry - 1),
                         fit_text(draw, title, font(11), col_w - 18),
                         font(11), INK, (cx + 14, ry - 3, cx + col_w - 2, ry + 13))
    return y + 26 + rows * 12 + 4


def draw_date_check(draw, y):
    x0, x1 = MARGIN, W - MARGIN
    title, body = DATE_CHECK
    draw.rectangle([x0, y, x1, y + 32], outline=RED, width=2)
    draw_checked(draw, (x0 + 10, y + 8), title, font(11, bold=True), RED,
                 (x0 + 6, y + 4, x0 + 330, y + 28))
    draw_checked(draw, (x0 + 330, y + 8),
                 fit_text(draw, body, font(11), x1 - x0 - 344),
                 font(11), INK, (x0 + 326, y + 4, x1 - 6, y + 28))
    return y + 38


def draw_footer(draw, y):
    for ln in FOOTER_LINES:
        fnt = font(10)
        tw = draw.textlength(ln, font=fnt)
        draw_checked(draw, ((W - tw) / 2, y), ln, fnt, GREY,
                     (MARGIN, y - 2, W - MARGIN, y + 13))
        y += 14
    return y


# ---------------------------------------------------------------- render
def render():
    AUDIT.clear()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 16
    y = draw_masthead(draw, y)
    y = draw_timeline(draw, y + 6)
    # Heroes: 3 across.
    hx0, hx1 = MARGIN, W - MARGIN
    hw = (hx1 - hx0 - 16) / 3
    for i, story in enumerate(HEROES):
        draw_hero(draw, (hx0 + i * (hw + 8), y + 4,
                         hx0 + i * (hw + 8) + hw, y + 174), story)
    y += 180
    # Featured: 2 rows x 5.
    fw = (hx1 - hx0 - 32) / 5
    for row in range(2):
        for col in range(5):
            story = FEATURED[row * 5 + col]
            draw_featured(draw, (hx0 + col * (fw + 8), y + row * 92,
                                 hx0 + col * (fw + 8) + fw, y + row * 92 + 84),
                          story)
    y += 192
    y = draw_kpi(draw, y)
    y = draw_map(draw, y + 6)
    y = draw_also_on(draw, y + 6)
    y = draw_date_check(draw, y + 4)
    y = draw_footer(draw, y + 4)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150,
                                             threshold=0))
    return img


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    img = render()
    entry = os.path.join(out_dir, "entry.png")
    img.save(entry, format="PNG")
    preview = img.resize((300, 300), Image.LANCZOS)
    preview.save(os.path.join(out_dir, "preview-300.png"), format="PNG")
    print("entry.png bytes:", os.path.getsize(entry))
    print("clearance violations:", clearance_violations())


if __name__ == "__main__":
    main()
