#!/usr/bin/env python3
"""Render entry.png for news-image-20261123.

A one-page newspaper front page summing up the world news of
Monday 23 November 2026: seven stories, drawn entirely with Pillow
shapes and DejaVu text. No photos, no downloaded art, no network.
Run:  python3 gen_image.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ---------------------------------------------------------
CREAM = (250, 246, 236)
PAPER = (255, 253, 247)
NAVY = (13, 26, 61)
NAVY_SOFT = (28, 44, 92)
GOLD = (233, 181, 45)
RED = (178, 34, 34)
TEAL = (14, 106, 94)
TEAL_DARK = (9, 82, 72)
GREEN = (46, 139, 87)
BLUE = (31, 92, 145)
INK = (24, 24, 24)
GREY = (92, 92, 92)
LINE = (205, 198, 184)
SKY = (214, 230, 240)
NIGHT = (16, 24, 54)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill, leading):
    """Draw wrapped paragraph; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fitted(draw, text, fnt, max_w, fill, xy, anchor="la"):
    """Draw one line, shrinking the font until it fits (never below 60%)."""
    size = fnt.size
    while size > int(fnt.size * 0.6):
        trial = font("DejaVuSerif-Bold.ttf", size) if "Serif" in str(fnt.getname()) else font("DejaVuSans-Bold.ttf", size)
        if draw.textlength(text, font=trial) <= max_w:
            draw.text(xy, text, font=trial, fill=fill, anchor=anchor)
            return size
        size -= 1
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)
    return fnt.size


def panel(draw, x, y, w, h, fill=PAPER, outline=LINE, width=2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=fill, outline=outline, width=width)


def kicker(draw, x, y, text, color):
    draw.text((x, y), text, font=SANS_B(17), fill=color)


def headline(draw, x, y, text, size, max_w, leading, fill=INK):
    fnt = SERIF_B(size)
    return para(draw, x, y, text, fnt, max_w, fill, leading)


def body(draw, x, y, text, max_w, size=19, leading=25):
    return para(draw, x, y, text, SANS(size), max_w, INK, leading)


# ---- canvas ----------------------------------------------------------
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- masthead --------------------------------------------------------
d.rectangle([0, 0, W, 106], fill=NAVY)
d.text((W // 2, 16), "THE WORLD IN ONE PICTURE",
       font=SERIF_B(44), fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 66), "MONDAY  23  NOVEMBER  2026",
       font=SANS_B(26), fill=GOLD, anchor="ma")
d.rectangle([0, 106, W, 112], fill=GOLD)

# ---- row 1: lead story (COP31) + Hormuz ------------------------------
ROW1_Y, ROW1_H = 126, 322
ART_H = 128

# --- lead panel ---
LX, LW = 24, 566
panel(d, LX, ROW1_Y, LW, ROW1_H)
d.rounded_rectangle([LX, ROW1_Y, LX + LW, ROW1_Y + ART_H], radius=10, fill=TEAL)
d.rectangle([LX, ROW1_Y + ART_H - 10, LX + LW, ROW1_Y + ART_H], fill=TEAL)
# sun dot
d.ellipse([LX + 22, ROW1_Y + 18, LX + 52, ROW1_Y + 48], fill=GOLD)
# globe: circle with meridians and a red slash for the failed deal
gx, gy, gr = LX + 150, ROW1_Y + ART_H // 2, 52
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(32, 148, 128),
          outline=(255, 255, 255), width=3)
d.ellipse([gx - 26, gy - gr, gx + 26, gy + gr], outline=(255, 255, 255), width=2)
d.line([gx - gr, gy, gx + gr, gy], fill=(255, 255, 255), width=2)
d.arc([gx - gr, gy - 26, gx + gr, gy + 26], 200, 340, fill=(255, 255, 255), width=2)
d.line([gx - 38, gy + 34, gx + 38, gy - 34], fill=(214, 48, 49), width=6)
# document stamped NO DEAL
dx, dy = LX + 392, ROW1_Y + 16
d.rounded_rectangle([dx, dy, dx + 132, dy + 96], radius=6, fill=(255, 255, 255))
for i in range(3):
    yy = dy + 18 + i * 16
    d.line([dx + 14, yy, dx + 118, yy], fill=(150, 150, 150), width=3)
