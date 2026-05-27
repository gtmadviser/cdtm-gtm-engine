# Email copy — step 1 + step 2

Write a 2-step sequence. Personalize from each lead's `trigger_signal`. Follow every rule.

## Rules (from real campaign data)
- **50–70 words**, max 3 short paragraphs.
- **Scenario opener** — start with their situation/pain, not your product or a stat.
- **No em-dashes (—).** Commas/periods only.
- **No unsupported stats** ("21x", "save 64%"). Worst performers, every time.
- **One soft CTA** (interest or a 10-min call), never a hard pitch.
- **Match tone to segment** (formal vs. informal) and be consistent.
- End the body with `{{signature}}` (no hardcoded greeting block).
- First line personalized from the trigger — specific enough it couldn't be sent to anyone else.

## Step 1 — cold (structure)
1. **Opener:** their scenario/trigger, in their words. (1 sentence)
2. **Bridge:** the cost of that problem + a hint you solve it. (1–2 sentences)
3. **CTA:** soft ask. (1 sentence)
4. `{{signature}}`

Write 2 subject lines to A/B test. Keep subjects ≤ 5 words, lowercase-ish, curiosity over hype.

## Step 2 — follow-up (send +3 days)
- Shorter than step 1. Reference the first email lightly, add one new angle or proof point. Do **not** just repeat features (follow-ups that repeat features get ~0 opportunities). One line + CTA is plenty.

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
