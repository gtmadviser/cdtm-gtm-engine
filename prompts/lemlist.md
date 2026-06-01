# Using the lemlist API — "set up my multichannel campaign"

Official docs: https://developer.lemlist.com/api-reference/getting-started/overview · index: https://developer.lemlist.com/llms.txt

- **Base URL:** `https://api.lemlist.com/api`
- **Auth:** HTTP Basic with an **empty username** and your API key as the **password**.
  - curl: `--user ":$LEMLIST_API_KEY"`
  - code: header `Authorization: Basic base64(":" + KEY)`
- **Key in `.env`:** `LEMLIST_API_KEY` (each person uses their OWN; create at lemlist → Settings → Integrations → API)
- **Required header:** `User-Agent: Mozilla/5.0 ...` — without a browser-like UA, Cloudflare returns **403**. curl/browsers set it automatically; Python `urllib` does NOT, so set it.
- **Rate limit:** ~20 requests / 2 seconds. Sleep ~0.15–0.2s between calls.

## The multichannel flow (LinkedIn-first + email)
The visual sequence builder in the lemlist UI is the easiest place to design the sequence, but you can do it all by API:

1. **Create a campaign** (lemlist UI, or `POST /campaigns`). Connect your **LinkedIn** + a **mailbox**. Copy the campaign id (`cam_...`).
2. **Add your leads** from `output/leads.csv` (the LinkedIn URL drives the LinkedIn steps; the email drives the email steps):
   `POST /campaigns/{campaignId}/leads/?deduplicate=true&verifyEmail=true`
   body: `{ "email", "firstName", "lastName", "companyName", "companyDomain", "linkedinUrl", "jobTitle" }`
   (for leads with no email yet, add `&findEmail=true&linkedinEnrichment=true`).
3. **Build the sequence steps.** `GET /campaigns/{id}/sequences` returns the sequence tree keyed by sequence id (each has `steps[]`); take the root sequence id, then `POST /sequences/{sequenceId}/steps` for each step:
   - connection note (≤300 chars): `{ "type":"linkedinInvite", "delay":0, "message":"hey {{firstName}}, ..." }`
   - DM after they accept: `{ "type":"linkedinSend", "delay":1, "message":"{{firstName}}, ..." }`
   - email backup: `{ "type":"email", "delay":3, "subject":"...", "message":"<div>...</div>" }`
4. Leave the campaign **paused** and review in the UI before launching.

`scripts/push_to_lemlist.py` does step 2 (and optionally step 3) from your output files:
```bash
python3 scripts/push_to_lemlist.py --campaign cam_xxx                       # add output/leads.csv
python3 scripts/push_to_lemlist.py --campaign cam_xxx --steps output/sequence.json --replace
```
`output/sequence.json` is just an array of step objects, e.g.
```json
[ {"type":"linkedinInvite","delay":0,"message":"hey {{firstName}}, ..."},
  {"type":"linkedinSend","delay":1,"message":"{{firstName}}, ..."},
  {"type":"email","delay":3,"subject":"quick one","message":"<div>Hi {{firstName}},<br><br>...{{accountSignature}}</div>"} ]
```

## Step types + rules
- Types: `linkedinInvite`, `linkedinSend`, `email`, `linkedinVisit`, `phone`.
- Email body is the **`message`** field (HTML), with a separate **`subject`**. It is NOT `body`.
- **PATCH a step requires `type`** even if unchanged (else 400). There's no upsert: to replace, GET → DELETE each → POST new.
- Template variables: `{{firstName}}`, `{{lastName}}`, `{{companyName}}`, and `{{accountSignature}}` (your mailbox signature). End emails with `{{accountSignature}}`, don't hardcode a signature.

## Other useful endpoints
- `GET /campaigns/{id}` — status (draft/paused/running), senders.
- `POST /v2/enrichments/bulk` then poll `GET /enrich/{id}` — find missing emails from LinkedIn URLs.
- `GET /activities?campaignId={id}&createdAtFrom=...&createdAtTo=...` — replies/opens/sends (NOT `/campaigns/{id}/activities`, which returns HTML).
- `GET /v2/campaigns/{id}/stats?startDate=...&endDate=...` — performance.
