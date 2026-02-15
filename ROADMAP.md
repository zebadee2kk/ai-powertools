# AI PowerTools Roadmap 🗺️

**Vision:** Building the 60+ foundational components that every production AI system needs.

## 📊 Summary of Tiers

AI PowerTools is structured into 6 logical tiers of increasing complexity:

###  Tier 0: Meta-Tools (Foundational)
- **Status:** Planning
- **Goal:** Build tools that help build the project (Scaffolders, Research Agents, Dev Orchestrators).

### Tier 1: Foundations (Core)
- **Status:** Prototype (LLM Router)
- **Goal:** The "must-haves": Router, Cost Tracking, Session Management, Privacy, and Logging.

### Tier 2: Middleware Layers (Infrastructure)
- **Status:** Design Phase
- **Goal:** Abstraction layers: Least-Cost Routing, Consensus Engines, and Resilience patterns.

### Tier 3: Tools (Functionality)
- **Status:** Planning / Designing (Memory Manager)
- **Goal:** Domain-specific tools: Memory, Output Validation, Prompt Building (RISEN/CARE).

### Tier 4: Orchestrators & Systems (Architecture)
- **Status:** Future
- **Goal:** High-level systems: Autonomous Workflow Engines and Agent Frameworks.

### Tier 5: Reference Applications (Dogfooding)
- **Status:** Design Phase
- **Goal:** Real-world examples like **whoamiAI** (Personal AI Mirror).

---

## 📅 Milestone 1: The Core Five (Weeks 1-4)
Implement the absolute essentials for any AI application:
1.  **#1 Project Scaffolder**: Auto-create standardized component skeletons. (The Builder)
2.  **#5 LLM Router**: Stable v1.0 with rule-based and simple complexity routing.
3.  **#6 Token & Cost Tracker**: Real-time tracking across OpenAI/Anthropic/Ollama.
4.  **#9 Structured Logger**: OTel-based logging for all components.
5.  **#11 Privacy Layer**: Basic PII masking and secret detection.

## 📅 Milestone 2: The Intelligence Layer (Weeks 5-8)
1.  **#18 Abstraction Layer**: Unified interface for major providers.
2.  **#25 Memory Manager**: SQLite-backed episodic and semantic memory.
3.  **#27 Output Validator**: Pydantic-based response enforcement.
4.  **#14 Least-Cost Router**: Use cost data to optimize routing decisions.
5.  **#55-64 whoamiAI**: Launch the first reference application prototype.

## 📅 Milestone 3: Scale & Automation (Weeks 9-12)
1.  **#4 MCP Server Framework**: Expose all tools via Model Context Protocol.
2.  **#48 Workflow Engine**: YAML-based DAG execution.
3.  **#51 Autonomous Task Processor**: Issue-to-PR automation.
4.  **#54 Local Model Evolver**: Knowledge distillation for local LLMs.

## 📅 Milestone 4: Content & Distribution (Weeks 13-16)
1.  **#46 Workspace Blogger**: Auto-generate work-in-progress blogs/vlogs.
2.  **#47 Social Media Multi-Poster**: Multi-platform distribution using style profiles.
3.  **#52 AI Gateway**: Drop-in proxy for external app integration.

---

> ⛓️ **Build Strategy:** For the detailed bootstrapping sequence and "Multiplier Tool" analysis, see [docs/BUILD_STRATEGY.md](./docs/BUILD_STRATEGY.md).

> 📄 **Deep Dive:** For a granular list of all 64 components, detailed competitive analysis, and strategic positioning, see [docs/RESEARCH_LANDSCAPE.md](./docs/RESEARCH_LANDSCAPE.md).
