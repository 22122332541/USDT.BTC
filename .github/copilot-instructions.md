# Copilot Instructions for `USDT.BTC`

## Repository reality (read first)
- This repository is currently a minimal bootstrap.
- Discoverable structure today:
  - `README.md` (only content: project title)
  - `.github/` exists but had no files before this document
- There is no application source directory, no dependency manifest, and no test/config files yet.

## Architecture and boundaries
- Current architecture is intentionally undefined: there are no modules/services to infer yet.
- Treat the repo as a seed project where the first implementation establishes conventions.
- Do not invent cross-service assumptions (API/database/queue layers) unless explicitly requested.

## Agent workflow in this repo
- Start every task by re-checking file layout (`README.md`, `.github/`, and any newly added files).
- Prefer incremental, explicit scaffolding over large one-shot generation.
- When adding a new stack (Python/Node/etc.), include only minimal required files for the requested task.
- If a command is needed, derive it from files actually present (e.g., do not assume `npm test` without `package.json`).

## Project-specific conventions (current)
- Source of truth for intent is `README.md`; keep it aligned with any new code you add.
- Keep changes surgical: avoid creating unrelated folders, tools, or CI pipelines.
- If you introduce a directory layout, document it immediately in `README.md` in the same change.

## Integration and dependencies
- No external integrations are configured yet (no SDK configs, env templates, or infra manifests discovered).
- Before adding dependencies, explain why they are needed for the specific task and keep the set minimal.

## Practical examples from this codebase
- Example of current project docs: `README.md` contains only:
  - `# USDT.BTC`
  - `USDT.BTC`
- Example of automation state: `.github/` existed but was empty before adding this file.

## When instructions are ambiguous
- Default to the simplest implementation that satisfies the request.
- Ask for clarification before making irreversible structural choices (framework, database, deployment target).