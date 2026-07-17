import os

NTFY_TOPIC = os.environ.get("NTFY_TOPIC") or "Omjnr-06-internship-grind"
NTFY_SERVER = "https://ntfy.sh"

TIER_A_TARGETS = {
    "google", "spotify", "apple", "meta", "microsoft", "databricks", "intuit",
    "disney", "tesla", "tiktok", "visa", "amazon", "waymo",
    "wealthsimple", "shopify", "bloomberg", "ramp", "datadog", "plaid",
    "cockroach labs", "unitedmasters",
}

COMPANY_ALIASES = {
    "google": ["alphabet", "youtube", "deepmind", "google llc"],
    "meta": ["facebook", "instagram", "meta platforms"],
    "amazon": ["aws", "amazon web services", "amazon.com"],
    "microsoft": ["msft"],
    "tiktok": ["bytedance"],
    "disney": ["walt disney", "hulu", "disney streaming"],
    "cockroach labs": ["cockroachdb", "cockroach"],
    "unitedmasters": ["united masters"],
    "waymo": ["waymo llc"],
    "databricks": [],
}

LOCATION_PHRASES = [
    "new york", "nyc", "manhattan", "brooklyn", "jersey city", "hoboken",
    "san francisco", "bay area", "silicon valley", "palo alto", "mountain view",
    "sunnyvale", "san jose", "menlo park", "cupertino", "redwood city",
    "santa clara", "san mateo", "foster city", "oakland", "berkeley",
    "emeryville", "san bruno", "south san francisco", "fremont", "milpitas",
    "toronto", "vancouver", "mississauga", "brampton", "markham", "vaughan",
    "north york", "scarborough", "etobicoke", "gta", "greater toronto",
    "london", "dubai", "united arab emirates", "uae",
    "remote",
]
LOCATION_TOKENS = {"sf", "ny", "on", "bc"}

ROLE_INCLUDE = [
    "intern", "internship", "co-op", "coop", "co op",
    "new grad", "new-grad", "newgrad", "university grad", "campus", "student",
]
ROLE_EXCLUDE = [
    "senior", "staff", "principal", "sr.", "sr ", "manager", "director",
    "phd", "ph.d", "doctoral", "mba", "vice president",
]

RESTRICTED_MARKERS = [
    "clearance", "secret", "ts/sci", "polygraph",
    "u.s. citizen", "us citizen", "citizenship is required",
    "citizenship required", "must be a citizen",
]

SOURCES = {
    "vanshb03": {
        "type": "simplify_json",
        "url": "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/.github/scripts/listings.json",
        "fallback_url": "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/main/.github/scripts/listings.json",
    },
    "zshah101": {
        "type": "zshah_json",
        "url": "https://raw.githubusercontent.com/zshah101/Automated-List-Of-Summer-2027-and-Fall-2026-Tech-Internships/main/data/jobs.json",
        "fallback_url": "https://raw.githubusercontent.com/zshah101/Automated-List-Of-Summer-2027-and-Fall-2026-Tech-Internships/master/data/jobs.json",
    },
    "sndsh404": {
        "type": "readme_table",
        "url": "https://raw.githubusercontent.com/sndsh404/summer-2027-internships/main/README.md",
        "fallback_url": "https://raw.githubusercontent.com/sndsh404/summer-2027-internships/master/README.md",
    },
    "speedyapply": {
        "type": "readme_table",
        "url": "https://raw.githubusercontent.com/speedyapply/2027-SWE-College-Jobs/main/README.md",
        "fallback_url": "https://raw.githubusercontent.com/speedyapply/2027-SWE-College-Jobs/master/README.md",
    },
    "speedyapply_intl": {
        "type": "readme_table",
        "url": "https://raw.githubusercontent.com/speedyapply/2027-SWE-College-Jobs/main/INTERN_INTL.md",
        "fallback_url": "https://raw.githubusercontent.com/speedyapply/2027-SWE-College-Jobs/master/INTERN_INTL.md",
    },
}

STATE_FILE = "seen.json"
LOG_FILE = "log.csv"