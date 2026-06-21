# Agentic Platform — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

**What is an LLM?** An LLM (Large Language Model) is a software service — accessible via an API — that takes text as input and produces text as output. It has no database connection, no memory between calls, and no ability to take actions in external systems by default. You call it like any other API: send a request (your prompt), receive a response (the generated text). GPT-4o, Claude, and Gemini are examples. That is the entirety of what an LLM is on its own.

**What this module is about:** An Agentic Knowledge Platform is the enterprise infrastructure layer that transforms an LLM — which on its own can only read text and write text — into a system that can take actions, access your data, coordinate with other AI agents, remember past interactions, and do all of this safely under your governance and compliance framework. This module teaches you how to design that infrastructure.

A single LLM is like a very smart consultant who can only answer questions by talking — no phone, no laptop, no access to your systems, no memory of the last meeting.

An **AI agent** gives that consultant a phone, a laptop, access to your systems, and a notebook. It can now look things up, run calculations, call APIs, read emails, write files, and remember what happened last week.

An **Agentic Platform** is the enterprise infrastructure that makes this safe, manageable, and scalable. Instead of each team building their own ad hoc agent setup with hardcoded API keys and no governance, an agentic platform provides:

- A shared **model gateway** — one front door to all LLMs (GPT-4o, Claude, Gemini, open-weight models), with authentication, rate limiting, cost tracking, and routing
- A **tool registry** — a managed catalogue of capabilities agents can call (APIs, databases, search, code execution), with access control for who/what can invoke which tools
- A **memory system** — working memory (what the agent holds in its active context right now) for within-conversation context, episodic memory (what the agent remembers from past conversations or sessions) for cross-session recall, semantic memory (general knowledge the agent has been given about your organisation or domain) for knowledge retrieval
- A **governance layer** — audit trails, guardrails, policy enforcement, budget caps, and compliance controls
- An **orchestration runtime** — the engine that runs the agent loop (think → act → observe → repeat) reliably at production scale

> **What is RAG?** RAG (Retrieval-Augmented Generation) means: instead of relying on the model's built-in training knowledge, you retrieve relevant documents from your own systems at query time and feed them to the model alongside the question. The model answers from *your data*, not from what it memorised during training. Think of it as giving the model a cheat-sheet of relevant pages from your internal wiki before asking it a question.

If a RAG pipeline is a research assistant who fetches documents, an agentic platform is the entire enterprise infrastructure that lets many research assistants work across all your systems without each one being a security risk or a cost center no one can track.

---

## 2. Why Should I Care

### For Solution Architects

You're being asked to evaluate or design systems where AI doesn't just answer questions — it takes actions. "Summarise this document" is a query. "Review this contract, extract the key risks, look up our internal policy for each risk, and draft a response email" is an agentic workflow.

The moment AI takes actions, the design questions change completely:

- **Authorization:** which systems can the agent call, with what permissions, on behalf of whom?
- **Blast radius:** if the agent makes a mistake (and it will), what's the maximum damage? A hallucinated summary is recoverable. An erroneous order cancellation or a misdirected email is not.
- **Observability:** how do you trace what an agent did and why — across 12 tool calls that happened in 8 seconds?
- **Cost control:** an agent that loops unexpectedly can make 500 LLM calls in a minute. Without budget caps, that's an unplanned bill.

An agentic platform is how you answer all of these questions with infrastructure rather than per-project point solutions.

### For Enterprise Architects

Agentic systems are the first AI pattern that crosses your entire integration estate. A single agent may touch your CRM, your OMS, your ERP, your knowledge base, your email system, and your analytics platform — all in one workflow. This is different from any previous enterprise AI integration.

The **Agent Knowledge Platform (AKP)** — the reference architecture framework for agentic systems — uses a 6-plane model to decompose this complexity into governable layers. Each plane maps to something you already have in your integration architecture: identity, API gateway, message bus, data platform, knowledge store, and observability stack. The AKP doesn't replace those — it organizes how AI agents interact with them.

---

## 3. Think About It Like This (Analogy)

**The Enterprise Help Desk Analogy**

Imagine you're running a large enterprise help desk for a retail company. You have employees (agents) who handle customer issues. Here's what the infrastructure looks like:

