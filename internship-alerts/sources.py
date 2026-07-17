import re
import json
import urllib.request
import urllib.error
import config


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "intern-alerts/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _fetch_text(src):
    try:
        return _get(src["url"])
    except Exception:
        if src.get("fallback_url"):
            return _get(src["fallback_url"])
        raise


def norm_url(u):
    if not u:
        return ""
    u = u.strip().split("#")[0].split("?")[0]
    u = re.sub(r"^https?://(www\.)?", "", u.lower()).rstrip("/")
    return u


def _posting(company, title, location, url, season, sponsorship, is_open, source):
    return {
        "company": (company or "").strip(),
        "title": (title or "").strip(),
        "location": (location or "").strip(),
        "url": (url or "").strip(),
        "url_key": norm_url(url),
        "season": (season or "").strip(),
        "sponsorship": (sponsorship or "").strip(),
        "is_open": bool(is_open),
        "source": source,
    }


def parse_simplify_json(raw, source):
    data = json.loads(raw)
    out = []
    for e in data:
        if not e.get("is_visible", True):
            continue
        locs = e.get("locations") or []
        out.append(_posting(
            e.get("company_name"), e.get("title"), " / ".join(locs),
            e.get("url"), e.get("season"), e.get("sponsorship"),
            e.get("active", True), source,
        ))
    return out


def parse_zshah_json(raw, source):
    data = json.loads(raw)
    items = data.values() if isinstance(data, dict) else data
    out = []
    for e in items:
        out.append(_posting(
            e.get("company"), e.get("title"), e.get("location"),
            e.get("url"), e.get("season"), e.get("sponsorship"),
            e.get("is_open", True), source,
        ))
    return out


_HREF = re.compile(r'href=["\']([^"\']+)["\']')
_MDLINK = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def _clean_cell(c):
    c = re.sub(r"<[^>]+>", " ", c)
    c = _MDLINK.sub(r"\1", c)
    c = c.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", c).strip()


def _is_homepage(u):
    path = re.sub(r"^https?://(www\.)?[^/]+", "", u).strip("/")
    return path == ""


def _row_urls(cells):
    urls = []
    for c in cells:
        for m in _HREF.finditer(c):
            urls.append(m.group(1))
        for m in _MDLINK.finditer(c):
            if m.group(2).startswith("http"):
                urls.append(m.group(2))
    urls = [u for u in urls if u.startswith("http") and "imgur.com" not in u]
    real = [u for u in urls if not _is_homepage(u)]
    if real:
        return real[-1]
    return urls[-1] if urls else ""


def parse_readme_table(raw, source):
    out = []
    last_company = ""
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        joined = " ".join(cells).lower()
        if set(joined.replace(" ", "")) <= set("-:") or "company" in joined and "role" in joined:
            continue
        company_raw = cells[0]
        company = _clean_cell(company_raw)
        if company in ("↳", "->", "same as above", "") or company_raw.strip() in ("↳",):
            company = last_company
        else:
            last_company = company
        title = _clean_cell(cells[1])
        location = _clean_cell(cells[2])
        url = _row_urls(cells)
        if not url or not company or not title:
            continue
        out.append(_posting(company, title, location, url, "", "", True, source))
    return out


PARSERS = {
    "simplify_json": parse_simplify_json,
    "zshah_json": parse_zshah_json,
    "readme_table": parse_readme_table,
}


def fetch_all():
    postings, errors = [], {}
    for name, src in config.SOURCES.items():
        try:
            raw = _fetch_text(src)
            postings.extend(PARSERS[src["type"]](raw, name))
        except Exception as e:
            errors[name] = str(e)
    return postings, errors