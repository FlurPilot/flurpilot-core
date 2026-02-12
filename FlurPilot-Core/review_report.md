# FlurPilot Project Review

## 1. Project Structure & Architecture
- **Monorepo**: Uses TurboRepo with `apps/web` (Next.js) and `apps/worker` (Python).
- **Compliance**: Matches "Tech Stack" requirements (Next.js 16, Python 3.12).
- **Issue**: `packages/database` and `packages/config` are underutilized. Supabase clients are re-initialized in both apps instead of using the shared package.

## 2. Functional Requirements (F-01 to F-03)

### F-01 Hybrid Acquisition Engine
- **Status**: ✅ Implemented in `apps/worker/main.py`.
- **Details**:
    - **OParl**: `OParlClient` implemented.
    - **SessionNet**: `SessionNetClient` implemented (Shadow API).
    - **Logic**: Implements Tier 1 (OParl) -> Tier 1.5 (SessionNet) -> Tier 2 (Google Dorks) fallback.
    - **Keywords**: Solar keywords defined and weighted.
- **Legal Hardening**:
    - `robots.txt` compliance needs verification in `connectors/`.
    - Rate limiting/Circuit breaker logic not explicitly seen in `main.py` (though `sleep` is used).

### F-02 Virtual Parcel Engine (F-02)
- **Status**: ⚠️ Partial / Logic in Frontend?
- **Details**:
    - `apps/web/components/dashboard/ParcelsMap.tsx` fetches from `geo_parcels`.
    - **Issue**: Lastenheft specifies "Bavarian Bypass" (difference calculation). I haven't seen the *calculation* logic (PostGIS pipeline) in the worker or database scripts yet, only the consumption.
    - **Security**: `ParcelsMap.tsx` does NOT implement the "MapLibre" style from the styling guide (uses `cartocdn`).

### F-03 Privacy Pipeline (F-03)
- **Status**: ❌ Missing / Not Found.
- **Details**:
    - No NER (Named Entity Recognition) code found in `apps/worker`.
    - No redaction logic visible in the paper ingestion flow in `main.py`.
    - **Critical**: Lastenheft requires "Privacy by Architecture" and GDPR compliance (Art. 32). Storing raw PDF text without redaction is a violation.

## 3. Design & Accessibility (Section 6)
- **Status**: ⚠️ Needs Improvement.
- **i18n**:
    - **Violation**: `apps/web/components/dashboard/ParcelsMap.tsx` contains hardcoded strings ("Loading Map Data...", "Error fetching parcels:").
    - **Requirement**: Lastenheft requires "i18n-strict".
- **Design System**:
    - Fonts: `layout.tsx` uses `Inter` and `JetBrains Mono`, but `tailwind.config.ts` references `var(--font-switzer)`.
    - Map Style: Uses standard CartoDB, not a custom style matching the "Clean Light" guide.
- **Accessibility**:
    - Needs `axe-core` or Lighthouse auditor integration.

## 4. Security & Legal (Section 2, 3, 5)
- **License**: No automated license scan found in CI/CD (GitHub Actions/GitLab CI not visible).
- **SBOM**: No SBOM generation script found.
- **Secrets**: `apps/worker/.env` contains keys. Ensure this is not committed (found `.gitignore`, seems safe).
- **Database**:
    - `apps/worker/main.py` uses `SUPABASE_SERVICE_ROLE_KEY` (Correct for worker).
    - `apps/web` components use `createClient` (Context: Client-side). Need to ensure RLS policies are in place to prevent leaking data.

## Recommendations
1.  **Implement NER Pipeline**: Add a cleaning step in `apps/worker/main.py` before `upsert`.
2.  **Fix i18n**: Extract strings in `ParcelsMap.tsx` to a dictionary/hook.
3.  **Standardize Design**: Fix font configuration in `apps/web`.
4.  **Strengthen Worker**: Add explicit rate limiting (e.g., `tenacity` library) to `OParlClient`.
