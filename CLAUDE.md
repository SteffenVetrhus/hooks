# CLAUDE.md

This file provides guidance for AI assistants (such as Claude Code) working in this repository.

## Project Overview

**Repository:** `SteffenVetrhus/hooks`

A Python FastAPI service providing CRUD operations for a **members** collection backed by [PocketBase](https://pocketbase.io/), plus an on-the-fly logo generation API. A React frontend lets users interact with the logo service. Both are containerised for deployment on [Coolify](https://coolify.io/).

## Repository Structure

```
hooks/
├── .claude/
│   └── settings.json          # Claude Code hooks and settings
├── app/
│   ├── __init__.py
│   ├── config.py              # Settings loaded from env vars / .env
│   ├── main.py                # FastAPI app entry point
│   ├── pocketbase_client.py   # Async HTTP client for PocketBase
│   ├── routes.py              # Members CRUD endpoint definitions
│   ├── schemas.py             # Pydantic members models
│   ├── organizations_client.py
│   ├── organizations_routes.py
│   ├── organizations_schemas.py
│   ├── logo_generator.py      # SVG logo generation engine
│   ├── logo_routes.py         # Logo generation endpoint
│   └── logo_schemas.py        # Pydantic logo request model
├── frontend/
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Root component
│   │   ├── LogoForm.jsx       # Logo generation form
│   │   ├── LogoPreview.jsx    # Logo display / download
│   │   └── index.css          # Global styles
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf             # Production nginx config
│   ├── Dockerfile             # Multi-stage build (node → nginx)
│   └── .dockerignore
├── Dockerfile                 # Backend image (python:3.12-slim)
├── .dockerignore
├── docker-compose.yml         # Coolify-ready compose stack
├── CLAUDE.md
└── requirements.txt
```

## Development Workflow

### Branch Conventions

- **Main branch:** `main` (or as configured)
- **Feature branches:** use descriptive names (e.g., `feature/add-webhook-handler`)
- Keep commits atomic and focused on a single change

### Commit Messages

- Use imperative mood (e.g., "Add feature" not "Added feature")
- Keep the subject line under 72 characters
- Add a blank line before the body if more detail is needed

### Code Style

- Follow consistent formatting conventions established by the project's linter/formatter configuration
- When a linter or formatter is added, document the commands here

### Testing

- When a test framework is added, document the test commands here
- Run tests before pushing changes

### Running (local)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `/docs`.

For the frontend:

```bash
cd frontend
npm install
npm run dev
```

The React app will be available at `http://localhost:5173`.

### Running (Docker / Coolify)

```bash
docker compose up --build
```

- **Backend API:** `http://localhost:8000`
- **Frontend:** `http://localhost:3000`

For Coolify deployment, point Coolify at this repo and select **Docker Compose** as the build pack. Set these environment variables in Coolify:

| Variable | Default | Description |
|---|---|---|
| `POCKETBASE_URL` | `http://127.0.0.1:8090` | PocketBase instance URL |
| `POCKETBASE_ADMIN_EMAIL` | *(empty)* | Admin email (optional) |
| `POCKETBASE_ADMIN_PASSWORD` | *(empty)* | Admin password (optional) |
| `VITE_API_URL` | `http://localhost:8000` | Public URL of the backend (build-time, used by frontend) |

## Hooks

A `SessionStart` hook is configured in `.claude/settings.json`. It runs at the beginning of every Claude Code session and outputs a reminder that **all Python functions must have extensive comments**, including:

- A detailed docstring explaining purpose, parameters, return values, and side effects
- Inline comments for any non-trivial logic within function bodies

## Key Conventions for AI Assistants

1. **Read before editing** — Always read a file before modifying it
2. **Minimal changes** — Only make changes that are directly requested or clearly necessary
3. **No unnecessary files** — Don't create files unless they are needed to accomplish the task
4. **Security first** — Never commit secrets, credentials, or `.env` files
5. **Preserve existing patterns** — Match the style and conventions already present in the codebase
6. **Test your changes** — Run any available linters and tests before committing
7. **Keep this file updated** — When adding new tooling, scripts, or conventions, update this CLAUDE.md accordingly
