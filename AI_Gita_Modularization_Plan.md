# AI Gita Modularization Plan

## 1. Objective

Refactor AI Gita into a maintainable, extensible, contributor-friendly structure without changing the current user experience.

This plan assumes:
- The visible tab structure stays intact.
- The current card order inside each tab stays intact.
- Search, glossary, TTS, quizzes, flashcards, reading state, and Mermaid behavior stay intact.
- No content rewrite happens in this phase.

## 2. Current-State Constraints

Verified current state:
- 35 visible tabs
- 287 rendered concept cards
- 40 rendered diagrams (`.arch-diagram` or `.mermaid-wrap`)
- 287 audio-enabled card tracks (`data-listen-track`)
- 22 mini quizzes
- 273 check-yourself blocks
- 160 Q&A items across three volumes
- 74 glossary terms

Behavioral constraints that must remain true during modularization:
- The app boots with the Start Here / plan tab visible first.
- Mermaid rendering is sensitive to hidden panels; only visible-panel rendering should happen during boot.
- Several helper surfaces are injected during boot and depend on stable panel/card structure.
- `reparentOrphans()` and conservative deduping are part of the current content recovery path.
- TTS currently attaches to card-level listen tracks after card generation, not to raw source markup.
- The current `docs/tabs/*.md` files are useful summary docs, but they are not the content source of truth.

## 3. Recommended End State

### 3.1 Architecture

Use a 4-layer content system:

1. App shell
- Keep `AI_Gita.html` as the runtime shell during the transition.
- The shell owns tab chrome, boot order, local state, keyboard shortcuts, search wiring, TTS, print behavior, and visible-panel Mermaid rendering.

2. Content modules
- Move narrative content into topic-oriented Markdown modules under `/content`.
- These modules become the editable source of truth for section text.

3. Structured data sidecars
- Move highly interactive datasets into structured files under `/content/_data`.
- This includes dependency graph data, weekly planner data, role-path metadata, freshness index data, and any future machine-generated summaries.

4. Tab assembly manifests
- Preserve the current UX by assembling each visible tab from ordered references to section IDs.
- This is the critical bridge between topic-oriented content modules and the current tab-oriented interface.

### 3.2 Why tab manifests are required

The user-facing tabs are not a clean 1:1 match with the preferred long-term modules.

Examples:
- `tab-agents` mixes prompting, agent loops, memory, and protocol-stack content.
- `tab-devexp` mixes prompt workflow, SDK ergonomics, access governance, and self-service platform topics.
- `tab-emerging` mixes frontier model topics, new fine-tuning methods, MCP, multimodal systems, and agentic trends.

Because of that, the correct target is:
- Topic-oriented content modules for maintainability
- Tab manifests for preserving the existing UX

### 3.3 Recommended filesystem

```text
/content/
  start-here.md
  quick-guide.md
  ai-landscape.md
  role-paths.md
  whats-new.md
  fundamentals.md
  llm.md
  prompt-engineering.md
  rag.md
  agents.md
  mcp.md
  fine-tuning.md
  specialized-ml.md
  architecture.md
  evaluation.md
  governance.md
  dev-experience.md
  adoption.md
  live-coding.md
  qa-vol-1.md
  qa-vol-2.md
  qa-vol-3.md
  interview-strategy.md
  career-path.md
  emerging-topics.md
  cloud-platforms.md
  glossary.md
  _data/
    dependency-map.json
    weekly-plans.json
    role-paths.json
    freshness-index.json
    tab-meta.json
  _manifests/
    tabs.json
    tab-plan.json
    tab-hub.json
    tab-landscape.json
    ...
/docs/tabs/
  foundations.md
  llm-genai.md
  rag-agents.md
  engineering.md
  practice.md
```

## 4. Ownership Split

### 4.1 Keep in the shell

Keep these runtime concerns in `AI_Gita.html` first, then extract them into JS/CSS modules later:
- Tab navigation, grouped nav labels, and tab switching behavior
- Boot orchestration and render ordering
- Visible-panel Mermaid rendering
- Search indexing and search UI wiring
- TTS service and toolbar
- Read-state, resume state, SRS stamps, and localStorage-backed preferences
- Flashcards, mini quizzes, Q&A toolbar, and randomization behaviors
- Print mode, back-to-top, and keyboard shortcuts
- Card rendering from section source

