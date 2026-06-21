# Agents & Prompting — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

There is a progression from using AI to designing AI systems. It goes like this:

**Prompting** is how you communicate intent to an LLM. A prompt is the instruction you give the model — and the quality of that instruction determines whether you get a useful answer or a fluent non-answer. Prompt engineering is the discipline of writing those instructions well: structuring them, providing examples, guiding the model's reasoning process.

**Function calling (tool use)** is the mechanism by which an LLM can invoke external capabilities — call an API, query a database, run code — instead of answering purely from its training weights. The model doesn't execute the call itself; it outputs a structured request ("call `get_order_status` with `order_id=12345`"), and the application executes it and returns the result.

**Agents** combine prompting and tool use with a loop: the model thinks, decides whether to use a tool, uses it, observes the result, thinks again, and repeats — until it has enough information to answer. An agent is an LLM that can take multi-step actions rather than produce a single response.

**The protocol stack** (MCP, A2A, AG-UI) is the emerging set of standards that make agents interoperable — so a tool built by one team can be used by any agent, an agent built on one framework can delegate to an agent built on another, and a human can interact with an agent workflow without custom integration.

For Solution Architects, this progression matters because each step is a design decision with architectural implications. "How should we prompt this?" is a different question from "should this be an agent?" is a different question from "how do we connect this agent to our enterprise tool estate?" This module gives you the mental model to answer all three.

---

## 2. Why Should I Care

### For Solution Architects

Prompting is not a developer task to be delegated — it is a system design decision. The system prompt defines the model's role, boundaries, tone, tool access, and escalation behaviour. A poorly designed system prompt produces inconsistent behaviour, unexpected refusals, and compliance risks. A well-designed system prompt is the first layer of governance for any LLM-based system.

The agent decision — "should this be a single LLM call or an agent loop?" — has major implications for your architecture:

- **Single call:** deterministic, fast, cheap, easy to test. Output is one response to one input.
- **Agent loop:** non-deterministic, variable latency, variable cost, harder to test. Output is a sequence of actions that may span multiple systems.

Most use cases start as a single LLM call and evolve toward agents when users ask for tasks the single call can't complete. Designing the boundary between "this is a generation task" and "this is an agent task" upfront saves significant rework.

### For Enterprise Architects

The MCP/A2A/AG-UI protocol stack is to agents what REST was to web APIs — a standardisation moment. Before REST, every API was bespoke. After REST, APIs could be composed and integrated at scale.

Before MCP: every team builds their own tool integrations — each agent team writes its own OMS connector, its own Confluence connector, its own email integration. No sharing, no governance, no central tool registry.

After MCP: tools are built once, registered centrally, and available to any agent that has permission. Your enterprise tool estate becomes a shared capability that all agent-based applications can draw on.

The architectural implication: the investment you make in MCP-compatible tool development today is infrastructure, not application code. It compounds. Every new agent that joins your enterprise benefits from the tools already built.

---

## 3. Think About It Like This (Analogy)

**The Operations Manager Analogy**

Think about an experienced operations manager at a logistics company. They have three modes of working:

**Mode 1 — Direct answer (prompting):** Someone asks "what's our standard lead time for European shipments?" They answer immediately from knowledge: "10–14 days, 7 for premium." No tools needed. The quality of their answer depends on how well they understood the question and how clearly they were briefed when they joined.

**Mode 2 — Tool-assisted lookup (function calling):** Someone asks "what's the status of shipment SH-9823?" They can't answer from memory — they open the tracking system, look it up, and report back. They know *which* tool to use and *how* to use it, but they need the tool to get the answer.

**Mode 3 — Multi-step investigation (agent loop):** Someone asks "why is our on-time delivery rate down 12% this month and what should we do?" The manager doesn't answer immediately. They check the tracking system (tool 1), identify the worst-performing carriers, query the carrier performance database (tool 2), look up recent weather events affecting those routes (tool 3), check whether the contracts have penalty clauses (tool 4), then synthesise everything into a recommendation. Each step informs the next.

**Prompting** is how well you briefed the manager when they started — what their role is, what they can and can't do, what tone to use, what to escalate.

**The protocol stack** is the company's standard systems and procedures — so the manager can look up shipments the same way regardless of which carrier, and delegate tasks to other managers using the same escalation framework.

The key insight: a well-briefed manager with clear procedures and good tools is dramatically more effective than a brilliant manager with none of these. The same is true for LLM-based systems.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 Prompt Engineering: A Practical Taxonomy

Prompt engineering is the practice of writing instructions that reliably get the output you need from an LLM. The techniques form a progression from simple to complex:

In prompt engineering, a 'shot' means an example you provide in the prompt. Zero-shot means no examples given — the model must infer what you want from the instruction alone. Few-shot means 2–5 examples are included — showing the model the pattern before asking it to continue.

