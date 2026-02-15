# Contributing to AI PowerTools 🤝

Thank you for your interest! AI PowerTools is a massive undertaking (60+ components) and requires strict discipline to maintain quality and composability.

## 🌿 Branching Strategy

We use a modified **Feature-Flow** strategy:

- **`master` / `main`**: Always stable, production-ready.
- **`develop`**: Integration branch for the current milestone.
- **`feature/[component-name]`**: Dedicated branch for implementing a specific PowerTools component (e.g., `feature/memory-manager`).
- **`fix/[issue-number]`**: Short-lived branches for bug fixes.
- **`research/[topic]`**: Branches for exploration and R&D (e.g., `research/mcp-integration`).

## 🔄 Development Handover Rules

Since multiple contributors (human and AI) work on this project, handovers must be explicit:

### 1. The "Work-in-Progress" (WIP) State
- Every session must end with a commit to the feature branch.
- If the task is incomplete, the commit message must start with `WIP: [description]`.
- A temporary "Handover Note" should be added to the project's internal tracking (or a comment on the PR).

### 2. The "Handover Checkpoint"
Before handing over to another contributor:
- [ ] **Tests Pass**: `pytest` must pass.
- [ ] **Linting**: `ruff check .` and `black .` must pass.
- [ ] **Documentation**: The `CHANGELOG.md` must be updated with a `[Unreleased]` section.
- [ ] **Status Update**: Update the status in `RESEARCH_LANDSCAPE.md` for the relevant component.

### 3. AI-to-Human Handover
If an AI agent completes a task:
- It MUST provide a summary of technical decisions made.
- It MUST list any new dependencies added.
- It MUST provide a "What's Next" section for the human reviewer.

## 🐙 Git & GitHub Hygiene

### 1. Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat: [component] ...`
- `fix: [issue] ...`
- `docs: [file] ...`
- `refactor: [module] ...`

### 2. PR Review Standards
- **Composability Check**: Does this component remain useful if other components are removed?
- **Dependency Minimization**: Avoid adding heavy dependencies unless absolutely necessary.
- **Type Safety**: All new code must use Python type hints and pass `mypy`.

### 3. Keeping Sync
- Always `git pull --rebase origin master` before starting work.
- Squash-merge feature branches into `master` to keep a clean history.

## 🏗️ Technical Best Practices

- **Modular Design**: One component = one package in `src/powertools/`.
- **Provider Agnostic**: Use the `Abstraction Layer` (#18) interface for all LLM calls.
- **Async First**: Use `asyncio` for all I/O bound operations (API calls, DB access).
- **Comprehensive Testing**: Target 95% line coverage.

---
*Stay Power-ful!* 🚀
