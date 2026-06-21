# System Design — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

**AI system design** is the discipline of architecting production AI systems — deciding how all the pieces fit together so the system is reliable, cost-effective, scalable, and governable.

It's not the same as designing a traditional distributed system. Not because the principles are different, but because AI systems have properties that traditional systems don't:

- **Non-deterministic outputs** — the same request can return different responses. You can't cache them the same way. You can't unit-test them the same way. SLAs look different.
- **Variable compute cost** — processing a 50-token query is 20× cheaper than a 1,000-token query. Cost is runtime-determined, not fixed per request.
- **Quality as a dimension** — a web API either returns 200 or it doesn't. An LLM returns 200 whether the answer is correct or hallucinated. Quality is a first-class design concern, not just an operational one.
- **Model as a dependency** — your system depends on a model (or multiple models) that can change, degrade, or become unavailable. The model is an external dependency with its own versioning, pricing, and SLA — like a database, but less predictable.
- **Context as state** — LLMs are stateless by default, but the quality of their response depends entirely on what's in the context window. Managing context — what goes in, in what order, how much — is a core design concern.

AI system design is the practice of making good decisions across all of these dimensions before a line of code is written. The decisions you make at design time — model choice, retrieval strategy, routing logic, caching approach, evaluation architecture — are expensive to reverse once the system is in production.

---

## 2. Why Should I Care

### For Solution Architects

You are the person who gets asked: "Can we build this?" before anyone knows how. AI system design is how you answer that question with confidence — not by guessing, but by decomposing the problem into solvable pieces and identifying where the risks live.

The questions that AI system design answers at the design stage:

- **Latency:** the user expects a response in 2 seconds. A single GPT-4o call takes 1.5–4 seconds. How do you build a system that meets a 2-second P95 SLA?
- **Cost:** 50,000 users × 10 queries/day × £0.03/query = £15,000/day. Is that in budget? What does the cost model look like as you scale?
- **Quality:** how do you know if the system is working? What does "working" mean for an LLM that gives fluent wrong answers?
- **Failure modes:** what happens when the LLM API is down? When the vector store returns no results? When the agent loops? What are the fallbacks?

### For Enterprise Architects

AI systems touch more of your enterprise stack than any other category of application — they read from your data platform, call your APIs, write to your CRM, and communicate with your customers. The system design decisions determine the blast radius, the data flows, and the compliance surface.

Three design decisions with enterprise-wide implications:

1. **Multi-tenancy model** — how do you serve multiple teams or customers from one AI system without data bleed, cost confusion, or one tenant's load degrading another's experience?
2. **Model routing strategy** — which queries go to which model? A routing layer that sends complex queries to GPT-4o and simple queries to Claude Haiku can cut costs by 60–80% with no user-facing quality difference. But it needs to be designed in, not bolted on.
3. **Feedback loop architecture** — how does what the system does in production inform how it improves? A system without a feedback loop is frozen at the quality it had at launch. This is a design concern, not an operational one.

---

## 3. Think About It Like This (Analogy)

**The Contact Centre Architecture Analogy**

Imagine you're designing a contact centre for a large retailer — not building it, but designing the architecture before anyone is hired or any software is procured.

You need to decide:

- **Routing** — does every call go to the same pool of agents, or do you route by query type? Returns to the returns team, technical support to tech, VIP customers to dedicated agents? *(Model routing in AI systems)*
- **Tiers** — do you have a self-service IVR for simple questions, a first-line agent for standard queries, and escalation to a senior specialist for complex issues? *(Model tiering: fast/cheap for simple, powerful/expensive for complex)*
- **Context passing** — when a customer is transferred from IVR to agent to specialist, what information travels with them? Do they have to re-explain their issue each time? *(Context management and session memory)*
- **Capacity and overflow** — what happens at peak? Do calls queue? Are there overflow rules? What's the maximum queue depth before you start returning "try again later"? *(Rate limiting, fallback routing, load shedding)*
- **Quality assurance** — how do you know if agents are giving good answers? You don't listen to every call — you sample, score, and use the results to train and calibrate. *(LLM evaluation and monitoring)*
- **Cost model** — IVR costs £0.02/minute. First-line agents cost £0.50/minute. Senior specialists cost £2.00/minute. The architecture that routes correctly saves enormous money at scale. *(LLM cost routing)*

Every one of these contact centre architecture decisions has a direct AI system design parallel. The decisions you make before the system is built determine whether it's operationally manageable and financially viable at scale.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