- **The phone switchboard (Model Gateway):** Every incoming call goes through the switchboard. It routes calls to the right employee, logs the call, and enforces "no calls after 10pm." No employee has a direct line that bypasses the switchboard.

- **The tool cabinet (Tool Registry):** Employees can look up orders in the OMS, issue refunds, schedule callbacks, and escalate tickets. But not every employee can issue a refund — there's a permissions matrix. The cabinet is locked; employees sign out tools based on their role.

- **The case notes system (Memory):** When a customer calls back, the employee can pull up notes from the last call (episodic memory), search the knowledge base for known issues with that product (semantic memory), and see what they've already tried this call (working memory).

- **The supervisor layer (Governance):** Certain actions — refunds over $500, account closures, data deletions — require a supervisor sign-off before they go through. There's an audit log of every action taken. Monthly cost reports show which teams are making the most calls.

- **The call routing engine (Orchestration Runtime):** The system that manages the queue, assigns calls to available employees, handles escalations, retries dropped calls, and ensures no single employee gets overwhelmed.

Now replace "employees" with "AI agents," replace "phone calls" with "LLM invocations," and replace "customers" with "enterprise users or automated workflows." That's an Agentic Platform.

The key insight: **you already know how to build this infrastructure.** API gateways, identity systems, audit logs, role-based access control, message queues, observability stacks — these are not new problems. The AKP is a framework for applying your existing enterprise patterns to AI agents.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 What is Agent Core? (Start Here)

Before understanding the platform, understand what an agent is at its simplest.

An **Agent Core** is a loop:

```
1. Receive task or user message
2. Think: call the LLM with the current context
3. Decide: is the answer ready, or do I need to use a tool?
4. Act: if a tool is needed, call it and get the result
5. Observe: add the tool result to context
6. Loop: back to step 2 with the updated context
7. Respond: when the LLM produces a final answer, return it
```

This is the **ReAct pattern** (Reasoning + Acting): the agent alternates between reasoning (LLM thinking) and acting (tool calls), with each action informing the next round of reasoning.

A simple example — "What's the status of order #12345 and is there a delay risk?":
1. LLM reasons: "I need to look up order #12345."
2. Agent calls: `OMS_API.get_order(id=12345)` → returns order details and estimated ship date
3. LLM reasons: "The ship date is in 2 days. I should check carrier capacity."
4. Agent calls: `logistics_API.get_carrier_capacity(carrier="FedEx", date="2026-06-23")` → returns current delay flag
5. LLM reasons: "Carrier shows 2-day delay. I can now answer the question."
6. Agent responds: "Order #12345 is in warehouse. FedEx currently has a 2-day delay on your zone — estimated delivery is June 25th instead of June 23rd."

This took 2 tool calls, 3 LLM invocations, and 8 seconds. Without the platform, each team would implement this loop differently. With the platform, this is a repeatable, governed, observable pattern.

### 4.2 The AKP Six-Plane Architecture

The **Agent Knowledge Platform (AKP)** organizes the agentic infrastructure into six planes. Think of these as six layers of governance and capability, not six separate systems:

> **Explain Like I'm an Architect**
>
> Six planes sounds like six new things to build. It isn't. Every plane maps to something you already have — the AKP just gives it an AI-specific face.
>
> | AKP Plane | What it is in your existing stack |
> |---|---|
> | Surfaces | Your existing web/mobile/API entry points, extended to accept agent task requests |
> | Agent Runtime | Your existing job queue / async worker infrastructure (Celery, Azure Service Bus workers, etc.) |
> | Tool Plane | Your existing API gateway, with a tool registry layer added on top |
> | Knowledge Plane | Your existing vector database (new) + your existing document/data stores (existing) |
> | Governance Plane | Your existing SIEM/audit log + IAM, extended to understand LLM-specific events |
> | Data Backbone | Your existing message bus and data platform |
>
> The new investment is the **AI-specific layer** on top: model gateway, tool registry, knowledge plane, and the governance extensions that understand LLM behaviour. You are not replacing your enterprise stack — you are extending it. Architects who approach AKP as a new greenfield platform instead of an extension of existing infrastructure overengineer it and create unnecessary complexity.

