# CLAUDE.md — newconsguide

This file provides context for AI assistants working on this repository.

## Project Overview

**newconsguide** is a single-page marketing website for **Allan Vega**, a Houston new construction real estate specialist. The site targets homebuyers looking for new construction homes in the Houston metro area and presents:

- Live Houston market statistics (auto-updated monthly)
- Current builder deals and incentives (manually curated)
- Embedded YLOPO property search widget
- Agent bio, testimonials, and a Google Forms lead capture

The site is statically hosted (likely via GitHub Pages) with a GitHub Actions workflow handling automatic monthly rebuilds.

---

## Repository Structure

```
newconsguide/
├── index.html                          # Built output — do NOT edit manually
├── template.html                       # Source template (used by build.py)
├── build.py                            # Build script: template + JSON → index.html
├── scrape_stats.py                     # Scraper: fetches market stats from HAR
├── deals.json                          # Data: current builder deals (manually curated)
├── stats.json                          # Data: Houston market stats (auto-updated)
├── README.md                           # Minimal project description
├── update (1).yml                      # Workflow draft/backup (not active)
└── .github/
    └── workflows/
        └── update.ymlupdate.yml        # Active GitHub Actions workflow (oddly named)
```

> **Important:** `index.html` is a **generated artifact**. Always edit `template.html`, `deals.json`, or `stats.json` — never edit `index.html` directly, as it will be overwritten on the next build.

> **Note:** The workflow file is named `update.ymlupdate.yml` (appears to be a naming error). This is the active workflow file used by GitHub Actions.

---

## How the Build System Works

### Data Flow

```
scrape_stats.py  →  stats.json  ┐
deals.json                      ├──► build.py ──► index.html
template.html  ─────────────────┘
```

### `build.py`

Reads `template.html`, performs string substitution using `{{placeholder}}` tokens, then writes `index.html`.

**Stats placeholders** (populated from `stats.json`):
| Placeholder | Source field |
|---|---|
| `{{median_price}}` | `stats.median_price` |
| `{{median_price_trend}}` | `stats.median_price_trend` |
| `{{active_listings}}` | `stats.active_listings` |
| `{{active_listings_trend}}` | `stats.active_listings_trend` |
| `{{days_on_market}}` | `stats.days_on_market` |
| `{{days_on_market_trend}}` | `stats.days_on_market_trend` |
| `{{builders_with_incentives}}` | `stats.builders_with_incentives` |
| `{{builders_with_incentives_trend}}` | `stats.builders_with_incentives_trend` |
| `{{stats_updated}}` | top-level `last_updated` |

**Deals placeholders** (populated from `deals.json`):
| Placeholder | Source |
|---|---|
| `{{deals_cards}}` | Rendered HTML cards from `deals` array |
| `{{deals_updated}}` | top-level `last_updated` |

**Deal badge colors** (hardcoded in `build.py`):
- `hot` → `#B03A2E` (dark red)
- `new` → `#5C3820` (dark brown)
- `featured` → `#C1603A` (terra/orange, default)

### `scrape_stats.py`

Fetches market data from **harconnect.com** (Houston Association of Realtors). It tries URLs in the pattern `houston-housing-market-{month}-{year}/` for the current and prior month, falling back to a known working URL.

Extracted fields via regex:
- Median price (pattern: `median (?:home |sales )?price[^$]*\$([0-9,]+)`)
- Days on Market (pattern: `Days on Market[^0-9]*([0-9]+)`)
- Active listings (pattern: `([0-9,]+) active listings`)
- Inventory months (pattern: `([0-9.]+)-months? (?:supply|inventory)`)

Prices ≥ $1,000 are formatted as `$NNNk`. The script exits cleanly (exit 0) without modifying `stats.json` if scraping fails, preserving the last known values.

---

## Data Files

### `deals.json`

Manually curated. Update this file to change the builder deals shown on the site.

```json
{
  "last_updated": "February 18, 2026",
  "deals": [
    {
      "badge": "hot",           // "hot" | "new" | "featured"
      "badge_text": "🔥 Hot Deal",
      "builder": "DR Horton",
      "community": "Bridgeland · Cypress, TX",
      "incentive": "Up to $20,000 in closing cost assistance...",
      "details": [
        "Homes from $299K – $380K",
        "3.99% rate buydown available (limited homes)"
      ],
      "expires": "February 28, 2026"
    }
  ]
}
```

