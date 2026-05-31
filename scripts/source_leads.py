#!/usr/bin/env python3
"""
Source a real target-market (TAM) list for your ICP via the Blitz API.

Reads your ICP from output/icp.json (Claude writes this for you), finds real
decision-makers on LinkedIn that match it, and writes them to output/leads.csv
with their LinkedIn URL (and, with --emails, a verified work email).

Usage:
    python3 scripts/source_leads.py                # ~25 leads for your ICP
    python3 scripts/source_leads.py --limit 50     # up to 50
    python3 scripts/source_leads.py --emails       # also enrich verified emails (slower)
    python3 scripts/source_leads.py --config path/to/icp.json
    python3 scripts/source_leads.py --dry-run      # check filters, fetch 1 page only

Needs BLITZAPI_API_KEY in a .env file in the repo root (see .env.example).
No pip installs required: standard library only.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "https://api.blitz-api.ai/v2"
RATE_LIMIT_SLEEP = 0.5  # API allows 5 req/s; wait 0.5s between calls
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# Sensible defaults so the script still runs if a field is missing from your ICP.
DEFAULTS = {
    "label": "My ICP",
    "country_code": "DE",
    "industries": [],          # LinkedIn industry names, exact match (see prompts/sourcing.md)
    "keywords": [],            # match company name/about; language-specific
    "employee_range": ["1-10", "11-50"],
    "exclude_type": ["Nonprofit"],
    "job_title_include": ["CEO", "Founder", "Co-Founder", "Owner",
                           "Managing Director", "Geschäftsführer", "Inhaber"],
    "job_title_exclude": ["Assistant", "Intern", "Working Student"],
    "job_level": ["C-Team", "Director"],
    "max_results": 25,
}

CSV_FIELDS = ["company", "website", "contact_name", "role", "email",
              "location", "linkedin_url", "trigger_signal", "source", "notes"]


def load_api_key():
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(env_path):
        sys.exit("ERROR: no .env file found. Copy .env.example to .env and paste the "
                 "BLITZAPI_API_KEY your instructor shared in class.")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("BLITZAPI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    sys.exit("ERROR: BLITZAPI_API_KEY is empty in .env. Paste the key your instructor shared.")


def api_post(key, endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL + endpoint, data=data, method="POST",
        headers={"x-api-key": key, "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")
            if e.code == 429:
                wait = int(e.headers.get("Retry-After") or 5)
                print(f"  rate limited, waiting {wait}s (shared key, this is normal)...")
                time.sleep(wait)
                continue
            if e.code in (401, 403):
                sys.exit(f"ERROR: Blitz API rejected the key ({e.code}). "
                         "Double-check BLITZAPI_API_KEY in .env.")
            print(f"  HTTP {e.code}: {body[:200]}")
            return None
        except Exception as e:  # noqa: BLE001 - keep it friendly for beginners
            print(f"  network hiccup (attempt {attempt + 1}/5): {e}")
            time.sleep(2)
    return None


def check_key(key):
    req = urllib.request.Request(BASE_URL + "/account/key-info", headers={"x-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            info = json.loads(resp.read().decode("utf-8"))
        print(f"Blitz API key OK (remaining credits: {info.get('remaining_credits', '?')}).")
    except Exception:
        print("Could not verify the key up front, will try the search anyway.")


def load_config(path):
    cfg = dict(DEFAULTS)
    if path and os.path.exists(path):
        with open(path) as f:
            cfg.update(json.load(f))
        print(f"Using ICP config: {path}")
    else:
        print("No ICP config found, using defaults. Tip: write your ICP to output/icp.json first.")
    return cfg


def build_payload(cfg, cursor=None):
    company = {
        "employee_range": cfg.get("employee_range") or DEFAULTS["employee_range"],
        "hq": {"country_code": [cfg.get("country_code", "DE")]},
    }
    if cfg.get("industries"):
        company["industry"] = {"include": cfg["industries"]}
    if cfg.get("keywords"):
        company["keywords"] = {"include": cfg["keywords"]}
    if cfg.get("exclude_type"):
        company["type"] = {"exclude": cfg["exclude_type"]}

    people = {"job_title": {"include": cfg.get("job_title_include") or DEFAULTS["job_title_include"]}}
    if cfg.get("job_title_exclude"):
        people["job_title"]["exclude"] = cfg["job_title_exclude"]
    if cfg.get("job_level"):
        people["job_level"] = cfg["job_level"]
    people["location"] = {"country_code": [cfg.get("country_code", "DE")]}

    payload = {"company": company, "people": people, "max_results": 50}
    if cursor:
        payload["cursor"] = cursor
    return payload


def current_company(person):
    exps = person.get("experiences", [])
    for exp in exps:
        if exp.get("job_is_current"):
            return exp
    return exps[0] if exps else {}


def search_people(key, cfg, limit, dry_run):
    people, cursor, page = [], None, 0
    while len(people) < limit:
        page += 1
        print(f"  page {page}...", end=" ", flush=True)
        result = api_post(key, "/search/people", build_payload(cfg, cursor))
        if not result or "results" not in result:
            print("no data")
            break
        batch = result["results"]
        people.extend(batch)
        print(f"got {len(batch)} (total {len(people)} / {result.get('total_results', '?')} match)")
        cursor = result.get("cursor")
        if dry_run or not cursor or not batch:
            break
        time.sleep(RATE_LIMIT_SLEEP)
    return people[:limit]


def enrich_emails(key, people):
    found = 0
    for i, p in enumerate(people, 1):
        url = p.get("linkedin_url")
        if not url:
            continue
        if i == 1 or i % 10 == 0:
            print(f"  enriching email {i}/{len(people)}...", flush=True)
        res = api_post(key, "/enrichment/email", {"person_linkedin_url": url})
        time.sleep(RATE_LIMIT_SLEEP)
        if res and res.get("found"):
            p["_email"] = res.get("email", "")
            found += 1
    print(f"  emails found for {found}/{len(people)} leads")
    return people


def to_rows(people, label):
    rows, seen = [], set()
    for p in people:
        url = p.get("linkedin_url", "")
        if url in seen:
            continue
        seen.add(url)
        comp = current_company(p)
        loc = p.get("location", {})
        rows.append({
            "company": comp.get("company_name", ""),
            "website": "",
            "contact_name": p.get("full_name", ""),
            "role": comp.get("job_title", ""),
            "email": p.get("_email", ""),
            "location": ", ".join(x for x in [loc.get("city", ""), loc.get("country_code", "")] if x),
            "linkedin_url": url,
            "trigger_signal": "",  # fill from research: why this lead, why now
            "source": f"Blitz API people search ({label})",
            "notes": p.get("headline", ""),
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description="Pull a real TAM list for your ICP via the Blitz API.")
    ap.add_argument("--config", help="Path to ICP JSON (default: output/icp.json, else data/icp.example.json)")
    ap.add_argument("--limit", type=int, default=25, help="Max leads to pull (default 25)")
    ap.add_argument("--emails", action="store_true", help="Also enrich verified emails (slower, more API calls)")
    ap.add_argument("--dry-run", action="store_true", help="Fetch only the first page to sanity-check filters")
    args = ap.parse_args()

    cfg_path = args.config
    if not cfg_path:
        out_icp = os.path.join(REPO_ROOT, "output", "icp.json")
        cfg_path = out_icp if os.path.exists(out_icp) else os.path.join(REPO_ROOT, "data", "icp.example.json")

    key = load_api_key()
    check_key(key)
    cfg = load_config(cfg_path)

    print(f"\nSearching: {cfg.get('label')} | country={cfg.get('country_code')} | "
          f"industries={cfg.get('industries') or '(any)'} | titles~{len(cfg.get('job_title_include', []))}")
    people = search_people(key, cfg, args.limit, args.dry_run)
    if not people:
        print("\nNo leads found. Loosen the filters: check the LinkedIn industry name (exact, "
              "case-sensitive, see prompts/sourcing.md), widen employee_range, or drop keywords. "
              "If the API is down, fall back to scripts/scrape_example.py or web search.")
        sys.exit(1)

    if args.emails and not args.dry_run:
        enrich_emails(key, people)

    rows = to_rows(people, cfg.get("label", "ICP"))
    out_dir = os.path.join(REPO_ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "leads.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)

    print(f"\nSaved {len(rows)} real leads to output/leads.csv")
    print("First few:")
    for r in rows[:3]:
        print(f"  - {r['contact_name']} | {r['role']} @ {r['company']} | {r['linkedin_url']}")
    if not args.emails:
        print("\nTip: these are LinkedIn-ready now. Add --emails to also pull verified work emails.")


if __name__ == "__main__":
    main()
