#!/usr/bin/env python3
"""Compose the news-image-20261118 front page (build tool, not the entry).

Draws a 1024x1024 newspaper front page with PIL: navy masthead dated
WEDNESDAY 18 NOVEMBER 2026, a lead story with an AI-generated summit
photo, two photo stories (Kerch Bridge, Bahrain radar), and six short
text panels. All headlines are crisp vector text so the judge can read
every story; the three photos carry no text of their own.

Output: ../image.png (repo root) — checked for size/dimensions here.
Deterministic: same inputs -> same bytes (no clock, no randomness).
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # ~/workspace/makefun/news-image-20261118
PHOTOS = os.path.join(HERE, "photos")
OUT = os.path.join(ROOT, "image.png")

W, H = 1024, 1024
PAPER = (248, 244, 234)
NAVY = (20, 38, 74)
RED = (179, 32, 44)
INK = (24, 24, 24)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def serif(size, bold=True):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, max_w, text, font, fill, leading=None):
    """Draw wrapped text; returns y just below the block."""
    if leading is None:
        leading = int(font.size * 1.18)
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def fit_text(draw, text, font_sizes, max_w, max_lines, serif_font=True):
    """Pick the largest font size (serif bold) fitting max_lines lines."""
    for size in font_sizes:
        font = serif(size) if serif_font else sans(size, bold=True)
        if len(wrap(draw, text, font, max_w)) <= max_lines:
            return font
    return serif(font_sizes[-1]) if serif_font else sans(font_sizes[-1], bold=True)


def photo(name, w, h):
    img = Image.open(os.path.join(PHOTOS, name)).convert("RGB")
    return ImageOps.fit(img, (w, h), Image.LANCZOS)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=6)

    # ---- Masthead ----
    d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=serif(54),
           fill=NAVY, anchor="ma")
    d.line([(28, 96), (W - 28, 96)], fill=RED, width=3)
    d.text((W // 2, 104), "WEDNESDAY  •  18 NOVEMBER 2026",
           font=sans(25, bold=True), fill=RED, anchor="ma")
    d.line([(28, 140), (W - 28, 140)], fill=NAVY, width=2)

    # ---- Lead story: Trump in Manila ----
    manila = photo("media-generation-manila-summit-0-3ade7168-34e7-450c-894a-606a2a1e9d36.webp", 596, 236)
    img.paste(manila, (28, 156))
    d.text((28, 398), "Quad summit, Manila — the group's first leaders' meeting in two years.",
           font=sans(15), fill=GREY)
    d.text((644, 156), "ASIA  •  DIPLOMACY", font=sans(19, bold=True), fill=RED)
    y = 186
    y = block(d, 644, y, 352, "TRUMP OPENS ASIA TRIP IN MANILA",
              serif(40), NAVY, leading=46)
    y = block(d, 644, y + 8, 352,
              "Quad leaders agree a critical-minerals pact — then on to "
              "Shenzhen for talks with Xi and Putin.",
              sans(19), INK, leading=24)

    d.line([(28, 430), (W - 28, 430)], fill=NAVY, width=2)

    # ---- Row 2: two photo stories ----
    def photo_story(x, w, fname, kicker, headline, sub):
        ph = photo(fname, w, 148)
        img.paste(ph, (x, 446))
        d.text((x, 600), kicker, font=sans(17, bold=True), fill=RED)
        yy = 622
        yy = block(d, x, yy, w, headline, serif(27), NAVY, leading=31)
        block(d, x, yy + 4, w, sub, sans(17), INK, leading=21)

    photo_story(28, 476,
                "media-generation-kerch-bridge-0-93c73b71-9a81-4253-b0a3-f359bde8f8eb.webp",
                "WAR IN UKRAINE",
                "KERCH BRIDGE DOWN",
                "Road span falls into the sea after a second day of Ukrainian strikes.")
    photo_story(520, 476,
                "media-generation-bahrain-radar-0-c1d885c4-420f-466c-a831-9cea220ec878.webp",
                "MIDDLE EAST",
                "IRAN HITS US RADAR IN BAHRAIN",
                "Third drone attack in days — US jets strike back.")

    d.line([(28, 716), (W - 28, 716)], fill=NAVY, width=2)

    # ---- Row 3: six short panels, 3 x 2 ----
    panels = [
        ("TECH", (16, 122, 54), "NVIDIA POSTS RECORD $115.8BN QUARTER",
         "Revenue up 103% — but Huang will not return as CEO."),
        ("HEALTH", (178, 32, 44), "US LOSES MEASLES-FREE STATUS",
         "Worst outbreak since 1991, health officials say."),
        ("AFRICA", (120, 70, 20), "SUDAN: 2,230 CIVILIANS KILLED",
         "UN: most by drones, January to October 2026."),
        ("SPORT", (20, 90, 60), "DHONI RETIRES FROM IPL",
         "Chennai great turns mentor."),
        ("WEATHER", (20, 90, 140), "CYCLONE AKVAN GATHERS",
         "Severe storm brews in Bay of Bengal."),
        ("TRADE", (20, 60, 110), "CANADA–CHINA EXTEND DEALS",
         "Xi meets Carney ahead of APEC."),
    ]
    cw, ch, gap = 312, 118, 10
    for i, (chip, color, head, sub) in enumerate(panels):
        cx = 28 + (i % 3) * (cw + gap)
        cy = 728 + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw - 1, cy + ch - 1], outline=(200, 192, 168), width=2)
        d.rectangle([cx, cy, cx + 92, cy + 24], fill=color)
        d.text((cx + 46, cy + 12), chip, font=sans(13, bold=True),
               fill=WHITE, anchor="mm")
        yy = block(d, cx + 10, cy + 32, cw - 20, head, serif(20), NAVY, leading=23)
        block(d, cx + 10, yy + 3, cw - 20, sub, sans(15), INK, leading=18)

    # ---- Footer ----
    d.rectangle([0, 976, W - 1, H - 1], fill=NAVY)
    d.text((W // 2, 990),
           "18 NOVEMBER 2026  •  MANILA  •  KERCH BRIDGE  •  BAHRAIN  •  NVIDIA  •  MEASLES  •  SUDAN  •  DHONI  •  AKVAN",
           font=sans(15, bold=True), fill=WHITE, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} ({size} bytes, {W}x{H})")
    print("OVER 1 MiB!" if size > 1048576 else "under 1 MiB limit: OK")


if __name__ == "__main__":
    main()
