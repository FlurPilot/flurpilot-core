# FlurPilot Core - Project Context

## Repository
**GitHub URL:** https://github.com/stochmann75-spec/flurpilot-core
**Status:** Private repository
**Branch:** main

## Project Structure
- **apps/web/** - Next.js 16 Frontend (React 19, TypeScript, Tailwind CSS v4)
- **apps/worker/** - Python AsyncIO Worker for data collection and processing
- **packages/geometry-engine/** - Rust-based geometry engine (WASM/Python bindings)
- **packages/database/** - Supabase client and database schema
- **packages/config/** - Shared configurations

## Key Features
- OParl integration for municipal council information systems
- AI-powered PDF analysis and keyword detection for solar project establishment decisions
- Privacy-compliant processing (Privacy Engine)
- Bavarian Bypass for Bavarian systems
- Job Queue for distributed processing

## Tech Stack
- **Frontend:** Next.js 16, React 19, Tailwind CSS v4, Framer Motion, MapLibre GL
- **Backend:** Python 3.x, AsyncIO, Supabase (PostgreSQL)
- **GIS:** MapLibre GL, Rust Geometry Engine
- **AI:** OpenAI SDK, Zod schema validation
- **Infrastructure:** Docker, Caddy, Vercel-ready

## GitHub Actions Workflows
- `ci.yml` - Tests (Python Worker, Next.js Web, Rust Geometry, Security Scan)
- `build.yml` - Docker builds & push to GitHub Container Registry
- `infracost.yml` - Cost estimation
- `legal-compliance.yml` - Compliance checks

## Recent Activity
- Project successfully pushed to GitHub with cleaned history (large files removed)
- PLAN-stack-optimization.md: All 4 phases COMPLETE
- Repository is private under FlurPilot organization

## Environment Notes
- `.env` files contain sensitive data and are NOT committed
- GitHub Secrets need to be configured for API keys (BRAVE_API_KEY, PHOENIX_API_KEY, etc.)

## Next Steps
- Configure GitHub Secrets in repository settings ✅ COMPLETED
- Review and activate GitHub Actions workflows ✅ COMPLETED
- Continue development based on PLAN-stack-optimization.md roadmap

## GitHub Secrets Status
All secrets configured: BRAVE_API_KEY, PHOENIX_API_KEY, RESEND_API_KEY, INFRACOST_API_KEY, SUPABASE_SERVICE_ROLE_KEY
