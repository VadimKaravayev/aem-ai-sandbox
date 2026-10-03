# Standalone AI Engineer Portfolio Project

## Project: AI Technical Due-Diligence & Engineering Research Agent

This is the second flagship project in the 24-week curriculum. It is intentionally **not connected to AEM**.

The purpose is to demonstrate that the developer can design and ship a production-style AI application independently of an existing specialization.

---

# Product idea

Build an AI application that helps an engineering team evaluate a software system, vendor, library, or proposed architecture.

A user creates an assessment workspace and provides material such as:

- GitHub repository or exported source files
- architecture documents
- PDFs
- API documentation
- ADRs
- security notes
- requirements
- benchmark/results files
- optionally selected external/public sources

The system gathers evidence, retrieves relevant material, calls approved tools, analyzes the information, and produces a structured assessment.

Example questions:

- What are the biggest technical risks in this system?
- Where are the security weaknesses?
- Does the implementation match the architecture documentation?
- What dependencies create upgrade or maintenance risk?
- What evidence supports this recommendation?
- Compare architecture A and B against cost, security, scalability, and maintainability.
- Which claims cannot be verified from the supplied evidence?

The important feature is **evidence-first AI**: every significant conclusion must be traceable to a source, tool result, or explicit assumption.

---

# Why this belongs in the portfolio

The application should demonstrate the capabilities employers expect from an AI application engineer:

- Python backend engineering
- LLM APIs
- structured outputs
- RAG
- embeddings
- vector and hybrid search
- reranking
- citations and provenance
- tool/function calling
- MCP
- agent workflows
- human-in-the-loop approval
- long-running/stateful jobs
- multimodal/document processing
- evaluation
- prompt-injection defenses
- authentication and authorization
- cloud identity
- observability
- deployment
- CI/CD
- latency and cost management

The project must look like a real product, not a notebook or prompt demo.

---

# Suggested architecture

```text
React / TypeScript UI
        |
        v
Python / FastAPI API
        |
        +--------------------------+
        |                          |
        v                          v
Workflow / Agent Layer       Ingestion Pipeline
LangGraph / Agent Framework        |
        |                           v
        |                    parsing / chunking
        |                           |
        |                           v
        |                    Azure AI Search
        |                    hybrid + vector
        |
        +----> LLM / Microsoft Foundry
        |
        +----> Approved tools
        |       - repository analysis
        |       - dependency lookup
        |       - document retrieval
        |       - calculator / deterministic analysis
        |       - optional MCP tools
        |
        v
Evidence / citations / assessment
        |
        v
Human review and export

Cross-cutting:
- Entra ID
- RBAC / Managed Identity
- Key Vault
- Application Insights / tracing
- evaluation harness
- CI/CD
```

---

# Core product features

## 1. Assessment workspace

Users can create a workspace for a technical assessment and attach multiple evidence sources.

Store:

- assessment objective
- source metadata
- processing status
- generated findings
- citations
- human decisions

---

## 2. Document and code ingestion

Support at least:

- Markdown/text
- PDF
- source-code files

Stretch goal:

- repository ingestion through GitHub API
- architecture diagrams/images

Implement:

- parsing
- chunking
- metadata
- embeddings
- indexing
- re-indexing/version handling

---

## 3. Evidence-grounded RAG

Use hybrid/vector retrieval and require citations for important claims.

The application should distinguish between:

- evidence-backed conclusion
- inference
- assumption
- missing evidence

Do not let the model present an unsupported assumption as fact.

---

## 4. Structured findings

Each finding should use a schema such as:

```json
{
  "title": "...",
  "severity": "low | medium | high | critical",
  "category": "security | architecture | maintainability | performance | operations",
  "summary": "...",
  "evidence": [],
  "confidence": 0.0,
  "recommendation": "...",
  "assumptions": []
}
```

The UI should make evidence and confidence visible.

---

## 5. Tool-using agent

The agent should decide when retrieval alone is insufficient and use approved tools.

Examples:

- inspect repository structure
- search source code
- inspect dependency manifests
- calculate metrics
- query an internal/public API
- retrieve additional evidence

All tools need:

- strict schemas
- allowlisting
- authorization checks
- timeouts
- tracing
- safe errors

---

## 6. Stateful analysis workflow

Use an explicit workflow rather than an unconstrained autonomous loop.

Example:

```text
Define objective
      |
      v
Plan evidence needed
      |
      v
Retrieve / call tools
      |
      v
Generate candidate findings
      |
      v
Verify evidence
      |
      +---- insufficient ----> retrieve again
      |
      v
Score confidence
      |
      v
Human review
      |
      v
Generate final assessment
```