d.line([dx + 14, dy + 66, dx + 80, dy + 66], fill=RED, width=4)
d.text((dx + 66, dy + 74), "NO DEAL", font=SANS_B(20), fill=RED, anchor="ma")
# lead text
ty = ROW1_Y + ART_H + 14
kicker(d, LX + 18, ty, "CLIMATE  \u2022  LEAD STORY", RED)
ty += 26
ty = headline(d, LX + 18, ty, "COP31 collapses \u2014 and the blame begins",
              34, LW - 36, 40)
ty += 6
body(d, LX + 18, ty,
     "The UN climate talks end with no deal after the draft dropped "
     "every mention of fossil fuels.", LW - 36)

# --- Hormuz panel ---
HX, HW = 604, 396
panel(d, HX, ROW1_Y, HW, ROW1_H)
d.rounded_rectangle([HX, ROW1_Y, HX + HW, ROW1_Y + ART_H], radius=10, fill=NIGHT)
d.rectangle([HX, ROW1_Y + ART_H - 10, HX + HW, ROW1_Y + ART_H], fill=NIGHT)
# stars and moon
for sx, sy in [(HX + 30, ROW1_Y + 18), (HX + 90, ROW1_Y + 34),
               (HX + 210, ROW1_Y + 14), (HX + 300, ROW1_Y + 30),
               (HX + 350, ROW1_Y + 16)]:
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
d.ellipse([HX + 318, ROW1_Y + 22, HX + 352, ROW1_Y + 56], fill=(238, 230, 200))
# tanker hull with containers and a flame
d.polygon([(HX + 18, ROW1_Y + 96), (HX + 378, ROW1_Y + 96),
           (HX + 352, ROW1_Y + 122), (HX + 44, ROW1_Y + 122)], fill=(72, 84, 110))
d.rectangle([HX + 52, ROW1_Y + 66, HX + 118, ROW1_Y + 96], fill=(214, 110, 44))
d.rectangle([HX + 128, ROW1_Y + 66, HX + 194, ROW1_Y + 96], fill=(62, 120, 178))
d.rectangle([HX + 300, ROW1_Y + 70, HX + 352, ROW1_Y + 96], fill=(200, 200, 200))
d.polygon([(HX + 218, ROW1_Y + 92), (HX + 238, ROW1_Y + 44),
           (HX + 258, ROW1_Y + 92)], fill=(247, 147, 30))
d.polygon([(HX + 228, ROW1_Y + 92), (HX + 238, ROW1_Y + 62),
           (HX + 248, ROW1_Y + 92)], fill=(247, 220, 60))
for cx, cy, cr in [(HX + 250, ROW1_Y + 30, 14), (HX + 272, ROW1_Y + 20, 18),
                   (HX + 296, ROW1_Y + 32, 12)]:
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(110, 110, 110))
# wave marks
for wx in range(HX + 24, HX + HW - 20, 34):
    d.arc([wx, ROW1_Y + ART_H - 16, wx + 26, ROW1_Y + ART_H + 2],
          180, 360, fill=(140, 180, 220), width=3)
ty = ROW1_Y + ART_H + 14
kicker(d, HX + 18, ty, "GULF  \u2022  STRAIT OF HORMUZ", BLUE)
ty += 26
ty = headline(d, HX + 18, ty, "Hormuz attacks hit a wartime high",
              30, HW - 36, 36)
ty += 6
body(d, HX + 18, ty,
     "Shipping attacks are at their highest level since the US\u2013Iran "
     "war began, maritime data shows.", HW - 36)

# ---- row 2: Korea, cricket, world in brief ---------------------------
ROW2_Y, ROW2_H = 462, 330
PW = 316
P1X, P2X, P3X = 24, 354, 684

# --- Korea panel ---
panel(d, P1X, ROW2_Y, PW, ROW2_H)
d.rounded_rectangle([P1X, ROW2_Y, P1X + PW, ROW2_Y + 118], radius=10, fill=SKY)
d.rectangle([P1X, ROW2_Y + 108, P1X + PW, ROW2_Y + 118], fill=SKY)
# graduation cap
cx, cy = P1X + PW // 2, ROW2_Y + 44
d.polygon([(cx - 78, cy), (cx, cy - 26), (cx + 78, cy), (cx, cy + 26)],
          fill=NAVY)
