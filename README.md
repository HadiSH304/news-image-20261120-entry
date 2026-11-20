# The World in One Page — Friday 20 November 2026

A make.fun entry for
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
one image that sums up 20 November 2026's world news.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/HadiSH304/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/HadiSH304/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120)

## The image

A newspaper front page in one 1024×1024 image. The masthead names the day
— **FRIDAY 20 NOVEMBER 2026** — and 36 stories cover it:

- **Lead:** Cyclone Akvan makes landfall in eastern India — 370,000+ evacuated
- **Lead:** Russia fires ~30 ballistic missiles at Kyiv — three bridges hit
- **Lead:** COP31 reaches its final day deadlocked — fossil-fuel phase-out cut
- **AI sell-off sweeps Asia** · **Anthropic closes its first day at $97.17** ·
  **BepiColombo reaches Mercury** · **Burnham hosts the EU–UK reset summit** ·
  **Phillips hits 118 against India** · **Bukele files for a third term** ·
  **Italy holds a general strike** · and 22 more briefs, with a dotted world
  map, a DATE CHECK box for what belongs to Thursday 19 November (or hasn't
  happened yet), and a verdict.

Every story was checked against at least two sources on 20 November 2026;
every story on the page is tagged CONFIRMED. The DATE CHECK names the
Thursday items deliberately left out, so the day boundary is policed in
the open.

## How it runs

`main.py` draws the page with PIL (`compose.py`) and writes it to
`/output/entry.png`. No network, no clock, no randomness — two runs write
identical bytes. Fonts are vendored under `fonts/`. The image is 1024×1024
and under 1 MiB.

```
python3 main.py
```