### 4.2 Move into Markdown modules

Move these into `/content/*.md`:
- All narrative section copy currently living inside tab panels
- All tab-specific explanatory sections
- All conceptual walkthroughs, decision guides, visual overviews, deep dives, and examples
- Q&A volume copy
- Interview and career guidance content
- Glossary definitions, if kept as authored Markdown rather than JS data

### 4.3 Move into structured sidecars

These should not stay as hand-edited HTML blocks inside the shell:
- Dependency map graph relationships
- Weekly planner schedules and pace options
- Role-path definitions and role-to-core-topic mappings
- Freshness / snapshot buckets
- Tab metadata currently hard-coded in `TAB_META`
- Optional machine-generated TTS summaries if they become explicit source data later

## 5. Target Module Catalog

| Target module | Purpose | Primary current sources |
| --- | --- | --- |
| `/content/start-here.md` | Onboarding and study flow | `tab-plan` |
| `/content/quick-guide.md` | Guided hub and jump-off experience | `tab-hub` |
| `/content/ai-landscape.md` | Market, role, and solution-space orientation | `tab-landscape` |
| `/content/role-paths.md` | Role-targeted learning plans and revision surfaces | `tab-paths` |
| `/content/whats-new.md` | Snapshot and freshness-oriented content | `tab-snapshot` |
| `/content/fundamentals.md` | Math, ML, and deep learning fundamentals | `tab-math`, `tab-ml`, `tab-dl` |
| `/content/llm.md` | LLMs, foundation models, multimodal, and long-context core content | `tab-llm`, parts of `tab-genai`, parts of `tab-longctx`, parts of `tab-emerging` |
| `/content/prompt-engineering.md` | Prompt patterns, prompt tooling, prompt lifecycle, output control | parts of `tab-genai`, `tab-agents`, `tab-devexp`, `tab-emerging` |
| `/content/rag.md` | Retrieval, chunking, reranking, vector search, RAG eval | `tab-rag`, part of `tab-longctx` |
| `/content/agents.md` | Agent loops, memory, multi-agent patterns, computer-use agents | most of `tab-agents`, parts of `tab-agentops`, parts of `tab-emerging` |
| `/content/mcp.md` | MCP and agent protocol stack content | parts of `tab-agents`, `tab-akp`, `tab-emerging` |
| `/content/fine-tuning.md` | Fine-tuning, PEFT, preference optimization, new tuning methods | `tab-finetune`, part of `tab-emerging` |
| `/content/specialized-ml.md` | RecSys, time series, tabular, CV, NLP | `tab-recsys`, `tab-cvnlp` |
| `/content/architecture.md` | Infra, serving, platform design, system design, AKP, cloud architecture | `tab-infra`, much of `tab-mlops`, `tab-sysdesign`, most of `tab-akp`, parts of `tab-agentops`, parts of `tab-cloud` |
| `/content/evaluation.md` | Experimentation, drift, monitoring, observability, benchmark thinking | `tab-datasci`, parts of `tab-longctx`, parts of `tab-mlops`, most of `tab-agentops` |
| `/content/governance.md` | Governance, policy, safety, release readiness, risk controls | `tab-gov2`, `tab-safety`, parts of `tab-devexp`, part of `tab-agentops` |
| `/content/dev-experience.md` | SDKs, portals, self-service developer workflows | most of `tab-devexp` |
| `/content/adoption.md` | Change management, literacy, organizational rollout | `tab-people` |
| `/content/live-coding.md` | Coding drill content and implementation walkthroughs | `tab-coding` |
| `/content/qa-vol-1.md` | Q&A volume 1 | `tab-qa` |
| `/content/qa-vol-2.md` | Q&A volume 2 | `tab-qa2` |
| `/content/qa-vol-3.md` | Q&A volume 3 | `tab-qa3` |
| `/content/interview-strategy.md` | Interview process, scoring, behaviorals, presentation | `tab-interview` |
| `/content/career-path.md` | Career ladders, promotion, transitions, team evaluation | `tab-career` |
| `/content/emerging-topics.md` | Frontier trends and near-term shifts | much of `tab-emerging` |
| `/content/cloud-platforms.md` | Cloud provider comparisons and cloud decision content | `tab-cloud` |
| `/content/glossary.md` | Glossary source of truth | `tab-glossary` |

