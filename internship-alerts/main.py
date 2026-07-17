import os
import csv
import json
import datetime
import config
import sources
import classify
import notify


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_state():
    if not os.path.exists(config.STATE_FILE):
        return None
    with open(config.STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    with open(config.STATE_FILE, "w") as f:
        json.dump(state, f, indent=0, sort_keys=True)


def append_log(rows):
    exists = os.path.exists(config.LOG_FILE)
    with open(config.LOG_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["ts", "tier", "company", "title", "location", "season", "sponsorship", "source", "url"])
        for p, tier in rows:
            w.writerow([
                _now(),
                tier, p["company"], p["title"], p["location"],
                p.get("season", ""), p.get("sponsorship", ""), p["source"], p["url"],
            ])


def dedupe(postings):
    merged = {}
    for p in postings:
        k = p["url_key"]
        if not k:
            continue
        cur = merged.get(k)
        if cur is None:
            merged[k] = p
        else:
            cur["is_open"] = cur["is_open"] or p["is_open"]
            if len(p["location"]) > len(cur["location"]):
                cur["location"] = p["location"]
            if not cur.get("season") and p.get("season"):
                cur["season"] = p["season"]
    return list(merged.values())


def main():
    now = _now()
    postings, errors = sources.fetch_all()
    if errors:
        for k, v in errors.items():
            print(f"[warn] source {k} failed: {v}")
    if not postings:
        print("[abort] no postings fetched from any source; leaving state untouched")
        return
    postings = dedupe(postings)
    print(f"[info] {len(postings)} unique postings after dedupe")

    state = load_state()
    seeding = state is None
    if seeding:
        state = {}
        print("[seed] first run: recording current postings WITHOUT notifying")

    a_new, b_new, log_rows = [], [], []

    for p in postings:
        key = p["url_key"]
        if not key:
            continue
        tier = classify.tier_for(p)
        prev = state.get(key)
        reopened = bool(prev) and (not prev.get("is_open", True)) and p["is_open"]
        is_new = prev is None or reopened

        state[key] = {
            "is_open": p["is_open"],
            "tier": tier,
            "company": p["company"],
            "title": p["title"],
            "first_seen": (prev or {}).get("first_seen", now),
            "last_seen": now,
        }

        if is_new and not seeding:
            log_rows.append((p, tier))
            if tier == "A":
                a_new.append(p)
            elif tier == "B":
                b_new.append(p)

    save_state(state)

    if seeding:
        print(f"[seed] recorded {len(state)} postings. Alerts start on next run.")
        return

    if not (a_new or b_new or log_rows):
        print("[info] no new postings this run")
        return

    print(f"[info] new: {len(a_new)} target(A), {len(b_new)} relevant(B), {len(log_rows)} total logged")
    for p in a_new:
        notify.ntfy_push(p, "A")
    for p in b_new:
        notify.ntfy_push(p, "B")
    if a_new or b_new:
        notify.send_email_digest(a_new, b_new)
    if log_rows:
        append_log(log_rows)


if __name__ == "__main__":
    main()