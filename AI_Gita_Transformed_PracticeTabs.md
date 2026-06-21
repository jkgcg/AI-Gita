# How to Use AI Gita — Guide for Solution Architects

> **Who this is for:** Solution Architects, Enterprise Architects, Integration Architects, and Technical Leads with no prior AI/ML background who are using AI Gita to build working AI knowledge for enterprise architecture decisions.

---

## 1. What Is It (Plain English)

AI Gita is a 35-tab learning platform covering the full AI and LLM landscape — from mathematical foundations to production governance. It is not a course you read front to back. It is a **reference platform with five types of tabs**, each serving a different purpose.

**The five tab types:**

| Type | Tabs | What they are for |
|---|---|---|
| **Learning modules** | AI Landscape, LLMs, Deep Learning, RAG, Agents, Fine-Tuning, Safety, Governance, and 16 others | Progressive 9-section learning: each teaches one domain from intuition to architecture decision |
| **Navigation** | Start Here, Quick Guide, Role Paths | Where to start, which tabs to read for your role, and how to sequence your learning |
| **Practice** | Q&A Vol 1–3, Interview Strategy, Live Coding | Active recall practice for 160 AI interview questions |
| **Reference** | Glossary, AI Snapshot | Look up a term or check current model pricing without re-reading a full module |
| **Career** | AI Career Path | Understanding the AI career landscape for architects moving into AI roles |

> **Explain Like I'm an Architect:** Think of AI Gita like a well-structured enterprise architecture framework (TOGAF, Zachman). You do not read the entire framework front to back. You read the section relevant to your current decision. When you are designing an integration, you go to the integration patterns section. When you need a governance model, you go there. AI Gita works the same way — use the Role Paths and Quick Guide to find your section, then go deep.

---

## 2. For Solution Architects — Start Here

**The 8 tabs that give architects the most decision-making leverage:**

| Priority | Tab | What it gives you |
|:---:|---|---|
| 1 | **AI Landscape** | Model selection framework, build vs buy criteria, the 2026 stack |
| 2 | **LLMs & Foundation** | How LLMs work — enough to make architecture decisions and not be misled |
| 3 | **System Design** | LLM system architecture patterns, latency/cost tradeoffs, request flow design |
| 4 | **Agents & Prompting** | How agentic systems work, MCP protocol, function calling, production failure modes |
| 5 | **RAG & Vector Databases** | Retrieval-augmented generation — the pattern behind most enterprise AI deployments |
| 6 | **AI Infrastructure** | GPU costs, inference serving, quantisation — why infrastructure is different for AI |
| 7 | **Safety & Ethics** | Hallucination, prompt injection, RLHF alignment — what can go wrong and how to govern it |
| 8 | **AI Governance** | EU AI Act, NIST RMF, risk tiers — your compliance and governance framework |

**Recommended reading order for a Solution Architect with no AI background:**

```
Week 1:  AI Landscape → LLMs & Foundation → Generative AI
Week 2:  RAG & Vector → Agents & Prompting → Agentic Platform
Week 3:  System Design → AI Infrastructure → MLOps / LLMOps
Week 4:  Safety & Ethics → AI Governance → People & Adoption
```

> **Explain Like I'm an Architect:** This is your critical path. Just as you would not design a microservices architecture without first understanding the domain model and the integration patterns, you should not design an AI system without first understanding how LLMs work (LLMs tab), how to ground them in your data (RAG tab), and how to keep them governable (Governance tab). The four-week sequence above gives you that foundation in the right order.

---

## 3. The Navigation Tabs

### Start Here
The onboarding tab. Select your role (Solution Architect, Enterprise Architect, AI Engineer, etc.) and it generates a personalised study plan with a weekly sequence and progress tracking. **Use this tab first**, before anything else.

**What it gives architects specifically:**
- A filtered view showing only the tabs relevant to architect roles
- A week-by-week plan calibrated for someone with no AI background
- A "Non-Negotiable Tabs by Role" reference — the minimum viable reading list for your role

### Quick Guide
One-page orientation hub for when you are lost or need a fast answer. Contains:
- **8 mental models** that make the rest of the platform click — read these first
- **Use-case quick routes** — "Build an AI Chatbot", "Design an Agent Platform", "Prepare for AI Interviews" — each a 4-tab ordered sequence
- **"Where am I lost?"** troubleshooter — maps specific problems ("I don't understand why RAG exists", "I can't explain attention") to the exact tab that solves them

