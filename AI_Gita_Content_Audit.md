# AI Gita — Learning Experience Audit

**Scope:** 35 tabs · 2,255 topics · 160 Q&A items · 74 glossary terms  
**Audit date:** June 2026  
**Method:** Scoring derived from section titles, section ordering, topic density, presence/absence of structured pedagogy markers (ELI5, Analogy, First principles, Visual overview, Hands-on, Check Yourself), and overlap patterns in the content inventory.  
**Purpose:** Identify modernization opportunities. No content rewrite in this document.

---

## Scoring Key

| Dimension | What it measures |
|---|---|
| **Beginner Friendliness (BF)** | Can someone new to AI follow without prior jargon knowledge? |
| **Readability (R)** | Is the content scannable, layered, and structured for the human eye? |
| **Architecture Relevance (AR)** | Does the tab clearly connect to system/platform decision-making? |
| **Use of Examples (EX)** | Are abstract concepts grounded in concrete cases or code? |
| **Use of Analogies (AN)** | Does intuition come before formalism? |
| **Learning Flow (LF)** | Does the tab scaffold from Why → How → Decide in a logical sequence? |

**Score 1–10.** 10 = excellent. 5 = passable. Below 5 = needs attention.

---

## Tab-by-Tab Scores

### Start Here

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 7 | Role selector helps personalise, but the Command Center widget introduces 6 learning modes before a beginner knows why any of them matter |
| Readability | 8 | Strong scaffold with Step 1 / Step 2 / Step 3 progression |
| Architecture Relevance | 6 | Architecture role exists in the selector, but no architecture-specific callout in the study flow itself |
| Use of Examples | 5 | Weekly study plan items are titles only — no worked example of what "doing" a week looks like |
| Use of Analogies | 4 | No analogies present at the entry point |
| Learning Flow | 7 | Step 1 → Step 2 → Step 3 structure is clear, but the Command Center disrupts the linear flow before orientation completes |

**Overall: 6.2**

**Flags:**
- Learning Command Center (6-mode widget) is positioned too early — a new learner hits it before completing orientation
- Weekly study plan is a list of titles without showing the learner what a completed study session looks like
- No analogy or mental model at the entry point to prime the whole document
- Role selector has 9 options; no guidance on how to choose between "AI Engineer" and "AI Architect"

---

### Quick Guide

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 8 | Use-case routes (Build a Chatbot, Learn RAG) are excellent entry points |
| Readability | 9 | Best-structured tab in the document — layered from intent → map → mental models |
| Architecture Relevance | 7 | "Design an Agent Platform" route exists; mental model #5 covers agent loop |
| Use of Examples | 6 | Mental models are stated but not illustrated with a concrete scenario |
| Use of Analogies | 8 | "LLM = Next-token slot machine", "Context = working memory" are strong analogies |
| Learning Flow | 9 | Why → How → Path progression is the strongest in the document |

**Overall: 7.8**

**Flags:**
- Mental models are declared but not demonstrated — each needs one sentence showing what breaks when you ignore it
- "Where do I go when I get stuck?" section has 12 escape hatches with no triage logic; no guidance on which to try first
- The glossary teaser (74 terms) appears mid-guide without saying why a learner needs vocabulary at this stage

---

### AI Landscape

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | "Role Taxonomy" and "Interview Signal Map by Role" assume the reader already knows they are in an AI hiring context |
| Readability | 7 | Well sectioned; decision framework table format is appropriate |
| Architecture Relevance | 8 | "AI Capability Map" and "Build vs Prompt vs Fine-tune vs Train" are directly architecture-decision relevant |
| Use of Examples | 6 | "Open-weight vs Closed Models" mentions the decision but the examples in the accordion questions suggest the body is thin |
| Use of Analogies | 3 | No analogy frame for the landscape; "what is AI in 2026" needs a map metaphor, not a taxonomy |
| Learning Flow | 6 | Starts with Role Taxonomy (identity-framing) before explaining what the landscape actually is |

**Overall: 5.8**

**Flags:**
- Section order: Role Taxonomy before Landscape overview means the reader is asked to self-categorise before understanding the space
- Jargon-before-intuition risk: "Open-weight vs Closed", "PEFT", "interview signal" all appear early without a plain-language primer
- Missing analogy: the 2026 tech stack map needs a "city map" or "food chain" metaphor before it lists 30 tools
- "What Interviewers Actually Test" is interview prep content inside a landscape orientation tab — misplaced pedagogically

---

### Role Paths

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | Cheat sheets help, but the "Top 20 Must-Know Answers" assumes interview framing |
| Readability | 7 | Anchored Learning Paths table format works well |
| Architecture Relevance | 5 | No dedicated architect path content visible in section titles |
| Use of Examples | 5 | "Top Formulas to Remember" is a reference list, not a worked example |
| Use of Analogies | 3 | No analogies present |
| Learning Flow | 6 | Revision Studio is placed first — review before initial exposure is backwards for new learners |

**Overall: 5.3**

**Flags:**
- Revision Studio is the first section — you can't revise what you haven't learned yet; this should be gated behind completion of at least one foundational tab
- "1-Page Cheat Sheets by Role" section has no content preview — it's a blind promise
- No architect-specific path visible in section titles despite "AI Architect" being a role selector option
- Analogy gap: the whole tab lacks a metaphor for what "learning paths" even are in this context

---

### What's New

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "Why This Tab Exists" section helps; but "Freshness Index by Tab" is a meta-concept hard to use without having read all tabs |
| Readability | 7 | Four-section structure is clean |
| Architecture Relevance | 5 | Speculative decoding and serving appear as accordion questions but architecture decision guidance is absent from section titles |
| Use of Examples | 4 | "Current Snapshot Buckets" is a category label — no worked example of how to apply new information |
| Use of Analogies | 3 | No analogies |
| Learning Flow | 5 | Freshness Index appears last but is arguably the most useful tool in the tab — ordering inverts importance |

**Overall: 5.0**

**Flags:**
- "Freshness Index by Tab" is buried last but is the tab's primary value proposition — should lead
- No mechanism shown for *how* a learner should update their knowledge when they see a freshness flag
- Section "Current Snapshot Buckets" reads as an internal editorial category, not a learner-facing concept
- Missing analogy: "knowledge has a half-life" or "like updating a map" would contextualise the whole tab

---

### Math & Stats

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 4 | "Information Bottleneck Principle" and "Contrastive vs Cross-Entropy" appear in the Check Yourself questions for a tab that is supposed to be prerequisite material |
| Readability | 7 | Visual cheatsheets and the 3-intuition structure help |
| Architecture Relevance | 3 | No connection made between math foundations and architecture-level decisions |
| Use of Examples | 6 | Gradient descent section likely has worked examples; attention section has a visual walkthrough |
| Use of Analogies | 7 | "Attention = Learned Weighted Average" is a strong analogy anchor |
| Learning Flow | 6 | The "Where Math Lives" section is a good orientation device, but it appears after the visual overview rather than first |

**Overall: 5.5**

**Flags:**
- Check Yourself accordions include "Information Bottleneck Principle" and "Contrastive Loss vs Cross-Entropy" — these are graduate-level topics surfaced in the prerequisites tab
- "Math Prerequisites by Role" is placed mid-tab; it should be first — a learner needs to know if they need this tab at all before reading it
- Architecture Relevance gap: math foundations tab never explains *why an architect needs to know this at all*
- No bridging statement connecting Softmax/Sigmoid to how they show up in production model behavior

---

### ML Fundamentals

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | XGBoost deep dive and bias-variance coverage is good foundational material |
| Readability | 7 | 8-section structure with clear sub-topics |
| Architecture Relevance | 4 | No section connects ML fundamentals to platform-level or architecture decisions |
| Use of Examples | 7 | Code is explicitly mentioned in the weekly study plan description for this tab |
| Use of Analogies | 5 | No analogy for bias-variance tradeoff visible in section titles |
| Learning Flow | 7 | Linear → Tree → Unsupervised → Evaluation is a logical progression |

**Overall: 6.0**

**Flags:**
- Architecture gap: no section on "when to use a classical ML model vs an LLM" — this is the most architecture-relevant question for this tab
- "ML Algorithm Landscape When to Use What" is excellent but positioned late (section 5 of 8); it should be early to help learners orient
- Check Yourself questions reference "knowledge distillation" and "training at scale" — these are out-of-scope for this tab's level
- Bias-variance analogy missing from section titles — "overfitting = memorising vs generalising" is the standard intuition and doesn't appear

---

### Deep Learning

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 4 | Tab only has 2 content sections after the visual overview — "Backpropagation: Full Derivation" is not beginner material |
| Readability | 5 | Thin section structure; the "Model Family Quick Comparison" sub-section is buried inside Normalization |
| Architecture Relevance | 4 | No section on how deep learning architecture choices affect production behaviour |
| Use of Examples | 7 | "Full Derivation" implies code and math worked through completely |
| Use of Analogies | 5 | Analogy is promised in the learning module list but not reflected in section titles |
| Learning Flow | 4 | Visual overview → Full Derivation is a steep jump; there is no "intuition first" ramp |

