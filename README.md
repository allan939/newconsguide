# Houston New Construction Website

**Live site: [allanvrealestate.com](https://allanvrealestate.com)**

The website for my real estate business. It helps Houston-area buyers compare new-construction builders, incentives and neighborhoods. I designed, built and maintain it myself, and I use it to capture buyer leads.

![Homepage of allanvrealestate.com](docs/screenshot-newconsguide.jpg)

## What it includes

- **20 pages:** a homepage, 11 neighborhood guides (Katy, Cypress, Pearland, Crosby, Baytown and more), buyer guides, a blog and an FAQ.
- **Lead capture:** contact and guide-request forms send submissions to a Google Sheet through Google Apps Script.
- **Search and AI visibility:** a sitemap, robots.txt, an `llms.txt` file, structured page titles and descriptions, and internal links between guides.

## How it works

| Part | What it does |
|---|---|
| `build.py` | Python script that builds the homepage from a template plus the market numbers in `stats.json`, and regenerates the sitemap. |
| GitHub Actions | When I update the monthly market numbers in `stats.json`, a workflow rebuilds the homepage and publishes it automatically. |
| GitHub Pages | Hosts the site on my custom domain. |

## Monthly market stats update

Once a month, after HAR publishes its market report:
1. Open HAR's monthly Houston housing report.
2. On GitHub, open `stats.json`, click the pencil icon, and update the month, median price, active listings, months of inventory and days on market.
3. Click **Commit changes**. The homepage rebuilds and goes live within a few minutes.

## Tools

HTML, CSS, JavaScript, Python, GitHub Actions, GitHub Pages, Google Apps Script. Built with help from AI coding tools (Claude), which I direct, review and test.

## What I learned

- Writing for a real audience: every page answers questions my buyers actually ask.
- Automation should respect the source. I first tried scraping HAR's market stats automatically, but HAR blocks bots, so I switched to a quick manual update that still rebuilds the site automatically.
- Small, frequent changes (400+ commits) beat big rewrites.

---
Allan Vega · REALTOR®, AEA Realty · TREC #777820 · [LinkedIn](https://www.linkedin.com/in/allan-vega-)
