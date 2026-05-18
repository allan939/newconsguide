import json

# Load data
with open('stats.json') as f:
    stats = json.load(f)

with open('deals.json') as f:
    deals_data = json.load(f)

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
def render_deal(deal):
    badge_type = deal.get('badge', 'featured')
    details_html = '\n'.join(
        f'<li class="deal-detail">{d}</li>'
        for d in deal.get('details', [])
    )
    expires = deal.get('expires', '')
    expires_html = f'<div class="deal-expires">Offer expires &middot; {expires}</div>' if expires else ''
    builder_slug = deal['builder'].lower().replace(' ', '_').replace('.', '')
    return f'''<div class="deal-card reveal">
  <span class="deal-badge {badge_type}">{deal["badge_text"]}</span>
  <div class="deal-builder">{deal["builder"]}</div>
  <div class="deal-community">{deal["community"]}</div>
  <div class="deal-incentive">{deal["incentive"]}</div>
  <ul class="deal-details">{details_html}</ul>
  {expires_html}
  <a href="#contact" class="btn-outline deal-cta" data-track="deal_cta_{builder_slug}">Claim This Deal &#8599;</a>
</div>'''

deals_cards = '\n'.join(render_deal(d) for d in deals_data.get('deals', []))
html = html.replace('{{deals_cards}}', deals_cards)
html = html.replace('{{deals_updated}}', deals_data.get('last_updated', ''))

with open('index.html', 'w') as f:
    f.write(html)

print('index.html built successfully!')