**Plane 1 — Surfaces**
The user-facing entry points: chat interfaces, API endpoints, embedded widgets, voice channels, CLI tools. This is where users or automated workflows initiate agent tasks. Each surface authenticates the caller and translates the request into a standard agent invocation.

**Plane 2 — Agent Runtime**
The execution environment for the Agent Core loop. Manages the lifecycle of agent tasks: spawning, scheduling, timeout handling, retries, and parallelism. If you have multiple agents running concurrently (a manager agent delegating to specialist sub-agents), the runtime coordinates them.

**Plane 3 — Tool Plane**
The managed registry of capabilities agents can invoke. Each tool entry specifies: what the tool does, what parameters it accepts, who/what is authorized to call it, rate limits, and how to handle errors. Tools include: REST API calls, database queries, code execution sandboxes, browser automation, file system operations, email/calendar integrations.

**Plane 4 — Knowledge Plane**
The memory and retrieval layer: vector stores for semantic search, document stores for raw retrieval, graph databases for relationship-aware queries, caches for frequently accessed context. This is what allows agents to "know things" beyond what's in their training data and what's in the current conversation.

**Plane 5 — Governance Plane**
Policy enforcement, guardrails, audit logging, budget management, compliance controls. Every LLM call and every tool call passes through governance before execution. This is where you enforce: PII redaction, content filters, action whitelisting, budget caps, GDPR-relevant data handling, and EU AI Act transparency requirements.

**Plane 6 — Data Backbone**
The underlying data infrastructure: message queues, event streams, data pipelines that connect the agent platform to your enterprise data systems. This plane ensures that agents work from current, consistent data — not stale snapshots.

### 4.3 The Model Gateway

The **Model Gateway** is the single front door to all LLMs in your organization. It sits between every agent (and every application) and the LLM providers.