**Overall: 4.8**

**Flags:**
- **Research-paper risk:** "Backpropagation: The Full Derivation" is the first real section — this is graduate textbook style, not layered pedagogy
- Only 2 main content sections for a topic (Deep Learning) that underpins the entire document — significant content gap
- No section on "what transformers replaced and why" — critical intuition for the LLM tabs that follow
- Model Family Quick Comparison is a sub-section inside Normalization Techniques; it should be a standalone section for orientation
- Missing: activation functions as standalone topic; loss functions as standalone topic; regularisation

---

### LLMs & Foundation

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "What is an LLM?" and the ELI5/Analogy/First Principles scaffolding help |
| Readability | 8 | 8-section structure with clear named milestones |
| Architecture Relevance | 7 | "LLM Knowledge Depth by Role" and the frontier model lineup are architecture-decision relevant |
| Use of Examples | 7 | "Attention Math — Concrete 3-Token Walkthrough" is an excellent worked example |
| Use of Analogies | 7 | Analogy modules are explicitly present |
| Learning Flow | 8 | What is it → Architecture → Role needs → Math → Parameters → Frontier models is logical |

**Overall: 7.2**

**Flags:**
- "Sampling Parameters Cheatsheet" is placed after the frontier model lineup — sampling parameters are needed *before* you can reason about model differences; reorder opportunity
- "LLM Content Map" section name is opaque — it reads as navigation metadata, not a learner-facing concept
- Check Yourself questions in LLM Architecture Evolution include "vanishing gradient" — this should be resolved in the Deep Learning tab already, not tested again here
- Architecture gap: no decision framework for "when to call an API vs host your own model" — the most common LLM architecture decision

---

### Generative AI

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | Diffusion Models as first content section is a steep entry; ELI5 module is present but its position relative to content is unclear |
| Readability | 7 | 8 sections with clear named topics |
| Architecture Relevance | 6 | "GenAI Architecture Patterns Visual Overview" is the right intent but positioned late (section 6 of 8) |
| Use of Examples | 8 | VAE Complete Implementation appears multiple times — concrete code present |
| Use of Analogies | 6 | Analogy modules listed but "2026 generative landscape" diagram is the primary orientation device |
| Learning Flow | 5 | Diffusion Models → GANs → Flow Matching → Production → VAE Implementation → Architecture Patterns — production and patterns should come before deep-dive implementations |

**Overall: 6.2**

**Flags:**
- **Research-paper risk:** "Diffusion Models: Complete Math & Architecture" is the opening content section — a learner new to GenAI needs "what problem does generative AI solve" first
- VAE appears in three separate sections (GANs/VAEs, Production Image Generation, VAE Complete Implementation) — significant structural duplication within a single tab
- "GenAI Architecture Patterns" is section 6 of 8 — it should frame the whole tab, not arrive after three deep-dives
- Prompt Engineering Techniques section is misplaced here (correctly flagged for migration to prompt-engineering module in the modularisation plan)
- "Analogy" learning module is listed twice in the inventory — possible DOM duplication

---

### Fine-tuning

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "When to Fine-tune vs RAG vs Prompting" as opener is excellent — decision-first |
| Readability | 7 | 13 sections is dense but logically grouped |
| Architecture Relevance | 8 | Decision tree and the RAG vs Fine-tune vs Prompting framework are directly architecture-relevant |
| Use of Examples | 8 | LoRA math derivation, QLoRA code, DPO training code all indicated |
| Use of Analogies | 6 | LoRA Visual Explanation implies analogy; RLHF pipeline lacks one |
| Learning Flow | 7 | Decision → Visual → Math → Dataset → Hyperparams → Evaluation → Advanced methods is sound |

**Overall: 7.0**

**Flags:**
- 13 sections is the highest section count of any foundational tab — risk of exhaustion before the learner reaches GRPO/RLVR (sections 11–12)
- "LoRA: The Math & Implementation" and "LoRA Math Complete Derivation" appear as separate sections — likely redundant; one should subsume the other
- "Preference Optimisation Zoo" — the word "Zoo" is evocative but the section will land as jargon-heavy if it lists DPO/ORPO/SimPO/GRPO without a decision matrix
- RLHF has no intuition-first section — it appears as "Explain the complete RLHF pipeline with code" in Check Yourself without any prior gentler introduction visible in section titles
- Architecture gap: no section on cost-of-fine-tuning vs cost-of-prompting at scale

---

### Long Context & SSMs

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 3 | "YaRN", "MLA", "Mamba", "RULER" appear as first-level topics with no plain-language primer |
| Readability | 5 | Section count is manageable (5) but the topics assume prior deep familiarity |
| Architecture Relevance | 8 | Long context decisions are directly architecture-relevant; decision tree diagram is present |
| Use of Examples | 5 | "Long Context in 2026 — what actually works at 1M+ tokens" implies benchmarks, not worked code examples |
| Use of Analogies | 2 | No analogy visible for SSMs or RoPE extension — this is the largest analogy gap in the document |
| Learning Flow | 5 | Starts with RoPE Extension (deep technique) before explaining why long context matters |

**Overall: 4.7**

**Flags:**
- **Jargon-before-intuition (severe):** YaRN, MLA, Mamba, RULER all appear in section and topic titles with no plain-language primer visible
- **Research-paper risk:** "RoPE Context Extension: YaRN & LongRoPE" as the first content section reads like a paper title
- Missing analogy: SSMs need a "filing cabinet vs scroll of paper" or equivalent mental model before the math
- "Advanced RAG Patterns" is a section in this tab but belongs in RAG — already flagged in modularisation plan; it disrupts the flow here
- Architecture gap: no explicit "when do you choose long context over RAG?" decision aid visible in section titles
- **Overwhelm risk for architects new to AI:** this tab will cause the most confusion for a solution architect without ML background

---

### RAG & Vector

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 7 | ELI5, Analogy, "Stop here if you just need the concept" all present |
| Readability | 8 | 9 sections with a production flow diagram as anchor |
| Architecture Relevance | 9 | The entire tab is architecture-decision relevant: chunking, hybrid search, reranking, eval, 2026 changes |
| Use of Examples | 8 | "Hands-on Implementation — Minimal RAG" and HNSW/BM25 worked content present |
| Use of Analogies | 7 | ELI5 and Analogy modules present; "give the LLM a memory" is excellent framing |
| Learning Flow | 8 | End-to-end flow → Chunking → Hybrid → Pipeline → Vector search → Evaluation → 2026 → Hands-on is excellent |

**Overall: 7.8**

**Flags:**
- "RAG in 2026 — what changed since the textbook" is section 7 of 9 — the "what changed" framing is only meaningful after the foundational content, so placement is correct, but the section title could be more specific
- "RAG Evaluation (RAGAS) & Failure Modes" is a single section that combines two distinct topics — evaluation deserves its own section
- Check Yourself questions include "PageRank algorithm" and "build a knowledge graph" — these are advanced/adjacent topics not signalled by the section titles

---

### Agents & Prompting

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | ELI5, "Stop here" present; but MCP/A2A/AG-UI appear early in the protocol stack section |
| Readability | 7 | 13 sections — same density risk as Fine-tuning |
| Architecture Relevance | 9 | Agent loop, multi-agent patterns, memory, protocol stack, vendor SDKs all architecture-relevant |
| Use of Examples | 8 | ReAct Complete Implementation, LangGraph, Minimal Tool-Calling Agent, Minimal MCP Client all present |
| Use of Analogies | 6 | "The canonical agent loop" diagram is present; analogy for MCP absent |
| Learning Flow | 6 | Prompt Engineering as first section is good, but multi-agent patterns appear before the single-agent implementation is fully established |

**Overall: 7.0**

**Flags:**
- Multi-agent patterns (section 3) appear before the complete single-agent implementation (section 5) — a learner needs the simple case before the complex case
- "Agent Protocol Stack — the 'OSI of agents'" is excellent framing but the section title/suffix merge noted in the modularisation plan will make it hard to anchor
- Vendor Agent SDKs section — without a decision matrix it will read as a vendor list, not architecture guidance
- The tab mixes prompt engineering and agent content; the modularisation plan correctly separates these — the current mixed state means a learner can't tell which skill they're developing at any moment
- MCP/A2A/AG-UI acronyms appear without prior definition within the tab (they are in the glossary, but not resolved inline)

---

### RecSys · TS · Tabular

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | "Two-Tower + Matrix Factorization" as the first content section is not beginner-friendly |
| Readability | 7 | 7 sections with a logical cascade pattern |
| Architecture Relevance | 8 | "Recommendation System Production Cascade Pipeline" and the Two-Tower vs DLRM comparison are architecture-relevant |
| Use of Examples | 7 | Code is implied in the weekly study module description |
| Use of Analogies | 4 | No analogies visible in section titles for any of the three domains |
| Learning Flow | 6 | RecSys → Time Series → Deep Learning for RecSys → Cascade → Two-Tower vs DLRM — the interleaving of RecSys theory and RecSys architecture without a clear boundary is confusing |