## 6. Complete Section-to-Module Mapping

The rule below is intentional:
- If a tab is homogeneous, it gets a default target module.
- If a tab mixes concerns, section-level exceptions are called out explicitly.
- Every rendered section listed below is accounted for.

### 6.1 Start-here and orientation tabs

#### `tab-plan` / Start Here
Default target module: `/content/start-here.md`
Structured sidecars: `/content/_data/dependency-map.json`, `/content/_data/weekly-plans.json`, `/content/_data/tab-meta.json`
Sections in this tab:
- Visual overview
- How to Use This Document - 3 Learning Modes
- Document At-a-Glance
- Step 2 Dependency Map: Study in This Order
- Step 3 Your Weekly Study Plan
- Quick Reference: Non-Negotiable Tabs by Role

#### `tab-hub` / Quick Guide
Default target module: `/content/quick-guide.md`
Structured sidecars: `/content/_data/role-paths.json`, `/content/_data/weekly-plans.json`, `/content/_data/tab-meta.json`
Sections in this tab:
- Use-case quick routes
- How to use this guide
- Your learning gaps right now
- The complete map - how all 34 core tabs fit together
- Your week-by-week study plan
- Role-based pathways - pick the closest match
- 8 mental models that make the rest click
- Where do I go when I get stuck?
- 74-term glossary - the vocabulary of 2026 AI
- The 2026 production stack at a glance

#### `tab-landscape` / AI Landscape
Default target module: `/content/ai-landscape.md`
Sections in this tab:
- Visual overview
- Role Taxonomy: What Each Role Actually Does
- 2026 Tech Stack Map
- What Interviewers Actually Test by Company Type
- Open-weight vs Closed Models: Enterprise Decision Framework
- Interview Signal Map by Role
- 2025 Market Signals: What Employers Actually Want
- AI Capability Map What Problems Each Technology Solves
- Decision: Which AI Approach For Which Problem?
- Build vs Prompt vs Fine-tune vs Train
- Go Deeper - AI Landscape

#### `tab-paths` / Role Paths
Default target module: `/content/role-paths.md`
Structured sidecars: `/content/_data/role-paths.json`
Sections in this tab:
- Revision Studio
- Anchored Learning Paths
- 1-Page Cheat Sheets by Role
- Top 20 Must-Know Answers
- Top Formulas to Remember

#### `tab-snapshot` / What's New
Default target module: `/content/whats-new.md`
Structured sidecars: `/content/_data/freshness-index.json`
Sections in this tab:
- Why This Tab Exists
- Current Snapshot Buckets
- Cross-Reference
- Freshness Index by Tab

### 6.2 Foundations

#### `tab-math` / Math & Stats
Default target module: `/content/fundamentals.md`
Sections in this tab:
- Visual overview
- Where Math Lives in This Document
- Math Building Blocks Learning Order
- Math Prerequisites by Role
- Visual Cheatsheets - The 3 Most-Asked Math Intuitions
- 1. Gradient Descent - How models actually learn
- 2. Attention = Learned Weighted Average
- 3. Softmax vs Sigmoid - Two Activations You Must Know Cold
- Go Deeper - Math & Stats

#### `tab-ml` / ML Fundamentals
Default target module: `/content/fundamentals.md`
Sections in this tab:
- Visual overview
- Linear Models Concept, Math & Code
- Tree-Based Models XGBoost Deep Dive
- Bias-Variance, Evaluation & Model Selection
- Unsupervised Learning
- ML Algorithm Landscape When to Use What
- Bias-Variance Tradeoff Visual
- Evaluation Metrics Which to Use When
- Go Deeper - ML Fundamentals

#### `tab-dl` / Deep Learning
Default target module: `/content/fundamentals.md`
Sections in this tab:
- Visual overview
- Backpropagation: The Full Derivation
- Normalization Techniques

### 6.3 LLM, GenAI, fine-tuning, and long context

#### `tab-llm` / LLMs & Foundation
Default target module: `/content/llm.md`
Sections in this tab:
- What is an LLM?
- LLM Content Map
- LLM Architecture Evolution
- LLM Knowledge Depth by Role
- Attention Math - A Concrete 3-Token Walkthrough
- Sampling Parameters Cheatsheet
- 2026 Frontier Model Lineup - Context, Pricing, Sweet Spot
- Go Deeper - LLMs & Foundation Models

