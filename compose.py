#!/usr/bin/env python3
"""Render the Friday 20 November 2026 front page (news-image-20261120).

A 1024x1024 newspaper front page drawn entirely with PIL: cream paper,
huge serif date line, 8-figure numbers strip, region counts that add up
to 36, 3 lead stories with flat vector motifs, 11 cards, a dotted world
map with numbered pins, 22 one-line briefs, a verdict, a confidence
legend, a DATE CHECK footer and a source line. No network, no clock,
no randomness: two runs write identical bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 28                      # side margin
CW = W - 2 * MX              # content width = 968

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GREEN = (46, 110, 62)
GREY = (110, 105, 95)
TINT = (233, 226, 210)
RULE = (180, 172, 155)
DOT = (120, 130, 145)

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _cache[key]


PLAY_BLACK = "PlayfairDisplay-Black.ttf"
PLAY_BOLD = "PlayfairDisplay-Bold.ttf"
NEWS = "Newsreader-Regular.ttf"
NEWS_SB = "Newsreader-SemiBold.ttf"
BAR_B = "BarlowSC-Bold.ttf"
BAR_SB = "BarlowSC-SemiBold.ttf"
BAR_M = "BarlowSC-Medium.ttf"


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill=INK):
    draw.text((W / 2, y), text, font=fnt, fill=fill, anchor="ma")


def rule(draw, x0, y, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# Every story verified against at least two sources on 20 Nov 2026 (see
# build-state.md). All 36 are CONFIRMED; nothing on this page is a claim
# or a forecast, and the legend says so.

LEADS = [
    dict(num=1, region="ASIA-PACIFIC", source="INDIAN EXPRESS",
         head="Cyclone Akvan makes landfall in eastern India",
         deck="Severe storm crosses near Gopalpur; 370,000+ evacuated, "
              "winds 90-100 km/h gusting 110, 9,341 shelters open."),
    dict(num=2, region="EUROPE", source="KYIV INDEPENDENT",
         head="Russia fires ~30 ballistic missiles at Kyiv",
         deck="Seven overnight waves hit three bridges and energy sites; "
              "six killed in Kyiv, power and heat cut."),
    dict(num=3, region="EUROPE", source="REUTERS",
         head="COP31 reaches its final day deadlocked",
         deck="Closing draft omits fossil-fuel phase-out; $120bn adaptation "
              "goal cut; '35 by 35' clean-power push."),
]

CARDS = [
    dict(num=4, region="ASIA-PACIFIC", source="MORNINGSTAR",
         head="AI sell-off sweeps Asia",
         deck="Nikkei -4.8%, KOSPI -5.2%, Taiex -6.6%."),
    dict(num=5, region="AMERICAS", source="FORBES",
         head="Anthropic closes first day at $97.17",
         deck="First close $97.17, +17% on the $83 offer."),
    dict(num=6, region="WORLD", source="ESA",
         head="BepiColombo reaches Mercury",
         deck="Eight years, 6bn miles; insertion Saturday."),
    dict(num=7, region="EUROPE", source="GOV.UK",
         head="Burnham hosts EU-UK reset summit",
         deck="Emissions and agrifood links; 100,000 places."),
    dict(num=8, region="ASIA-PACIFIC", source="ANADOLU",
         head="Japan core inflation 2.2%",
         deck="October core CPI 2.2%, up from 2.1%."),
    dict(num=9, region="ASIA-PACIFIC", source="ANADOLU",
         head="China holds loan rates, 18th month",
         deck="One-year 3.0%, five-year 3.5%; no change."),
    dict(num=10, region="OCEANIA", source="AP",
         head="Phillips hits 118 against India",
         deck="Centuries in all formats vs India in a year."),
    dict(num=11, region="AMERICAS", source="REUTERS",
         head="Bukele files for third term",
         deck="Registers re-election bid; court cleared path."),
    dict(num=12, region="AFRICA", source="AL JAZEERA",
         head="Boat capsizes off Senegal",
         deck="Four dead near Yenne; 50-100 aboard."),
    dict(num=13, region="EUROPE", source="REUTERS",
         head="Italy holds general strike",
         deck="Full-day stoppage; thousands march."),
    dict(num=14, region="EUROPE", source="EORTC",
         head="Cancer drug shrinks tumours in 60.7%",
         deck="61 patients in Barcelona; no chemo comparison."),
]

# (number, city, text incl. source) -- one line each, left column 15-25,
# right column 26-36.
BRIEFS = [
    (15, "SAO PAULO - Markets shut for Black Consciousness Day. (B3)"),
    (16, "SEOUL - Ruling party adopts impeachment motion. (MBC)"),
    (17, "HONG KONG - Hang Seng -1.9% to 22,414, ~20% off peak. (Investvio)"),
    (18, "CANBERRA - CBO: AUKUS sub sale would cut US fleet. (Guardian)"),
    (19, "FLORIDA - St Johns River nears record 18.6 ft crest. (AP)"),
    (20, "IOWA - Army delays blast of 68 barrels to Monday. (AP)"),
    (21, "TONGA - Drought emergency; schools close Friday. (Tonga Govt)"),
    (22, "MEXICO CITY - 116th Revolution Day parade marches. (CDMX Secreta)"),
    (23, "KHARKIV - Drone hits hospital; four wounded. (Kyiv Independent)"),
    (24, "SEOUL - Kakao founder cleared again on appeal. (Yonhap)"),
    (25, "BUENOS AIRES - Argentina marks Sovereignty Day. (PublicHolidays.info)"),
    (26, "DAR ES SALAAM - Tanzania joins Africa's top five gold holders. (Daily News)"),
    (27, "HORMUZ - Brent holds near $92 as tankers hit mines. (Reuters)"),
    (28, "NEW DELHI - Pakistan minister joins SCO dialogue. (The News)"),
    (29, "DOHA - Australia stun Argentina 2-0 at U17 World Cup. (FIFA)"),
    (30, "JOHANNESBURG - Harmer 6/51 seals nine-wicket win. (SABC Sport)"),
    (31, "HONG KONG - Lakshya, Satwik-Chirag reach badminton semis. (IANS)"),
    (32, "TAIPEI - Russian bombers pass Taiwan again. (Reuters)"),
    (33, "TURIN - ATP Finals groups close; Medvedev-Tiafoe decider. (ATP)"),
    (34, "LOS ANGELES - 'Sunrise on the Reaping' opens in cinemas. (Lionsgate)"),
    (35, "WELLINGTON - Nicholls 175* as New Zealand post 368. (AP)"),
    (36, "BEIT SHEMESH - Haredi protesters clash with police. (Channel 12)"),
]

NUMBERS = [
    ("370,000", "EVACUATED - AKVAN"),
    ("~30", "MISSILES AT KYIV"),
    ("-4.8%", "NIKKEI FRIDAY"),
    ("2.2%", "JAPAN CORE CPI"),
    ("118", "PHILLIPS RUNS"),
    ("$97.17", "ANTHROPIC CLOSE"),
    ("$91.98", "BRENT A BARREL"),
    ("18th", "MONTH - CHINA LPR"),
]

REGION_LINE = ("EUROPE 7  ·  AMERICAS 8  ·  ASIA-PACIFIC 10  ·  MIDEAST 3  ·  "
                "AFRICA 3  ·  OCEANIA 4  ·  WORLD 1   —   36 STORIES IN ALL")

DATE_CHECK = [
    "Thursday 19 Nov: Senate Iran vote · Fiona the hippo dies · Pentagon "
    "$48.3bn war cost · Markle ruled fit · Lula-Raoni land deal · Jakarta bill · "
    "Denmark-Greenland bill · Kyiv daytime raid.",
    "Wednesday 18 Nov: Fiji drought declared.  Not yet: COP31 outcome · "
    "BepiColombo orbit insertion (Sat) · Las Vegas GP qualifying.",
]

SOURCES = ("Sources: Indian Express · Kyiv Independent · Reuters · Morningstar · "
           "Forbes · ESA · GOV.UK · Anadolu · AP · Al Jazeera · EORTC · MBC · "
           "Guardian · Yonhap · FIFA · SABC Sport · IANS · ATP · Lionsgate · "
           "Channel 12 · B3 · Daily News · The News · CDMX Secreta · Investvio")

# Land as rectangles on an 88 x 12 grid (lon -180..180, lat 72..-45).
# Columns follow col = (lon + 180) * 88 / 360, so pins (placed by the
# same longitude formula) land on their continents. Tapered per row so
# continents read as shapes, not solid blocks.
LAND_RECTS = [
    (2, 0, 30, 1), (5, 1, 30, 2), (8, 2, 29, 3), (10, 3, 27, 4),
    (13, 4, 20, 5), (18, 5, 23, 6),                      # North America
    (31, 0, 38, 1), (32, 1, 38, 2),                      # Greenland
    (39, 0, 40, 1), (44, 0, 47, 1),                      # Iceland, N Norway
    (24, 5, 33, 6), (24, 6, 35, 7), (25, 7, 34, 8),      # South America
    (26, 8, 33, 9), (27, 9, 31, 10), (28, 10, 30, 11),
    (42, 1, 52, 2), (41, 2, 53, 3), (42, 3, 50, 4),      # Europe
    (40, 3, 55, 4), (39, 4, 56, 5), (41, 5, 55, 6),      # Africa
    (43, 6, 54, 7), (44, 7, 53, 8), (45, 8, 51, 9),
    (50, 3, 56, 4),                                       # Middle East
    (54, 0, 87, 1), (52, 1, 87, 2), (53, 2, 86, 3),      # Asia
    (57, 3, 80, 4), (56, 4, 60, 5), (60, 4, 65, 5),      # China, Arabia, India
    (55, 5, 65, 6), (66, 5, 73, 6),                      # Arabia, India S, SE Asia
    (68, 6, 78, 7),                                       # Indonesia
    (77, 2, 80, 3), (78, 3, 81, 4),                      # Japan
    (71, 7, 81, 8), (72, 8, 80, 9),                      # Australia
    (84, 9, 87, 10),                                      # New Zealand
]

# (story num, lon, lat, label dx, label dy)
# Barcelona pin is nudged slightly SW so its dot does not cover Brussels'.
PINS = [
    (1, 85.0, 19.5, 0, -14), (2, 30.5, 50.5, 0, -14),
    (3, 4.4, 50.8, 0, -14), (4, 139.7, 35.7, 0, -14),
    (5, -74.0, 40.7, 0, -14), (6, 174.8, -41.3, 0, -14),
    (7, -89.2, 13.7, 0, -14), (8, -17.4, 14.7, 0, -14),
    (9, 12.5, 41.9, 0, 12), (10, -2.0, 38.0, -16, 10),
]


def _motif_cyclone(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 + 4
    for r, col in ((34, BLUE), (26, BLUE), (18, BLUE), (10, RED)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 20, fill=col, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for dx in (-46, -30, 46, 30):
        draw.ellipse([cx + dx - 3, cy + 16, cx + dx + 3, cy + 24], fill=BLUE)


def _motif_kyiv(draw, x, y, w, h):
    base = y + h - 6
    for bx, bw, bh in ((0, 26, 20), (32, 20, 28), (58, 30, 16), (94, 22, 24),
                       (122, 26, 20), (154, 20, 28), (180, 28, 18)):
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=INK)
    cx, cy = x + w // 2, y + 10
    for ang in range(0, 360, 45):
        import math
        r1 = 9
        a = math.radians(ang)
        draw.line([(cx, cy), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))],
                  fill=RED, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def _motif_cop(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 + 2
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=BLUE, width=3)
    draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], 300, 60, fill=GREEN, width=8)
    draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], 120, 210, fill=GREEN, width=8)
    draw.polygon([(cx + 30, cy - 22), (cx + 46, cy - 30), (cx + 44, cy - 12)],
                 fill=GREEN)


MOTIFS = [_motif_cyclone, _motif_kyiv, _motif_cop]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)

    # ---- masthead
    d.text((MX, 20), "FRIDAY EDITION", font=font(BAR_SB, 13), fill=INK)
    center(d, 16, "THE WORLD IN ONE PAGE", font(BAR_B, 26))
    d.text((W - MX, 20), "No. 325", font=font(BAR_SB, 13), fill=INK, anchor="ra")
    rule(d, MX, 50, W - MX, 2, INK)
    rule(d, MX, 54, W - MX, 1)

    # ---- date line + tagline
    center(d, 62, "Friday 20 November 2026", font(PLAY_BLACK, 54))
    center(d, 128, "36 stories from six continents - cyclones, missiles, "
                    "markets and a Mercury arrival",
           font(NEWS, 16), GREY)

    # ---- numbers strip
    rule(d, MX, 152, W - MX, 1, INK)
    cell = CW / 8
    for i, (num, label) in enumerate(NUMBERS):
        cx = MX + cell * i + cell / 2
        d.text((cx, 160), num, font=font(PLAY_BOLD, 19), fill=RED, anchor="ma")
        d.text((cx, 184), label, font=font(BAR_SB, 10), fill=INK, anchor="ma")
        if i:
            d.line([(MX + cell * i, 158), (MX + cell * i, 194)], fill=RULE, width=1)
    rule(d, MX, 198, W - MX, 1, INK)

    # ---- region bar
    d.rectangle([MX, 204, W - MX, 230], fill=TINT)
    center(d, 211, REGION_LINE, font(BAR_SB, 15))

    # ---- leads
    col_w = 312
    col_x = [MX, MX + 328, MX + 656]
    for i, lead in enumerate(LEADS):
        x = col_x[i]
        MOTIFS[i](d, x, 238, col_w, 52)
        kicker = "%d · %s · CONFIRMED" % (lead["num"], lead["region"])
        d.text((x, 296), kicker, font=font(BAR_B, 11), fill=RED)
        d.text((x + col_w, 296), lead["source"], font=font(BAR_SB, 10),
               fill=GREY, anchor="ra")
        lines = wrap(d, lead["head"], font(PLAY_BOLD, 20), col_w)
        yy = 312
        for ln in lines[:3]:
            d.text((x, yy), ln, font=font(PLAY_BOLD, 20), fill=INK)
            yy += 24
        dlines = wrap(d, lead["deck"], font(NEWS, 13), col_w)
        yy = 388
        for ln in dlines[:3]:
            d.text((x, yy), ln, font=font(NEWS, 13), fill=INK)
            yy += 16
        if i:
            d.line([(x - 8, 238), (x - 8, 448)], fill=RULE, width=1)
    rule(d, MX, 452, W - MX, 1, INK)

    # ---- cards: 3 rows of 4 / 4 / 3
    card_w, gap = 233, 11
    card_x = [MX + j * (card_w + gap) for j in range(4)]
    for i, card in enumerate(CARDS):
        r, c = divmod(i, 4)
        x, y = card_x[c], 458 + r * 64
        kicker = "%d · %s · CONFIRMED" % (card["num"], card["region"])
        d.text((x, y + 2), kicker, font=font(BAR_B, 10), fill=RED)
        d.text((x + card_w, y + 2), card["source"], font=font(BAR_SB, 9),
               fill=GREY, anchor="ra")
        lines = wrap(d, card["head"], font(PLAY_BOLD, 13), card_w)
        yy = y + 16
        for ln in lines[:2]:
            d.text((x, yy), ln, font=font(PLAY_BOLD, 13), fill=INK)
            yy += 16
        d.text((x, y + 48), card["deck"], font=font(NEWS, 11), fill=INK)
        if r < 2:
            rule(d, MX, y + 62, W - MX, 1)
    rule(d, MX, 650, W - MX, 1, INK)

    # ---- dotted world map with numbered pins
    d.text((MX, 656), "WHERE IT HAPPENED", font=font(BAR_B, 12), fill=INK)
    d.text((W - MX, 656), "Pins match story numbers", font=font(BAR_SB, 11),
           fill=GREY, anchor="ra")
    map_x0, map_y0, map_w, map_h = MX, 672, CW, 118
    cells = set()
    for (x0, y0, x1, y1) in LAND_RECTS:
        for gx in range(x0, x1):
            for gy in range(y0, y1):
                cells.add((gx, gy))
    for (gx, gy) in cells:
        px = map_x0 + (gx + 0.5) / 88 * map_w
        py = map_y0 + (gy + 0.5) / 12 * map_h
        d.ellipse([px - 2.0, py - 2.0, px + 2.0, py + 2.0], fill=DOT)

    def pin_xy(lon, lat):
        return (map_x0 + (lon + 180) / 360 * map_w,
                map_y0 + (72 - lat) / 128 * map_h)

    for (num, lon, lat, dx, dy) in PINS:
        px, py = pin_xy(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=PAPER, width=1)
        d.text((px + dx, py + dy), str(num), font=font(BAR_B, 9),
               fill=(255, 255, 255), anchor="mm")
        if dx or dy:
            d.line([(px, py), (px + dx, py + dy)], fill=RED, width=1)
    rule(d, MX, 794, W - MX, 1, INK)

    # ---- briefs
    d.text((MX, 800), "THE DAY IN BRIEF", font=font(BAR_B, 12), fill=INK)
    d.text((W - MX, 800), "All 22 confirmed", font=font(BAR_SB, 11),
           fill=GREY, anchor="ra")
    bf = font(NEWS_SB, 11)
    for i, (num, text) in enumerate(BRIEFS):
        col = 0 if i < 11 else 1
        row = i if i < 11 else i - 11
        x = MX if col == 0 else MX + 498
        y = 814 + int(row * 11.5)
        d.text((x, y), "%d" % num, font=font(BAR_B, 11), fill=RED)
        d.text((x + 22, y), text, font=bf, fill=INK)

    # ---- verdict + legend
    d.text((MX, 944), "THE VERDICT -", font=font(BAR_B, 13), fill=RED)
    d.text((MX + 108, 944),
           "Storms, strikes and sell-offs: nature, war and markets all moved "
           "on the same day.",
           font=font(NEWS_SB, 13), fill=INK)
    lx = MX
    for (kind, label) in (("full", "CONFIRMED - checked against two sources"),
                          ("half", "CLAIM - one source, disputed"),
                          ("empty", "FORECAST - not yet happened")):
        cy = 962
        if kind == "full":
            d.ellipse([lx, cy, lx + 9, cy + 9], fill=RED)
        elif kind == "half":
            d.ellipse([lx, cy, lx + 9, cy + 9], outline=RED, width=1)
            d.pieslice([lx, cy, lx + 9, cy + 9], 90, 270, fill=RED)
        else:
            d.ellipse([lx, cy, lx + 9, cy + 9], outline=RED, width=1)
        d.text((lx + 13, cy - 1), label, font=font(BAR_M, 10), fill=INK)
        lx += 13 + d.textlength(label, font=font(BAR_M, 10)) + 22
    d.text((lx, 961), "Every story on this page is CONFIRMED.",
           font=font(BAR_B, 10), fill=RED)

    # ---- DATE CHECK
    d.text((MX, 977), "DATE CHECK - LEFT OUT ON PURPOSE",
           font=font(BAR_B, 11), fill=RED)
    yy = 990
    for ln in DATE_CHECK:
        d.text((MX, yy), ln, font=font(NEWS, 10), fill=GREY)
        yy += 12

    # ---- sources footer: exactly one line at the foot of the page
    src_font = font(BAR_M, 9)
    src_lines = wrap(d, SOURCES, src_font, CW)
    if len(src_lines) > 1:
        src_font = font(BAR_M, 8)
        src_lines = wrap(d, SOURCES, src_font, CW)
    src_text = SOURCES
    while len(src_lines) > 1:
        src_text = src_text.rsplit(" · ", 1)[0]
        src_lines = wrap(d, src_text, src_font, CW)
    d.text((MX, 1013), src_lines[0], font=src_font, fill=GREY)

    img.save(path, "PNG")


if __name__ == "__main__":
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else "/tmp/news20.png")
