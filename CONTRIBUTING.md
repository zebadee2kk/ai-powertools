# Contributing to AI PowerTools 🤝

Thank you for your interest in AI PowerTools! This project aims to be the standard toolkit for AI engineering, and we welcome contributions of all kinds.

## 🛠️ Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[your-username]/ai-powertools.git
    cd ai-powertools
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install development dependencies:**
    ```bash
    pip install -e ".[dev]"
    ```

## 📜 Pull Request Guidelines

1.  **Branching:** Create a feature branch for your changes (`feature/your-component-name`).
2.  **Testing:** Ensure all tests pass and your new code has at least 95% test coverage.
3.  **Documentation:** Update relevant documents (README, ROADMAP, ARCHITECTURE) and add docstrings to new functions/classes.
4.  **Style:** Follow PEP 8 guidelines. We use `black` and `ruff` for formatting.

## 🏗️ Adding a New Component

If you want to add a new component from the roadmap (or a new idea):

1.  Identify the appropriate Tier (Foundation, Tool, or Orchestrator).
2.  Follow the directory structure in `src/powertools/`.
3.  Implement the core logic, provider interfaces (if applicable), and unit tests.
4.  Add a usage example in the `examples/` directory.

## 🐞 Reporting Issues

Please use the GitHub Issue templates to report bugs or request new features.

---
*Stay Power-ful!* 🚀
