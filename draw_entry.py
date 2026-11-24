#!/usr/bin/env python3
"""Draw the 24 November 2026 front page for news-image-20261124.

A newspaper front page in the house style: navy masthead with a gold
date, one lead story with a large illustration, and four more stories
in a 2x2 grid, each with a small flat illustration. Pure Pillow,
DejaVu fonts, fully deterministic output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (244, 239, 228)      # warm cream
NAVY = (26, 35, 64)          # masthead band
GOLD = (232, 168, 28)        # date + rules
RED = (164, 32, 40)          # kickers
INK = (24, 24, 24)           # headline ink
GREY = (110, 108, 100)       # secondary text
RULE = (60, 60, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill, leading):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def caption_bar(draw, box, label):
    """Small navy caption bar with white caps text at the bottom of a picture."""
    x0, y0, x1, y1 = box
    fnt = SANS_B(17)
    tw = draw.textlength(label, font=fnt)
    bar_h = 26
    draw.rectangle([x0, y1 - bar_h, x0 + tw + 18, y1], fill=NAVY)
    draw.text((x0 + 9, y1 - bar_h + 4), label, font=fnt, fill=(255, 255, 255))


def stars(draw, box, n, seed=7):
    """Deterministic scatter of small stars inside a box."""
    import random
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rng.randint(x0 + 6, x1 - 6)
        y = rng.randint(y0 + 6, y1 - 6)
        r = rng.choice([1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))


def draw_space(draw, box):
    """Lead illustration: a satellite above the Earth at night."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 22, 48))
    stars(draw, box, 46, seed=11)
    # orbit arc
    draw.arc([x0 - 180, y0 - 60, x1 + 60, y1 + 260], 200, 340,
             fill=GOLD, width=3)
    # Earth curve at the bottom
    draw.pieslice([x0 - 120, y1 - 90, x1 + 120, y1 + 260], 180, 360,
                  fill=(46, 110, 168))
    draw.arc([x0 - 120, y1 - 90, x1 + 120, y1 + 260], 180, 360,
             fill=(140, 200, 235), width=3)
    # satellite body with two solar panels
    cx, cy = (x0 + x1) // 2 + 60, (y0 + y1) // 2 - 40
    draw.rectangle([cx - 70, cy - 8, cx - 22, cy + 8], fill=(90, 120, 180))
    draw.rectangle([cx + 22, cy - 8, cx + 70, cy + 8], fill=(90, 120, 180))
    draw.rectangle([cx - 22, cy - 14, cx + 22, cy + 14], fill=(210, 210, 220))
    draw.rectangle([cx - 22, cy - 14, cx + 22, cy + 14], outline=NAVY, width=2)
    draw.line([cx, cy - 14, cx, cy - 30], fill=(210, 210, 220), width=3)
    draw.ellipse([cx - 4, cy - 34, cx + 4, cy - 26], fill=(232, 168, 28))
    caption_bar(draw, box, "SPACE PLEDGE")


def draw_jet(draw, box):
    """North Korea item: a jet over sea and island."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(176, 214, 235))
    # sea at the bottom
    draw.rectangle([x0, y1 - 52, x1, y1], fill=(52, 110, 160))
    # island
    draw.polygon([(x0 + 28, y1 - 52), (x0 + 62, y1 - 92),
                  (x0 + 96, y1 - 52)], fill=(96, 140, 90))
    # jet silhouette
    jx, jy = (x0 + x1) // 2 + 18, y0 + 52
    draw.polygon([(jx - 46, jy + 6), (jx + 46, jy), (jx - 46, jy - 6)],
                 fill=(40, 40, 48))
    draw.polygon([(jx - 8, jy - 4), (jx + 2, jy - 26), (jx + 12, jy - 4)],
                 fill=(40, 40, 48))
    draw.polygon([(jx - 8, jy + 4), (jx + 2, jy + 24), (jx + 12, jy + 4)],
                 fill=(40, 40, 48))
    # speed lines
    for i, yy in enumerate((jy - 34, jy - 14, jy + 10)):
        draw.line([x0 + 14, yy, x0 + 34 + i * 6, yy], fill=(255, 255, 255),
                  width=3)
    caption_bar(draw, box, "ULLEUNG")


def draw_crosses(draw, box):
    """Russia item: a field of small crosses under a grey sky."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(64, 68, 76))
    draw.rectangle([x0, y1 - 40, x1, y1], fill=(44, 48, 54))
    rows = [(y0 + 34, 14), (y0 + 62, 17), (y0 + 92, 21)]
    for yy, gap in rows:
        x = x0 + 16
        while x < x1 - 16:
            draw.rectangle([x, yy, x + 4, yy + 18], fill=(200, 198, 190))
            draw.rectangle([x - 5, yy + 5, x + 9, yy + 9], fill=(200, 198, 190))
            x += gap + 22
    caption_bar(draw, box, "THE TOLL")


