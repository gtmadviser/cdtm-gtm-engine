# Live lead sourcing — find 25–50 real leads

We source **live** — no canned dataset. Real companies, real people, for *this* team's market. Small and real beats big and fake.

## Order of attack (use the first that works, stop at 25–50)

1. **Public directories & marketplaces.** Industry associations, "best X in [city]" lists, review sites, app/tool marketplaces, Crunchbase-style lists, local chamber listings. These are designed to be read and rarely block.
2. **Maps / local search** (for local/SMB ICPs). Search a category in a city, collect business name + website + phone. Repeat across a few cities.
3. **Company websites.** Once you have companies, visit their sites for a generic/role-based contact (info@, or a named owner on an About/Team page).
4. **LinkedIn search URLs** (manual). Build a search for the role + industry; collect names/companies the team can use. Respect that LinkedIn blocks scraping — use it to *identify*, not bulk-extract.
5. **Free API tiers** only if a team already has one (Apollo/Hunter). Don't burn class time on signups.

## Robustness rules
- **Target 25–50.** Do not try to scrape thousands.
- Be polite: modest request rates, honor robots, prefer official/public pages.
- **Never end with zero.** If scraping is blocked, fall back to web search → open the directory page → extract the rows manually. Hand-built 25 is fine.
- Capture a **trigger signal** per lead when you can (what made them a fit). It powers personalization.

## Write to `output/leads.csv`

Use the schema in `data/leads_template.csv`:

```
company,website,contact_name,role,email,location,trigger_signal,source,notes
```

- `email` may be blank or a guessed pattern (e.g. `info@domain` or `first@domain`) — flag guesses in `notes`.
- `trigger_signal` = the specific reason this lead fits (e.g. "hiring 2 SDRs", "uses Shopify", "5-star but no online booking").
- `source` = where you found them (directory URL, maps, etc.).

Quality bar: a teammate should be able to read any row and understand *why* this lead is on the list.
