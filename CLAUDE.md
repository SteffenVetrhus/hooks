# CLAUDE.md

This file provides guidance for AI assistants (such as Claude Code) working in this repository.

## Project Overview

**Repository:** `SteffenVetrhus/hooks`

This is a newly initialized repository. Update this section as the project scope is defined.

## Repository Structure

```
hooks/
├── .claude/
│   └── settings.json  # Claude Code hooks and settings
├── CLAUDE.md          # AI assistant guidance (this file)
└── (project files)    # To be added
```

Update this tree as the project grows.

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

### Building

- When a build system is added, document the build commands here

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