> **Explain Like I'm an Architect**
>
> The 6-layer architecture exists because each layer has a fundamentally different job — and mixing those jobs creates systems that are expensive to change and impossible to govern.
>
> The most common mistake: putting routing logic, orchestration logic, and LLM API calls all inside the same application service. This works for a proof of concept. It becomes a problem the moment you need to: (a) add a second LLM provider as a fallback, (b) apply cost tracking across all model calls, (c) enforce data residency requirements, or (d) add content filtering. All four changes require touching application code, and any of them can break the others.
>
> A model gateway as a separate layer solves all four at once: every LLM call from every part of the application passes through one service that handles routing, fallback, cost tracking, data residency, and content filtering. The application layer just calls an API. This is the same reason enterprises have API gateways instead of every service calling every other service directly — centralised governance, centralised observability, and the ability to change routing rules without rewriting application code.
>
> **Why this matters architecturally:** Each layer boundary in the 6-layer model is a governance enforcement point. The model gateway is where you enforce cost controls and data residency. The retrieval layer is where you enforce data access permissions. The observability layer is where you enforce audit logging. Collapsing layers collapses governance checkpoints.

### 4.1 The 6-Layer Production LLM Architecture

A production LLM system is not just "application → LLM API." At any meaningful scale, it decomposes into six distinct layers, each with its own responsibilities and failure modes.

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: Client / Surface Layer                    │
│  Web, mobile, API, internal tools, voice            │
│  Responsibilities: auth, rate limit per user,       │
│  request validation, response formatting            │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Layer 2: Orchestration Layer                       │
│  LangChain / LangGraph / custom agent framework     │
│  Responsibilities: task decomposition, agent loop,  │
│  tool dispatch, context assembly, retry logic       │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Layer 3: Model Gateway                             │
│  LiteLLM / custom proxy / cloud-native              │
│  Responsibilities: model routing, fallback,         │
│  rate limiting, cost tracking, auth to LLM APIs     │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Layer 4: Knowledge / Retrieval Layer               │
│  Vector DB + document store + cache                 │
│  Responsibilities: semantic search, chunk retrieval,│
│  knowledge freshness, retrieval quality             │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Layer 5: Data & Integration Layer                  │
│  Feature stores, APIs, databases, legacy connectors │
│  Responsibilities: structured data retrieval,       │
│  tool execution, write-back to systems of record    │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Layer 6: Observability & Governance Layer          │
│  OTel, cost tracking, eval pipeline, audit log      │
│  Responsibilities: traces, metrics, LLM quality     │
│  signals, compliance logging, budget alerts         │
└─────────────────────────────────────────────────────┘
```

**What an architect owns at each layer boundary:**

| Boundary | Key design decision |
|---|---|
| Client → Orchestration | Authentication model, rate limit per user/tenant, request schema |
| Orchestration → Gateway | Which queries go to which model (routing policy) |
| Gateway → LLM APIs | Fallback order, budget caps, data residency constraints |
| Orchestration → Knowledge | Retrieval strategy (semantic, hybrid, keyword), chunk size, reranking |
| Orchestration → Data | Which tools can be called, with what auth, with what blast radius controls |
| All layers → Observability | What is logged, what is alerted on, what feeds the eval pipeline |

The most common architectural mistake: collapsing layers 2 and 3 into a single application. This couples orchestration logic to model routing, making it impossible to change models, add fallbacks, or add a new model tier without rewriting application code.

> **Explain Like I'm an Architect**
>
> Model tiering is the AI equivalent of tiered service staffing: you do not assign your most expensive consultant to every task. You assign junior staff to standard tasks and escalate to senior specialists for complex ones.
>
> The pattern translates directly: 60–70% of queries in most enterprise AI systems are simple — intent classification, FAQ lookups, brief Q&A, simple summarisation. A "nano" model (GPT-4o-mini, Claude Haiku) handles these at one-tenth the cost of a premium model and in half the latency. Reserve premium reasoning models for complex multi-step tasks, code generation, and tasks where the quality difference justifies the cost premium.
>
> The routing classifier itself must be cheap and fast — it runs on every single request, so a complex expensive classifier defeats the purpose. A simple heuristic (query length + keyword patterns) or a fast nano model call works well and costs almost nothing.
>
> **Why this matters architecturally:** At scale, tiered routing is one of the highest-leverage architectural decisions you can make. On 100K queries per day, routing 65% to a nano model instead of always using a premium model saves approximately £62,000 per year at typical pricing — with no user-facing quality difference for correctly-routed queries. Design this in from the start, not as a later optimisation.

### 4.2 Model Routing: Tiered Cost Architecture

Not all queries need the most capable (and expensive) model. A routing layer that classifies queries by complexity and routes them to the appropriate model tier is one of the highest-leverage architectural decisions in any LLM system.

**Typical model tier structure:**

| Tier | Model examples | Cost/1M tokens | Latency | Use for |
|---|---|---|---|---|
| Nano | GPT-4o-mini, Claude Haiku | £0.10–0.20 | < 1s | Classification, simple Q&A, intent detection |
| Standard | GPT-4o, Claude Sonnet | £1.50–3.00 | 1–3s | Standard queries, summarisation, RAG responses |
| Premium | o3, Claude Opus | £10–20 | 3–15s | Complex reasoning, multi-step planning, code generation |

**Routing classifier design:**

```
Incoming query
    │
    ▼
