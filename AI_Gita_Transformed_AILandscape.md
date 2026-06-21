# AI Landscape — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

The AI landscape is the map of what exists, what each thing does, which organisations build which parts, and how they fit together into a working system.

As of 2026, the landscape has three distinct layers:

**Layer 1 — Foundation (the models)**
Large language models, multimodal models, embedding models, image generation models. These are the capability engines — they do the work. Providers: Anthropic (Claude), OpenAI (GPT-4o, o3), Google (Gemini), Meta (Llama), Mistral, Cohere, and dozens of others.

**Layer 2 — Infrastructure (the plumbing)**
The systems that make models deployable at scale: cloud ML platforms (AWS Bedrock, Azure OpenAI, GCP Vertex), vector databases (Pinecone, Weaviate, pgvector), observability tools (LangFuse, Helicone), MLOps platforms (MLflow, Weights & Biases), serving frameworks (vLLM, SGLang).

**Layer 3 — Applications (the products)**
AI-powered products built on top of layers 1 and 2: enterprise copilots (Microsoft Copilot, Salesforce Einstein), developer tools (GitHub Copilot, Cursor), custom enterprise applications built by your organisation.

**Why this matters for architects:** when someone asks "should we use AI for X?", the answer is never just "use an LLM." It's a decision about which capability from layer 1, hosted on which infrastructure from layer 2, built into which application pattern from layer 3. The landscape map is the vocabulary for making that decision clearly.

---

## 2. Why Should I Care

### For Solution Architects

The AI landscape changes every 3–6 months. A model that was state-of-the-art in early 2024 may now be outperformed by open-weight alternatives at 1/10th the cost. Capabilities that required custom ML engineering in 2023 (structured extraction, multi-step reasoning, multimodal understanding) are now available as API calls.

This rate of change creates two risks:
1. **Technology lock-in:** building on a specific model or vendor without understanding the landscape makes migration harder
2. **False limitation:** assuming AI cannot do something because a previous attempt failed, when the current generation of models handles it reliably

Architects who track the landscape make better build-vs-buy decisions, select the right tool for each use case, and avoid both over-engineering and premature optimisation.

### For Enterprise Architects