> **The 8 mental models summarised for architects:**
> 1. **LLM = next-token slot machine.** It predicts the most statistically likely next word. It does not understand. It does not verify. It produces the most *plausible* text — which is often correct but not guaranteed to be.
> 2. **Context window = whiteboard.** Everything the model can see at once. When it fills, earlier content is forgotten. 128K–1M tokens ≈ 90K–750K words. This is your working memory budget.
> 3. **RAG > long-context > fine-tune — usually.** For enterprise knowledge integration, retrieval is cheaper, safer, and more governable than either long prompts or model retraining.
> 4. **Agents = LLM + loop + tools.** An agent is just an LLM that can call tools and run multiple times until done. Everything else is infrastructure to make that loop safe and governable.
> 5. **Embeddings = meaning as coordinates.** Text converted to numbers such that similar meanings land close together in space. The foundation of semantic search and RAG.
> 6. **Tokens = billing unit.** 1 token ≈ ¾ of an English word. APIs charge per token (input and output separately). Token count drives both cost and context window consumption.
> 7. **Fine-tuning ≠ teaching the model new facts.** It adjusts *behaviour and style*, not knowledge. For new facts and current data, use RAG. For consistent format, tone, or task structure, use fine-tuning.
> 8. **Hallucination is structural, not a bug.** The model generates the most plausible next token — it has no mechanism to verify truth. Architect accordingly: retrieval grounding, output validation, human-in-the-loop for high-stakes outputs.

### Role Paths
Curated sequences for specific outcomes — "ship RAG in a weekend", "prepare for a frontier-model interview", "become MLOps-fluent". Each is an ordered list of tabs with progress tracking. **Use when you have a specific deliverable in mind** rather than building broad knowledge.

---

## 4. The Practice Tabs

### Q&A Volumes 1–3 (160 Questions)

160 AI interview questions organised in three volumes by difficulty:
- **Vol 1 (Q1–Q60):** Foundations and core concepts — LLMs, ML basics, RAG, Agents
- **Vol 2 (Q61–Q103):** Applied and systems — production architecture, trade-off decisions
- **Vol 3 (Q104–Q160):** Advanced and production — enterprise deployment, governance, edge cases

**How to use them correctly (active recall, not passive reading):**

> **Do not read the answers first.** Read the question. Attempt your own answer in your head or on paper. Then reveal the answer and compare. The gap between what you said and what the answer says is exactly where your learning is. Passive reading feels productive but does not build durable recall. Active recall does.

**For architects:** Each question is tagged by role (ARCHITECT, ML ENG, AI ENG, etc.). Filter to ARCHITECT first. The architect-relevant questions focus on: system design decisions, trade-off rationale, governance and compliance, cost estimation, and technology selection. Deep ML engineering questions (implement backpropagation, write a PyTorch training loop) are tagged ML ENG and can be skipped unless you want full coverage.

**Answer quality calibration (used across all three volumes):**

| Level | What it looks like |
|---|---|
| **Weak** | Names the concept correctly but cannot explain it, gives a one-liner, cannot discuss trade-offs |
| **Solid** | Explains the mechanism clearly, can discuss when to use it and when not to |
| **Senior/Architect** | Frames as a system design decision with trade-offs, costs, failure modes, and governance implications — not just "what it is" but "how I would architect for it" |

### Interview Strategy

Covers what standard prep guides skip: how FAANG and enterprise AI interviews are actually scored, how to handle system design questions for AI systems, STAR templates with AI-specific behavioural scenarios.

**Architect-specific sections to prioritise:**
- "Design an AI system for X" — how to structure your answer as a decision tree (data? RAG? agents? governance tier?)
- Trade-off conversations — how to present model selection rationale without sounding like a vendor pitch
- Handling "what would you do if the model hallucinated?" — the governance-first answer that senior interviewers are looking for

### Live Coding

Six canonical AI algorithm implementations interviewers ask for: Multi-Head Attention, Backpropagation, K-Means, BPE Tokenizer, VAE, and Transformer Block.

> **Note for architects:** Live coding interviews in this depth are standard for ML Engineer and AI Engineer roles. For Solution Architect and Technical Lead interviews, the expectation is conceptual understanding of these algorithms — not implementation from memory. Use this tab to build intuition, not to memorise syntax. The "what does this prove you understand" section for each implementation is the part most relevant to architects.

---

## 5. The Reference Tabs

### Glossary

74 terms defined for Solution Architects and Enterprise Architects — each with a one-sentence plain-English definition, a "why it matters architecturally" note, and a cross-reference to the tab that covers it in depth.

**How to use it:** When you encounter a term in a learning module that is not immediately clear, look it up here first before going to an external source. The glossary is calibrated for this audience — you will get the architect-relevant framing, not the ML engineer definition.