Query classifier (fast, cheap — runs on nano model or rule-based)
    │
    ├── Simple factual → Nano tier
    ├── Standard task → Standard tier
    ├── Complex reasoning → Premium tier
    └── Safety-sensitive → Standard tier + safety guardrail
```

**Cost impact example:**
- Without routing: 100K queries/day × all GPT-4o → ~£300/day
- With routing: 60% nano + 35% standard + 5% premium → ~£90/day
- Saving: 70% cost reduction, no user-facing quality difference for routed-correctly queries

**Design consideration:** the routing classifier itself must be cheap and fast (< 50ms, < £0.001/call). A complex router that's almost as expensive as just using the premium model defeats the purpose.

> **Explain Like I'm an Architect**
>
> Latency budget design is the discipline of working backward from your SLA commitment to the component-level performance requirements. It is the AI system equivalent of a network engineer calculating that a 100ms round-trip time means no more than 20ms can be spent at each of five network hops.
>
> The common mistake is to choose all your components (model, vector database, reranker) and then hope their combined latency meets the SLA. By the time you discover the P95 combination is 4.2 seconds against a 2-second SLA, you have already integrated three services and changing any of them is expensive.
>
> The correct approach: subtract the non-negotiable costs (network, auth, parsing) from the SLA first. What remains is your budget for AI processing. Now you know exactly what the LLM call is allowed to cost, what retrieval is allowed to cost, and what each component must deliver. Your vector database selection spec is "P95 < 150ms" — not "find a good vector database."
>
> **Why this matters architecturally:** Latency budgets are how you turn a vague SLA ("respond in 2 seconds") into a concrete component specification ("LLM call: 1,300ms, retrieval: 150ms, intent classification: 80ms"). These specs drive component selection, not the other way around. If the remaining budget after non-negotiable costs is smaller than the P95 of your chosen model, you need a different model, a caching strategy, or a SLA renegotiation — not an optimistic assumption.

### 4.3 Latency Budget Design

For any AI system with a user-facing SLA, you must design the **latency budget** before choosing components. Work backward from the SLA to determine what each layer is allowed to cost.

**Example: 3-second P95 SLA for a customer service assistant**

```
Total budget:                    3,000ms
  ├── Client-side overhead:        100ms
  ├── Network (round trips):       150ms
  ├── Intent classification:        80ms  (nano model, cached)
  ├── Knowledge retrieval:         200ms  (vector search)
  ├── Context assembly:             50ms
  ├── LLM call (standard model):  1,800ms  (P95 for GPT-4o)
  ├── Response processing:          80ms
  └── Budget remaining:            540ms  (buffer for spikes)
