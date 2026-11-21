#!/usr/bin/env python3
"""Render the Friday 20 November 2026 front page, v3 (news-image-20261120).

A 1024x1024 newspaper front page drawn entirely with PIL: cream paper,
huge serif date line + italic subhead, 6-figure numbers strip, region
counts that add up to 38, 3 lead stories with LARGE full-bleed flat
illustration panels (Kyiv night skyline, Akvan landfall map, AI sell-off
chart + market table), 10 cards each with a small flat illustration and
a data chip, a solid-land world map with numbered pins, 25 one-line
briefs, a boxed DATE CHECK and a source line. No network, no clock, no
randomness: two runs write identical bytes.

v3 changes vs v2 (see ~/workspace/makefun/news20-analysis/v3-gap-analysis.md):
leads are Kyiv / Akvan / AI sell-off (was Akvan / Kyiv / COP31); cards
are the consensus core (COP31, UK-EU, Poland missile, Iraq army, Italy,
Japan, Seoul impeach, Kenya oil, Bukele, Phillips); numbers strip is the
6 consensus figures; Kyiv deck uses the later verified toll (~110
missiles, 9 killed); map is solid tan land; DATE CHECK is boxed.
"""
import math
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
NAVY = (20, 33, 61)
SEA = (47, 111, 143)
TAN = (222, 208, 178)
TAN_DARK = (198, 182, 148)
SKY = (178, 204, 220)
ORANGE = (220, 110, 40)
GOLD = (212, 175, 55)
DARKBLUE = (24, 48, 88)

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


def chip(draw, x, y, text, bg=RED, fg=(255, 255, 255), size=10, pad=5, h=16):
    fnt = font(BAR_B, size)
    w = int(draw.textlength(text, font=fnt)) + 2 * pad
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + pad, y + 1), text, font=fnt, fill=fg)
    return w


# ---------------------------------------------------------------- stories
# Every story verified against at least two sources on 20 Nov 2026 (see
# build-state.md + v3-gap-analysis.md). All 38 are CONFIRMED; nothing on
# this page is a claim or a forecast, and the footer legend says so.

LEADS = [
    dict(num=1, kicker="1 · KYIV, UKRAINE · WAR", source="KYIV INDEPENDENT",
         head="Russian missiles hit three Kyiv bridges",
         deck="An overnight barrage of about 110 missiles and 400 drones "
              "killed at least nine people across Ukraine; power and water "
              "cut in the capital. (Kyiv Independent, BBC)"),
    dict(num=2, kicker="2 · ODISHA, INDIA · CYCLONE", source="IMD",
         head="Cyclone Akvan comes ashore in eastern India",
         deck="The storm crossed the coast near Gopalpur from about 8 am "
              "after more than 370,000 people were moved to shelters. No "
              "deaths were reported. (IMD, Deccan Herald)"),
    dict(num=3, kicker="3 · TAIPEI · SEOUL · TOKYO · MARKETS",
         source="AL JAZEERA",
         head="AI sell-off sinks Asia's stock markets",
         deck="Taiwan's index fell 6.2% to end its worst week since 1991. "
              "Seoul lost 5.2% and Tokyo 4.8% as chipmakers led the slide. "
              "(Al Jazeera, Anadolu)"),
]

CARDS = [
    dict(num=4, kicker="4 · ANTALYA · CLIMATE", source="UN NEWS",
         head="COP31 reaches its last day with no deal",
         deck="Draft omits fossil fuels; $120bn goal cut."),
    dict(num=5, kicker="5 · BRUSSELS · DIPLOMACY", source="REUTERS",
         head="UK and EU seal a 'reset' deal",
         deck="Food trade, carbon link; 100,000 youth visas."),
    dict(num=6, kicker="6 · EASTERN POLAND · SECURITY", source="AP",
         head="Russian cruise missile lands in Poland",
         deck="Fell in a field; two airports paused."),
    dict(num=7, kicker="7 · CENTRAL IRAQ · SECURITY", source="REUTERS",
         head="Iraqi army enters a militia stronghold",
         deck="Troops deploy to Jurf al-Sakhar."),
    dict(num=8, kicker="8 · ITALY · LABOUR", source="REUTERS",
         head="General strike over Italy's budget",
         deck="Full-day stoppage; thousands march."),
    dict(num=9, kicker="9 · TOKYO · ECONOMY", source="ANADOLU",
         head="Japan's inflation picks up to 2.3%",
         deck="October core CPI 2.2%, up from 2.1%."),
    dict(num=10, kicker="10 · SEOUL · POLITICS", source="YONHAP",
         head="Korea's ruling party to impeach top judge",
         deck="Adopts impeach top judge as policy."),
    dict(num=11, kicker="11 · TURKANA, KENYA · ENERGY", source="KBC",
         head="Kenya starts drilling its first oil well",
         deck="First crude due on 1 December."),
    dict(num=12, kicker="12 · SAN SALVADOR · POLITICS", source="AP",
         head="Bukele files to run for a third term",
         deck="Registers re-election bid; vote Feb 2027."),
    dict(num=13, kicker="13 · WELLINGTON · CRICKET", source="ICC",
         head="Phillips hits 118 against India",
         deck="Centuries in all formats vs India."),
]

