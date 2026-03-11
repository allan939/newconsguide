#!/usr/bin/env python3
"""
scrape_deals.py — Uses Claude + web search to auto-update builder deals in deals.json

Requires: pip install anthropic
Env var:  ANTHROPIC_API_KEY

Run manually:  python3 scrape_deals.py
In CI:         called by update.yml before build.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).parent
DEALS_JSON = REPO_DIR / "deals.json"

BUILDERS = [
    "Lennar Houston Texas new construction",
    "DR Horton Houston Texas new construction",
    "Perry Homes Houston Texas new construction",
    "Meritage Homes Houston Texas new construction",
    "Pulte Homes Houston Texas new construction",
    "David Weekley Homes Houston Texas new construction",
    "Highland Homes Houston Texas new construction",
    "Taylor Morrison Houston Texas new construction",
    "Coventry Homes Houston Texas new construction",
]

SYSTEM_PROMPT = """\
You are a real estate research assistant for a Houston new construction specialist.
Your job: find the CURRENT, ACTIVE builder incentives and promotions for Houston-area
homebuilders as of today, then return them as a structured JSON array.

For each builder look for:
- Price reductions or discounts on specific communities
- Closing cost contributions or credits
- Mortgage rate buydowns or special financing
- Included upgrades (appliances, design packages, options)
- Move-in-ready home specials or quick move-in events
- Limited-time promotions with expiration dates

RETURN FORMAT — a raw JSON array only, no prose before or after:
[
  {
    "badge": "hot" | "new" | "featured",
    "badge_text": "🔥 Hot Deal" | "✦ New Deal" | "⭐ Featured",
    "builder": "<Builder Name>",
    "community": "<Community or Area> · TX",
    "incentive": "<1-2 sentence headline incentive>",
    "details": ["<bullet 1>", "<bullet 2>", "<bullet 3>"],
    "expires": "<Month DD, YYYY> or 'Limited time'"
  }
]

Badge rules:
- "hot"      → large price cuts ($20K+), multiple incentives stacked, or rate buydowns
- "new"      → just-announced promotions (this month)
- "featured" → solid standard deals

Include 3–6 deals total. Skip builders with no findable current incentive.
Do NOT invent deals — only report what you find on official builder sites or credible news.
"""


def load_existing_deals() -> list:
    """Return current deals as fallback if Claude finds nothing."""
    try:
        with open(DEALS_JSON) as f:
            return json.load(f).get("deals", [])
    except Exception:
        return []


def fetch_deals_with_claude() -> list:
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    today = datetime.now().strftime("%B %Y")
    user_prompt = f"""\
Today is {today}. Search for current Houston-area new construction builder incentives.

Search each of these builders for active promotions on their official websites or
recent press releases:

{chr(10).join(f'- {b}' for b in BUILDERS)}

After searching, return ONLY the JSON array — no explanation, no markdown fences.
"""

    print("Querying Claude with web search for builder deals...")

    # Use streaming to avoid timeout on searches that take a while
    deals = []
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[
            {"type": "web_search_20260209", "name": "web_search"},
        ],
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        final = stream.get_final_message()

    # Extract JSON array from the last text block
    for block in reversed(final.content):
        if block.type == "text":
            text = block.text.strip()
            # Strip optional markdown fences
            if text.startswith("```"):
                text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end > start:
                try:
                    deals = json.loads(text[start:end])
                    break
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}")

    return deals


def write_deals_json(deals: list) -> None:
    today = datetime.now().strftime("%B %-d, %Y")
    data = {
        "last_updated": today,
        "deals": deals,
    }
    with open(DEALS_JSON, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Written {len(deals)} deals to {DEALS_JSON}")


def main():
    existing = load_existing_deals()

    deals = fetch_deals_with_claude()

    if not deals:
        print("Claude returned no deals — keeping existing deals.json unchanged.")
        return

    print(f"\nFound {len(deals)} deals:")
    for d in deals:
        print(f"  [{d.get('badge','?')}] {d.get('builder','?')}: {d.get('incentive','')[:70]}...")

    write_deals_json(deals)
    print("\nDone. Run 'python3 build.py' to regenerate index.html.")


if __name__ == "__main__":
    main()
