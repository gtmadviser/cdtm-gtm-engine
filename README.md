# cdtm-gtm-engine

Build the first version of your product's **outbound GTM engine** in ~35 minutes, with Claude Code doing the heavy lifting.

By the end you'll have a **ready-to-send LinkedIn + email campaign** for *your* product: a sharp ICP, a real list of target leads (with LinkedIn URLs), and personalized copy, set up in lemlist.

> You don't have to launch anything in class. You'll walk out with a real campaign you *could* send.

---

## Before you start (do this BEFORE class)

See the setup guide your instructor sent. You need:
1. **Claude Code** installed and authenticated (Claude Pro/Max or an Anthropic API key)
2. This repo **forked** and your fork cloned
3. One successful `claude` run to confirm it works

In class we spend ~5 min on setup, not 25. Arrive ready.

### Keys (a few minutes, free)
```bash
cp .env.example .env
```
Paste your own **BLITZAPI_API_KEY** (https://app.blitz-api.ai) and **LEMLIST_API_KEY** (lemlist -> Settings -> Integrations -> API). Both are free to start; `.env` is gitignored.

---

## The task (~35 min, with your team)

Open this folder and run:
```bash
claude
```
Tell Claude what your product is and work through 4 steps. Claude knows the workflow (see `CLAUDE.md`), let it drive, you make the calls.

1. **Define your ICP** — who exactly, and the *trigger* that says they need you *now*. Claude writes it to `output/icp.md` and `output/icp.json`.
2. **Source a real list** — Claude runs `scripts/source_leads.py` to pull 25–50 real decision-makers (with LinkedIn URLs) for your market via the Blitz API → `output/leads.csv`.
3. **Write the copy** — a LinkedIn connection note + DMs, plus a 2-step email backup, with a soft pilot / design-partner CTA. → `output/campaign.md`.
4. **Set it up in lemlist** — import the leads, paste the sequence. Ready to send.

Just say to Claude:
> "Read CLAUDE.md, then walk me through building a first campaign. Our product is ___ and it helps ___."

---

## Definition of done

In `output/` you have:
- [ ] `icp.md` + `icp.json` — your ICP + trigger (human + machine-readable)
- [ ] `leads.csv` — 25–50 real leads with LinkedIn URLs (columns in `data/leads_template.csv`)
- [ ] `campaign.md` — connection note + DMs + a 2-step email, ready to paste
- [ ] a campaign set up in **lemlist**
- [ ] you can name your **one north-star metric** (e.g. pilot calls / 100 reaches)

See `examples/example_campaign.md` for the target shape.

---

## Repo map

```
README.md                 you are here, the task
CLAUDE.md                 the engine's brain: workflow + guardrails Claude follows
RECOMMENDED-STACK.md      the tools to actually run this (ask Claude "what should I use for X?")
.env.example              copy to .env, paste the Blitz API key from your instructor
prompts/icp.md            ICP definition framework
prompts/sourcing.md       how to build a real list (Blitz API first, free fallback)
prompts/blitzapi.md       Blitz API contract — "find my TAM"
prompts/lemlist.md        lemlist API contract — "set up my multichannel campaign"
prompts/copy.md           copy rules (learned from real campaigns)
scripts/source_leads.py   pulls a real TAM list via the Blitz API (no pip installs)
scripts/push_to_lemlist.py adds your leads (+ optional steps) into a lemlist campaign
scripts/scrape_example.py polite scraper skeleton, the free fallback
data/icp.example.json     shape for output/icp.json (the sourcing config)
data/leads_template.csv   the lead schema
examples/                 a worked example so you know what "done" looks like
output/                   your campaign lands here
```

## Go deeper after class
- **Which tools to use?** Ask Claude, or open `RECOMMENDED-STACK.md`.
- Everything from the session lives at **cdtm.gtmadviser.com**.
- Clay University — free GTM-engineering course · Eric Nowoslawski (Growth Engine X) — free cold-email course · r/GTMEngineering — the community.
