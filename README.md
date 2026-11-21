# The World in One Day — Friday 20 November 2026

A make.fun entry for
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
one image that sums up 20 November 2026's world news.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/HadiSH304/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/HadiSH304/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120)

## The image

A newspaper front page in one 1024×1024 image. The masthead names the day
— **FRIDAY 20 NOVEMBER 2026** — and 38 stories cover it:

- **Lead:** Russian missiles hit three Kyiv bridges — about 110 missiles
  and 400 drones, at least nine killed across Ukraine
- **Lead:** Cyclone Akvan makes landfall in eastern India — 370,000+
  evacuated, no deaths reported
- **Lead:** AI sell-off sinks Asia's stock markets — Taiwan's index −6.2%,
  its worst week since 1991
- **COP31 reaches its last day with no deal** · **UK and EU seal a
  'reset' deal** · **Russian cruise missile lands in Poland** · **Iraqi
  army enters a militia stronghold** · **General strike over Italy's
  budget** · **Japan's inflation picks up to 2.3%** · **Korea's ruling
  party to impeach top judge** · **Kenya starts drilling its first oil
  well** · **Bukele files for a third term** · **Phillips hits 118
  against India** · and 25 more briefs, with a solid-land world map, a
  DATE CHECK box for what belongs to Thursday 19 November (or hasn't
  happened yet), and a confidence legend.

Every story was checked against at least two sources on 20 November 2026;
every story on the page is tagged CONFIRMED. The DATE CHECK names the
Thursday items deliberately left out, so the day boundary is policed in
the open.

## How it runs

`main.py` copies the pre-rendered front page (`image.png`, produced by
`compose.py`) to `/output/entry.png`. The entrypoint uses only the Python
standard library — no third-party packages, no network, no clock, no
randomness — two runs write identical bytes. Fonts are vendored under
`fonts/`. The image is 1024×1024 and under 1 MiB.

```
python3 main.py
```
