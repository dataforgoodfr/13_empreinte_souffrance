# syntax=docker.io/docker/dockerfile:1

# Define version variables
ARG NODE_VERSION=22-alpine
#ARG PNPM_VERSION=10.12.1

FROM node:${NODE_VERSION} AS base

# Enable Corepack and prepare pnpm (pin version for reproducibility)
#RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate
#ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy lockfiles and package manager configs
COPY package.json package-lock.json* ./

# Install dependencies using pnpm
RUN npm install --frozen-lockfile

# Rebuild the source code only when needed
FROM base AS builder

# Add non-root user early for correct ownership
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

USER nextjs

WORKDIR /app

# Copy node_modules and app files with correct ownership
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --chown=nextjs:nodejs . .

# Optionally disable Next.js telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner

# Add non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

USER nextjs

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy built assets and public files with correct ownership
COPY --from=builder --chown=nextjs:nodejs /app .

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Start your app (adjust if using standalone output)
CMD ["npm", "start"]
