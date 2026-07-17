import datetime
import sources
import classify
import main
import notify
import config

INCLUDE_TIER_B = True
EMAIL_TIER_B = False


def _key(p):
    return (p["company"].lower(), p.get("season") or "", p["location"].lower())


def build():
    uniq = main.dedupe(sources.fetch_all()[0])
    a = sorted([p for p in uniq if p["is_open"] and classify.tier_for(p) == "A"], key=_key)
    b = sorted([p for p in uniq if p["is_open"] and classify.tier_for(p) == "B"], key=_key)
    return a, b


def render_md(a, b):
    day = datetime.date.today().isoformat()
    lines = [f"# Open roles board — {day}", "",
             f"**{len(a)} target-company roles open.** Real-time pings cover new drops; this board is the full standing list so nothing gets lost.", ""]
    if a:
        lines.append("## Target companies")
        for p in a:
            season = p.get("season") or "term n/a"
            lines.append(f"- **{p['company']}** — {p['title']}  \n  {p['location']} · {season} · [{p['source']}]  \n  {p['url']}")
        lines.append("")
    if INCLUDE_TIER_B and b:
        lines.append(f"## Other relevant ({len(b)})")
        for p in b:
            season = p.get("season") or "term n/a"
            lines.append(f"- {p['company']} — {p['title']} — {p['location']} · {season}  \n  {p['url']}")
    return "\n".join(lines) + "\n"


def render_email(a, b):
    lines = [f"{len(a)} target-company roles open right now.", ""]
    for p in a:
        season = p.get("season") or "term n/a"
        lines.append(f"- {p['company']} — {p['title']}")
        lines.append(f"  {p['location']} · {season} · [{p['source']}]")
        lines.append(f"  {p['url']}")
    if EMAIL_TIER_B and b:
        lines.append("")
        lines.append(f"--- {len(b)} other relevant roles ---")
        for p in b:
            lines.append(f"- {p['company']} — {p['title']} — {p['location']}")
            lines.append(f"  {p['url']}")
    elif b:
        lines.append("")
        lines.append(f"(+ {len(b)} other relevant roles — see OPEN_ROLES.md on the bot-state branch)")
    return "\n".join(lines)


def main_run():
    a, b = build()
    md = render_md(a, b)
    with open("OPEN_ROLES.md", "w") as f:
        f.write(md)
    print(f"[digest] {len(a)} target roles, {len(b)} other; wrote OPEN_ROLES.md")
    notify.send_email(f"Daily board: {len(a)} target roles open", render_email(a, b))
    summary = {
        "company": f"{len(a)} target roles open",
        "title": "Daily board updated — see email / OPEN_ROLES.md",
        "location": "", "season": "", "url": "", "source": "digest",
    }
    notify.ntfy_push(summary, "B")


if __name__ == "__main__":
    main_run()