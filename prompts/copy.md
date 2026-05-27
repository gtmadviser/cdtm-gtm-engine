# Email copy — step 1 + step 2

Write a 2-step sequence. Personalize from each lead's `trigger_signal`. Follow every rule.

## Rules (from real campaign data)
- **50–70 words**, max 3 short paragraphs.
- **Scenario opener** — start with their situation/pain, not your product or a stat.
- **No em-dashes (—).** Commas/periods only.
- **No unsupported stats** ("21x", "save 64%"). Worst performers, every time.
- **One soft CTA — default to a pilot / design-partner ask**, not a sale ("open to being one of our first design partners?"). Never a hard pitch.
- **Match tone to segment** (formal vs. informal) and be consistent.
- End the body with `{{signature}}` (no hardcoded greeting block).
- First line personalized from the trigger — specific enough it couldn't be sent to anyone else.

## Step 1 — cold (structure)
1. **Opener:** their scenario/trigger, in their words. (1 sentence)
2. **Bridge:** the cost of that problem + a hint you solve it. (1–2 sentences)
3. **CTA:** soft ask. (1 sentence)
4. `{{signature}}`

Write 2 subject lines to A/B test. Keep subjects ≤ 5 words, lowercase-ish, curiosity over hype.

### First-line strategies (pick one per lead — this is where beginners get stuck)
- **Problem-sniffing** (best when you have a trigger): "I looked you up and noticed [specific trigger]…" then the implied problem.
- **Whole-offer** (best when you have NO trigger data — common for early teams): put the value prop straight in the subject + first line. "We help [ICP] do [outcome] without [pain]."
- **AI-generic-with-a-detail**: use one real variable from their website/LinkedIn so it reads researched, not blasted.
Tell the team which strategy you used and why, so they can repeat it.

## Step 2 — follow-up (send +3 days)
- Shorter than step 1. Reference the first email lightly, add one new angle or proof point. Do **not** just repeat features (follow-ups that repeat features get ~0 opportunities). One line + CTA is plenty.

## Pre-flight check (run before writing the file)
Reject and rewrite if any fails:
- [ ] ≤ 70 words, ≤ 3 short paragraphs
- [ ] No em-dashes
- [ ] No unsupported stats / hype numbers
- [ ] None of: "hope this finds you well", "just checking in", "let's hop on a call", "circle back"
- [ ] CTA answerable in ≤ 5 words
- [ ] First line is specific enough it couldn't be sent to anyone else
- [ ] Ends with `{{signature}}`, no hardcoded greeting

## Write to `output/campaign.md`

```
# Campaign: [name]
North-star metric: [e.g. meetings booked / 100 sends]
ICP: [one line]

## Step 1 (Day 1)
Subject A: ...
Subject B: ...

[body]
{{signature}}

## Step 2 (Day 4)
Subject: Re: [step-1 subject]

[body]
{{signature}}
```

Then show the team how a personalized step-1 looks for **3 specific leads** from their list, using each lead's real trigger.

## If the channel is LinkedIn (not email)
Same pipeline, shorter copy, no subject lines:
- **Connection note:** ≤ 300 characters, one personalized line tied to their trigger + a soft reason to connect. No pitch.
- **DM 1 (after they accept):** 2–3 sentences. Scenario opener + the pilot/design-partner ask.
- **DM 2 (+3 days):** one line, new angle, soft nudge.
Write these to `output/campaign.md` under a `## LinkedIn` heading instead of the email steps. All other rules (short, no em-dashes, no fake stats, personalize from trigger) still apply.
