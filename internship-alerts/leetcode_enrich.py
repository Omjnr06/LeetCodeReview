import os
import time
import json
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "leetcode_companies.json")) as f:
    INDEX = json.load(f)

NOTION_TOKEN = (os.environ.get("NOTION_TOKEN") or "").strip()
LEETCODE_DB_ID = (os.environ.get("LEETCODE_DB_ID") or "").strip()
TOP_N = 4

API = "https://api.notion.com"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def _req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        print(f"  [notion {e.code}] {method} {path} -> {detail}")
        raise

def slug_from_url(url):
    u = (url or "").strip().rstrip("/").split("?")[0]
    if "/problems/" in u:
        return u.split("/problems/")[-1].split("/")[0].lower()
    return u.split("/")[-1].lower()


def get_url_value(props):
    p = props.get("Problem URL") or {}
    t = p.get("type")
    if t == "url":
        return p.get("url") or ""
    if t == "rich_text":
        return "".join(x.get("plain_text", "") for x in p.get("rich_text", []))
    if t == "title":
        return "".join(x.get("plain_text", "") for x in p.get("title", []))
    return ""


def companies_empty(props):
    p = props.get("Companies") or {}
    return not (p.get("multi_select") or [])


def fetch_candidate_rows():
    rows, cursor = [], None
    while True:
        body = {
            "filter": {"property": "Companies", "multi_select": {"is_empty": True}},
            "page_size": 100,
        }
        if cursor:
            body["start_cursor"] = cursor
        data = _req("POST", f"/v1/databases/{LEETCODE_DB_ID}/query", body)
        rows.extend(data.get("results", []))
        if data.get("has_more"):
            cursor = data.get("next_cursor")
        else:
            break
    return rows


def enrich():
    if not NOTION_TOKEN or not LEETCODE_DB_ID:
        print("[abort] NOTION_TOKEN or LEETCODE_DB_ID not set")
        return
    rows = fetch_candidate_rows()
    print(f"[info] {len(rows)} rows with empty Companies")
    filled, skipped_nomatch, skipped_nourl = 0, 0, 0

    for page in rows:
        props = page.get("properties", {})
        if not companies_empty(props):
            continue
        url = get_url_value(props)
        if not url:
            skipped_nourl += 1
            continue
        slug = slug_from_url(url)
        companies = INDEX.get(slug, [])[:TOP_N]
        if not companies:
            skipped_nomatch += 1
            continue
        body = {"properties": {"Companies": {"multi_select": [{"name": c} for c in companies]}}}
        try:
            _req("PATCH", f"/v1/pages/{page['id']}", body)
            filled += 1
            print(f"  filled {slug} -> {', '.join(companies)}")
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")
            except Exception:
                pass
            print(f"  write failed for {slug}: HTTP {e.code} {detail}")

    print(f"[done] filled {filled}, no-match {skipped_nomatch}, no-url {skipped_nourl}")


if __name__ == "__main__":
    enrich()