> **Explain Like I'm an Architect**
>
> Think about how you brief a new contractor on a task. You have three options:
>
> - **Zero-shot** — you describe the task and trust the contractor to figure it out from the description alone. Works for straightforward, unambiguous tasks. "Write a SQL query that returns all orders over £500."
>
> - **Few-shot** — you describe the task AND show 3–5 examples of exactly the output format you want. The contractor stops guessing at your style or format — they can see it. Use this whenever you need a specific structure, tone, or format that isn't obvious from the instruction alone.
>
> - **Chain-of-Thought** — you tell the contractor to think through the problem step by step and show their working before giving the answer. This dramatically improves quality for complex decisions where the right answer isn't immediately obvious. It's like asking someone to show their reasoning in a business case rather than just giving you the recommendation.
>
> The practical rule: if the model gives inconsistent outputs on zero-shot, add examples (few-shot). If the model gives wrong answers on complex reasoning tasks, add "think step by step" (CoT). If the task is simple and the output is obvious, zero-shot is fine and cheaper.

**Zero-shot prompting**
No examples — just the instruction.
```
Classify the sentiment of this customer review as positive, negative, or neutral:
"The delivery was late but the product quality was excellent."
```
Use when: the task is straightforward and the model has strong training signal for it.

**Few-shot prompting**
Provide 2–5 examples of input → output pairs before the actual query.
```
Classify the sentiment:
Review: "Fast delivery, exactly as described." → Positive
Review: "Arrived broken, terrible packaging." → Negative
Review: "Product is fine, nothing special." → Neutral

Review: "The delivery was late but the product quality was excellent." → 
```
Use when: zero-shot quality is inconsistent; when you need a specific output format; when the task is domain-specific.

**Chain-of-Thought (CoT) prompting**
Instruct the model to reason step by step before answering. The model's intermediate reasoning improves the final answer quality.
```
A customer ordered 3 items: £45, £23, and £12. 
They have a 15% loyalty discount and paid £5 shipping.
What is their total? Think step by step.
```
Use when: the task involves multi-step reasoning, calculation, or logic. CoT dramatically improves accuracy on complex tasks.

**Zero-shot CoT**
Add "Let's think step by step." to any prompt — surprisingly effective.
```
Is this refund request eligible under our 30-day policy? 
Order date: 15 May. Return request: 18 June.
Let's think step by step.
```

**Structured output prompting**
Instruct the model to return a specific format (JSON, XML, markdown table). Modern LLMs support this natively via "structured output" or "JSON mode."
```
Extract the following from this contract clause and return as JSON:
{fields: party_names, effective_date, termination_notice_period}

Clause: "This agreement between RetailCo Ltd and SupplierX GmbH, 
effective 1 January 2026, may be terminated by either party 
with 90 days written notice..."
```
Use when: downstream systems need to parse the output programmatically.

**Role prompting**
Assign the model an explicit role that activates relevant knowledge and tone.
```
You are a senior contract analyst for a retail company. 
Your role is to identify clauses that deviate from our standard MSA template 
and flag them with a risk rating (High/Medium/Low) and brief explanation.
```

**System prompt design principles for production:**
- State the role explicitly at the start
- Define what the model can and cannot do (boundaries)
- Specify the output format
- Include escalation instructions ("if you cannot answer from the provided context, say 'I don't have that information'")
- Add few-shot examples for the most common and most error-prone cases
- Never rely on a single instruction for safety-critical behaviours — back up prompt instructions with technical controls

### 4.2 Function Calling: How Tools Actually Work

Function calling (also called tool use) is the mechanism by which an LLM can request the execution of an external function. The model does not execute the function — it outputs a structured request, and the application executes it.

**The mechanism, step by step:**

```
1. Application sends the LLM:
   - The user's message
   - A list of available tools (name, description, parameters, required fields)
   - The system prompt

2. LLM decides whether a tool call is needed.
   If yes, instead of a text response, it outputs:
   {
     "tool_call": {
       "name": "get_order_status",
       "arguments": {"order_id": "12345"}
     }
   }

3. Application receives the tool call specification.
   Application executes: OMS_API.get_order(id="12345")
   Result: {"status": "shipped", "estimated_delivery": "2026-06-23"}

4. Application sends the tool result back to the LLM:
   [previous messages] + [tool result]

5. LLM generates the final text response based on the tool result.
   "Order 12345 has shipped and is estimated to arrive on 23 June."
```

> **What is the context window?** The context window is the maximum amount of text the model can hold in working memory at once — your prompt, conversation history, retrieved documents, and the model's response all count toward this limit. Think of it as a whiteboard: everything the model needs to reason with must be written on this whiteboard. When it fills up, earlier content falls off and the model can no longer see it. Current models support 128K–1M tokens (roughly 90,000–750,000 words), but long agent workflows with rich tool outputs fill this faster than you expect.

**Why this matters architecturally:**
- The LLM decides *when* to call a tool and *which* tool to call based on the tool descriptions you provide. Tool descriptions are part of your system design — write them precisely.
- The model never has direct access to your systems. The application controls execution. This is the correct security boundary.
- Tool results go back into the context window — large tool responses (e.g., a full order history with 200 entries) consume context budget. Return only what the model needs.

**Tool description quality matters enormously:**
```
Poor: "get_order": "Gets an order."

Good: "get_order_status": "Retrieve the current status and estimated 
delivery date for a customer order. Use when the customer asks about 
order progress, delivery timing, or shipment tracking. 
Parameters: order_id (string, required) - the 8-digit order number 
from the customer's confirmation email."
```
The richer description helps the model choose the right tool for the right query and use the correct parameters.