```

If the LLM call alone takes 1,800ms at P95, and you have 200ms for retrieval, every component selection and optimization target is now defined. You don't pick a vector database then discover its P95 is 800ms — you specify 200ms and evaluate accordingly.

**Latency optimization levers:**

| Technique | Latency saving | Cost impact | Notes |
|---|---|---|---|
| Streaming responses | 0ms actual, perceived improvement | None | User sees words appearing immediately |
| Prompt caching | 200–400ms | Slight reduction | Works for static system prompt portions |
| Semantic caching | Eliminates LLM call entirely | Major reduction | For repeated similar queries |
| Smaller model routing | 500–2000ms | Major reduction | Only for appropriate query types |
| Speculative decoding | 20–40% faster generation | Slight increase | Model-side, not always available |
| Async tool calls | Parallel tool execution | None | When multiple tools can run simultaneously |

### 4.4 Multi-Tenancy in LLM Systems

A single AI system serving multiple internal teams or customers (multi-tenant) has design requirements that a single-tenant system doesn't.

> **Common Misconception:** "We can add multi-tenancy controls later once we prove the system works."
>
> Multi-tenancy is not an add-on — it is a structural design decision. Adding tenant isolation to a system built without it requires touching every layer: the retrieval layer (to add filtering or separate indexes), the gateway layer (to add per-tenant rate limits and cost tracking), the orchestration layer (to add tenant-scoped tool permissions), and the logging layer (to add tenant-segregated audit trails). Retrofitting these changes is more expensive than designing them in from the start. More importantly, a system that went live without tenant isolation has already exposed cross-tenant data in logs and potentially in retrieval results — a data governance incident, not a future engineering task.

**The four multi-tenancy concerns:**

**1. Data isolation**
Tenant A must not see Tenant B's data — in retrieval results, in context, in logs. Design options:
- **Index-per-tenant:** each tenant has their own vector store index. Strong isolation, higher infrastructure cost.
- **Metadata filtering:** all tenants share one index, but every document is tagged with a tenant ID, and every retrieval query is filtered by the requesting tenant's ID. Cheaper, but requires careful query construction — a missing filter is a data leak.
- **Hybrid:** shared index for public/shared knowledge, per-tenant index for sensitive data.

**2. Cost isolation**
Which team is spending what? Required for internal chargeback and for detecting runaway usage.
- Tag every LLM call with tenant ID at the model gateway layer
- Track token usage per tenant, per model, per time period
- Set per-tenant budget caps and alert thresholds

**3. Rate limiting**
One tenant's burst usage should not degrade other tenants' latency.
- Per-tenant rate limits at the client layer (requests/minute, tokens/minute)
- Token bucket (a rate-limiting algorithm that allows burst requests up to a maximum, then throttles — standard in distributed systems) algorithm for smoothing burst patterns
- Priority queuing: premium tenants get lower queue depth, faster processing

**4. Configuration isolation**
Different tenants may need different system prompts, different model tiers, different tool access.
- Tenant configuration stored in a registry, loaded at request time
- System prompts versioned per tenant, separate from shared base prompt
- Tool permissions defined per-tenant role, not globally

### 4.5 Caching Strategy

Caching in LLM systems has three distinct levels, each with different hit rates and design implications:

**Level 1 — Exact match (response cache)**
Cache the full LLM response for an exact input string.
- Hit rate: low (LLM queries are rarely identical)
- Best for: FAQs, common greetings, boilerplate responses
- TTL: hours to days
- Storage: Redis or Memcached

**Level 2 — Semantic similarity (semantic cache)**
Cache responses for inputs that are semantically equivalent, not just lexically identical.
- "What is your return policy?" and "How do I return a product?" → same cache entry
- Hit rate: moderate (5–15% in practice for conversational systems)
- Implementation: embed the query, check vector similarity against cached queries, return cached response if similarity > threshold (typically 0.95)
- Storage: vector store with TTL metadata

**Level 3 — Prompt caching (provider-side)**
OpenAI, Anthropic, and Google cache the KV computation for the static portion of your prompt (system prompt + few-shot examples). If the first N tokens of the prompt match a cached prefix, you pay only for the new tokens.
- Hit rate: high (if your system prompt is stable and long)
- Cost saving: 50–80% reduction on cached tokens
- Latency saving: 200–400ms
- Requirement: static portion must come first, before the variable user query

**Combined caching architecture:**
```
Request arrives
    │
    ▼
Exact match cache check → hit: return cached response
    │ miss
    ▼
Semantic cache check → hit: return semantically matched response
    │ miss
    ▼
LLM call (with prompt cache prefix if applicable)
    │
    ▼
Store in exact + semantic cache
    │
    ▼
Return response
```

### 4.6 Fallback and Resilience Patterns

LLM APIs have uptime SLAs of 99.5–99.9% — meaning 4–44 hours of downtime per year. For business-critical systems, you need fallback architecture.

**Fallback patterns (in order of preference):**

**Primary → Secondary model fallback:**
If GPT-4o returns a 503, retry on Claude Sonnet. Configure at the model gateway layer so the calling application is unaware.
```
Request → GPT-4o → 503 error
        → retry on Claude Sonnet → success
