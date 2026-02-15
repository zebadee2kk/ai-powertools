# AI PowerTools Architecture 🏗️

AI PowerTools is designed with a **modular, 6-tier architecture** to ensure maximum flexibility, production readiness, and clear separation of concerns.

## 🏗️ The 6-Tier System

```text
TIER 5: REFERENCE APPLICATIONS
├─ whoamiAI (Personal AI Mirror)
└─ [Future templates and demo apps]

TIER 4: ORCHESTRATORS & SYSTEMS
├─ Workflow Engine (YAML-defined DAGs)
├─ Agent Framework (Multi-agent roles)
├─ Air-Gapped AI Brain (Offline-only)
└─ Autonomous Task Processor (Issue → PR)

TIER 3: TOOLS (DOMAIN LOGIC)
├─ Memory Manager (Hierarchical/Multi-type)
├─ Output Validator (Pydantic enforcement)
├─ RISEN/CARE Prompt Builders
└─ Fact Checker & Evaluation Suite

TIER 2: MIDDLEWARE LAYERS (INFRASTRUCTURE)
├─ Least-Cost Router (Cost optimization)
├─ Sanitisation Layer (In/Out cleaning)
├─ Orchestration Layer (Task coordination)
├─ Consensus Engine (Multi-model voting)
└─ Abstraction Layer (Universal AI interface)

TIER 1: FOUNDATIONS (CORE)
├─ LLM Router (Complexity-based switching)
├─ Token & Cost Tracker (Budget management)
├─ Session Manager (State persistence)
├─ Privacy Layer (PII & Secret masking)
└─ Structured Logger (OTel-based)

TIER 0: META-TOOLS (BUILD THE BUILDER)
├─ Project Scaffolder (Repo generation)
├─ Dev Practices Engine (Standard injection)
├─ Auto Researcher (R&D pipelines)
└─ MCP Server Framework (Tool exposure)
```

## 📐 Design Principles

1.  **Independent Components:** Every component should be usable as a standalone library (`pip install ai-powertools[router]`).
2.  **Local-First, Cloud-Optional:** Default to local models (Ollama/llama.cpp) to minimize costs and maximize privacy.
3.  **Provider Agnostic:** All LLM interactions flow through a universal Abstraction Layer.
4.  **95%+ Test Coverage:** High reliability is mission-critical for production-grade AI engineering.
5.  **Security Built-In:** Prompt guard, PII redaction, and secret scanning are first-class citizens.
6.  **Cost Transparency:** Real-time token counting and budget enforcement on every call.

## 📁 Repository Structure

```text
ai-powertools/
├── src/
│   └── powertools/
│       ├── meta/           # Tier 0: Scaffolders, Research
│       ├── core/           # Tier 1: Foundations (Router, Cost, Logging)
│       ├── middleware/     # Tier 2: Infrastructure (Consensus, Abstraction)
│       ├── tools/          # Tier 3: Specialized (Memory, Validation)
│       ├── orchestrators/  # Tier 4: High-level systems (Workflows, Agents)
│       └── utils/          # Shared utilities and shared schemas
├── docs/                   # Specifications and research
├── examples/               # Reference implementations
├── tests/                  # Unit & Integration tests
└── tools/                  # CLI and maintenance scripts
```

---
*Stay Power-ful!* 🚀