# (number, text incl. source) -- one line each; left column 14-26,
# right column 27-38.
BRIEFS = [
    (14, "SAO PAULO - Markets shut for Black Consciousness Day. (B3)"),
    (15, "HONG KONG - Hang Seng -1.9% to 22,414. (Investvio)"),
    (16, "CANBERRA - CBO: AUKUS sale would cut US fleet. (Guardian)"),
    (17, "FLORIDA - St Johns River nears record 18.6 ft crest. (AP)"),
    (18, "IOWA - Army delays blast of 68 barrels to Monday. (AP)"),
    (19, "TONGA - Drought emergency; schools close Friday. (Tonga Govt)"),
    (20, "MEXICO CITY - 116th Revolution Day parade marches. (CDMX)"),
    (21, "KHARKIV - Drone hits hospital, four wounded. (Kyiv Ind.)"),
    (22, "SEOUL - Kakao founder cleared again on appeal. (Yonhap)"),
    (23, "DAR ES SALAAM - Tanzania a top-five gold holder. (Daily News)"),
    (24, "HORMUZ - Brent holds near $92 as tankers hit mines. (Reuters)"),
    (25, "NEW DELHI - Pakistan minister joins SCO dialogue. (The News)"),
    (26, "DOHA - Australia stun Argentina 2-0 at U17 World Cup. (FIFA)"),
    (27, "JOHANNESBURG - Harmer 6/51, nine-wicket win. (SABC Sport)"),
    (28, "HONG KONG - Lakshya, Satwik-Chirag into semis. (IANS)"),
    (29, "TAIPEI - Russian bombers pass Taiwan again. (Reuters)"),
    (30, "TURIN - ATP Finals groups close; Medvedev-Tiafoe decider. (ATP)"),
    (31, "LOS ANGELES - 'Sunrise on the Reaping' opens. (Lionsgate)"),
    (32, "WELLINGTON - Nicholls 175* as New Zealand post 368. (AP)"),
    (33, "BEIT SHEMESH - Haredi protesters clash. (Channel 12)"),
    (34, "NEW YORK - Anthropic closes first day at $97.17, +17%. (Forbes)"),
    (35, "SPACE - BepiColombo reaches Mercury after 8 years. (ESA)"),
    (36, "BEIJING - China holds loan rates, 18th month. (Anadolu)"),
    (37, "DAKAR - Boat capsizes off Senegal; four dead. (Al Jazeera)"),
    (38, "BARCELONA - Cancer drug shrinks tumours in 60.7%. (EORTC)"),
]

NUMBERS = [
    ("3", "BRIDGES DAMAGED IN KYIV"),
    ("370,000+", "EVACUATED BEFORE AKVAN"),
    ("-6.2%", "TAIPEI INDEX, FRIDAY"),
    ("100,000", "YOUTH VISAS - UK-EU DEAL"),
    ("2.3%", "JAPAN INFLATION, OCT"),
    ("118", "PHILLIPS RUNS VS INDIA"),
]

REGION_LINE = ("EUROPE 7  ·  AMERICAS 7  ·  ASIA-PACIFIC 10  ·  MIDEAST 4  ·  "
                "AFRICA 4  ·  OCEANIA 4  ·  WORLD 2   —   38 STORIES IN ALL")

