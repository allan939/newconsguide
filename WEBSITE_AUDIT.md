# Website Audit — newconsguide

Date: 2026-04-06 (UTC)
Audited file: `index.html`

## Executive summary
The site is visually strong and conversion-focused, but there are a few important technical risks to fix:

1. Social previews are likely broken because `og-image.jpg` is referenced but not present in the repo.
2. The sticky CTA form can show a success message even if the lead submission fails (`no-cors` + unconditional success flow).
3. Tracking scripts load immediately without a visible consent or privacy-policy flow.
4. Hero implementation uses 12 full-screen background images plus animation, which is likely expensive on slower devices.

---

## Findings

### 1) Missing Open Graph / Twitter image asset (High)
**What I found**
- Metadata references `og-image.jpg` for both Open Graph and Twitter cards.
- That file is not present in this repository.

**Why this matters**
- Shared links may render without a preview image (or show an unpredictable fallback), reducing CTR.

**Evidence**
- `og:image` points to `/og-image.jpg` in meta tags.
- `twitter:image` points to `/og-image.jpg` in meta tags.

**Recommended fix**
- Add `og-image.jpg` at the repo root, sized for social cards (e.g., 1200×630), and verify that it is publicly reachable.

### 2) Sticky CTA can report success when submission fails (High)
**What I found**
- Sticky CTA submits with `fetch(..., mode: 'no-cors')`.
- The code catches errors but still runs `.finally(...)`, where it always hides the form and shows success.

**Why this matters**
- False positives can hide lead-delivery failures and hurt conversion quality.

**Recommended fix**
- Remove `mode: 'no-cors'` by enabling CORS on the endpoint, then show success only on confirmed HTTP success.
- If CORS cannot be enabled, use a same-origin relay endpoint (e.g., serverless function) and return explicit status.

### 3) Consent/compliance gap around analytics pixels (Medium)
**What I found**
- Meta Pixel and GA4 load immediately on page load.
- I did not find a visible privacy policy / consent banner in the current page code.

**Why this matters**
- Depending on traffic source and jurisdiction, this can create compliance risk and can impact ad platform policy posture.

**Recommended fix**
- Add a consent manager banner and defer non-essential tracking until consent.
- Add accessible Privacy Policy and Cookie Policy links in footer.

### 4) Performance risk from hero media strategy (Medium)
**What I found**
- Hero section cycles through 12 background images with fade transitions and desktop Ken Burns animations.

**Why this matters**
- This can increase LCP and total bytes on first visit, especially mobile/3G users (despite mobile animation reductions).

**Recommended fix**
- Reduce to 3–5 optimized images, precompress to modern formats (WebP/AVIF), and lazy-load non-critical visual assets.
- Consider using `<img>`/`<picture>` for better loading controls instead of CSS backgrounds.

---

## What was checked
- HTML structure + metadata review.
- Form submission behavior review.
- Tracking and third-party script review.
- Repo-level asset existence check for social image target.

## Suggested next steps (priority order)
1. Fix sticky CTA success logic and endpoint CORS behavior.
2. Add and validate `og-image.jpg`.
3. Add consent/privacy UX for tracking.
4. Run Lighthouse and Core Web Vitals tuning pass (focus on LCP/CLS/INP).
