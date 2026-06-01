# Live lead sourcing — build a real TAM list

We source **live**, real people for *this* team's market. Small and real (25–50) beats big and fake.

## Primary path: the Blitz API (pre-wired)

`scripts/source_leads.py` pulls real decision-makers (with LinkedIn URLs) that match the ICP, using the Blitz API (your own `BLITZAPI_API_KEY` in `.env`, free at https://app.blitz-api.ai). Full API contract + gotchas: `prompts/blitzapi.md`. No pip installs.

**Step 1 — write the machine-readable ICP.** From the team's ICP, write `output/icp.json` (shape in `data/icp.example.json`):
```json
{
  "label": "what you're targeting",
  "country_code": "DE",
  "industries": ["Software Development"],
  "keywords": [],
  "employee_range": ["1-10", "11-50"],
  "job_title_include": ["CEO", "Founder", "Geschäftsführer", "Owner"],
  "job_title_exclude": ["Assistant", "Intern"],
  "job_level": ["C-Team", "Director"],
  "max_results": 25
}
```

**Step 2 — pull the list.**
```bash
python3 scripts/source_leads.py --limit 30          # LinkedIn URLs (fast, cheap)
python3 scripts/source_leads.py --limit 30 --emails # also verified work emails
python3 scripts/source_leads.py --dry-run           # 1 page, to test your filters
```
Writes `output/leads.csv`. Show the team the first few on screen, that is the wow.

### Industry names are exact (LinkedIn taxonomy, case-sensitive)
`industries` must match LinkedIn's names exactly. Common ones:
`"Software Development"`, `"IT Services and IT Consulting"`, `"Financial Services"`, `"Accounting"`,
`"Real Estate"`, `"Hospitality"`, `"Restaurants"`, `"Construction"`, `"Retail"`, `"Marketing Services"`,
`"Medical Practices"`, `"Hospitals and Health Care"`, `"Automotive"`, `"Insurance"`, `"Legal Services"`,
`"Staffing and Recruiting"`, `"Wellness and Fitness Services"`, `"E-Learning Providers"`.
If unsure, leave `industries` empty and use `keywords` (matches company name/about) plus country and titles. Keywords are language-specific (German keywords won't match in France).

### If it returns nothing
Loosen one thing at a time: confirm the industry name is exact, widen `employee_range`, drop `keywords`, or broaden `job_title_include`. Still stuck? Use the fallback below. **Never let the team end at zero.**

## Fallback path: free sources (no API)
1. **Public directories & marketplaces** (association lists, "best X in [city]", review sites, app marketplaces). Designed to be read, rarely block.
2. **Maps / local search** for local SMB ICPs: business name + website.
3. **Company sites** for a role-based contact (info@, owner on the About page).
4. **`scripts/scrape_example.py`** — a polite scraper skeleton Claude can adapt.
Be polite: modest rates, honor robots, prefer official/public pages. Hand-built 25 is fine.

## The schema (`output/leads.csv`)
`company, website, contact_name, role, email, location, linkedin_url, trigger_signal, source, notes`
- `linkedin_url` powers the LinkedIn-first sequence; `email` powers the email backup.
- `trigger_signal` = the specific reason this lead fits (what made them a fit, why now). It powers personalization, fill it in even if the API didn't.
- A teammate should be able to read any row and understand *why* this lead is on the list.
