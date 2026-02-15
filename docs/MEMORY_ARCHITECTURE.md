# AI PowerTools: Memory Architecture Specification

**Date:** February 15, 2026  
**Component:** #25 — Memory Manager  
**Status:** Design Phase  
**Source:** Real-world taxonomy derived from extensive AI conversation history  

---

## 📊 OVERVIEW

The Memory Manager is one of the most ambitious components in AI PowerTools. Most AI frameworks treat memory as a single conversation buffer. Real intelligence requires **multiple, specialised memory types** organised in a **hierarchical taxonomy** with cross-cutting tags.

This document defines:
1. The **domain taxonomy** (what categories of knowledge exist)
2. The **memory types** (how knowledge is stored and retrieved)
3. The **storage architecture** (how it's implemented)
4. The **retrieval system** (how knowledge is accessed)

---

## 🏗️ DOMAIN TAXONOMY

### 1️⃣ LIFE
Personal growth, identity, health, relationships, and long-term direction.

#### 1.1 Personal Identity & Vision
- Core values & beliefs
- Personal mission & life goals
- Motivations & drivers
- Personal strengths & weaknesses
- Legacy & long-term vision

#### 1.2 Health & Wellbeing
- Physical health metrics
- Mental health & stress patterns
- Sleep & energy tracking
- Fitness routines
- Diet & nutrition insights

#### 1.3 Relationships & Social
- Family notes & important dates
- Friends & contacts context
- Professional network insights
- Social commitments & follow-ups
- Communication preferences

#### 1.4 Personal Development
- Skills being learned
- Books & learning insights
- Courses & certifications
- Habit tracking
- Behavioural improvements

#### 1.5 Lifestyle & Interests
- Hobbies & projects
- Travel history & plans
- Entertainment preferences
- Experiences & memories

---

### 2️⃣ WORK
Everything related to income, professional output, and business creation.

#### 2.1 Career & Professional Direction
- Career strategy
- CV & experience highlights
- Skills & certifications
- Market positioning

#### 2.2 Business & Income Streams
- Business ideas & validation
- Revenue models
- Market research & demand signals
- Go-to-market strategies
- Automation opportunities

#### 2.3 AI & Engineering Projects
- Project architectures & designs
- Agents & automation workflows
- Local LLM infrastructure
- Tooling & integrations
- System architectures

#### 2.4 Research & Knowledge Base
- Security & red-team research
- AI trends & tools
- Industry insights
- Technical deep dives
- Competitive analysis

#### 2.5 Operations & Productivity
- Task workflows
- Process improvements
- Productivity systems
- Decision frameworks
- Documentation & SOPs

---

### 3️⃣ HOME
Physical environment, infrastructure, and personal logistics.

#### 3.1 Home Infrastructure
- Network topology
- Servers & local AI hardware
- Storage & backups
- Security & monitoring
- Smart home devices

#### 3.2 Finance & Household Management
- Budgeting & expenses
- Subscriptions & recurring costs
- Cost optimisation ideas
- Asset tracking

#### 3.3 Property & Maintenance
- Repairs & maintenance logs
- Appliance details & warranties
- Improvement projects
- Energy usage & efficiency

#### 3.4 Digital Home & Data Management
- Local data repositories
- Backup routines
- Personal cloud architecture
- Privacy & encryption

---

### 4️⃣ SYSTEM (Meta Layer)
Rules and configuration governing the AI ecosystem itself.

#### 4.1 AI Memory & Context Rules
- What to remember vs. forget
- Context window priorities
- Memory decay policies
- Cross-domain linking rules

#### 4.2 Automation Policies & Permissions
- What the AI can do autonomously
- Approval workflows
- Escalation thresholds
- Safety guardrails

#### 4.3 Agent Roles & Behaviours
- Agent personality definitions
- Role-specific instructions
- Communication styles
- Tool permissions per agent

#### 4.4 Security & Access Controls
- Data classification levels
- Provider trust levels
- PII handling rules
- Audit requirements

#### 4.5 Data Classification & Privacy
- What data can leave the local network
- Provider-specific data policies
- Retention periods
- Deletion protocols

---

### 5️⃣ IDEAS & INCUBATION
Capture and mature high-value ideas without losing them.

#### 5.1 Raw Ideas Inbox
- Unprocessed ideas as captured
- Source context (what triggered the idea)
- Initial gut rating

#### 5.2 Validated Concepts
- Ideas that passed initial evaluation
- Market/feasibility assessment
- Resource requirements

#### 5.3 Experiments & Prototypes
- Active experiments
- Prototype results
- Iteration history

#### 5.4 Future Opportunities
- Time-dependent opportunities
- Market timing notes
- Dependencies on external factors

#### 5.5 Archived / Parked Ideas
- Ideas shelved for later
- Reason for parking
- Trigger conditions for revisiting

---

## 🏷️ CROSS-CUTTING TAG SYSTEM

Instead of duplicating entries across categories, use tags for cross-category retrieval:

### Priority & Status Tags
| Tag | Purpose |
|-----|---------|
| `urgent` | Requires immediate attention |
| `high-impact` | Significant potential value |
| `long-term` | Strategic, not immediate |
| `blocked` | Waiting on external dependency |
| `completed` | Done, kept for reference |

### Type Tags
| Tag | Purpose |
|-----|---------|
| `monetisable` | Has revenue potential |
| `research-needed` | Requires further investigation |
| `automation-candidate` | Could be automated |
| `security-sensitive` | Handle with extra care |
| `decision-pending` | Needs a decision made |

### Source Tags
| Tag | Purpose |
|-----|---------|
| `from-chatgpt` | Originated in ChatGPT conversation |
| `from-claude` | Originated in Claude conversation |
| `from-gemini` | Originated in Gemini conversation |
| `from-manual` | Manually entered |
| `from-ingestion` | Auto-ingested from external source |

---

## 🧠 MEMORY TYPES (Storage Mechanisms)

The taxonomy above describes **what** is stored. The memory types below describe **how** it's stored and retrieved. Each entry in the taxonomy can be stored using one or more memory types.

### Type 1: Conversation Buffer (Short-Term)
- **Scope:** Current active conversation
- **Lifetime:** Session-only (ephemeral)
- **Storage:** In-memory / Redis
- **Retrieval:** Sequential, most recent first
- **Use case:** Active chat context, working scratchpad

### Type 2: Episodic Memory (Event-Based)
- **Scope:** Timestamped events and interactions
- **Lifetime:** Persistent, indefinite
- **Storage:** SQLite + Vector DB (for similarity search)
- **Retrieval:** By time range, by similarity, by category
- **Use case:** "What happened last time we deployed to staging?"
- **Schema:**
  ```json
  {
    "id": "uuid",
    "timestamp": "2026-02-15T22:30:00Z",
    "event_type": "conversation | decision | action | observation",
    "category": "work.ai_projects.architectures",
    "summary": "Designed the LLM Router with fallback logic",
    "details": "...",
    "embedding": [0.123, 0.456, ...],
    "tags": ["high-impact", "from-claude"],
    "source_ref": "conversation_id_xyz"
  }
  ```

### Type 3: Semantic Memory (Fact-Based)
- **Scope:** Stable facts, entities, and relationships
- **Lifetime:** Persistent, updatable
- **Storage:** Knowledge graph / Vector DB
- **Retrieval:** By entity, by relationship, by similarity
- **Use case:** "What tech stack does Project X use?"
- **Schema:**
  ```json
  {
    "id": "uuid",
    "entity": "Project Lodestar",
    "category": "work.ai_projects",
    "facts": [
      {"key": "tech_stack", "value": "Python, FastAPI, Ollama", "confidence": 0.95},
      {"key": "status", "value": "v2.1-alpha", "confidence": 1.0}
    ],
    "relationships": [
      {"type": "evolved_into", "target": "AI PowerTools"},
      {"type": "uses", "target": "Ollama"}
    ],
    "last_updated": "2026-02-15T22:30:00Z",
    "tags": ["high-impact"]
  }
  ```

### Type 4: Procedural Memory (How-To)
- **Scope:** Learned procedures, workflows, patterns
- **Lifetime:** Persistent, improvable
- **Storage:** YAML/JSON + success metrics
- **Retrieval:** By task type, by success rate
- **Use case:** "How do we usually handle a hotfix?"
- **Schema:**
  ```yaml
  id: uuid
  procedure: "Deploy hotfix to production"
  category: "work.operations.workflows"
  steps:
    - "Create hotfix branch from main"
    - "Apply fix and add tests"
    - "Run CI pipeline"
    - "Deploy to staging, verify"
    - "Merge to main, deploy to prod"
  success_count: 12
  failure_count: 1
  last_used: "2026-02-10"
  notes: "Skip staging only for P0 incidents"
  tags: ["automation-candidate"]
  ```

### Type 5: Working Memory (Scratchpad)
- **Scope:** Multi-step reasoning and task decomposition
- **Lifetime:** Task-scoped (garbage collected after task completion)
- **Storage:** In-memory, ephemeral
- **Retrieval:** By current task ID
- **Use case:** Complex reasoning chains, intermediate results

### Type 6: Long-Term Summary Memory
- **Scope:** Compressed summaries of old conversations and events
- **Lifetime:** Persistent
- **Storage:** SQLite + periodic LLM summarisation
- **Retrieval:** By time period, by topic similarity
- **Use case:** Providing historical context without flooding the context window
- **Process:**
  1. After N conversations (or T time), trigger summarisation
  2. LLM condenses detailed episodic memories into a paragraph
  3. Original episodes are archived (not deleted)
  4. Summary is used for context in future conversations

---

## 🔌 STORAGE ARCHITECTURE

### Backend Options

| Backend | Best For | Tradeoffs |
|---------|----------|-----------|
| **SQLite** | Single-user, portable, air-gapped | Limited concurrency, no distributed |
| **Redis** | Short-term, high-speed, session data | Volatile, requires infrastructure |
| **ChromaDB** | Vector search, embeddings, semantic | Young project, Python-only |
| **Qdrant** | Production vector search, filtering | More setup, but more robust |
| **FAISS** | Fast local vector search | Facebook lib, no metadata storage |
| **PostgreSQL + pgvector** | Full SQL + vector search | Heavy, but production-grade |
| **Neo4j** | Knowledge graphs, relationships | Heavy, but ideal for semantic memory |

### Recommended Default Stack

```
Tier 1 (Minimum viable):
├── SQLite (episodic, procedural, summaries, metadata)
├── ChromaDB (embeddings, vector search)
└── In-memory dict (conversation buffer, working memory)

Tier 2 (Production):
├── PostgreSQL + pgvector (all persistent memory)
├── Redis (buffers, caches, session state)
└── Neo4j (semantic memory, knowledge graph)

Tier 3 (Air-gapped):
├── SQLite (everything)
├── FAISS (local vector search)
└── In-memory (buffers)
```

---

## 🔍 RETRIEVAL SYSTEM

### Query Types

| Query Type | Example | Memory Types Searched |
|-----------|---------|----------------------|
| **Temporal** | "What did I work on last week?" | Episodic, Summary |
| **Semantic** | "What do I know about Kubernetes?" | Semantic, Episodic |
| **Procedural** | "How do I deploy to staging?" | Procedural |
| **Entity** | "Tell me about Project X" | Semantic (entity lookup) |
| **Similarity** | "Something similar to this code pattern" | Episodic, Semantic (embedding search) |
| **Tag-based** | "Show all monetisable ideas" | Any (tag filter) |
| **Category** | "Everything under work.ai_projects" | Any (category filter) |

### Retrieval Pipeline

```
User Query
    │
    ├── 1. Intent Classification (what type of query?)
    │       → temporal, semantic, procedural, entity, similarity
    │
    ├── 2. Category Inference (which domains to search?)
    │       → Use query embedding to identify relevant categories
    │
    ├── 3. Multi-Memory Search (search appropriate memory types)
    │       → Parallel search across episodic, semantic, procedural
    │
    ├── 4. Result Ranking (score and deduplicate)
    │       → Relevance score, recency boost, tag boost
    │
    ├── 5. Context Assembly (pack into context window)
    │       → Most relevant memories first, respect token budget
    │
    └── 6. Response Generation (LLM uses assembled context)
```

---

## 🔧 IMPLEMENTATION API

```python
from powertools.tools.memory import (
    MemoryManager,
    EpisodicMemory,
    SemanticMemory,
    ProceduralMemory,
    WorkingMemory,
    SummaryMemory,
    ConversationBuffer
)

# Initialise with taxonomy
memory = MemoryManager(taxonomy="powertools_default")

# Register memory types with backends
memory.register(ConversationBuffer())
memory.register(EpisodicMemory(backend="sqlite", path="./memory.db"))
memory.register(SemanticMemory(backend="chromadb", collection="facts"))
memory.register(ProceduralMemory(backend="yaml", path="./procedures/"))
memory.register(WorkingMemory())
memory.register(SummaryMemory(
    backend="sqlite",
    summariser_model="ollama:mistral",
    trigger_after_conversations=10
))

# Store events
await memory.store_episode(
    event="Completed LLM Router implementation",
    category="work.ai_projects.architectures",
    tags=["high-impact", "completed"],
    details="Implemented complexity-based routing with Ollama and OpenAI providers"
)

# Store facts
await memory.store_fact(
    entity="AI PowerTools",
    category="work.ai_projects",
    facts={"tech_stack": "Python, asyncio, Pydantic", "status": "Phase 1"},
    relationships=[("part_of", "AI OS ecosystem")]
)

# Store procedures
await memory.store_procedure(
    name="Deploy AI PowerTools update",
    category="work.operations.workflows",
    steps=["Run tests", "Update version", "git commit", "git push", "Verify CI"],
    tags=["automation-candidate"]
)

# Retrieve
results = await memory.recall(
    query="What architecture decisions have we made?",
    memory_types=["episodic", "semantic"],
    categories=["work.ai_projects"],
    limit=10
)

# Smart retrieval with context assembly
context = await memory.assemble_context(
    query="Help me design the cost tracker",
    max_tokens=4096,
    priority=["semantic", "episodic", "procedural"]
)

# Category-based browsing
all_ideas = await memory.browse(category="ideas.*", tags=["monetisable"])

# Tag-based retrieval across all categories
urgent_items = await memory.search(tags=["urgent"], limit=20)
```

---

## 🏗️ MEMORY LIFECYCLE

```
New Information
    │
    ├── 1. Classify (which category, which memory type?)
    │
    ├── 2. Extract (pull entities, facts, events, procedures)
    │
    ├── 3. Embed (generate vector embedding for similarity search)
    │
    ├── 4. Tag (apply relevant tags)
    │
    ├── 5. Store (persist to appropriate backend)
    │
    ├── 6. Link (connect to existing entities and memories)
    │
    └── 7. Index (update search indices)

Memory Maintenance (periodic):
    │
    ├── Summarise old conversations → Long-Term Summary Memory
    ├── Merge duplicate entities → Semantic Memory dedup
    ├── Update confidence scores → Based on new information
    ├── Decay irrelevant memories → Lower retrieval priority
    └── Archive completed items → Move from active to archive
```

---

## 🎯 DESIGN PRINCIPLES

1. **Local-first:** Default storage is SQLite + ChromaDB. No cloud dependency.
2. **Privacy-native:** Memory Manager never sends data externally unless explicitly configured.
3. **Taxonomy-flexible:** Users can define custom taxonomies. The default 5-domain structure is a starting point.
4. **Multi-backend:** Any memory type can use any storage backend via adapters.
5. **Composable:** Memory Manager works standalone or integrates with Router, Privacy Layer, etc.
6. **Progressive enhancement:** Start with SQLite, add vector search when needed, add knowledge graphs later.
7. **Auditable:** Every memory operation is logged. Users can see exactly what the system remembers and why.

---

## 📚 EXAMPLE USE CASES

### Example 1: Multi-Domain Entry
**Input:** "The Dell GPU server is set up with 2x RTX 4090 for local AI workloads"

**Storage:**
- → **Home > Home Infrastructure > Servers & hardware** (episodic: "Set up Dell GPU server")
- → **Work > AI & Engineering Projects > Local LLM infrastructure** (semantic: "Dell server has 2x RTX 4090")
- Tags: `high-impact`, `completed`

### Example 2: Idea Capture
**Input:** "Could we build a tool that auto-generates GitHub project boards from a README?"

**Storage:**
- → **Ideas > Raw Ideas Inbox** (episodic: idea captured)
- → **Work > Business & Income Streams > Automation opportunities** (linked)
- Tags: `monetisable`, `automation-candidate`, `research-needed`

### Example 3: Procedural Learning
**Input:** Successfully deployed v2.1 using the blue-green deployment pattern

**Storage:**
- → **Work > Operations > Workflows** (procedural: "Blue-green deployment" with steps)
- → Update success_count for existing procedure
- Tags: `completed`

---

**Document Version:** 1.0  
**Last Updated:** February 15, 2026  
**Next Step:** Implement `MemoryManager` base class and SQLite backend
