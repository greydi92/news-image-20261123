[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/greydi92/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/greydi92/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Picture — Monday 23 November 2026

A newspaper front page that sums up the world's news of
**Monday 23 November 2026** in a single 1024×1024 image: seven stories
that happened or were first reported that day, from a collapsed climate
summit to a record cricket total.

Bounty: https://make.fun/bounty/news-image-20261123

## The seven stories

1. **COP31 collapses — and the blame begins** (lead story). The UN
   climate talks in Antalya end with no deal: the draft dropped every
   mention of fossil fuels, the UN chief is "deeply disappointed", and
   the EU says oil states hijacked the text. Sources: CNN, Le Monde,
   WSJ, The Times.
2. **Hormuz attacks hit a wartime high.** Shipping attacks reach their
   highest level since the US–Iran war began in February; three tankers
   were struck over the weekend. Sources: CNN, NY Post, Arab News.
3. **Minister quits over AI exam cheating.** South Korea's education
   minister resigns after an AI-driven cheating scandal in the national
   exams. Sources: Observer Voice, The Daily Jagran.
4. **India's record 720 puts NZ on the ropes.** India declare on 720
   for 9 at the Basin Reserve, Wellington — a record Test total in New
   Zealand. Source: Observer Voice.
5. **Nine killed in Gaza in 48 hours.** The toll since the October 2025
   ceasefire reaches 1,661. Source: The Random Department daily roundup.
6. **Nepal PM talks with Modi in Delhi.** Balendra Shah, on a state
   visit, holds bilateral talks with India's prime minister. Source:
   Observer Voice.
7. **Swimmer crosses the Strait of Hormuz.** Lewis Pugh swims the
   strait as tankers burn nearby, to flag the war's toll on wildlife.
   Sources: CBS News, France 24.

## How the entry is built

- `gen_image.py` draws `entry.png` from scratch with Pillow and the
  DejaVu fonts — masthead, four illustrated story panels, a
  three-item "World in Brief" column, and a one-line summary footer.
  No photos, no downloaded images, no borrowed logos; every pixel is
  drawn by this code. Text is wrapped to each panel's width so no
  headline or standfirst can overflow.
- `main.ts` (Node 22, standard library only, no network) copies the
  shipped `entry.png` into `MAKEFUN_OUTPUT_DIR` (or `/output`) and
  chmods it 0644, so two runs write byte-identical output.
- `entry.png` is a 1024×1024 PNG, about 144 KB — inside the 1 MiB cap.

## Run it

```sh
python3 gen_image.py            # re-render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

Built for the make.fun bounty — referral code `qgn48q27`.
