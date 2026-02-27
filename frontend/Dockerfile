# ---------- React logo-generator frontend ----------
# Stage 1 – build the production bundle
FROM node:22-alpine AS build

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .

# VITE_API_URL is set at build time so the React app knows where to send API
# requests.  When left empty the app uses the current origin which works if
# a reverse proxy routes /api/* to the backend.
ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Stage 2 – serve with nginx
FROM nginx:stable-alpine

# Replace the default nginx config with one that handles SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
