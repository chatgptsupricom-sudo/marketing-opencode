FROM node:20-alpine AS builder
WORKDIR /app
COPY api/package*.json ./
RUN npm install
COPY api/ .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 80
CMD ["node", "server.js"]
