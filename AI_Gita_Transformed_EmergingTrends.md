# Emerging Trends — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

Emerging trends in AI are the capability shifts happening right now that will change what you can build, what it costs, and how it should be governed — within the next 12–24 months.

As of mid-2026, five shifts are material enough that architects designing systems today need to account for them:

1. **Reasoning models** — a new class of models that "think before they answer," dramatically improving accuracy on complex multi-step problems at the cost of higher latency and token usage
2. **Mixture of Experts (MoE)** — the architecture behind every frontier model, which explains why large models can be cost-competitive despite their apparent size
3. **Computer Use / GUI agents** — models that can operate software interfaces, opening automation use cases that previously required RPA or custom integration
4. **Persistent memory agents** — agents that maintain context across sessions, enabling genuinely stateful AI assistants
5. **Multimodal-first models** — the frontier is no longer text-only; image, audio, video input/output is standard, which changes the document intake and media processing architectures

This tab is a radar, not a textbook. The goal is not to master each topic in depth, but to have enough understanding to know which trends affect your current or near-term projects, and when to revisit the specialist tabs for deeper coverage.

---

## 2. Why Should I Care

### For Solution Architects

Emerging trends affect system design decisions you make today:

- **Reasoning models** change when to use expensive frontier models vs cheap models. A task that previously required GPT-4o (the only model that could reliably do it) may now be better served by o3-mini or DeepSeek-R1 at lower cost — or o3 at higher quality. The capability tier map needs quarterly recalibration.
- **MoE architecture** explains why model size doesn't linearly map to inference cost anymore. A "400B parameter" MoE model activates only ~40B parameters per token — understanding this prevents you from dismissing large models as automatically too expensive.
- **Computer Use** opens automation of legacy workflows that have no API: reading a CRM screen, filling in a web form, navigating an internal portal. For integration architects dealing with legacy system estates, this is a significant unlock.
- **Persistent memory** changes the architecture of AI assistants. A stateless API call is sufficient for a one-off task; a persistent-memory agent changes how you design conversation history, user context, and personalisation.

### For Enterprise Architects

Trends that create new governance requirements:

- **Agentic AI with computer use** can take actions in systems that weren't designed for automation — creating audit trail gaps, bypassing approval workflows, accessing data without conventional access controls. Governance frameworks designed for "AI that answers questions" are insufficient for "AI that operates software."
- **Reasoning model token usage** (thinking tokens) can be 5–20× the output token count, dramatically changing cost projections for use cases that adopt reasoning models.
- **Persistent memory** means AI systems now have state that persists across sessions — creating data residency, retention, and privacy questions that stateless models don't raise.

---

## 3. Think About It Like This (Analogy)

**The Skilled Trades Analogy**

Traditional AI (pre-reasoning models) is like hiring a fast typist: give them a clear task, they execute it immediately and quickly. They're great at well-defined, single-step tasks. They struggle with problems that require stopping to think, consulting references, and checking work.

**Reasoning models** are like hiring a junior consultant who is taught to "think out loud before answering." Before responding, they write out a scratchpad: "The question is X. The key constraint is Y. Let me check if approach A satisfies Y... it does partially, but fails on Z. Let me try approach B..." This thinking process is invisible to the client but produces dramatically better final answers on hard problems — at the cost of a longer meeting.

**Mixture of Experts** is like a law firm with 100 specialist partners, but only 8–10 partners work on any given client matter. The firm is large (lots of expertise available), but efficient (only the relevant specialists are activated for each task). The per-matter cost is similar to a smaller generalist firm — but the quality on specialised matters is much higher.

**Computer Use agents** are like giving an intern a computer and saying "log in to the supplier portal and download all invoices from last month." You don't write an API integration — you explain the task and they navigate the interface the same way a human would. Powerful for legacy systems; risks the same mistakes an unsupervised intern might make.

**Persistent memory** is the difference between a new temp who starts fresh every day and a long-tenured colleague who remembers your preferences, past decisions, and project history. The long-tenured colleague is far more useful — but you also need to think about what they "remember" and whether that memory is accurate.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

