# Website Audit — allanvrealestate.com

Date: 2026-08-08 · Scope: full technical SEO pass, accessibility contrast check, broken-link check, and manual performance/UX review across all 12 indexable pages.

## Priority 1 — Fix these

### 1. Legally-required footer links are nearly invisible (accessibility + compliance)
`template.html:394` — `.footer-trec a{color:rgba(255,255,255,0.22);...}` on the dark footer background computes to a **1.52:1 contrast ratio**, far below WCAG AA's 4.5:1 minimum for normal text. This class styles the **TREC Consumer Protection Notice**, **Information About Brokerage Services**, and **Privacy Policy** links — the two TREC links are a legal requirement per Texas real estate advertising rules, so having them nearly unreadable undermines the point of including them. Recommend raising to at least `rgba(255,255,255,0.6)` (≈4.6:1) or using a dedicated lighter color token.

### 2. `--text-3` fails contrast wherever it's used at normal text size
`--text-3: #9a8e82` on `--bg: #F9F7F4` computes to **2.99:1** (fails both AA normal and, barely, AA large-text too). This token drives `.stat-label`, `.cred-label`, `.community-dir`, and several other small uppercase labels sitewide — all currently below the readability bar for users with low vision. Recommend darkening to roughly `#7a6f63` (~4.5:1) or bumping font size/weight if the token must stay light for design reasons.

### 3. HAR.com's "Information About Brokerage Services" link may dead-end for visitors
`https://www.har.com/mhf/terms/dispBrokerInfo?sitetype=aws&cid=777820` (footer + FAQ) currently returns HAR.com's bot-verification interstitial ("Please verify you are a person to continue") instead of the broker info page when fetched programmatically. This may be bot-detection triggering only on automated fetches, not real visitors — worth clicking through yourself on a normal browser to confirm real users aren't hitting the same wall on a legally-required disclosure link. The TREC PDF link (`content.harstatic.com/pdf/TREC_CPN.pdf`) fetched cleanly, no issue there.

## Priority 2 — Worth doing

### 4. Meta descriptions run well past the SERP truncation point sitewide
Every content page's meta description is 165–222 characters, past Google's ~155–160 character display cutoff — they're all getting cut off mid-sentence in search results. Homepage (`template.html:9`) is worst at 222 chars. Only `blog-houston-new-construction-2026.html` (151 chars) is in range. Trim all of them to ≤155 chars, front-loading the value proposition since the tail gets clipped.

### 5. Homepage `<title>` truncates in search results
`template.html:8` — "Houston New Construction Homes | Allan Vega  -  New Construction Specialist" is 75 characters; Google typically truncates around 60. "New Construction Specialist" (the differentiator) gets cut. Recommend shortening — the phrase is redundant with the first half anyway.

### 6. Schema inconsistency between older and newer content pages
The two newest pages (`houston-new-construction-under-300k.html`, `how-much-is-3-5-percent-down-houston.html`) use `Article` schema with an `Organization` publisher and `dateModified`. The seven older pages (both city guides and blog posts) still use `BlogPosting` with a bare `Person` publisher and no `dateModified` — which makes them ineligible for Google's Article rich-result treatment. Worth standardizing all nine on the newer pattern.

### 7. Hero images: better than before, but still unoptimized
Down to 6 background-image hero slides (was 12 per the April audit) — real progress — but they're still plain `.jpeg` totaling ~814KB, all loaded immediately via inline `background-image` with no lazy-loading or modern format (WebP/AVIF), and no responsive sizing. This is real weight on first paint, especially mobile. Recommend converting to WebP (should cut file size 30–50% at equivalent quality) and lazy-loading everything past the first visible slide.

## Priority 3 — Minor / cosmetic
- Twitter card title drops the "| Allan Vega" suffix on 5 pages (present in `<title>`, missing from `twitter:title`) — cosmetic only.

## What's already solid (verified, no action needed)
- **No broken links, anywhere.** Checked every internal `.html` href and every same-page `#anchor` link across all 12 pages — zero broken targets, zero dead anchors. (The old dead `#deals` footer link from the retired Builder Deals feature is confirmed gone.)
- Viewport meta present on all pages; H1/H2 hierarchy clean and unique per page; all images have descriptive alt text; canonical tags correct and self-referential everywhere; `sitemap.xml`'s 11 URLs match the live page set exactly, no orphans; `privacy-policy.html` correctly `noindex`'d and excluded from the sitemap.
- Homepage JSON-LD (WebSite/RealEstateAgent/Person/FAQPage, TREC license) intact and valid.
- Contact form and sticky CTA bar: every input has a properly associated `<label for="...">`, decorative/icon-only controls all carry `aria-label`, the exit-intent popup and mobile nav toggle are marked up correctly for screen readers. This part of the accessibility story is already in good shape.
- GA4 (Consent Mode v2, default denied) and Meta Pixel both gated behind consent — the April audit's "tracking loads without consent" finding is already resolved.

## Suggested next step
Priority 1 items (footer link contrast, `--text-3` contrast, verifying the HAR link) are small, low-risk CSS/verification fixes — happy to make those now if you give the go-ahead. Priority 2 is more involved (meta description rewrites across 9+ pages, image format conversion) and better scoped as its own pass.