**Overall: 6.2**

**Flags:**
- Three separate domains (RecSys, Time Series, Tabular) are in one tab — each is a full sub-discipline; the tab title "RecSys · TS · Tabular" signals density but doesn't help a learner know which sub-domain to enter first
- "Recommendation Metrics" is the last section before Go Deeper — metrics should appear earlier to help learners evaluate their understanding of the earlier architecture content
- Analogy gap: time series forecasting needs a "predicting weather vs predicting stock prices" type intuition; RecSys needs a "librarian who knows your taste" metaphor
- "Deep Learning for Recommendations" as a standalone section creates confusion with the earlier "Recommendation Systems: Two-Tower + Matrix Factorization" section — the relationship between them is unclear

---

### Data Science

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | Causal inference is foundational material well-suited to new learners |
| Readability | 7 | 7 sections with reasonable sub-structure |
| Architecture Relevance | 4 | A/B testing and causal inference connect to evaluation platform design, but this connection is never made explicit |
| Use of Examples | 6 | "A/B Testing & SQL" likely has worked queries; uplift modelling likely has code |
| Use of Analogies | 5 | "Confounding Why Correlation Fails" is an analogy-friendly topic but the analogy isn't visible in the title |
| Learning Flow | 7 | Causal → A/B → Advanced A/B → Confounding → Design → Uplift is logical |

**Overall: 5.8**

**Flags:**
- Architecture gap: no section on how an A/B testing platform is built or integrated with an ML pipeline — the most architecture-relevant question for this tab
- "Confounding Why Correlation Fails" has a strong analogy opportunity (the classic "ice cream and drowning" or "sunglasses and cancer" examples) — not visible in current titles
- "Uplift Modelling Target the Right Users" — "uplift modelling" is jargon that will stop most adidas practitioners before they read the section; needs a plain-language sub-title
- Check Yourself questions reference "rate limiting for an LLM API" and "production monitoring dashboard" — completely out of scope for this tab

---

### CV & NLP

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | "BPE Tokenizer: Complete Implementation from Scratch" and "NLP Task Reference" assume substantial background |
| Readability | 6 | 10 sections, but "CV vs NLP Task Map" and "CV vs NLP Task Mapping" appear to be near-duplicate sections |
| Architecture Relevance | 5 | No section on when to use off-the-shelf vision/NLP models vs train from scratch — the most architecture-relevant decision |
| Use of Examples | 7 | BPE implementation and the classification pipeline are concrete |
| Use of Analogies | 4 | No analogies visible in section titles for CV architectures or NLP embeddings |
| Learning Flow | 5 | "CV vs NLP Task Map" (section 6) and "CV vs NLP Task Mapping" (section 8) and "Transfer Learning CV vs NLP" (section 7) and "Transfer Learning: CV vs NLP" (section 9) appear to be structural duplicates — the flow is broken by repetition |

**Overall: 5.3**

**Flags:**
- **Structural duplication (confirmed):** "CV vs NLP Task Map" and "CV vs NLP Task Mapping" are near-identical section titles; same for "Transformer Transfer Learning CV vs NLP" and "Transfer Learning: CV vs NLP" — likely a DOM duplication issue
- Jargon-before-intuition: "NLP Task Reference" appears before any analogy frame for what NLP tasks even are
- No section bridging CV/NLP to the LLM era — "how CLIP connects vision to language" is the key architecture insight and it's absent from section titles
- 10 sections for a survey tab across two disciplines creates exhaustion risk

---

### AI Infrastructure

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 3 | "Disaggregated Prefill / Decode (P/D split)" and "Quantisation — the 2026 menu" as standalone sections require deep GPU architecture background |
| Readability | 7 | 12 sections, well-named; the production serving stack diagram anchors the tab |
| Architecture Relevance | 10 | Every section is directly architecture-relevant |
| Use of Examples | 7 | Code is indicated for GPU memory math, quantization, distributed training, and vLLM |
| Use of Analogies | 4 | Only the disaggregated serving diagram serves as an analogy vehicle; explicit verbal analogies are absent |
| Learning Flow | 6 | GPU Hierarchy → Distributed Training → Quantisation → GPU Architecture → Distributed Strategies (again) — distributed training appears twice across sections 2 and 5 |

**Overall: 6.2**

**Flags:**
- **Research-paper risk:** "Disaggregated Prefill / Decode (P/D split)" as a named section will overwhelm any architect not already familiar with KV cache internals
- Distributed Training appears in sections 2 ("Which Strategy for Which Problem") and 5 ("Distributed Training Strategies") — structural duplication
- Architecture gap: no cost model section — "how much does it cost to serve a 70B model?" is the first question every architect asks; it's implied in the weekly study module description but absent from section titles
- Analogy gap: GPU memory hierarchy needs a "hotel room vs hallway vs lobby" or "CPU RAM vs disk" type metaphor visible in the content
- "Knowledge Distillation & Structured Pruning" is placed between distributed training and inference serving — it breaks the logical GPU-to-serving progression
- **Overwhelm risk for architects new to AI:** this tab requires the deepest hardware background of any tab

---

### MLOps / LLMOps

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | ELI5 present; "LLMOps: What's Different" is a good orientation section |
| Readability | 7 | 10 sections; the "production traffic feeds eval set" diagram is a strong anchor |
| Architecture Relevance | 9 | CI/CD, drift detection, observability, LLMOps vs MLOps comparison — all architecture-relevant |
| Use of Examples | 6 | CI/CD pipeline YAML is mentioned in the weekly study description; not visible in section titles |
| Use of Analogies | 4 | The "eval gate" metaphor in the diagram description is strong but no verbal analogies in section titles |
| Learning Flow | 7 | Pipeline Architecture → LLMOps What's Different → CI/CD → Pipeline Visual → Drift → LLMOps vs MLOps → Monitoring → Observability is logical |

**Overall: 6.3**

**Flags:**
- "LLM & Agent Observability in 2026 — OpenTelemetry GenAI Conventions" reads as a standards document header, not a learner-facing section title
- "Reasoning-Model Observability — the new dashboards" is positioned last — if reasoning models are the 2026 paradigm, this should not be an afterthought
- Drift Detection and Production Monitoring are correctly flagged for migration to the evaluation module — their presence here fragments the monitoring story
- No section on "what does an LLMOps platform actually look like as infrastructure" — the architecture of the MLOps platform itself is missing
- Check Yourself questions in this tab include "RLHF pipeline" and "recommendation system for video streaming" — out of scope

---

### System Design

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | Two scenario sections (Legal Q&A, Recommendation + LLM Hybrid) are good concrete anchors |
| Readability | 7 | 7 sections; FRAME interview framework provides a consistent scaffold |
| Architecture Relevance | 10 | The tab's entire purpose is architecture — all sections are relevant |
| Use of Examples | 8 | Two concrete scenarios with named systems; cost math implied |
| Use of Analogies | 4 | No analogies in section titles; the 6-layer architecture diagram is the closest substitute |
| Learning Flow | 7 | Overview → 6-Layer Architecture → Multi-Tenancy → Scenarios → Core Patterns → FRAME Framework is reasonable |

**Overall: 6.8**

**Flags:**
- "Multi-Tenancy in LLM Systems" as section 3 is too specific too early — a learner needs to understand the full system before understanding tenancy isolation
- No section on latency budget / cost envelope — these are the first constraints any architect identifies; mentioned in the weekly study description but absent from section titles
- "System Design Interview Framework (FRAME)" is placed last — if FRAME is the meta-skill, it should be introduced first so the learner can apply it to the scenarios
- Architecture gap: no section on failure modes / graceful degradation — a production architecture tab without a resilience section is incomplete
- Analogy gap: the 6-layer architecture needs a "plumbing system" or "OSI model" metaphor to make the layers memorable

---

### Agentic Platform

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 3 | "AKP — 8-Plane Reference Architecture" as the first content section assumes the learner knows what AKP is |
| Readability | 6 | 13 sections with multiple near-duplicate AKP sections |
| Architecture Relevance | 10 | The entire tab exists to describe the platform architecture |
| Use of Examples | 6 | "Model Gateway: Full Implementation & OTel Instrumentation" is concrete; others are conceptual |
| Use of Analogies | 3 | No analogy for "what is an agentic platform" visible — this is the most architecture-abstract tab |
| Learning Flow | 4 | AKP 8-Plane → AKP Six Planes → AKP Six-Plane Architecture → AKP 6-Plane Architecture Visual → AKP 6-Plane Architecture — five near-identical section titles in sequence break all flow |

**Overall: 5.3**

