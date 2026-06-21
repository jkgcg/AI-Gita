# Practice & Navigation Tabs — Improvement Notes
### Chief Learning Experience Designer Edition

> These tabs serve different purposes from the learning modules. Rather than forcing a 9-section learning format onto navigation, practice, and reference content, this document captures the specific improvements needed for each tab to fulfil its intended purpose more effectively.

---

## Tab: 📚 Start Here

**Purpose:** Onboarding — orient the learner, surface their role path, and get them into the right content as fast as possible.

**Current strengths:** Role-based personalisation is excellent. The dependency map (study in this order) is well-structured. The weekly study plan content per topic is genuinely useful.

**Improvement priorities:**

**1. Elevate the architect-specific path to the top.**
The tab currently lists 9 role paths. For the primary audience of this platform (Solution Architects, Enterprise Architects, Integration Architects), the path should appear immediately — not buried after ML Engineer, AI Engineer, Data Scientist, MLOps. Consider reordering: Architect paths first, then technical roles.

**2. The Learning Command Center is front-loaded but confusing.**
Active Recall Ratio, spaced reviews, forgetting risk — these concepts require explanation before they're useful. Consider: brief the learner on how to use the platform in 3 bullets before presenting the dashboard.

**3. The "Quick Reference: Non-Negotiable Tabs by Role" is high-value — surface it above the fold.**
This section (which tabs are must-reads for your role) answers the first question every new learner has. It should be the second thing they see, not the fifth.

**4. Clarify what "transformed" tabs are vs original content.**
As the 9-section progressive learning modules are integrated back into the HTML, the Start Here page should communicate: "The tabs marked [Learning] have been redesigned as progressive learning modules — start with those for your role path."

---

## Tab: 🎯 Quick Guide

**Purpose:** Decision support for experienced learners who need a specific answer fast — not a learning path, but a routing guide.

**Current strengths:** "Where do I go when I get stuck?" section is excellent — maps specific problems to the tab that solves them. The 8 mental models are genuinely valuable orientation content. Role-based pathways are well-structured.

**Improvement priorities:**

**1. The "8 mental models that make the rest click" should be the first content block.**
These eight mental models (LLM = Next-token slot machine, Context = working memory, RAG > long-context > fine-tune usually, etc.) are the fastest orientation available. Any learner who absorbs these 8 models understands the landscape well enough to start asking the right questions. Move to position 1.

**2. "Where do I go when I get stuck?" — add two missing links:**
- "How do I choose a cloud platform?" → Cloud Platforms tab (now transformed)
- "How do I get my team to adopt AI?" → People & Adoption tab (now transformed)

**3. The complete map diagram needs an architect-specific callout.**
The 34-tab map is comprehensive. Add a visual callout or filter: "Architects — these 8 tabs are your critical path" (AI Landscape, System Design, Agents & Prompting, RAG & Vector, Infrastructure, Governance, Safety & Ethics, People & Adoption).

**4. Week-by-week study plan — add architect variant.**
The study plan paces through ML fundamentals before getting to LLM content. For architects with no ML background, a reordered path starting with AI Landscape → LLMs & Foundation → System Design → Agents → RAG is more immediately applicable. Consider adding a "Solution Architect" pace option alongside the existing Fast/Standard/Deep pacing.

---

## Tab: 🌎 AI Landscape

**A full 9-section transformation has been written:** `AI_Gita_Transformed_AILandscape.md`

The original tab's strengths (Open-weight vs Closed enterprise framework, Build vs Prompt vs Fine-tune vs Train, AI Capability Map) are preserved and significantly expanded. The interview-focused sections (What Interviewers Test by Company Type, Interview Signal Map by Role) are retained in the Architecture Perspective section with a broader framing.

---

## Tab: 🛥 Role Paths

**Purpose:** Curated learning paths and revision tools for specific roles.

**Current strengths:** Anchored Learning Paths, 1-Page Cheat Sheets by Role, Top 20 Must-Know Answers are all well-designed for their purpose. Top Formulas to Remember is appropriate for technical roles (ML Engineer, Data Scientist) but irrelevant for architects.

**Improvement priorities:**

**1. Add an explicit architect cheat sheet.**
The current cheat sheets appear to focus on ML/AI engineering roles. Add: "Solution/Enterprise Architect — 1-page cheat sheet" covering the key decisions an architect must be able to make (model selection framework, build vs buy criteria, RAG vs fine-tune, governance tiers, cost estimation).

**2. Revision Studio — clarify the intended workflow.**
The revision format (active recall, spaced repetition) is a learning science best practice, but the UX for how to use it should be clearer. A one-paragraph "how to use this" at the top of the Revision Studio section would reduce friction.