```

**Graceful degradation:**
If the premium model is unavailable, fall back to a standard model with a simpler prompt. Quality degrades, but the system keeps running.

**Cached fallback:**
If all live models are unavailable, return a cached response for semantically similar queries. For some use cases (FAQ answering, policy lookups) this is acceptable. For others (real-time data queries) it is not.

**Circuit breaker:**
After N consecutive failures on a provider, open the circuit — stop sending requests to that provider and route all traffic to the fallback. After a timeout, probe the primary with one request; if it succeeds, close the circuit and resume normal routing.

**Graceful degradation to rule-based:**
For the most critical path (e.g., order status lookup), have a simple rule-based fallback that doesn't use an LLM at all. Less quality, but zero dependency on LLM availability.

---

## 5. Enterprise Example

**Scenario: Design a Legal Document Q&A System**

Your legal team handles 500 supplier contract reviews per month. Each review involves answering questions like: "Does this contract include a limitation of liability clause? What is the notice period for termination? Does this align with our standard MSA template?"

Currently: a paralegal reads each contract and answers questions manually — 4–6 hours per contract.

**System design walkthrough using the 6-layer architecture:**

**Layer 1 — Client/Surface**
- Internal web interface for paralegals to upload contracts and ask questions
- Authentication: SSO via your enterprise identity provider
- Rate limit: 50 queries per user per hour (prevent accidental runaway)
- Input validation: file type check (PDF, DOCX), file size limit (50MB), virus scan before ingestion

**Layer 2 — Orchestration**
- Query type classifier: "Is this a factual lookup (find specific clause) or a comparison (does this match our MSA)?"
- Factual lookups → single RAG retrieval + generation
- Comparison queries → retrieve from both the uploaded contract and the MSA template, then compare
- Multi-step queries (e.g., "List all clauses that deviate from our standard terms") → agent loop with multiple retrieval steps

**Layer 3 — Model Gateway**
- Simple factual queries → Claude Sonnet (cost-effective, fast)
- Complex comparison and multi-step → Claude Opus (better reasoning for legal nuance)
- Routing classifier: keyword + query length heuristic (simple, fast, £0.001/query)
- Fallback: if Claude is unavailable → GPT-4o

**Layer 4 — Knowledge/Retrieval**
- Per-contract index: each uploaded contract is chunked (512 tokens, 50-token overlap) and embedded into a per-matter vector store namespace
- Shared index: MSA template and standard clause library (used for comparison queries)
- Hybrid retrieval: semantic + BM25 (a keyword relevance algorithm that scores documents by exact term frequency, complementing semantic search's meaning-based matching) keyword search (legal language has precise terms that semantic search sometimes misses)
- Reranking: cross-encoder reranker (a model that scores query-document pairs for relevance — more accurate than vector search but applied only to the top 20–50 candidates) to improve precision before sending to LLM

**Layer 5 — Data/Integration**
- Document storage: Azure Blob, organised by matter ID
- Matter metadata: contract type, counterparty, date, assigned paralegal — retrieved from matter management system
- Write-back: approved summaries and flagged clauses written back to matter record in the document management system

**Layer 6 — Observability/Governance**
- Every query and response logged with: matter ID, query, retrieved chunks, model used, response, latency, cost
- PII handling: counterparty names and specific financial terms redacted in the LLM call, re-injected into the response from the raw document after generation
- Cost tracking: per-matter, per-paralegal, monthly
- LLM judge: 10% of responses evaluated for accuracy and groundedness (did the answer come from the contract, or did the model hallucinate?)
- Audit trail: every AI-assisted response marked as "AI-assisted" in the matter record, including which document chunks were retrieved

**Latency budget:**
- Target: < 5 seconds for simple factual queries (acceptable for legal research)
- P95 breakdown: 200ms retrieval + 200ms reranking + 3,500ms LLM call + overhead = 4,200ms ✅

**Cost model:**
- 500 contracts/month × 20 queries per contract = 10,000 queries/month
- Mix: 70% standard (Claude Sonnet, ~£0.04/query) + 30% complex (Claude Opus, ~£0.25/query)
- Monthly LLM cost: (7,000 × £0.04) + (3,000 × £0.25) = £280 + £750 = **£1,030/month**
- Current cost (paralegal time): 500 contracts × 5 hours × £40/hour = **£100,000/month**
- ROI: the system pays for itself if it reduces paralegal time by 1.5%.

---

## 6. Architecture Perspective

### Decision Framework: Five Core Design Choices

Every AI system design converges on five decisions. Make these explicitly, not by default.

**Decision 1 — RAG vs Long Context vs Fine-Tune**

| Signal | Choose |
|---|---|
| Knowledge changes frequently (products, policies, prices) | RAG |
| Documents fit in 128K context and volume is low | Long context |
| Domain language is highly specialised and consistent | Fine-tune |
| All three signals present | RAG + fine-tune |

**Decision 2 — Single model vs routed model tiers**

| Signal | Choose |
|---|---|
| Query complexity is uniform and volume is low | Single model |
| Clear complexity distribution (simple/medium/complex) | Tiered routing |
| Cost is a primary constraint | Tiered routing (saves 50–70%) |
| Latency is a primary constraint | Tiered routing (faster for simple queries) |

**Decision 3 — Synchronous vs asynchronous processing**

| Signal | Choose |
|---|---|
| User expects immediate response (chat, search) | Synchronous |
| Task takes > 10 seconds (document analysis, batch) | Asynchronous + polling or webhook |
| Task involves human approval gates | Asynchronous (task queue + notification) |

**Decision 4 — Stateless vs stateful agent**

| Signal | Choose |
|---|---|
| Single-turn queries, no context continuity needed | Stateless (simplest, most scalable) |
| Multi-turn conversations | Stateful with session memory |
| Long-running tasks spanning hours or days | Stateful with durable task queue |

**Decision 5 — Evaluation strategy**

| Signal | Choose |
|---|---|
| Clear correct answers exist (structured data extraction) | Automated exact match |
| Quality is multidimensional (tone, accuracy, completeness) | LLM judge |
| Regulatory or safety-critical decisions | Human evaluation + LLM judge |
| All production systems | LLM judge + periodic human review |

### Common AI System Design Patterns

**Pattern A — RAG Q&A System**
```
Query → Retrieval → Context assembly → LLM → Response
                        ↑
              Vector DB + Document Store
```
Use when: knowledge-intensive Q&A, document search, policy lookup.

**Pattern B — Agentic Workflow**
```
Task → Orchestrator → [Plan → Tool calls → Observe] loop → Response
                              ↑
                         Tool Registry
