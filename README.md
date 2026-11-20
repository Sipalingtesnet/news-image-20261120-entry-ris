# Sum up 20 November 2026 world news in one image

[![Bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/Sipalingtesnet/news-image-20261120-entry-ris/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/Sipalingtesnet/news-image-20261120-entry-ris/reward.svg)](https://make.fun/bounty/news-image-20261120)

# THE WORLD TODAY — Friday, 20 November 2026

Entry for the [make.fun bounty "Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120). The entry is a newspaper front page, THE WORLD TODAY, dated FRIDAY, 20 NOVEMBER 2026, that sums up the day's world news in a single 1024x1024 PNG: six headline panels laid out in a two-column grid under a bold masthead, each with a kicker, headline, short deck, and a hand-drawn vector icon, plus a news ticker across the footer. It is generated deterministically with Pillow (no network, no randomness), and `main.py` delivers it to `/output/entry.png` as a plain byte copy.

## How to run

- `python3 generate_image.py` — regenerates `entry.png` deterministically (requires Pillow and the DejaVu fonts; byte-identical across runs).
- `python3 main.py` — copies the repo-held `entry.png` to `/output/entry.png` (Python 3.13, stdlib only, no network) and prints the output path, size in bytes, and sha256.

## The six stories

1. WORLD — Trump: no rush on Iran; will see what happens after Jan. 1.
2. JUSTICE — ICJ rules Myanmar committed genocide against the Rohingya, a historic first.
3. SPACE — Voyager 1 reaches one light-day from Earth (16 billion miles out).
4. INDIA — Cyclone Akvan strikes the Odisha coast; 300,000 evacuated.
5. EUROPE — Leaders in Berlin ready for talks with Russia to end the Ukraine war, with Kyiv at the table.
6. GAMES — GTA 6 tops $1.84 billion on day one, the biggest launch in game history.