### `stats.json`

Auto-updated by `scrape_stats.py` and the GitHub Actions workflow. Can be edited manually if the scraper produces wrong values.

```json
{
  "last_updated": "February 2026",
  "source": "HAR.com - Houston Association of Realtors",
  "source_url": "https://...",
  "stats": {
    "median_price": "$335K",
    "median_price_trend": "Source: HAR January 2026",
    "active_listings": "52,727",
    "active_listings_trend": "4.5 months inventory",
    "days_on_market": "64",
    "days_on_market_trend": "Days to sell · Houston MSA",
    "builders_with_incentives": "Most builders",
    "builders_with_incentives_trend": "offering incentives now"
  }
}
```

---

## GitHub Actions Workflow

**File:** `.github/workflows/update.ymlupdate.yml`

**Triggers:**
- **Scheduled:** 12th of every month at 9:00 AM CT (14:00 UTC) — runs after HAR posts monthly data (~10th)
- **Push:** When `deals.json` or `stats.json` are modified
- **Manual:** Via GitHub Actions → "Run workflow"

**Steps:**
1. Checkout repo
2. Set up Python 3.11
3. Run `scrape_stats.py` (fetch latest HAR market data → update `stats.json`)
4. Run `build.py` (regenerate `index.html` from template + updated data)
5. Commit and push `index.html` and `stats.json` back to the repo (commit message: `Auto-update: {Month Year} market stats refreshed`)

**To trigger a manual rebuild:** Go to GitHub → Actions → "Update Website" → "Run workflow".

---

## Website Sections

The single-page site (`index.html`) is divided into these sections:

| Section | ID | Description |
|---|---|---|
| Navigation | (fixed) | Logo, nav links, "Get Free Guide" CTA |
| Hero | — | Main headline, subhead, dual CTAs |
| Market Stats | `#stats` | 4-card grid from `stats.json` |
| Builder Deals | `#deals` | Deal cards from `deals.json` |
| Property Search | `#search` | YLOPO widget (embedded) |
| About | `#about` | Agent bio and credentials |
| Testimonials | — | Client quote cards |
| Contact | `#contact` | Google Forms iframe for lead capture |
| Footer | — | Contact info + TREC compliance links |

---

## Design System

### Color Palette (CSS custom properties)

| Variable | Hex | Usage |
|---|---|---|
| `--cream` | `#F5EFE4` | Main background |
| `--cream-dark` | `#EDE3D3` | Alternate section backgrounds |
| `--parchment` | `#FAF6EF` | Cards, form backgrounds |
| `--terra` | `#C1603A` | Primary brand/accent (burnt orange) |
| `--terra-dark` | `#A04E2E` | Hover states |
| `--terra-pale` | `#EDD5C8` | Light accent, dark-bg text |
| `--brown` | `#2E1A0E` | Primary text, dark sections |
| `--brown-mid` | `#5C3820` | Secondary text |
| `--brown-light` | `#8A5C3A` | Muted text |
| `--sand` | `#B8956A` | Tertiary text, labels |
| `--sand-light` | `#D4B48C` | Light sand accents |
| `--white` | `#FDFAF5` | Near-white for buttons on dark |

### Typography

- **Outfit** (Google Fonts, sans-serif) — body text, nav, buttons, labels
- **Fraunces** (Google Fonts, serif/display) — headings, stat numbers, testimonials, deal builder names

### Animation Conventions

- `.reveal` class + IntersectionObserver — fade-up on scroll for most content blocks
- `.reveal-delay-1/2/3/4` — staggered delays (0.1s–0.4s)
- CSS keyframes: `fadeUp`, `fadeIn`, `scrollPulse`

---

## Third-Party Integrations

| Integration | Purpose | Config location |
|---|---|---|
| **YLOPO** | Property search widget | `index.html` `#search` section |
| **Google Forms** | Lead capture iframe | `index.html` `#contact` section |
| **Google Fonts** | Outfit + Fraunces | `<head>` link tag |
| **HAR / harconnect.com** | Market data source | `scrape_stats.py` |

