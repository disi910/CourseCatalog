# === STAGE 1: BUILD ===
# Use Node.js to install dependencies and build the React app
# This stage is ~300MB but we throw it away after building
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files first (Docker caches this layer)
# If package.json hasn't changed, Docker skips npm install on rebuild = much faster
COPY package.json package-lock.json ./
RUN npm ci    # ci = clean install, faster & more reliable than npm install

# Now copy source code and build
COPY . .
RUN npm run build
# After this, the built app is in /app/dist/

# === STAGE 2: SERVE ===
# Take ONLY the built static files and serve them with nginx
# Final image is ~10MB instead of ~300MB
FROM nginx:alpine

# Copy built React app into nginx's serving directory
COPY --from=build /app/dist /usr/share/nginx/html

# Custom nginx config for SPA (single-page app) routing
COPY nginx.conf /etc/nginx/conf.d/default.conf