> **Explain Like I'm an Architect**
>
> The key architectural decision with reasoning models is not "which is better?" but "when does the quality improvement justify the cost and latency?" The thinking token budget — the scratchpad the model writes before answering — is not free. It can be 1,000–20,000 tokens per response at premium pricing, with 10–60 second latency. For a customer service chatbot answering "what are your opening hours?", this is waste. For a legal document analysis that catches a contract clause conflict worth £500,000, it is justified.
>
> The decision framework maps to a familiar enterprise pattern: you do not send a senior partner to answer every client question. You route by complexity — receptionist for simple queries, junior for standard work, senior partner for the hard cases where the quality difference matters. Reasoning models are the senior partner tier. Use them only when (a) the task requires multi-step reasoning and (b) the cost of a wrong answer exceeds the cost of the thinking tokens.
>
> **Why this matters architecturally:** Routing between standard and reasoning models is a cost and latency decision that must be designed in from the start. A system that uses reasoning models for every query at 10K queries per day will have a monthly API cost that surprises finance. A query classifier that routes ~5% of queries to reasoning models and 95% to standard models can deliver the same quality on hard cases at a fraction of the cost.

### 4.1 Reasoning Models: Thinking Before Answering

**What they are:**

Reasoning models (OpenAI o1, o3, o4-mini; DeepSeek-R1; Qwen QwQ; Gemini Thinking) are LLMs trained to generate an internal "chain of thought" scratchpad before producing their final answer. The scratchpad — called "thinking tokens" — is typically hidden from the user but consumes tokens (and therefore costs money and time).

**Why this matters:**

Standard LLMs generate responses one token at a time, left-to-right, without backtracking. If the model commits to an incorrect direction early in the response, it continues in that direction. Reasoning models effectively implement a "draft, evaluate, revise" loop at training time — the model learns to explore multiple approaches before committing to an answer.

**The performance uplift:**

On tasks requiring multi-step logic (mathematics, code that must pass tests, legal reasoning, complex planning), reasoning models typically outperform standard models by 20–40% on accuracy benchmarks. The gain is smaller on tasks that are well-specified and single-step (classification, summarisation, format conversion) — for those, a standard model is usually sufficient and cheaper.

**The cost/latency trade-off:**

```
Standard model (Claude Sonnet, GPT-4o):
  Thinking tokens: 0
  Time to response: 1–5 seconds
  Cost: £1–5 / M tokens

Reasoning model (o3, DeepSeek-R1):
  Thinking tokens: 1,000–20,000 per response (hidden but billed)
  Time to response: 10–60 seconds (variable — depends on problem difficulty)
  Cost: £5–30 / M tokens (thinking + output)
```

**When to use reasoning models:**

| Use case | Reasoning model? | Why |
|---|---|---|
| Complex code generation (must pass tests) | ✅ Yes | Multi-step logic; quality outweighs cost |
| Mathematical / quantitative analysis | ✅ Yes | Reasoning errors are expensive |
| Legal document analysis with complex dependencies | ✅ Yes | High-stakes; accuracy critical |
| Customer service Q&A | ❌ No | Single-step; speed matters; cost not justified |
| Product description generation | ❌ No | Creative, single-pass; standard model fine |
| Data extraction from documents | ❌ No | Format + instruction following, not logic |
| Architecture / system design planning | ✅ Yes | Complex trade-off analysis benefits from thinking |

**The architect's rule:** use reasoning models when (a) the task requires multi-step logic and (b) the cost of a wrong answer exceeds the cost of the thinking tokens. For high-volume, latency-sensitive tasks: standard models. For low-volume, high-stakes, complex tasks: reasoning models.

### 4.2 Mixture of Experts (MoE): Why Frontier Models Stay Affordable

**The problem MoE solves:**

A dense model with 400B parameters activates all 400B parameters for every input token. This is computationally expensive — the cost scales with parameter count.

**How MoE works:**

Instead of a single dense feed-forward network, a MoE model has N "expert" networks (typically 64–256 per layer) and a learned "router" that selects K of them (typically 2–8) for each token. Only the selected experts are activated — the rest are idle.

```
Dense 400B model:
  Every token → ALL 400B parameters activated
  
MoE 400B model (e.g., 64 experts, top-2 routing):
  Every token → router selects 2 of 64 experts
  Active parameters per token: 400B × (2/64) ≈ 12.5B
  Inference cost ≈ equivalent to a 12.5B dense model
  But model quality ≈ a 400B+ dense model (all experts available during training)
```

> **Common Misconception:** "A 400B parameter model is always 4× more expensive to run than a 100B parameter model."
>
> In a Mixture of Experts architecture (which underpins every major frontier model), parameter count is not the inference cost driver — active parameter count is. A 400B MoE model activates roughly 10–15B parameters per token at inference time. It can be cheaper to serve than a 70B dense model at equivalent quality. Before making any infrastructure sizing or cost decisions based on a model's headline parameter count, ask: is this a dense or MoE model? What is the active parameter count? Parameter count without this context is a marketing number, not an engineering specification.

