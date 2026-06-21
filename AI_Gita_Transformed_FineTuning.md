# Fine-tuning — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

> **What is a token?** A token is the basic unit of text that LLMs process — and the unit that APIs charge for. Roughly 3–4 characters or 0.75 words in English. "Hello world" = 2 tokens. 1,000 tokens ≈ 750 words ≈ 1.5 pages. APIs charge separately for **input tokens** (your prompt) and **output tokens** (the model's response). When you see pricing like "$2 per million tokens", that is the cost per million of these text chunks.

Fine-tuning is the process of taking a model that has already learned general language understanding from trillions of tokens, and continuing to train it on a much smaller, domain-specific dataset — so it becomes specialised for your use case.

Think of it as the difference between hiring a university graduate (the base model — broad knowledge, general capability) and running them through a company-specific onboarding programme (fine-tuning — they now know your processes, your terminology, your output format, your risk tolerance).

After fine-tuning, the model:
- Uses your company's terminology and style naturally
- Follows your output format consistently (JSON schema, clause numbering, ticket format)
- Refuses requests outside its specialised scope reliably
- Performs your specific task better than a general-purpose model of the same size

> **What is RAG?** RAG (Retrieval-Augmented Generation) means: instead of relying on the model's built-in training knowledge, you retrieve relevant documents from your own systems at query time and feed them to the model alongside the question. The model answers from *your data*, not from what it memorised during training. Think of it as giving the model a cheat-sheet of relevant pages from your internal wiki before asking it a question.

What fine-tuning **cannot** do:
- Inject knowledge the model has never seen (for knowledge, use RAG)
- Fix reasoning errors in the base model
- Make a small model perform like a large one on complex tasks
- Replace the need for good prompting — the best-fine-tuned model still needs clear instructions

**The honest cost picture:** fine-tuning requires a dataset (hundreds to thousands of examples), GPU time (hours to days), evaluation infrastructure, and ongoing maintenance as the model or requirements evolve. For most enterprise use cases, prompting or RAG solves the problem more cheaply. Fine-tuning is for when they don't.

---

## 2. Why Should I Care

### For Solution Architects

Fine-tuning decisions arise at specific points in a system's evolution:

- **The consistency problem:** your GPT-4o-powered assistant produces correctly structured JSON in 95% of cases but diverges in 5% — causing downstream pipeline failures. Fine-tuning on structured examples can push this to 99.8%.
- **The terminology problem:** your supply chain assistant uses generic logistics vocabulary but your team uses domain-specific terms (SKU codes, fulfilment centre IDs, system names). Fine-tuning teaches the model your vocabulary without rewriting prompts.
- **The cost optimisation problem:** a fine-tuned 7B model can match a GPT-4o response on a narrow task at 1/10th the cost. Once you have sufficient volume, this matters.
- **The latency problem:** a fine-tuned small model generates 3–5× faster than a frontier model for simple classification or extraction tasks.

The risk: fine-tuning creates a **model dependency**. Your fine-tuned model is tied to a specific base model version. When the base model is deprecated or updated, you either retrain or stay on an old model version. This is a real lifecycle management cost that prompting-based solutions avoid.

### For Enterprise Architects

Fine-tuning introduces AI model versioning into your software delivery lifecycle. Unlike a software update, a model update changes system behaviour in probabilistic, non-deterministic ways. Enterprise implications:

- **Governance:** a fine-tuned model is an artifact that requires version control, evaluation records, and deployment approval — the same as any software release
- **Data governance:** the training dataset is an artifact that must be tracked, curated, and potentially defensible under audit (what did you train on? was it licensed? was it PII-scrubbed?)
- **Regression risk:** fine-tuning can improve performance on the target task while degrading performance on adjacent tasks (catastrophic forgetting)
- **Cost model:** fine-tuning is a one-time training cost + ongoing serving cost at the fine-tuned model's compute tier, versus ongoing API cost that scales with usage

For enterprise architects: the governance and lifecycle complexity of fine-tuning is often underestimated at project initiation. Budget for it explicitly.

---

## 3. Think About It Like This (Analogy)

**The Management Consultant Analogy**

Imagine you hire a top management consulting firm to run a specific process for your company — say, quarterly supplier risk reviews.

**Base model = the consultant on their first day.** They're brilliant, broad, highly capable. But they don't know your supplier naming conventions, your risk scoring framework, your escalation thresholds, or your report format. Every time they produce a report, you spend 30 minutes correcting terminology and reformatting the output.

**Prompting = detailed briefing documents.** You write a comprehensive brief: "Use the following format... when you see supplier name X, it refers to... flag any score below 7 as high risk..." This works well. But you repeat this brief in every session, and if the brief is too long, the consultant occasionally forgets parts of it.

**RAG = giving the consultant access to your knowledge base.** You give them a file server of supplier records, previous reports, and policy documents. They look things up as needed. This solves the knowledge problem but not the style/format/behaviour problem.

**Fine-tuning = a two-week onboarding programme.** You have the consultant read 500 past reports. They sit in on 20 real risk review meetings. They practice producing reports in your format and get feedback until they get it right. After onboarding, they know your vocabulary, your format, your risk thresholds — without needing to be briefed every time.

**The trade-off is real:** the onboarding programme takes two weeks and costs money. If you only need 10 reports a year, the prompting approach is more efficient. If you're producing 5,000 reports a year, the onboarding investment pays back quickly.

**LoRA = condensed onboarding notes.** Instead of changing everything the consultant knows (expensive, risky), you give them a small reference card that modifies just the relevant parts of their behaviour. They still have all their general knowledge; the card just adjusts how they apply it in your specific context.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 The Decision Framework: Fine-tuning vs RAG vs Prompting

Before spending engineering time on fine-tuning, work through this decision framework. Most teams reach for fine-tuning too early.

**Step 1: Can prompting solve it?**

Try these in order before considering fine-tuning:

| Technique | What it solves | When it's enough |
|---|---|---|
| Zero-shot prompting | Basic task with clear instructions | General tasks, no edge cases |
| Few-shot prompting (5–20 examples in prompt) | Consistent format, style, classification | When 10–20 examples cover most cases |
| System prompt engineering | Persona, scope, tone, refusal behaviour | Behaviour and constraint problems |
| Chain-of-thought | Complex reasoning, step-by-step tasks | Accuracy problems on hard reasoning |

If you've tried these and the problem persists: the issue is likely one of (a) knowledge gap, (b) format consistency at scale, or (c) a general model being too expensive/slow for the task volume. Only then proceed.

**Step 2: Is it a knowledge problem or a behaviour problem?**

| It's a knowledge problem | It's a behaviour problem |
|---|---|
| The model answers incorrectly because it doesn't have the facts | The model has the capability but doesn't format, style, or scope correctly |
| Correct answer: **RAG** | Correct answer: **Fine-tuning** |
| Example: asks about your internal API schema | Example: formats JSON with wrong field names despite correct facts |
| Example: doesn't know your 2025 product catalogue | Example: uses generic customer service tone instead of your brand voice |

**Fine-tuning cannot inject facts reliably.** A model trained on "the API endpoint is /v2/orders" will memorise this for common patterns but won't reliably retrieve it under varied phrasings. Use RAG for facts. Use fine-tuning for behaviour.

> **Common Misconception:** "We can fine-tune the model with our company data so it knows everything about us." Fine-tuning teaches the model how to behave (format, style, scope, tone) — not what to know. Knowledge injected via fine-tuning is unreliable: the model may have memorised a few common phrasings but will hallucinate or give wrong answers on rarer variations. For company-specific knowledge (product catalogue, policies, procedures, recent events), the correct mechanism is RAG — retrieve the relevant documents at query time and inject them into the context. Fine-tuning + RAG together is the mature pattern: fine-tune for behaviour, RAG for knowledge.

**Step 3: Apply the full decision matrix**

| Signal | Prompting | RAG | Fine-tuning |
|---|---|---|---|
| Need to inject updated/private knowledge | ✅ partial | ✅ | ❌ not reliable |
| Need consistent output format at scale | ✅ partial | ❌ | ✅ |
| Need domain-specific tone/style | ✅ partial | ❌ | ✅ |
| Cost too high at current volume | ❌ | ❌ | ✅ (smaller model) |
| Latency too high at current volume | ❌ | ❌ | ✅ (smaller model) |
| Task is narrow and well-defined | ❌ | ❌ | ✅ |
| Task is broad and general | ✅ | ✅ | ❌ risky |
| Data is fresh / changes frequently | ✅ | ✅ | ❌ requires retraining |
| Need full behaviour change (new task type) | ❌ | ❌ | ✅ |
| Have < 100 high-quality examples | ✅ few-shot | ✅ | ❌ insufficient data |
| Have 500+ high-quality examples | — | — | ✅ ready to fine-tune |

**The combination pattern:** in production, most mature AI systems use all three — a fine-tuned model for task-specific behaviour, RAG for knowledge, and system prompts for context and constraints. They are not mutually exclusive.

### 4.2 The 2026 Post-Training Stack

Modern LLMs are not trained once — they go through a multi-stage post-training pipeline:

```
Pre-training
  (Billions of tokens, general language understanding)
  │
  ▼
Supervised Fine-tuning (SFT)
  (Thousands of examples: prompt → ideal response)
  (Teaches: format, task type, basic instruction following)
  │
  ▼
Preference Optimisation  [optional but common]
  (RLHF / DPO / GRPO — pairs of good/bad responses, human or AI labelled)
  (Teaches: alignment with human preferences, helpfulness, harmlessness)
  │
  ▼
Evaluation Gate  [mandatory — skipping is not optional]
  (Automated metrics + human eval + regression tests)
  │
  ▼
Production Model
```

For most enterprise fine-tuning projects: **SFT only** is the starting point. Preference optimisation is complex, requires preference pairs (not just examples), and is often unnecessary for narrow task fine-tuning. GRPO and RLVR (for reasoning models) are advanced topics for teams building custom reasoning capabilities.

### 4.3 LoRA: What It Is and Why It Dominates

> **Explain Like I'm an Architect**
>
> Fine-tuning a large language model sounds like it should require enormous resources — you're updating 7 billion numbers in a 7B model, or 70 billion in a 70B model. Full fine-tuning actually does require that: loading all those weights, computing gradients, updating every parameter. For a 70B model at full precision, that requires approximately 700 GB of GPU VRAM — the equivalent of 9 H100 GPUs running simultaneously. Very few organisations have this.
>
> LoRA (Low-Rank Adaptation) is the insight that you don't need to update all 70 billion parameters to meaningfully change the model's behaviour. In practice, the changes needed during fine-tuning are low-rank — they happen along a small number of directions in the mathematical space. LoRA exploits this by training only two small matrices (A and B) that together approximate the change, instead of updating the full weight matrix.
>
> **The analogy:** imagine you have a 10,000-page reference manual (the model). Full fine-tuning rewrites the entire manual. LoRA adds a small set of sticky notes (the A and B matrices) that modify how you read specific pages. The full manual is unchanged; the sticky notes redirect your attention and interpretation. You can add or remove the sticky notes without touching the original manual — and the sticky notes are tiny compared to the manual itself.
>
> **The practical result:** a 70B model that requires ~700 GB VRAM for full fine-tuning requires ~35 GB with QLoRA (4-bit quantisation + LoRA). That's one A100 80GB GPU. This is the difference between "requires a cloud cluster" and "requires a single cloud instance."

**The problem with full fine-tuning:**

A standard fine-tuning run updates all model parameters. For a 7B model at FP16, that's 7 billion × 2 bytes = 14GB of weights that must be loaded into GPU VRAM, forward-passed, and then updated via backpropagation. The gradient computation and optimiser states (Adam requires 2 copies of the gradients) add another 3–4× the weight size. Full fine-tuning a 7B model requires ~80GB GPU VRAM — a single H100. Full fine-tuning a 70B model requires ~800GB VRAM — 10× H100s. Prohibitively expensive for most teams.

**LoRA (Low-Rank Adaptation) solves this:**

The key insight: you don't need to change all the model's weights. Most of the meaningful change during fine-tuning happens along a small number of directions in the weight space — LoRA exploits this by training only a compact pair of matrices that approximate those directions. Think of it as editing margin notes in a book rather than rewriting the book.

The key observation: when fine-tuning, the change to each weight matrix (∆W) is low-rank. Instead of updating the full weight matrix W (7B × 7B, conceptually), you can decompose the update into two small matrices A and B:

```
Original weight update:   W + ΔW   (ΔW is a huge matrix)
LoRA approximation:       W + A × B (A and B are tiny matrices)

Where:
  W has shape [d_model × d_model] — e.g., [4096 × 4096] = 16.7M parameters
  A has shape [d_model × r]       — e.g., [4096 × 16] = 65K parameters  (r = "rank", typically 4–64)
  B has shape [r × d_model]       — e.g., [16 × 4096] = 65K parameters

Total LoRA parameters: 130K  vs  16.7M  =  0.8% of original
```

During fine-tuning:
- The original weights W are **frozen** (no gradients, no updates, no memory needed)
- Only the tiny A and B matrices are trained
- After training, the LoRA adapter (A and B matrices) is saved separately — ~0.8% of model size

**QLoRA (Quantised LoRA):** combine 4-bit quantisation of the base model (reducing its memory from 14GB to 3.5GB for 7B) with LoRA adapters. This enables fine-tuning a 7B model on a single 16GB consumer GPU, or a 70B model on 2× 48GB GPUs — hardware that most teams already have access to.

**What LoRA parameters to set:**

| Parameter | What it controls | Typical value |
|---|---|---|
| **rank (r)** | Adapter expressiveness; higher = more parameters = more memory | 8–64 (start with 16) |
| **alpha (α)** | Scaling factor for the adapter's contribution; often set to 2×r | 32 (if r=16) |
| **target modules** | Which weight matrices to adapt | query, key, value, output, feed-forward |
| **dropout** | Regularisation for the adapter | 0.05–0.1 |
| **learning rate** | How fast the adapter learns | 1e-4 to 3e-4 (higher than full fine-tuning) |

**LoRA vs Full Fine-tuning: the practical comparison:**

| Dimension | Full Fine-tuning | LoRA | QLoRA |
|---|---|---|---|
| GPU VRAM (7B model) | ~80 GB | ~30 GB | ~10 GB |
| Trainable parameters | 100% | 0.1–1% | 0.1–1% |
| Training time | Baseline | ~1.5× longer per step | ~2× longer (quant overhead) |
| Quality vs full fine-tune | 100% | 95–99% | 90–97% |
| Hardware requirement | Multiple A100/H100 | 1–2 A100 | Consumer GPU (RTX 4090) |
| When to use | Maximum quality, compute available | Production fine-tuning standard | Limited hardware, cost-sensitive |
| Catastrophic forgetting risk | High | Low (base weights frozen) | Low |

**Catastrophic forgetting** is real for full fine-tuning: the model learns your task but forgets general capabilities. This is why a model full-fine-tuned on customer service queries may struggle to do arithmetic it could previously handle. LoRA largely avoids this because the base weights are frozen.

**The PEFT Landscape Beyond LoRA (2026):**

| Technique | How it differs from LoRA | When to prefer |
|---|---|---|
| **LoRA** | Low-rank decomposition of weight updates | Standard choice for most SFT |
| **LoRA+** | Asymmetric learning rates for A and B matrices | Slightly better convergence |
| **DoRA** | Decomposes into magnitude + direction updates | Better generalisation on some tasks |
| **IA³** | Learns scaling vectors, not matrices; fewer parameters than LoRA | Extremely parameter-efficient; simpler |
| **Prefix tuning** | Adds learnable tokens to the input; no weight changes | When base model cannot be modified |
| **Adapters** | Adds small dense layers between existing layers | Architecture-agnostic; legacy |

For enterprise projects: **LoRA or QLoRA** is the right choice in nearly all cases. The differences between variants are marginal for narrow task fine-tuning.

### 4.4 Dataset Preparation: The Quality Gate

**The most common fine-tuning failure is poor data, not the training technique.**

A fine-tuned model learns to replicate the patterns in your training data. If your training data contains:
- Inconsistent output formats → the model will output inconsistently
- Wrong answers → the model will learn those wrong answers
- Ambiguous instructions → the model will behave ambiguously
- Biased examples → the model will amplify the bias

> **Explain Like I'm an Architect**
>
> "The most common fine-tuning failure is poor data" sounds obvious — but the specific ways data quality fails are worth understanding because they map directly to production failure modes.
>
> **Inconsistent labelling → inconsistent outputs.** If 30% of your training examples use field name "order_id" and 70% use "orderId" in the JSON schema, the model learns both patterns — and produces inconsistent output in production. It's not a model problem; it's a data problem that the model faithfully learned.
>
> **Wrong answers in training data → model learns wrong answers.** A model trained on past customer service agent responses will learn whatever those agents did — including their mistakes. If agents sometimes issued refunds they shouldn't have, the model learns that pattern too. Training data quality is the ceiling on fine-tuned model quality, not just the floor.
>
> **Edge cases absent from training → model fails on edge cases.** A model trained only on straightforward cases will look excellent on benchmarks of straightforward cases and fall apart on the 5% of edge cases that show up in production. Deliberately including edge cases in the training set is the only way to cover them.
>
> **The governance implication:** the training dataset is an artifact that must be curated with the same rigour as production code — reviewed, versioned, tested, and maintained. Treat it as a first-class engineering artifact, not as a one-time data export.

**Dataset size as a starting point:**

| Task type | Minimum viable examples | Production quality |
|---|---|---|
| Format/style consistency | 100–200 | 500–1,000 |
| Domain classification | 200–500 per class | 1,000+ per class |
| Domain-specific generation | 500–1,000 | 2,000–5,000 |
| Instruction following (general domain shift) | 1,000–3,000 | 5,000–10,000 |
| Behaviour alignment (preference optimisation) | 1,000 preference pairs | 5,000–10,000 pairs |

**The data format (SFT):** training data is structured as (prompt, completion) pairs in JSONL format:

```json
{"messages": [
  {"role": "system", "content": "You are a supply chain assistant..."},
  {"role": "user", "content": "Summarise this purchase order."},
  {"role": "assistant", "content": "PO-2024-0891 | Supplier: Flex Ltd | Items: 500 units SKU-4421..."}
]}
```

**Data quality checklist:**

- [ ] Each example demonstrates the exact behaviour you want, not approximate
- [ ] Output format is consistent across all examples (field names, casing, punctuation)
- [ ] Examples cover edge cases, not just easy/typical cases
- [ ] No PII in training data (check with automated scanners)
- [ ] Data is licensed / owned / sourced with appropriate rights
- [ ] Train/validation split is stratified (random split can create imbalanced splits)
- [ ] At least 10% held out as evaluation set that training never sees
- [ ] Examples reviewed by domain experts, not just engineers

**The synthetic data trap:** LLMs can generate training data cheaply — but models trained on synthetic data generated by themselves (or a similar model) risk **model collapse**: the distribution narrows, diversity decreases, and the model becomes confidently wrong on edge cases. Synthetic data is acceptable for augmenting real data (80% real, 20% synthetic), not for replacing it.

### 4.5 Evaluation: How You Know the Model is Better

> **Explain Like I'm an Architect — What these metrics actually mean**
>
> In traditional software you test a function by checking: given input X, does the output exactly equal expected value Y? This works because code is deterministic. LLMs are not deterministic — ask the same question twice and you get two different valid answers. You cannot check for exact equality. You need a scoring system that says *this answer is roughly as good as the reference* rather than *this answer is identical to the reference*.
>
> **Precision:** Of all the times the model said "yes" (or flagged something), how often was it correct? A model that rarely says "yes" can have 100% precision — but may miss many real cases.
>
> **Recall:** Of all the real "yes" cases that exist, how many did the model find? A model that always says "yes" has 100% recall — but is also always wrong.
>
> **F1:** The balanced score between precision and recall. An F1 of 0.90 means the model is both accurate when it says yes *and* catches most of the real cases. For a production classifier (fraud detection, support ticket routing), target F1 above 0.85 before deploying.
>
> **ROUGE / BLEU:** Measure how similar the model's generated text is to a reference answer, by counting word overlaps. A ROUGE score of 0.85 means 85% of the key phrases in the reference appear in the model's output. Used to evaluate summarisation and translation quality. A ROUGE score below 0.70 typically means the model is generating plausible-but-wrong summaries.
>
> **Why this matters architecturally:** These are the metrics your ML engineer will report. If you cannot interpret them, you cannot hold the team accountable for quality thresholds, set acceptance criteria for go-live, or understand when a model regression has occurred in production.

Never deploy a fine-tuned model without an evaluation gate. The gate must include:

**Automated metrics (fast, cheap, run on every training run):**
- Task-specific accuracy (classification: F1, precision, recall; extraction: exact match; generation: ROUGE, BLEU)
- Format compliance rate: does the output match the expected schema 100% of the time?
- Length distribution: is the output length distribution within expected bounds?

**LLM-as-judge (medium cost, catches quality issues automated metrics miss):**
- Use a strong model (GPT-4o or Claude Opus) to score your fine-tuned model's outputs against reference responses
- Score on dimensions relevant to your task: relevance, correctness, format, tone
- Compare fine-tuned model vs baseline model on same evaluation set

**Regression testing (non-negotiable):**
- Test on capabilities you didn't fine-tune for — arithmetic, general Q&A, reasoning tasks
- Catastrophic forgetting in fine-tuning can silently degrade capabilities you depend on but didn't measure

**Human evaluation (expensive, but required before the first production deployment):**
- Domain experts evaluate a sample of outputs (100–200) across the full range of expected inputs
- Use a structured rubric; don't rely on "feels right"
- Record results — they become your baseline for future fine-tuning iterations

---

## 5. Enterprise Example

**Scenario: Fine-tuning for Supply Chain Exception Handling Reports**

A logistics company produces daily exception reports from their supply chain monitoring system. Each report summarises delayed orders, flags root causes, and recommends actions. Currently:
- A GPT-4o-based system generates these reports from raw event data
- Cost: £18,000/month (high volume, complex prompts with 3,000-token context)
- Quality issue: 12% of reports use incorrect supplier terminology, require manual correction
- Latency issue: reports must be ready within 45 seconds of an exception event; GPT-4o averages 38 seconds

**Analysis: Fine-tune or prompt engineer?**

| Problem | Root cause | Right solution |
|---|---|---|
| Incorrect supplier terminology | Behaviour (model doesn't know custom codes) | Fine-tuning |
| Manual correction overhead | Behaviour (inconsistent output format) | Fine-tuning |
| High cost at volume | General model expensive for narrow task | Fine-tune + downsize |
| Near-SLA latency | Large model is slow | Fine-tune a smaller model |

Verdict: Fine-tuning is warranted — behaviour problem + cost + latency all point the same direction.

**Implementation:**

1. **Dataset creation:** extract 1,400 existing (event data, approved report) pairs from the last 6 months. Domain experts review and correct 150 edge case examples. Final: 1,250 training examples, 150 validation.

2. **Model selection:** Llama-3 8B Instruct as the base model. At 8B parameters with QLoRA 4-bit quantisation, it fits on a single A10G GPU for training, and serves at ~200ms/report.

3. **Training:** QLoRA fine-tuning (r=32, α=64, targeting all attention + MLP layers), 3 epochs, learning rate 2e-4 with cosine warmup. Training time: 4 hours on 1× A10G. Training cost: 4 hrs × £0.80/hr = £3.20.

4. **Evaluation results:**
   - Supplier terminology accuracy: 97.8% (vs 88% baseline GPT-4o)
   - Format compliance: 99.4% (vs 92.3%)
   - Report quality (LLM judge, 1–5 scale): 4.1 (vs 4.4 GPT-4o) — acceptable degradation
   - Regression (general reasoning): no significant degradation detected
   - Latency: 180ms average (vs 38,000ms GPT-4o)

5. **Production decision:**
   - Self-host the fine-tuned Llama-3 8B on 2× A10G instances (redundancy): 2 × £0.80/hr × 730 hrs/month = £1,168/month
   - vs GPT-4o: £18,000/month
   - Saving: £16,832/month. Payback on dataset + training time (£8,000 one-time): < 15 days

6. **Maintenance cost (overlooked at initiation):**
   - Quarterly retraining as exception types evolve: ~8 hours × engineer time
   - Evaluation pipeline maintenance: ongoing
   - Model versioning and deployment overhead: 1 day/quarter
   - Llama-3 base model deprecation cycle: ~18 months, requires retraining

**Total annual cost:** £14,016 (serving) + ~£12,000 (ops overhead) = £26,016 vs GPT-4o £216,000/year. Net saving: ~£190,000/year. The ops overhead is real and often forgotten in the initial business case.

---

## 6. Architecture Perspective

### Fine-tuning in the System Lifecycle

Fine-tuning is not a one-time event — it introduces a **model training and evaluation pipeline** into your system. Architects should design for this from day one:

```
Data Pipeline
  (collect examples → curate → label → version)
        │
        ▼
Training Pipeline
  (QLoRA / LoRA → evaluation gate → model registry)
        │
        ▼
Deployment Pipeline
  (canary → A/B test against baseline → full rollout)
        │
        ▼
Monitoring
  (format compliance, output distribution, regression metrics)
        │
        ▼
Trigger: drift detected / new training data available → loop back
```

Each stage has engineering cost. Teams that build only the training step and skip the evaluation gate and monitoring pipeline are building a system that degrades silently in production.

### Preference Optimisation: When You Go Beyond SFT

SFT teaches the model to produce the right output format. It doesn't teach it to prefer *better* outputs over *worse* ones — it just trains it to imitate examples. When you need the model to make quality judgements (prefer a more concise response, prefer more cautious phrasing), preference optimisation adds this.

**Scope note:** This section is relevant if your team moves beyond standard supervised fine-tuning (SFT) — most enterprise fine-tuning projects in year one will use SFT or DPO. Read this section to understand what your ML engineers are referring to, not to implement it yourself.

**The 2026 preference optimisation options:**

| Method | How it works | When to use |
|---|---|---|
| **RLHF** | Human raters rank outputs; reward model trained on rankings; RL optimises the policy toward higher reward | Complex alignment; original ChatGPT approach; expensive |
| **DPO (Direct Preference Optimisation)** | Trains directly on (chosen, rejected) pairs without a separate reward model | Simpler, stable, now standard for preference training |
| **ORPO** | Combines SFT and preference optimisation into a single loss | Single-stage training; efficient |
| **GRPO** | Group Relative Policy Optimisation; reward from comparing multiple outputs from same prompt | Reasoning models (DeepSeek-R1 used this); verifiable rewards |
| **RLVR** | RL with Verifiable Rewards; reward from an external verifier (code executes, math answer is correct) | Code generation, math, any task with ground-truth verification |

For enterprise fine-tuning projects: **DPO** is the practical choice when SFT alone doesn't achieve alignment goals. GRPO and RLVR are relevant only if you're building a reasoning-specialised model (a significant undertaking, not a typical enterprise project).

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — Validate before fine-tuning**

A product manager says the team's customer service chatbot "doesn't sound like us — it's too generic" and requests a fine-tuning project. Is fine-tuning the right solution, and how would you validate this before committing to the project?

> **Simple Explanation:** Before commissioning a fine-tuning project (which requires a dataset, GPU compute, evaluation infrastructure, and ongoing maintenance), spend one day testing whether a better prompt solves the problem. Write a detailed system prompt with brand voice guidelines and 5–10 examples of correct responses. If the chatbot now sounds right: you saved months of work. If it still doesn't: now you have evidence that fine-tuning is warranted — and you've also produced examples that can go into the training dataset.
>
> **Detailed Answer:** Possibly, but first validate through prompting. "Doesn't sound like us" is a tone/style problem — which can often be solved with a well-crafted system prompt and 5–10 few-shot examples of the correct brand voice. First experiment: rewrite the system prompt with explicit brand voice guidelines and add 5 examples of ideal responses; test with 50 representative queries. If 90%+ of outputs now sound correct: prompting solved it. If the problem persists or is inconsistent: fine-tuning is warranted. Fine-tuning is justified when the prompting solution requires a system prompt so long that it consumes significant context budget, or when tone consistency at high volume requires more stability than few-shot prompting provides. Also evaluate: do you have 500+ examples of "this is our voice, not this"? Without training data, fine-tuning cannot proceed. The PM's request may be a dataset creation project before it's a training project.
>
> **Architecture Takeaway:** Always validate "can prompting fix this?" before starting a fine-tuning project. The validation experiment takes one day. The fine-tuning project takes weeks, produces a model artifact that requires versioning and monitoring, and creates a base model lifecycle dependency. If prompting achieves 90%+ of the quality target: use it. Fine-tuning is the right tool for the remaining 10% gap — not the first tool to try.

---

**Question 2 — Hardware feasibility**

Your team wants to fine-tune a Llama-3 70B model but has a budget of 2× A100 80GB GPUs. Is this feasible, and what technique would you recommend?

> **Simple Explanation:** Full fine-tuning of a 70B model is like trying to rewrite a 700-page book on a notepad that only holds 160 pages. It physically doesn't fit. QLoRA is the solution: it's like adding sticky notes to the existing book instead of rewriting it — the sticky notes (LoRA adapters) are tiny, the book itself (quantised to 4-bit) now fits. The result is nearly the same quality at 4× less memory.
>
> **Detailed Answer:** Feasible with the right technique. Full fine-tuning of Llama-3 70B requires ~700GB VRAM (weights + gradients + optimiser states) — far beyond 2× A100 80GB (160GB total). Options: (1) QLoRA — quantise the base model to 4-bit (reduces weights from ~140GB to ~35GB), then apply LoRA adapters. The 4-bit model fits on 1× A100 80GB; LoRA adapter parameters add ~1GB. With 2× A100, you can run larger batch sizes or train more confidently with a redundant setup. This is the practical choice. (2) Consider whether Llama-3 8B suffices for the task — an 8B model fine-tuned for a specific task often matches 70B on that task while being far cheaper to train and serve. Try 8B first; upgrade to 70B only if evaluation shows meaningful quality gap for your specific task. The recommendation: start with QLoRA on Llama-3 8B, evaluate quality, and only escalate to 70B if the quality gap is worth the additional infrastructure cost.
>
> **Architecture Takeaway:** When specifying fine-tuning infrastructure requirements, calculate: (model parameters × bytes per parameter at target quantisation level) + headroom for LoRA adapters + training framework overhead = minimum VRAM. For 70B at INT4: ~35 GB. For 7B at INT4: ~3.5 GB. These calculations belong in the project scoping document before any hardware is provisioned.

---

**Question 3 — Evaluation completeness**

You've fine-tuned a model for a classification task and it achieves 96% accuracy on your evaluation set. Is it ready for production?

> **Simple Explanation:** 96% accuracy is a good start but not a deployment decision. It tells you "this model answers correctly on the types of questions in our evaluation set." It doesn't tell you whether those questions represent what production traffic actually looks like, whether it fails catastrophically on edge cases you didn't think to include, or whether fine-tuning accidentally broke something it could do before. You need all five checks to have a credible "ready for production" claim.
>
> **Detailed Answer:** Not yet — the evaluation is incomplete. 96% accuracy on a held-out evaluation set is necessary but not sufficient. Missing checks: (1) Is the evaluation set representative? If you split randomly from a single time period, you may be measuring in-distribution performance — the model may degrade significantly on examples from a different time period, different customer segment, or edge cases not well-represented in the original data. (2) Regression testing: does the fine-tuned model perform comparably to the base model on tasks you depend on but didn't fine-tune for? Run a regression suite. (3) Error analysis: what is the model getting wrong in the 4%? Are the failures concentrated in a specific category, severity, or edge case type? A model that fails 100% on a specific class (even if it's rare) is a production risk. (4) Production distribution: does your evaluation set reflect the distribution of real production inputs? If production traffic contains longer inputs, noisier inputs, or different topic distributions, lab accuracy may not translate. (5) Latency and serving: 96% on the eval set doesn't test the serving infrastructure. Run a load test before declaring production-ready.
>
> **Architecture Takeaway:** Define the evaluation gate before training begins, not after. The gate should include: minimum accuracy on the held-out test set, passing regression tests on non-fine-tuned capabilities, error analysis showing no catastrophic failures on any subclass, and a load test at expected production throughput. All four must pass before deployment — not just the accuracy number.

---

**Question 4 — Synthetic data risks**

Your data science team proposes generating synthetic training data using GPT-4o to reduce the cost of human labelling. What are the risks and when is this acceptable?

> **Simple Explanation:** Training a model on data generated by another AI model is like a student learning by copying another student's homework. If the other student was right, great. But if they had systematic misconceptions, you've now copied those misconceptions too — and they're harder to detect because everything looks internally consistent. Synthetic data is cheap and fast; real labelled data is slow and expensive and is the only reliable source of ground truth. The right ratio is ~80% real, ~20% synthetic.
>
> **Detailed Answer:** Synthetic data is acceptable as a supplement, not a replacement. The key risk is model collapse: if you train exclusively on data generated by GPT-4o, the fine-tuned model learns to imitate GPT-4o's distribution. When GPT-4o makes systematic errors (and it does — over-explanation, hedging, specific factual patterns), your model learns those errors too. More subtly, the diversity of the training distribution narrows — GPT-4o generates plausible-seeming examples but misses the long tail of real-world inputs. This causes overconfident failure on edge cases. When synthetic data IS acceptable: (1) 20–30% of the training set, mixed with real examples — diversity is preserved while reducing labelling cost. (2) For augmenting underrepresented classes — if you have few real examples of a specific failure mode, synthetic examples can supplement. (3) For data augmentation via paraphrase — same example rephrased multiple ways. When it's NOT acceptable: replacing human-labelled examples entirely; generating data for tasks requiring ground-truth correctness (legal, medical, financial — GPT-4o can hallucinate ground truth); tasks where the model's errors are hard to detect without domain expertise reviewing each example.
>
> **Architecture Takeaway:** Establish a synthetic data policy before the project starts: what percentage of training data can be synthetic, what tasks are excluded from synthetic generation (regulated domains, ground-truth-critical tasks), and what human review process applies to synthetic examples before they enter the training set. Document this in the data governance record for the training dataset.

---

**Question 5 — Drift and retraining architecture**

A fine-tuned model that performed excellently in month 1 has gradually degraded to 82% accuracy by month 4. What is happening and what does the architecture need?

> **Simple Explanation:** The model was trained on data from a specific point in time. The world moved on — new products, new policies, new customer language. The model didn't. Three months of silent drift is a monitoring gap: this should have been caught in week 2, not month 4. A quality dashboard with a weekly accuracy metric would have surfaced the degradation early enough to retrain before it affected users.
>
> **Detailed Answer:** This is likely data drift — the production distribution has changed relative to the training distribution. Common causes in enterprise contexts: new products added (new terminology, new SKU patterns), policy changes (new refusal categories, new output formats), seasonal patterns (different query types at different times of year), user behaviour evolution (different phrasings as users learn the system). The architecture is missing: (1) Monitoring: a continuous metric pipeline comparing recent production outputs against expected quality indicators — this should have surfaced the degradation early, not after 3 months of silent decline. (2) Drift detection: automated comparison of the input distribution (embedding drift, token distribution shift) between training time and current time. (3) Retraining trigger: a defined threshold that initiates a retraining cycle when drift exceeds a threshold. (4) Data collection pipeline: a mechanism for capturing production inputs and human-corrected outputs to build the next training set — without this, retraining requires starting from scratch each time. The fix: retrain with a dataset that includes recent production examples (especially from the period where quality degraded). The process fix: build the monitoring and data collection infrastructure before deploying a fine-tuned model, not after the degradation is noticed.
>
> **Architecture Takeaway:** Fine-tuned model deployment is not a one-time event — it's the start of a continuous lifecycle: deploy → monitor → detect drift → retrain → evaluate → deploy. The monitoring and data collection pipeline must be built before or alongside the model deployment, not retrofitted after the first degradation incident. Budget for two things at project initiation: the fine-tuning project itself, and the operational infrastructure (monitoring, data collection, retraining pipeline) that keeps it working.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers LoRA mathematics and advanced alignment methods (GRPO/RLVR). It is safe to skip on a first pass; return here when your team is ready to implement fine-tuning rather than just commission it.

### 8.1 The Complete LoRA Math

LoRA modifies the forward pass of a weight matrix W:

```
Standard forward: h = Wx
LoRA forward:     h = Wx + (BA)x × (α/r)

Where:
  W ∈ R^{d × k}   — frozen pre-trained weights
  B ∈ R^{d × r}   — initialised to zeros (so adapter starts at identity)
  A ∈ R^{r × k}   — initialised with Gaussian noise
  r               — rank (hyperparameter, << d and k)
  α               — scaling factor (hyperparameter)
```

B is initialised to zero so that at the start of training, the LoRA term is zero — the model begins training from exactly the pre-trained weights. This is important for training stability.

The scaling factor α/r normalises the adapter's contribution to be independent of the rank chosen. Setting α = 2r is common practice.

**Why does low-rank work?** The empirical finding is that the meaningful weight updates during fine-tuning are intrinsically low-dimensional — the high-dimensional weight matrices change along only a few principal directions. LoRA exploits this: even though W is enormous, ∆W = BA can be well-approximated with a small r.

### 8.2 GRPO and RLVR: Reasoning Model Training

**GRPO (Group Relative Policy Optimisation)** is the training technique behind DeepSeek-R1 and the wave of open-source reasoning models. Key insight: instead of training a separate reward model (complex, expensive), generate N responses to the same prompt from the model, then score all N and use the relative rankings as the reward signal.

```
For a math problem P:
  1. Sample N=8 responses from the current policy model
  2. Score each response (0 or 1: correct/incorrect answer)
  3. Compute group-relative advantage: A_i = (score_i - mean_score) / std_score
  4. Update the policy to increase probability of responses with positive advantage
  5. KL penalty: keep the policy from drifting too far from the reference model
```

**RLVR (RL with Verifiable Rewards)** is the broader category: instead of human ratings (slow, expensive, subjective), use a verifier — a function that checks if the answer is correct. For maths: check if the final numerical answer matches. For code: run the code and check if tests pass. For structured output: validate against a schema.

**Why this matters for enterprise:** RLVR-style training can be applied to any task with verifiable outputs. Code generation with passing tests as the reward signal. Supply chain exception classification where the reward is whether the recommended action was correct. Legal clause extraction where the reward is F1 against expert annotations. The technique is accessible (no human reward model required) if you have a reliable verifier.

### 8.3 Hyperparameter Reference

| Hyperparameter | What it controls | Typical range |
|---|---|---|
| Learning rate | Step size during optimisation | 1e-5 to 3e-4 |
| LR schedule | How LR changes during training | Cosine with warmup (standard) |
| Warmup steps | Steps before LR reaches peak | 5–10% of total steps |
| Batch size | Samples per gradient update | 4–32 (effective, via gradient accumulation) |
| Gradient accumulation | Steps before actual weight update | 4–16 (to simulate larger batch) |
| Epochs | Full passes through training data | 1–5 (overfitting risk beyond 3) |
| Max sequence length | Token limit per training example | Match your expected production context |
| Weight decay | L2 regularisation | 0.01–0.1 |
| Gradient clipping | Prevents gradient explosion | 0.3–1.0 (clip by norm) |

**Early stopping:** monitor validation loss at the end of each epoch. If validation loss increases while training loss continues to decrease: the model is overfitting — stop training. This is the most common cause of a model that performs well on your eval set but poorly in production (the eval set was too similar to training).

---

## 9. Key Takeaways (5 Bullets)

- **Fine-tuning solves behaviour problems, not knowledge problems — use RAG for the latter.** If the model gives wrong answers because it lacks facts, fine-tuning won't reliably fix it; RAG will. Fine-tuning is the right tool when the model has the underlying capability but doesn't apply it consistently in the right format, style, or scope for your domain.

- **Try prompting first, then RAG, then fine-tuning — in that order.** Most teams reach for fine-tuning too early. A well-engineered system prompt with 5–10 few-shot examples solves the majority of style and format consistency problems without the training data investment or maintenance overhead. Fine-tuning is warranted when prompting is exhausted or the cost/latency math demands a smaller model.

- **LoRA / QLoRA is the practical standard — full fine-tuning is rarely necessary.** QLoRA reduces GPU VRAM requirements by 4–8×, making fine-tuning of 7B–70B models accessible on modest hardware, with 1–10% quality degradation on most tasks. The base model weights remain frozen, avoiding catastrophic forgetting of general capabilities.

- **Data quality determines fine-tuning quality — 500 excellent examples outperform 5,000 mediocre ones.** The model learns to replicate the patterns in your training data exactly. Inconsistent labelling, format drift, or wrong answers in the training set are directly learned. Invest in data curation, domain expert review, and a rigorous evaluation gate before training.

- **Fine-tuning creates a model lifecycle that must be managed.** A fine-tuned model requires versioning, regression testing on every update, drift monitoring in production, and periodic retraining as data distribution evolves. These operational costs are real and often underestimated at project initiation — budget for them explicitly before committing to fine-tuning over a managed API.