#### `tab-genai` / Generative AI
Default target module: `/content/llm.md`
Section-level exception:
- Prompt Engineering Techniques When to Use Each -> `/content/prompt-engineering.md`
Sections staying in `/content/llm.md`:
- Diffusion Models: Complete Math & Architecture
- GANs, VAEs & Multimodal
- Flow Matching & Modern Image Generation Stack
- Production Image Generation & VAE Implementation
- VAE Complete Implementation
- GenAI Architecture Patterns Visual Overview
- Go Deeper - Generative AI

#### `tab-finetune` / Fine-tuning
Default target module: `/content/fine-tuning.md`
Sections in this tab:
- When to Fine-tune vs RAG vs Prompting
- LoRA Visual Explanation
- Fine-tuning vs RAG vs Prompting Decision Guide
- LoRA: The Math & Implementation
- Dataset Preparation & Quality
- Fine-tuning Hyperparameter Reference & Dataset Quality
- Fine-tuning Decision Tree
- LoRA vs Full Fine-tune Side by Side
- LoRA Math Complete Derivation
- Preference Optimisation Zoo - pick the right loss in 2026
- GRPO + RLVR - the reasoning-model recipe
- PEFT in 2026 - LoRA is just the start
- Go Deeper - Fine-tuning

#### `tab-longctx` / Long Context & SSMs
Default target module: `/content/llm.md`
Section-level exceptions:
- Advanced RAG Patterns -> `/content/rag.md`
- Long-Context Benchmarks - what to actually measure -> `/content/evaluation.md`
Sections staying in `/content/llm.md`:
- RoPE Context Extension: YaRN & LongRoPE
- Long Context in 2026 - what actually works at 1M+ tokens
- Go Deeper - Long Context & SSMs

### 6.4 RAG, prompting, agents, and protocols

#### `tab-rag` / RAG & Vector
Default target module: `/content/rag.md`
Sections in this tab:
- RAG Pipeline End-to-End Flow
- Chunking Strategy Comparison
- Hybrid Search Why You Need Both
- RAG Pipeline Architecture
- Vector Search: HNSW Internals & BM25
- RAG Evaluation (RAGAS) & Failure Modes
- RAG in 2026 - what changed since the textbook
- Hands-on Implementation - Minimal RAG
- Go Deeper - RAG & Vector Search

#### `tab-agents` / Agents & Prompting
Default target module: `/content/agents.md`
Section-level exceptions:
- Prompt Engineering: Every Technique -> `/content/prompt-engineering.md`
- Agent Protocol Stack - the "OSI of agents" Go Deeper - Agents & Prompting -> `/content/mcp.md`
Sections staying in `/content/agents.md`:
- ReAct Agent Loop Step by Step
- Multi-Agent Architecture Patterns
- 4-Layer Memory Architecture
- ReAct Agent: Complete Implementation
- LangGraph: Stateful Multi-Agent Workflows

Note:
- The protocol-stack section label is visibly merged with the deeper-reading suffix in the current DOM export. During migration, split it into a normal section title plus separate related-links metadata, but keep the rendered user text unchanged unless content revision is explicitly requested later.

### 6.5 Specialized ML coverage

#### `tab-recsys` / RecSys · TS · Tabular
Default target module: `/content/specialized-ml.md`
Sections in this tab:
- Visual overview
- Recommendation Systems: Two-Tower + Matrix Factorization
- Time Series Forecasting
- Deep Learning for Recommendations & Production Architecture
- Recommendation System Production Cascade Pipeline
- Two-Tower vs DLRM Retrieval vs Ranking
- Recommendation Metrics What Matters and Why
- Go Deeper - RecSys, Time Series & Tabular

#### `tab-datasci` / Data Science
Default target module: `/content/evaluation.md`
Sections in this tab:
- Visual overview
- Causal Inference
- A/B Testing & SQL
- Advanced A/B Testing & Uplift Modeling
- Confounding Why Correlation Fails
- A/B Test Design Flow
- Uplift Modelling Target the Right Users
- Go Deeper - Data Science