The workflow should support resuming an interrupted assessment.

---

## 7. Human-in-the-loop

Require approval before actions such as:

- adding external evidence automatically
- triggering expensive deep analysis
- publishing/exporting the final report
- executing any future write-capable tool

Demonstrate that authorization is enforced by application code, not left to the LLM.

---

## 8. Evaluation system

Create a small gold dataset with known documents and expected findings.

Measure at least:

- retrieval relevance
- citation correctness
- groundedness
- finding completeness
- tool-call correctness
- unsupported-claim rate
- latency
- token/cost usage

Run evaluations automatically when prompts, models, or retrieval settings change.

---

## 9. Security

Test attacks including:

- prompt injection inside uploaded documents
- instructions hidden in retrieved content
- attempts to invoke unauthorized tools
- cross-workspace data leakage
- malicious filenames/metadata
- oversized input

Use:

- least privilege
- Managed Identity
- RBAC
- secrets in Key Vault
- input validation
- tenant/workspace boundaries

---

## 10. Observability

Record traces for:

- model calls
- retrieval
- reranking
- tool execution
- workflow steps
- errors
- latency
- token usage
- cost estimates

A reviewer should be able to inspect why a finding was produced.

---

# Curriculum integration

This project should reuse concepts from the AEM project rather than doubling the weekly workload.

## Weeks 1–4 — Foundation

Do not build the full app yet.

Reuse the lessons on:

- Python
- structured output
- FastAPI
- tool contracts

At the end of Week 4, create the standalone project's repository skeleton and a minimal API.

Deliverable:

`POST /assessments` creates an assessment with a structured objective.

---

## Weeks 5–8 — RAG MVP

Build the first usable version.

Add:

- file upload
- parsing
- chunking
- embeddings
- vector search
- citations
- basic evaluation dataset

Milestone:

The app can answer technical questions about uploaded documents with verifiable citations.

---

## Weeks 9–12 — Tools and MCP

Add deterministic analysis tools.

Recommended first tools:

- repository/file search
- dependency-manifest parser
- source-code statistics

Expose at least one capability through MCP or consume an MCP server.

Milestone:

The agent can decide when to retrieve documents and when to call a deterministic tool.

---

## Weeks 13–16 — Agent workflow and UI

Add:

- LangGraph or equivalent explicit workflow
- state persistence
- human approval
- React/TypeScript UI
- assessment progress
- evidence viewer
- structured findings

Milestone:

A user can create an assessment, observe its progress, review evidence, and approve the final findings.

---

## Weeks 17–20 — Azure / Microsoft Foundry

Move the portfolio app onto the same production stack being learned for AI-103.

Use where appropriate:

- Microsoft Foundry
- Foundry models / agents
- Azure AI Search
- Managed Identity
- Entra ID
- RBAC
- Key Vault
- Azure Container Apps / App Service / suitable Azure hosting
- Application Insights

Add CI/CD and deployment.

Milestone:

A recruiter can open a deployed version of the application rather than only reading source code.

---

## Weeks 21–22 — Security and evaluation

Create:

- adversarial prompt-injection tests
- authorization tests
- evaluation harness
- regression dataset
- quality dashboard/report

Milestone:

The GitHub repository contains evidence that the application is evaluated systematically.

---

## Week 23 — Quality/cost optimization

Compare at least two configurations or models.

Measure:

- quality
- latency
- token usage
- estimated cost

Document the trade-off and select a production configuration based on evidence.

---

## Week 24 — Portfolio release

Release **v1.0**.

The project must include:

1. public-quality README
2. architecture diagram
3. live demo or deployable demo environment
4. screenshots
5. short demo video
6. sample assessment
7. evaluation results
8. threat model
9. cost/latency benchmark
10. CI/CD pipeline
11. Docker configuration
12. design-decision document

---

# What the final demo should show

A strong 5–8 minute demonstration:

1. Create a technical assessment.
2. Upload a small repository plus architecture/documentation files.
3. Ask the system to identify the main technical risks.
4. Show retrieval evidence and citations.
5. Show the agent invoking a deterministic repository/dependency tool.
6. Open one trace and explain how the finding was produced.
7. Show a human approval checkpoint.
8. Display evaluation results.
9. Briefly show the Azure architecture and security model.

This tells a much stronger hiring story than simply showing that an LLM can answer questions.

---

# Hiring story

The project should let the developer say:

> I built and deployed an evidence-grounded AI engineering application that combines hybrid RAG, structured outputs, tool-using agents, stateful orchestration, evaluation, security, Azure identity, observability, and CI/CD. I can show how I measure answer quality, prevent unsupported claims, secure tools, and operate the system in production.

That is the target portfolio signal.