> **What is a token?** A token is the basic unit of text that LLMs process — and the unit that APIs charge for. Roughly 3–4 characters or 0.75 words in English. "Hello world" = 2 tokens. 1,000 tokens ≈ 750 words ≈ 1.5 pages. APIs charge separately for **input tokens** (your prompt) and **output tokens** (the model's response). When you see pricing like "$2 per million tokens", that is the cost per million of these text chunks.

What it provides:
- **Authentication & authorization:** which teams, agents, and applications can call which models
- **LLM routing:** send cost-sensitive tasks to cheaper models (GPT-3.5, Claude Haiku), high-stakes tasks to frontier models (GPT-4o, Claude Opus), and latency-sensitive tasks to self-hosted open-weight models
- **Rate limiting:** prevent any single agent or team from exhausting API quotas
- **Cost tracking:** per-team, per-agent, per-workflow token usage — essential for internal chargeback and budget governance
- **Observability:** every LLM call is logged with input, output, latency, tokens used, and model version — for debugging, auditing, and fine-tuning data collection
- **Fallback routing:** if GPT-4o is unavailable, automatically route to Claude — without any application code change

Without a model gateway, you have teams independently managing API keys, no unified cost visibility, and no single place to apply governance policies.

### 4.4 The Tool Registry and MCP

The **Tool Registry** is the catalogue of everything an agent is allowed to do. Each entry is a tool definition:

```json
{
  "name": "cancel_order",
  "description": "Cancel an order in the OMS. Use only when the customer has explicitly confirmed cancellation.",
  "parameters": { "order_id": "string", "reason": "string" },
  "authorization": ["customer_service_agent", "supervisor_agent"],
  "rate_limit": "10 per minute",
  "requires_confirmation": true,
  "audit_log": "mandatory"
}
```

**MCP (Model Context Protocol)** is an open standard (Anthropic, 2024) for how agents discover and invoke tools. It defines a standard interface so that tools built once can be used by any agent, regardless of which LLM framework or orchestration engine is running. Think of it as "USB-C for agent tools" — a standard plug that works across different device brands.

**MCP Gateway vs Direct Tool Call:**

| | Direct Tool Call | MCP Gateway |
|---|---|---|
| Discovery | Hardcoded in agent | Dynamic — agent queries registry |
| Auth | Per-tool, per-agent | Centralized gateway enforces policy |
| Versioning | Manual updates per agent | Registry manages versions |
| Observability | Each tool logs separately | Gateway logs all tool traffic |
| Use case | Simple, one-off agents | Production, multi-team, enterprise |

### 4.5 The Agent Request Flow (End to End)

```
User / Workflow initiates task
        │
        ▼
  Surface (chat UI, API, workflow trigger)
  → authenticates user, packages request
        │
        ▼
  Agent Runtime
  → creates agent task, allocates budget, starts timeout clock
        │
        ▼
  Agent Core Loop:
  ┌─────────────────────────────────────────┐
  │  1. Build context (working memory +     │
  │     retrieved knowledge from Plane 4)   │
  │  2. Call Model Gateway → LLM            │
  │     (Governance Plane checks policy)    │
  │  3. Parse LLM output:                   │
  │     - Tool call? → Tool Plane via MCP   │
  │       (auth check, rate limit, execute) │
  │     - Final answer? → exit loop         │
  │  4. Add tool result to context          │
  │  5. Repeat                              │
  └─────────────────────────────────────────┘
        │
        ▼
  Governance Plane (post-execution)
  → audit log, cost record, policy check on output
        │
        ▼
  Response to user / downstream system
```

**What an architect controls at each boundary:**
- Surface → Runtime: authentication, request schema, SLA
- Runtime → Model Gateway: model selection policy, budget cap
- Model Gateway → LLM: provider contracts, data residency
- Agent Core → Tool Plane: authorization matrix, blast radius controls
- Governance: what gets logged, what gets blocked, what triggers human review

### 4.6 AKP vs Traditional API Architecture

This is the comparison that helps architects map the new to the familiar:

> **Explain Like I'm an Architect**
>
> In every enterprise system you've designed, the application is in charge. You write code that says "call the OMS API, then call the payment API, then update the CRM." The sequence is fixed in your code. If something unexpected happens, your explicit error handling runs. You know exactly what will happen and in what order because you programmed it.
>
> In an agentic system, the LLM is in charge of the sequence. You give it a task and a toolbox. It decides which tools to call, in which order, based on what each tool returns. The sequence is not in your code — it emerges at runtime from the model's reasoning. This is fundamentally different from anything in your existing integration portfolio.
>
> **The implication:** your traditional governance controls (code review, static analysis, pre-approved API call sequences) do not apply to agentic systems. The only governance controls that work are runtime ones — the platform mechanisms that intercept each LLM call and each tool call as it happens. This is why the Governance Plane is not optional infrastructure: it is the only place where you can enforce policy in a system whose behaviour you cannot predict at design time.
>
> **Common Misconception:** "We can just add guardrails to the prompt." Prompt-based restrictions can be bypassed by clever user inputs (prompt injection) or degraded by model updates. Runtime governance controls — enforced by the platform, not by the model — are the only reliable backstop.

| Traditional API Integration | Agentic Platform (AKP) |
|---|---|
| Request is deterministic — same input, same output | Request is non-deterministic — LLM reasoning varies |
| Action sequence is hardcoded in application logic | Action sequence is decided by LLM at runtime |
| API calls are explicit, pre-approved in design | Tool calls are dynamic, chosen by the agent |
| Error handling is explicit try/catch | Errors may be silently absorbed into LLM context |
| Audit log captures what happened | Audit log must capture *why* (LLM reasoning trace) |
| Cost is fixed per operation | Cost is variable (number of LLM calls is runtime-determined) |
| Permissions are per application | Permissions are per agent, per tool, per context |

The critical architectural shift: in a traditional integration, the application is in control. In an agentic platform, the LLM is in control of the action sequence — and the platform's governance layer is your only check on that.

---

## 5. Enterprise Example

**Scenario: Customer Return Resolution at a Retail Company**

Customer contacts support: "I ordered 3 pairs of shoes last week, two arrived but one is missing from the box. I want a refund."

**Without an agentic platform (traditional flow):**
Support agent logs into OMS, searches for the order, checks the manifest, cross-references the warehouse scan log, checks the return policy for the item category, creates a refund ticket, and emails the customer. 12–20 minutes of manual work.

**With an agentic platform:**

An AI agent receives the message, and the following tool calls happen automatically:

1. `OMS.get_customer_orders(customer_id)` → finds 3 orders from last 7 days, identifies the relevant order
2. `OMS.get_order_details(order_id)` → sees 3-item order, all 3 items shipped as one parcel
3. `warehouse.get_scan_log(parcel_id)` → sees parcel was scanned as 2.1kg at dispatch; expected weight for 3 pairs is 3.2kg — discrepancy flagged
4. `policy_engine.get_return_policy(item_category="footwear", channel="ecomm")` → returns: eligible for refund without return for items under £150
5. `OMS.create_refund(order_id, item_id, reason="missing_item", amount=79.99)` → creates refund
6. `comms.send_email(customer_id, template="missing_item_refund", amount=79.99)` → sends confirmation

Total: 6 tool calls, ~15 seconds, zero human involvement for this standard case.

**Governance controls in this flow:**
- The `create_refund` tool has a limit: refunds over £200 require human approval — a supervisor agent is notified
- Every tool call is in the audit log with the LLM reasoning trace that triggered it
- The customer's PII (name, address) is redacted in the LLM call — the agent works with IDs, not raw personal data
- Budget cap: if the agent exceeds 20 LLM calls on a single ticket, it escalates to a human — looping prevention

**What you design as an architect:**
- The tool registry (which tools exist, who can call them, what limits apply)
- The authorization matrix (which agent roles can invoke which tools)
- The escalation thresholds (refund limit, loop count, cost cap)
- The observability schema (what gets logged for compliance vs. what gets logged for debugging)

---

## 6. Architecture Perspective

### The Blast Radius Problem

Every tool call an agent makes carries risk. The blast radius principle: **design tools so that mistakes are reversible and scoped**.

| Tool | Reversible? | Scope | Design implication |
|---|---|---|---|
| `search_knowledge_base()` | Yes | Read-only | No special controls needed |
| `get_order_status()` | Yes | Read-only | No special controls needed |
| `create_refund()` | Partially (within SLA) | Financial action | Amount limit, audit log, human threshold |
| `send_email()` | No | External communication | Requires confirmation template, no bulk |
| `cancel_order()` | No (if already shipped) | Supply chain action | Requires explicit confirmation |
| `delete_customer_data()` | No | Irreversible | Human approval mandatory, regulatory log |

**Design rule for architects:** tools that have side effects in external systems should be explicitly flagged in the registry as requiring pre-execution policy checks. The governance plane intercepts these calls and applies the appropriate controls.

### Multi-Agent Patterns

In complex workflows, a single agent is not enough. The AKP supports **multi-agent orchestration**:

**Orchestrator + Specialist pattern:** A manager agent decomposes the task and delegates to specialist agents (one for OMS queries, one for logistics, one for customer communications). Each specialist has a narrower tool permission set, reducing blast radius.

**Parallel agents:** Multiple agents work independently on sub-tasks simultaneously (e.g., one checks order status while another checks carrier status), then the results are merged.

**Agent-to-Agent (A2A) protocol:** The emerging standard (Google, 2024) for how agents discover and delegate to other agents — this enables a manager agent to discover and delegate to specialist agents dynamically, rather than hardcoding which sub-agents exist. Analogous to MCP for tools — a standard interface for agent-to-agent communication.

```
Manager Agent
     │
     ├── Order Agent (OMS tools only)
     ├── Logistics Agent (carrier API tools only)
     └── Comms Agent (email/SMS tools only, no read access to order data)
```

This pattern **limits blast radius at the agent level** — no single agent has broad permissions across all systems.

### Fitting AKP Into Your Existing Enterprise Stack

```
Existing Enterprise                    AKP Layer
─────────────────                      ──────────
API Gateway        ←── Model Gateway (extends)
Identity / IAM     ←── Agent Authorization (integrates)
Message Bus        ←── Agent Runtime queue (uses)
Data Platform      ←── Knowledge Plane / Data Backbone (feeds)
SIEM / Audit       ←── Governance Plane logs (feeds)
Observability      ←── OTel traces from every LLM + tool call (extends)
```

The AKP is not a replacement for your enterprise stack — it's an extension that adds the AI-specific layer on top of what you already have.

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — Direct database access**

Your engineering team proposes giving a customer service agent direct database write access "because it's simpler than going through the API." What is the architectural objection?

> **Simple Explanation:** "Direct database access is simpler" is the same argument as "we'll skip the API gateway because it's faster." You wouldn't do that for human-operated systems. Don't do it for AI agents — especially since AI agents can make wrong decisions with high confidence, at high speed, repeatedly, before anyone notices.
>
> **Detailed Answer:** Direct database write access bypasses every governance control that the tool registry provides. If the agent miscalculates a refund amount, receives malformed LLM output, or is manipulated by a prompt injection attack, it can corrupt database records directly — with no authorization check, no amount limit, no audit trail, and no human intervention point. The tool registry enforces: authorization (only the right agents can invoke the right tools), rate limits (preventing runaway tool calls), amount limits (refunds above £200 require supervisor approval), audit logging (every write is recorded with the LLM reasoning that triggered it), and blast radius controls (the tool can be disabled without changing agent code). "Simpler" at the integration layer trades development convenience for operational risk across all of these dimensions. The principle: all agent actions affecting external systems go through the managed tool registry, always.
>
> **Architecture Takeaway:** The tool registry is not just an abstraction layer — it is the primary blast radius control for agentic systems. Every tool that can change state in an external system must go through it. The registry is where authorization, rate limits, and audit happen. Without it, governance is impossible.

---

**Question 2 — Runaway agent cost control**

An agent designed to handle 1 LLM call per ticket unexpectedly makes 400 LLM calls in a minute. What platform controls should prevent or catch this?

> **Simple Explanation:** A runaway agent is like a process that gets stuck in an infinite loop — except it costs money per iteration and may be taking real actions (sending emails, modifying records) each time around. You need an automatic circuit breaker that stops it before it runs up a large bill or causes widespread data corruption. Budget caps, loop detection, timeouts, and API rate limits are the four circuit breakers. All four are needed.
>
> **Detailed Answer:** Four layers of control: (1) **Per-agent budget caps in the Governance Plane** — trigger an alert and halt the agent after N calls or £X cost within a rolling time window. This is the primary financial control. (2) **Loop detection in the Agent Runtime** — if the agent is calling the same tool with identical arguments repeatedly, it is stuck in a loop; the runtime detects this (e.g., same tool call signature seen 3+ times) and escalates to human review or terminates the task. (3) **Task-level timeout** — no single agent task should execute beyond a configured maximum wall-clock time (e.g., 60 seconds); this prevents a single stuck task from consuming resources indefinitely. (4) **Rate limits on the Model Gateway** — per-agent token-per-minute rate limits prevent runaway consumption at the API level, even if the task-level controls fail. These four controls are complementary and should all be in place — any single control can be bypassed by edge cases; defence in depth is appropriate.
>
> **Architecture Takeaway:** Cost and loop controls are not monitoring features — they are safety mechanisms that must be active on every agent task from day one. Define these limits during agent design (not after the first runaway incident): max steps per task, max cost per task, loop detection threshold, task timeout. These limits belong in the agent configuration registry alongside the tool permissions.

---

**Question 3 — MCP value proposition**

What is the Model Context Protocol (MCP) and why does it matter for enterprise architecture?

> **Simple Explanation:** MCP is "USB-C for agent tools." Before USB-C, every device had its own charger. After USB-C, one cable works everywhere. Before MCP, every agent team rebuilds the same integrations. After MCP, tools are built once and shared. The cost saving compounds with every new agent that joins the enterprise.
>
> **Detailed Answer:** MCP is an open standard interface for how agents discover and invoke tools. It defines a standard contract (tool name, description, parameter schema, authentication requirements) so a tool built once can be used by any agent, regardless of which LLM framework, orchestration engine, or model provider is running. **Before MCP:** each agent team builds its own integration to each enterprise system — five teams building five agents each needing OMS access means five separate OMS integrations, each with its own authentication, error handling, and documentation. At 10 teams × 20 enterprise systems = 200 point-to-point integrations. **After MCP:** build the OMS MCP server once, register it in the tool registry, and all agents use the same integration. 20 enterprise systems, regardless of agent count. The economics shift from O(agents × systems) to O(systems). The governance economics are equally important: one integration point means one place to enforce authentication, rate limiting, audit logging, and blast radius controls.
>
> **Architecture Takeaway:** MCP-compatible tool development is infrastructure investment, not application code. Prioritise building MCP servers for your highest-traffic enterprise systems (OMS, CRM, knowledge base, email) early. Every subsequent agent benefits from tools already built. Treat MCP tool development with the same governance rigour as API development — versioning, documentation, access control, and breaking-change policy.

---

**Question 4 — Audit requirements for agentic actions**

Your legal team asks: "If an agent made a wrong decision that resulted in a customer being incorrectly charged, can we trace why?" What does the audit architecture need to provide?

> **Simple Explanation:** Traditional audit logs say "record X was updated at 14:32 by agent-007." That's sufficient for a database operation where the logic is in code you can read. For an agent, the logic was in the LLM's reasoning — which only existed for a moment during the call. If you don't capture that reasoning at the time it happened, it's gone. The audit log must capture the reasoning, not just the action.
>
> **Detailed Answer:** The audit log must capture the complete chain of reasoning, not just the final action. Required: (1) the full input to the LLM invocation that triggered the decision (system prompt, conversation history, retrieved context at that moment); (2) the LLM's reasoning output — the "thought" the model produced before the tool call; (3) the specific tool call made, including all parameters; (4) the tool response; (5) the final decision output. This is a chain-of-reasoning trace — not just "the agent called create_charge()" but "the agent called create_charge() because it reasoned that condition X was met, based on data it retrieved from tool Y." Standard application logs capture the what. Agentic audit logs must capture the why. OpenTelemetry (OTel) extended to cover LLM spans is the current production standard for this. Each LLM call and each tool call produces a trace span that, together, reconstruct the agent's complete decision path.
>
> **Architecture Takeaway:** Implement OTel tracing with LLM span extensions from the start of any agentic deployment. This is not a future optimisation — legal and compliance requirements around AI decision traceability are active and growing. The cost of adding tracing retroactively (retrofitting instrumentation across a live agentic system) is high. Build it on day one.

---

**Question 5 — Agentic vs traditional error handling**

How does an agentic platform differ from a traditional API integration when it comes to error handling, and what does this mean for your operations team?

> **Simple Explanation:** With a traditional API, when something goes wrong it throws an error and you know about it. With an agent, when something goes wrong it might just quietly produce the wrong answer and call itself done. Your monitoring systems are watching for error codes that never fire. You need a completely different monitoring approach that watches for behavioural anomalies, not just technical failures.
>
> **Detailed Answer:** In traditional API integration, errors are explicit and structured: an exception is thrown, a catch block handles it, the error is logged with a standardised code, and alerts fire on known patterns. The system either succeeds or fails with a defined error state. In an agentic system, errors can be silently absorbed: the LLM may receive a tool error, reason that it can work around it, and continue — producing a confidently wrong answer without surfacing any error to the calling system. Or the LLM may misinterpret ambiguous tool output, reach a wrong conclusion, and proceed. There is no exception thrown; the system reports "success" with incorrect output. **For operations teams:** the monitoring mental model shifts from reactive error-rate dashboards to proactive behavioural anomaly detection: unexpected tool call sequences, unusual latency profiles, budget spikes, output confidence mismatches, and RAGAS-style quality degradation monitoring. Human-in-the-loop escalation for high-stakes actions is the primary safety control — not error handling. Operations must be prepared to investigate "the agent did the wrong thing but reported success" as a failure mode, not just service outages.
>
> **Architecture Takeaway:** Operations teams supporting agentic systems need retraining on AI-specific failure modes before go-live. Define operational runbooks for: runaway agent loops, silent wrong answers, unexpected tool call sequences, and budget overruns. These are the agentic equivalents of "service down" and "latency spike" — they need detection, alerting, and response procedures before the system goes live.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section goes further for architects who want to understand the mechanisms in detail. It is safe to skip on a first pass and return here later.

### 8.1 The 8-Plane AKP Reference Architecture

The core AKP model uses 6 planes for most production implementations, but the full reference architecture adds 2 more for mature enterprise deployments:

**Plane 7 — Evaluation Plane**
Continuous evaluation infrastructure: judges (LLMs that assess the quality of other LLM outputs), golden dataset tests run on every deployment, A/B frameworks for comparing agent versions. In production, you can't manually review every agent interaction — the evaluation plane automates quality assurance.

**Plane 8 — Persona / Identity Plane**
Agent identity management: each agent has a defined persona (name, tone, capability scope, escalation behavior), role-based access profile, and versioned configuration. When you deploy "CustomerServiceAgentV2," the identity plane manages the rollout — routing 10% of traffic to the new version while the evaluation plane monitors quality.

### 8.2 Context Budget Management

> **What is the context window?** The context window is the maximum amount of text the model can hold in working memory at once — your prompt, conversation history, retrieved documents, and the model's response all count toward this limit. Think of it as a whiteboard: everything the model needs to reason with must be written on this whiteboard. When it fills up, earlier content falls off and the model can no longer see it. Current models support 128K–1M tokens (roughly 90,000–750,000 words), but long agent workflows with rich tool outputs fill this faster than you expect.

An agent's **context budget** is the amount of the LLM's context window the agent is allowed to use. This matters because:

- As the agent loops, its context grows (each tool result is added back)
- A 128K context window can fill up in a long agentic workflow
- When context fills, the agent must either truncate (potentially losing important information) or summarize (lossy compression)
- Cost is proportional to context size — a bloated context is expensive

**Context budget strategies:**
- **Sliding window:** keep the most recent N turns, drop older ones
- **Summarization:** when context exceeds a threshold, call the LLM to summarize the history into a compact representation, then discard the raw history
- **Structured working memory:** store structured data (order details, customer profile) as a compact JSON object rather than as raw conversation text — much more token-efficient
- **Episodic memory:** after a task completes, extract key facts to durable memory and clear the working context for the next task

### 8.3 Prompt Drift Detection

In a long-running agentic deployment, the effective prompt the agent receives changes over time — not because you changed it, but because:

- The few-shot examples you provided are now dated (they reference 2024 return policies, but it's 2026)
- The tool descriptions reference APIs that have been updated
- The system prompt was written for one model but the model gateway has rotated to a different version

**Prompt drift detection** is a monitoring pattern: periodically replay a golden set of test inputs and compare the agent's output to a reference baseline. If output drift exceeds a threshold, trigger a review. This is part of the evaluation plane.

### 8.4 The IIB Adapter Pattern

When integrating an agent platform with legacy enterprise systems (SAP, IBM MQ, COBOL mainframes) that don't have modern REST APIs, the **IIB (IBM Integration Bus) Adapter Pattern** uses an integration middleware layer as the translation boundary:

```
Agent Tool Call (JSON/REST)
        │
        ▼
  Integration Middleware (MuleSoft / IIB / Azure Logic Apps)
  → translates REST → SOAP / flat file / MQ message
        │
        ▼
  Legacy System (SAP, mainframe)
```

The tool registry wraps the middleware endpoint as if it were a native API. The agent has no knowledge of the underlying legacy protocol — it calls `get_inventory_levels()`, the middleware handles the rest. This is the standard integration architecture pattern for phased AI adoption in enterprises with significant legacy system estates.

---

## 9. Key Takeaways (5 Bullets)

- **An agent is just an LLM with tools and a loop.** The Agent Core is: think (LLM call) → act (tool call) → observe (add result to context) → repeat until done. Everything else in the agentic platform is infrastructure to make this loop safe, governed, and observable at enterprise scale.

- **The Model Gateway and Tool Registry are your primary governance controls.** Every LLM call goes through the gateway (auth, cost tracking, routing, rate limiting). Every tool call goes through the registry (auth, blast radius controls, audit log). Without these, there is no consistent governance — each agent team manages its own.

- **Agentic systems require a different audit model.** Traditional audit captures *what* happened. Agentic audit must capture *why* — the LLM reasoning trace that preceded each action. OpenTelemetry extended to LLM spans is the current production standard.

- **Blast radius management is the key design principle for tool authorization.** Read-only tools need minimal controls. Tools that write to external systems, send communications, or make financial changes need: amount limits, human approval thresholds, loop detection, and irreversibility flags. Design the permission matrix before you design the agents.

- **The AKP is not a new architecture — it's your existing enterprise stack extended for AI agents.** Your API gateway, IAM, message bus, data platform, and observability stack are all reused. The AKP adds the AI-specific layer on top: model gateway, tool registry, knowledge plane, and governance controls that understand LLM-specific failure modes.