**Flags:**
- **Structural duplication (severe):** "AKP — Six Planes Architecture", "AKP Six-Plane Architecture", "AKP 6-Plane Architecture Visual Breakdown", and "AKP 6-Plane Architecture" are four near-identical section titles — likely represents multiple rendering passes of the same content
- **Jargon-before-intuition (severe):** "AKP" appears in 7 of 13 section titles; the acronym is never expanded in a section title visible to first-time readers
- No "What problem does the Agentic Platform solve?" opener visible in section titles
- "What is Agent Core?" is section 12 of 13 — this foundational question should be section 1 or 2
- **Overwhelm risk for architects new to AI:** this is the tab most likely to confuse a solution architect — it describes a full platform paradigm using internal terminology without any grounding metaphor

---

### Governance Deep Dive

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | PRR Checklist and Risk Tier Model are well-structured for practitioners |
| Readability | 7 | 10 sections; the checklist format aids scanability |
| Architecture Relevance | 9 | PRR, Artifact Registry, Red-Teaming, Saga Pattern — all architecture-operational |
| Use of Examples | 6 | "Red-Teaming AI/Agentic Systems" has a sub-section on HA for MCP Servers — concrete |
| Use of Analogies | 4 | "Saga Pattern" is a metaphor but it's unexplained in the title |
| Learning Flow | 7 | PRR → Registry → Red-Teaming → Checklist → Risk Tier → Saga → Policy vs Controls → EU Act Decision → Policy vs Controls → EU Act: Which Tier — last 4 sections feel like a separate mini-module appended at the end |

**Overall: 6.5**

**Flags:**
- "Policy vs Technical Controls" appears as both sections 8 and 9 — structural duplication
- "EU AI Act Risk Tier Decision" (section 8) and "EU AI Act Which Tier?" (section 10) are near-duplicate sections — likely DOM duplication of the same content
- No introductory section explaining why governance exists before diving into the PRR checklist
- "Saga Pattern Compensating Transactions in Agentic Workflows" — "Saga Pattern" is a distributed systems term that will be opaque to many AI practitioners; needs an analogy
- Architecture gap: no section on how governance integrates into the CI/CD pipeline — the operational question every platform architect has

---

### Agent Runtime Ops

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 4 | "IIB/TIBCO in Agent Context" is highly specific enterprise middleware jargon |
| Readability | 6 | 8 sections; the HITL Gate diagram is a strong anchor |
| Architecture Relevance | 9 | Four-Layer Memory, HITL Gates, Monitoring Dimensions, Drift Detection — all runtime architecture |
| Use of Examples | 5 | "Enterprise Legacy Connectors" is concrete but niche; other sections are conceptual |
| Use of Analogies | 3 | No analogies visible; "prompt drift" is a technical term with no metaphor scaffold |
| Learning Flow | 5 | Memory Architecture → Prompt Drift → Enterprise Connectors → Monitoring Dimensions → HITL → Monitoring What to Watch → Monitoring Metrics — "what to watch" and "metrics" are near-duplicate sections |

**Overall: 5.3**

**Flags:**
- "Enterprise Legacy Connectors (IIB/TIBCO in Agent Context)" — IIB (IBM Integration Bus) and TIBCO are very specific middleware products; this section will be opaque to anyone outside IBM/TIBCO shops and creates a "who is this for?" moment
- "Agent Monitoring What to Watch" and "Agent Monitoring Metrics" are near-duplicate sections — likely a duplication in the DOM
- Analogy gap: "prompt drift" needs a "instrument drift in manufacturing" type metaphor
- "Four-Layer Memory Architecture" is the most important concept in the tab but is placed first without any scaffolding for why memory layers exist
- Architecture gap: no section on failure recovery in agent runtime — what happens when an agent gets stuck?

---

### Safety & Ethics

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "Hallucination: Root Causes, Types & Mitigations" is a good opening — approachable topic |
| Readability | 7 | 7 sections; well-named; the defence-in-depth diagram is a strong anchor |
| Architecture Relevance | 8 | Guardrail architecture, defence-in-depth, OWASP Top 10 are directly architecture-relevant |
| Use of Examples | 6 | "Guardrail Architecture: Implementation" implies code; OWASP implies specific attack patterns |
| Use of Analogies | 5 | "Defence-in-Depth" is itself an analogy; hallucination section likely uses examples |
| Learning Flow | 7 | Hallucination → Guardrail → Defence-in-Depth → EU AI Act → Bias/Fairness → OWASP moves from technical to regulatory to ethical — logical |

**Overall: 6.5**

**Flags:**
- "EU AI Act Risk Tier Pyramid" is positioned at section 4 — it interrupts the technical guardrail content with a regulatory framework; regulatory content should follow all technical content
- "Bias, Fairness & Regulatory Landscape" combines two separate concerns (mathematical fairness metrics and regulatory compliance) into one section
- No section on "Constitutional AI" as an architectural pattern — mentioned in the weekly study description but absent from section titles
- Check Yourself questions include "RLHF reward hacking" and "optimizer bias correction" — these belong in Fine-tuning and ML Fundamentals respectively; their presence here signals scope bleed

---

### Dev Experience

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "Prompt Library & Playground" is approachable; "Model Access Tiers Self-Service Portal" is more abstract |
| Readability | 7 | 11 sections — the tab is over-sectioned for its scope |
| Architecture Relevance | 7 | SDK vs API, Model Access Governance, and rate limiting are architecture-decision relevant |
| Use of Examples | 5 | No hands-on implementation section visible — the tab is more conceptual than practical |
| Use of Analogies | 4 | No analogies visible |
| Learning Flow | 5 | 11 sections covering both prompt tooling and platform access; the two concerns are never cleanly separated within the current tab structure |

**Overall: 5.7**

**Flags:**
- 11 sections for developer experience creates a sprawling tab without a clear throughline
- "Go Deeper — Governance" is a section inside the Dev Experience tab — cross-domain pollution that confuses the tab's identity
- No hands-on section — a tab about developer experience with no hands-on example is ironic
- "SDK vs Raw API Why the Abstraction Matters" and "SDK vs Direct API Call" are near-duplicate sections
- Prompt Library, Prompt Engineering Tooling, and Prompt Lifecycle are three overlapping prompt-related sections — these belong in the prompt engineering module (correctly flagged in modularisation plan)
- Architecture gap: no section on how to build a model access portal — the tab describes what one is but not how to build it

---

### People & Adoption

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 8 | Non-technical content; most accessible tab in the document |
| Readability | 7 | 7 sections with a clear change management progression |
| Architecture Relevance | 3 | No connection to platform/system design; the closest is "Pilot vs Enterprise Rollout" |
| Use of Examples | 5 | "Responsible AI Training" and "Change Management Program" are conceptual; no worked case study |
| Use of Analogies | 5 | Change Management Fear and Response diagram implies visual analogy |
| Learning Flow | 7 | Skills → Change Management → Responsible AI → Fear & Response → Skills Matrix → Rollout is logical |

**Overall: 5.8**

**Flags:**
- Architecture gap: no section on how to instrument a CoE (Centre of Excellence) as a platform function — the most architecture-relevant question for an organisation adopting AI
- No worked case study visible — "how did one team actually roll out LLMs at an enterprise" would make this tab memorable
- "Pilot vs Enterprise Rollout" section has no sub-structure visible — it's likely a short section for the most complex real-world challenge in the tab
- Check Yourself questions include "key challenges in training LLMs at scale" and "most important thing about deploying LLMs in production" — out of scope for a people & adoption tab
- The tab's relationship to the Governance tab is never explicitly stated — governance is the policy layer; people & adoption is the execution layer; a bridging statement is missing

---

### Live Coding

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 4 | "Multi-Head Attention (FAANG Standard)" as the first section signals elite interview preparation, not accessible learning |
| Readability | 8 | 9 sections with numbered implementations — highly scannable |
| Architecture Relevance | 5 | Implementations are algorithm-level, not architecture-level |
| Use of Examples | 10 | The entire tab is code implementations |
| Use of Analogies | 3 | No analogies visible — by design for a coding tab, but the "why this implementation matters" is absent |
| Learning Flow | 6 | Multi-Head Attention → Backpropagation → Coding Interview Framework → K-Means → More Implementations → BPE → VAE → Transformer Block — the Interview Framework (section 3) should be first |

**Overall: 6.0**

**Flags:**
- Interview Coding Framework (section 3) should be section 1 — it's the meta-skill that makes all other implementations learnable
- "FAANG Standard" label on section 1 is intimidating for anyone not targeting FAANG — should be renamed to something like "Production Reference Implementation"
- No section on "how to debug a failing implementation" — the most common learner problem in a live coding context
- No section connecting each implementation to its production use case — "why does this code matter outside an interview?"
- "More Critical Implementations" as a section title is a catch-all that obscures what it contains

---

