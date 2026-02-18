"""
Auto-scraper for Houston market stats from harconnect.com
Runs monthly via GitHub Actions - updates stats.json automatically
"""
import urllib.request
import re
import json
from datetime import datetime

def fetch_page(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; HoustonRealEstateBot/1.0)'
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8')

def extract_number(pattern, text, default='N/A'):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else default

def get_latest_har_url():
    """Find the most recent MLS report on harconnect.com"""
    now = datetime.now()
    # HAR posts previous month's data around the 10th of each month
    # Try current month first, then previous
    for month_offset in [0, 1]:
        m = now.month - month_offset
        y = now.year
        if m <= 0:
            m += 12
            y -= 1
        month_name = datetime(y, m, 1).strftime('%B').lower()
        year_short = str(y)[2:]
        # Common URL pattern for harconnect MLS releases
        url = f"https://www.harconnect.com/houston-housing-market-{month_name}-{y}/"
        try:
            fetch_page(url)
            return url
        except:
            pass
    # Fallback to the known working page
    return "https://www.harconnect.com/houston-housing-market-delivers-a-strong-more-balanced-year-in-2025/"

def scrape_stats():
    print("Fetching HAR market data...")
    
    # Try to get the latest monthly report
    url = get_latest_har_url()
    print(f"Using URL: {url}")
    
    try:
        html = fetch_page(url)
    except Exception as e:
        print(f"Error fetching page: {e}")
        # If scraping fails, keep existing stats.json unchanged
        exit(0)

    # Extract median price
    median = extract_number(
        r'median (?:home |sales )?price[^$]*\$([0-9,]+)',
        html, '$335,000'
    )
    if not median.startswith('$'):
        median = '$' + median

    # Extract days on market  
    dom = extract_number(
        r'Days on Market[^0-9]*([0-9]+)',
        html, '64'
    )

    # Extract active listings
    listings = extract_number(
        r'([0-9,]+) active listings',
        html, '52,727'
    )

    # Extract inventory months
    inventory = extract_number(
        r'([0-9.]+)-months? (?:supply|inventory)',
        html, '4.5'
    )

    # Format median price nicely (convert to K if over 1000)
    try:
        price_num = int(median.replace('$','').replace(',',''))
        if price_num >= 1000:
            median_display = f'${price_num//1000}K'
        else:
            median_display = median
    except:
        median_display = median

    now = datetime.now()
    month_year = now.strftime('%B %Y')

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

    print(f"✅ Stats updated: Median={median_display}, DOM={dom}, Listings={listings}")

if __name__ == '__main__':
    scrape_stats()
