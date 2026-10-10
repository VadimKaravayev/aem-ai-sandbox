# AEM AI Sandbox — 24-Week AI Engineer Curriculum

## Goal

Transition from experienced AEM/Java/React engineer to a market-ready AI application engineer who can design, build, secure, evaluate, deploy, and operate production AI systems.

Primary portfolio project: **AEM Operations & Diagnostics Agent**.

Time budget: approximately **5–6 hours per week**.

Certification target: **Microsoft Certified: Azure AI Apps and Agents Developer Associate (AI-103)**.

Official course: https://learn.microsoft.com/en-us/training/courses/ai-103t00

Certification page: https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-apps-and-agents-developer-associate/

---

## Curriculum principles

This curriculum is optimized for an experienced software engineer. It does not treat AI as a separate academic subject. The emphasis is on building production systems that combine:

- Python for AI engineering
- Java/AEM integration
- LLM APIs and structured outputs
- RAG and hybrid/vector search
- tool calling and MCP
- agent harnesses and orchestration
- Microsoft Foundry and Azure AI services
- identity, RBAC, Managed Identity, and secrets
- evaluation, observability, safety, and cost control
- CI/CD and production deployment

The Microsoft AI-103 material is integrated into the existing 24-week project rather than studied as a separate parallel track.

---

# Phase 1 — AI Application Foundations

## Week 1 — LLM fundamentals

### Learn
- tokens and context windows
- system/user/tool messages
- temperature and sampling
- latency and cost trade-offs
- model selection
- hallucinations and grounding

### Build
Call an LLM from Python and analyze AEM diagnostic text.

### AI-103 alignment
Generative AI fundamentals and Microsoft Foundry concepts.

---

## Week 2 — Structured outputs

### Learn
- JSON schema
- Pydantic
- schema-constrained generation
- validation and retries
- deterministic application boundaries

### Build
Return validated diagnostic findings as typed objects instead of free-form text.

---

## Week 3 — Tool calling for AEM diagnostics

### Required tools
- `get_bundle_status`
- `get_component_status`

### Engineering requirements
- deterministic mocks
- strict schemas
- allowlisted tool registry
- argument validation
- correlated `call_id`
- safe failures
- no MCP/JMX/RAG/LangGraph yet

### Learn
Understand the agent loop: model proposes an action, application validates it, tool executes, model receives the result.

---

## Week 4 — AI service/API layer

### Learn
- FastAPI
- async request handling
- dependency injection
- API contracts
- streaming
- timeouts and retries
- basic AI-specific error handling

### Build
Expose the diagnostics assistant through an HTTP API.

### Market skill
Production AI engineers need to package AI functionality as reliable software services, not notebooks.

---

# Phase 2 — Retrieval-Augmented Generation

## Week 5 — Embeddings and vector search

### Learn
- embeddings
- similarity search
- cosine similarity
- vector indexes
- semantic search
- vector-search limitations

### Build
Index a small AEM documentation corpus.

---

## Week 6 — Chunking and retrieval quality

### Learn
- chunk size and overlap
- metadata
- document structure
- retrieval recall/precision
- query rewriting

### Build
Experiment with multiple chunking strategies and record retrieval results.

---

## Week 7 — Production RAG

### Learn
- grounded answers
- citations
- reranking
- hybrid search
- filtering
- retrieval debugging
- failure modes

### Build
Answer AEM operational questions only from retrieved documentation and include sources.

### Azure extension
Rebuild the retrieval layer with **Azure AI Search / Foundry knowledge connections** when practical.

---

## Week 8 — RAG evaluation

### Learn
- retrieval evaluation datasets
- answer relevance
- groundedness
- context relevance
- hallucination testing

### Build
Create a repeatable benchmark with 20–30 AEM questions and expected sources.

---

# Phase 3 — Tools, MCP, and Agent Harnesses

## Week 9 — JMX/Jolokia diagnostics

### Learn
- JMX concepts
- Jolokia HTTP/JSON access
- safe read-only operational tooling

### Build
Read selected AEM metrics and expose normalized diagnostic data.

---

## Week 10 — MCP

### Learn
- MCP servers and clients
- tools/resources
- capability discovery
- transport concepts
- authentication boundaries

### Build
Expose read-only AEM diagnostic capabilities through an MCP server.

---

## Week 11 — Build an agent harness from scratch

### Learn
- agent loop
- state
- tool selection
- execution limits
- retries
- tracing
- termination conditions

### Build
Implement your own minimal agent harness without LangGraph.

### Goal
Understand what an agent framework actually does before adopting one.

---

## Week 12 — Reliability and safety of tool-using agents

### Learn
- prompt injection
- tool abuse
- allowlists
- schema enforcement
- max-step limits
- idempotency
- approval boundaries
- failure recovery

### Build
Add security and failure tests to the harness.

---

# Phase 4 — Agent Orchestration

## Week 13 — LangGraph fundamentals

### Learn
- state graphs
- nodes and edges
- conditional routing
- persistence
- checkpoints

### Build
Reimplement the diagnostics workflow with LangGraph.

### Suggested course
LangChain Academy — LangGraph / agent fundamentals.

---

## Week 14 — Stateful workflows

### Learn
- long-running workflows
- resumability
- memory vs application state
- retries
- human checkpoints

### Build
Persist diagnostics sessions and resume interrupted workflows.

---

## Week 15 — Human-in-the-loop and guarded remediation

### Learn
- approval gates
- high-risk tool separation
- read vs write capabilities
- rollback concepts

