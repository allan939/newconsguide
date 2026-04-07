# GitHub Pages Automation Setup

Date: 2026-04-06

This repo now includes a GitHub Actions workflow that auto-deploys your static site to GitHub Pages whenever you push to `work` or `main`.

## One-time setup in GitHub UI
1. Open repository **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Save.

## What happens after setup
- Every push to `work` or `main` triggers deployment automatically.
- You no longer need to manually publish/merge just to refresh the live site.

## Recommended workflow
1. Make/update files locally.
2. Commit.
3. Push to `work`.
4. Wait ~1–3 minutes for the Actions run to complete.
5. Refresh https://allanvrealestate.com/

## Notes
- If deployment fails, check **Actions** tab logs in GitHub.
- If you only want deploys from one branch later, edit `.github/workflows/deploy-pages.yml` and remove the other branch.