**The 10 terms architects are most likely to need first:**

| Term | One-liner |
|---|---|
| Token | Basic unit LLMs process and APIs charge for — roughly ¾ of a word |
| Context window | The model's working memory — maximum text it can hold at once |
| Embedding | Text converted to a list of numbers capturing its meaning |
| RAG | Retrieving relevant documents from your own systems before asking the LLM |
| Fine-tuning | Adapting a pre-trained model's behaviour (not its knowledge) on your data |
| Hallucination | The model generating plausible but incorrect content with apparent confidence |
| Inference | Running the model to get an answer (vs training, which is building the model) |
| Agent | An LLM that can use tools and loop until a task is complete |
| MCP | Model Context Protocol — the standard for connecting agents to enterprise tools |
| KV cache | The model's saved computation for prior tokens — primary driver of long-context serving cost |

### AI Snapshot

Time-sensitive facts: current frontier model names, pricing, and benchmark comparisons. Updated as models are released. **Use this tab when you need current pricing for a cost model or a decision document** — do not use pricing figures from learning modules, which may be months old.

---

## 6. Architecture Perspective — How to Get Maximum Value

**The single most important mindset shift for architects using this platform:**

Every concept in AI Gita has two layers — the *mechanism* (how it works technically) and the *decision* (what it means for your architecture). The learning modules are structured to get you to the decision layer as quickly as possible. When reading any module, always ask:

> "Given this, what would I do differently when designing a system?"

If you cannot answer that question after reading a section, re-read the "Architecture Perspective" subsection (present in every module) — that is where the decision-layer content lives.

**A practical heuristic for Solution Architects:**

```
Reading a learning module:
  - Section 1 (What Is It):       Understand the concept in plain English
  - Section 2 (For Architects):   Find your decision levers
  - Section 4 (Core Concepts):    Build enough depth to reason about trade-offs
  - Section 5 (Enterprise Example): Anchor it in a recognisable scenario
  - Section 6 (Architecture Perspective): Distil into design principles
  - Section 7 (Self-Check):       Test whether you can articulate it
  - Section 8 (Advanced):         Optional — go here only if you need depth
```

You do not need to read Section 8 to be architecturally competent on a topic. Section 8 exists for those who need to reason about the mechanism in detail — useful when evaluating vendor claims or reviewing an ML engineer's technical proposal.

---

## 7. Self-Check — Can You Do These?

After completing the architect critical path (8 tabs above), you should be able to answer each of these without looking them up:

**LLM & Architecture:**
- Explain what a token is and why it affects both cost and system design.
- Describe the context window constraint and its implication for agent loop design.
- Explain why LLMs hallucinate and what architectural pattern addresses it.

**RAG & Knowledge:**
- Explain what an embedding is using an analogy a non-technical stakeholder would understand.
- Describe the RAG pipeline from user query to grounded LLM response in five steps.
- State when you would choose RAG over fine-tuning, and vice versa.

**Agents & Platform:**
- Describe the ReAct loop (Reason → Act → Observe → Repeat) and what breaks it in production.
- Explain what MCP is and why it changes the economics of enterprise tool development.
- Name the six planes of an Agentic Knowledge Platform and what each governs.

**Governance & Safety:**
- Name three prompt injection mitigation strategies.
- Explain what the EU AI Act's risk tier system means for a system you are designing.
- Describe what RLHF alignment is and why reward hacking is the architect's concern.

**Simple explanation:** You are ready to lead an AI architecture design session, evaluate vendor AI offerings, and hold an ML engineering team accountable for design decisions when you can answer all of the above clearly and without notes.

**Architecture takeaway:** These are not exam questions. They are the questions your CTO, your risk committee, and your client's architecture review board will ask you in 2026. The goal of AI Gita is to make your answers authoritative, not approximate.

---

## 8. Key Takeaways

- **AI Gita is a reference platform, not a linear course.** Use Role Paths to find your sequence, then go deep on the tabs that matter for your current decision.
- **The 8 mental models in Quick Guide are the fastest orientation available.** Read them before anything else.
- **The Intuition → Analogy → Example → Architecture → Technical sequence is intentional.** Every learning module is structured this way — you can stop at any layer once you have what you need.
- **Q&A active recall is the fastest route to durable knowledge.** Read the question, attempt the answer, then check. The gap is where learning happens.
- **The Glossary and AI Snapshot are your day-to-day reference tools.** Use them when you encounter unfamiliar terms or need current pricing — do not re-read full modules for a quick lookup.
- **Section 8 Advanced content is optional for architects.** You need conceptual depth and decision-layer fluency, not implementer-level detail, for most architecture work.