**3. Top 20 Must-Know Answers — ensure architect-relevant questions are represented.**
Review the 20 questions: if they skew toward ML engineering (which is likely given the platform's original scope), add 5–7 architect-specific questions: How do you decide when to self-host vs use an API? What is the EU AI Act and what does it require? How do you design a production LLM system with SLAs? etc.

---

## Tab: 📰 What's New

**Purpose:** Freshness — surface what has changed since the rest of the platform was written.

**Current strengths:** The concept (a "freshness index by tab" and "current snapshot buckets") is excellent. A platform this comprehensive needs a maintenance signal.

**Improvement priorities:**

**1. The "Last verified" date must be prominent.**
This is the most important piece of information in this tab. It should be at the top, formatted clearly, and updated whenever any tab is refreshed. Hidden in a learning module it loses its value.

**2. The freshness index should link directly to tabs.**
Rather than listing tabs with a freshness status, link each entry to the tab — so a reader can go directly from "RAG & Vector (updated June 2026)" to the tab.

**3. Add a "What changed in this refresh" section.**
When tabs are updated (such as the 9-section transformations in this project), note specifically what changed — not just "refreshed" but "Added: 2026 model pricing comparison, updated quantisation table, added disaggregated prefill/decode section."

**4. Emerging Trends tab should be flagged as the highest-refresh-priority tab.**
AI capabilities change fastest. The Emerging Trends tab (now transformed) should have a explicit note: "This tab is reviewed every 3 months; if the last review was > 3 months ago, treat frontier model comparisons as provisional."

---

## Tab: 🎯 Interview Strategy

**Purpose:** Prepare for AI-focused technical and system design interviews.

**Current strengths:** Interview loop structure, what interviewers actually score, STAR templates with AI context are all well-designed. Portfolio presentation section is genuinely useful.

**Improvement priorities:**

**1. Distinguish interview prep from architect/lead decision-making.**
Much of the interview content is appropriate for ML Engineer / AI Engineer interviews. For Solution Architects and Technical Leads, the interview format is different: system design discussions, technology selection rationale, risk and governance conversations. Add a "Architect / Technical Lead interview" section addressing: how to handle "design an AI system for X" questions, how to present trade-off decisions, how to answer "what would you do if the model hallucinated?"

**2. The STAR templates need AI-specific behavioural scenarios.**
Current STAR templates appear generic. Add architect-specific scenarios: "Tell me about a time you had to choose between multiple AI approaches" (fine-tune vs RAG vs prompting), "Describe a time you had to convince stakeholders to invest in AI governance," "Tell me about a production AI system failure and how you handled it."

**3. Common Mistakes to Avoid — add AI-specific mistakes.**
Generic interview mistakes are already covered. Add AI-specific mistakes: jumping to "we need a neural network" when classical ML is sufficient, ignoring data residency in system design, treating hallucination as a solvable problem rather than a managed risk, using cost-per-API-call without accounting for volume.

---

## Tab: 📈 AI Career Path

**Purpose:** Help learners navigate career development in AI.

**Current strengths:** IC levels with what each means in AI, Breaking Into AI from Other Backgrounds, and 2025 AI Job Market Reality are all grounded and useful.

**Improvement priorities:**

**1. The "IC Levels" section needs explicit architect-track content.**
Currently IC levels appear to describe the ML Engineer / AI Engineer track (L3 → L4 → L5 → Staff). For architects, the progression looks different: SA → Senior SA → Principal SA → Distinguished/Fellow, or equivalent. Add parallel architect IC level descriptions.

**2. "Breaking Into AI from Other Backgrounds" — add an explicit "integration/solution architect path."**
Many readers of this platform are experienced enterprise architects moving into AI. This path (leverages: API design, enterprise architecture patterns, stakeholder management; needs to develop: AI model fluency, evaluation methodology, governance frameworks) deserves explicit treatment rather than being subsumed under "Software Engineer → AI Engineer."

**3. "How to Evaluate an AI Team Before Joining" is excellent — make it more prominent.**
This section (what questions to ask, what signals to look for in an AI team's maturity) is uniquely valuable and hard to find elsewhere. It's buried at section 7. Move earlier or cross-reference from Start Here.

**4. Add: "What makes an AI architect portfolio different from a software architect portfolio?"**
Building AI systems has different proof points: evaluations you've designed and run, models you've selected and justified, governance frameworks you've implemented, adoption programmes you've led. A section bridging from "software architect CV" to "AI architect CV" would be high value for the target audience.

---

## Tab: Live Coding

**Purpose:** Practice implementing core AI algorithms from scratch — for interview preparation and for building mental models by implementing.

**Current strengths:** The selection of 6 implementations (Multi-Head Attention, Backpropagation, K-Means, BPE Tokenizer, VAE, Transformer Block) is excellent. These are the canonical implementations interviewers ask for. The "Interview Coding Framework 5 Steps" is practical and actionable.

**Improvement priorities:**

**1. Add difficulty and time estimates per implementation.**
A learner should know: Multi-Head Attention is harder than K-Means; Transformer Block takes 45 minutes under interview conditions, BPE takes 20 minutes. This helps with preparation pacing.

**2. The "Live Coding Interview What Each Implementation Tests" section is high-value — expand it.**
For each implementation, answer: what concept does writing this prove you understand, what are the common mistakes interviewers look for, and what follow-up questions to expect. This turns implementations from "things to memorise" into "things to understand."

**3. Add a "quick-test-yourself" section per implementation.**
Before the full implementation, add 2–3 questions to check if the learner understands the algorithm conceptually before coding it: "Before implementing Multi-Head Attention, can you explain: what Q, K, V represent? Why divide by √d_k? What happens if you remove the residual connection?" Understanding first, then implementation.

---

## Tabs: Q&A Vol 1 (1–60), Vol 2 (61–103), Vol 3 (104–160)

**Purpose:** 160 interview questions with model answers, structured for active recall practice.

**Current strengths:** The calibration rubrics (Weak/Solid/Senior answer quality descriptors) are excellent learning tools. The three-volume structure (Foundations → Applied → Production/Advanced) maps well to interview difficulty progression.

**Improvement priorities (apply to all three volumes):**

**1. Each volume needs a "Architect shortlist" — the 10–15 questions most relevant to architect roles.**
160 questions is too many to review without prioritisation. Many questions are deep ML engineering (implement backprop, PyTorch training loop, gradient clipping) which are not relevant to architect interviews. Architect-specific questions (system design, governance, trade-off analysis, cost estimation) should be flagged so architects can prioritise.

**2. The "How to Use This Volume" section should explicitly state: don't read the answers first.**
Active recall (attempt the answer, then check) is dramatically more effective for retention than passive reading. This is not obvious to all learners. Make it explicit and bold.

**3. Add cross-references to the learning module tabs.**
For each question, link to the tab that covers the underlying concept. "Q45: How does RAG differ from fine-tuning?" → RAG & Vector tab + Fine-tuning tab. This turns the Q&A from standalone drill into a learning navigation tool.

**4. Vol 3 calibration (Senior answers sound like rollout plans with ownership, controls, rollback) is the strongest of the three — this framing should be applied back to Vols 1 and 2.**
The maturation of the calibration rubric across volumes (Weak → Solid → Senior) is the most distinctive feature of this Q&A approach. Ensure this progression is reflected consistently, not just in Vol 3.

---

## Tab: 📚 Glossary

**Purpose:** 74-term reference for the vocabulary of 2026 AI.

**Current strengths:** The A–Z coverage is comprehensive. The selection of terms (HNSW, AKP, MLA, RLVR, ColBERT — not just the basics) reflects genuine 2026 depth.

**Improvement priorities:**

**1. Add: context for each term (what tab covers it in depth).**
"HNSW — see RAG & Vector tab" turns the glossary from a standalone reference into a navigation tool. Every term should link to its primary treatment in the platform.

**2. Add: "Why it matters" — one sentence per term from an architect's perspective.**
"Hallucination: a model confidently stating incorrect facts — requires architectural guardrail design, not just better prompting." This turns a vocabulary list into a decision-relevant reference.

**3. Flag terms that are architecture decisions vs implementation details.**
Some terms (LoRA, KV cache, BM25) are primarily implementation concerns for engineers. Others (MCP, RLHF, EU AI Act, Governance Tiers) are architecture and governance concerns that architects must understand. A simple icon or flag (🏗 Architect concern vs ⚙ Engineering detail) would help the primary audience prioritise.

**4. Ensure all terms introduced in the transformed learning modules are present.**
The 9-section transformations introduced some terms and frameworks specific to those modules (FRAME, AKP planes, PRR checklist, T0–T3 tiers). Verify these are in the glossary.

---

## Summary: Improvement Priority Matrix

| Tab | Primary improvement | Effort |
|---|---|---|
| Start Here | Elevate architect path; surface Non-Negotiable Tabs earlier | Low |
| Quick Guide | 8 mental models to top; add missing stuck-on-X links | Low |
| AI Landscape | Full 9-section transformation — DONE | Complete |
| Role Paths | Add architect cheat sheet; architect-relevant Q coverage | Medium |
| What's New | Prominent last-verified date; tab-linking freshness index | Low |
| Interview Strategy | Architect/lead interview section; AI-specific STAR templates | Medium |
| AI Career Path | Architect IC track; integration architect path; portfolio section | Medium |
| Live Coding | Difficulty/time estimates; conceptual check before coding | Low |
| Q&A Vol 1/2/3 | Architect shortlist flags; cross-references to tabs | Medium |
| Glossary | "Why it matters" line; architect vs engineering flags; tab links | Medium |