### 4.3 The ReAct Agent Loop

**ReAct (Reasoning + Acting)** is the canonical pattern for AI agents. The agent alternates between reasoning (thinking about what to do) and acting (calling a tool), with each action informing the next round of reasoning.

**The loop in full:**

```
Task: "Check if order #12345 is at risk of being late 
       and draft a proactive message to the customer."

Step 1 — Reason:
  "I need to know the order status. I'll call get_order_status."

Step 2 — Act:
  Tool call: get_order_status(order_id="12345")
  Result: {status: "in_warehouse", ship_date: "2026-06-22", 
           carrier: "FedEx", estimated_delivery: "2026-06-24"}

Step 3 — Reason:
  "Ship date is tomorrow. I should check current FedEx delays 
   to assess late delivery risk."

Step 4 — Act:
  Tool call: get_carrier_delays(carrier="FedEx", region="UK")
  Result: {delay_status: "2-day delay on standard services", 
           effective_date: "2026-06-21"}

Step 5 — Reason:
  "2-day delay means delivery by 26 June instead of 24 June. 
   The order is at risk of being late. I have enough to draft 
   the customer message now."

Step 6 — Generate final response:
  "Order #12345 is at moderate risk of a 2-day delay due to current 
   FedEx service disruptions. Here is a draft customer message:
   
   Subject: Update on your RetailCo order #12345
   Dear [Customer], we want to give you advance notice that your order 
   may arrive slightly later than our original estimate of 24 June..."
```

This took 2 tool calls, 3 LLM reasoning steps, and produced an output that a single LLM call could never have produced — because the information about FedEx delays wasn't in the model's training data; it required a live tool call.

**The six production failure modes:**

> **Explain Like I'm an Architect**
>
> These failure modes are the equivalent of concurrency bugs in multi-threaded code — they're subtle, non-deterministic, and often don't show up in simple tests. Each one is a real production incident pattern:
>
> - **Infinite loop** — the agent keeps asking the same tool for the same data because it's never satisfied with the answer. Like a process spinning on a lock that's never released. The fix is a maximum step count, just like a timeout.
>
> - **Context overflow** — each tool call result gets added to the conversation context. A long workflow with rich tool outputs fills the 128K context window. The model starts losing its earlier reasoning, like RAM filling up and the system starting to swap. Budget context like you budget memory.
>
> - **Goal drift** — the agent starts pursuing a sub-goal so intently it forgets the original task. Like a developer who starts fixing a related bug while implementing a feature and ships neither. Periodically re-anchor the agent to the original task in the system prompt.
>
> - **Overconfident completion** — the agent reports success without actually finishing. Like a contractor who emails "job done" but only completed 80% of the work. Add a verification step: "before marking complete, confirm each required action was taken."
>
> Plan for all six before deployment. They are not edge cases — they are the normal failure modes of agentic systems in production.

| Failure mode | What happens | Mitigation |
|---|---|---|
| **Infinite loop** | Agent calls the same tool repeatedly without progress | Loop detection: flag if identical tool call appears > 3 times; max step limit |
| **Tool error spiral** | Tool returns an error; agent retries without backing off | Circuit breaker on tool calls; explicit error handling instruction in system prompt |
| **Context overflow** | Tool results fill the context window; agent loses earlier reasoning | Context budget management; summarise older steps; limit tool response size |
| **Hallucinated tool call** | Agent calls a tool that doesn't exist or with wrong parameter names | Strict schema validation on tool calls; return clear error if tool unknown |
| **Goal drift** | Agent pursues a sub-goal that diverges from the original task | Include the original task in every reasoning step; periodically re-anchor to goal |
| **Overconfident completion** | Agent stops and reports success without actually completing the task | Include a verification step: "before responding, confirm each required action was completed" |

### 4.4 Multi-Agent Architecture Patterns

A single agent has limits — context window, tool permission scope, reasoning depth. Multi-agent architectures distribute work across specialised agents.

**Pattern 1 — Orchestrator + Specialist**
A manager agent decomposes the task, delegates sub-tasks to specialist agents, and synthesises the results.

```
User task: "Analyse this month's supply chain performance 
            and identify the top 3 improvement opportunities."

Manager Agent:
  ├── Delegates to: On-Time Delivery Agent (OMS + carrier data tools)
  ├── Delegates to: Cost Analysis Agent (ERP + finance tools)  
  └── Delegates to: Supplier Performance Agent (supplier data tools)
  
Each specialist runs independently and returns a structured report.
Manager synthesises the three reports into a unified recommendation.
```

Benefits: each specialist has a narrow tool permission set (reduced blast radius), can run in parallel (faster), and can be tested independently.

**Pattern 2 — Sequential Pipeline**
Agents in a chain, where each agent's output is the next agent's input.

```
Document → Extraction Agent → Validation Agent → Enrichment Agent → Output
```

Use when: each step requires different tools or domain expertise, and the output of one step must be verified before passing to the next.

**Pattern 3 — Critic / Verifier**
A generator agent produces an output; a separate critic agent evaluates it.