def draw_blast(draw, box):
    """Yemen item: an explosion over a desert town at dusk."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 164, 110))
    draw.rectangle([x0, y1 - 44, x1, y1], fill=(150, 104, 66))
    # low buildings
    draw.rectangle([x0 + 12, y1 - 74, x0 + 44, y1 - 44], fill=(120, 84, 56))
    draw.rectangle([x0 + 52, y1 - 66, x0 + 88, y1 - 44], fill=(120, 84, 56))
    draw.rectangle([x0 + 96, y1 - 80, x0 + 128, y1 - 44], fill=(120, 84, 56))
    # blast starburst
    bx, by = (x0 + x1) // 2 + 6, y0 + 52
    import math
    for k in range(12):
        ang = math.pi * k / 6
        r1, r2 = 12, 34 if k % 2 == 0 else 22
        x_a, y_a = bx + r1 * math.cos(ang), by + r1 * math.sin(ang)
        x_b, y_b = bx + r2 * math.cos(ang), by + r2 * math.sin(ang)
        draw.line([x_a, y_a, x_b, y_b], fill=(232, 120, 30), width=5)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 196, 60))
    # smoke puffs
    for sx, sy, sr in ((bx - 30, by - 34, 10), (bx + 26, by - 40, 12),
                       (bx + 2, by - 52, 9)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 84, 80))
    caption_bar(draw, box, "HODEIDA")


def draw_gavel(draw, box):
    """Myanmar item: a gavel on a dark bench."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(58, 44, 66))
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(36, 28, 42))
    # gavel head and handle, tilted
    draw.rectangle([x0 + 34, y0 + 42, x0 + 108, y0 + 70], fill=(150, 104, 60))
    draw.rectangle([x0 + 34, y0 + 42, x0 + 108, y0 + 70],
                   outline=(90, 60, 30), width=2)
    draw.rectangle([x0 + 62, y0 + 66, x0 + 74, y0 + 122], fill=(120, 84, 48))
    # sound block
    draw.ellipse([x0 + 44, y1 - 46, x0 + 92, y1 - 30], fill=(150, 104, 60))
    caption_bar(draw, box, "SANCTIONS")


def paste_art(img, art, box):
    """Render one illustration into its own image and paste it, so no
    shape can ever spill outside its box."""
    x0, y0, x1, y1 = box
    tmp = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    d2 = ImageDraw.Draw(tmp)
    art(d2, (0, 0, x1 - x0, y1 - y0))
    img.paste(tmp, (x0, y0))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title = "THE WORLD TODAY"
    tf = SERIF_B(62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title,
           font=tf, fill=(255, 255, 255))
    date = "TUESDAY 24 NOVEMBER 2026"
    df = SANS_B(29)
    d.text(((W - d.textlength(date, font=df)) / 2, 76), date,
           font=df, fill=GOLD)
    d.rectangle([0, 118, W, 122], fill=GOLD)

    # --- kicker line ---------------------------------------------------
    kick = "FIVE STORIES THAT DEFINED THE DAY"
    kf = SANS(17)
    d.text(((W - d.textlength(kick, font=kf)) / 2, 138), kick,
           font=kf, fill=GREY)

    # --- lead story ----------------------------------------------------
    lx, lw = 36, 448
    y = 168
    d.text((lx, y), "SPACE  ·  NATO  ·  RUSSIA", font=SANS_B(18), fill=RED)
    y += 30
    y = para(d, lx, y, "NATO extends defence pledge to space",
             SERIF_B(38), lw, INK, 42)
    y += 6
    para(d, lx, y,
         "An attack in orbit counts as an attack on any member, NATO "
         "says, as Russia reportedly readies a nuclear-armed "
         "satellite. Merz: Europe is ready to negotiate.",
         SANS(20), lw, INK, 25)
    paste_art(img, draw_space, (500, 168, 988, 408))
    d.rectangle([500, 168, 988, 408], outline=NAVY, width=2)

    # --- divider -------------------------------------------------------
    d.line([36, 436, 988, 436], fill=RULE, width=2)

    # --- grid ----------------------------------------------------------
    cells = [
        # (illustration, kicker, headline, deck)
        (draw_jet, "NORTH KOREA",
         "Suspect North Korean jet enters South Korean air",
         "An aircraft breaches airspace near Ulleung island and "
         "residents are ordered to take shelter."),
        (draw_crosses, "RUSSIA",
         "Hacked data points to nearly 500,000 Russian dead",
         "Leaked figures suggest almost half a million soldiers "
         "have been killed in the war."),
        (draw_blast, "YEMEN",
         "Saudi strikes kill 17 in Yemen's Hodeida",
         "Houthis say 17 are killed in Hodeida, and more than 25 "
         "civilians killed or injured in Lahj."),
        (draw_gavel, "MYANMAR",
         "UK sanctions Myanmar's president",
         "Britain sanctions the president and military figures after "
         "the world court ruling on the Rohingya."),
    ]
    origins = [(36, 458), (524, 458), (36, 716), (524, 716)]
    for (art, kicker, head, deck), (cx, cy) in zip(cells, origins):
        box = (cx, cy, cx + 148, cy + 148)
        paste_art(img, art, box)
        d.rectangle(box, outline=NAVY, width=2)
        tx = cx + 164
        tw = 300
        d.text((tx, cy + 2), kicker, font=SANS_B(17), fill=RED)
        y = para(d, tx, cy + 28, head, SERIF_B(28), tw, INK, 34)
        para(d, tx, y + 4, deck, SANS(19), tw, INK, 25)

    # --- footer --------------------------------------------------------
    d.line([36, 962, 988, 962], fill=RULE, width=2)
    foot = "THE WORLD TODAY  •  24 NOVEMBER 2026"
    ff = SANS(17)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 976), foot,
           font=ff, fill=GREY)

    return img


if __name__ == "__main__":
    out = os.environ.get("DRAW_OUT", "entry.png")
    build().save(out, "PNG")
    print("wrote", out)