```
Use when: multi-step tasks, cross-system workflows, tasks that require decisions.

**Pattern C — Hybrid (Recommendation + LLM)**
```
User context → Candidate retrieval (fast, collaborative/content-based)
                   → Re-ranking LLM (slow, personalised reasoning)
                   → Response with LLM-generated explanation
```
Use when: high-volume retrieval where LLM reasoning is too expensive for all candidates but valuable for the final selection.

**Pattern D — Batch Processing Pipeline**
```
Document corpus → Chunking → Embedding → Index build
                                 ↑
                        Nightly scheduled job
```
Use when: knowledge base construction, bulk document analysis, training data preparation.

---

## 7. Check Yourself (3–5 Questions)

**Question 1 — Separating orchestration from model routing**

Your team's design for a customer support AI has the orchestration logic, model routing, and LLM API calls all inside a single application service. What is the architectural risk, and how would you restructure it?

> **Detailed Answer:** Coupling orchestration to model routing means any change to the routing policy (adding a new model tier, changing fallback logic, adding a new LLM provider) requires changes to application code, testing, and redeployment. It also means there is no central point to apply cost tracking, rate limiting, or compliance logging across all LLM calls. The restructure: extract the model gateway as a separate service (or use LiteLLM/a proxy) responsible for routing, fallback, auth, cost tracking, and rate limiting. Application code talks to the gateway; the gateway manages the LLM provider relationships. This decouples application logic from model selection and gives you a single governance point.
>
> **Simple Explanation:** Without a separate model gateway, changing "which model handles which request" requires rewriting application code. With a gateway, it is a routing rule change in one place. The same reason you have an API gateway instead of every service calling every other service directly: centralised routing, centralised governance, decoupled change management.
>
> **Architecture Takeaway:** Extract the model gateway as a separate layer before writing application code, not after. Every LLM call must pass through it. This single decision gives you: model routing, fallback logic, cost tracking, rate limiting, data residency enforcement, and audit logging — all from one layer, without touching application code when any of these requirements change.

**Question 2 — Multi-tenant data isolation strategies**

You're designing a multi-tenant AI knowledge assistant that will serve 12 internal teams. Your security team requires that Team A cannot see Team B's documents in any retrieval results. What are two architectural approaches, and what are the tradeoffs?

> **Detailed Answer:** (1) Index-per-tenant — each team has a separate vector store namespace or collection. Strong isolation: a missing filter can never cause a cross-tenant data leak because the indexes are physically separate. Cost: higher storage and maintenance overhead, especially if teams have small document sets. (2) Shared index with metadata filtering — all documents share one index, each tagged with a tenant ID, every retrieval query must include a tenant ID filter. Lower cost and operationally simpler. Risk: if the tenant ID filter is accidentally omitted in a code path, it becomes a data leakage incident. Mitigation: enforce the filter at the retrieval service layer (not in application code), so no calling code can bypass it. For a security-sensitive deployment, index-per-tenant is safer; for an internal knowledge tool where data sensitivity is lower, shared index with enforced filtering is acceptable.
>
> **Simple Explanation:** Index-per-tenant is separate filing cabinets — even if you forget to lock one, documents from different cabinets cannot mix. Shared index with filtering is one big filing cabinet with colour-coded tabs — cheaper, but if someone forgets to check the colour code, documents can be seen by the wrong team.
>
> **Architecture Takeaway:** For sensitive data, prefer index-per-tenant — the isolation is structural, not dependent on filter correctness in every code path. For lower-sensitivity internal tools, shared index with retrieval-layer-enforced filtering is acceptable. Never enforce tenant filters in application code — enforce them in the retrieval service so they cannot be bypassed by any calling service.

**Question 3 — Latency budget design for a 2-second SLA**

Walk through how you would design the latency budget for a customer-facing AI chat feature with a 2-second P95 SLA requirement.

> **Detailed Answer:** Start with the total budget (2,000ms) and work backward by subtracting the irreducible costs: client/network round trip (~150ms), response processing (~50ms), leaving ~1,800ms for the AI processing path. The LLM call at P95 for a standard model (GPT-4o/Claude Sonnet) is 1,200–1,800ms. If the LLM call alone consumes the full budget, there is nothing left for retrieval, context assembly, or any tool calls. Design response: (1) use streaming to improve perceived latency — user sees first tokens in 400ms even if full response takes 2s; (2) semantic cache for repeated similar queries — eliminates the LLM call entirely for ~10% of traffic; (3) route simple queries to a nano model (200–500ms vs 1,500ms for premium models); (4) keep retrieval under 150ms by ensuring the vector database is co-located with the application. A realistic budget: 150ms network + 80ms intent classification + 150ms retrieval + 50ms context assembly + 1,300ms LLM call + 270ms buffer = 2,000ms P95.
>
> **Simple Explanation:** Work backward from the total budget: subtract what you cannot control (network, auth), then check what the LLM call alone costs at P95. If that leaves nothing for retrieval and tool calls, you need to either use a faster model, add caching, or renegotiate the SLA. The budget is a constraint you design to, not a hope you discover was wrong at launch.
>
> **Architecture Takeaway:** Latency budget design is a component specification exercise. The output is not "we will try to be fast" — it is "retrieval: P95 < 150ms, LLM call: P95 < 1,300ms, intent classification: < 80ms." These specs drive component selection. Discover the mismatch at design time, not in production.

**Question 4 — Business case for tiered model routing**

A product manager asks why you're proposing to add a model routing layer when "we could just always use GPT-4o." Make the business case for tiered model routing.

> **Detailed Answer:** The business case is cost and latency, not capability. At scale, 60–70% of queries in most enterprise AI systems are simple: intent classification, FAQ lookups, basic summarisation, short Q&A. A nano model (GPT-4o-mini, Claude Haiku) handles these at £0.10–0.20/million tokens with sub-second latency. GPT-4o costs £2–3/million tokens and takes 1.5–3 seconds. If you run 100K queries/day and 65% are simple: without routing, cost is ~£250/day at GPT-4o rates. With routing (65% nano, 35% standard), cost drops to ~£80/day — saving £62,000/year at this volume. Latency for simple queries drops from 1.5s to under 0.5s. The complexity added (routing classifier + gateway layer) is a one-time engineering cost that pays back in weeks.
>
> **Simple Explanation:** You do not send a senior partner to answer every question a client asks — you have a receptionist for simple routing, a junior for standard work, and a partner for complex matters. The billing rates are different and the quality of the answer is indistinguishable at the tier it belongs in. AI model tiering is the same principle.
>
> **Architecture Takeaway:** On 100K queries per day, routing 65% to nano models saves approximately £62,000 per year with no user-facing quality difference for correctly-routed queries. The routing classifier is a one-time engineering investment that pays back in weeks. Design this in at the model gateway layer — adding it later requires touching both routing and application code.

**Question 5 — PII pseudonymisation before LLM API calls**

Your AI document analysis system processes uploaded PDFs. A security review flags that supplier names, contract values, and counterparty addresses are being sent verbatim to a third-party LLM API. What architectural change addresses this?

> **Detailed Answer:** Implement PII detection and pseudonymisation in the context assembly layer (Layer 2 / Orchestration), before the context is sent to the model gateway and LLM. The pattern: (1) run a PII detector over the assembled context (Microsoft Presidio, AWS Comprehend, or a fine-tuned classifier); (2) replace detected PII with placeholder tokens (COUNTERPARTY_1, CONTRACT_VALUE_USD_1, ADDRESS_1); (3) store the mapping of placeholder → real value in a session-scoped lookup; (4) after the LLM returns its response, run a reverse substitution pass — replace placeholders with real values in the output. The LLM only ever sees the pseudonymised version. This pattern also has a secondary benefit: it prevents the LLM from "remembering" sensitive business information across calls, and it simplifies your data processing agreement with the LLM provider (you can argue no personal data is transmitted).
>
> **Simple Explanation:** Replace "Supplier: Acme GmbH, contract value: €2.4M" with "Supplier: COUNTERPARTY_1, contract value: CONTRACT_VALUE_1" before sending to the LLM, keep the mapping locally, and re-substitute in the response. The LLM does its reasoning job on anonymised tokens; your system handles the real values. The LLM provider never sees the sensitive data.
>
> **Architecture Takeaway:** PII pseudonymisation belongs in the context assembly layer (Layer 2), applied to every context before it reaches the model gateway. It must be designed in as a standard pipeline step, not added as a special case. Secondary benefits: simplified DPA with LLM providers (no personal data transmitted), and no cross-call information leakage from the model's context.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section goes further for architects who want to understand the mechanisms in detail. It is safe to skip on a first pass and return here later.

### 8.1 The FRAME Design Framework

When designing any AI system (or presenting a design in a review), use the **FRAME** structure to ensure completeness:

**F — Functional requirements**
What must the system do? Be specific: who are the users, what tasks do they perform, what are the inputs and outputs, what is the volume and frequency?

**R — Reliability and scale**
What are the SLAs? What is the expected volume now and in 12 months? What are the peak-to-average ratios? What happens when a component fails?

**A — Architecture decisions**
Which of the five core design choices (RAG vs fine-tune, single vs tiered models, sync vs async, stateless vs stateful, evaluation strategy) apply, and what did you choose and why?

**M — Monitoring and evaluation**
How do you know the system is working? What quality signals do you track? What are the alert thresholds? How does the feedback loop work?

**E — Economics**
What does this cost at current volume? At 10× volume? What are the cost drivers? What happens to unit economics as you scale?

**FRAME applied to the Legal Document Q&A example:**

| Component | Answer |
|---|---|
| Functional | 500 contracts/month, paralegals ask factual and comparison questions, 5-second SLA, internal only |
| Reliability | 99.5% availability during business hours, fallback to Claude if primary unavailable, async for batch analysis |
| Architecture | RAG (knowledge changes per contract), tiered routing (standard for lookup, premium for comparison), synchronous for queries, LLM judge for eval |
| Monitoring | OTel traces, 10% LLM judge sampling, cost per matter, retrieval precision alerts |
| Economics | £1,030/month LLM cost vs £100K/month paralegal cost — 97% cost reduction on AI-assisted queries |

### 8.2 High-Volume Hybrid: Recommendation + LLM

A common enterprise pattern: you have a high-volume retrieval system (e.g., product search, content recommendation) where LLM reasoning adds value but is too expensive to run on all candidates.

**The two-stage hybrid pattern:**

**Stage 1 — Candidate retrieval (fast, cheap)**
Traditional ML or vector search retrieves top-N candidates.
- Collaborative filtering: "users like you also bought..."
- Semantic search: "products semantically similar to this query"
- BM25 keyword: exact term matching for product names and SKUs
- Cost: < £0.001/query, < 50ms

**Stage 2 — LLM re-ranking and explanation (slow, expensive — applied to top N only)**
LLM takes the top 10–20 candidates from Stage 1 and applies reasoning:
- Personalisation: "given this customer's purchase history and stated preferences, reorder these 10 products"
- Explanation generation: "why is this product the top recommendation?"
- Filter application: "remove any candidates that violate the customer's stated constraints"
- Cost: £0.02–0.10/query (10 candidates × ~500 tokens each)

**Key design principle:** never run the LLM on the full candidate space. Always use a cheap retrieval stage to filter to a manageable set first.

```
10M product catalogue
    │
    ▼