#### `tab-cvnlp` / CV & NLP
Default target module: `/content/specialized-ml.md`
Sections in this tab:
- Visual overview
- Computer Vision: Architectures & Algorithms
- NLP: Tokenization, Embeddings & Tasks
- NLP Task Reference
- Production CV Patterns & NLP Evaluation
- BPE Tokenizer: Complete Implementation from Scratch
- CV vs NLP Task Map
- Transformer Transfer Learning CV vs NLP
- CV vs NLP Task Mapping
- Transfer Learning: CV vs NLP
- Go Deeper - CV & NLP

### 6.6 Infrastructure, architecture, ops, governance

#### `tab-infra` / AI Infrastructure
Default target module: `/content/architecture.md`
Sections in this tab:
- GPU Memory Hierarchy Why Bandwidth Matters
- Distributed Training Which Strategy for Which Problem
- Quantisation Decision Guide
- GPU Architecture & Memory
- Distributed Training Strategies
- Knowledge Distillation & Structured Pruning
- Inference & Serving - 2026 Production Stack
- Speculative Decoding - the latency cheat code
- Disaggregated Prefill / Decode (P/D split)
- Quantisation - the 2026 menu
- Prefix / Prompt Caching - mandatory for cost control
- Go Deeper - AI Infrastructure

#### `tab-mlops` / MLOps / LLMOps
Default target module: `/content/architecture.md`
Section-level exceptions:
- Drift Detection What to Monitor and When to Act -> `/content/evaluation.md`
- Production Monitoring What to Alert On -> `/content/evaluation.md`
- LLM & Agent Observability in 2026 - OpenTelemetry GenAI Conventions -> `/content/evaluation.md`
- Reasoning-Model Observability - the new dashboards -> `/content/evaluation.md`
Sections staying in `/content/architecture.md`:
- ML Pipeline Architecture
- LLMOps: What's Different
- CI/CD Pipeline for ML Systems
- ML Pipeline Full Lifecycle Visual
- LLMOps vs Classic MLOps Key Differences
- Go Deeper - MLOps / LLMOps

#### `tab-sysdesign` / System Design
Default target module: `/content/architecture.md`
Sections in this tab:
- Visual overview
- Production LLM System: Complete 6-Layer Architecture
- Multi-Tenancy in LLM Systems
- System Design Scenario: Design a Legal Document Q&A System
- System Design Scenario: High-Volume Recommendation + LLM Hybrid
- ML System Design Core Architecture Patterns
- System Design Interview Framework (FRAME)
- Go Deeper - System Design

#### `tab-akp` / Agentic Platform
Default target module: `/content/architecture.md`
Section-level exceptions:
- MCP Gateway Tool Registry Pattern -> `/content/mcp.md`
- MCP Gateway vs Direct Tool Call -> `/content/mcp.md`
Sections staying in `/content/architecture.md`:
- Visual overview
- AKP - 8-Plane Reference Architecture
- AKP - Six Planes Architecture
- Agent Runtime Request Flow
- AKP Six-Plane Architecture
- Model Gateway: Full Implementation & OTel Instrumentation
- AKP 6-Plane Architecture Visual Breakdown
- AKP 6-Plane Architecture
- AKP vs Traditional API Architecture
- AKP Component Responsibilities
- What is Agent Core?
- Go Deeper - Agentic Platform (AKP)

#### `tab-gov2` / Governance Deep Dive
Default target module: `/content/governance.md`
Sections in this tab:
- Visual overview
- Production Readiness Review (PRR) for AI/Agentic Systems
- Artifact Registry: Versioning Everything
- Red-Teaming AI/Agentic Systems
- PRR Checklist Gate Before Every Production Release
- Risk Tier Model T0 to T3
- Saga Pattern Compensating Transactions in Agentic Workflows
- AI Governance Policy vs Technology Controls
- EU AI Act Risk Tier Decision
- Policy vs Technical Controls
- EU AI Act Which Tier?