> **What is a token?** A token is the basic unit of text that LLMs process — and the unit that APIs charge for. Roughly 3–4 characters or 0.75 words in English. "Hello world" = 2 tokens. 1,000 tokens ≈ 750 words ≈ 1.5 pages. APIs charge separately for **input tokens** (your prompt) and **output tokens** (the model's response). When you see pricing like "$2 per million tokens", that is the cost per million of these text chunks.

The AI landscape creates new vendor categories that don't map cleanly to existing procurement processes:
- **LLM API providers** (Anthropic, OpenAI): subscription or pay-per-token; subject to model deprecation cycles; require data processing agreements
- **Cloud AI platforms** (AWS Bedrock, Azure OpenAI, GCP Vertex): enterprise agreements, SLAs, data residency — familiar procurement but new capabilities
- **Open-weight models** (Meta Llama, Mistral): free to use but require self-hosting infrastructure and operational overhead
- **AI-native SaaS** (Salesforce Einstein, ServiceNow Now Assist): AI bundled into existing SaaS — fastest to deploy, least flexible

Enterprise architecture governance needs a framework for evaluating these categories — not just evaluating individual products.

---

## 3. Think About It Like This (Analogy)

**The Utilities Analogy**

The AI landscape today is similar to the utilities landscape of the early 20th century: a fast-moving, partially mature infrastructure that every organisation needs but few fully understand.

**Foundation models (Layer 1) are like electricity generation.** Different generators (coal, hydro, nuclear — or Anthropic, OpenAI, Google) produce essentially the same output (electrical power / text generation capability). The quality and cost differ; the interface is standardised (plug / API). You don't need to know how the power plant works to use electricity.

**Infrastructure (Layer 2) is like the electrical grid and distribution system.** The transformer substations, switching infrastructure, and distribution network (cloud platforms, serving infrastructure, databases) make the raw power useful for specific applications. Some organisations build their own substations (self-hosted infrastructure); most use the grid (cloud services).

**Applications (Layer 3) are like the appliances and industrial equipment.** A factory (enterprise application) plugged into the grid has very different requirements from a household (consumer app). The applications determine value; the infrastructure determines reliability and cost.

**The open-weight vs closed-model debate** is like the debate between municipal power (open, community-owned) and private utilities: open-weight models are free to use but require you to build and maintain your own distribution infrastructure; closed APIs are pay-per-use with the infrastructure maintained by the provider.

**The landscape changes fast** — like the transition from gas lighting to electric lighting in the 1890s. Organisations that mapped the technology clearly and made deliberate infrastructure choices scaled well; those that ignored the shift or chose the wrong infrastructure faced expensive rewiring later.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 The 2026 AI Capability Map

Not all AI problems are LLM problems. The capability map aligns problem types to the right technology:

**Text understanding and generation**
- Summarisation, Q&A, classification, extraction, translation, writing → **LLMs** (GPT-4o, Claude, Gemini, Llama)
- Semantic similarity, search, clustering, deduplication → **Embedding models** (text-embedding-3-large, BGE, E5)

**Structured data and prediction**
- Tabular prediction (churn, fraud, demand) → **Traditional ML** (XGBoost, Random Forest, LightGBM) — often outperforms LLMs on tabular tasks
- Time series forecasting → **Specialised models** (TFT, N-BEATS) or **LLMs** (for narrative context + quantitative)
- Recommendation → **Two-tower models, matrix factorisation, deep learning RecSys**

**Image and video**
- Image generation → **Diffusion models** (Stable Diffusion, DALL-E, Flux)
- Image classification, object detection → **Vision models** (ViT, ResNet, YOLOv8)
- Document/image understanding (OCR + comprehension) → **Vision-language models** (GPT-4V, Claude Vision, Gemini Vision)

**Audio**
- Speech-to-text → **Whisper** (OpenAI), Deepgram, AssemblyAI
- Text-to-speech → ElevenLabs, OpenAI TTS, AWS Polly
- Music/audio generation → Suno, AudioCraft (niche, emerging)

**Code**
- Code generation, completion, review → **LLMs** (especially Claude Sonnet, GPT-4o, DeepSeek-Coder, CodeLlama)
- Code execution, testing → requires separate execution sandbox

> **Explain Like I'm an Architect**
>
> The most expensive mistake in enterprise AI today is treating LLMs as a universal tool. It's the equivalent of saying "we should use a database for everything" — technically you could, but a spreadsheet handles a budget tracker, a message queue handles event streaming, and a relational database handles transactions. Each problem has a right tool.
>
> The AI capability map above is a problem-to-tool matching guide. When someone says "we should use AI for supply chain forecasting," the question is: which row in that map does this problem sit in? Supply chain demand forecasting with structured historical data is a "time series forecasting" problem — TFT or LightGBM, not an LLM. Sentiment analysis of customer reviews is a "text understanding" problem — an LLM or embedding model. Generating personalised outreach emails is a "text generation" problem — an LLM.
>
> The discipline of asking "which row?" before selecting a tool separates AI-fluent architects from AI-aware ones.
>
> **Common Misconception:** "LLMs are getting so good they'll replace all other AI approaches." For unstructured language tasks, this is increasingly true. For structured tabular prediction, time-series forecasting, and collaborative filtering recommendation, it is not — classical methods still outperform LLMs on accuracy at 1/10th the cost, because the signal in those problems is in numbers and patterns, not in language. This distinction will remain true for the foreseeable future.

**The architect's decision rule:** always ask "is this an LLM problem?" before defaulting to one. For structured/tabular problems with clear labels and clean data, classical ML frequently outperforms LLMs at lower cost. LLMs excel at unstructured text, multi-step reasoning, and problems where the solution is hard to specify algorithmically.

### 4.2 Role Taxonomy: Who Does What

Understanding AI roles is essential for architects building AI teams and assessing partner capabilities.

> **What is RAG?** RAG (Retrieval-Augmented Generation) means: instead of relying on the model's built-in training knowledge, you retrieve relevant documents from your own systems at query time and feed them to the model alongside the question. The model answers from *your data*, not from what it memorised during training. Think of it as giving the model a cheat-sheet of relevant pages from your internal wiki before asking it a question.

| Role | Primary responsibility | Key skills | Where they sit |
|---|---|---|---|
| **ML Engineer** | Builds and trains models; implements ML pipelines | PyTorch/TF, distributed training, MLOps | AI/ML team |
| **AI/LLM Engineer** | Builds LLM-powered applications; prompt engineering, RAG, agents | LLM APIs, RAG, LangChain/LlamaIndex, evaluation | Product/AI team |
| **Data Scientist** | Statistical analysis, experiment design, business insight | Statistics, Python, SQL, A/B testing | Data/analytics team |
| **MLOps Engineer** | Deploys and operates ML systems; CI/CD for models | Kubernetes, monitoring, feature stores, drift detection | Platform/infra team |
| **AI Architect** | Designs AI system architecture; governance; platform standards | System design, security, governance frameworks | Architecture team |
| **Solution Architect (with AI)** | Designs enterprise AI solutions; vendor selection; integration | Business requirements, API integration, AI capability map | Client-facing / internal |

**Key distinction for solution architects:** you don't need to be able to do the ML Engineer's job. You need to understand what each role produces and what hand-offs between roles look like. The most common gap in enterprise AI projects is the absence of an AI Architect who bridges technical capability and enterprise constraints.

### 4.3 Open-weight vs Closed Models: The Enterprise Decision

This is one of the most consequential architectural decisions in any AI programme. It's not just a technical choice — it's a governance, cost, and capability choice.

**Closed/proprietary models (GPT-4o, Claude, Gemini)**

Accessed via API; weights are not publicly available:

| Dimension | Characteristic |
|---|---|
| Quality | Highest available; regularly updated |
| Context window | 128K–1M tokens |
| Cost | Pay-per-token; 2026 range £0.0003–0.015/K tokens |
| Data privacy | Prompts leave your network; data processing agreement required |
| Operational overhead | Zero — provider manages infrastructure |
| Customisation | Limited to prompting, system prompts, fine-tuning via API |
| Availability | Provider SLA; typically 99.9%+ |
| Vendor risk | Subject to pricing changes, deprecation cycles |

**Open-weight models (Llama-3, Mistral, Qwen, DeepSeek)**

Weights are publicly available; you host and operate them:

| Dimension | Characteristic |
|---|---|
| Quality | Strong at 7B–70B; competitive with closed for many tasks at fine-tuned scale |
| Context window | Typically 8K–128K depending on model |
| Cost | GPU compute cost only; no per-token charge |
| Data privacy | Data stays on your infrastructure — full control |
| Operational overhead | High — you run the GPU fleet, upgrades, monitoring |
| Customisation | Full — can fine-tune, modify, distil |
| Availability | Dependent on your infrastructure |
| Vendor risk | No vendor lock-in; model is yours |

> **Explain Like I'm an Architect**
>
> Think of closed API models as SaaS and open-weight models as self-hosted software. You've made this decision hundreds of times in your career.
>
> **Closed API (SaaS model):** you pay per use, the vendor handles infrastructure, updates, and reliability. Fast to get started. Operational overhead is near zero. The trade-off: your data goes to the vendor's servers, you're subject to their pricing changes, and if they deprecate the model you're using, you must migrate.
>
> **Open-weight (self-hosted model):** the weights are yours to run. Data never leaves your network. Cost is compute-only (no per-token tax). But you provision the GPUs, manage the serving infrastructure, handle upgrades, and absorb any outages. There is no Anthropic or OpenAI support desk — your MLOps team is the support desk.
>
> The decision is not about which model is "better" — it's about which risk profile you're buying. Closed API trades data residency and vendor lock-in risk for operational simplicity. Open-weight trades vendor risk for operational complexity.
>
> **The hybrid pattern most mature enterprises use:** closed API for high-stakes, low-volume tasks where frontier quality matters (legal analysis, complex reasoning) and open-weight for high-volume, cost-sensitive, or data-sensitive workloads (customer service at scale, anything processing PII that cannot leave your jurisdiction).

**The enterprise decision matrix:**

| Signal | Closed API | Open-weight |
|---|---|---|
| Need latest frontier reasoning capability | ✅ | ❌ |
| Data cannot leave your network (legal/regulated) | ❌ | ✅ |
| Volume > 1M requests/day (cost break-even) | ❌ | ✅ |
| Need to fine-tune for specific domain | Partial (API fine-tuning) | ✅ Full control |
| Team has GPU ops capability | — | ✅ Required |
| Fast time-to-production | ✅ | ❌ |
| Startup / no ops team | ✅ | ❌ |
| Regulatory: model lineage + audit required | Partial | ✅ Full |
| Multimodal (image + text) | ✅ | Growing (LLaVA, Idefics) |

**The hybrid pattern** (most mature enterprises): use closed APIs for frontier capability and low-volume high-stakes tasks (legal analysis, complex reasoning); use open-weight for high-volume, cost-sensitive, or data-sensitive workloads (customer service at scale, internal knowledge management).

### 4.4 The 2026 Tech Stack Map

**How to read this map:** Focus on category literacy, not tool mastery. The goal is to know what each layer does and which tools dominate it — not to evaluate every product. The **bold/starred entries** below are the tools you're most likely to encounter in enterprise AI conversations in 2026; the others are worth knowing exist.

A production AI system in 2026 pulls from each of these layers:

```
User Interface / Application
  (web app, chatbot, API, internal tool)
        │
        ▼
Orchestration / Application Layer
  LangChain · LlamaIndex · LangGraph · custom
        │
        ▼
LLM / Model Layer
  Closed: Anthropic Claude · OpenAI GPT-4o · Google Gemini
  Open: Llama-3 · Mistral · Qwen · DeepSeek
  Serving: vLLM · SGLang · TGI
        │
        ▼
Knowledge / Data Layer
  Vector DB: Pinecone · Weaviate · pgvector · Qdrant · Chroma
  Document store: S3 · Azure Blob · GCS
  Feature store: Tecton · Feast · Vertex Feature Store
        │
        ▼
Cloud Platform Layer
  AWS Bedrock · Azure OpenAI · GCP Vertex AI
  Self-managed Kubernetes (for open-weight serving)
        │
        ▼
MLOps / Observability Layer
  Experiment tracking: MLflow · W&B
  LLM observability: LangFuse · Helicone · Arize
  Model registry: MLflow · SageMaker Model Registry
  CI/CD: GitHub Actions · Tekton
        │
        ▼
Data Layer
  Warehouses: Snowflake · BigQuery · Redshift
  Lakes: Delta Lake · Iceberg · Hudi
  Real-time: Kafka · Kinesis
```

Most commonly encountered in enterprise: **OpenAI/Anthropic/Google APIs** (foundation layer), **LangChain/LangGraph** (orchestration), **Pinecone/Weaviate/pgvector** (vector store), **vLLM** (self-hosted serving), **MLflow/Weights & Biases** (experiment tracking).

**The architect's role:** you don't need to master every tool in this stack. You need to: (a) know the category each tool fits, (b) have evaluated at least one tool per critical category for your organisation's requirements, and (c) have defined the interfaces between layers as clean contracts rather than implementation details.

### 4.5 The Build vs Prompt vs Fine-tune vs Train Decision

Every AI feature starts with this decision:

**Build (from scratch or near-scratch):**
- Use when: unique data, unique task, existing models don't come close
- Cost: high (engineering months, training costs)
- Fit for: core product differentiators where AI capability is the business

**Prompt (use a general model via API):**
- Use when: the task is within the general model's capability and no domain-specific data is available
- Cost: lowest initial; API costs scale with usage
- Fit for: most enterprise AI use cases — don't underestimate what good prompting achieves

**Fine-tune (adapt a base model to your domain):**
- Use when: prompting achieves 80% quality; you need 95%+; you have 500+ labelled examples; cost or latency at scale demands a smaller model
- Cost: medium one-time; lower running costs than frontier API
- Fit for: high-volume, well-scoped tasks with stable requirements

**Train from scratch / pre-train:**
- Use when: unique data modality (proprietary molecule structures, specialised sensor data), competitive differentiation in model capability itself
- Cost: very high (millions in compute + ML engineering)
- Fit for: research organisations, AI-native companies, large-scale commodity tasks

**The decision heuristic:**
```
1. Can a general-purpose LLM + good prompt solve this?
   → YES: use it; don't build what you can prompt
   
2. Are prompting limitations due to knowledge (missing facts) or behaviour (wrong format/style)?
   → Knowledge: add RAG
   → Behaviour: consider fine-tuning
   
3. Is fine-tuning justified by: volume economics, data sensitivity, or quality gap?
   → All three: fine-tune
   → None: stay on API
   
4. Is this task unique to you and core to your competitive advantage?
   → YES: invest in training
   → NO: use existing models
```

---

## 5. Enterprise Example

**Scenario: AI Platform Strategy for a Financial Services Group**

A financial services group (retail banking, insurance, wealth management) is building their enterprise AI strategy. The CTO has asked the architecture team to define which AI capabilities to buy, which to build, and which to host on which infrastructure.

**Current state (inventory of requests from business units):**
1. Customer service chatbot for retail banking (2M customer interactions/month)
2. Document extraction from loan applications (50K applications/month, PDF + scans)
3. Internal knowledge assistant for 8,000 employees
4. Fraud detection signal enhancement (tabular features, 10M transactions/day)
5. Regulatory compliance document review (500 complex documents/month)
6. Personalised product recommendations (online banking, 500K active users)

**Architecture team's landscape assessment:**

| Use case | Problem type | Right AI modality | Open vs closed | Rationale |
|---|---|---|---|---|
| Customer service chatbot | Text generation + knowledge retrieval | LLM + RAG | Closed API (Azure OpenAI EU) | Customer PII processed but stays in EU; frontier quality needed for customer trust; volume justifies dedicated Azure endpoint |
| Loan application extraction | Document understanding | Multimodal LLM | Closed API (Azure OpenAI Vision) | Handwritten + printed + varied formats; needs OCR + comprehension; data stays in EU |
| Internal knowledge assistant | Text generation + RAG | LLM + RAG | Closed API (Azure OpenAI) or open-weight | Internal docs are non-PII; Azure OpenAI for speed to deploy; evaluate open-weight at 6 months if volume justifies it |
| Fraud detection enhancement | Tabular prediction | Classical ML (XGBoost) + feature engineering | N/A — not an LLM problem | Structured numerical features; 10M tx/day; XGBoost outperforms LLMs on tabular with existing feature engineering; LLM only for narrative signal extraction |
| Regulatory compliance review | Long-form legal reasoning | Frontier LLM | Closed API (Claude Opus) | Highest-stakes task; complex legal reasoning; low volume (£120/month API cost at volume); data classification requires EU residency |
| Product recommendations | Collaborative filtering + context | Hybrid: RecSys + LLM | Classical RecSys for retrieval; LLM for personalised messaging | Recommendation is a collaborative filtering problem (user-item matrices); LLM adds personalised explanation layer; separation of concerns |

**Key decisions made:**

1. **Not everything is an LLM problem.** Fraud detection stays XGBoost. Product recommendations use classical RecSys for the retrieval layer. Forcing LLMs onto tabular/collaborative filtering problems would decrease accuracy and increase cost.

2. **Data residency drives infrastructure.** All PII-touching use cases use Azure OpenAI EU endpoints. If volume grows to justify self-hosting, they'll evaluate open-weight on EU-hosted GPU clusters.

3. **Frontier model only where it's justified.** Claude Opus (highest quality) is reserved for regulatory compliance (500 documents/month, £120/month). Everything else uses Sonnet or GPT-4o-mini tiers.

4. **Phased open-weight evaluation.** Internal knowledge assistant starts on Azure OpenAI for speed. 6-month review: if volume exceeds break-even (~100K queries/day), evaluate self-hosted Llama-3 70B with QLoRA fine-tuning on internal documents.

**Governance outcome:**
- Approved model catalogue: 3 providers (Anthropic via API, Azure OpenAI, self-hosted via Bedrock Custom Model Import for approved open-weight)
- Data classification matrix: Tier 1 (internal, non-PII) → any approved provider; Tier 2 (customer PII) → EU-hosted only; Tier 3 (regulated data) → self-hosted or Azure OpenAI EU with BAA
- Review cadence: landscape review every 6 months — model deprecations, new capabilities, open-weight quality improvements

---

## 6. Architecture Perspective

### The AI Capability Maturity of Your Organisation's Partners

When evaluating partners and vendors, their AI capability level directly affects delivery risk. The signals to look for:

**Immature AI capability (high risk):**
- "AI-powered" claims without specifics about which models, which evaluation, which governance
- Demos that work on curated examples but no production deployment evidence
- No mention of hallucination mitigation, output validation, or human review processes
- Prompt engineering is their full AI capability — no evaluation harness, no versioning

**Mature AI capability (lower risk):**
- Specific model choices with documented rationale
- Evaluation frameworks (automated metrics + human eval)
- Production deployments with availability SLAs
- Governance processes: data handling, model versioning, incident response
- Clear articulation of what AI does and doesn't handle (human-in-the-loop design)

### How to Communicate AI Architecture Decisions to Stakeholders

When presenting AI architecture decisions to senior stakeholders, the conversation is rarely about deep technical knowledge. Effective communication focuses on:

1. **Decision clarity:** "Why this model, not that one?" — can you explain the trade-off, not just state the choice
2. **Cost fluency:** "What does this cost at scale?" — concrete numbers, not "it depends"
3. **Failure mode awareness:** "What happens when the model is wrong?" — do you have a mitigation, not just optimism
4. **Governance literacy:** "How does this handle customer PII?" — not "we'll figure it out"
5. **Landscape awareness:** "Is there a better/cheaper alternative?" — have you looked at the full landscape, not just the first API you tried

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — Problem-to-tool matching**

A product manager says "we should add AI to our supply chain forecasting tool — can we use ChatGPT?" How do you respond?

> **Simple Explanation:** "Use ChatGPT for supply chain forecasting" is like "use a hammer for all construction." ChatGPT is a language model — it's designed for text. Supply chain forecasting is a numbers-and-patterns problem. You'd use a specialist tool: a model trained for time series prediction. The question isn't "should we use AI?" but "which type of AI matches which type of problem?"
>
> **Detailed Answer:** Start with the problem, not the tool. Supply chain forecasting is typically a structured/tabular prediction problem: time-series demand forecasting, inventory level prediction, supplier lead time estimation. For these problems, classical ML models (XGBoost, LightGBM, TFT for time series) typically outperform LLMs on accuracy at lower cost, because the signal is in the numbers, not the natural language. An LLM would be appropriate for: narrative signal extraction from supplier communications, exception report generation, Q&A over supply chain documentation. The answer is: "AI could help, but ChatGPT is likely not the right tool for the forecasting itself. Let me map out which specific problems need which AI capability, then we'll identify the right approach for each."
>
> **Architecture Takeaway:** Always start with a problem-to-modality mapping before selecting a tool. For every AI initiative, answer: is this a language problem, a numbers problem, an image problem, a search problem? The modality determines the tool category. Only then choose a specific product.

---

**Question 2 — Open vs closed at scale**

Your organisation has a choice between building on the OpenAI API vs deploying an open-weight Llama-3 70B model for a customer service chatbot (estimated 200K interactions/day). Walk through the decision.

> **Simple Explanation:** The open vs closed model decision is the "build your own data centre or use the cloud" decision from a decade ago — same principles, different asset (GPU serving infrastructure vs general compute). Below a certain volume, the operational overhead of running your own is more expensive than the per-use cloud cost. Above a certain volume, the economics flip. Run the numbers with your specific volume and GPU costs. The numbers in this example are the framework — your actual costs will differ.
>
> **Detailed Answer:** At 200K interactions/day the volume economics become relevant. Step 1 — estimate costs. 200K × (avg 800 input + 250 output tokens) = 160M input + 50M output tokens/day. API cost (GPT-4o-mini): 160M × £0.15/M + 50M × £0.60/M = £24 + £30 = £54/day = £1,620/month. Open-weight (2× A100 80GB at £3.50/hr): £3.50 × 2 × 24 × 30 = £5,040/month infrastructure + ~0.5 FTE MLOps engineer (~£3,000/month fully loaded) = £8,040/month. At 200K/day: API is cheaper. Break-even is closer to 500K–700K/day depending on model size and GPU spec. Step 2 — data residency. Does the customer service chatbot process PII? If yes, can you ensure data stays in your required jurisdiction via the API? Azure OpenAI has EU endpoints; direct OpenAI may not satisfy strict requirements. Step 3 — quality. Test both on your specific use case — don't rely on benchmarks. Step 4 — ops capability. Does your team have the skills to operate vLLM + GPU fleet reliably? Decision: at 200K/day, API is cheaper — use it unless data residency prevents it. Reassess at 12 months with actual volume data.
>
> **Architecture Takeaway:** Do the break-even analysis before making the infrastructure decision, not after. Define: (1) expected daily volume, (2) average token count per interaction, (3) API cost at that volume, (4) GPU infrastructure cost + ops FTE at that volume. The crossover point is your decision threshold. Revisit every 6 months as volume grows and API pricing changes.

---

**Question 3 — AI team roles**

Explain the difference between an MLOps Engineer, an ML Engineer, and an AI/LLM Engineer. When building an AI team, which role is most critical first?

> **Simple Explanation:** ML Engineer = the person who builds and trains the engine. AI/LLM Engineer = the person who takes a pre-built engine (GPT-4, Claude) and wires it into a product. MLOps Engineer = the person who keeps the engine running reliably in production. Most enterprises starting today don't need to build their own engines — they need someone who can wire a pre-built engine into their business, and someone who can keep that system healthy. That order: AI/LLM Engineer first, MLOps second, ML Engineer when you have a genuine need to train or fine-tune.
>
> **Detailed Answer:** ML Engineer: trains and builds models — PyTorch, distributed training, fine-tuning, custom architectures. Primary output: trained model artifacts. AI/LLM Engineer: builds applications using pre-trained models — prompt engineering, RAG systems, agent workflows, API integration, evaluation harnesses. Primary output: AI-powered features and systems. Does not typically train models from scratch. MLOps Engineer: deploys and operates ML/AI systems at scale — CI/CD pipelines for models, monitoring, feature stores, infrastructure management. Primary output: reliable, observable AI systems in production. Which is critical first depends on what you're building. For most enterprise organisations starting with AI: an AI/LLM Engineer is the highest-leverage first hire — they can deliver business value immediately using API-based models without requiring GPU infrastructure or deep ML expertise. MLOps capability becomes critical when you move from a single AI application to a portfolio of AI systems that need standardised deployment and monitoring. ML Engineers become essential when off-the-shelf models can't meet your requirements and fine-tuning or training is needed.
>
> **Architecture Takeaway:** The first AI hire should match your current build phase. If you're building API-based applications: AI/LLM Engineer. If you're moving to production reliability at scale: MLOps. If you're fine-tuning or training: ML Engineer. Hiring an ML Engineer when you need an AI/LLM Engineer is the most common mis-hire in enterprise AI teams.

---

**Question 4 — Provider standardisation**

A colleague argues "we should standardise on one AI provider to reduce complexity." What are the trade-offs and what's your recommendation?

> **Simple Explanation:** Standardising on one cloud provider for all infrastructure would have been a mistake in 2010, and standardising on one AI provider today has the same problem: you're locking in a trade-off that may not be correct for every use case. The correct standardisation point is the interface — build your applications to talk to an internal AI gateway, and let the gateway route to whichever provider is best for each request. Then you can add, switch, or remove providers without touching application code.
>
> **Detailed Answer:** The single-provider argument has merit and limits. Merits: simpler procurement (one vendor agreement, one data processing agreement), simpler developer experience (one SDK, one authentication model), simpler governance (one set of policies), potential volume discounts. Limits: (1) Different providers have different strengths — Claude Opus is often better at complex reasoning and long documents; GPT-4o-mini is cheap and fast for simple tasks; Gemini has the largest context window for full-corpus tasks. Standardising on one means accepting suboptimal performance or cost on some use cases. (2) Single-provider creates concentration risk — if the provider has an outage or changes pricing, all AI systems are affected simultaneously. (3) The AI landscape moves too fast for permanent standardisation — the best provider today may not be the best in 12 months. Recommendation: standardise the interface (an internal API gateway that abstracts the provider), not the provider itself. Define approved provider categories (EU-hosted for PII, frontier API for high-stakes reasoning, efficient API for high-volume tasks), and let use-case requirements determine which category — and therefore which provider — applies. Review the approved list every 6 months as the landscape evolves.
>
> **Architecture Takeaway:** Never let application code call AI provider APIs directly. All AI provider calls should go through an internal model gateway. This single architectural decision enables provider switching, A/B testing, cost routing, and governance controls without application code changes. The gateway is the standardisation point; the provider is a configuration setting.

---

**Question 5 — AI fluency vs AI awareness**

What distinguishes an architect who is "AI-fluent" from one who is merely "AI-aware"?

> **Simple Explanation:** AI-aware knows that hammers exist. AI-fluent knows which type of hammer to use for each type of nail, how long it will take, and what to do when the nail bends. The difference isn't depth of knowledge about one specific tool — it's breadth of judgment across the full toolset.
>
> **Detailed Answer:** AI-aware: can describe what AI can do in general terms; knows the major providers; has used an LLM API. AI-fluent: (1) Can match problem type to the right AI modality — knows when not to use an LLM. (2) Can size cost and latency before building — has the token economics mentally loaded. (3) Understands failure modes — hallucination, drift, prompt injection — and designs mitigations into the architecture. (4) Knows where the boundaries are — what LLMs reliably handle vs where they degrade (complex multi-hop reasoning, arithmetic, strict factual recall). (5) Can read the landscape — track model capability improvements and identify when a capability that wasn't viable 6 months ago is now worth reconsidering. (6) Designs for governance from day one — data residency, model versioning, human-in-the-loop, audit logging. The test: put an unfamiliar business problem in front of them. AI-aware asks "can AI help with this?" AI-fluent says "this part is a structured prediction problem for classical ML, this part is a RAG problem, this part needs a multimodal model for the document intake — here's what each costs and where the risks are."
>
> **Architecture Takeaway:** The path from AI-aware to AI-fluent runs through three skills: (1) problem-to-modality matching (which AI type for which problem), (2) cost estimation before coding (token economics, infrastructure trade-offs), and (3) failure mode design (what happens when it's wrong, how do you detect it, how do you mitigate it). These three skills cover 80% of what architects need in practice.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers frontier model evaluation methodology and AI safety/ethics at depth. It is safe to skip on a first pass and return here later.

### 8.1 The 2026 Frontier Model Lineup

The frontier model comparison changes regularly. Use this framework rather than memorising specific specs (which will be outdated within months):

**Dimensions that matter for selection:**

| Dimension | Why it matters | How to evaluate |
|---|---|---|
| Reasoning benchmark (MMLU, GPQA) | Proxy for complex task performance | Check provider leaderboard + independent LMSYS |
| Context window | Maximum document/conversation length | Check official spec |
| Speed (tokens/sec) | Interactive UX feasibility | Benchmark on your hardware/API |
| Cost (input/output per M tokens) | Operating cost at scale | Check provider pricing page |
| Multimodal support | Image/document intake | Try with your document types |
| Tool use / function calling | Agent workflow capability | Test with your tool schemas |
| Data residency | Compliance | Check provider's available regions |

**The LMSYS Chatbot Arena** (lmarena.ai) provides human preference rankings across models — useful for benchmarking "which model do humans prefer" for your task type. Always supplement with task-specific evaluation.

### 8.2 AI Safety and Ethics in the Landscape

The AI landscape is not just a map of capabilities — it's also a map of risks. Understanding which providers have which safety posture affects procurement decisions:

**Constitutional AI (Anthropic):** Claude models are trained with a values framework that prioritises helpfulness, harmlessness, and honesty. The model is explicitly trained to refuse harmful requests and to be transparent about its limitations.

**RLHF (Reinforcement Learning from Human Feedback — a training process where human raters score model outputs to shape the model toward helpful, harmless behaviour; covered in depth in the Safety & Ethics module) alignment (OpenAI, others):** Models trained with reinforcement learning from human feedback to align with human preferences — more responsive to user instructions, including potentially harmful ones if the instructions are phrased carefully.

**Open-weight models:** Safety alignment quality varies significantly. A model with no RLHF and no safety training will follow almost any instruction. Deploying open-weight models in customer-facing contexts requires your own safety layer (input/output moderation).

For enterprise deployments: closed API models typically have stronger built-in safety alignment; open-weight models give you more control but more responsibility. Neither eliminates the need for your own content moderation layer for customer-facing applications.

---

## 9. Key Takeaways (5 Bullets)

- **The AI landscape has three layers: foundation models, infrastructure, and applications — architects need fluency across all three, not just the API layer.** Understanding which cloud platform, which vector database, and which serving framework connects to which use case requirement is the architecture competency, not just knowing which model to call.

- **Not every AI problem is an LLM problem.** Structured tabular prediction, time series forecasting, and collaborative filtering recommendation are often better solved by classical ML at lower cost with higher accuracy. Defaulting to LLM for every AI use case is a sign of tool-first thinking rather than problem-first thinking.

- **Open-weight vs closed-API is a governance, cost, and operations decision, not a quality decision.** Closed APIs provide frontier quality with zero ops overhead; open-weight provides data control and cost efficiency at scale with significant ops investment. Most mature enterprises use a hybrid approach by workload type and data sensitivity.

- **The 2026 landscape changes every 3–6 months — build on interfaces, not on specific models.** Architecture decisions that lock tightly to a specific model (hardcoded version, no abstraction layer, no evaluation gate) require expensive rework when models are updated or deprecated. Abstract the model behind an interface; pin versions explicitly; treat model changes as deployment events.

- **AI fluency for architects means matching problem type to AI modality, sizing cost before building, and designing for failure modes.** The progression from AI-aware to AI-fluent is measurable: can you tell the difference between a RAG problem and a fine-tuning problem, estimate token costs before writing code, and explain what happens when the model is wrong? These three skills cover 80% of what architects need.
