#!/usr/bin/env python3
"""Deterministic newspaper front page generator.

Renders a 1024x1024 newspaper front page ("THE WORLD TODAY") to entry.png
using only Pillow. No network, no external images, no randomness, no
timestamps -> byte-identical output across runs.
"""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants
W, H = 1024, 1024
MARGIN = 20
BLACK = (17, 17, 17)
RED = (192, 0, 0)
GREY = (236, 236, 236)
WHITE = (255, 255, 255)
BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_at(x, y_top, text, f, fill):
    """Draw text so its ink box starts exactly at (x, y_top). Return bottom."""
    b = f.getbbox(text)
    d.text((x - b[0], y_top - b[1]), text, font=f, fill=fill)
    return y_top + (b[3] - b[1])


def centered(y_top, text, f, fill):
    b = f.getbbox(text)
    return draw_at((W - (b[2] - b[0])) // 2, y_top, text, f, fill)


def wrap(text, f, width):
    """Greedy word wrap. Returns None if any single word cannot fit."""
    lines, cur = [], ""
    for word in text.split():
        if f.getlength(word) > width:
            return None
        trial = word if not cur else cur + " " + word
        if f.getlength(trial) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, path, start, minimum, max_lines, width, max_h=None, lh=1.2):
    """Shrink font size until text wraps within max_lines / max_h."""
    for size in range(start, minimum - 1, -1):
        f = font(path, size)
        lines = wrap(text, f, width)
        if lines and len(lines) <= max_lines:
            line_h = int(size * lh)
            if max_h is None or line_h * len(lines) <= max_h:
                return f, lines, line_h
    raise RuntimeError("text does not fit: %r" % text)


# ---------------------------------------------------------------- masthead
y = centered(14, "THE WORLD TODAY", font(BOLD_PATH, 84), BLACK)
y = centered(y + 10, "FRIDAY, 20 NOVEMBER 2026 - WORLD NEWS IN ONE PAGE",
             font(BOLD_PATH, 22), BLACK)
rule_y = y + 10
d.rectangle([MARGIN, rule_y, W - MARGIN, rule_y + 4], fill=BLACK)  # thick rule

# ---------------------------------------------------------------- grid geometry
PANEL_H = 250
FOOTER_H = 44
footer_top = H - MARGIN - FOOTER_H
grid_top = rule_y + 5 + 12
grid_bottom = footer_top - 12
col_w = (W - 2 * MARGIN) // 2                     # 492
row_gap = (grid_bottom - grid_top - 3 * PANEL_H) // 2
if row_gap < 4:
    raise RuntimeError("not enough vertical room for grid")

# separators: one vertical rule, two horizontal rules
mid_x = MARGIN + col_w
d.line([(mid_x, grid_top), (mid_x, grid_bottom)], fill=BLACK, width=2)
for r in range(2):
    ry = grid_top + PANEL_H + r * (PANEL_H + row_gap) + row_gap // 2
    d.line([(MARGIN, ry), (W - MARGIN, ry)], fill=BLACK, width=2)

# ---------------------------------------------------------------- icons (90x90)
def icon_globe(x, y):
    cx, cy = x + 45, y + 45
    d.ellipse([x + 5, y + 5, x + 85, y + 85], outline=BLACK, width=3)
    d.ellipse([cx - 18, y + 5, cx + 18, y + 85], outline=BLACK, width=2)
    d.line([(x + 5, cy), (x + 85, cy)], fill=BLACK, width=2)
    d.arc([x + 10, cy - 30, x + 80, cy + 10], 180, 360, fill=BLACK, width=2)
    d.arc([x + 10, cy - 10, x + 80, cy + 30], 0, 180, fill=BLACK, width=2)


def icon_rocket(x, y):
    cx = x + 45
    d.rectangle([cx - 12, y + 22, cx + 12, y + 64], outline=BLACK, width=3)
    d.polygon([(cx - 12, y + 22), (cx, y + 4), (cx + 12, y + 22)], fill=BLACK)
    d.polygon([(cx - 12, y + 50), (cx - 26, y + 70), (cx - 12, y + 64)], fill=BLACK)
    d.polygon([(cx + 12, y + 50), (cx + 26, y + 70), (cx + 12, y + 64)], fill=BLACK)
    d.ellipse([cx - 6, y + 30, cx + 6, y + 42], outline=BLACK, width=2)
    d.polygon([(cx - 7, y + 66), (cx, y + 86), (cx + 7, y + 66)], fill=RED)