DATE_CHECK = ("DATE CHECK — Left out on purpose, first reported Thursday 19 "
              "November: the Trump–Xi–Putin Shenzhen summit · Anthropic's $83 "
              "IPO pricing · ICJ Myanmar verdict · GTA VI launch · the "
              "$190.4m Van Gogh sale · Voyager 1 one light-day · the Senate "
              "51–48 Iran vote.  Not yet happened, so not shown: "
              "BepiColombo's Mercury orbit entry (Sat 21) · any final COP31 "
              "text · Las Vegas GP qualifying.")

SOURCES = ("Sources: Kyiv Independent · BBC · IMD · Deccan Herald · Al Jazeera "
           "· Anadolu · Reuters · AP · UN News · GOV.UK · Yonhap · KBC · "
           "allAfrica · ICC · EORTC · B3 · Guardian · Investvio · FIFA · "
           "SABC Sport · IANS · ATP · Lionsgate · Channel 12 · Daily News · "
           "The News · CDMX · Forbes · ESA · NBC · VOA")

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

# (story num, lon, lat, label dx, label dy) -- pins 1-13, lead & feature.
# Europe cluster (Kyiv / Poland / Brussels / Antalya / Rome / Iraq) is
# tight on a 300px map, so labels are spread with leader lines.
PINS = [
    (1, 30.5, 50.5, 0, -16),     # Kyiv
    (2, 85.0, 19.5, 8, -12),     # Gopalpur / Akvan
    (3, 121.5, 25.0, 8, 12),     # Taipei (AI sell-off)
    (4, 30.7, 36.9, 16, 0),      # Antalya / COP31
    (5, 4.4, 50.8, -14, 14),     # Brussels
    (6, 22.0, 50.0, -18, 0),     # Poland missile
    (7, 44.2, 32.9, 16, 10),     # Jurf al-Sakhar, Iraq
    (8, 12.5, 41.9, 0, 16),      # Rome
    (9, 139.7, 35.7, 8, -12),    # Tokyo
    (10, 127.0, 37.5, -14, 12),  # Seoul
    (11, 36.0, 3.0, 8, -12),     # Turkana, Kenya
    (12, -89.2, 13.7, 8, -12),   # San Salvador
    (13, 174.8, -41.3, 8, -12),  # Wellington
]

# ---------------------------------------------------------------- lead panels
# Each draws a full-bleed flat illustration into a (x, y, w, h) box.

def _burst(draw, cx, cy, r, cols=(ORANGE, RED, GOLD)):
    for k, (rr, col) in enumerate(((r, cols[0]), (int(r * 0.65), cols[1]),
                                   (int(r * 0.35), cols[2]))):
        pts = []
        for i in range(16):
            a = math.pi * i / 8 + (k * 0.2)
            rad = rr if i % 2 == 0 else rr * 0.45
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        draw.polygon(pts, fill=col)


def _lead_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars (fixed positions)
    for sx, sy in ((18, 12), (52, 26), (96, 10), (140, 22), (188, 12),
                   (232, 26), (272, 14), (300, 30), (70, 40), (210, 42),
                   (120, 52), (260, 52), (30, 58), (170, 60)):
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(255, 255, 255))
    # missile trails: dashed arcs from upper right down to the bridges
    for (tx, ty, bx, by) in ((292, 8, 78, 108), (262, 4, 158, 110),
                             (232, 6, 238, 108)):
        for t in range(0, 11):
            f = t / 10.0
            px = tx + (bx - tx) * f
            py = ty + (by - ty) * f - 34 * math.sin(math.pi * f)
            if t % 2 == 0:
                draw.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2],
                             fill=GOLD)
    # river band
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=DARKBLUE)
    # skyline silhouettes
    for bx, bw, bh in ((0, 30, 34), (34, 22, 46), (60, 28, 30), (92, 24, 40),
                       (120, 30, 28), (154, 22, 44), (180, 28, 32),
                       (212, 24, 42), (240, 28, 30), (272, 40, 38)):
        draw.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                       fill=(8, 12, 24))
        for wy in range(y + h - 26 - bh + 6, y + h - 30, 9):
            for wx in (bx + 6, bx + 16):
                if wx < bx + bw - 3:
                    draw.rectangle([x + wx, wy, x + wx + 3, wy + 4],
                                   fill=(240, 200, 90))
    # three bridges across the river, with bursts where they are hit
    for bx in (58, 148, 228):
        draw.arc([x + bx - 26, y + h - 44, x + bx + 26, y + h - 6],
                 180, 360, fill=(200, 200, 200), width=3)
        draw.line([(x + bx - 26, y + h - 24), (x + bx + 26, y + h - 24)],
                  fill=(200, 200, 200), width=2)
    _burst(draw, x + 58, y + h - 34, 12)
    _burst(draw, x + 148, y + h - 36, 10)
    _burst(draw, x + 228, y + h - 34, 11)
    # title bars + caption
    chip(draw, x + 8, y + 8, "KYIV", bg=RED, size=13, h=22)
    bw = chip(draw, x + 8, y + 34, "3 BRIDGES HIT", bg=(255, 255, 255),
              fg=NAVY, size=10, h=18)
    draw.text((x + 8, y + h - 20), "Officials' count",
              font=font(BAR_SB, 9), fill=(255, 255, 255))


