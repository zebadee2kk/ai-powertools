# AI PowerTools 🚀

**The composable toolkit that LangChain should have been.**

AI PowerTools is a comprehensive collection of 64+ modular, production-ready AI engineering components. Whether you need a simple cost tracker, a complex multi-model consensus engine, or a privacy-first memory system, PowerTools provides the building blocks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🌟 Why AI PowerTools?

Every AI engineering team rebuilds the same foundational components. Most existing frameworks are either **too monolithic** (hard to use just one part) or **too enterprise** (requires cloud subscription). 

**AI PowerTools is different:**
- **Truly Modular**: `pip install ai-powertools[router]` installs JUST the router.
- **Local-First**: Defaults to local models (Ollama/llama.cpp) to save costs and protect privacy.
- **Provider Agnostic**: One unified interface for OpenAI, Anthropic, Gemini, Grok, and local models.
- **Composability**: Use our components inside LangChain, CrewAI, or your own custom agent.

---

## 🏗️ The 6-Tier Architecture

| Tier | Name | Goal |
|---|---|---|
| **0** | **Meta-Tools** | Tools to automate the development of your AI projects. |
| **1** | **Foundations** | The core "plumbing": Routing, Costing, Privacy, State. |
| **2** | **Middleware** | Infrastructure layers for resilience and optimization. |
| **3** | **Tools** | Specialized logic like Memory, Validation, and Prompt Engineering. |
| **4** | **Orchestrators** | High-level systems for agents and autonomous workflows. |
| **5** | **Reference Apps** | Real-world applications built entirely with PowerTools. |

---

## 🚀 Quick Start (Mockup)

*Note: AI PowerTools is currently in the **Research & Design phase**. The first components are being prototyped.*

```python
from powertools.router import LLMRouter
from powertools.cost import CostTracker
from powertools.memory import MemoryManager

# 1. Initialize with local-first strategy
router = LLMRouter(local_default="mistral")

# 2. Track everything with one line
with CostTracker(budget=5.00) as tracker:
    # 3. Intelligent routing based on task complexity
    result = await router.route("Summarize this 50-page PDF", complexity=0.8)
    
    # 4. Save to persistent, hierarchical memory
    await MemoryManager().store_episode(
        event="Summary generated",
        category="work.research",
        details=result.content
    )
```

---

## 🛠️ Status & Documentation

We are currently tracking **61 component ideas**.

- 🎯 **[ROADMAP.md](ROADMAP.md)**: High-level vision and 3-month milestones.
- 🔬 **[docs/RESEARCH_LANDSCAPE.md](./docs/RESEARCH_LANDSCAPE.md)**: Deep-dive research, competitive analysis, and 61 component details.
- 🧠 **[docs/MEMORY_ARCHITECTURE.md](./docs/MEMORY_ARCHITECTURE.md)**: Detailed spec for the Memory Manager.
- 🛡️ **[SECURITY.md](SECURITY.md)**: Our privacy-first security protocols.
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)**: Branching strategy and human/AI handover rules.

---

## 🤝 Community

We are building a community of AI engineers who value stability, privacy, and modularity.

- **Found a bug?** Open an [Issue](https://github.com/zebadee2kk/ai-powertools/issues).
- **Want to help?** Check the [CONTRIBUTING.md](CONTRIBUTING.md) guide.
- **Stay Updated:** Follow the [CHANGELOG.md](CHANGELOG.md).

---
*Stay Power-ful!* 🚀