d.polygon([(cx - 42, cy + 8), (cx + 42, cy + 8), (cx + 42, cy + 34),
           (cx - 42, cy + 34)], fill=(20, 34, 74))
d.line([cx + 78, cy, cx + 78, cy + 34], fill=GOLD, width=3)
d.ellipse([cx + 72, cy + 34, cx + 84, cy + 46], fill=GOLD)
# exam card with AI crossed out
d.rounded_rectangle([cx - 62, cy + 44, cx + 62, cy + 74], radius=6,
                    fill=(255, 255, 255), outline=GREY, width=2)
d.text((cx, cy + 50), "AI", font=SANS_B(24), fill=INK, anchor="ma")
d.line([cx - 52, cy + 70, cx + 52, cy + 50], fill=RED, width=5)
d.line([cx - 52, cy + 50, cx + 52, cy + 70], fill=RED, width=5)
ty = ROW2_Y + 118 + 14
kicker(d, P1X + 16, ty, "SOUTH KOREA", BLUE)
ty += 26
ty = headline(d, P1X + 16, ty, "Minister quits over AI exam cheating",
              25, PW - 32, 30)
ty += 6
body(d, P1X + 16, ty,
     "South Korea\u2019s education minister resigns after an AI-driven "
     "cheating scandal in the national exams.", PW - 32, size=18, leading=23)

# --- cricket panel ---
panel(d, P2X, ROW2_Y, PW, ROW2_H)
d.rounded_rectangle([P2X, ROW2_Y, P2X + PW, ROW2_Y + 118], radius=10, fill=GREEN)
d.rectangle([P2X, ROW2_Y + 108, P2X + PW, ROW2_Y + 118], fill=GREEN)
# outfield, pitch strip, stumps, bat, ball
d.rectangle([P2X, ROW2_Y + 88, P2X + PW, ROW2_Y + 118], fill=(198, 164, 110))
d.rectangle([P2X + 118, ROW2_Y + 10, P2X + 168, ROW2_Y + 118], fill=(232, 214, 178))
for sx in (P2X + 132, P2X + 142, P2X + 152):
    d.line([sx, ROW2_Y + 22, sx, ROW2_Y + 48], fill=(150, 110, 30), width=4)
d.polygon([(P2X + 196, ROW2_Y + 40), (P2X + 216, ROW2_Y + 40),
           (P2X + 206, ROW2_Y + 92), (P2X + 190, ROW2_Y + 88)], fill=(240, 220, 160))
d.ellipse([P2X + 252, ROW2_Y + 52, P2X + 284, ROW2_Y + 84], fill=(178, 34, 34))
d.ellipse([P2X + 258, ROW2_Y + 58, P2X + 270, ROW2_Y + 70], fill=(214, 90, 90))
# score badge
d.rounded_rectangle([P2X + 14, ROW2_Y + 14, P2X + 118, ROW2_Y + 48], radius=16,
                    fill=(255, 255, 255))
d.text((P2X + 66, ROW2_Y + 20), "720-9d", font=SANS_B(24), fill=RED, anchor="ma")
ty = ROW2_Y + 118 + 14
kicker(d, P2X + 16, ty, "CRICKET  \u2022  WELLINGTON", GREEN)
ty += 26
ty = headline(d, P2X + 16, ty, "India\u2019s record 720 puts NZ on the ropes",
              25, PW - 32, 30)
ty += 6
body(d, P2X + 16, ty,
     "India declare on 720 for 9 at the Basin Reserve \u2014 a record "
     "Test total in New Zealand.", PW - 32, size=18, leading=23)

# --- world in brief panel ---
panel(d, P3X, ROW2_Y, PW, ROW2_H)
d.text((P3X + 16, ROW2_Y + 14), "WORLD IN BRIEF",
       font=SANS_B(20), fill=RED)
d.line([P3X + 16, ROW2_Y + 44, P3X + PW - 16, ROW2_Y + 44], fill=LINE, width=2)