def _lead_akvan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    # India east-coast landmass (left)
    land = [(x, y + 18), (x + 62, y + 26), (x + 92, y + 58),
            (x + 84, y + 96), (x + 52, y + 128), (x + 30, y + h),
            (x, y + h)]
    draw.polygon(land, fill=TAN)
    draw.line(land + [land[0]], fill=TAN_DARK, width=2)
    # house on the coast
    draw.rectangle([x + 26, y + 96, x + 44, y + 110], fill=(255, 255, 255))
    draw.polygon([(x + 22, y + 96), (x + 35, y + 86), (x + 48, y + 96)],
                 fill=RED)
    draw.text((x + 10, y + 114), "GOPALPUR", font=font(BAR_B, 9),
              fill=INK)
    # cyclone spiral (white concentric arcs)
    cx, cy = x + 208, y + 70
    for r in (14, 24, 34, 44):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 20, fill=(255, 255, 255),
                 width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    # dashed track from Gopalpur to the spiral
    for t in range(0, 11):
        f = t / 10.0
        px = 96 + (208 - 96) * f
        py = 92 + (70 - 92) * f - 10 * math.sin(math.pi * f)
        if t % 2 == 0:
            draw.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2],
                         fill=(255, 255, 255))
    draw.ellipse([x + 91, y + 87, x + 101, y + 97], fill=RED,
                 outline=(255, 255, 255), width=1)
    # title bars + caption
    chip(draw, x + 8, y + 8, "CYCLONE AKVAN", bg=RED, size=13, h=22)
    chip(draw, x + 8, y + 34, "LANDFALL · 8 AM", bg=(255, 255, 255),
         fg=NAVY, size=10, h=18)
    draw.text((x + 8, y + h - 20), "Weather office · IMD",
              font=font(BAR_SB, 9), fill=(255, 255, 255))
    draw.text((x + w - 8, y + h - 20), "BAY OF BENGAL",
              font=font(BAR_SB, 9), fill=(255, 255, 255), anchor="ra")


def _lead_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # faint grid
    for gy in range(y + 30, y + h - 20, 22):
        draw.line([(x + 10, gy), (x + 178, gy)], fill=(52, 68, 102), width=1)
    # descending red chart
    pts = [(x + 14, y + 34), (x + 48, y + 52), (x + 82, y + 48),
           (x + 116, y + 78), (x + 150, y + 96), (x + 172, y + 122)]
    draw.line(pts, fill=(220, 60, 40), width=4, joint="curve")
    draw.polygon(pts + [(x + 172, y + h - 8), (x + 14, y + h - 8)],
                 fill=(120, 30, 26))
    draw.line(pts, fill=(220, 60, 40), width=4, joint="curve")
    for (px, py) in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 120, 90))
    # market table (right)
    rows = [("Taipei", "-6.2%"), ("Seoul", "-5.2%"), ("Tokyo", "-4.8%"),
            ("Hong Kong", "-1.9%")]
    draw.text((x + 190, y + 34), "INDEX CLOSE", font=font(BAR_B, 9),
              fill=(170, 180, 200))
    for i, (city, val) in enumerate(rows):
        ry = y + 52 + i * 20
        draw.text((x + 190, ry), city, font=font(BAR_SB, 12),
                  fill=(255, 255, 255))
        draw.text((x + w - 8, ry), val, font=font(BAR_B, 12), fill=(255, 120, 90),
                  anchor="ra")
    # title bars + caption
    chip(draw, x + 8, y + 8, "AI SELL-OFF", bg=RED, size=13, h=22)
    draw.text((x + 8, y + h - 20), "Closing prices · Reuters",
              font=font(BAR_SB, 9), fill=(255, 255, 255))