### Q&A Vol 1 (1–60)

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 7 | Calibration rubric (Weak / Solid / Senior) is excellent pedagogical scaffolding |
| Readability | 8 | Two-volume structure with Interview Loop section |
| Architecture Relevance | 5 | Foundations volume — architecture relevance is appropriately lower |
| Use of Examples | 7 | Questions are practical and implementation-focused |
| Use of Analogies | 6 | Q&A format naturally surfaces analogies in answers |
| Learning Flow | 7 | Q1–60 foundations progression is logical |

**Overall: 6.7**

**Flags:**
- "Interview Loop" section — the loop format is powerful but no description of what happens when you fail a loop iteration
- No visible mechanism for distinguishing which Q&A items are must-knows vs nice-to-knows for each role
- Check Yourself questions in Vol 1 sections are repeated from other tabs — the 160 Q&A items appear duplicated across nearly every tab in the overlap section, suggesting the question bank assignment logic is over-broad

---

### Q&A Vol 2 (61–103)

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | Applied and systems — requires Vol 1 completion |
| Readability | 8 | Calibration rubric continues; "System-Design Loop" is a good practice scaffold |
| Architecture Relevance | 8 | Systems and deployment questions are architecture-heavy |
| Use of Examples | 7 | System design questions imply worked architecture scenarios |
| Use of Analogies | 5 | Format doesn't lend itself to extended analogies |
| Learning Flow | 7 | Logical continuation from Vol 1 |

**Overall: 6.8**

**Flags:**
- "How to Use This Volume" section is present in all three volumes but the content likely repeats — a single "How to use Q&A volumes" guide would be more efficient
- No tagging of questions by difficulty within the volume — a learner can't identify which questions to do first

---

### Q&A Vol 3 (104–160)

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 5 | Advanced and production — requires both prior volumes |
| Readability | 8 | Production Review Loop is an excellent practice mechanism |
| Architecture Relevance | 9 | Architecture, scaling, ethics, regulatory content |
| Use of Examples | 7 | Production rollout questions are scenario-heavy |
| Use of Analogies | 5 | Format doesn't lend itself to extended analogies |
| Learning Flow | 7 | Q104–160 progression is the most architecture-relevant volume |

**Overall: 6.8**

**Flags:**
- "Q&A Final Q151 to Q160" as a separate section within Vol 3 is structurally odd — why are questions 151–160 isolated from 114–150?
- The "Production Review Loop" is the most sophisticated practice tool in the document but it's introduced in the most advanced volume — a preview of the loop concept in Vol 1 would improve learning transfer

---

### Interview Strategy

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "FAANG/Senior AI Interviews Are Structured" is a concrete anchor |
| Readability | 7 | 5 focused sections |
| Architecture Relevance | 5 | Interview strategy is role-relevant but not system-architecture relevant |
| Use of Examples | 7 | STAR templates with AI context are concrete |
| Use of Analogies | 5 | No analogies — acceptable for a strategy/process tab |
| Learning Flow | 7 | Structure → Scoring → Behaviorals → Portfolio → Mistakes is a logical interview prep sequence |

**Overall: 6.2**

**Flags:**
- "Common Interview Mistakes to Avoid" as the final section ends the tab on a negative framing — consider reordering to end on Portfolio Presentation
- No section on "how to negotiate compensation after clearing the technical interview" — this is the most practical post-interview question
- Check Yourself questions in this tab include "vanishing gradient problem" and "model collapse" — these are technical questions that belong in technical tabs, not interview strategy

---

### AI Career Path

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 8 | Career content is accessible and motivational |
| Readability | 7 | 7 well-named sections |
| Architecture Relevance | 5 | "IC Levels in AI" and "How to Evaluate an AI Team" are relevant for architect hiring decisions |
| Use of Examples | 5 | "Breaking Into AI from Other Backgrounds" likely has case studies but they're not signalled in titles |
| Use of Analogies | 5 | No analogies visible |
| Learning Flow | 7 | IC Levels → Promotion → Breaking In → Brand Building → Market Reality → IC vs Management → Team Evaluation is logical |

**Overall: 6.1**

**Flags:**
- "2025 AI Job Market Reality" — the year in the section title will become stale; should use a relative framing or a versioned date
- No section on "what to look for in an AI platform role vs a product AI role" — the most common career decision point for engineers joining AI teams
- Check Yourself questions include "how does RAG differ from fine-tuning" and "Flash Attention" — these are technical topics with no relevance to career path content

---

### Emerging Trends

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 4 | "Reasoning Models — o1, o3, DeepSeek-R1 Class" assumes familiarity with model naming conventions |
| Readability | 7 | 11 sections; well-named |
| Architecture Relevance | 8 | MoE, structured output, computer use, MCP — all architecture-relevant |
| Use of Examples | 6 | "2026 Frontier Model Comparison" is a reference table, not a worked example |
| Use of Analogies | 4 | No analogies for why MoE or reasoning models work the way they do |
| Learning Flow | 5 | Reasoning Models → Agentic Framework Comparison → New Fine-tuning Methods → Multimodal → Persistent Memory → MCP → Computer Use → Frontier Comparison → Reasoning Models (again) → MoE → Structured Output — "Reasoning Models" appears twice; no clear thematic grouping |

**Overall: 5.7**

**Flags:**
- "Reasoning Models" appears as sections 1 and 9 — structural duplication or unresolved near-duplicate
- No "what is the 2026 paradigm shift?" orientation section that positions the learner before the detail — all sections are equally deep
- The tab contains content for 8 different modules (per the modularisation plan) — it is the most fragmented tab in the document and this is reflected in the incoherent flow
- Architecture gap: no decision aid for "when to use a reasoning model vs a standard model" — the most common architect question for this topic
- Analogy gap: MoE needs a "specialist team vs generalist team" metaphor; reasoning models need a "thinking slowly vs fast" metaphor (System 2 vs System 1)

---

### Cloud Platforms

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 6 | "Cloud LLM Platform Decision" is a practical starting point |
| Readability | 7 | 6 sections with clear named comparisons |
| Architecture Relevance | 9 | AWS vs Azure vs GCP, HuggingFace Ecosystem, ROI Template — all architecture-decision relevant |
| Use of Examples | 6 | "AWS SageMaker Pipelines Deep Dive" implies worked examples |
| Use of Analogies | 3 | No analogies for cloud platform selection |
| Learning Flow | 6 | Platform Decision → Build/Buy/Fine-tune → AWS Deep Dive → HuggingFace → ROI → Technical Debt — the ROI template and Technical Debt feel like separate tabs appended at the end |

**Overall: 6.2**

**Flags:**
- "Technical Debt in AI Systems" is the final section — it's a broad topic that deserves its own tab, not an appendix to Cloud Platforms
- "HuggingFace Ecosystem Production Depth" is placed after an AWS-specific deep dive — implies AWS is the default and HuggingFace is secondary; a vendor-neutral comparison should lead
- No section on Azure-specific or GCP-specific deep dives to match the AWS SageMaker section — the tab is asymmetric
- ROI Template is a valuable artifact but it's placed late — ROI justification is the first conversation in any cloud platform selection, not the last

---

### Glossary

| Dimension | Score | Notes |
|---|---|---|
| Beginner Friendliness | 8 | Alphabetical navigation with cross-references is well-suited for all levels |
| Readability | 9 | A–Z structure with sub-section anchors is excellent |
| Architecture Relevance | 7 | AKP, MCP, A2A, AG-UI — architecture terms are present |
| Use of Examples | 4 | Glossary definitions rarely include worked examples by nature |
| Use of Analogies | 4 | Glossary definitions rarely include analogies by nature |
| Learning Flow | 7 | Alphabetical order is functional; no thematic grouping option visible |

**Overall: 6.5**

**Flags:**
- No thematic view available — a learner who wants "all inference-related terms" or "all agent protocol terms" has no grouped view
- 74 terms is a small glossary for a 2,255-topic document — many terms referenced in Check Yourself questions do not appear in the glossary (e.g., "RULER", "ColBERT", "ANN")
- No "terms added this month" or freshness marker on glossary entries — a growing glossary without freshness signals becomes unreliable
- Check Yourself questions in the Glossary tab reference "production-ready vector database pipeline" and "transformer fine-tuning for sequence classification" — out of scope for a reference tab

---

## Summary Scoreboard