#### `tab-agentops` / Agent Runtime Ops
Default target module: `/content/evaluation.md`
Section-level exceptions:
- Four-Layer Memory Architecture -> `/content/agents.md`
- Enterprise Legacy Connectors (IIB/TIBCO in Agent Context) -> `/content/architecture.md`
- HITL Gate Design Risk-Tiered Approvals -> `/content/governance.md`
Sections staying in `/content/evaluation.md`:
- Visual overview
- Prompt Drift Detection & Retrieval Quality Signals
- Agent Operations Monitoring Dimensions
- Agent Monitoring What to Watch
- Agent Monitoring Metrics
- Go Deeper - Agent Ops

#### `tab-safety` / Safety & Ethics
Default target module: `/content/governance.md`
Sections in this tab:
- Visual overview
- Hallucination: Root Causes, Types & Mitigations
- Guardrail Architecture: Implementation
- Defence-in-Depth Guardrail Architecture
- EU AI Act Risk Tier Pyramid
- Bias, Fairness & Regulatory Landscape
- OWASP LLM Top 10 (2025) What to Know for Every Interview
- Go Deeper - Safety & Ethics

#### `tab-devexp` / Dev Experience
Default target module: `/content/dev-experience.md`
Section-level exceptions:
- Prompt Library & Playground -> `/content/prompt-engineering.md`
- Prompt Engineering Tooling & Model Access Governance -> `/content/prompt-engineering.md`
- Prompt Lifecycle From Draft to Production -> `/content/prompt-engineering.md`
- Go Deeper - Governance -> `/content/governance.md`
Sections staying in `/content/dev-experience.md`:
- Visual overview
- Platform AI SDK & Model Access Portal
- Model Access Tiers Self-Service Portal
- Developer Experience Key Components
- SDK vs Raw API Why the Abstraction Matters
- Developer Experience Components
- SDK vs Direct API Call
- Go Deeper - Dev Experience

#### `tab-people` / People & Adoption
Default target module: `/content/adoption.md`
Sections in this tab:
- Visual overview
- Skills Foundation for AI Adoption
- Change Management Program
- Responsible AI Training
- Change Management Fear and Response
- AI Literacy Skills Matrix by Role
- Pilot vs Enterprise Rollout
- Go Deeper - People & Adoption

### 6.7 Practice, interview, and career

#### `tab-coding` / Live Coding
Default target module: `/content/live-coding.md`
Sections in this tab:
- Visual overview
- 1. Multi-Head Attention (FAANG Standard)
- 2. Backpropagation from Scratch
- Live Coding Interview What Each Implementation Tests
- Interview Coding Framework 5 Steps Every Time
- 3. K-Means with K-Means++ Init
- More Critical Implementations
- 4. BPE Tokenizer (GPT / Llama tokeniser core)
- 5. VAE - Variational Autoencoder (encoder + decoder + ELBO)
- 6. Transformer Block (pre-norm, residuals, MHA + SwiGLU FFN)

#### `tab-qa` / Q&A Vol 1
Default target module: `/content/qa-vol-1.md`
Sections in this tab:
- How to Use This Volume
- Interview Loop
- Q&A Volume 1 Extended Q21 to Q60
Additional content scope in same module:
- All 60 visible Q&A items in volume 1

#### `tab-qa2` / Q&A Vol 2
Default target module: `/content/qa-vol-2.md`
Sections in this tab:
- How to Use This Volume
- System-Design Loop
- Q&A Volume 2 Extended Q71 to Q103
Additional content scope in same module:
- All 43 visible Q&A items in volume 2

#### `tab-qa3` / Q&A Vol 3
Default target module: `/content/qa-vol-3.md`
Sections in this tab:
- How to Use This Volume
- Production Review Loop
- Q&A Volume 3 Extended Q114 to Q160
- Q&A Final Q151 to Q160
Additional content scope in same module:
- All 57 visible Q&A items in volume 3

#### `tab-interview` / Interview Strategy
Default target module: `/content/interview-strategy.md`
Sections in this tab:
- Visual overview
- How FAANG/Senior AI Interviews Are Structured
- What Interviewers Actually Score
- Behavioral Questions STAR Templates with AI Context
- Portfolio Presentation for AI Engineers
- Common Interview Mistakes to Avoid

#### `tab-career` / AI Career Path
Default target module: `/content/career-path.md`
Sections in this tab:
- Visual overview
- IC Levels What Each Level Actually Means in AI
- What Actually Gets You Promoted
- Breaking Into AI from Other Backgrounds
- Building Your AI Brand Open Source & Community
- 2025 AI Job Market Reality
- IC Track vs Management Track
- How to Evaluate an AI Team Before Joining

