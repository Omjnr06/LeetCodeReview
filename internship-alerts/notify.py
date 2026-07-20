import os
import ssl
import json
import smtplib
import urllib.request
import urllib.error
import urllib.parse
from email.message import EmailMessage
import config


def _ascii(s):
    return s.encode("ascii", "ignore").decode("ascii").strip()


def _track_action(posting, url):
    endpoint = (os.environ.get("TRACK_ENDPOINT") or "").strip()
    if not endpoint or posting.get("source") == "digest":
        return None
    secret = (os.environ.get("TRACK_SECRET") or "").strip()

    def q(s):
        return urllib.parse.quote((s or "")[:150], safe="")

    track_url = (
        f"{endpoint}?k={q(secret)}&c={q(posting.get('company'))}"
        f"&r={q(posting.get('title'))}&loc={q(posting.get('location'))}"
        f"&u={q(url)}&src={q(posting.get('source'))}"
    )
    if "," in track_url or ";" in track_url:
        return None
    return f"view, Applied, {track_url}"


def ntfy_push(posting, tier):
    if tier == "A":
        priority, label, tags = "5", "TARGET", "dart,rotating_light"
    else:
        priority, label, tags = "2", "NEW", "seedling"
    title = _ascii(f"{label}: {posting['company']}") or label
    body = f"{posting['title']}\n{posting['location']} - {posting.get('season') or 'season n/a'} [{posting['source']}]"
    headers = {"Title": title, "Priority": priority, "Tags": tags}
    url = posting.get("url") or ""
    actions = []
    if url:
        headers["Click"] = url
        if "," not in url:
            actions.append(f"view, Open posting, {url}")
    track = _track_action(posting, url)
    if track:
        actions.append(track)
    if actions:
        headers["Actions"] = "; ".join(actions)
    req = urllib.request.Request(
        f"{config.NTFY_SERVER}/{config.NTFY_TOPIC}",
        data=body.encode("utf-8"), headers=headers, method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=20)
        return True
    except Exception as e:
        print(f"  ntfy failed for {posting['company']}: {e}")
        return False


def _send_via_resend(subject, body_text):
    key = (os.environ.get("RESEND_API_KEY") or "").strip()
    to = (os.environ.get("MAIL_TO") or "").strip()
    if not key or not to:
        return None
    frm = (os.environ.get("RESEND_FROM") or "onboarding@resend.dev").strip()
    print(f"  [resend] key_len={len(key)} starts_ok={key.startswith('re_')} to={to}")
    payload = json.dumps({"from": frm, "to": [to], "subject": subject, "text": body_text}).encode()
    req = urllib.request.Request(
        "https://api.resend.com/emails", data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=20)
        print("  email sent via Resend")
        return True
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        print(f"  resend failed: HTTP {e.code} {detail}")
        return False
    except Exception as e:
        print(f"  resend failed: {e}")
        return False


def _send_via_smtp(subject, body_text):
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    pw = os.environ.get("SMTP_PASS")
    to = os.environ.get("MAIL_TO")
    if not all([host, user, pw, to]):
        print("  email skipped (no Resend key and SMTP secrets incomplete)")
        return False
    port = int(os.environ.get("SMTP_PORT", "465"))
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.set_content(body_text)
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=ctx) as s:
            s.login(user, pw)
            s.send_message(msg)
        print("  email sent via SMTP")
        return True
    except Exception as e:
        print(f"  email failed: {e}")
        return False


def send_email(subject, body_text):
    r = _send_via_resend(subject, body_text)
    if r is not None:
        return r
    return _send_via_smtp(subject, body_text)


def _row(p):
    return f"- {p['company']} — {p['title']} | {p['location']} | {p.get('season') or ''}\n  {p['url']}"


def send_email_digest(a_list, b_list):
    parts = []
    if a_list:
        parts.append("=== TARGET COMPANIES ===\n" + "\n".join(_row(p) for p in a_list))
    if b_list:
        parts.append("=== OTHER RELEVANT ===\n" + "\n".join(_row(p) for p in b_list))
    subject = f"[{len(a_list)} target / {len(b_list)} other] new internship postings"
    return send_email(subject, "\n\n".join(parts) or "No new postings.")