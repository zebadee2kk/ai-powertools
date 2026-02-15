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
1.  **#5 LLM Router**: Stable v1.0 with rule-based and simple complexity routing.
2.  **#6 Cost Tracker**: Real-time tracking across OpenAI/Anthropic/Ollama.
3.  **#11 Privacy Layer**: Basic PII masking and secret detection.
4.  **#18 Abstraction Layer**: Unified interface for 5 major providers.
5.  **#25 Memory Manager**: SQLite-backed episodic and semantic memory.

## 📅 Milestone 2: The Infrastructure (Weeks 5-8)
Connect the core components into a robust system:
1.  **#14 Least-Cost Router**: Use cost data to optimize routing decisions.
2.  **#17 Consensus Engine**: Implement local multi-model evaluation.
3.  **#27 Output Validator**: Pydantic-based response enforcement.
4.  **#28 RISEN Builder**: Structured prompt framework.
5.  **#52-61 whoamiAI**: Launch the first reference application prototype.

## 📅 Milestone 3: Ecosystem & Scale (Weeks 9-12)
1.  **#4 MCP Server**: Expose all tools via Model Context Protocol.
2.  **#40 Workflow Engine**: YAML-based DAG execution.
3.  **#49 Autonomous Task Processor**: Issue-to-PR automation.

---

> 📄 **Deep Dive:** For a granular list of all 61 components, detailed competitive analysis, and strategic positioning, see [docs/RESEARCH_LANDSCAPE.md](./docs/RESEARCH_LANDSCAPE.md).