| Tab | BF | R | AR | EX | AN | LF | Avg |
|---|---|---|---|---|---|---|---|
| Quick Guide | 8 | 9 | 7 | 6 | 8 | 9 | **7.8** |
| RAG & Vector | 7 | 8 | 9 | 8 | 7 | 8 | **7.8** |
| LLMs & Foundation | 6 | 8 | 7 | 7 | 7 | 8 | **7.2** |
| Fine-tuning | 6 | 7 | 8 | 8 | 6 | 7 | **7.0** |
| Agents & Prompting | 6 | 7 | 9 | 8 | 6 | 6 | **7.0** |
| Q&A Vol 2 | 6 | 8 | 8 | 7 | 5 | 7 | **6.8** |
| Q&A Vol 3 | 5 | 8 | 9 | 7 | 5 | 7 | **6.8** |
| System Design | 5 | 7 | 10 | 8 | 4 | 7 | **6.8** |
| Q&A Vol 1 | 7 | 8 | 5 | 7 | 6 | 7 | **6.7** |
| Governance Deep Dive | 6 | 7 | 9 | 6 | 4 | 7 | **6.5** |
| Safety & Ethics | 6 | 7 | 8 | 6 | 5 | 7 | **6.5** |
| Glossary | 8 | 9 | 7 | 4 | 4 | 7 | **6.5** |
| MLOps / LLMOps | 5 | 7 | 9 | 6 | 4 | 7 | **6.3** |
| Start Here | 7 | 8 | 6 | 5 | 4 | 7 | **6.2** |
| Generative AI | 5 | 7 | 6 | 8 | 6 | 5 | **6.2** |
| RecSys · TS · Tabular | 5 | 7 | 8 | 7 | 4 | 6 | **6.2** |
| Interview Strategy | 6 | 7 | 5 | 7 | 5 | 7 | **6.2** |
| Cloud Platforms | 6 | 7 | 9 | 6 | 3 | 6 | **6.2** |
| Live Coding | 4 | 8 | 5 | 10 | 3 | 6 | **6.0** |
| ML Fundamentals | 6 | 7 | 4 | 7 | 5 | 7 | **6.0** |
| AI Career Path | 8 | 7 | 5 | 5 | 5 | 7 | **6.1** |
| AI Landscape | 5 | 7 | 8 | 6 | 3 | 6 | **5.8** |
| What's New | 6 | 7 | 5 | 4 | 3 | 5 | **5.0** |
| Math & Stats | 4 | 7 | 3 | 6 | 7 | 6 | **5.5** |
| Data Science | 6 | 7 | 4 | 6 | 5 | 7 | **5.8** |
| Dev Experience | 6 | 7 | 7 | 5 | 4 | 5 | **5.7** |
| Emerging Trends | 4 | 7 | 8 | 6 | 4 | 5 | **5.7** |
| People & Adoption | 8 | 7 | 3 | 5 | 5 | 7 | **5.8** |
| Role Paths | 6 | 7 | 5 | 5 | 3 | 6 | **5.3** |
| CV & NLP | 5 | 6 | 5 | 7 | 4 | 5 | **5.3** |
| Agentic Platform | 3 | 6 | 10 | 6 | 3 | 4 | **5.3** |
| Agent Runtime Ops | 4 | 6 | 9 | 5 | 3 | 5 | **5.3** |
| AI Infrastructure | 3 | 7 | 10 | 7 | 4 | 6 | **6.2** |
| Deep Learning | 4 | 5 | 4 | 7 | 5 | 4 | **4.8** |
| Long Context & SSMs | 3 | 5 | 8 | 5 | 2 | 5 | **4.7** |

---

## Cross-Cutting Problem Patterns

### Sections That Feel Like Research Papers

These sections lead with formalism, math, or technical architecture before establishing intuition. A learner encounters "what" before "why".

| Section | Tab | Why it reads as a paper |
|---|---|---|
| Backpropagation: The Full Derivation | Deep Learning | First content section; "Full Derivation" signals academic completeness over pedagogy |
| Diffusion Models: Complete Math & Architecture | Generative AI | First content section; combines math and architecture in one dense section |
| RoPE Context Extension: YaRN & LongRoPE | Long Context & SSMs | First content section; uses three acronyms in the title before any plain-language framing |
| Disaggregated Prefill / Decode (P/D split) | AI Infrastructure | Standalone section title reads as a technical paper section heading |
| AKP — 8-Plane Reference Architecture | Agentic Platform | First content section; "reference architecture" signals spec document, not tutorial |
| RLHF → DPO → GRPO (from weekly plan) | Start Here / Fine-tuning | Loss derivations without prior intuition scaffold |
| Preference Optimisation Zoo | Fine-tuning | "Zoo" is playful but the content is a taxonomy of loss functions without entry-level framing |
| Long-Context Benchmarks — what to actually measure | Long Context & SSMs | "What to actually measure" is a research evaluation framing |
| Distributed Training Which Strategy for Which Problem | AI Infrastructure | Implies the reader already knows the strategies before the decision guide helps |

---

### Sections That Feel Like Interview Preparation Notes

These sections are well-structured for recall but are optimised for Q&A performance rather than conceptual understanding.

| Section | Tab | Why it reads as interview notes |
|---|---|---|
| What Interviewers Actually Test by Company Type | AI Landscape | Explicitly interview-framed; placed inside an orientation tab |
| Interview Signal Map by Role | AI Landscape | Same issue — interview framing in a landscape/orientation tab |
| Top 20 Must-Know Answers | Role Paths | List-based recall, no conceptual scaffolding |
| Top Formulas to Remember | Role Paths | Reference list without worked context |
| 1-Page Cheat Sheets by Role | Role Paths | Cheat sheets are by definition interview-prep artifacts |
| Common Interview Mistakes to Avoid | Interview Strategy | Closing a tab on avoidance rather than mastery |
| Behavioral Questions STAR Templates | Interview Strategy | Template-fill format optimised for recall performance |
| Interview Coding Framework 5 Steps Every Time | Live Coding | Meta-process for interviews, not for learning to code |
| Volume 1 / 2 / 3 answer calibration rubrics | Q&A Vols 1–3 | Calibration against "Weak / Solid / Senior" is interview-level scoring |

---

### Sections That Introduce Jargon Before Intuition

These sections use technical terms in their title or opening structure without a plain-language primer preceding them within the same tab.

| Section | Tab | Jargon introduced without prior intuition |
|---|---|---|
| RoPE Context Extension: YaRN & LongRoPE | Long Context & SSMs | YaRN, RoPE, LongRoPE |
| AKP — 8-Plane Reference Architecture | Agentic Platform | AKP (never expanded in a section title within the tab) |
| Disaggregated Prefill / Decode (P/D split) | AI Infrastructure | P/D split, prefill, decode as distinct phases |
| Enterprise Legacy Connectors (IIB/TIBCO) | Agent Runtime Ops | IIB, TIBCO — product-specific middleware terms |
| GRPO + RLVR — the reasoning-model recipe | Fine-tuning | GRPO, RLVR — both introduced without prior section establishing the reasoning-model context |
| Preference Optimisation Zoo | Fine-tuning | DPO, ORPO, SimPO, GRPO listed as equals without a decision ladder |
| LLM & Agent Observability — OpenTelemetry GenAI Conventions | MLOps / LLMOps | OpenTelemetry GenAI Conventions — standards body jargon |
| MLA, Mamba, RULER (in Quick Guide role path) | Quick Guide | Three acronyms in one topic title with no primer |
| Vendor Agent SDKs | Agents & Prompting | Vendor-specific framing without a neutral mental model first |
| BPE Tokenizer: Complete Implementation from Scratch | CV & NLP | BPE — term used in title before tokenization as a concept is introduced |

---

### Sections Missing Examples

These sections have no hands-on, code, or scenario-based example visible in their section titles or sub-section structure.

| Section | Tab | What example is missing |
|---|---|---|
| What's New — Current Snapshot Buckets | What's New | How to apply freshness information to a study plan |
| Role Paths — 1-Page Cheat Sheets by Role | Role Paths | What a completed cheat sheet looks like |
| What's New — Freshness Index by Tab | What's New | How to use a freshness score in practice |
| AI Landscape — Role Taxonomy | AI Landscape | A day-in-the-life example for each role |
| AI Landscape — 2026 Tech Stack Map | AI Landscape | A sample architecture using tools from the stack |
| Agentic Platform — AKP Component Responsibilities | Agentic Platform | A worked request trace through all 6 planes |
| People & Adoption — Pilot vs Enterprise Rollout | People & Adoption | A case study of a real rollout |
| Dev Experience — Model Access Tiers | Dev Experience | A worked example of requesting and receiving model access |
| Governance — AI Governance Policy vs Technology Controls | Governance | A scenario where policy and technical controls conflict |
| Math & Stats — Math Prerequisites by Role | Math & Stats | A sample "what you need to know for ML Engineer role" prerequisites checklist |
| Agent Runtime Ops — Prompt Drift Detection | Agent Runtime Ops | A concrete example of a prompt that has drifted and how to detect it |

---

### Sections Missing Analogies

These sections cover abstract concepts where an analogy would significantly reduce cognitive load, but no analogy frame is visible in section titles or known scaffold.

