# Using the Blitz API — "find my TAM / source leads"

Official docs: https://docs.blitz-api.ai · Get a key (free credits): https://app.blitz-api.ai · Key details: https://docs.blitz-api.ai/api-reference/account/get-api-key-details

- **Base URL:** `https://api.blitz-api.ai/v2`
- **Auth:** header `x-api-key: <YOUR_KEY>` + `Content-Type: application/json`
- **Key in `.env`:** `BLITZAPI_API_KEY` (each person uses their OWN key)
- **Rate limit:** 5 requests/second (all plans). Sleep ~0.2s between calls.
- **Check key + credits:** `GET /v2/account/key-info`

## The workshop default
`scripts/source_leads.py` already does this end to end: it reads `output/icp.json` and calls `POST /v2/search/people`, writing `output/leads.csv`.
```bash
python3 scripts/source_leads.py --limit 30           # decision-makers + LinkedIn URLs
python3 scripts/source_leads.py --limit 30 --emails  # also verified work emails
python3 scripts/source_leads.py --dry-run            # 1 page, to test the filters
```

## Under the hood

### People search — `POST /v2/search/people` (best for finding decision-makers)
Combines company + person filters. Max 50 per page, cursor pagination.
```json
{
  "company": { "industry": {"include": ["Software Development"]}, "employee_range": ["1-10","11-50"],
               "hq": {"country_code": ["DE"]}, "type": {"exclude": ["Nonprofit"]} },
  "people":  { "job_title": {"include": ["CEO","Founder","Geschäftsführer","Owner"], "exclude": ["Assistant","Intern"]},
               "job_level": ["C-Team","Director"], "location": {"country_code": ["DE"]} },
  "max_results": 50,
  "cursor": "<pass the cursor from the previous response for the next page>"
}
```
Each result has `first_name, last_name, full_name, headline, location, linkedin_url, experiences[]` (the current company is the experience where `job_is_current` is true).

### Other endpoints
- `POST /v2/search/companies` — companies only (max 25/page).
- `POST /v2/enrichment/email` — `{ "person_linkedin_url": "..." }` → verified work email (`found`, `email`).
- `POST /v2/enrichment/domain-to-linkedin` — `{ "domain": "..." }` → `company_linkedin_url`.
- `POST /v2/enrichment/company` — `{ "company_linkedin_url": "..." }` → size, industry, headcount, founded year.

## Gotchas
- **Industry names are LinkedIn's exact taxonomy**, case-sensitive (e.g. `"IT Services and IT Consulting"`). If you get 0 results: check the industry name, widen `employee_range`, or drop `keywords`. Common names are in `prompts/sourcing.md`.
- **Keywords are language-specific** — German keywords return 0 in FR/IT/ES.
- `employee_count.min/max: 0` means "no filter", not "0 employees".
- Email enrichment needs the person's LinkedIn URL, not the company's.