LEAD_PANELS = [_lead_kyiv, _lead_akvan, _lead_markets]


# ---------------------------------------------------------------- card motifs
# Each draws a small flat scene into a (x, y, w, h) box, with a data chip
# top-left and the source bottom-right inside the panel.

def _card_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(215, 228, 238))
    cx, cy = x + 34, y + 26
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=BLUE, width=3)
    draw.arc([cx - 20, cy - 20, cx + 20, cy + 20], 300, 60, fill=GREEN, width=6)
    draw.arc([cx - 20, cy - 20, cx + 20, cy + 20], 120, 210, fill=GREEN, width=6)
    # thermometer
    draw.rectangle([x + 118, y + 12, x + 128, y + 40], outline=INK, width=2,
                   fill=(255, 255, 255))
    draw.rectangle([x + 120, y + 22, x + 126, y + 38], fill=RED)
    draw.ellipse([x + 114, y + 36, x + 132, y + 48], fill=RED)
    draw.text((x + 140, y + 16), "35 by 35", font=font(BAR_B, 10), fill=INK)
    chip(draw, x + 4, y + 4, "NO DEAL", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "UN News", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_ukeu(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    # EU flag
    draw.rectangle([x + 12, y + 12, x + 62, y + 38], fill=(31, 58, 138))
    for k in range(8):
        a = math.pi * k / 4
        draw.ellipse([x + 37 + 8 * math.cos(a) - 1, y + 25 + 8 * math.sin(a) - 1,
                      x + 37 + 8 * math.cos(a) + 1, y + 25 + 8 * math.sin(a) + 1],
                     fill=GOLD)
    # UK flag (simplified)
    draw.rectangle([x + 72, y + 12, x + 122, y + 38], fill=(31, 58, 138))
    draw.line([(x + 72, y + 12), (x + 122, y + 38)], fill=(255, 255, 255), width=3)
    draw.line([(x + 122, y + 12), (x + 72, y + 38)], fill=(255, 255, 255), width=3)
    draw.line([(x + 97, y + 12), (x + 97, y + 38)], fill=RED, width=5)
    draw.line([(x + 72, y + 25), (x + 122, y + 25)], fill=RED, width=5)
    chip(draw, x + 4, y + 4, "AGREED", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "Reuters", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_poland(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 230, 235))
    # pine forest
    for tx in (18, 44, 70, 96, 122, 148):
        draw.polygon([(x + tx, y + 22), (x + tx + 9, y + 40), (x + tx + 18, y + 22)],
                     fill=GREEN)
        draw.rectangle([x + tx + 7, y + 40, x + tx + 11, y + 46], fill=(90, 60, 30))
    # cruise missile, diagonal
    draw.line([(x + 30, y + 14), (x + 150, y + 6)], fill=(120, 120, 120), width=7)
    draw.polygon([(x + 150, y + 2), (x + 162, y + 8), (x + 150, y + 14)],
                 fill=(90, 90, 90))
    draw.line([(x + 30, y + 14), (x + 44, y + 22)], fill=(120, 120, 120), width=4)
    chip(draw, x + 4, y + 4, "2 AIRPORTS PAUSED", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "AP", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_iraq(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    # tank
    draw.rectangle([x + 16, y + 26, x + 66, y + 40], fill=(60, 80, 50))
    draw.rectangle([x + 26, y + 18, x + 48, y + 26], fill=(60, 80, 50))
    draw.line([(x + 48, y + 22), (x + 78, y + 18)], fill=(60, 80, 50), width=4)
    for wx in (22, 34, 46, 58):
        draw.ellipse([x + wx, y + 40, x + wx + 8, y + 46], fill=INK)
    # palm
    draw.line([(x + 140, y + 46), (x + 140, y + 16)], fill=(120, 80, 40), width=4)
    for a in (200, 240, 280, 320, 0):
        r = math.radians(a)
        draw.line([(x + 140, y + 16),
                   (x + 140 + 16 * math.cos(r), y + 16 + 8 * math.sin(r))],
                  fill=GREEN, width=3)
    chip(draw, x + 4, y + 4, "JURF AL-SAKHAR", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "Reuters", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_italy(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(235, 232, 225))
    # crowd silhouettes
    for hx in (20, 46, 72, 98, 124, 150):
        draw.ellipse([x + hx, y + 18, x + hx + 12, y + 30], fill=INK)
        draw.pieslice([x + hx - 2, y + 30, x + hx + 14, y + 48], 180, 360,
                      fill=INK)
    # banner
    draw.rectangle([x + 30, y + 34, x + 140, y + 46], fill=RED)
    draw.text((x + 85, y + 35), "SCIOPERO", font=font(BAR_B, 9),
              fill=(255, 255, 255), anchor="ma")
    chip(draw, x + 4, y + 4, "24-HR STRIKE", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "Reuters", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_japan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.ellipse([x + 14, y + 18, x + 38, y + 42], fill=RED)
    # rising bar chart
    for i, bh in enumerate((10, 16, 22, 30)):
        bx = x + 58 + i * 26
        draw.rectangle([bx, y + 42 - bh, bx + 16, y + 42], fill=INK)
    draw.line([(x + 54, y + 42), (x + 168, y + 42)], fill=INK, width=2)
    chip(draw, x + 4, y + 4, "+2.3%", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "Anadolu", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_seoul(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 228, 236))
    # assembly building
    draw.polygon([(x + 52, y + 10), (x + 132, y + 10), (x + 92, y + 2)],
                 fill=BLUE)
    draw.rectangle([x + 52, y + 10, x + 132, y + 16], fill=BLUE)
    for cx0 in (58, 76, 94, 112, 128):
        draw.rectangle([x + cx0, y + 16, x + cx0 + 5, y + 42], fill=(240, 240, 240))
    draw.rectangle([x + 46, y + 42, x + 138, y + 47], fill=BLUE)
    draw.text((x + 148, y + 20), "DP", font=font(BAR_B, 14), fill=INK)
    chip(draw, x + 4, y + 4, "IMPEACH", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "Yonhap", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_kenya(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 200, 150))
    draw.ellipse([x + 140, y + 6, x + 162, y + 28], fill=(240, 160, 60))
    # oil derrick
    draw.line([(x + 40, y + 46), (x + 60, y + 8)], fill=INK, width=3)
    draw.line([(x + 80, y + 46), (x + 60, y + 8)], fill=INK, width=3)
    draw.line([(x + 46, y + 34), (x + 74, y + 34)], fill=INK, width=2)
    draw.line([(x + 52, y + 20), (x + 68, y + 20)], fill=INK, width=2)
    draw.line([(x + 60, y + 8), (x + 60, y + 2)], fill=INK, width=2)
    draw.rectangle([x + 96, y + 38, x + 128, y + 46], fill=(120, 80, 40))
    chip(draw, x + 4, y + 4, "FIRST OIL", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "KBC", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_bukele(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 228, 240))
    # ballot box
    draw.rectangle([x + 52, y + 20, x + 112, y + 46], fill=BLUE)
    draw.rectangle([x + 52, y + 20, x + 112, y + 26], fill=NAVY)
    draw.polygon([(x + 76, y + 20), (x + 82, y + 8), (x + 92, y + 10),
                  (x + 86, y + 20)], fill=(255, 255, 255))
    # flag stripe
    draw.rectangle([x + 128, y + 14, x + 158, y + 20], fill=(31, 58, 138))
    draw.rectangle([x + 128, y + 20, x + 158, y + 26], fill=(255, 255, 255))
    draw.rectangle([x + 128, y + 26, x + 158, y + 32], fill=(31, 58, 138))
    draw.text((x + 14, y + 22), "2027", font=font(BAR_B, 13), fill=INK)
    chip(draw, x + 4, y + 4, "FEB 2027 VOTE", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "AP", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


def _card_phillips(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(200, 220, 190))
    # pitch + stumps
    draw.rectangle([x + 20, y + 30, x + 160, y + 46], fill=(232, 220, 180))
    for sx in (28, 34, 40):
        draw.line([(x + sx, y + 22), (x + sx, y + 32)], fill=GOLD, width=2)
    # bat
    draw.line([(x + 96, y + 44), (x + 130, y + 8)], fill=(200, 160, 110), width=8)
    draw.line([(x + 130, y + 8), (x + 138, y + 2)], fill=(120, 80, 40), width=4)
    # ball
    draw.ellipse([x + 148, y + 32, x + 158, y + 42], fill=RED)
    draw.text((x + 58, y + 6), "118", font=font(PLAY_BOLD, 20), fill=INK)
    chip(draw, x + 4, y + 4, "118 · RECORD", bg=RED, size=8, h=14)
    draw.text((x + w - 4, y + h - 12), "ICC", font=font(BAR_SB, 8),
              fill=GREY, anchor="ra")


CARD_MOTIFS = [_card_cop, _card_ukeu, _card_poland, _card_iraq, _card_italy,
               _card_japan, _card_seoul, _card_kenya, _card_bukele,
               _card_phillips]


# ---------------------------------------------------------------- render

def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)

    # ---- masthead band
    d.text((MX, 16), "THE WORLD IN ONE DAY", font=font(BAR_B, 14), fill=RED)
    d.text((W - MX, 16),
           "38 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026",
           font=font(BAR_SB, 11), fill=INK, anchor="ra")
    rule(d, MX, 40, W - MX, 2, INK)
    rule(d, MX, 44, W - MX, 1)

    # ---- date line + subhead
    center(d, 52, "Friday 20 November 2026", font(PLAY_BLACK, 54))
    center(d, 118,
           "Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India "
           "· An AI sell-off sinks Asia's markets · UK and EU seal a deal",
           font(NEWS, 15), GREY)

    # ---- numbers strip (6 figures)
    rule(d, MX, 142, W - MX, 1, INK)
    cell = CW / 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = MX + cell * i + cell / 2
        d.text((cx, 150), num, font=font(PLAY_BOLD, 20), fill=RED, anchor="ma")
        d.text((cx, 176), label, font=font(BAR_SB, 10), fill=INK, anchor="ma")
        if i:
            d.line([(MX + cell * i, 148), (MX + cell * i, 186)], fill=RULE, width=1)
    rule(d, MX, 190, W - MX, 1, INK)

    # ---- region bar
    d.rectangle([MX, 196, W - MX, 222], fill=TINT)
    center(d, 203, REGION_LINE, font(BAR_SB, 15))

    # ---- leads: big illustration panel + kicker + headline + deck
    col_w = 312
    col_x = [MX, MX + 328, MX + 656]
    for i, lead in enumerate(LEADS):
        x = col_x[i]
        LEAD_PANELS[i](d, x, 230, col_w, 144)
        d.text((x, 380), lead["kicker"], font=font(BAR_B, 11), fill=RED)
        d.text((x + col_w, 380), lead["source"], font=font(BAR_SB, 10),
               fill=GREY, anchor="ra")
        lines = wrap(d, lead["head"], font(PLAY_BOLD, 20), col_w)
        yy = 394
        for ln in lines[:2]:
            d.text((x, yy), ln, font=font(PLAY_BOLD, 20), fill=INK)
            yy += 24
        dlines = wrap(d, lead["deck"], font(NEWS, 13), col_w)
        yy = 446
        for ln in dlines[:3]:
            d.text((x, yy), ln, font=font(NEWS, 13), fill=INK)
            yy += 16
        if i:
            d.line([(x - 8, 230), (x - 8, 492)], fill=RULE, width=1)
    rule(d, MX, 498, W - MX, 1, INK)

    # ---- cards: 2 rows of 5, each with a small illustration + data chip
    card_w, gap = 185, 10
    card_x = [MX + j * (card_w + gap) for j in range(5)]
    for i, card in enumerate(CARDS):
        r, c = divmod(i, 5)
        x, y = card_x[c], 506 + r * 144
        CARD_MOTIFS[i](d, x, y, card_w, 50)
        d.text((x, y + 54), card["kicker"], font=font(BAR_B, 10), fill=RED)
        d.text((x + card_w, y + 54), card["source"], font=font(BAR_SB, 9),
               fill=GREY, anchor="ra")
        lines = wrap(d, card["head"], font(PLAY_BOLD, 13), card_w)
        yy = y + 68
        for ln in lines[:2]:
            d.text((x, yy), ln, font=font(PLAY_BOLD, 13), fill=INK)
            yy += 15
        dlines = wrap(d, card["deck"], font(NEWS, 11), card_w)
        yy = y + 100
        for ln in dlines[:2]:
            d.text((x, yy), ln, font=font(NEWS, 11), fill=INK)
            yy += 13
        if c:
            d.line([(x - 5, y), (x - 5, y + 132)], fill=RULE, width=1)
    rule(d, MX, 798, W - MX, 1, INK)

    # ---- map (left) + briefs (right, two columns)
    map_x0, map_y0, map_w, map_h = MX, 828, 300, 118
    d.text((MX, 804), "WHERE IT HAPPENED · PINS 1–13", font=font(BAR_B, 12),
           fill=INK)
    d.text((W - MX, 804), "ALSO ON FRIDAY 20 NOVEMBER — 25 MORE STORIES",
           font=font(BAR_B, 12), fill=RED, anchor="ra")
    # solid tan land
    for (x0, y0, x1, y1) in LAND_RECTS:
        px0 = map_x0 + x0 / 88 * map_w
        py0 = map_y0 + y0 / 12 * map_h
        px1 = map_x0 + x1 / 88 * map_w
        py1 = map_y0 + y1 / 12 * map_h
        d.rectangle([px0, py0, px1, py1], fill=TAN)
    # faint graticule
    for gx in range(1, 12):
        gx_px = map_x0 + gx / 12 * map_w
        d.line([(gx_px, map_y0), (gx_px, map_y0 + map_h)],
               fill=TAN_DARK, width=1)
    for gy in range(1, 6):
        gy_px = map_y0 + gy / 6 * map_h
        d.line([(map_x0, gy_px), (map_x0 + map_w, gy_px)],
               fill=TAN_DARK, width=1)

    def pin_xy(lon, lat):
        return (map_x0 + (lon + 180) / 360 * map_w,
                map_y0 + (72 - lat) / 128 * map_h)

    for (num, lon, lat, dx, dy) in PINS:
        px, py = pin_xy(lon, lat)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + dx, py + dy), str(num), font=font(BAR_B, 9),
               fill=INK, anchor="mm")
        if dx or dy:
            d.line([(px, py), (px + dx, py + dy)], fill=RED, width=1)

    # briefs, two columns to the right of the map
    bf_x0 = MX + 316
    bf_w = (CW - 316) // 2 - 6
    bf = font(NEWS_SB, 10)
    for i, (num, text) in enumerate(BRIEFS):
        col = 0 if i < 13 else 1
        row = i if i < 13 else i - 13
        x = bf_x0 + col * (bf_w + 12)
        y = 824 + int(row * 9.8)
        d.text((x, y), "%d" % num, font=font(BAR_B, 10), fill=RED)
        d.text((x + 20, y), text, font=bf, fill=INK)

    # ---- legend line
    lx = MX
    ly = 956
    for (kind, label) in (("full", "CONFIRMED - checked against two sources"),
                          ("half", "CLAIM - one source, disputed"),
                          ("empty", "FORECAST - not yet happened")):
        if kind == "full":
            d.ellipse([lx, ly, lx + 9, ly + 9], fill=RED)
        elif kind == "half":
            d.ellipse([lx, ly, lx + 9, ly + 9], outline=RED, width=1)
            d.pieslice([lx, ly, lx + 9, ly + 9], 90, 270, fill=RED)
        else:
            d.ellipse([lx, ly, lx + 9, ly + 9], outline=RED, width=1)
        d.text((lx + 13, ly - 1), label, font=font(BAR_M, 10), fill=INK)
        lx += 13 + d.textlength(label, font=font(BAR_M, 10)) + 20
    d.text((lx, ly - 1), "Every story on this page is CONFIRMED.",
           font=font(BAR_B, 10), fill=RED)

    # ---- DATE CHECK box
    dc_lines = wrap(d, DATE_CHECK, font(NEWS, 10), CW - 24)
    box_top = 968
    box_h = 6 + len(dc_lines) * 12 + 6
    d.rectangle([MX, box_top, W - MX, box_top + box_h], outline=RED, width=1)
    yy = box_top + 6
    for ln in dc_lines:
        d.text((MX + 12, yy), ln, font=font(NEWS, 10), fill=INK)
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
