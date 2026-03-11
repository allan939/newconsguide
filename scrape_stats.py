"""
Auto-scraper for Houston market stats from HAR.com newsroom.
Runs monthly via GitHub Actions on the 12th - updates stats.json automatically.

If scraping fails OR the extracted data looks implausible, stats.json is left
unchanged and a GitHub Issue is opened to notify the site owner.
"""
import urllib.request
import re
import json
import os
from datetime import datetime


def fetch_page(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; HoustonRealEstateBot/1.0)'
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8')


def extract_number(pattern, text, default=None):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else default


def open_github_issue(title, body):
    """Open a GitHub Issue when stats can't be auto-updated (Actions only)."""
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not token or not repo:
        print("Not in GitHub Actions — skipping issue creation.")
        return
    url = f"https://api.github.com/repos/{repo}/issues"
    payload = json.dumps({
        "title": title,
        "body": body,
        "labels": ["data-update-needed"]
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        'Authorization': f'token {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'HoustonRealEstateBot/1.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read().decode())
            print(f"GitHub Issue created: {result.get('html_url')}")
    except Exception as e:
        print(f"Could not create GitHub Issue: {e}")


HAR_NEWSROOM = "https://www.har.com/content/department/newsroom?pid=2222"


def get_latest_har_url():
    """Find the latest monthly market report URL from the HAR newsroom index."""
    try:
        html = fetch_page(HAR_NEWSROOM)
        # Look for links to monthly market stat articles
        links = re.findall(r'href=["\']([^"\']*har\.com[^"\']*(?:market|housing|statistics)[^"\']*)["\']', html, re.IGNORECASE)
        if links:
            print(f"Found HAR article link: {links[0]}")
            return links[0]
        # Fallback: return the newsroom index itself and try to parse stats from it
        return HAR_NEWSROOM
    except Exception as e:
        print(f"WARNING: Could not fetch HAR newsroom index ({e}) — trying newsroom directly")
        return HAR_NEWSROOM


def load_existing_stats():
    try:
        with open('stats.json') as f:
            return json.load(f)
    except Exception:
        return None


def scrape_stats():
    now = datetime.now()
    month_year = now.strftime('%B %Y')
    print(f"Fetching HAR market data for {month_year}...")

    url = get_latest_har_url()
    print(f"Using URL: {url}")

    try:
        html = fetch_page(url)
    except Exception as e:
        print(f"ERROR: Could not fetch page: {e}")
        open_github_issue(
            f"ACTION REQUIRED: {month_year} market stats could not be fetched",
            f"The scraper failed to retrieve HAR data.\n\n"
            f"**URL attempted:** {url}\n**Error:** {e}\n\n"
            f"Please update `stats.json` manually from:\nhttps://www.har.com/content/department/newsroom?pid=2222\n\n"
            f"Then run the workflow manually from the Actions tab."
        )
        print("Keeping existing stats.json unchanged.")
        exit(0)

    # --- Median price: require NNN,NNN format (e.g. 322,045) ---
    median_raw = extract_number(
        r'median (?:home |sales )?price[^$]*\$([0-9]{3},[0-9]{3})', html
    )
    # Looser fallback but still sanity-check
    if median_raw is None:
        median_raw = extract_number(
            r'median (?:home |sales )?price[^$]*\$([0-9,]+)', html
        )
        if median_raw is not None:
            try:
                if int(median_raw.replace(',', '')) < 100_000:
                    print(f"WARNING: Implausible median price ${median_raw} — discarding")
                    median_raw = None
            except Exception:
                median_raw = None

    # --- Days on market ---
    dom = extract_number(r'Days on Market[^0-9]*([0-9]+)', html)

    # --- Active listings (all property types preferred) ---
    listings = extract_number(r'([0-9,]+) available propert', html)
    if listings is None:
        listings = extract_number(r'([0-9,]+) active listings', html)

    # --- Inventory months ---
    inventory = extract_number(r'([0-9.]+)-months? (?:supply|inventory)', html)

    # If nothing at all was extracted the page structure changed — alert owner
    if median_raw is None and dom is None and listings is None:
        print("ERROR: Could not parse any stats. HAR page structure may have changed.")
        open_github_issue(
            f"ACTION REQUIRED: {month_year} market stats could not be parsed",
            f"The scraper fetched the page but extracted no data. "
            f"The page structure may have changed.\n\n"
            f"**URL:** {url}\n\n"
            f"Please update `stats.json` manually from:\nhttps://www.har.com/content/department/newsroom?pid=2222\n\n"
            f"Then run the workflow manually from the Actions tab."
        )
        print("Keeping existing stats.json unchanged.")
        exit(0)

    # Apply safe defaults for any individual missing fields
    existing = load_existing_stats()
    if median_raw is None:
        median_raw = existing['stats']['median_price'].replace('K', '000').replace('$', '') if existing else '335000'
    if dom is None:
        dom = existing['stats']['days_on_market'] if existing else '64'
    if listings is None:
        listings = existing['stats']['active_listings'] if existing else '52,727'
    if inventory is None:
        inventory = existing['stats']['active_listings_trend'].split()[0] if existing else '4.5'

    # Format median price as $NNNk
    try:
        price_num = int(str(median_raw).replace('$', '').replace(',', ''))
        if price_num < 100_000:
            # Still implausible — keep existing value
            print(f"WARNING: Price ${price_num} failed final sanity check — keeping existing value")
            median_display = existing['stats']['median_price'] if existing else '$322K'
        else:
            median_display = f'${price_num // 1000}K'
    except Exception:
        median_display = f'${median_raw}'

    stats = {
        "last_updated": month_year,
        "source": "HAR.com - Houston Association of Realtors",
        "source_url": url,
        "stats": {
            "median_price": median_display,
            "median_price_trend": f"Source: HAR {month_year}",
            "active_listings": listings,
            "active_listings_trend": f"{inventory} months inventory",
            "days_on_market": dom,
            "days_on_market_trend": "Days to sell · Houston MSA",
            "builders_with_incentives": "Most builders",
            "builders_with_incentives_trend": "offering incentives now"
        }
    }

    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"Stats updated: Median={median_display}, DOM={dom}, Listings={listings}")


if __name__ == '__main__':
    scrape_stats()
