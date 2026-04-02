import json
from email.utils import parsedate_to_datetime
import re
import requests

# for p in patches:
#     print(f"{p['patch']:<8} {p['timestamp'].isoformat()}")

def get_patches():
    resp = requests.get(
        "https://raw.communitydragon.org/json/",
        headers={"User-Agent": "Mozilla/5.0 (compatible; patch-tracker/1.0)"}
    )
    resp.raise_for_status()
    data = resp.json()

    PATCH_RE = re.compile(r"^\d+\.\d+$")

    patches = []
    for entry in data:
        name = entry["name"]
        if entry["type"] != "directory" or not PATCH_RE.match(name):
            continue

        major, minor = map(int, name.split("."))
        mtime = parsedate_to_datetime(entry["mtime"])

        patches.append({
            "patch": name,
            "major": major,
            "minor": minor,
            "timestamp": mtime,
        })

    # Sort by version numerically
    patches.sort(key=lambda p: (p["major"], p["minor"]))

    RELIABLE_FROM = (9, 21)

    patches = [p for p in patches if (p["major"], p["minor"]) >= RELIABLE_FROM]

    return {p['patch']: p['timestamp'] for p in patches}