```
Draft Agent → produces initial response
Critic Agent → evaluates for accuracy, policy compliance, tone
  → approves or returns to Draft Agent with specific feedback
```

Use when: output quality is critical and the cost of a verification pass is worth the quality improvement.

**Pattern 4 — Parallel Explorers + Synthesiser**
Multiple agents explore different aspects of a problem simultaneously; a synthesiser combines their findings.

```
Task: "Should we switch OMS providers?"

Parallel:
  Agent A: Technical capabilities assessment
  Agent B: Cost and licensing analysis  
  Agent C: Integration complexity assessment
  Agent D: Vendor risk and support assessment

Synthesiser: Combines all four assessments into a recommendation
```

Use when: the problem has multiple independent dimensions that can be researched simultaneously without coordination.

### 4.5 The Agent Protocol Stack — MCP, A2A, AG-UI

The agent protocol stack is the emerging set of open standards for how agents connect to tools, other agents, and humans. Think of it as the "OSI model for agents" — each protocol addresses a different layer of interoperability.

> **Explain Like I'm an Architect**
>
> Before REST became the standard for web APIs (circa 2005–2010), every enterprise integration was bespoke: SOAP, proprietary message formats, custom authentication. Integrating two systems was weeks of work. After REST became the standard, integration patterns were reusable — you knew the shape of the contract before you started.
>
> Agent protocols are at the same inflection point today. MCP, A2A, and AG-UI are solving three different integration layers:
>
> | Problem | Protocol | Analogy |
> |---|---|---|
> | How does an agent call a tool? | **MCP** | USB-C standard: one plug, any device |
> | How does one agent delegate to another? | **A2A** | SWIFT for inter-bank transfers: standard message format for passing work between organisations |
> | How does an agent show its progress to a human? | **AG-UI** | SSE/WebSocket for streaming: standard event format for streaming progress and requesting approvals |
>
> The architectural implication: tools and agents built to these standards today are infrastructure assets. They can be reused by any future agent without re-integration work. Building to proprietary frameworks instead means rebuilding integrations every time you add a new agent capability or switch providers.

**MCP (Model Context Protocol)**
*What it does:* defines how agents discover and invoke tools.
*Analogy:* USB-C for agent tools — a standard plug that works regardless of which agent framework or LLM is running.
*Why it matters architecturally:* tools built to MCP standard can be registered once and used by any agent. Your OMS integration, your Confluence connector, and your email tool are built once, not once per agent team.

```
MCP Server (exposes tools):
  Tools: [get_order_status, create_refund, send_email, ...]
  Each with: name, description, parameter schema, auth requirements

MCP Client (agent framework):
  Discovers available tools from server
  Calls tools via standard MCP protocol
  Works with any LLM: GPT-4o, Claude, Llama, etc.
```

**A2A (Agent-to-Agent Protocol)**
*What it does:* defines how agents discover and delegate to other agents.
*Analogy:* the standard escalation procedure that lets any manager in the organisation delegate to any other manager without knowing how their team works internally.
*Why it matters:* enables composable multi-agent systems. Your customer service agent can delegate to your logistics specialist agent without either knowing about the other's internal implementation.

```
Agent A (customer service) receives task it can't complete alone
  → Queries A2A registry: "is there an agent that can handle logistics?"
  → Finds Logistics Agent, sends delegation request
  → Logistics Agent executes, returns result
  → Customer Service Agent incorporates result and responds to user
```

**AG-UI (Agent-User Interface Protocol)**
*What it does:* defines the streaming interface between an agent workflow and a human-facing UI.
*Why it matters:* standardises how agent progress, tool calls, intermediate results, and HITL approval requests are streamed to the user interface — so UI components can be built once and work with any agent framework.

```
Agent workflow streams events:
  → thinking: "Checking order status..."
  → tool_call: get_order_status(12345)
  → tool_result: {status: "shipped"...}
  → approval_required: "Refund £450 — requires supervisor approval"
  → awaiting_approval
  → approval_received
  → final_response: "Refund of £450 has been approved..."

UI renders each event type appropriately — progress indicator, 
tool call log, approval dialog, final response
```

**The complete stack:**

```
Human / Application
      │ AG-UI (streaming UX events)
      ▼
Agent Framework (LangGraph, CrewAI, custom)
      │ A2A (agent-to-agent delegation)
      ▼
Other Agents (specialists, sub-agents)
      │ MCP (tool invocation)  
      ▼
Tool Servers (OMS, CRM, knowledge base, email...)
      │
      ▼
Enterprise Systems
```

---

## 5. Enterprise Example

**Scenario: Order Exception Handling Agent at a Retail Company**

Customer contacts support: "I've been waiting 3 weeks for my order #OD-78234. I want an update and compensation."

This is a multi-step task: look up the order, diagnose the delay, check compensation policy, calculate appropriate offer, draft a response. A single LLM call cannot do this. An agent can.

**System prompt design:**