| Section | Tab | Suggested analogy direction |
|---|---|---|
| Long Context & SSMs — RoPE Context Extension | Long Context & SSMs | "Extending a ruler vs replacing it" |
| Long Context & SSMs — Mamba / SSMs | Long Context & SSMs | "A conveyor belt that forgets old items vs a whiteboard" |
| Agentic Platform — all AKP sections | Agentic Platform | "Power grid: generation / transmission / distribution / metering" |
| AI Infrastructure — GPU Memory Hierarchy | AI Infrastructure | "Hotel room (registers) vs hallway (shared memory) vs lobby (DRAM) vs outside (disk)" |
| AI Infrastructure — Disaggregated Prefill/Decode | AI Infrastructure | "Assembly line with separate stations for setup vs production" |
| Agent Runtime Ops — Prompt Drift | Agent Runtime Ops | "Instrument drift in manufacturing — gradual deviation from spec" |
| Governance — Saga Pattern | Governance | "Undo receipt" — reversing a distributed transaction like refunding a multi-step purchase |
| Emerging Trends — MoE | Emerging Trends | "Specialist team vs generalist: you route the question to the expert" |
| Emerging Trends — Reasoning Models | Emerging Trends | "System 1 vs System 2 thinking (Kahneman)" |
| Data Science — Uplift Modelling | Data Science | "Targeting the persuadable voter, not the sure bet" |
| Math & Stats — Information Bottleneck | Math & Stats | "Compressing a photograph without losing the subject" |

---

### Sections Missing Architecture Guidance

These sections are abstract or algorithmic but never connect to a system-level decision a platform or solution architect would make.

| Section | Tab | Missing architecture connection |
|---|---|---|
| Math & Stats (entire tab) | Math & Stats | When does an architect need to understand gradient descent vs trust it as a black box? |
| Deep Learning (entire tab) | Deep Learning | How does the choice of normalisation or activation affect inference latency or fine-tuning cost? |
| ML Fundamentals — Unsupervised Learning | ML Fundamentals | When would you deploy a clustering model vs a classification model in a production pipeline? |
| People & Adoption (entire tab) | People & Adoption | How does organisational structure map to platform component ownership? |
| Data Science — Causal Inference | Data Science | How does a causal inference platform integrate with an ML experimentation platform? |
| Live Coding (entire tab) | Live Coding | How does each implementation connect to a production system component? |
| CV & NLP — Computer Vision: Architectures | CV & NLP | When to use off-the-shelf vision API vs fine-tuned vision model vs train from scratch |
| Interview Strategy (entire tab) | Interview Strategy | How does interview preparation map to demonstrating architecture competency? |

---

### Sections That May Overwhelm Architects New to AI

These are sections likely to be encountered by a solution architect or enterprise architect approaching AI for the first time, which use language or framing that assumes deep ML background.

| Section | Tab | Overwhelm trigger |
|---|---|---|
| AKP — 8-Plane Reference Architecture | Agentic Platform | "8 planes" introduced without any reference to what the system is trying to do |
| Disaggregated Prefill / Decode | AI Infrastructure | Requires understanding of KV cache and GPU memory before "disaggregated" means anything |
| RoPE Context Extension: YaRN & LongRoPE | Long Context & SSMs | Three acronyms, zero analogy, zero plain-language opener |
| GRPO + RLVR — the reasoning-model recipe | Fine-tuning | Both acronyms are undefined in the section title; "recipe" implies ease that the content doesn't deliver |
| Preference Optimisation Zoo | Fine-tuning | A taxonomy of loss functions without any framing for why the zoo exists |
| Long-Context Benchmarks — RULER | Long Context & SSMs | RULER is a benchmark acronym that appears with no expansion |
| Quantisation — the 2026 menu | AI Infrastructure | NF4/AWQ/GPTQ listed without the core intuition that quantisation trades precision for speed |
| GPU Memory Hierarchy Why Bandwidth Matters | AI Infrastructure | Requires hardware architecture background to follow the "why bandwidth" framing |
| Governance — Saga Pattern Compensating Transactions | Governance | Distributed systems terminology that will stop most AI practitioners |
| AKP Component Responsibilities | Agentic Platform | Architectural vocabulary specific to the AKP framework with no prior grounding |

---

## Prioritised Improvement Opportunities

### High Priority

These issues affect the most important tabs (highest traffic, highest architectural relevance) or block the learning experience for the largest audience.

---

**H1 — Deep Learning tab: add intuition-first sections before the derivation**

*Tabs:* Deep Learning  
*Issue:* Only 2 content sections after visual overview; first section is a full derivation. The tab underpins the entire document but has the thinnest scaffolding.  
*Opportunity:* Add "Why Neural Networks? The problem classical ML can't solve" and "What does a layer actually do?" before the backpropagation derivation. Add a standalone activations section and a "what transformers replaced and why" bridge section.  
*Impact:* Every subsequent tab (LLMs, GenAI, Fine-tuning, Agents) assumes Deep Learning is understood. Fixing this improves comprehension across ~15 downstream tabs.

---

**H2 — Long Context & SSMs tab: add analogy and plain-language primer before all technical sections**

*Tabs:* Long Context & SSMs  
*Issue:* Lowest analogy score (2/10) in the document. First section is RoPE Extension — a graduate-level technique. No "why long context matters" section visible.  
*Opportunity:* Add a "Why this tab exists — the context window problem in plain language" opener. Add a "conveyor belt vs whiteboard" type analogy for SSMs vs transformers. Add a decision aid: "when does long context beat RAG?"  
*Impact:* This tab is rated the most confusing for architects new to AI. Fixing it removes the single highest overwhelm risk in the document.

---

**H3 — Agentic Platform tab: resolve structural duplication and add "what problem does this solve?" opener**

*Tabs:* Agentic Platform  
*Issue:* Five near-identical AKP section titles in sequence; "What is Agent Core?" is section 12; no plain-language opener.  
*Opportunity:* Consolidate the five AKP architecture sections into one master section with sub-headings. Move "What is Agent Core?" to section 1. Add "The problem this platform solves: why you can't just call an API" as an orientation opener.  
*Impact:* Second-highest overwhelm risk for architects. Architecture Relevance is 10/10 but Learning Flow is 4/10 — the content is right, the structure is not.

---

**H4 — Start Here: reposition Learning Command Center after the dependency map**

*Tabs:* Start Here  
*Issue:* The 6-mode Command Center widget fires before a learner has completed the 3-step orientation. New learners hit a complex dashboard before they understand the document.  
*Opportunity:* Move the Learning Command Center to after Step 3 (Weekly Study Plan). Add a one-paragraph analogy at the very top: "This document is a GPS for AI knowledge — Step 1 sets your destination, Step 2 shows the road, Step 3 gives you the schedule."  
*Impact:* Start Here is the entry point for every learner. Its flow directly determines drop-off.

---

**H5 — Emerging Trends tab: add a thematic grouping layer and remove structural duplication**

*Tabs:* Emerging Trends  
*Issue:* "Reasoning Models" appears as sections 1 and 9; 11 sections with no thematic arc; 8 different content modules are currently co-located here (per modularisation plan).  
*Opportunity:* Group sections into 3 themes: (a) New model paradigms, (b) New protocols and patterns, (c) New deployment realities. Add a "2026 paradigm shift" opener. Remove or merge the duplicate Reasoning Models sections.  
*Impact:* This tab is frequently referenced from Quick Guide as the destination for cutting-edge content. Its incoherence reduces the value of every tab that points to it.

---

**H6 — CV & NLP tab: resolve confirmed structural duplication**

*Tabs:* CV & NLP  
*Issue:* "CV vs NLP Task Map" and "CV vs NLP Task Mapping" are near-identical; "Transformer Transfer Learning CV vs NLP" and "Transfer Learning: CV vs NLP" are near-identical. Four sections are likely DOM duplicates.  
*Opportunity:* Audit and consolidate duplicates. The tab should have one task-map section and one transfer learning section.  
*Impact:* Structural duplication undermines learner trust — if they see the same content twice, they question whether the rest of the document is reliable.

---

**H7 — Fine-tuning tab: merge LoRA derivation sections and add RLHF intuition opener**

*Tabs:* Fine-tuning  
*Issue:* "LoRA: The Math & Implementation" and "LoRA Math Complete Derivation" are near-duplicate sections. RLHF has no intuition-first section.  
*Opportunity:* Merge LoRA math sections into one. Add "RLHF in plain language — why reward matters" before the code-heavy section.  
*Impact:* Fine-tuning scores 7.0 overall but has 13 sections — the highest count in the document. Reducing to 11 focused sections would improve completion rate.

---

**H8 — AI Infrastructure tab: resolve distributed training duplication and add cost model section**

*Tabs:* AI Infrastructure  
*Issue:* Distributed Training appears in sections 2 and 5; no cost model section visible.  
*Opportunity:* Merge distributed training sections. Add "The cost envelope: how much does it cost to serve a model?" as a dedicated section — this is the first architecture question any budget-constrained team asks.  
*Impact:* Architecture Relevance is 10/10 but the tab has the third-highest overwhelm score. A cost framing would ground the technical content in a business context architects understand.

---

### Medium Priority

These issues affect important content but have a smaller blast radius or are less likely to block a learner completely.

