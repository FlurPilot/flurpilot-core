# FlurPilot Core - Production Deployment Guide

This guide describes how to deploy FlurPilot Core (SaaS & Worker) to a production server (Ubuntu 22.04 LTS recommended).

## 1. Prerequisites
- **Docker & Docker Compose** installed (v2+).
- **Git** installed.
- **DNS Records** pointing `flurpilot.de` and `www.flurpilot.de` to your server IP.

## 2. Initial Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourOrg/FlurPilot-Core.git
    cd FlurPilot-Core
    ```

2.  **Environment Configuration:**
    Create a `.env` file (or rename `.env.example` if it exists) and populate secrets.
    
    *Important: Verify `SUPABASE_URL` and keys match your production Supabase project or local DB config.*

    ```ini
    # .env
    NODE_ENV=production
    
    # Database (If using embedded Postgres, use internal container name or volume)
    DB_PASSWORD=YOUR_STRONG_PASSWORD_HERE
    
    # Supabase / External DB
    SUPABASE_URL=http://db:5432 # or real external URL
    SUPABASE_ANON_KEY=ey...
    SUPABASE_SERVICE_ROLE_KEY=ey...
    
    # Worker Config
    REDIS_URL=redis://redis:6379
    ```

3.  **Caddy Configuration:**
    Verify `Caddyfile` for correct domain names and email (implied for Let's Encrypt).

## 3. Running the Application

Use the included `Makefile` for convenience.

1.  **Pull latest images** (if using GHCR artifact registry):
    ```bash
    make pull
    ```

2.  **Start Services:**
    ```bash
    make up
    ```
    This launches:
    - `caddy` (Reverse Proxy & SSL)
    - `web` (Next.js App)
    - `worker` (Python GIS Engine)
    - `db` (PostgreSQL/PostGIS - *if running stateful mode*)
    - `redis` (Queue)

3.  **Verify Status:**
    ```bash
    docker ps
    ```
    Or check logs:
    ```bash
    make logs
    ```

## 4. Local Verification (Preview Mode)

Before deploying, you can test the production Docker build locally.

1.  **Configure `.env`**: Ensure you have valid `SUPABASE_URL` etc.
    > **Warning**: The local `db` container only runs PostgreSQL. It does **not** provide the Supabase API (PostgREST/Auth).
    > If your app uses `@supabase/supabase-js`, you must verify that `SUPABASE_URL` points to a project that supports the API (e.g., Supabase Cloud), or the client will fail to connect.

2.  **Run Preview**:
    ```bash
    make preview
    # OR (Windows/No Make)
    npm run preview
    ```
    This builds the images from your local source and starts the stack on `http://localhost`.

3.  **Stop**:
    ```bash
    make down
    # OR (Windows/No Make)
    npm run docker:down
    ```

## 5. Database Migrations

If running the `db` container for the first time, it starts empty. Use the migrate command to apply SQL files from `packages/database/supabase/migrations/`.

```bash
make migrate
```
*Note: This pipes local `.sql` files into the `psql` command inside the docker container.*

## 6. Maintenance

- **Restarting:** `make restart`
- **Updates:**
    ```bash
    git pull
    make pull
    make up # Recreates containers with new images
    ```
- **Shell Access:**
    - Web: `make shell-web`
    - Worker: `make shell-worker`
    - DB: `make db-shell`

## 7. Troubleshooting

- **Caddy SSL Issues**: Check `make logs SERVICE=caddy`. Ensure ports 80/443 are open (`ufw allow 80/443`).
- **Database Connection**: Ensure `SUPABASE_URL` in `.env` is reachable from the containers (use `db` hostname if internal).
- **Permissions**: Ensure `./caddy_data` and `./caddy_config` (managed by docker volumes) are writable or let docker manage them.