**Why MoE matters for architects:**

1. "Mixture of Experts" models can be larger (and better quality) than their inference cost implies. A "400B parameter MoE model" does not cost 4× what a "100B dense model" costs to serve.
2. Every major frontier model (GPT-4, Gemini, Claude, Llama-3-405B) is widely believed to use MoE architecture.
3. Router failures (load imbalance — too many tokens routed to the same experts) are the primary reliability risk. MoE models need load-balancing losses during training to prevent expert collapse.

**For architects:** you don't need to understand MoE implementation details. You need to know that "parameter count" is not a reliable proxy for "inference cost" in 2026 — a 400B MoE model may be cheaper to serve than a 70B dense model for the same quality level. Always benchmark on your task before making infrastructure decisions based on parameter count alone.

> **Explain Like I'm an Architect**
>
> Computer Use is automation for the systems that were never designed to be automated — the ERP screens that only work in Internet Explorer, the supplier portal that requires clicking through seven nested menus, the government reporting portal that doesn't have an API because it predates the concept.
>
> The capability is genuinely powerful: you describe the task in plain language, and the agent navigates the GUI the same way a human would. But the governance gap is significant. Traditional RPA leaves a complete audit log of every action (which field was filled, what value was entered, what the screen looked like before and after). Computer Use agents, without explicit engineering, leave no audit trail at all — you have a task description and an outcome, but no record of every click in between.
>
> Think of it as the difference between a supervised contractor who logs every hour and every material used, and an unsupervised assistant who completed the task but cannot explain exactly what they did if something went wrong.
>
> **Why this matters architecturally:** Computer Use without governance controls creates audit trail gaps that are unacceptable for any regulated workflow. The engineering required to make Computer Use enterprise-ready (screenshot audit logging, credential vault integration, minimum-privilege account scoping, human review gates for consequential actions) is not optional — it is the difference between a tool and a liability.

### 4.3 Computer Use / GUI Agents: Automation Without APIs

**What it is:**

Computer Use is the capability of a vision-language model to observe a screenshot of a computer interface and generate mouse/keyboard actions to accomplish a goal — navigating through a GUI the same way a human would.

**Anthropic's Computer Use**, available via API, takes:
- Input: a screenshot + a task description
- Output: a series of mouse clicks, keyboard inputs, and scroll actions that accomplish the task

**Why this matters for enterprise architects:**

Most enterprise systems were built long before they were expected to be automated. They have GUIs but no APIs, or APIs that are incomplete. Computer Use opens automation for:

- Legacy ERP and CRM systems (SAP GUI, legacy Oracle screens) without API integration
- Supplier portals with no EDI/API support
- Government or regulatory reporting portals
- Internal tools built before API-first design was standard

**The architecture pattern:**

```
Task: "Download all invoices from supplier portal for October 2026"

1. Agent receives task + initial screenshot of portal login page
2. Vision model identifies: username field, password field, login button
3. Actions: click username → type credentials → click password → type → click login
4. New screenshot: dashboard
5. Vision model identifies: "Invoices" menu item
6. Actions: click Invoices → set date filter → click Download
7. Screenshot confirms: download started
8. Task complete; file in local filesystem
```

**The governance risks (non-trivial):**

- **Unintended actions:** the model may click the wrong button or take an action in a system that cannot be undone. Computer Use agents need sandboxed environments and human review for consequential actions.
- **Audit trail:** traditional RPA leaves a detailed audit log of every action. Computer Use agents require explicit logging infrastructure — the screenshots and action sequences must be captured for compliance.
- **Access control:** the agent operates with the credentials of whoever is logged in. Over-privileged accounts used by agents can access more than the task requires.
- **Error recovery:** when the agent gets stuck (unexpected page state, CAPTCHA, error message), it needs explicit fallback logic — unlike a human, it may silently fail or loop indefinitely.

**When to use Computer Use vs traditional integration:**

| Scenario | Computer Use | API / RPA |
|---|---|---|
| No API available, no budget to build one | ✅ | ❌ |
| Action is high-frequency (> 1K/day) | ❌ (fragile at scale) | ✅ |
| Action requires human judgement on screen | ✅ | ❌ |
| Regulatory audit trail required | ❌ (needs careful logging) | ✅ |
| Proof of concept / validation | ✅ | ❌ |