### 6.8 Frontier and cloud tabs

#### `tab-emerging` / Emerging Trends
Default target module: `/content/emerging-topics.md`
Section-level exceptions:
- Agentic Framework Comparison -> `/content/agents.md`
- New Fine-tuning Methods: ORPO and SimPO -> `/content/fine-tuning.md`
- Multimodal LLM Architecture (GPT-4V / LLaVA / Gemini) -> `/content/llm.md`
- Persistent Memory Agents (MemGPT / Letta Pattern) -> `/content/agents.md`
- Model Context Protocol (MCP) The de-facto AI tool-use standard (2026) -> `/content/mcp.md`
- Computer Use / GUI Agents (2026 now GA) -> `/content/agents.md`
- Mixture of Experts (MoE) Why Every Frontier Model Uses It -> `/content/llm.md`
- Structured Output Production Standard for 2025 -> `/content/prompt-engineering.md`
Sections staying in `/content/emerging-topics.md`:
- Visual overview
- Reasoning Models - o1, o3, DeepSeek-R1 Class
- 2026 Frontier Model Comparison
- Reasoning Models the 2026 paradigm

#### `tab-cloud` / Cloud Platforms
Default target module: `/content/cloud-platforms.md`
Sections in this tab:
- Visual overview
- Cloud LLM Platform Decision: AWS Bedrock vs Azure OpenAI vs GCP Vertex
- Decision Framework: Build vs Buy vs Fine-tune
- AWS SageMaker Pipelines Deep Dive
- HuggingFace Ecosystem Production Depth
- ROI Template for AI Projects
- Technical Debt in AI Systems

### 6.9 Glossary

#### `tab-glossary` / Glossary
Default target module: `/content/glossary.md`
Sections in this tab:
- How to Use the Glossary
- Glossary Navigation Flow
Additional content scope in same module:
- All 74 glossary terms and their cross-references

## 7. Audio-Enabled Sections

Current fact:
- Every rendered concept card currently receives a `data-listen-track` value.
- Audio coverage is therefore card-scoped, not tab-scoped and not paragraph-scoped.
- Current parity is 287 cards and 287 listen tracks.

Implication for modularization:
- The content pipeline must compile Markdown sections into the same card structure before TTS enhancement runs.
- TTS should continue to derive listen tracks after card assembly.
- Do not hand-author TTS strings for every section unless there is a clear editorial reason.

Recommended future metadata:
- `tts_summary`: optional override if a section needs a custom commute-friendly summary
- `tts_skip`: optional flag for sections that should not be spoken
- `tts_priority`: optional rank for future queue or commute modes

## 8. Reusable Components to Extract

| Component family | Current markers / functions | Recommended future ownership |
| --- | --- | --- |
| Tab shell | `.tb`, `.panel`, tab grouping, `sw()` | Shell runtime |
| Concept card renderer | `.sh`, `.concept-card-shell`, `buildCardsForPanel()` | Shared renderer |
| Study cards and takeaways | `.studycard`, `.takeaways`, `injectStudyCards()`, `injectTakeaways()` | Renderer + module metadata |
| Onramps and worked examples | `injectOnramps()`, `injectWorkedExamples()` | Renderer + authored block syntax |
| Read-state widgets | `.read-toggle`, `.srs-stamp`, `injectReadToggles()`, `injectSrsStamps()` | Runtime feature module |
| Glossary surface | `GLOSSARY`, `buildGlossary()`, `.gloss-*` | Glossary renderer + glossary source module |
| Q&A tools | `.qa-toolbar`, flashcards, random quiz | Practice feature module |
| Check-yourself and mini-quiz | `.check-yourself`, `.mini-quiz` | Authored block syntax + renderer |
| Role and dependency maps | `.rsel-btn`, `.dep-btn`, role paths, weekly plan | Structured data + dashboard renderer |
| Diagram wrappers | `.arch-diagram`, `.mermaid-wrap`, `renderMermaidInPanel()` | Shared diagram renderer |
| TTS toolbar and service | `#tts-bar`, `window.speechSynthesis`, queue/section/autoscroll modes | Runtime service |
| Search and indexing | `buildIndex()`, `setupSearch()` | Runtime service driven by compiled content |

