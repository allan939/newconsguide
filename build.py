import json, re

# Load data
with open('deals.json') as f:
    deals = json.load(f)
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

# ---- DEALS ----
cards_html = ''
badge_styles = {
    'hot': 'background:#B03A2E;',
    'new': 'background:#5C3820;',
    'featured': 'background:#C1603A;'
}

delay_classes = ['reveal-delay-1', 'reveal-delay-2', 'reveal-delay-3']
for i, d in enumerate(deals['deals']):
    details_html = ''.join(f'<li>{item}</li>' for item in d['details'])
    badge_style = badge_styles.get(d['badge'], 'background:#C1603A;')
    delay_class = delay_classes[i % len(delay_classes)]
    cards_html += f'''
    <div class="deal-card reveal {delay_class}">
      <span class="deal-badge" style="{badge_style}">{d["badge_text"]}</span>
      <div class="deal-builder">{d["builder"]}</div>
      <div class="deal-community">{d["community"]}</div>
      <div class="deal-incentive">&ldquo;{d["incentive"]}&rdquo;</div>
      <ul class="deal-details">{details_html}</ul>
      <div class="deal-expires">Expires: <span>{d["expires"]}</span></div>
      <button class="btn-deal" onclick="document.getElementById(&apos;contact&apos;).scrollIntoView({{behavior:&apos;smooth&apos;}});">Claim This Deal &rarr;</button>
    </div>
    '''

html = html.replace('{{deals_cards}}', cards_html)
html = html.replace('{{deals_updated}}', deals['last_updated'])

with open('index.html', 'w') as f:
    f.write(html)

print('index.html built successfully!')
