"""
scrape_example.py — a polite, adaptable starting point for live lead sourcing.

This is a SKELETON. Ask Claude Code to adapt it to your actual source
(a directory page, a category listing, etc.). It deliberately:
  - fetches one page at a time with a delay (be a good citizen)
  - extracts links/text generically so you can shape it to your target
  - writes rows in the repo's leads schema

Run:  python scripts/scrape_example.py "https://some-directory-page"
Then point Claude at the output and let it clean/enrich the rows.

No paid APIs. Standard-library + requests/bs4 if available; Claude can
swap in plain urllib if a team doesn't have the packages.
"""
import csv
import sys
import time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing requests/bs4. Ask Claude to install them or rewrite with urllib.")
    sys.exit(1)

OUT = Path(__file__).resolve().parents[1] / "output" / "leads.csv"
COLUMNS = ["company", "website", "contact_name", "role", "email",
           "location", "trigger_signal", "source", "notes"]
HEADERS = {"User-Agent": "CDTM-MPD-student-project/1.0 (educational)"}


def fetch(url: str) -> str:
    """Fetch one page, politely."""
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    time.sleep(1.5)  # be polite — don't hammer the source
    return resp.text


def extract(html: str, source_url: str) -> list[dict]:
    """
    Generic extraction. ADAPT THIS to your source with Claude:
    most directories list businesses as <a> links or repeated cards.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for a in soup.select("a[href]"):
        text = a.get_text(strip=True)
        href = a["href"]
        if not text or len(text) < 3:
            continue
        rows.append({
            "company": text,
            "website": href if href.startswith("http") else "",
            "contact_name": "",
            "role": "",
            "email": "",
            "location": "",
            "trigger_signal": "",   # fill in why this lead fits
            "source": source_url,
            "notes": "raw extract — clean with Claude",
        })
    return rows


def write(rows: list[dict]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} raw rows to {OUT}")
    print("Now ask Claude: filter to your ICP, dedupe, add trigger_signal, cap at 25-50.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python scripts/scrape_example.py "<directory-url>"')
        sys.exit(1)
    url = sys.argv[1]
    write(extract(fetch(url), url))
