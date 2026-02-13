FROM node:20-bookworm-slim AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY package.json ./package.json
COPY packages/geometry-engine/pkg/package.json ./packages/geometry-engine/pkg/package.json
RUN npm install

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image, copy all the files and run next
# Security Hardening: Use Google Distroless (No Shell, No Package Manager)
FROM gcr.io/distroless/nodejs20-debian12 AS runner
WORKDIR /app
ENV NODE_ENV production

# Distroless runs as nonroot (uid 65532) by default
COPY --from=builder /app/apps/web/public ./public
COPY --from=builder --chown=nonroot:nonroot /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nonroot:nonroot /app/apps/web/.next/static ./.next/static

USER nonroot
EXPOSE 3000
ENV PORT 3000

CMD ["server.js"]