> **Explain Like I'm an Architect**
>
> Every standard LLM API call starts with a blank slate. The model has no memory of the conversation you had yesterday, the preferences you stated last month, or the project context you explained three months ago. For a one-off task this is fine. For an AI assistant that is supposed to be genuinely helpful to a specific person over time, it creates an exhausting repetition: re-explain your context every session.
>
> Persistent memory solves this by maintaining a structured store of facts, preferences, and history outside the context window, with explicit read/write operations. The assistant remembers. But "the assistant remembers" means your organisation is now holding a new category of data asset: structured records of user preferences, past conversations, and inferred personal characteristics. This is not a technical question — it is a data governance question with retention, access control, privacy, and deletion implications.
>
> **Why this matters architecturally:** Design the governance model for persistent memory before building the capability. What data is stored? How long is it retained? Who can access it? What is the deletion process for a departing employee or a customer invoking GDPR rights? A memory store that cannot answer these questions is a compliance incident waiting to happen.

### 4.4 Persistent Memory Agents: Stateful AI Assistants

**The stateless problem:**

Every standard LLM API call is stateless. The model has no memory of previous calls. For a customer service agent, this means the customer must re-explain their context every session. For an internal AI assistant, the model can't remember that "you prefer concise summaries" or "the project uses AWS, not Azure."

**The MemGPT / Letta pattern:**

Persistent memory architectures (popularised by MemGPT, now Letta) maintain a structured memory store outside the context window, with explicit read/write operations:

```
User: "What was the conclusion of yesterday's supplier meeting?"

Agent:
  1. Search memory store: query("supplier meeting", date=yesterday)
  2. Retrieve: [Meeting notes: Supplier X agreed to 10% price reduction for Q4]
  3. Include in context → generate response
  4. After response: update memory if new information emerged
```

**Memory taxonomy (four types):**
- **Working memory:** current context window (ephemeral, lost after session)
- **Episodic memory:** past interactions and events (retrieved by similarity/recency)
- **Semantic memory:** general knowledge and user preferences (structured facts)
- **Procedural memory:** learned workflows and skills (how to do specific tasks)

**Enterprise architecture implications:**

