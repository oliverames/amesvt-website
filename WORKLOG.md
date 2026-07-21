# Worklog

## 2026-07-21 - Cloudflare Pages and R2 asset delivery

**What changed**: Kept GitHub `main` as the editable source of truth for the amesvt.com utility landing page and moved production deployment to Cloudflare Pages. The build uploads and rewrites website imagery to the dedicated `ames-website-assets` R2 bucket under the `amesvt/` prefix, served through `assets.amesvt.com`. Repository workflows use encrypted, scoped GitHub Actions secrets, with canonical credentials retained in 1Password.

**Live infrastructure**: Commits merged to `main` deploy the static site to Cloudflare Pages. `amesvt.com` is the landing page and utility access point. A hostname-scoped Cloudflare Cache Rule for `assets.amesvt.com` sets browser cache lifetime to 3,600 seconds while respecting the R2 origin lifetime at the edge.

**Verification**:
- The static-site validation and Cloudflare deployment workflows pass.
- The production landing page and representative R2 favicon return HTTP 200.
- The R2 response advertises `Cache-Control: public, max-age=3600, stale-while-revalidate=604800`.
- Re-running the cache-rule configuration reports the rule as already correct.

**Left off at**: The landing page, Git-driven Cloudflare deployment, and dedicated R2 image delivery are live and verified.

**Open questions**: None.