def _rot_rect(cx, cy, w, h, ang_deg):
    a = math.radians(ang_deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return [(cx + px * ca - py * sa, cy + px * sa + py * ca) for px, py in pts]


def icon_gavel(x, y):
    d.polygon(_rot_rect(x + 32, y + 24, 46, 20, -35), fill=BLACK)
    d.line([(x + 42, y + 36), (x + 70, y + 68)], fill=BLACK, width=7)
    d.rectangle([x + 16, y + 76, x + 64, y + 84], fill=BLACK)


def icon_cyclone(x, y):
    d.arc([x + 4, y + 4, x + 86, y + 86], 300, 210, fill=BLACK, width=3)
    d.arc([x + 14, y + 14, x + 76, y + 76], 210, 120, fill=BLACK, width=3)
    d.arc([x + 24, y + 24, x + 66, y + 66], 120, 30, fill=BLACK, width=3)
    d.arc([x + 34, y + 34, x + 56, y + 56], 30, 300, fill=RED, width=3)
    d.ellipse([x + 41, y + 41, x + 49, y + 49], fill=BLACK)


def icon_flags(x, y):
    d.line([(x + 24, y + 8), (x + 24, y + 84)], fill=BLACK, width=3)
    d.line([(x + 60, y + 8), (x + 60, y + 84)], fill=BLACK, width=3)
    d.polygon([(x + 24, y + 10), (x + 54, y + 20), (x + 24, y + 30)], fill=RED)
    d.polygon([(x + 60, y + 12), (x + 88, y + 22), (x + 60, y + 32)], fill=BLACK)
    # small triangle "dove"
    d.polygon([(x + 34, y + 56), (x + 58, y + 46), (x + 50, y + 62)], fill=BLACK)
    d.polygon([(x + 42, y + 50), (x + 50, y + 36), (x + 52, y + 52)], fill=BLACK)


def icon_controller(x, y):
    d.rounded_rectangle([x + 5, y + 25, x + 85, y + 70], radius=16,
                        outline=BLACK, width=3)
    d.rectangle([x + 17, y + 43, x + 35, y + 51], fill=BLACK)   # d-pad
    d.rectangle([x + 22, y + 38, x + 30, y + 56], fill=BLACK)
    d.ellipse([x + 57, y + 37, x + 67, y + 47], fill=RED)       # buttons
    d.ellipse([x + 67, y + 48, x + 77, y + 58], fill=BLACK)


# ---------------------------------------------------------------- panels
STORIES = [
    ("WORLD", "TRUMP: NO RUSH ON IRAN",
     "President says he is not rushing into any decision on new strikes. "
     "Will see what happens after Jan. 1.", icon_globe),
    ("JUSTICE", "ICJ: MYANMAR COMMITTED GENOCIDE",
     "UN top court rules against Myanmar over the Rohingya in a historic "
     "first: a state found guilty of genocide.", icon_gavel),
    ("SPACE", "VOYAGER 1 REACHES ONE LIGHT-DAY",
     "NASA probe is now 16 billion miles out, the first human-made object "
     "a full light-day from Earth.", icon_rocket),
    ("INDIA", "CYCLONE AKVAN: 300,000 EVACUATED",
     "Severe storm strikes the Odisha coast today, winds to 110 km/h; "
     "shelters readied across the state.", icon_cyclone),
    ("EUROPE", "EUROPE READY FOR TALKS WITH RUSSIA",
     "Leaders in Berlin say they are ready to negotiate an end to the "
     "Ukraine war, with Kyiv at the table.", icon_flags),
    ("GAMES", "GTA 6 TOPS 1.84 BILLION DOLLARS ON DAY ONE",
     "Sensor Tower estimate beats The Odyssey box-office total of 1.805B "
     "dollars: the biggest launch in game history.", icon_controller),
]

BAND_H = 30
PAD = 12
ICON = 90
kicker_font = font(BOLD_PATH, 18)


def place_icon(fn, ix, body_top, body_bottom):
    """Draw icon fully inside the panel body, vertically centered, clear of
    the band rule above and the panel edge/rule below. Shrinks if too tall."""
    global d
    scratch = Image.new("RGB", (ICON, ICON), WHITE)
    main_d = d
    d = ImageDraw.Draw(scratch)
    fn(0, 0)
    d = main_d
    bbox = ImageChops.difference(
        scratch, Image.new("RGB", (ICON, ICON), WHITE)).getbbox() \
        or (0, 0, ICON, ICON)
    ink_h = bbox[3] - bbox[1]
    body_h = body_bottom - body_top
    clearance = 10                      # min gap to band rule / panel edge
    scale = min(1.0, (body_h - 2 * clearance) / ink_h)
    cy = (body_top + body_bottom) // 2
    if scale >= 1.0:
        iy = cy - (bbox[1] + bbox[3]) // 2
        fn(ix, iy)                      # same vector draw, just re-centered
    else:
        s = int(round(ICON * scale))
        small = scratch.resize((s, s), Image.Resampling.LANCZOS)
        sb = ImageChops.difference(
            small, Image.new("RGB", (s, s), WHITE)).getbbox() \
            or (0, 0, s, s)
        iy = cy - (sb[1] + sb[3]) // 2
        img.paste(small, (ix, iy))


for i, (kicker, headline, deck, icon) in enumerate(STORIES):
    row, col = divmod(i, 2)
    px = MARGIN + col * col_w
    py = grid_top + row * (PANEL_H + row_gap)

    # light grey header band + thin rule under it
    d.rectangle([px, py, px + col_w - 1, py + BAND_H], fill=GREY)
    d.line([(px, py + BAND_H), (px + col_w - 1, py + BAND_H)], fill=BLACK, width=1)
    kb = kicker_font.getbbox(kicker)
    draw_at(px + PAD, py + (BAND_H - (kb[3] - kb[1])) // 2, kicker,
            kicker_font, RED)

    content_top = py + BAND_H + 10
    panel_bottom = py + PANEL_H - 8
    text_x = px + PAD
    text_w = col_w - PAD - ICON - PAD - PAD        # text column left of icon

    hf, hlines, hlh = fit(headline, BOLD_PATH, 32, 20, 2, text_w, lh=1.15)
    ty = content_top
    for line in hlines:
        draw_at(text_x, ty, line, hf, BLACK)
        ty += hlh
    ty += 8

    df, dlines, dlh = fit(deck, REG_PATH, 21, 13, 3, text_w,
                          max_h=panel_bottom - ty, lh=1.22)
    for line in dlines:
        draw_at(text_x, ty, line, df, BLACK)
        ty += dlh

    place_icon(icon, px + col_w - PAD - ICON,
               py + BAND_H + 1, py + PANEL_H)

# ---------------------------------------------------------------- footer ticker
TICKER = ("TRUMP-XI-PUTIN SUMMIT IN SHENZHEN - HAYABUSA2 ENGINE TROUBLE "
          "SCRAPS ASTEROID LANDING - NICHOLLS 113 NOT OUT AS INDIA FACE NZ "
          "IN WELLINGTON - ANTHROPIC VALUATION REPORTED AT 1.5 TRILLION DOLLARS.")
d.rectangle([MARGIN, footer_top, W - MARGIN, footer_top + FOOTER_H], fill=BLACK)
tf = font(BOLD_PATH, 18)
tb = tf.getbbox(TICKER)
tick_img = Image.new("RGBA", (int(tb[2] - tb[0]) + 4, int(tb[3] - tb[1]) + 4),
                     (0, 0, 0, 0))
ImageDraw.Draw(tick_img).text((2 - tb[0], 2 - tb[1]), TICKER, font=tf,
                              fill=WHITE + (255,))
inner_w = W - 2 * MARGIN - 24
if tick_img.width > inner_w:
    # condense horizontally so the full ticker stays on one line
    tick_img = tick_img.resize((inner_w, tick_img.height),
                               Image.Resampling.LANCZOS)
img.paste(tick_img, ((W - tick_img.width) // 2,
                     footer_top + (FOOTER_H - tick_img.height) // 2), tick_img)

# ---------------------------------------------------------------- save
img.save("entry.png", format="PNG")
print("wrote entry.png")
