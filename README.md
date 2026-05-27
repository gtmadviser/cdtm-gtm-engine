# gtm-engine-starter

Build the first version of your product's **outbound GTM engine** — in 30 minutes, with Claude Code doing the heavy lifting.

By the end you'll have a **ready-to-send cold email campaign** for *your* MPD product: a real list of target leads, sharp ICP, and personalized copy.

> You will **not** send anything in this session. You'll produce a campaign you *could* load into Instantly/Lemlist and send later.

---

## Before you start (do this BEFORE class)

See the setup guide your instructor sent. You need:
1. **Claude Code** installed and authenticated (API key or Claude Pro/Max)
2. This repo cloned
3. One successful `claude` run to confirm it works

In class we spend ~5 min on setup, not 25. Arrive ready.

---

## The task (30 min, with your team)

Open this folder and run:

```bash
claude
```

Then tell Claude what your product is, and work through these 4 steps. Claude knows the workflow (see `CLAUDE.md`) — let it drive, you make the calls.

1. **Define your ICP** — who exactly, and what *trigger* says they need you *now*.
2. **Source 25–50 real leads** — Claude finds them live (web/scrape/free sources) for your actual market.
3. **Write the copy** — personalized step-1 + step-2 emails, following the rules in `CLAUDE.md`.
4. **Assemble the campaign** — output a leads CSV + the email sequence to `output/`.

Just say to Claude:
> "Read CLAUDE.md, then walk me through building a first campaign. Our product is ___ and it helps ___."

---

## Definition of done

In `output/` you have:
- [ ] `icp.md` — your ICP + trigger, in one tight paragraph
- [ ] `leads.csv` — 25–50 real leads with the columns in `data/leads_template.csv`
- [ ] `campaign.md` — step-1 + step-2 copy, ready to paste into a sending tool
- [ ] You can name your **one north-star metric** (e.g., meetings / 100 sends)

See `examples/example_campaign.md` for the target shape.

---

## Repo map

```
README.md             you are here — the task
CLAUDE.md             the engine's brain: workflow + guardrails Claude follows
prompts/icp.md        ICP definition framework
prompts/sourcing.md   how to live-source leads (free, robust, polite)
prompts/copy.md       email copy rules (learned from real campaigns)
data/leads_template.csv   the lead schema
scripts/scrape_example.py polite scraper skeleton Claude can adapt
examples/             a worked example so you know what "done" looks like
output/               your campaign lands here
```