```
You are a customer service resolution specialist for RetailCo.

YOUR ROLE: Resolve customer order issues by investigating the root cause, 
applying our compensation policy, and communicating with the customer 
professionally and empathetically.

YOUR TOOLS:
- get_order_details: look up any order by order ID
- get_carrier_history: check shipment tracking history
- get_compensation_policy: retrieve our current compensation guidelines
- create_compensation_offer: generate a compensation offer in our system
- draft_customer_email: prepare a response email for human review

BOUNDARIES:
- Compensation offers above £100 require supervisor approval (use the 
  create_compensation_offer tool and it will route appropriately)
- Never promise a specific delivery date you cannot confirm from tracking data
- Never reveal internal system IDs or carrier account details
- If the order has a fraud flag, stop and escalate to the fraud team

ESCALATION: If you cannot resolve the issue with your available tools, 
say "I'm transferring you to a specialist" and create an escalation ticket.
```

**Agent execution trace:**

```
Step 1 → get_order_details(order_id="OD-78234")
Result: {status: "in_transit", order_date: "2026-05-28", 
         expected_delivery: "2026-06-05", carrier: "Hermes",
         last_scan: "2026-06-02", scan_location: "Birmingham depot"}

Step 2 → Reason: Order is 18 days past expected delivery. 
         Last scan was 19 days ago. Need carrier history.

Step 3 → get_carrier_history(tracking_id="HRM-99234")
Result: {scans: [{date: "2026-06-02", status: "arrived_depot"}, 
                  {date: "2026-06-02", status: "sorting_error_flagged"}],
         carrier_note: "Item misrouted, located at Birmingham. 
                       Rescheduled delivery attempt 2026-06-24."}

Step 4 → Reason: Carrier error caused the delay. 
         Need to check compensation policy for carrier-fault delays.

Step 5 → get_compensation_policy(reason="carrier_fault", 
                                  delay_days=18, order_value=85.00)
Result: {eligible: true, 
         compensation_range: "£10-£25 store credit for delays > 14 days",
         escalation_threshold: "£100+"}

Step 6 → Reason: Eligible for compensation. Offer mid-range (£15) 
         given 18-day delay and confirmed carrier fault.
         Below £100 threshold — can proceed without supervisor.

Step 7 → create_compensation_offer(order_id="OD-78234", 
                                    amount=15.00, type="store_credit",
                                    reason="carrier_fault_delay")
Result: {offer_id: "CO-4521", status: "created"}

Step 8 → draft_customer_email(...)
Result: email draft created for human review

Final response to agent interface: 
"I've investigated your order OD-78234. I found that a sorting error at 
the carrier's Birmingham depot caused the delay. Your order is now 
scheduled for delivery on 24 June. As an apology for the inconvenience, 
I've arranged a £15 store credit to your account. You'll receive a 
confirmation email shortly. Is there anything else I can help with?"
```

**What the architecture enabled:**
- 5 tool calls, 4 reasoning steps, 8 seconds end-to-end
- Compensation policy was applied consistently — same policy logic for every similar case
- Compensation amount was below the HITL threshold — no human needed
- Full audit trail: every tool call, reasoning step, and final output logged with the case ID
- The draft email goes to a human review queue before it's sent to the customer

---

## 6. Architecture Perspective

### When to Use Agents vs Single LLM Calls

