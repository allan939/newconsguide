import json
from datetime import datetime
from pathlib import Path


SITE_URL = 'https://allanvrealestate.com'
SITEMAP_PAGES = [
    {'source': 'index.html', 'loc': '', 'changefreq': 'weekly', 'priority': '1.0'},
    {'source': 'blog.html', 'loc': 'blog.html', 'changefreq': 'weekly', 'priority': '0.9'},
    {'source': 'katy-new-construction-homes.html', 'loc': 'katy-new-construction-homes.html', 'changefreq': 'monthly', 'priority': '0.9'},
    {'source': 'cypress-new-construction-homes.html', 'loc': 'cypress-new-construction-homes.html', 'changefreq': 'monthly', 'priority': '0.9'},
    {'source': 'fulshear-new-construction-homes.html', 'loc': 'fulshear-new-construction-homes.html', 'changefreq': 'monthly', 'priority': '0.9'},
    {'source': 'pearland-new-construction-homes.html', 'loc': 'pearland-new-construction-homes.html', 'changefreq': 'monthly', 'priority': '0.9'},
    {'source': 'blog-houston-new-construction-2026.html', 'loc': 'blog-houston-new-construction-2026.html', 'changefreq': 'monthly', 'priority': '0.8'},
    {'source': 'blog-katy-vs-cypress-new-construction.html', 'loc': 'blog-katy-vs-cypress-new-construction.html', 'changefreq': 'monthly', 'priority': '0.8'},
    {'source': 'blog-builder-incentives-houston.html', 'loc': 'blog-builder-incentives-houston.html', 'changefreq': 'monthly', 'priority': '0.8'},
    {'source': 'houston-new-construction-under-300k.html', 'loc': 'houston-new-construction-under-300k.html', 'changefreq': 'monthly', 'priority': '0.9'},
    {'source': 'how-much-is-3-5-percent-down-houston.html', 'loc': 'how-much-is-3-5-percent-down-houston.html', 'changefreq': 'monthly', 'priority': '0.9'},
]


def load_json(path):
    with open(path) as f:
        return json.load(f)


def build_index():
    stats = load_json('stats.json')

    with open('template.html') as f:
        html = f.read()

    stats_payload = stats['stats']
    html = html.replace('{{median_price}}', stats_payload['median_price'])
    html = html.replace('{{median_price_trend}}', stats_payload['median_price_trend'])
    html = html.replace('{{active_listings}}', stats_payload['active_listings'])
    html = html.replace('{{active_listings_trend}}', stats_payload['active_listings_trend'])
    html = html.replace('{{days_on_market}}', stats_payload['days_on_market'])
    html = html.replace('{{days_on_market_trend}}', stats_payload['days_on_market_trend'])
    html = html.replace('{{builders_with_incentives}}', stats_payload['builders_with_incentives'])
    html = html.replace('{{builders_with_incentives_trend}}', stats_payload['builders_with_incentives_trend'])
    html = html.replace('{{stats_updated}}', stats['last_updated'])

    with open('index.html', 'w') as f:
        f.write(html)


def build_sitemap():
    entries = []
    for page in SITEMAP_PAGES:
        source_path = Path(page['source'])
        if not source_path.exists():
            continue

        lastmod = datetime.fromtimestamp(source_path.stat().st_mtime).date().isoformat()
        loc = f'{SITE_URL}/' if not page['loc'] else f'{SITE_URL}/{page["loc"]}'
        entries.append(
            '  <url>\n'
            f'    <loc>{loc}</loc>\n'
            f'    <lastmod>{lastmod}</lastmod>\n'
            f'    <changefreq>{page["changefreq"]}</changefreq>\n'
            f'    <priority>{page["priority"]}</priority>\n'
            '  </url>'
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(entries)
        + '\n</urlset>\n'
    )

    with open('sitemap.xml', 'w') as f:
        f.write(sitemap)


build_index()
build_sitemap()

print('index.html and sitemap.xml built successfully!')