### Build
Allow the agent to propose a remediation but require explicit approval before execution.

---

## Week 16 — Multi-agent and orchestration patterns

### Learn
- router agents
- specialist agents
- handoffs
- sequential vs concurrent orchestration
- when NOT to use multi-agent designs

### Build
Split diagnostics into two or three specialists only where it improves the system.

### Microsoft Learn
Complete relevant modules from **Develop AI agents on Azure**:
https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-azure/

Include Microsoft Agent Framework and multi-agent orchestration concepts.

---

# Phase 5 — Microsoft Foundry and Azure Production Engineering

## Week 17 — Microsoft Foundry fundamentals

### Learn
- Foundry projects
- model deployment
- endpoints
- SDK usage
- environment/configuration management

### Build
Connect the existing diagnostics application to Microsoft Foundry.

### Certification track
Start **AI-103T00-A: Develop AI apps and agents on Azure**.

---

## Week 18 — Foundry agents and secure tools

### Architecture

`Java or .NET service → Microsoft Foundry → AI agent → tools/API → Managed Identity`

### Learn
- Foundry Agent Service
- tools
- API integration
- Microsoft Agent Framework
- agent deployment

### Build
Create a Foundry-hosted agent that invokes diagnostic tools.

---

## Week 19 — Azure identity and security

### Learn
- Microsoft Entra ID
- RBAC
- Managed Identity
- Key Vault
- least privilege
- private networking concepts
- secure API access

### Build
Remove hard-coded secrets wherever Azure identity can be used.

### Market skill
An AI engineer should be able to explain exactly which identity can access which tool/data source.

---

## Week 20 — Deployment, observability, and load testing

### Learn
- containerization
- Azure deployment options
- Application Insights / tracing
- latency
- token usage
- quotas
- cost monitoring
- rate limiting
- retries
- CI/CD

### Build
Deploy the application and compare local vs Azure behavior under load.

### AEM extension
Include the **AEM Edge Functions** hands-on topic where it fits the integration architecture.

---

# Phase 6 — Production AI Quality

## Week 21 — AI security and red-team thinking

### Learn
- prompt injection
- indirect prompt injection
- data exfiltration
- unsafe tool invocation
- authorization vs model decisions
- tenant/data boundaries
- secrets management

### Build
Create an adversarial test suite for the diagnostics agent.

---

## Week 22 — Evaluation harness

### Learn
- regression datasets
- groundedness
- relevance
- tool-call correctness
- task completion
- latency and cost metrics
- human evaluation
- automated evaluators

### Build
Create a reusable evaluation harness that can compare prompts/models/configurations.

### Suggested course
LangChain Academy material on **agent observability and evaluations / production monitoring**.

---

## Week 23 — Anomaly detection and operational intelligence

### Learn
- time-series basics
- baselines
- anomaly detection
- simple forecasting
- when ML is preferable to an LLM

### Build
Analyze AEM operational metrics and surface anomalies to the agent as evidence.

### Goal
Avoid becoming an "LLM-only" engineer. Learn to combine conventional analytics/ML with generative AI.

---

## Week 24 — Final production integration

### Final project
**AEM Operations & Diagnostics Agent**

The finished system should demonstrate:

- structured LLM interaction
- RAG over AEM knowledge
- hybrid/vector retrieval
- tool calling
- MCP integration
- JMX/Jolokia diagnostics
- an explicit agent harness
- LangGraph workflow orchestration
- Microsoft Foundry / Foundry Agent Service
- Azure identity and RBAC
- safe tool execution
- observability
- evaluation
- anomaly detection
- CI/CD/deployment

### Portfolio deliverables

1. Architecture diagram
2. README explaining business value
3. threat model / security notes
4. evaluation report
5. deployment instructions
6. short demo video
7. benchmark results
8. design decisions and trade-offs

---

# AI-103 Certification Overlay

The certification is a milestone, not the curriculum's end goal.

## During Weeks 1–16

Build the engineering fundamentals that make the Microsoft material easier:

- Python
- APIs/SDKs
- generative AI
- RAG
- agents
- tools
- orchestration

## During Weeks 17–20

Work through **AI-103T00-A** alongside the Foundry project.

Pay special attention to:

- generative AI apps in Azure
- Microsoft Foundry
- AI agents
- knowledge connections
- tool integration
- natural language solutions
- visual/multimodal data
- deployment and management

## During Weeks 21–24

Complete the official AI-103 study guide and practice assessment.

Do not book the exam based only on course completion. Be able to implement the tested concepts and explain why one Azure service/design is preferable to another.

---

# Skills expected at the end

## AI engineering
- LLM APIs
- prompt and context design
- structured generation
- embeddings
- RAG
- vector/hybrid search
- tool/function calling
- agents
- MCP
- LangGraph
- multimodal AI basics

## Production engineering
- Python
- FastAPI
- Java integration
- REST APIs
- Docker
- CI/CD
- Azure deployment
- monitoring/tracing
- testing

## Azure / Microsoft AI
- Microsoft Foundry
- Foundry Agent Service
- Microsoft Agent Framework
- Azure AI Search
- Entra ID
- RBAC
- Managed Identity
- Key Vault
- Application Insights

## Quality and safety
- evaluation datasets
- groundedness/relevance testing
- retrieval evaluation
- prompt-injection defenses
- secure tool execution
- observability
- latency/cost analysis

## Existing strengths retained
The curriculum intentionally builds on AEM, Java, React, and TypeScript instead of replacing them. The target profile is an experienced enterprise developer who can add AI capabilities to real systems.