This is the most consequential design decision in AI application architecture. Get it wrong and you either under-build (a complex task fails because the model can't do it in one call) or over-build (a simple Q&A becomes an agent with all the complexity that entails).

**Decision framework:**

> **What is a token?** A token is the basic unit of text that LLMs process — and the unit that APIs charge for. Roughly 3–4 characters or 0.75 words in English. "Hello world" = 2 tokens. 1,000 tokens ≈ 750 words ≈ 1.5 pages. APIs charge separately for **input tokens** (your prompt) and **output tokens** (the model's response). When you see pricing like "$2 per million tokens", that is the cost per million of these text chunks.

| Signal | Single call | Agent |
|---|---|---|
| Task requires live data | ❌ Use function calling (still single call with tool) | — |
| Task requires multiple sequential tool calls | — | ✅ |
| Output depends on intermediate results | — | ✅ |
| Task can be fully specified upfront | ✅ | — |
| Task requires exploration / decision at runtime | — | ✅ |
| Latency SLA < 2 seconds | ✅ | ❌ (agents are slower) |
| Cost must be minimised | ✅ | ❌ (agents use more tokens) |
| Simple, deterministic task | ✅ | — |

**The common mistake:** building an agent when a single call with a well-designed prompt and one or two tool calls would suffice. Agents introduce non-determinism, variable cost, loop risk, and observability complexity. The simplest architecture that meets the requirement is always preferred.

**The progression:** start with a single LLM call. Add function calling when the model needs live data. Add an agent loop only when the task genuinely requires multi-step reasoning where each step depends on the previous.

### Vendor SDK Selection in 2026

| Framework | Best for | Avoid when |
|---|---|---|
| **LangGraph** | Complex stateful workflows, human-in-loop gates, durable task queues | Simple single-agent use cases (overkill) |
| **CrewAI** | Multi-agent orchestration with defined roles, fast to prototype | Production enterprise deployments (less mature observability) |
| **AutoGen (Microsoft)** | Code execution agents, developer tooling agents | Non-technical workflows |
| **Semantic Kernel** | Microsoft/Azure stack, enterprise C# or Python | Non-Microsoft environments |
| **Custom / minimal** | When you need full control over the loop, or existing frameworks add too much abstraction | When you need to move fast (framework handles boilerplate) |

**Practical advice for architects:** evaluate frameworks on three criteria for your use case — (1) does it support MCP natively? (2) does it have production-grade observability (OTel integration)? (3) does it support durable execution (the ability of an agent workflow to survive a process restart or a long human approval pause and resume from exactly where it stopped, rather than starting over — critical for multi-hour or multi-day enterprise workflows)? In 2026, LangGraph leads on all three for enterprise deployments.

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — System prompt design**

A developer proposes writing the system prompt as: "Be helpful, answer customer questions about orders and products, and be polite." What are the three most important things missing from this system prompt for a production customer service agent?

> **Simple Explanation:** "Be helpful and polite" is like an employee handbook that only says "do your job well and be nice to customers." It tells the new hire nothing about what they're actually allowed to do, what to do when a situation is outside their authority, or how to present information. You'd never accept that as an onboarding document. Don't accept it as a system prompt.
>
> **Detailed Answer:** (1) **Explicit boundaries** — what the agent cannot do or discuss. Without this, the model will attempt to answer anything, including competitor questions, speculation about future promotions, internal system details, or medical/legal advice tangentially related to a product. "Be helpful" means the model will try to help with everything. (2) **Escalation instructions** — when should the agent transfer to a human? What triggers escalation? Without this, the agent either refuses edge cases abruptly or attempts to resolve situations it cannot handle safely. (3) **Output format and behavioural specification** — how should the agent respond? What tone? Should it ask for an order ID before looking anything up? Should it draft emails or send them? How long should responses be? "Be polite" is not a format specification. These three gaps produce inconsistent, unpredictable behaviour at scale — different users receive different experiences based on how their query phrase happens to land.
>
> **Architecture Takeaway:** The system prompt is an engineering artifact, not a creative writing exercise. Treat it with the same rigour as an API specification: define the role (what it does), the scope (what it handles), the boundaries (what it refuses), the escalation conditions (what it hands off), and the output contract (format, length, tone). Version-control it alongside application code. Review it when the model version changes.

---

**Question 2 — Agent loop failure**

An order management agent is looping — it keeps calling `get_carrier_status` repeatedly for the same order without progressing. Walk through the causes and the architectural mitigations.

> **Simple Explanation:** The agent is stuck in the equivalent of refreshing a web page hoping for different content — it keeps asking the same question because it doesn't know what else to do. The solution is a combination of a runtime that detects the loop (the same call appearing 3+ times) and a system prompt that gives the agent a graceful exit ("if you can't get the answer in two tries, escalate").
>
> **Detailed Answer:** **Causes:** (1) the tool is returning an error or ambiguous result the agent is retrying; (2) the agent's reasoning is stuck — it concludes it needs more carrier data each time, gets it, but cannot determine what to do with it (perhaps the system prompt doesn't give it an exit condition for unavailable data); (3) a hallucinated expectation — the model expects a field in the tool response that doesn't exist and keeps retrying hoping it will appear. **Mitigations:** (1) **Loop detection in the runtime** — if the same tool is called with identical arguments more than N times (typically 3), flag as a loop and escalate; this is the primary control. (2) **Circuit breaker** — if the tool returns errors N times in a row, fail fast with a structured error rather than retrying indefinitely. (3) **Explicit exit conditions in the system prompt** — "If you cannot determine carrier status after two attempts, inform the customer you are investigating and create a follow-up ticket." (4) **Max step limit** — no agent task should exceed a configured maximum number of steps before it escalates to human review.
>
> **Architecture Takeaway:** Loop detection is a mandatory agent runtime control — not a post-launch optimisation. Define loop detection thresholds, circuit breaker conditions, and max step limits during agent design. These are the agentic equivalent of HTTP timeouts and retry policies. No production agentic system should be deployed without them.

---

**Question 3 — MCP economics**

What is the Model Context Protocol (MCP) and how does it change the economics of tool development for enterprise AI teams?

> **Simple Explanation:** Before USB-C, every device had its own charger. The economics were terrible: every new device meant a new charger to buy, carry, and manage. After USB-C, one cable works for everything. MCP is USB-C for agent tools. Before MCP: every team rebuilds the same integrations. After MCP: build once, use everywhere.
>
> **Detailed Answer:** MCP is an open standard interface for how agents discover and invoke tools. It defines a standard contract — tool name, description, parameter schema, authentication — so a tool built once can be used by any agent regardless of which LLM framework or model is running. **Before MCP:** five teams each building an agent that needs OMS access means five separate OMS integrations, each with its own authentication handling, error handling, rate limiting, and documentation. At 10 teams × 20 enterprise systems = 200 bespoke point-to-point integrations to build and maintain. **After MCP:** build the OMS MCP server once, register it in the tool registry, all 10 teams (and every future team) use the same integration. The integration count is O(systems), not O(teams × systems). The governance benefit compounds the economic benefit: one integration point means one place to enforce authentication, rate limits, audit logging, and blast radius controls.
>
> **Architecture Takeaway:** MCP tool development is infrastructure investment that compounds. Identify the top 5–10 enterprise systems that agents will most commonly need to access (OMS, CRM, knowledge base, email, finance). Build their MCP servers as shared infrastructure. Every subsequent agent built at the company benefits from these investments. This is the same compounding logic that made a well-designed API gateway worthwhile — the investment is justified by the reuse.

---

**Question 4 — Multi-agent access control**

You are designing a multi-agent system where a Manager Agent delegates to three specialist agents (Order, Logistics, Customer Comms). The security team asks about data access controls. What architectural principle governs how you assign tool permissions, and how does multi-agent architecture help enforce it?

> **Simple Explanation:** You wouldn't give every employee in the building a master key to every room just because it's more convenient. You give them access to the rooms they need for their job. The same principle applies to AI agents. Breaking one large agent into smaller specialist agents isn't just about efficiency — it's how you limit the blast radius when something goes wrong.
>
> **Detailed Answer:** The principle is **minimal privilege** — each agent should have access only to the tools and data it needs for its specific function. The Order Agent gets OMS read/write tools only. The Logistics Agent gets carrier API and WMS tools only. The Customer Comms Agent gets email and notification tools only — but no access to order financial data. No single agent has permissions across all systems. Multi-agent architecture enforces this naturally by decomposing the task: because each specialist does only one type of work, it only needs one category of tools. This dramatically reduces blast radius: if the Customer Comms Agent is manipulated by a prompt injection attack, it can send emails — but it cannot access order financial data or initiate refunds. Compare to a monolithic agent with all permissions: a single successful attack has full blast radius across all enterprise systems. The tool registry enforces these boundaries at the infrastructure layer so no application code can accidentally grant broader access.
>
> **Architecture Takeaway:** Design the permission matrix before you design the agents. For every agent role, answer: which tools can it call? What data can it read? What state can it write? What financial limits apply? Define this in the tool registry before any agent code is written. Security and blast radius are architecture decisions — they cannot be retrofitted cleanly after agents are in production.

---

**Question 5 — Chain-of-Thought prompting**

Explain Chain-of-Thought prompting, when it improves results, and when it doesn't help (or can hurt).

> **Simple Explanation:** Asking someone to "show their working" helps when the problem has multiple steps where getting intermediate steps wrong leads to the wrong final answer. It doesn't help when the answer is obvious and immediate — you wouldn't ask someone to show their working for "what's 2+2?" You'd just ask for the answer. The same logic applies to LLMs: CoT for complex reasoning, direct instruction for simple tasks.
>
> **Detailed Answer:** Chain-of-Thought (CoT) prompting instructs the model to reason step by step before giving its final answer — either explicitly ("think step by step") or by example (showing input → reasoning → answer in few-shot examples). **When it improves results:** multi-step reasoning tasks; arithmetic and calculation; logical inference; tasks where the correct answer depends on intermediate conclusions (e.g., "is this refund request within our 30-day policy?" requires computing the date difference before answering). The intermediate reasoning gives the model "scratch space" to work through complexity before committing to an answer — like asking an analyst to show their working rather than just giving a number. **When it doesn't help or hurts:** simple factual lookups ("what is the capital of France?"); classification tasks where the answer is immediate; structured data extraction with a clear schema; high-volume tasks where the added output tokens are a significant cost. It can actively hurt when the model "reasons itself into the wrong answer" — the intermediate steps contain an error that the model then builds on, producing a wrong conclusion it wouldn't have reached without the CoT scaffold. **Cost implication:** CoT significantly increases output token count — every reasoning step is billed at output token prices. For high-volume tasks, CoT adds cost without adding value if the task doesn't require multi-step reasoning.
>
> **Architecture Takeaway:** CoT is a configuration choice with a cost implication, not a default improvement. Classify your use cases: extraction, classification, and formatting → no CoT needed, keep it cheap. Multi-step reasoning, policy interpretation, and complex calculations → CoT dramatically improves accuracy and is worth the token cost. Never apply CoT uniformly across an entire system without evaluating whether each task type actually benefits.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section is for architects ready to evaluate agent frameworks and implement production agent systems. It is safe to skip on a first pass and return here later.

### 8.1 LangGraph: Stateful Multi-Agent Workflows

LangGraph is the most widely used framework for building production-grade stateful agent workflows. Its core abstraction: a workflow is a **directed graph** where nodes are agent steps (LLM calls or tool calls) and edges define the flow between them — including conditional branches and loops.

**Why the graph abstraction matters:**
- Cycles are first-class: LangGraph supports loops (the ReAct loop is literally a cycle in the graph)
- Conditional routing: edges can carry conditions — "if the agent decided to escalate, go to the escalation node; otherwise continue"
- State is explicit: the graph maintains a typed state object that every node can read and update — no implicit context drift
- Checkpointing: LangGraph can checkpoint the graph state at each node, enabling durable execution (the agent can resume after a crash, restart, or human approval pause)

**Minimal LangGraph agent structure:**
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated

class AgentState(TypedDict):
    messages: list          # conversation history
    tool_calls_made: int    # loop detection counter
    task_complete: bool

def should_continue(state: AgentState):
    if state["task_complete"]:
        return END
    if state["tool_calls_made"] > 10:  # loop guard
        return "escalate"
    return "agent"

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_llm)
workflow.add_node("tools", execute_tools)
workflow.add_node("escalate", escalate_to_human)

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")  # tools always return to agent

