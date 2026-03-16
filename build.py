import json

# Load data
with open('stats.json') as f:
    stats = json.load(f)

# Read template
with open('template.html') as f:
    html = f.read()

# ---- STATS ----
s = stats['stats']
html = html.replace('{{median_price}}', s['median_price'])
html = html.replace('{{median_price_trend}}', s['median_price_trend'])
html = html.replace('{{active_listings}}', s['active_listings'])
html = html.replace('{{active_listings_trend}}', s['active_listings_trend'])
html = html.replace('{{days_on_market}}', s['days_on_market'])
html = html.replace('{{days_on_market_trend}}', s['days_on_market_trend'])
html = html.replace('{{builders_with_incentives}}', s['builders_with_incentives'])
html = html.replace('{{builders_with_incentives_trend}}', s['builders_with_incentives_trend'])
html = html.replace('{{stats_updated}}', stats['last_updated'])

with open('index.html', 'w') as f:
    f.write(html)

print('index.html built successfully!')