BRIEFS = [
    ("Nine killed in Gaza in 48 hours",
     "The toll since the October 2025 ceasefire reaches 1,661.",
     "burst"),
    ("Nepal PM talks with Modi in Delhi",
     "On a state visit, Shah holds bilateral talks with PM Modi.",
     "flags"),
    ("Swimmer crosses the Strait of Hormuz",
     "Pugh swims the strait as tankers burn nearby.",
     "waves"),
]

by = ROW2_Y + 56
for title, text, kind in BRIEFS:
    ix, iy = P3X + 16, by
    if kind == "burst":
        d.rectangle([ix, iy, ix + 58, iy + 58], fill=(43, 16, 16))
        d.polygon([(ix + 29, iy + 6), (ix + 38, iy + 22), (ix + 52, iy + 20),
                   (ix + 42, iy + 32), (ix + 50, iy + 46), (ix + 34, iy + 44),
                   (ix + 29, iy + 54), (ix + 22, iy + 42), (ix + 8, iy + 46),
                   (ix + 16, iy + 32), (ix + 6, iy + 20), (ix + 22, iy + 22)],
                  fill=GOLD)
        d.ellipse([ix + 21, iy + 21, ix + 37, iy + 37], fill=RED)
    elif kind == "flags":
        d.rectangle([ix, iy, ix + 58, iy + 58], fill=(238, 236, 228))
        d.rectangle([ix + 8, iy + 12, ix + 26, iy + 46], fill=(178, 34, 34),
                    outline=NAVY, width=2)
        d.rectangle([ix + 32, iy + 12, ix + 50, iy + 46], fill=(255, 153, 51))
        d.rectangle([ix + 32, iy + 12, ix + 50, iy + 24], fill=(255, 153, 51))
        d.rectangle([ix + 32, iy + 24, ix + 50, iy + 35], fill=(255, 255, 255))
        d.rectangle([ix + 32, iy + 35, ix + 50, iy + 46], fill=(19, 136, 8))
        d.ellipse([ix + 38, iy + 27, ix + 44, iy + 33], outline=NAVY, width=1)
    else:
        d.rectangle([ix, iy, ix + 58, iy + 58], fill=(31, 92, 145))
        d.ellipse([ix + 18, iy + 10, ix + 40, iy + 26], fill=(232, 196, 150))
        for wy in (iy + 34, iy + 44):
            d.arc([ix + 6, wy, ix + 26, wy + 14], 180, 360,
                  fill=(255, 255, 255), width=3)
            d.arc([ix + 30, wy, ix + 52, wy + 14], 180, 360,
                  fill=(255, 255, 255), width=3)
    tx = ix + 70
    ty = headline(d, tx, iy, title, 19, PW - 86, 22)
    body(d, tx, ty + 2, text, PW - 86, size=14, leading=18)
    by += 92
    if kind != "waves":
        d.line([P3X + 16, by - 12, P3X + PW - 16, by - 12], fill=LINE, width=1)

# ---- footer: the day in one line --------------------------------------
FY = 806
d.rounded_rectangle([24, FY, 1000, 1000], radius=12, fill=NAVY)
d.text((W // 2, FY + 16), "THE DAY IN ONE LINE",
       font=SANS_B(18), fill=GOLD, anchor="ma")
summary = ("A climate summit collapses, tankers burn in the Gulf, "
           "a minister quits over AI cheating \u2014 and India piles up 720.")
lines = wrap(d, summary, SERIF(26), 900)
sy = FY + 46
for line in lines:
    d.text((W // 2, sy), line, font=SERIF(26), fill=(255, 255, 255), anchor="ma")
    sy += 34
d.text((W // 2, sy + 6),
       "All seven stories happened or were first reported on "
       "Monday 23 November 2026.",
       font=SANS(17), fill=(200, 205, 220), anchor="ma")
d.text((W // 2, sy + 32),
       "Drawn from live reporting: CNN \u2022 Reuters \u2022 BBC \u2022 Le Monde \u2022 WSJ \u2022 ANI",
       font=SANS(15), fill=(150, 158, 180), anchor="ma")

# ---- save --------------------------------------------------------------
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")