graph = workflow.compile(checkpointer=memory_checkpointer)
```

The `checkpointer` is what enables durable execution — state is persisted at each node, so a HITL pause or process restart can resume from exactly where it stopped.

### 8.2 Agent Evaluation Benchmarks

When selecting or comparing agent-capable models, these are the benchmarks that appear in enterprise model evaluations:

| Benchmark | What it measures | Why it matters |
|---|---|---|
| **GAIA** | Multi-step real-world task completion | Tests end-to-end agent capability on realistic tasks |
| **SWE-Bench** | Software engineering tasks (fixing GitHub issues) | Proxy for code agent capability |
| **ToolBench** | Tool selection and invocation accuracy | Directly tests function calling quality |
| **τ-bench** | Multi-turn tool-use in simulated environments | Tests agent behaviour over long horizons |
| **AgentBench** | Agent performance across 8 environments | Breadth coverage |

**What to ask vendors:** "What is your model's GAIA score at the L2 level?" L2 tasks require 5–10 tool calls and moderate reasoning. A model that scores well at L2 is practically useful for enterprise agent tasks. L3 (more complex) is relevant for the most demanding agent workflows.

**The calibration caveat:** benchmark scores are measured on public test sets. Models may have been trained on benchmark-adjacent data. Always evaluate on your own golden test set in addition to published benchmarks.

### 8.3 Modern Agent Loop — Reference Pseudocode

The minimal production-grade agent loop, including all the defensive patterns:

```python
async def run_agent(task: str, config: AgentConfig) -> AgentResult:
    state = AgentState(
        messages=[SystemMessage(config.system_prompt), 
                  HumanMessage(task)],
        step_count=0,
        tool_calls=[]
    )
    
    while True:
        # Guard: max steps
        if state.step_count >= config.max_steps:
            return AgentResult(status="max_steps_exceeded", 
                             escalate=True)
        
        # Guard: budget
        if state.token_cost > config.budget_cap:
            return AgentResult(status="budget_exceeded", 
                             escalate=True)
        
        # LLM call (through model gateway)
        response = await model_gateway.complete(
            messages=state.messages,
            tools=tool_registry.get_permitted_tools(config.agent_role),
            model=config.model_tier
        )
        
        state.step_count += 1
        state.token_cost += response.usage.total_tokens
        
        # Final answer — done
        if response.finish_reason == "stop":
            return AgentResult(status="complete", 
                             output=response.content)
        
        # Tool call requested
        if response.finish_reason == "tool_calls":
            for tool_call in response.tool_calls:
                
                # Guard: loop detection
                if state.tool_calls.count(tool_call.signature) >= 3:
                    return AgentResult(status="loop_detected", 
                                     escalate=True)
                
                # Guard: HITL check
                if requires_approval(tool_call, config):
                    approval = await request_human_approval(tool_call)
                    if not approval.approved:
                        state.messages.append(
                            ToolMessage("Action not approved by supervisor.")
                        )
                        continue
                
                # Execute tool (via MCP)
                try:
                    result = await mcp_client.call_tool(
                        tool_call.name, 
                        tool_call.arguments,
                        timeout=config.tool_timeout_ms
                    )
                except ToolError as e:
                    result = f"Tool error: {e}. Do not retry."
                
                # Circuit breaker check
                if circuit_breaker.should_open(tool_call.name):
                    return AgentResult(status="tool_unavailable", 
                                     escalate=True)
                
                state.tool_calls.append(tool_call.signature)
                state.messages.append(ToolMessage(result))
                
                # Log for audit
                audit_log.record(task_id, tool_call, result)