Stage 1: Vector search + collaborative filter → top 20 candidates (< 50ms, < £0.001)
    │
    ▼
Stage 2: LLM reranker on 20 candidates → top 5 with explanations (1,500ms, ~£0.05)
    │
    ▼
Response to user: top 5 products with personalised explanations
```

### 8.3 Cost Math: Unit Economics at Scale

Before any AI system design is approved, you need the unit economics model. The standard calculation:

```
Daily cost = (queries/day) × (avg tokens/query) × (cost per 1K tokens)

Example: customer service assistant
  - 50,000 queries/day
  - Average: 800 input tokens + 200 output tokens = 1,000 tokens
  - Model: Claude Sonnet at £1.50/1M input, £6.00/1M output
  - Input cost: 50,000 × 800 / 1,000,000 × £1.50 = £60/day
  - Output cost: 50,000 × 200 / 1,000,000 × £6.00 = £60/day
  - Total: £120/day = £3,600/month = £43,800/year
```

**Cost levers to present in a design review:**

| Lever | Typical saving | Tradeoff |
|---|---|---|
| Tiered routing (nano for 60%) | 50–70% | Engineering complexity |
| Prompt caching | 20–40% | Static prompt structure required |
| Semantic caching | 10–15% | Cache infrastructure needed |
| Shorter system prompt | 5–10% | May reduce quality |
| Output length limits | 10–20% | May truncate useful responses |
| Chunking optimisation | 15–30% (RAG) | Affects retrieval quality |

---

## 9. Key Takeaways (5 Bullets)

- **AI system design is about making the hard decisions before code is written.** Model choice, routing strategy, caching approach, fallback architecture, multi-tenancy model — these decisions are expensive to reverse. Design time is when they cost nothing to change.

- **The 6-layer architecture separates concerns that must not be coupled.** Surface, orchestration, model gateway, knowledge, data, and observability are each a distinct responsibility. Collapsing layers — especially coupling orchestration with model routing — creates systems that are expensive to change and impossible to govern centrally.

- **Cost is a design variable, not a post-launch discovery.** Model tiering (routing simple queries to cheap models) typically saves 50–70% compared to using the most capable model for everything. Run the unit economics calculation before the system is built, not after the first invoice arrives.

- **Latency budget must be designed in, not hoped for.** Work backward from the SLA: subtract network, subtract processing overhead, what's left is your LLM + retrieval budget. If the remaining budget is smaller than the P95 latency of your chosen model, you need a different model, a caching strategy, or a different SLA negotiation — not an optimistic assumption.

- **Fallback architecture is not optional for production systems.** LLM API uptime is 99.5–99.9% — that's 4–44 hours of downtime per year. Design the primary → secondary model fallback, graceful degradation, and circuit breaker patterns before launch. Discovering you have no fallback during a production outage is the worst time to design one.

---
**Recommended next modules:** [RAG & Vector](AI_Gita_Transformed_RAG_Vector.md) (retrieval patterns) → [Agents & Prompting](AI_Gita_Transformed_Agents_Prompting.md) (agentic architecture) → [AI Infrastructure](AI_Gita_Transformed_AIInfrastructure.md) (cost and serving decisions).
