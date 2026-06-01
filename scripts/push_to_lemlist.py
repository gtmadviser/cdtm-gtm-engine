#!/usr/bin/env python3
"""
Push your campaign to lemlist: add the leads from output/leads.csv into a lemlist
campaign, and optionally set up the LinkedIn + email sequence steps.

Usage:
    # 1) create a campaign in lemlist (UI or API), connect LinkedIn + a mailbox, copy its id (cam_...)
    python3 scripts/push_to_lemlist.py --campaign cam_xxx                                  # add leads
    python3 scripts/push_to_lemlist.py --campaign cam_xxx --steps output/sequence.json     # + push steps
    python3 scripts/push_to_lemlist.py --campaign cam_xxx --steps output/sequence.json --replace  # clear old steps first

Needs LEMLIST_API_KEY in .env (lemlist -> Settings -> Integrations -> API).
No pip installs (standard library only). Full API notes: prompts/lemlist.md
"""

import argparse
import base64
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error

API = "https://api.lemlist.com/api"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36"  # lemlist 403s without a browser UA
SLEEP = 0.2  # rate limit is ~20 requests / 2 seconds
REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def load_key():
    env = os.path.join(REPO, ".env")
    if not os.path.exists(env):
        sys.exit("ERROR: no .env. Copy .env.example to .env and add your LEMLIST_API_KEY.")
    for line in open(env):
        line = line.strip()
        if line.startswith("LEMLIST_API_KEY="):
            k = line.split("=", 1)[1].strip().strip('"').strip("'")
            if k:
                return k
    sys.exit("ERROR: LEMLIST_API_KEY is empty in .env (lemlist -> Settings -> Integrations -> API).")


def http(method, path, key, body=None):
    headers = {
        "Authorization": "Basic " + base64.b64encode((":" + key).encode()).decode(),
        "Accept": "application/json",
        "User-Agent": UA,
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw
    try:
        return 200, json.loads(raw)
    except Exception:
        return 200, raw


def split_name(full):
    full = (full or "").strip()
    if not full:
        return "", ""
    parts = full.split()
    return parts[0], (" ".join(parts[1:]) if len(parts) > 1 else "")


def add_leads(key, campaign):
    path = os.path.join(REPO, "output", "leads.csv")
    if not os.path.exists(path):
        sys.exit("ERROR: output/leads.csv not found. Run scripts/source_leads.py first.")
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    print(f"Adding {len(rows)} leads to {campaign}...")
    ok = skip = fail = 0
    for r in rows:
        email = (r.get("email") or "").strip()
        first, last = split_name(r.get("contact_name"))
        body = {
            "firstName": first,
            "lastName": last,
            "companyName": (r.get("company") or "").strip(),
            "companyDomain": (r.get("website") or "").strip(),
            "linkedinUrl": (r.get("linkedin_url") or "").strip(),
            "jobTitle": (r.get("role") or "").strip(),
            "source": "cdtm-gtm-engine",
        }
        body = {k: v for k, v in body.items() if v}
        if email:
            body["email"] = email
        if not email and not body.get("linkedinUrl"):
            skip += 1
            continue
        q = "?deduplicate=true&verifyEmail=true" if email else "?deduplicate=true&findEmail=true&verifyEmail=true&linkedinEnrichment=true"
        code, resp = http("POST", f"/campaigns/{campaign}/leads/{q}", key, body)
        time.sleep(SLEEP)
        if code in (200, 201):
            ok += 1
        elif code == 409:
            skip += 1
        else:
            fail += 1
            print(f"  ! {first} {last}: HTTP {code} {str(resp)[:120]}")
    print(f"Done: {ok} added, {skip} skipped, {fail} failed.")


def push_steps(key, campaign, steps_file, replace):
    if not os.path.exists(steps_file):
        sys.exit(f"ERROR: {steps_file} not found. It should be a JSON array of steps (see prompts/lemlist.md).")
    steps = json.load(open(steps_file))
    if not isinstance(steps, list):
        sys.exit("ERROR: steps file must be a JSON array of {type, delay, message, subject?}.")
    code, seqs = http("GET", f"/campaigns/{campaign}/sequences", key)
    if code != 200 or not isinstance(seqs, dict):
        sys.exit(f"ERROR: could not read sequences (HTTP {code}). Create the campaign in lemlist first.")
    seq_id = None
    for sid, s in seqs.items():
        if isinstance(s, dict) and not s.get("parentId"):
            seq_id = sid
            break
    if not seq_id:
        seq_id = next(iter(seqs))
    print(f"Using sequence {seq_id}")
    if replace:
        for st in seqs.get(seq_id, {}).get("steps", []):
            if st.get("_id"):
                http("DELETE", f"/sequences/{seq_id}/steps/{st['_id']}", key)
                time.sleep(SLEEP)
        print("  cleared existing steps")
    for st in steps:
        payload = {"type": st["type"], "delay": st.get("delay", 0)}
        if st.get("message") is not None:
            payload["message"] = st["message"]
        if st.get("subject"):
            payload["subject"] = st["subject"]
        code, resp = http("POST", f"/sequences/{seq_id}/steps", key, payload)
        time.sleep(SLEEP)
        flag = "ok" if code in (200, 201) else f"HTTP {code}"
        print(f"  + {st['type']} (delay {payload['delay']}): {flag}")
    print("Steps pushed. Review in lemlist before launching.")


def main():
    ap = argparse.ArgumentParser(description="Add leads + optional sequence steps to a lemlist campaign.")
    ap.add_argument("--campaign", required=True, help="lemlist campaign id (cam_...)")
    ap.add_argument("--steps", help="optional JSON file of sequence steps (see prompts/lemlist.md)")
    ap.add_argument("--replace", action="store_true", help="clear existing steps before pushing")
    args = ap.parse_args()

    key = load_key()
    code, _ = http("GET", "/team", key)
    if code != 200:
        sys.exit(f"ERROR: lemlist rejected the key (HTTP {code}). Check LEMLIST_API_KEY in .env.")
    print("lemlist key OK.")

    if args.steps:
        push_steps(key, args.campaign, args.steps, args.replace)
    add_leads(key, args.campaign)


if __name__ == "__main__":
    main()