```

---

## 9. Key Takeaways (5 Bullets)

- **Prompting is a design decision, not a developer task.** The system prompt defines the model's role, boundaries, escalation behaviour, and output contract. A poorly designed system prompt produces inconsistent behaviour at scale. Write it with the same rigour you'd apply to an API specification.

- **Function calling is the bridge between LLMs and enterprise systems — and the model never directly touches your systems.** The model outputs a structured request; the application executes it. This separation is the correct security boundary. Tool descriptions are part of your system design — write them with the same care as API documentation.

- **The ReAct loop is the foundation of all agents.** Reason → Act → Observe → Repeat. Every agent framework is an implementation of this loop with different abstractions on top. The six production failure modes (infinite loop, tool error spiral, context overflow, hallucinated call, goal drift, overconfident completion) apply to every agent regardless of framework.

- **MCP/A2A/AG-UI is the standardisation moment for agents.** MCP makes tools reusable across agents. A2A makes agents composable with other agents. AG-UI makes agent workflows accessible to humans. Building tools to MCP standard today means every future agent benefits from work done once — the economics shift from O(agents × tools) to O(tools).

- **Use agents only when the task genuinely requires multi-step reasoning with runtime decisions.** Simple tasks done with an agent incur unnecessary cost, latency, and complexity. The progression is: single LLM call → single call with function calling → agent loop. Start simple and move right only when the task requires it.