## 9. Authoring Model for Contributors and AI Assistants

### 9.1 Authoring rules

Use Markdown as the source of truth for narrative content, with stable front matter.

Recommended section schema:

```md
---
section_id: llm.attention-math-3-token
tab_slots:
  - llm
title: Attention Math - A Concrete 3-Token Walkthrough
difficulty: int
estimated_time: 40 min
roles: [aie, mle, arc]
prereq: [dl]
next: [genai, finetune, rag, agents]
has_diagram: true
has_quiz: true
---
```

Recommended authored block syntax:
- Standard Markdown headings for section titles
- Fenced `mermaid` blocks for diagrams
- Custom callout blocks for study cards / worked examples / takeaways
- Custom `check-yourself` and `mini-quiz` blocks for interactive pedagogy

### 9.2 Build responsibilities

The build step should:
- Parse front matter and content blocks
- Emit current tab/panel/card structure with stable anchors
- Generate or attach TTS listen tracks
- Preserve search text and printable output
- Generate tab manifests and cross-links
- Feed summary docs under `docs/tabs/*.md`

### 9.3 Contributor workflow

Recommended workflow:
1. Edit only `/content/*.md` or `/content/_data/*`
2. Run the content compiler
3. Run parity validation for touched tabs
4. Review generated DOM counts and anchor stability
5. Review visual output only after parity passes

### 9.4 AI-assisted workflow

Recommended AI rules:
- AI should edit source modules, never compiled HTML
- AI should preserve `section_id`, tab slots, and cross-reference keys
- AI should not change narrative order inside a tab unless explicitly asked
- AI should not alter glossary keys, path IDs, or dependency IDs casually
- AI should treat TTS summaries and quiz blocks as structured fields, not freeform prose blobs

## 10. Migration Phases

### Phase 0: Freeze the current UX baseline
- Capture current counts by tab and globally.
- Freeze anchor IDs and tab order.
- Record parity targets: 35 tabs, 287 cards, 40 diagrams, 287 listen tracks, 160 Q&A, 74 glossary terms.

### Phase 1: Externalize structured metadata first
- Move `TAB_META` to `/content/_data/tab-meta.json`.
- Move dependency map, week planner, role-path metadata, and freshness data into sidecars.
- Keep tab rendering in the shell.

### Phase 2: Externalize narrative modules tab-by-tab
- Start with homogeneous tabs first: math, ml, dl, llm, rag, infra, sysdesign, interview, career.
- Then move mixed tabs that require manifest stitching: agents, devexp, emerging, agentops.
- Compile the Markdown back into the same card structure.

### Phase 3: Move glossary and Q&A sources out of inline JS/HTML
- Move glossary source into `/content/glossary.md` or a glossary-sidecar schema.
- Move Q&A corpora into `/content/qa-vol-*.md` with stable question IDs.

### Phase 4: Extract runtime feature modules
- Split TTS, glossary renderer, Q&A tools, dashboard widgets, and search into standalone JS files.
- Reduce `AI_Gita.html` to shell markup plus loader references.

### Phase 5: Generate overview docs
- Generate or refresh `docs/tabs/*.md` from source manifests.
- Keep them as contributor overviews, not primary authored content.

## 11. Validation Gates

After each migration slice, validate the touched tabs against these invariants:
- Same tab count and tab order
- Same visible section/card count for touched tabs
- Same diagram count for touched tabs
- Same `data-listen-track` count as card count
- Same glossary term count and cross-reference behavior
- Same Q&A item count
- Same tab boot behavior and visible-panel Mermaid behavior
- Same search discoverability for section titles and glossary terms

Recommended automated checks:
- DOM snapshot by tab
- Section-title parity by tab
- Anchor parity by section ID
- Card-count parity by tab
- TTS-track parity by tab
- Diagram-count parity by tab

## 12. Practical Recommendation

Do not try to map one tab to one Markdown file.

The current UI is tab-oriented, but the requested long-term structure is concept-oriented. The maintainable answer is:
- concept-oriented source modules
- manifest-driven tab assembly
- shell-owned runtime behavior

That gives you all three goals at once:
- no UX change
- contributor-friendly source layout
- room to grow without returning to a single monolithic HTML file