---

**M1 — AI Landscape tab: reorder sections to put Landscape before Role Taxonomy**

*Tabs:* AI Landscape  
*Issue:* Role Taxonomy is section 1 — asks the learner to self-categorise before understanding the space.  
*Opportunity:* Move "2026 Tech Stack Map" and "AI Capability Map" before Role Taxonomy. Add a one-sentence analogy: "The AI landscape is like a city — some zones are research labs, some are factories, some are service centres."  
*Impact:* Beginner Friendliness is 5/10; reordering and one analogy would raise it to ~7.

---

**M2 — Governance tab: resolve EU AI Act section duplication and add governance-in-CI/CD section**

*Tabs:* Governance Deep Dive  
*Issue:* "Policy vs Technical Controls" appears twice; "EU AI Act Risk Tier Decision" and "EU AI Act Which Tier?" are near-duplicates.  
*Opportunity:* Consolidate to one Policy vs Controls section and one EU AI Act section. Add "How governance integrates into your release pipeline" — a practical section that connects the checklist to the CI/CD tab.  
*Impact:* Governance scores 6.5 but is architecturally critical. Removing duplication raises readability; the CI/CD bridge raises architecture relevance.

---

**M3 — Quick Guide: add a "consequence" line to each mental model**

*Tabs:* Quick Guide  
*Issue:* 8 mental models are stated but not demonstrated. What happens if you ignore mental model #6 ("Inference is memory-bandwidth bound")?  
*Opportunity:* For each mental model, add one sentence: "Ignore this and you will [specific failure]." This is a single authoring pass across 8 items.  
*Impact:* Quick Guide scores 7.8 — the highest in the document. This improvement elevates the best tab from good to exceptional.

---

**M4 — Agent Runtime Ops: add failure recovery section and resolve monitoring duplication**

*Tabs:* Agent Runtime Ops  
*Issue:* "Agent Monitoring What to Watch" and "Agent Monitoring Metrics" are near-duplicate sections. No failure recovery section.  
*Opportunity:* Merge the two monitoring sections. Add "When an agent gets stuck: recovery patterns and circuit breakers."  
*Impact:* Runtime Ops scores 5.3 with Architecture Relevance 9/10 — the gap between its relevance and its learning quality is one of the largest in the document.

---

**M5 — MLOps / LLMOps: elevate Reasoning-Model Observability and add LLMOps platform architecture section**

*Tabs:* MLOps / LLMOps  
*Issue:* Reasoning-Model Observability is last; no section on the architecture of an LLMOps platform itself.  
*Opportunity:* Move Reasoning-Model Observability to section 2 (after "What is an LLMOps platform"). Add "What does an LLMOps platform look like as infrastructure?" bridging MLOps to the System Design tab.  
*Impact:* MLOps scores 6.3 with Architecture Relevance 9/10 — similar gap to Agent Runtime Ops.

---

**M6 — What's New tab: promote Freshness Index and add "how to update your knowledge" workflow**

*Tabs:* What's New  
*Issue:* Freshness Index is last; no learner workflow for acting on freshness data.  
*Opportunity:* Move Freshness Index to section 1. Add "How to use this tab: the 10-minute freshness review" as a workflow.  
*Impact:* What's New scores 5.0 — lowest among the non-technical tabs. A single structural reorder would significantly improve its utility.

---

**M7 — Live Coding: move Interview Framework to section 1 and rename FAANG Standard**

*Tabs:* Live Coding  
*Issue:* Framework is section 3; "FAANG Standard" label is intimidating.  
*Opportunity:* Move Interview Coding Framework to section 1 as the meta-skill anchor. Rename section 1 to "Multi-Head Attention — Production Reference Implementation."  
*Impact:* Live Coding scores 6.0. The Framework-first change would improve Learning Flow from 6 to ~8.

---

**M8 — Role Paths: gate Revision Studio behind foundational tab completion**

*Tabs:* Role Paths  
*Issue:* Revision Studio is section 1 — you cannot revise what you haven't learned.  
*Opportunity:* Add a "complete at least one Foundations tab before starting revision" gate or note. Move Revision Studio to section 3 or later.  
*Impact:* Role Paths scores 5.3. This is a structural fix that doesn't require content authoring.

---

**M9 — System Design: move FRAME framework to section 1**

*Tabs:* System Design  
*Issue:* FRAME framework is the last section; it's the meta-skill that makes all scenarios learnable.  
*Opportunity:* Introduce FRAME in section 1, then apply it to each scenario.  
*Impact:* System Design scores 6.8 overall — a structural reorder improves Learning Flow from 7 to ~9 without any content authoring.

---

**M10 — Math & Stats: move Math Prerequisites by Role to section 1**

*Tabs:* Math & Stats  
*Issue:* Prerequisites section is mid-tab; a learner needs to know if they need this tab before reading it.  
*Opportunity:* Make "Math Prerequisites by Role" the first section. A learner who discovers they don't need the full derivations can skip confidently.  
*Impact:* Beginner Friendliness is 4/10. This single reorder would raise it to ~6 with no authoring.

---

### Low Priority

These issues are real but have lower blast radius, affect less frequently visited tabs, or require only minor authoring additions.

---

**L1 — Generative AI: consolidate VAE sections**

Three near-duplicate VAE sections (GANs/VAEs, Production Image Generation, VAE Complete Implementation) can be consolidated without changing the learning experience.

---

**L2 — Data Science: add architecture bridge for A/B testing platform**

The tab has no connection to how an experimentation platform is built. A one-paragraph bridge to the System Design and MLOps tabs would improve Architecture Relevance from 4 to ~6.

---

**L3 — People & Adoption: add one CoE case study**

"Pilot vs Enterprise Rollout" is the most important section but has no example. One anonymised or fictional case study (e.g., "a 500-person engineering org rolling out an internal code assistant") would raise Use of Examples from 5 to ~7.

---

**L4 — Cloud Platforms: add Azure and GCP deep-dive sections to match AWS SageMaker depth**

Currently asymmetric — AWS has a dedicated deep-dive, Azure and GCP do not. Two parallel sections would complete the platform comparison.

---

**L5 — Q&A volumes: add role-based filtering or priority tagging**

No mechanism for a learner to identify which Q&A items are must-knows for their role vs nice-to-knows. A simple tagging system (ML Engineer: Q1, Q4, Q7...) would add significant navigation value without content authoring.

---

**L6 — Glossary: add thematic groupings and freshness markers**

74 terms with no thematic view. Adding 5–6 themed clusters (inference terms / agent terms / training terms / regulatory terms / architecture terms) would enable quicker lookup for specific practitioners.

---

**L7 — Interview Strategy: reorder to end on Portfolio Presentation**

Currently ends on "Common Mistakes to Avoid" — a negative close. Ending on Portfolio Presentation is a positive, forward-looking finish.

---

**L8 — AI Career Path: update "2025 AI Job Market Reality" section title**

The year in the title will become stale. A relative framing ("Current AI Job Market") or a versioned date tied to the document's freshness system would prevent premature staling.

---

**L9 — RecSys · TS · Tabular: add a domain-selection opener**

Three sub-disciplines with no guidance on which to enter first. A "choose your sub-domain" decision aid at the top would reduce the 7-section density feeling.

---

**L10 — Dev Experience: remove "Go Deeper — Governance" section**

A governance deep-dive link inside a developer experience tab is disorienting. The link belongs in the Governance tab as a cross-reference, not as a section inside Dev Experience.

---

## Appendix: Check Yourself Question Scope Bleed

The most pervasive cross-cutting issue in the document is Check Yourself question assignment. Questions are surfaced in tabs where the topic they test is not addressed by the tab's content. This creates a "surprise quiz" effect that damages learner confidence.

**Most frequent out-of-scope question appearances:**

| Question | Appears in tabs where it's out of scope |
|---|---|
| How do you prevent data leakage in time-series model evaluation? | 24 tabs — appears in every tab including Safety & Ethics, Agentic Platform, Dev Experience |
| What is the vanishing gradient problem? | 13 tabs — appears in Interview Strategy, Emerging Trends, AI Career Path |
| How do you design evaluation for a code generation model? | 22 tabs — appears in AI Infrastructure, People & Adoption, Agent Runtime Ops |
| Explain the complete RLHF pipeline with code | Safety & Ethics, MLOps, Dev Experience — tabs that don't cover RLHF |
| How would you design a recommendation system for a video streaming platform? | 10 tabs — appears in Safety & Ethics, Agent Runtime Ops |

**Recommendation:** Assign each Check Yourself question to a maximum of 3 tabs — the home tab where the concept is taught, the first application tab where it becomes relevant, and the Q&A volume where it is formally tested. This is a data clean-up task in the question bank, not a content authoring task.

---

*Audit prepared for AI Gita content modernisation. No content was rewritten. All findings are derived from section titles, topic structure, learning module markers, and pedagogical scaffold signals in the content inventory.*