Persistent memory creates new data assets that need governance:
- Memory stores contain user data that may be PII
- Memory retention policies must align with data governance (how long do you store AI conversation history?)
- Memory accuracy degrades over time as context changes (the AI's memory of "the project uses AWS" becomes wrong when you migrate to Azure)
- Multi-user memory systems must enforce access control (one user's memories must not leak to another)

### 4.5 Multimodal-First Architecture: 2026 Standard

In 2026, the frontier models (Claude, GPT-4o, Gemini) are multimodal by default. The architectural implication: any system design that assumes text-only input is artificially limiting the capabilities available.

**What changed:**

| Capability | 2023 | 2026 |
|---|---|---|
| Image input | GPT-4V only (expensive) | All frontier models; mid-tier too |
| Document (PDF) input | Requires OCR preprocessing | Native in-context PDF reading |
| Audio input | Whisper transcription then LLM | End-to-end (GPT-4o, Gemini) |
| Video input | Not available | Gemini 1.5 Pro, some others |
| Image generation | Separate model (DALL-E 3) | Integrated in some (GPT-4o) |

**System design patterns that change:**

Old pattern for document intake:
```
PDF → OCR (Tesseract/AWS Textract) → text → LLM
```

2026 pattern:
```
PDF → multimodal LLM (reads layout + text natively)
```

The old pattern requires an OCR pipeline, error handling for OCR failures, and loses layout information (tables, columns, headings that indicate structure). The 2026 pattern handles the full document natively — at API pricing, often cheaper than maintaining a separate OCR pipeline.

**When to still use dedicated OCR:** very high volume (1M+ documents/month where per-document API cost matters), documents requiring 100% field extraction accuracy with structured validation, or regulatory requirements for a specific certified OCR system.

---

## 5. Enterprise Example

**Scenario: Upgrading a Procurement Automation System**

A manufacturing company has a procurement team handling 2,000 supplier invoices/month and 500 purchase orders/day across 150 suppliers. Their existing automation:
- EDI connections to 20 large suppliers (covers 60% of volume)
- Manual data entry for the remaining 40% (80 suppliers with no API/EDI)
- A 3-person team processing manual invoices: average 8 minutes/invoice = 200 hours/month

**Applying the emerging trends:**

**Problem 1: Manual invoice processing (40% of volume)**

Previous bottleneck: the 80 non-EDI suppliers send invoices via email as PDF attachments, images, or even photos of handwritten invoices. Custom OCR pipelines were built for the 5 largest, but the long tail is manual.

2026 solution: multimodal LLM invoice extraction
- Send each attachment directly to Claude Vision
- Prompt: extract structured fields (vendor name, invoice number, date, line items, totals, payment terms)
- Structured output (JSON) feeds directly into the ERP
- Accuracy on typed invoices: 97%. Handwritten: 88% — human review queue for low-confidence extractions
- Result: 80% of previously manual invoices processed automatically; 200 → 40 hours/month manual work

**Problem 2: 15 suppliers with no API and complex portal UIs**

These suppliers require logging into individual supplier portals to download invoices. No EDI, no API, no email — everything lives in a portal that requires navigation.

2026 solution: Computer Use agent for portal automation
- Agent trained on each portal's navigation pattern
- Scheduled nightly run: log in, navigate to invoices section, apply date filter, download
- Files transferred to ERP intake folder
- Human review: monthly spot-check of downloaded invoices vs ERP entries
- Governance: all screenshots captured to audit log; credentials stored in vault (not in agent prompt)
- Result: 15 portals automated, covering ~200 invoices/month previously requiring dedicated human time

**Problem 3: Purchase order exception handling**

The 500 daily POs have an 8% exception rate (price mismatch, quantity discrepancy, terms issue). Each exception requires a team member to read the PO, compare to the supplier agreement, and decide: approve, reject, or escalate to procurement manager.

2026 solution: reasoning model for exception analysis
- Exception POs routed to reasoning model pipeline (o3-mini)
- Context: PO details + relevant supplier agreement clause + approval history
- Model produces: recommended action (approve/reject/escalate) + reasoning trace
- Human reviewer sees: recommendation + the model's reasoning (the thinking chain that produced the recommendation)
- For straightforward exceptions (price within tolerance, known supplier): automatic approval
- For complex cases: escalation to procurement manager with pre-populated analysis
- Result: 65% of exceptions processed automatically; manager time on exceptions reduced by 70%

**Combined impact:**
- Manual processing hours: 200 → 55/month
- Portal downloading: 40 person-hours/month → near zero
- Exception handling: 30 person-hours/month → 9 person-hours
- Total saving: ~200 hours/month at £35/hr = £7,000/month = £84,000/year
- AI cost: ~£800/month (API + infrastructure)
- ROI: 8.75× in year 1

---

## 6. Architecture Perspective

### The Agentic Architecture Evolution

The most significant architectural shift from the five trends above is the move from **reactive AI** (model called, model responds, done) to **agentic AI** (model takes multi-step actions, maintains state, operates tools, potentially over extended time periods).

```
2023 AI system architecture:
  User input → LLM API call → response → user

2026 AI system architecture:
  User task → Agent runtime
    ├── Reasoning model (complex planning)
    ├── Tool calls (APIs, databases, computer use)
    ├── Memory read/write (persistent context)
    ├── Sub-agent delegation (specialist agents)
    └── Human-in-the-loop gates (for consequential actions)
  → Result delivered (possibly after minutes of work)
```

This change introduces new architectural concerns:
- **Durability:** agents may run for minutes or hours — the system must handle interruptions gracefully (agent checkpointing, resume-on-failure)
- **Observability:** multi-step agent traces are much more complex than single API calls — full trace logging with tool call sequences and reasoning steps
- **Safety gates:** consequential actions (sending an email, modifying a database, executing a financial transaction) need explicit human review gates — not assumed approval
- **Cost control:** a misbehaving agent can generate thousands of API calls before being stopped — budget limits and circuit breakers are mandatory

### Framework Comparison for Agentic Systems

| Framework | Best for | Key limitation |
|---|---|---|
| **LangGraph** | Stateful multi-step agents; production-ready; explicit state machine | More complex to set up than LangChain |
| **LangChain** | Rapid prototyping; broad tool ecosystem | Opaque internals; hard to debug at scale |
| **AutoGen (Microsoft)** | Multi-agent conversation patterns | Less production-hardened than LangGraph |
| **CrewAI** | Role-based multi-agent workflows; simple to configure | Less flexible than LangGraph for complex state |
| **Custom (direct SDK)** | Full control; maximum debuggability | Maximum build effort |

For production enterprise systems: LangGraph or direct SDK. For prototyping and exploration: LangChain or CrewAI.

---

## 7. Check Yourself (3–5 Questions)

**Question 1 — Reasoning models for all queries**

A developer proposes using a reasoning model (o3) for all LLM calls in a customer service chatbot to "maximise quality." What are the problems with this approach?

> **Detailed Answer:** Three problems. (1) Cost: reasoning models generate thinking tokens (1,000–20,000 per response) at £10–30/M tokens. A customer service chatbot making 200K calls/day would generate enormous thinking token costs for simple queries like "what are your opening hours?" that do not benefit from complex reasoning. (2) Latency: reasoning models take 10–60 seconds per response depending on complexity. Customer service chatbots need 1–3 second response times for good UX — a 30-second "thinking" pause is unacceptable for most interactions. (3) Wasted capability: the quality improvement from reasoning models is concentrated on complex multi-step logic. A chatbot responding to simple FAQs, order status queries, and return requests sees minimal quality improvement over a standard model. The correct approach: route by complexity. Simple, well-defined queries → standard fast model (Haiku, GPT-4o-mini). Complex cases (customer dispute resolution, multi-part technical support, exception analysis) → reasoning model. A simple intent classifier can route between them at minimal cost.
>
> **Simple Explanation:** Assigning a senior specialist to answer every phone call — including "what are your opening hours?" — is expensive and slow. Route by complexity: receptionist for simple queries, specialist for hard ones. Reasoning models are the specialist tier: reserve them for the ~5% of queries where multi-step logic genuinely improves the outcome.
>
> **Architecture Takeaway:** Reasoning model routing is a cost and latency design decision. Design a query complexity classifier (cheap nano model or rule-based) that routes ~5% of complex queries to the reasoning tier and ~95% to standard models. This typically delivers equivalent quality on hard cases at 20–30% of the all-reasoning-model cost.

**Question 2 — Computer Use governance before go-live**

Your organisation wants to automate downloading invoices from 20 supplier portals using Computer Use. What governance controls must be in place before this goes live?

> **Detailed Answer:** Minimum five controls. (1) Audit logging: every session must capture a complete screenshot trail and action sequence — logged to an immutable store. Without this, you have no audit trail for compliance or debugging. (2) Credential management: portal credentials must be stored in a secrets vault (not in the agent prompt, not in environment variables). The agent retrieves credentials at runtime via API call to the vault — credentials are never exposed in logs. (3) Access scoping: the agent operates with the minimum-privilege account for each portal — read-only where possible (download but not modify). Review that existing accounts do not have unneeded write or admin permissions. (4) Human review gate for consequential actions: downloading is read-only and safe; any action that modifies portal data (submitting a dispute, approving a quote) requires explicit human approval before the agent takes the action. (5) Failure handling and alerting: when the agent gets stuck (unexpected page state, CAPTCHA, session timeout), it must alert a human rather than retrying indefinitely. Define: max retries, alert threshold, fallback to manual process.
>
> **Simple Explanation:** Traditional RPA logs every field, every value, every screen state. Computer Use without explicit engineering logs only "started task / completed task." The governance controls listed above reconstruct the audit trail that Computer Use would otherwise leave blank. They are not optional for any enterprise deployment — they are what makes the tool compliant.
>
> **Architecture Takeaway:** Computer Use governance requires five explicit controls before any enterprise deployment: screenshot audit log, credential vault, minimum-privilege account, human review gate for write actions, and automated failure alerting with manual fallback. Missing any one of these creates either a compliance gap (no audit trail) or an operational risk (agent loops or takes unintended actions silently).

**Question 3 — Mixture of Experts: intuition and cost implication**

Explain Mixture of Experts at an intuition level. Why does it mean "400B parameters" doesn't mean "expensive to run"?

> **Detailed Answer:** In a standard dense model, every token processed activates every layer and every parameter — if the model has 400B parameters, all 400B are involved in processing each token. In a Mixture of Experts model, each transformer layer contains multiple "expert" sub-networks (typically 64–256 per layer) and a learned "router" that selects only 2–8 experts per token. The other experts are completely idle — their parameters do not participate in the computation. A 400B MoE model with 64 experts and top-2 routing activates approximately 400B × (2/64) ≈ 12.5B parameters per token in the MoE layers. The inference cost is closer to a 12–15B dense model — but the model quality reflects having 400B parameters available because all experts are trained together and each expert specialises in different input patterns. For architects: "400B parameters" in a MoE model description does not mean 4× the compute cost of a 100B model. Always ask: is this dense or MoE? What is the active parameter count? This changes both cost projections and infrastructure sizing.
>
> **Simple Explanation:** A law firm with 100 specialist partners has the capability of 100 specialists. But on any given client matter, only 8–10 partners are engaged — the billing cost is similar to a smaller generalist firm. MoE is the same pattern: a 400B parameter model has the expertise of 400B parameters, but activates only ~12B per token — paying for a smaller model, getting the quality of a larger one.
>
> **Architecture Takeaway:** Parameter count alone is not a reliable proxy for inference cost or infrastructure sizing in 2026. A 400B MoE model may be cheaper to serve than a 70B dense model at equivalent quality. Before any cost estimate or GPU sizing exercise involving a large model, ask: dense or MoE? What is the active parameter count per token? These are the numbers that drive infrastructure decisions, not the headline parameter count.

**Question 4 — Data governance for persistent memory agents**

A product team wants to build a persistent-memory AI assistant for their sales team — the assistant will remember customer preferences, past meeting notes, and deal history across sessions. What data governance questions must be resolved before building?

> **Detailed Answer:** Five questions minimum. (1) Data classification: what category of data will be stored in the memory? Customer PII, deal financials, competitive intelligence — these may have different retention rules, access controls, and geographic restrictions. (2) Retention and deletion: how long is memory retained? What triggers deletion (customer request under GDPR, employee leaving, account closed)? The memory store must have explicit TTL policies and delete-on-request capability. (3) Access control: can salesperson A see salesperson B's customer memories? What happens when a customer account is transferred? Memory access must follow the same ACL as the underlying CRM data, not just "any logged-in user." (4) Memory accuracy and right to correction: if the AI remembers something incorrectly about a customer, who can correct it and how? There must be a human-readable audit and edit interface for memory content. (5) Regulatory context: in financial services, customer interaction records may be subject to MiFID II, FCA rules, or similar. Memory records may constitute a "record of advice" that has retention and disclosure requirements. Legal review required before any regulated-context AI memory deployment.
>
> **Simple Explanation:** "The assistant remembers" means your organisation is now holding a new category of structured data about customers and employees. That data has a classification, a retention period, access controls, a deletion process, and potentially regulatory implications. These are not technical questions — they are data governance questions that must be answered before any code is written.
>
> **Architecture Takeaway:** Persistent memory is a data asset, not a feature. Design the governance model first: data classification, retention policy, deletion-on-request capability, per-user access controls, and human-readable audit interface. A memory store that cannot answer "who can see this?", "how long is it kept?", and "how do we delete it?" is a GDPR incident waiting to happen.

**Question 5 — Standard LLM vs reasoning model: the thinking tokens mechanism**

What is the difference between a standard LLM and a reasoning model, and how does the "thinking tokens" mechanism improve accuracy on complex tasks?

> **Detailed Answer:** A standard LLM generates tokens left-to-right in a single pass. The model commits to each token based on what it has generated so far — there is no mechanism to backtrack and reconsider if an early decision was wrong. For simple, single-step tasks this is fine. For multi-step reasoning (solve this 5-step math problem, analyse this legal argument, plan a system architecture), the model can "go down the wrong path" early and produce a plausible-sounding but incorrect result. A reasoning model is trained to generate a hidden "thinking" sequence before the final answer. During this thinking phase, the model explores multiple approaches, checks intermediate results for consistency, identifies when an approach is not working, and backtracks to try alternatives. This scratchpad is not shown to the user but is generated and billed as tokens. The accuracy improvement comes from: (a) the model has more compute budget to explore the problem space before committing, (b) the training objective rewards correct final answers, which drives the model to develop effective thinking strategies. Practically: for complex problems requiring logic, reasoning models are 20–40% more accurate than standard models on benchmarks. For simple tasks, the improvement is marginal and the cost/latency overhead is not justified.
>
> **Simple Explanation:** A standard LLM answers immediately, committing to each word as it types. A reasoning model writes a private scratchpad first — "let me check if approach A works... no, fails here... let me try approach B..." — then gives the final answer. The scratchpad is invisible to you but costs tokens and time. For hard problems, the detour through the scratchpad produces far better answers.
>
> **Architecture Takeaway:** Reasoning models are specialised tools for complex multi-step tasks, not universal upgrades. Use them when (a) the task requires backtracking and checking intermediate results, and (b) the cost of a wrong answer exceeds the cost of the thinking tokens. For high-volume simple tasks: standard models. For low-volume high-stakes complex tasks: reasoning models. Design the routing decision before launch, not after the first unexpected API bill.

---

## 8. Advanced Deep Dive

### 8.1 Structured Output: The 2026 Production Standard

Structured output mode (JSON mode with schema enforcement) is now available from all major providers and should be the default for any integration use case. The mechanism:

**OpenAI and Anthropic (2025–2026):** structured output constrains token sampling at the generation layer. The model can only generate tokens that result in valid JSON matching the provided schema — it's not just instructed to produce JSON, it's constrained to at the sampling level. This eliminates the category of "model produced invalid JSON" failures entirely.

```python
from pydantic import BaseModel
from typing import Literal

class InvoiceExtraction(BaseModel):
    vendor_name: str
    invoice_number: str
    total_amount: float
    currency: Literal["GBP", "EUR", "USD"]
    line_items: list[dict]
    confidence: Literal["high", "medium", "low"]

# OpenAI structured output
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=InvoiceExtraction,
)
invoice = response.choices[0].message.parsed  # typed InvoiceExtraction object
```

The schema is transmitted to the model and constrains token generation. No JSON parsing errors, no defensive try/except, no format retry logic needed. For any new integration use case: start with structured output mode.

### 8.2 — Agent Observability Tooling: LangSmith, Langfuse, and Arize

When agents run in production, traditional application monitoring is not enough. An agent that calls 12 tools across 4 reasoning steps generates a trace that looks nothing like a standard API call — you need tooling designed for the agent execution model.

**The three main options in 2026:**

| Tool | Best for | Key capability | Cost model |
|---|---|---|---|
| **LangSmith** (LangChain) | Teams using LangChain/LangGraph | Deep integration with LangChain primitives; trace every agent step | Paid per trace volume |
| **Langfuse** (open-source) | Teams wanting self-hosted observability | Full trace capture, LLM-as-judge scoring, dataset management | Free self-hosted; cloud tier available |
| **Arize Phoenix** | Production monitoring at scale | Drift detection, hallucination scoring, embedding drift | Enterprise pricing |

**What these tools capture:**
- Full agent reasoning trace (every step, tool call, and intermediate output)
- Token consumption per step (for cost attribution)
- Latency per step (to find the bottleneck)
- Output quality scores (via LLM-as-judge or human review)
- Prompt version tracking (which prompt version produced which output)

**For architects:**
The architectural decision is the same as for any observability tooling: centralise or federate? A single observability platform across all AI systems gives you portfolio-level visibility (cost, quality, incidents). Per-team tooling gives flexibility but makes cross-system comparisons hard.

The minimum viable monitoring setup for a production agent: (1) full trace capture to a queryable store, (2) token cost attribution per use case, (3) weekly LLM-as-judge quality sampling on 1–5% of traces, (4) alert on latency or cost anomalies.

**When to invest in this:**
As soon as your first agent goes to production. Debugging a production agent without trace capture is like debugging a distributed system without logs — technically possible, but extremely costly in engineer time.

---

## 9. Key Takeaways (5 Bullets)

- **Reasoning models are not an upgrade to all LLM tasks — they're a specialised tool for complex multi-step logic.** Use them when the task requires backtracking, checking intermediate results, or exploring multiple approaches — legal analysis, complex code, quantitative reasoning. For high-volume, latency-sensitive, or single-step tasks, standard models are faster and cheaper with negligible quality loss.

- **Mixture of Experts means parameter count is no longer a reliable proxy for inference cost.** A 400B MoE model may be cheaper to serve than a 70B dense model at equivalent quality. Always ask whether a model uses MoE architecture and what the active parameter count is before making infrastructure sizing or cost decisions based on the headline parameter count.

- **Computer Use opens automation of legacy systems without APIs — but requires explicit governance controls before any enterprise deployment.** Audit logging of all actions, credential vault management, minimum-privilege scoping, and human-in-the-loop gates for consequential actions are not optional. Computer Use without these controls creates audit trail gaps and access control risks that outweigh the automation benefit.

- **Persistent memory agents change AI from a stateless tool into a stateful assistant — with new data governance implications.** Memory stores contain user data subject to retention policies, access control, and deletion rights. Design the governance model for memory before building the capability, not after.

- **Multimodal-first architecture eliminates many preprocessing pipelines.** Document intake that previously required OCR → text extraction → LLM now runs end-to-end through a vision-language model. This simplifies architecture, reduces failure modes in the preprocessing pipeline, and often improves extraction accuracy — especially for complex layouts, tables, and mixed handwritten/printed documents.