### YLOPO Widget Configuration

The widget uses domain `allan.askozzie.com` and the script is loaded from `search.askozzie.com`:

```html
<script>window.YLOPO_WIDGETS = { domain: 'allan.askozzie.com' };</script>
<script src="https://search.askozzie.com/build/js/widgets-1.0.0.js"></script>
<div class="YLOPO_searchWidget"></div>
<div class="YLOPO_resultsWidget" data-search='{"locations":[...],...}'></div>
```

The results widget is configured to show Houston-area new construction homes (Crosby, Baytown, Katy, New Caney, TX) priced $250K–$500K, year built ≥ 2026. A JavaScript MutationObserver limits visible cards to 3 via DOM manipulation.

### TREC Compliance (Footer)

Texas Real Estate Commission requires these two links in the footer:
- [Consumer Protection Notice](https://content.harstatic.com/pdf/TREC_CPN.pdf)
- [Information About Brokerage Services](https://www.har.com/mhf/terms/dispBrokerInfo?sitetype=aws&cid=777820)

**Do not remove these links.** They are a legal requirement for Texas real estate agents.

---

## Development Workflow

### To update builder deals

1. Edit `deals.json` — add, remove, or modify entries in the `deals` array
2. Update `last_updated` at the top of `deals.json`
3. Push to `master` — GitHub Actions will automatically rebuild `index.html`

### To manually update market stats

1. Edit `stats.json` directly, or
2. Run `python3 scrape_stats.py` locally, then
3. Run `python3 build.py` to preview `index.html` locally

### To rebuild locally

```bash
python3 scrape_stats.py   # optional: fetch fresh HAR data
python3 build.py          # generates index.html from template.html
```

> Requires Python 3 standard library only — no `pip install` needed.

### To add a new page section

1. Add the HTML section to `template.html`
2. Add corresponding CSS inline in the `<style>` block in `template.html`
3. If the section needs dynamic data, add a `{{placeholder}}` and wire it up in `build.py`
4. Run `python3 build.py` to test

---

## Key Conventions

- **Single file output:** All CSS is inline in `<style>`, all JS is inline in `<script>` — there are no external `.css` or `.js` files to maintain.
- **No build tools:** No npm, webpack, or bundlers. Just Python for templating and the browser for rendering.
- **Mobile breakpoint:** `@media(max-width:768px)` — nav links hide, sections reduce padding, about image hides, footer stacks.
- **Scroll animations:** Add `.reveal` to any element that should fade up on scroll; optionally add `.reveal-delay-1` through `.reveal-delay-4` for staggered animation within a group.
- **Button patterns:**
  - `.btn-primary` — filled terra background, used for primary CTAs
  - `.btn-outline` — transparent with brown border, used for secondary CTAs
  - `.btn-nav` — dark brown, used in navigation
  - `.btn-deal` — transparent with brown border, full-width, used inside deal cards
- **Section pattern:** Each section uses `.section-eyebrow` (small caps label) + `.section-title` (serif heading with `<em>` for italic terra accent) + `.section-divider` (thin gradient line).

---

## Known Issues / Watch-outs

- **`template.html` not committed:** `build.py` reads from `template.html`, but this file is not present in the repository as tracked. The current `index.html` is the built output. If you need to make HTML/CSS changes, treat `index.html` as the source and add a `template.html` before running `build.py`.
- **Workflow file naming:** `.github/workflows/update.ymlupdate.yml` has an unusual name (double suffix). This is the active workflow but may cause confusion. Do not rename it without verifying GitHub still picks it up.
- **`update (1).yml`** in the repo root is not active (only files inside `.github/workflows/` are picked up by GitHub Actions). It appears to be a local copy/backup.
- **YLOPO `yearMin: 2026`:** The results widget filters for homes built ≥ 2026. Adjust this in `index.html` (or `template.html` once established) if the search returns too few results.
- **Stats scraper fallback:** If `scrape_stats.py` cannot find a monthly URL, it uses a hardcoded 2025 fallback URL. Verify this URL remains valid or update it annually.
