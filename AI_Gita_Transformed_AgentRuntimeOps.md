# Agent Runtime Ops — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

You've deployed an AI agent. It's handling customer queries, processing returns, routing tickets. It worked perfectly in testing.

**Agent Runtime Ops** is everything you do to keep it working in production — and to know when it stops.

This is the operational layer that sits on top of the agent platform. If the Agentic Platform module covered *how to build* an agent system, Agent Runtime Ops covers *how to run it*. The concerns are:

- **Memory management** — how the agent maintains context across turns and across sessions without running out of context window (the model's working memory — everything it can see in a single API call, measured in tokens) or leaking information between users
- **Monitoring** — which signals tell you an agent is degrading, looping, hallucinating, or drifting — before your customers notice
- **Human-in-the-loop (HITL) gates** — which agent decisions must stop and wait for a human, and how to design those checkpoints without making the whole system slow
- **Prompt drift detection** — how to catch the moment when your carefully designed prompts stop working because the world has changed around them
- **Legacy system connectors** — how to connect an agent to your existing integration middleware (IBM MQ, MuleSoft, TIBCO, SAP) without rewiring your enterprise

The key distinction from traditional application operations: in a conventional system, you monitor *errors*. In an agent system, the scariest failures produce **no errors** — the agent confidently does the wrong thing, logs a success, and moves on.

---

## 2. Why Should I Care

### For Solution Architects

Every operational decision you're used to making — SLA, rollback strategy, incident runbook, capacity planning — has an agent-specific equivalent that behaves differently from what you know.

- **SLA**: a traditional API call has deterministic latency. An agent call has variable latency — 3 tool calls takes 5 seconds; an unexpected loop takes 45 seconds. Your SLA must cover the distribution, not just the average.
- **Rollback**: rolling back an agent version doesn't undo the actions it already took. If version 1.2 issued 200 incorrect refunds before you detected the problem, rolling back to 1.1 stops further damage but doesn't reverse the damage already done. Blast radius controls are your primary defence, not rollback.
- **Capacity**: LLM inference is expensive per call, and agents make multiple LLM calls per task. A sudden spike in agent activity translates directly to API cost — not just server load. Cost alerting is as critical as latency alerting.

### For Enterprise Architects

The operational maturity model for agent systems is 2–3 years behind traditional application operations. Most teams are figuring out the runbooks, dashboards, and escalation paths as they go.

What this means for enterprise architecture: plan for **observability investment upfront**, not as a retrofit. The hardest thing to add to an agent system after deployment is a comprehensive trace of why it made every decision it made. OpenTelemetry instrumentation, prompt logging, tool call capture, and the reasoning chain must be built in from day one — not bolted on when an incident happens.

---

## 3. Think About It Like This (Analogy)

**The Air Traffic Control Analogy**

Imagine you're running an air traffic control operation. You have many aircraft (agents) in the air simultaneously, each making decisions based on instructions and sensor readings.

**Memory management** is like each aircraft's flight computer — it has limited memory, so it only keeps the last N radar contacts and discards older ones. But before discarding, it writes key facts to the flight recorder. You don't want the aircraft to forget that it was warned about turbulence at 35,000 feet three minutes ago.

**Monitoring** is the radar display — you're not watching every aircraft continuously. You're watching for signals that indicate something needs attention: unexpected trajectory changes, radio silence, entering a no-fly zone, fuel below threshold. The aircraft might not report a problem; you have to detect it from the pattern.

**HITL gates** are the no-fly zones and mandatory clearances. Certain actions — crossing into restricted airspace, descending below a certain altitude — require tower clearance regardless of how confident the aircraft's computer is. The aircraft cannot proceed autonomously past those gates.

**Prompt drift** is like navigational chart updates. If the airspace boundaries changed last month and your charts weren't updated, the aircraft is following correct procedures for the wrong map. Everything looks fine on the instruments, but you're heading somewhere you didn't intend to go.

The key insight: **air traffic controllers don't control the aircraft directly — they control the boundaries and escalation triggers.** That's exactly what Agent Runtime Ops does.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 Four-Layer Memory Architecture

Agents need different kinds of memory for different purposes. Using the context window for everything is expensive, slow, and doesn't persist across sessions. The production pattern is four distinct memory layers:

> **Explain Like I'm an Architect**
>
> Why does an agent need four memory layers? Because the LLM's context window is like working RAM — fast, limited, and expensive. Every token in the context window costs money on every LLM call. An agent that stuffs six months of customer history, the entire product catalogue, and all previous conversations into a single context will run out of space and cost a fortune.
>
> The four-layer architecture is the same principle as enterprise data tiering: hot data in fast expensive memory, warm data in cheaper storage, cold data in archival. You'd never cache every historical database record in RAM — you cache what's actively needed. Same principle applies here.
>
> - **Working memory** (in-context): what the agent is actively thinking about right now — this call, this task, the immediate tool results. Expensive. Keep it lean.
> - **Episodic memory** (recent history): what happened in past sessions with this customer or task. Stored in a database, retrieved on demand. Cheap.
> - **Semantic memory** (knowledge base): your company's policies, products, procedures. Stored in a vector database, retrieved via RAG when relevant. Cheap.
> - **Procedural memory** (system prompt): how the agent should behave — its role, permissions, escalation rules. Fixed overhead, but small.
>
> The design discipline: before putting something in the context window, ask "does the agent need this for the current call, or can it be retrieved on demand?" Everything that can be retrieved on demand should be in a lower memory layer.

**Layer 1 — Working Memory (In-Context)**
What the agent holds in the LLM context window right now: the current conversation, the last few tool call results, the task instructions.

- Capacity: limited by the context window (typically 8K–32K tokens reserved for working memory, leaving room for knowledge and output)
- Lifespan: one task or conversation session
- Cost: high — every token in working memory is paid for on every LLM call
- Use for: the active conversation, the current task state, the immediate tool results

**Layer 2 — Episodic Memory (Short-Term Persistent)**
A log of what happened in recent sessions: past conversations, prior actions taken, outcomes observed.

- Storage: a database (relational or document store), not the LLM context
- Retrieval: query for relevant past episodes before starting a new task ("has this customer contacted us about this order before?")
- Lifespan: days to weeks, then summarized or archived
- Cost: cheap — stored outside the context, retrieved on demand
- Use for: cross-session continuity, personalisation, avoiding repeating questions the customer already answered

**Layer 3 — Semantic Memory (Knowledge Base)**
Structured knowledge the agent can retrieve: product catalogues, policy documents, FAQs, process guides.

- Storage: vector database (for semantic search) + document store (for full retrieval)
- Retrieval: RAG — embed the query, find the most relevant chunks, inject into working memory
- Lifespan: updated as knowledge changes (not ephemeral)
- Cost: retrieval cost only (cheap compared to keeping all knowledge in context)
- Use for: policy lookups, product information, process guidance, anything that would otherwise bloat the context

**Layer 4 — Procedural Memory (Agent Configuration)**
The agent's "how to behave" layer: system prompt, persona definition, tool permissions, escalation rules.

- Storage: configuration files / agent registry
- Lifespan: versioned and deployed, not ephemeral
- Cost: fixed overhead on every context (system prompt tokens)
- Use for: role definition, tone, boundaries, escalation thresholds, tool access scope

**Context budget rule:** Allocate your context window explicitly across these layers. A typical production allocation:

```
128K context window
├── 2K  — System prompt (procedural memory)
├── 20K — Retrieved knowledge (semantic memory, per-request)
├── 10K — Episodic context (relevant past interactions)
├── 40K — Working memory (current conversation + tool results)
└── 56K — Reserved for model reasoning + output generation
```

Exceeding the budget forces truncation. Design the truncation policy before it happens in production.

### 4.2 Monitoring: What to Watch

Agents fail in ways that traditional applications don't. Your monitoring stack needs to cover **five signal categories**:

**Signal 1 — Task Completion Health**
Is the agent finishing tasks, or hanging? Abandoning mid-task? Looping?

| Metric | What it means | Alert threshold |
|---|---|---|
| Task completion rate | % of initiated tasks that produce a final output | < 95% |
| Mean task duration | Average time from task start to final response | > 2× baseline |
| Loop detection | Tasks where the same tool is called with identical args > N times | > 3 identical calls |
| Timeout rate | Tasks that hit the max-duration limit | > 2% |

**Signal 2 — Tool Call Health**
Are tool calls succeeding? Are they being called at unexpected rates?

| Metric | What it means | Alert threshold |
|---|---|---|
| Tool error rate | % of tool calls returning errors | > 5% per tool |
| Tool call volume | Calls per minute per tool, per agent | > 2× baseline (runaway agent) |
| Unauthorized tool attempt | Agent tried to call a tool it doesn't have permission for | Any — indicates prompt injection or misconfiguration |
| Unexpected tool sequence | Agent calling tools in a sequence never seen before | Flag for review |

**Signal 3 — LLM Output Quality**
Is the model still producing useful, safe, on-topic outputs?

An LLM judge is a second model call that scores the first call's output — asking 'given this question, was this a good answer?' — and returns a quality score. It scales better than human review for large volumes.

| Metric | What it means | How to measure |
|---|---|---|
| Hallucination rate | Agent cites facts not in context or tool results | LLM judge, fact-checking pipeline |
| Off-topic rate | Agent response addresses a different question | Semantic similarity to query |
| Refusal rate | Agent refuses to answer when it shouldn't | Track refusals vs. task type |
| Confidence calibration | Agent's stated certainty vs. actual correctness | Requires labelled ground truth |

**Signal 4 — Cost and Resource**
Unexpected spikes in cost are often the first visible symptom of agent malfunction.

| Metric | Alert |
|---|---|
| Tokens per task (P95) | > 2× rolling average |
| Total hourly cost | > configured budget cap |
| Context window saturation | Tasks hitting max context > 5% |

**Signal 5 — Business Outcome Quality**
The most important signals — and the hardest to instrument.

| Metric | Example |
|---|---|
| Decision accuracy | Refund decisions: correct? overturned by human? |
| Customer satisfaction | CSAT score for agent-handled tickets |
| Escalation rate | % of tasks that ended in human escalation |
| False escalation rate | % of tasks escalated that humans resolved with the same answer the agent gave |

### 4.3 HITL Gate Design — Risk-Tiered Approvals

**Human-in-the-Loop (HITL)** gates are points in an agent workflow where the agent must pause and wait for human approval before proceeding.

Getting this design wrong in either direction is costly:
- **Too few gates:** the agent makes consequential mistakes autonomously, and you find out when a customer complains
- **Too many gates:** every task requires human approval, and you've automated nothing — just added an LLM wrapper to manual work

The design principle: **tier approvals by risk, not by task type**.

> **Explain Like I'm an Architect**
>
> The most common HITL design mistake is tiering by task category: "all refund requests need human approval." This sounds safe — but it's both over-controlling (a £3.50 refund goes through the same approval queue as a £500 one) and under-controlling (a £199 refund slips through autonomously when the threshold should be £150).
>
> The correct design principle is tiering by risk dimensions: reversibility, value, and consequence.
>
> - **Reversibility**: can the action be undone in 60 seconds? Sending an automated status update email can be undone with a correction email. Deleting a customer account cannot be undone at all.
> - **Value**: a £5 refund and a £500 refund are both "refunds" — but their financial risk is two orders of magnitude different.
> - **Consequence**: some actions have regulatory or legal implications regardless of their financial value. Sending a bulk marketing communication, filing a customs form, terminating a contract — these require human sign-off not because of cost, but because of irreversibility and downstream impact.
>
> The framework below maps these dimensions to four approval levels. The power of this design: a low-value, reversible, standard-case action never touches the approval queue (no unnecessary friction). A high-value, irreversible, non-standard action always pauses (no autonomous catastrophic mistake).

**Risk-tiered approval framework:**

| Risk Level | Criteria | Gate Behaviour |
|---|---|---|
| **Low** | Read-only, reversible, low-value, customer-initiated | No gate — agent proceeds autonomously |
| **Medium** | Writes to a system, value < threshold, standard case | Soft gate — agent proceeds, logs for async human review |
| **High** | Irreversible action, value > threshold, or non-standard case | Hard gate — agent pauses, notifies human, waits up to SLA |
| **Critical** | PII deletion, regulatory-impacted, security-sensitive | Mandatory human approval — agent cannot proceed without explicit sign-off |

**Example matrix for a customer service agent at a retail company:**

| Action | Risk Level | Gate |
|---|---|---|
| Look up order status | Low | Autonomous |
| Issue refund < £50 | Low | Autonomous |
| Issue refund £50–£200 | Medium | Proceeds + async review flag |
| Issue refund > £200 | High | Hard gate — supervisor approval required |
| Cancel order (unshipped) | Medium | Proceeds + async review flag |
| Cancel order (shipped) | High | Hard gate — ops team approval |
| Send bulk communication | Critical | Mandatory human approval |
| Delete customer account | Critical | Mandatory human approval + regulatory log |

**Gate implementation pattern:**

```
Agent determines action needed
        │
        ▼
Risk classifier (rule-based or LLM judge)
        │
     ┌──┴──┐
   Low    High
     │      │
  Proceed  Create approval task
           → notify approver (Slack / email / ticket)
           → agent suspends (state serialized to DB)
           │
     ┌─────┴─────┐
  Approved     Rejected / Timeout
     │              │
  Agent resumes   Agent notifies user,
  with approval   logs outcome, closes task
  context
```

**SLA design for HITL gates:** A suspended agent task has a waiting SLA. If no human approves within (e.g.) 4 hours during business hours, the task either auto-escalates to the next tier or auto-closes with a customer notification. Never let tasks silently queue forever.

### 4.4 Prompt Drift Detection

Your agent prompts are not static. They encode assumptions about:
- The tools that exist (a tool you referenced might have been renamed or deprecated)
- The data formats tools return (a field name changed in the OMS API response)
- The policies and rules the agent should follow (return policy updated last month)
- The model it's running against (model gateway rotated from GPT-4o to a new version)

Any of these changes can silently degrade agent performance without a single error being thrown.

> **Explain Like I'm an Architect**
>
> Prompt drift is the agent operations equivalent of configuration drift in infrastructure — the system was deployed correctly, nothing explicitly changed in your code, but it gradually stops working as intended. The cause: the world around the agent changed while the agent's instructions did not.
>
> Your return policy changed from 30 days to 14 days — the policy document was updated in the knowledge base, but the system prompt still says "30 days." The OMS API now returns carrier names in a different format — the agent still references the old field name in its reasoning. A model update subtly changed how the base model interprets your role prompt — the agent is slightly less assertive than it was last month.
>
> None of these changes throw an error. The agent still processes requests and returns responses. The quality just silently degrades.
>
> **Why a golden test set is the only reliable detection mechanism:** you need a set of fixed, known-answer test cases that you can replay against the live system on a schedule. The test set is the "known good state" — if the live agent's answers on these cases start diverging from the expected answers, something in the system has drifted. Without the test set, you find out about drift from customer complaints or audit findings — after it has already caused harm.

**Prompt drift detection pipeline:**

1. **Golden test set:** a curated set of 50–200 test tasks with known correct outputs. These cover edge cases, standard cases, and the cases that failed in production
2. **Scheduled regression:** run the golden test set daily (or on every deployment) through the live agent
3. **Scoring:** an LLM judge evaluates each output against the reference answer — scores correctness, completeness, and policy compliance
4. **Drift alerting:** if the mean score drops more than X% from the baseline, trigger an alert and flag for investigation

**Retrieval quality signals** — drift also appears in what the agent retrieves from the knowledge plane:

| Signal | What it detects |
|---|---|
| Retrieval precision drop | Knowledge base documents have drifted from query patterns |
| Low-similarity retrievals | Queries are no longer finding semantically relevant content |
| Stale document rate | Retrieved documents have not been updated in > N days |
| Coverage gap | Query classes that return no results above threshold |

The monitoring principle: **treat prompt and retrieval quality as first-class operational signals, not one-time configuration concerns.**

### 4.5 Enterprise Legacy Connectors

Most enterprises have critical data in systems that predate REST APIs: SAP ERP, IBM MQ message queues, TIBCO event buses, COBOL mainframes. Agents need to reach this data.

The pattern: don't expose legacy systems directly to agents. Wrap them in the integration middleware layer you already operate.

**Three connector patterns:**

**Pattern A — REST Facade (recommended for new work):**
Build a REST/OpenAPI endpoint in your integration middleware (MuleSoft, Azure APIM, IBM APIC) that wraps the legacy system. Register this endpoint as a tool in the tool registry. The agent calls the REST facade; the middleware handles the protocol translation.

```
Agent → Tool Registry → REST Facade (MuleSoft) → SAP RFC → SAP ERP
```

**Pattern B — Event-Driven (for real-time data):**
For systems that publish events to a message bus (IBM MQ, TIBCO, Kafka), connect the agent's knowledge plane to the event stream. The agent's semantic memory is updated in near-real-time from the event feed rather than via synchronous API calls.

```
SAP ERP → IBM MQ → Event Processor → Agent Knowledge Plane (vector store / cache)
Agent reads from knowledge plane (no synchronous SAP call at inference time)
```

**Pattern C — Async Task Dispatch (for long-running processes):**
For processes that take minutes or hours (e.g., triggering a warehouse pick-and-pack, initiating a supplier order), the agent dispatches a task message to the queue and registers a callback. The agent suspends, and the runtime resumes it when the callback arrives.

```
Agent → Tool: dispatch_warehouse_task(task_spec)
      → Message queued to WMS
      → Agent suspends, state persisted
      ← WMS completes, sends completion event
      → Runtime resumes agent with result
```

**Design principle:** all three patterns preserve the agent's tool abstraction — the agent makes a clean tool call with no knowledge of the underlying protocol. The legacy complexity lives entirely in the connector layer, which is owned and operated by your integration team.

---

## 5. Enterprise Example

**Scenario: Agent Operations for a Supply Chain Exception Handler**

Your supply chain team runs an AI agent that monitors inbound shipments and handles exceptions: delayed carriers, customs holds, damaged goods. 2,000 shipments tracked daily, 150–200 exceptions per day that previously required manual handling.

**Memory architecture for this agent:**

- Working memory: current exception case — shipment ID, delay reason, carrier status, impacted orders
- Episodic memory: previous exceptions on the same carrier route (is this carrier frequently delayed in December?)
- Semantic memory: supplier SLA agreements, escalation playbooks, carrier contact details, customs documentation requirements
- Procedural memory: system prompt defining escalation rules, tool permissions, communication tone

**Monitoring dashboard:**

| Metric | Target | Current | Status |
|---|---|---|---|
| Exception resolution rate | > 85% autonomous | 88% | ✅ |
| Mean resolution time | < 4 hours | 2.3 hours | ✅ |
| HITL escalation rate | < 15% | 12% | ✅ |
| False escalation rate | < 5% | 8% | ⚠️ Review |
| Tool error rate (carrier API) | < 2% | 6% | 🔴 Alert |
| Cost per exception | < £0.15 | £0.22 | ⚠️ Review |

The carrier API tool error rate of 6% and cost per exception of £0.22 both appeared in the same week. Investigation: the carrier API introduced a new rate limit; the agent is retrying failed calls, each retry costs LLM tokens to process the error, and 3 retries per failed call × 6% error rate is compounding cost. Fix: add a circuit breaker to the carrier API tool — after 2 failed calls in a row, fail fast and escalate rather than retrying.

**HITL gate configuration for this agent:**

- Autonomous: contact carrier for status update, update internal tracking, notify downstream teams
- Async review: re-route shipment to alternative carrier (cost < £500)
- Hard gate: authorize air freight upgrade (cost > £500), delay release of import goods, trigger supplier penalty clause
- Mandatory approval: customs documentation filing, regulatory non-compliance escalation

**Prompt drift example from this deployment:**
In March, the supplier SLA agreement was updated — penalty clauses now kick in at 3-day delays instead of 5. The agent's semantic memory (the SLA document) was updated. But the agent's procedural memory (system prompt) still said "escalate if delay > 5 days." The drift went undetected for 2 weeks because no errors were thrown. The golden test set caught it: a test case with a 4-day delay that should have triggered an escalation was not escalating. Fix: update the system prompt and add the 4-day delay scenario to the golden test set.

---

## 6. Architecture Perspective

### Observability Stack for Agent Systems

Traditional application observability: logs, metrics, traces.

Agent observability: logs, metrics, traces **+ reasoning traces + tool call graphs + LLM quality signals**.

**OpenTelemetry (OTel) extended for LLMs:**
OTel is the open standard for distributed tracing. The GenAI semantic conventions (finalized 2024) extend OTel to capture LLM-specific spans:

```
Trace: "handle_exception(shipment_12345)"
  ├── Span: "retrieve_episodic_memory"      [2ms]
  ├── Span: "retrieve_knowledge(SLA_docs)"  [45ms]
  ├── Span: "llm_call_1"                   [1.2s]
  │     attributes: model=gpt-4o, tokens_in=2400, tokens_out=180
  │     llm.reasoning: "delay is 4 days, check SLA threshold..."
  ├── Span: "tool_call: get_carrier_status" [340ms]
  │     attributes: tool=carrier_api, status=success
  ├── Span: "llm_call_2"                   [0.9s]
  │     attributes: model=gpt-4o, tokens_in=2800, tokens_out=220
  └── Span: "tool_call: create_escalation"  [120ms]
        attributes: tool=ticketing, escalation_type=hard_gate
```

This trace is what lets you answer: "why did the agent escalate this shipment exception?" — you can read the reasoning trace and see the exact decision point.

**The four observability layers for agent systems:**

| Layer | What it captures | Primary use |
|---|---|---|
| Infrastructure metrics | CPU, GPU, memory, network | Capacity planning |
| Application traces (OTel) | Latency, errors, tool call graph | Debugging, SLA tracking |
| LLM quality signals | Hallucination rate, relevance, refusals | Quality monitoring |
| Business outcome metrics | Task accuracy, escalation rate, CSAT | ROI and drift detection |

Most teams instrument layers 1 and 2 but skip 3 and 4. The failures that matter most show up in layers 3 and 4.

### Agent Version Management

Agents are versioned software artifacts, but rolling them out is more complex than rolling out a microservice because:

- The agent's behavior is a combination of: model version + system prompt version + tool registry version + knowledge base version. All four can change independently.
- A/B testing agent versions requires routing at the task level, not the request level — you don't want the same user's multi-turn conversation to switch agent versions mid-session.

**Agent versioning matrix:**

```
Agent Version = {
  model:        "gpt-4o-2025-01-15",
  prompt:       "customer-service-v2.3",
  tools:        "tool-registry-snapshot-2026-06-15",
  knowledge:    "knowledge-base-2026-06-20"
}
```

Deploy new versions with **shadow mode** first: the new agent processes the same tasks as the live agent but its outputs go to a review queue rather than the customer. Compare new vs. old outputs using an LLM judge before promoting the new version to live traffic.

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — Silent quality degradation**

An agent that was resolving 90% of customer refund requests autonomously last month is now resolving only 70%, and the difference is going to human escalation. No errors in the logs. What are the first three things you investigate?

> **Detailed Answer:** (1) Prompt drift — did the return policy change recently? Was the system prompt or knowledge base updated and did the agent's behavior change as a result? Run the golden test set to see if benchmark scores dropped. (2) Retrieval quality — are the knowledge base documents the agent retrieves for policy lookups still accurate and relevant? Check retrieval precision and document freshness. (3) Model change — did the model gateway route to a different model version? LLM behavior changes between model versions can affect tool call decisions. Check the model version in the LLM call logs around the time the metric changed.
>
> **Simple Explanation:** No errors in the logs means the system is working correctly from a technical standpoint — it's making calls, getting responses, and completing tasks. The quality problem is in the agent's decisions, not its infrastructure. That narrows it to three causes: the instructions changed (prompt drift), the knowledge changed (retrieval drift), or the underlying model changed (model version drift). All three are invisible to standard error monitoring.
>
> **Architecture Takeaway:** "No errors" is not the same as "working correctly" for agent systems. Build quality monitoring that runs alongside error monitoring: golden test set score as a daily metric, retrieval precision as a daily metric, and model version logged per call. A drop in the quality metric triggers an investigation before users notice — not after.

---

**Question 2 — HITL design for bulk communications**

Your team wants to deploy an agent that can send promotional emails to customer segments based on purchase history. What HITL gate design would you propose, and why?

> **Detailed Answer:** Sending bulk communications is irreversible and high blast-radius — a misfired promotional email to the wrong segment, or with wrong content, cannot be undone. This warrants a critical-tier HITL gate: the agent prepares the email draft, selects the target segment, and presents both to a human approver before any send. The approval should include: segment size, sample recipients (3–5 for review), email preview, and an estimated unsubscribe risk. Automated sending without human review would be architecturally inappropriate for any communication going to more than a handful of recipients. Additional controls: a dry-run mode that sends only to an internal test list first; a maximum send rate (e.g., 10K recipients/hour) to limit blast radius if an error is discovered mid-send; an automatic send-abort trigger if bounce/unsubscribe rates exceed a threshold.
>
> **Simple Explanation:** Sending a promotional email to 500,000 customers is one of the highest-blast-radius actions an agent can take — it's irreversible, visible to customers, and creates regulatory risk if the content or targeting is wrong. Every email marketing team knows this: no bulk send goes out without human review and approval. An AI agent that can send bulk communications autonomously bypasses a control that exists for very good reasons.
>
> **Architecture Takeaway:** Blast radius should be the primary driver of HITL gate placement. The question to ask for any irreversible action: "if the agent gets this wrong, what's the maximum damage?" For bulk email: potentially hundreds of thousands of wrong emails, regulatory violations, customer churn, legal liability. That risk profile mandates a mandatory human approval gate regardless of how confident the agent is.

---

**Question 3 — Memory layer distinction**

What is the difference between episodic memory and semantic memory in an agent's memory architecture, and give a concrete example of each in a supply chain context?

> **Detailed Answer:** Episodic memory is a record of what actually happened — past events and interactions. Example: "Carrier X was 3 days late on the Milan route in November, and again in December — flagged as a seasonal pattern." Semantic memory is structured knowledge — what the agent "knows" about the world, independent of what it has personally experienced. Example: "The SLA agreement with Supplier Y states that delays exceeding 3 days trigger a penalty clause of 2% of order value." Episodic memory is retrieved by temporal or entity-based lookup ("what happened with this carrier before?"). Semantic memory is retrieved by semantic similarity ("what does our policy say about carrier delays?").
>
> **Simple Explanation:** Episodic memory is the agent's diary — what actually happened, when, and to whom. Semantic memory is the agent's reference library — what the rules and facts are, independent of any specific event. The diary and the library answer different questions. "Has this carrier been late before?" → diary (episodic). "What is our policy when a carrier is late?" → library (semantic). You need both because neither alone is sufficient for handling complex cases.
>
> **Architecture Takeaway:** Episodic and semantic memory require different storage and retrieval patterns. Episodic memory typically lives in a relational or document database, indexed by entity ID and timestamp. Semantic memory lives in a vector database, indexed by embedding for similarity search. Do not conflate them into a single store — the retrieval mechanisms are fundamentally different, and conflating them degrades both.

---

**Question 4 — Cost monitoring for agents**

Why is cost monitoring as critical as latency monitoring for agent systems, and what pattern causes unexpected cost spikes?

> **Detailed Answer:** In a conventional API service, cost is tied to infrastructure (fixed) — load spikes hit latency before cost. In agent systems, cost is proportional to LLM token consumption, which is runtime-determined by the agent's behavior. An agent that loops (calls the same tool repeatedly without progressing), retries errors without a circuit breaker, or receives unexpectedly large tool responses can consume 10–100× the expected tokens with no latency alert triggering. A task that normally costs £0.02 can cost £2.00 if the agent loops 100 times. Cost alerting with per-agent and per-task caps is a hard requirement, not a nice-to-have. The most common pattern causing spikes: a tool starts returning errors → the agent retries → each retry invokes a full LLM reasoning step → retry loop runs until max steps is hit → 20× normal cost per task for the duration of the tool outage.
>
> **Simple Explanation:** For a traditional API, if traffic doubles, your server load doubles but your cost is roughly fixed (you're paying for the server whether it's busy or not). For an agent using an LLM API, if an agent goes into a loop, your cost goes up with every loop iteration because you're paying per token processed. A broken tool that triggers retries isn't just a latency problem — it's a cost spike. You need budget alerts that fire before the next invoice, not when you see it.
>
> **Architecture Takeaway:** Set per-task cost caps as a hard limit in the agent runtime before deployment. Define: the expected average cost per task (£X), the maximum acceptable cost (£X × 10, as a circuit breaker), and a per-agent daily budget cap (alert at 80%, halt at 100%). These parameters belong in your agent configuration alongside the tool permissions and HITL thresholds. Cost runaway is operationally as serious as a service outage — treat it with equivalent alerting.

---

**Question 5 — Wrong answer diagnostic runbook**

Your operations team asks for a runbook for "agent is producing wrong answers." What are the five diagnostic steps you'd include?

> **Detailed Answer:** (1) Check the reasoning trace in OTel — what tools did the agent call, what did they return, and what was the LLM's reasoning at the decision point? (2) Check retrieval quality — was the agent retrieving the right knowledge? Were retrieved documents current? (3) Check model version — did the model gateway change the routing recently? LLM behavior changes between model versions can affect tool call decisions. (4) Run the golden test set — is the benchmark score below baseline, confirming systematic degradation vs. a one-off case? (5) Check the tool results — did the tools return correct data? If a tool returned stale or incorrect data, the agent's wrong answer is a data quality problem, not an agent quality problem.
>
> **Simple Explanation:** "The agent gave a wrong answer" has five possible root causes: (1) the agent reasoned incorrectly from correct information (LLM quality issue), (2) the agent retrieved the wrong information (retrieval issue), (3) the model changed and behaves differently (model version issue), (4) the problem is systematic (quality degradation — check test set), or (5) a tool gave the agent wrong data to reason from (data quality issue). The diagnostic steps are ordered from "most visible" to "most systematic." The OTel trace answers question 1 and 2 immediately. The golden test set answers question 4. Tool result logs answer question 5.
>
> **Architecture Takeaway:** The five-step runbook is only possible if the underlying observability infrastructure was built: OTel traces with LLM spans, retrieval logs, model version logging, a scheduled golden test set runner, and tool call result logging. If any of these are missing, the corresponding diagnostic step becomes guesswork. Build the observability infrastructure before you need the runbook — not after your first wrong-answer incident.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section goes further for architects who want to understand the mechanisms in detail. It is safe to skip on a first pass and return here later.

### 8.1 Agent Task Tree Visualization

Complex multi-agent workflows create a **task tree**: a hierarchical structure of parent tasks spawning child tasks, with dependencies between them.

```
Task: "Resolve supply chain exception batch (50 exceptions)"
├── Sub-task: "Resolve exception EX-001" [autonomous]
│     ├── Tool: get_carrier_status → delayed
│     ├── Tool: get_impacted_orders → 3 orders
│     └── Tool: notify_operations → sent
├── Sub-task: "Resolve exception EX-002" [HITL gate triggered]
│     ├── Tool: get_carrier_status → critical delay
│     ├── HITL: escalation created → waiting for supervisor
│     └── [suspended]
└── Sub-task: "Resolve exception EX-003" [failed]
      ├── Tool: get_carrier_status → API error (timeout)
      ├── Tool: get_carrier_status → API error (timeout)  [retry 1]
      └── Circuit breaker triggered → escalated to human
```

Visualizing the task tree is essential for debugging multi-agent systems. A task tree view in your monitoring dashboard shows immediately which branches are stuck, which tools are failing, and where HITL gates are creating queues.

### 8.2 Context Window Pressure Strategies

When working memory approaches the context budget:

**Summarization:** call the LLM to compress the conversation history into a compact summary, then discard the raw history. Cost: one extra LLM call. Gain: 70–80% context reduction. Risk: lossy — some details in the raw history may not survive summarization.

**Structured state extraction:** instead of keeping raw conversation text, extract the key facts into a structured object at each step:

```json
{
  "customer_id": "C-12345",
  "issue_type": "missing_item",
  "order_id": "O-67890",
  "items_ordered": 3,
  "items_received": 2,
  "missing_item": "SKU-ABC",
  "warehouse_scan_weight_discrepancy": true,
  "refund_eligible": true,
  "refund_amount": 79.99
}
```

This JSON state object is ~200 tokens. The raw conversation that produced it is ~2,000 tokens. A 10× compression with zero information loss for the decision the agent needs to make.

**Memory offload:** move tool results to episodic memory after each step. The agent retains a summary ("carrier API confirmed 2-day delay"), not the full raw response (which might be 1,500 tokens of JSON). Retrieve the full response only if a later step needs it.

### 8.3 Circuit Breakers for Tool Calls

Borrowed from distributed systems, a **circuit breaker** pattern wraps tool calls to prevent a failing external system from cascading into agent failure:

**Closed (normal):** tool calls proceed normally
**Open (failing):** after N consecutive failures, the circuit opens — calls fail immediately without hitting the external system
**Half-open (recovering):** after a timeout, one probe call is allowed through; if it succeeds, the circuit closes again

For agents, circuit breakers serve a second purpose: **preventing retry loops from consuming tokens**. Without a circuit breaker, an agent that encounters a tool error will often retry (using LLM tokens to reason about the error each time). A circuit breaker transforms this into a fast, cheap failure with a clear escalation path.

```
Tool call: carrier_api.get_status()
    │
    ▼
Circuit breaker check:
  - Error count in last 60s: 4
  - Threshold: 3
  - State: OPEN
    │
    ▼
Fast fail → return: {status: "circuit_open", escalate: true}
    │
    ▼
Agent: "Tool unavailable — escalating to human"
```

---

## 9. Key Takeaways (5 Bullets)

- **Agent failures are often silent.** The agent confidently does the wrong thing, logs a success, and moves on — no errors thrown. Your monitoring strategy must watch for behavioral anomalies (unexpected tool sequences, cost spikes, quality score drops), not just error rates.

- **Design HITL gates by risk tier, not by task type.** The question is not "which tasks need human approval?" but "which outcomes are irreversible, high-value, or regulatory-impacted?" Low-risk reversible actions should be autonomous. Irreversible or high-value actions need hard gates — regardless of how confident the agent is.

- **Four-layer memory is not optional overhead — it's cost and quality management.** Putting everything in the context window is expensive and unreliable at scale. Working memory for the current task, episodic memory for history, semantic memory for knowledge, and procedural memory for behavior — each layer has the right storage type, retrieval pattern, and cost profile for its purpose.

- **Prompt drift is a production reliability concern, not a one-time setup task.** Your system prompt, knowledge base, tool definitions, and model version all change over time. A golden test set run on a schedule is the only reliable way to detect when those changes have silently degraded agent quality.

- **The observability stack for agents requires LLM-specific extensions.** Standard application traces (latency, errors, throughput) are necessary but not sufficient. You need reasoning traces (why did the agent make that decision?), tool call graphs (what did it do and in what sequence?), and LLM quality signals (is it hallucinating, refusing, or drifting?). Instrument with OTel + GenAI semantic conventions from day one.
