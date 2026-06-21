# AI Infrastructure — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

AI infrastructure is the hardware, software, and serving stack that makes AI models run — fast enough, cheaply enough, and reliably enough to be useful in production.

Most architects never need to train a large model. But every architect deploying an AI system makes infrastructure decisions that directly affect cost, latency, and reliability:

- **Which model to use** — a 7B parameter open-weight model self-hosted on your GPU, a 70B model via API, or a frontier model like GPT-4o at a premium price point
- **How to serve it** — serverless API calls (pay per token), a dedicated endpoint (fixed cost), or self-hosted inference (capital cost + ops burden)
- **How to optimise it** — quantisation (run a smaller, cheaper version with minimal quality loss), caching (avoid recomputing what you've already computed), batching (process multiple requests together for efficiency)
- **How to scale it** — when traffic spikes, what happens? How does cost scale with volume? What's the latency at P95 under load?

Understanding AI infrastructure gives you the vocabulary and the mental models to have these conversations credibly — with engineering teams, cloud vendors, and finance stakeholders — without needing to have built a GPU cluster yourself.

---

## 2. Why Should I Care

### For Solution Architects

Infrastructure decisions are cost decisions. The difference between a poorly chosen infrastructure setup and a well-optimised one can be 5–10× on the monthly AI bill at scale.

Concrete examples of infrastructure decisions that architects own:

- **Self-hosted vs API:** a 7B model self-hosted on a single A10G GPU (£0.60/hr) can handle ~100 requests/minute at £0.001/request. The equivalent via GPT-4o API is £0.003–0.006/request — 3–6× more expensive, but zero ops burden, no GPU procurement, and automatic scaling.
- **Quantisation trade-off:** a 70B model at FP16 precision requires ~140GB GPU memory (2× H100s). The same model quantised to 4-bit requires ~35GB (one H100). 75% memory reduction, 5–10% quality degradation. For many use cases, the quality loss is invisible; the cost saving is decisive.
- **Caching:** if 15% of your API requests have identical system prompts, prompt caching saves 50–80% on those requests' input token costs. At 1M requests/day, this compounds quickly.

### For Enterprise Architects

AI infrastructure introduces a new cost model to enterprise IT. Traditional software infrastructure costs are fixed or scale with compute (CPU/memory). AI inference costs scale with **tokens** — the amount of text processed. This is a fundamentally different cost structure:

- A 5-word query costs a fraction of a 5,000-word document analysis
- Output length is variable and model-determined — not fixed like a database row
- A model swap (GPT-4o → GPT-4o-mini) can cut costs 10× with no infrastructure change
- Context window length is the primary cost driver for long-document use cases — not the number of requests

Enterprise architects need to understand token economics to forecast AI costs accurately, build governance controls around them, and evaluate build-vs-buy decisions for AI serving infrastructure.

---

## 3. Think About It Like This (Analogy)

**The Delivery Fleet Analogy**

Imagine you're running a delivery operation. You need to get packages from warehouse to customers.

**The GPU is your fleet.** A high-end H100 GPU is like a fleet of 100 vans — enormous capacity, very fast, very expensive. An A10G is like 20 vans — still capable, much cheaper. A CPU trying to do inference is like a bicycle — technically possible, but not viable at any meaningful scale.

**Quantisation is like load optimisation.** Your vans can carry packages in custom foam packaging (full precision, FP16) — safe, but each van carries fewer packages. Or you can standardise packaging (quantise to INT4/FP4) — slightly less protection, but you fit 4× as many packages per van. The packages arrive in essentially the same condition; you've just dramatically increased fleet utilisation.

**Batching is filling the van before it leaves.** Sending one package per van trip is wasteful. If you wait 50ms to collect 10 requests and process them together, each GPU computation amortises across 10 requests. Throughput goes up; cost per request goes down.

**KV cache is your local depot.** When a van makes a repeat delivery to the same neighbourhood (same prompt prefix), it's wasteful to drive from the central warehouse every time. The local depot (KV cache) stores the work already done for that neighbourhood — the van starts from there, not from scratch.

**Speculative decoding is the fast courier service.** You have a small motorbike (small draft model) that guesses the next few deliveries and races ahead, and a big van (the main model) that quickly verifies and approves the guesses. When the guesses are right (they usually are), you've delivered 4 packages in the time it would take the van to deliver 1.

**Serverless API vs self-hosted** is the classic make-vs-buy decision: use a courier service (API) for variable demand — pay per package, no fleet management — or run your own fleet (self-hosted) for predictable high volume — higher fixed cost, lower per-package cost at scale.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 GPU Memory: Why It's the Primary Constraint

Everything about LLM inference — which models you can run, at what speed, at what cost — is constrained by **GPU memory (VRAM)**.

The model weights must fit entirely in GPU VRAM before any inference can happen. If the model doesn't fit, it either can't run or runs with severe performance penalties (offloading to CPU memory, which is 10–50× slower for this workload).

> **Explain Like I'm an Architect**
>
> GPU VRAM is the single most important number in self-hosted AI infrastructure. Think of it as the RAM of a specialist computer that does AI — and unlike your laptop's RAM, you cannot exceed it. If the model doesn't fit, it simply cannot run.
>
> "Parameters" is the measure of model size — a 7B model has 7 billion numbers (weights) that must all be loaded before the model can process a single word. Each number takes a certain amount of storage depending on its precision: a 16-bit float (FP16) takes 2 bytes, a 4-bit integer (INT4) takes 0.5 bytes.
>
> The arithmetic is straightforward: 7 billion parameters × 2 bytes each = 14 GB of VRAM just to load the model. Nothing else, no requests being served yet — just loading. If your GPU has 16 GB, you have 2 GB left for everything else (which is not enough). If it has 24 GB, you have 10 GB breathing room.
>
> This is why "quantisation" (explained in §4.2) is so consequential: reducing from FP16 (2 bytes) to INT4 (0.5 bytes) shrinks a 70B model from 140 GB down to 35 GB — the difference between needing 4 very expensive H100 GPUs and needing 1.

**Memory required to load a model:**

```
Memory (bytes) = Parameters × Bytes per parameter

FP32 (full precision):     7B model  = 7B × 4 bytes  = 28 GB
FP16 / BF16 (half):        7B model  = 7B × 2 bytes  = 14 GB
INT8 (8-bit quantised):    7B model  = 7B × 1 byte   =  7 GB
INT4 / FP4 (4-bit):        7B model  = 7B × 0.5 byte =  3.5 GB

FP16:                      70B model = 70B × 2 bytes = 140 GB
INT4:                      70B model = 70B × 0.5 byte = 35 GB
```

**Common GPU VRAM capacities:**

| GPU | VRAM | Fits at FP16 | Fits at INT4 | Typical cost |
|---|---|---|---|---|
| RTX 4090 (consumer) | 24 GB | 13B models | 48B models | £0.40/hr (cloud) |
| A10G | 24 GB | 13B models | 48B models | £0.80/hr |
| A100 40GB | 40 GB | 20B models | 80B models | £2.50/hr |
| A100 80GB | 80 GB | 40B models | 160B models | £3.50/hr |
| H100 80GB | 80 GB | 40B models | 160B models | £5.00/hr |
| H100 NVLink (2×) | 160 GB | 80B models | 320B models | £10.00/hr |

**The KV cache is additional memory on top of model weights.** When generating a response, the model caches the key-value pairs from the attention computation for all processed tokens — this avoids recomputing them on every generation step. The KV cache grows with sequence length:

In plain terms: longer inputs, more layers, and larger batches all multiply together to determine how much GPU memory the KV cache consumes. The formula below makes this precise — but the key insight is that context length is the most controllable lever architects have.

```
KV cache memory = 2 × num_layers × num_heads × head_dim × seq_length × batch_size × bytes_per_value

For Llama-3 70B at FP16, 4K sequence, batch size 1:
≈ 2 × 80 × 8 × 128 × 4096 × 1 × 2 bytes ≈ 1.3 GB
```

At 128K context length, the KV cache for a single request approaches 40GB on some models — exceeding the model weights themselves. This is why long-context serving is memory-constrained, not compute-constrained.

**The memory bandwidth bottleneck:**

LLM inference (at typical batch sizes) is **memory-bandwidth bound**, not compute bound. The GPU spends most of its time moving data between VRAM and the compute cores — not doing arithmetic. This is why:

- A GPU with 2TB/s memory bandwidth generates tokens faster than a GPU with 1TB/s bandwidth, even at the same FLOP count
- Smaller models often serve faster than larger ones even when the larger model "fits" — less data to move per token
- Quantisation helps not just by fitting the model in less memory, but by reducing the data moved per operation

### 4.2 Quantisation: The Practical Decision Guide

**Quantisation** reduces the numerical precision of model weights — from 16-bit floats (FP16) to 8-bit integers (INT8) or 4-bit integers (INT4/FP4). The model becomes smaller and faster; there is some quality degradation, which varies by model and task.

> **Explain Like I'm an Architect**
>
> Numbers can be stored at different levels of precision. A 32-bit float stores a number with very high precision — 7–9 significant decimal digits. A 16-bit float (FP16) stores it with lower precision — about 3–4 significant digits. A 4-bit integer stores it as one of only 16 discrete values.
>
> When we say "quantise a model," we're reducing the precision of the 7 billion (or 70 billion) numbers stored in the model's weights. Like rounding £1.23456789 to £1.23 — you lose some decimal places, but for most purposes, the rounded number is just as useful. The question is: at what precision does the rounding error become noticeable in the model's outputs?
>
> For most conversational and instruction-following tasks: at 4-bit precision, the quality difference is essentially invisible — most users cannot tell whether they're talking to a 16-bit or 4-bit version of the same model. For complex reasoning, code generation, and tasks requiring precise numeric calculations: the quality difference becomes noticeable at 4-bit.
>
> **The practical implication:** moving from FP16 to 4-bit for a self-hosted model cuts your GPU memory requirement by 4×. A model that needed 2 H100s now fits on 1. For most enterprise use cases, this is a free lunch. Always test your specific use case before committing — but don't assume you need full precision.

**The 2026 quantisation menu:**

| Format | Bits | Memory saving vs FP16 | Quality impact | Best for |
|---|---|---|---|---|
| **FP16 / BF16** | 16 | Baseline | None (full quality) | Training, high-precision inference |
| **GPTQ** | 4 | 4× | 1–3% on benchmarks | Self-hosted open-weight models |
| **AWQ** (Activation-aware) | 4 | 4× | < 1% on benchmarks | Self-hosted, quality-sensitive |
| **NF4** (QLoRA) | 4 | 4× | Minimal for fine-tuning | Fine-tuning large models on limited GPU |
| **FP8** | 8 | 2× | < 0.5% | H100/H200 inference, best quality/size ratio |
| **FP4** | 4 | 4× | 1–2% | Bleeding edge; H200 and Blackwell GPUs |
| **GGUF** (llama.cpp) | 2–8 (mixed) | 2–8× | Variable by bit depth | Local / edge inference, CPU-compatible |

**The practical decision matrix:**

| Scenario | Recommended quantisation |
|---|---|
| Cloud API (GPT-4o, Claude) | Irrelevant — provider handles this |
| Self-hosted, quality-critical (legal, medical) | FP16 or AWQ 4-bit |
| Self-hosted, cost-optimised, quality tolerance | GPTQ 4-bit or AWQ 4-bit |
| Edge / local inference (laptop, on-prem constrained) | GGUF Q4_K_M or Q5_K_M |
| Fine-tuning a large model on limited GPU | NF4 (QLoRA) |
| H100 production serving | FP8 (best perf/quality tradeoff for this hardware) |

**What architects should know:**
- Going from FP16 to 4-bit for a 7B model: 14GB → 3.5GB, enabling it to run on a single 4090 or A10G
- Quality degradation at 4-bit is typically imperceptible for instruction-following and conversation tasks; noticeable for complex reasoning and code generation
- Always evaluate quantised models on your specific task before deploying — benchmark numbers are averages that may not represent your use case

### 4.3 The Production Inference Stack

The inference stack is the software layer that takes model weights and serves them as an API endpoint. In 2026, the production standard is:

**vLLM** (open-source, most widely deployed)
Key innovations:
- **PagedAttention:** manages the KV cache like virtual memory in an OS — allocates KV cache in non-contiguous blocks ("pages"), eliminating fragmentation. Enables serving 2–4× more concurrent requests on the same GPU vs naïve KV cache management.
- **Continuous batching:** instead of processing a batch as a unit (waiting for the slowest request), processes tokens continuously — new requests join the batch as soon as a slot is free. Dramatically improves GPU utilisation under variable load.
- **Prefix caching:** caches KV states for common prompt prefixes — if 80% of your requests share the same system prompt, that prefix is computed once and reused, cutting input processing time for those requests.

**SGLang** (strong alternative for structured output and complex workflows)
Optimised for:
- Structured generation (JSON, constrained output) — runtime constraint enforcement during generation
- Multi-call programs (where the same model is called multiple times in a workflow) — state is shared across calls rather than re-initialised
- Speculative decoding with RadixAttention (their equivalent of PagedAttention)

**TGI (Text Generation Inference, Hugging Face)**
Good for: straightforward deployment of HuggingFace models; solid observability; simpler configuration than vLLM for standard use cases.

**The 2026 production serving stack:**

```
Load Balancer (nginx / cloud LB)
    │
    ▼
vLLM / SGLang Inference Servers
  (multiple instances for horizontal scale)
    │
    ├── Continuous batching
    ├── PagedAttention KV cache
    ├── Prefix caching
    ├── FP8 / INT4 quantised weights
    └── OTel instrumentation
    │
    ▼
GPU Fleet (H100s / A100s / A10Gs)
    │
    ▼
Metrics → Prometheus / Grafana
Traces → OTel collector
```

### 4.4 Speculative Decoding: Faster Generation for Free

LLM generation is slow because it's **autoregressive** — each token is generated one at a time, requiring a full forward pass of the model. A 70B model producing a 200-token response makes 200 sequential forward passes.

**Speculative decoding** breaks this bottleneck:

> **Explain Like I'm an Architect**
>
> The fundamental problem is that LLMs generate one token at a time. To produce a 200-word response, the model makes ~250 sequential "what comes next?" predictions. You cannot skip ahead or parallelize — each prediction depends on the previous one.
>
> Speculative decoding is a clever workaround: deploy a small, fast "guesser" model alongside the large, slow "verifier" model. The guesser predicts the next 5 tokens almost instantly (it's small and cheap). The verifier, in a single pass, checks whether all 5 guesses are correct. Because the verifier is checking, not generating, it can process all 5 in parallel.
>
> When the guesser is right (which it usually is for common phrases, standard boilerplate, predictable completions), you've produced 5 tokens in roughly the time it would take the verifier to produce 1. 5× throughput, same quality.
>
> **What this means architecturally:** speculative decoding is a serving-level optimization — it happens inside vLLM or SGLang, not in your application code. If you're using a cloud API, the provider may already apply it. If you're self-hosting, this is a configuration flag worth enabling. It delivers the most benefit for structured outputs (code, JSON, template-like text) where the guesser's predictions are highly accurate.

1. A small **draft model** (e.g., 7B) generates K tokens speculatively (very fast — it's small)
2. The large **target model** (e.g., 70B) verifies all K tokens in a single forward pass (parallel, not sequential)
3. If the draft's tokens match what the target model would have generated: accept all K tokens — you've generated K tokens in the time of 1 large model pass
4. If the draft diverges at token j: accept tokens 1…j-1, reject j and everything after, regenerate from j with the target model

**The gain:** in practice, draft models get 3–5 tokens right before diverging. This means 3–5× throughput improvement with zero quality degradation (the target model controls the final distribution; wrong drafts are rejected).

**Requirements:** the draft model must use the same tokeniser as the target model and output compatible token distributions. Many model providers now publish dedicated draft models (e.g., Meta's Llama-3 8B as draft for Llama-3 70B).

**When it helps:** speculative decoding helps most when output is predictable — common phrases, structured formats, code with boilerplate. It helps less when output is highly creative or diverse (the draft is wrong more often, rejection overhead increases).

### 4.5 Disaggregated Prefill / Decode (P/D Split)

> **Advanced serving topology** — This section is relevant if you are planning infrastructure at 100+ GPU scale or overseeing a platform engineering team building an inference cluster. For most enterprise AI deployments using managed API services, this is background context rather than an immediate design decision. Safe to skim on a first pass.

LLM serving has two computationally distinct phases:

**Prefill:** processing the input prompt. Compute-intensive — all input tokens are processed in parallel. A 4,000-token input prompt is processed in one shot. This phase is **compute-bound** (arithmetic-heavy).

**Decode:** generating output tokens one at a time. Memory-bandwidth intensive — each generation step loads the full model weights and KV cache. This phase is **memory-bandwidth bound**.

These phases have completely different hardware requirements. On a single GPU, they compete for the same resources.

**Disaggregated serving** runs prefill and decode on separate GPU pools:

```
Request with long prompt (4K tokens)
    │
    ▼
Prefill Pool (compute-optimised GPUs — e.g., H100 SXM)
  → Process input prompt in parallel
  → Generate initial KV cache
  → Transfer KV cache to decode pool
    │
    ▼
Decode Pool (memory-bandwidth-optimised GPUs — e.g., H100 NVL)
  → Generate output tokens autoregressively
  → Using transferred KV cache
```

**Benefits:**
- Each pool can be independently scaled and optimised
- Prefill spikes (sudden large batch of long prompts) don't slow down decode for existing requests
- Hardware can be selected for the specific bottleneck of each phase

**When it matters:** disaggregated serving matters for large-scale deployments (100+ GPUs) or for use cases with highly variable input length (some requests with 100-token inputs, others with 100K-token inputs). For smaller deployments, the engineering complexity is not justified.

### 4.6 Cost Model: Self-Hosted vs API

The make-vs-buy decision for AI inference is one of the most consequential infrastructure decisions an architect makes. Here is the framework:

**API pricing (pay-per-token):**
- No fixed cost
- Scales to zero at zero usage
- No GPU procurement, no ops burden
- Cost scales linearly with usage
- Subject to provider pricing changes and availability

**Self-hosted (fixed + variable):**
- Fixed cost: GPU reservation (£0.60–£5.00/GPU/hr depending on type)
- Variable cost: electricity, networking (usually minor)
- Requires MLOps team to operate
- Fully predictable once utilisation is understood

**Break-even analysis:**

```
Self-hosted break-even daily requests:

GPU cost:     1× A10G at £0.80/hr = £19.20/day
Serves:       ~100 req/min for a 7B model = 144,000 req/day max
At 60% util: 86,400 req/day

API equivalent (GPT-4o-mini at £0.0003/req):
  86,400 × £0.0003 = £25.92/day

Break-even: ~74,000 req/day
Below 74K req/day → API cheaper (no ops overhead)
Above 74K req/day → self-hosted cheaper
```

**The hidden costs of self-hosted:**
- MLOps engineering team (typically 1–2 FTEs)
- GPU procurement lead time (weeks to months)
- Model update and maintenance overhead
- Redundancy and availability infrastructure
- Security and compliance for self-hosted model endpoints

**The hidden costs of API:**
- Vendor lock-in risk (pricing changes, model deprecation)
- Data residency constraints (prompts leave your network)
- Latency variability (shared infrastructure)
- Rate limits that constrain burst capacity

**Decision framework:**

| Signal | Self-hosted | API |
|---|---|---|
| Volume > 1M requests/day | ✅ | ❌ too expensive |
| Data cannot leave your network | ✅ | ❌ |
| Team has GPU ops capability | ✅ | — |
| Variable/unpredictable demand | — | ✅ |
| Need latest frontier model | ❌ | ✅ |
| Startup / no ops team | — | ✅ |
| Regulatory: model lineage required | ✅ | Partial |

---

## 5. Enterprise Example

**Scenario: Infrastructure Design for a Retail Customer Intelligence Platform**

Your retail company wants to run three AI workloads:
1. **Real-time product Q&A** — 200K queries/day, average 800 input tokens, 150 output tokens, SLA: 2-second P95
2. **Nightly contract analysis** — 500 contracts/day, average 40K input tokens, 2K output tokens, no SLA constraint
3. **Internal knowledge assistant** — 50K queries/day, average 1K input tokens, 300 output tokens, SLA: 3-second P95

**Workload analysis:**

| Workload | Daily tokens | Pattern | Cost driver |
|---|---|---|---|
| Product Q&A | 200K × 950 = 190M | Real-time, bursty | Latency + throughput |
| Contract analysis | 500 × 42K = 21M | Batch, overnight | Input cost (long context) |
| Knowledge assistant | 50K × 1.3K = 65M | Real-time, steady | Cost efficiency |

**Infrastructure decisions:**

**Product Q&A:**
- Model: GPT-4o-mini via API (fast, cheap, adequate quality for product Q&A)
- Serving: serverless API — demand is bursty (peaks at lunch and evening); self-hosting would require over-provisioning for peak
- Optimisations: semantic caching (15% cache hit rate estimated → 15% cost reduction); prompt caching for static system prompt (saves ~200 tokens per request)
- Cost: 190M tokens/day × £0.00015/1K tokens = £28.50/day ≈ £855/month
- With caching: ~£730/month

**Contract analysis:**
- Model: Claude Opus via API (best long-context performance for legal reasoning)
- Pattern: batch job, 2am–4am window, no SLA
- Serving: API with async batch endpoint (50% discount on batch pricing at Anthropic)
- Key concern: 40K input tokens per contract × £0.015/1K = £0.60 input cost per contract. 500 contracts = £300/day input cost alone.
- Optimisation: contextual retrieval — pre-process contracts to extract structured clause summaries, reducing average input from 40K to 8K tokens
- Cost before: £300/day. After: £60/day. Saving: 80% on the most expensive workload.

**Knowledge assistant:**
- Model: open-weight Llama-3 70B (quantised AWQ 4-bit, 2× A100 80GB)
- Reason: 50K queries/day at steady load, data sensitivity (internal employee queries should not leave company network), cost break-even analysis favours self-hosted at this volume
- Serving: vLLM with continuous batching and prefix caching
- GPU config: 2× A100 80GB per node (model fits at INT4 with room for KV cache), 2 nodes (4 GPUs total) for redundancy and headroom
- Cost: 4× A100 80GB at £3.50/hr = £14/hr = £336/day
- API equivalent: 65M tokens/day at £0.003/1K = £195/day
- Decision: API is cheaper. Switch to self-hosted only if volume doubles or data residency requirements change.

**Total monthly AI infrastructure cost:**
| Workload | Monthly cost |
|---|---|
| Product Q&A (API, with caching) | £730 |
| Contract analysis (API, batch, optimised) | £1,800 |
| Knowledge assistant (API, pending volume growth) | £5,850 |
| **Total** | **£8,380/month** |

Before the infrastructure analysis and optimisations (no caching, no contextual retrieval, no batch pricing): estimated £31,000/month. The infrastructure decisions reduced the cost by 73%.

---

## 6. Architecture Perspective

### The Infrastructure Decision Stack

Every AI system requires decisions at four levels:

```
Level 1 — Model selection
  Which model fits the quality/cost/latency envelope?
  (Frontier API vs mid-tier API vs self-hosted open-weight)

Level 2 — Serving strategy
  API (serverless) vs dedicated endpoint vs self-hosted?
  (Demand pattern, data residency, ops capability)

Level 3 — Optimisation
  Which efficiency techniques apply?
  (Quantisation, caching, batching, speculative decoding)

Level 4 — Scaling
  How does cost and latency behave as volume grows?
  (Linear scaling? Break-even thresholds? Spot vs reserved?)
```

Make all four decisions explicitly at design time. The default (always use the frontier API, no optimisations) is almost never the right answer for production systems.

### The 2026 GPU Landscape for Architects

You don't need to know GPU specifications to make infrastructure decisions. You need to know the decision-relevant categories:

| Category | GPUs | When to choose |
|---|---|---|
| **Consumer / edge** | RTX 4090, RTX 5090 | Local dev, small models, cost experiments |
| **Cloud mid-tier** | A10G, L4 | Self-hosted models up to 13B (INT4: up to 48B), balanced cost |
| **Cloud high-end** | A100 40/80GB | Models up to 40B (FP16), multi-tenant serving |
| **Frontier serving** | H100, H200 | Large model serving, FP8 support, best performance/watt |
| **Next generation** | Blackwell B200 | 2025-2026 deployments, FP4 support, 2× H100 performance |

For most enterprise deployments: choose A10G or L4 for cost efficiency with open-weight models; H100 for frontier model hosting or high-throughput serving. The GPU choice is largely determined by which cloud provider you're on and which models you need to run.

### Distributed Training (For Architects Who Oversee Fine-Tuning Projects)

Most architects don't train models — but you may oversee a team that does fine-tuning. Three strategies at a glance:

**Data Parallelism (DDP):** copy the full model to N GPUs; each GPU processes a different batch; gradients are synchronised across GPUs. Straightforward, works when the model fits on one GPU. Most fine-tuning uses this.

**Tensor Parallelism (TP):** split individual weight matrices across N GPUs; each GPU holds a slice of every layer. Required when the model is too large for one GPU. High communication overhead.

**Pipeline Parallelism (PP):** split model layers across N GPUs; GPU 1 runs layers 1–20, GPU 2 runs 21–40, etc. Lower communication overhead than TP; introduces pipeline "bubbles" (GPUs waiting). Used for very large models.

For a typical enterprise fine-tuning project (LoRA fine-tuning of a 7B–70B model): DDP with QLoRA (NF4 quantisation for fine-tuning) on 1–4 A100 80GB GPUs is the standard setup. Full pre-training requires hundreds to thousands of GPUs and is not an enterprise activity.

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — GPU memory sizing**

Your team wants to self-host a Llama-3 70B model. A developer says one H100 80GB GPU should be sufficient. Is this correct, and what memory would actually be required for production serving?

> **Detailed Answer:** Insufficient. At FP16, a 70B model requires 140GB just for weights — nearly 2× the H100's 80GB VRAM. You need at minimum 2× H100 80GB (160GB total) for the model weights at FP16. In practice, you also need memory for the KV cache during inference (scales with batch size and sequence length) and framework overhead, so 2× H100 is tight for anything beyond minimal throughput. Options: (1) Use 2× H100 NVLink with 160GB total VRAM for FP16. (2) Quantise to AWQ or GPTQ 4-bit, reducing memory to ~35GB — fits comfortably on a single H100 80GB with room for KV cache. For production serving with reasonable batch sizes, 2× A100 80GB (quantised to INT4/FP8) or 2× H100 80GB (FP16) are the standard configurations for 70B models.
>
> **Simple Explanation:** The calculation is straightforward: 70 billion parameters × 2 bytes per parameter (FP16) = 140 GB. One H100 has 80 GB. 140 > 80. The developer is wrong. Options: get 2 GPUs (160 GB total), or quantise to 4-bit (35 GB, fits on one H100 with room to spare). The quantisation option cuts memory 4× with typically less than 2% quality degradation on most tasks.
>
> **Architecture Takeaway:** Always calculate memory requirements before selecting hardware. The formula is: Parameters × Bytes per parameter = minimum model VRAM. Add 20–30% headroom for KV cache and framework overhead. Run this calculation in the design document — not after the GPU is provisioned and the model won't load.

---

**Question 2 — Batch cost analysis**

Your nightly batch process sends 10,000 documents averaging 8,000 tokens each to an LLM for summarisation. The current API cost is £2,400/month. An engineer proposes switching to a self-hosted model to save money. Walk through the cost comparison.

> **Detailed Answer:** First, calculate the actual usage: 10,000 docs × 8,000 tokens = 80M input tokens/month, plus output (say 500 tokens × 10,000 = 5M output tokens). At GPT-4o pricing (£2/M input, £8/M output): £160 + £40 = £200/month — not £2,400. The £2,400 suggests either a more expensive model (Opus/GPT-4 at ~£15/M tokens) or much higher volume. For a batch workload: (1) Check if batch API pricing applies — Anthropic and OpenAI offer 50% discounts for asynchronous batch jobs; this alone may halve the cost. (2) Self-hosted break-even: a single A10G at £0.80/hr = £576/month. At this batch volume (processed overnight in ~4 hours), you could use a spot/preemptible instance for ~£0.25/hr = £30/month. Self-hosted wins decisively if the team can operate it. (3) Quantise to INT4 to fit a capable open-weight model (Llama-3 70B INT4) on a single A10G. The real answer: run the numbers with your actual model pricing before committing to infrastructure investment.
>
> **Simple Explanation:** Before engineering self-hosted infrastructure, first ask "have we checked the batch API pricing?" Most providers offer 50% discounts for non-real-time batch processing — this is often enough to change the decision without any infrastructure change. Always calculate the actual token cost before assuming the current price is unavoidable.
>
> **Architecture Takeaway:** For batch workloads, check batch API pricing before self-hosting. Then calculate: (estimated monthly API cost at batch pricing) vs (GPU instance cost × hours needed + ops overhead). A 4-hour nightly window on a spot instance is dramatically cheaper than a 24/7 dedicated server. Match the infrastructure commitment to the actual usage pattern.

---

**Question 3 — Prefix caching value**

What is prefix caching and in what specific scenario does it produce the largest cost saving?

> **Detailed Answer:** Prefix caching stores the KV cache computation for a static prefix of the prompt — typically the system prompt and any fixed few-shot examples. When subsequent requests share the same prefix, the model skips re-computing those tokens and starts from the cached KV state. This saves both compute time and input token costs (most providers charge for cached tokens at 50–90% discount). Largest saving scenario: a system where every request shares a long, static system prompt. Example: a customer service agent with a 2,000-token system prompt (role definition, tool descriptions, policy guidelines, few-shot examples) and 200K queries/day. Without prefix caching: 2,000 tokens × 200K requests = 400M tokens/day of system prompt processing. With prefix caching: 2,000 tokens computed once per cache TTL, then cached. The saving is 400M tokens/day → near zero for the cached portion — potentially 70–80% of total input cost. The saving is proportional to (system prompt length / average total request length). When the system prompt is 80% of the average request, caching saves ~80% on input costs.
>
> **Simple Explanation:** Prefix caching is like memoisation for the repeated part of your prompts. If every customer service request starts with the same 2,000-token system prompt, you're paying to re-process those 2,000 tokens every single time — paying for the same work 200,000 times a day. With prefix caching, you process it once and store the result. Subsequent requests skip straight to the user's actual message.
>
> **Architecture Takeaway:** Prefix caching delivers the highest return on effort of all LLM cost optimisations — it requires no hardware change and often no code change (just a configuration flag at the serving layer or provider API call). Measure your average system prompt / total request length ratio. If your system prompt is more than 40% of the average request length, prefix caching is worth implementing immediately.

---

**Question 4 — Memory bandwidth bottleneck**

Explain the difference between compute-bound and memory-bandwidth-bound, and why this distinction matters for LLM serving architecture decisions.

> **Detailed Answer:** Compute-bound means the bottleneck is arithmetic operations — the GPU is spending most of its time doing matrix multiplications and the limit is FLOPS (floating-point operations per second). Memory-bandwidth-bound means the bottleneck is moving data between VRAM and compute cores — the GPU is spending most of its time on data transfer and the limit is GB/s (memory bandwidth). LLM inference at typical serving batch sizes is memory-bandwidth-bound. Each token generation step loads the full model weights and KV cache from VRAM — the data movement cost dominates the arithmetic cost. This matters for architecture decisions: (1) When comparing GPUs, memory bandwidth (GB/s) matters more than raw FLOPS for serving throughput at normal batch sizes — an H100 SXM (3.35 TB/s) generates tokens faster than an H100 PCIe (2 TB/s) even though both have similar compute specs. (2) Quantisation helps throughput not just by reducing memory footprint but by reducing the bytes moved per operation — INT4 moves 4× less data than FP16. (3) Disaggregated prefill/decode exists because prefill IS compute-bound (processing all input tokens in parallel) while decode is bandwidth-bound — optimal hardware differs for each phase.
>
> **Simple Explanation:** Think of a factory: compute-bound is when the machines can't work fast enough (need faster machines). Memory-bandwidth-bound is when the conveyor belt bringing materials to the machines is too slow (need a faster conveyor belt, not faster machines). LLM token generation is conveyor-belt-limited at typical scales — each token generation step needs to load billions of model weights from VRAM. This is why an H100 SXM (fastest conveyor belt: 3.35 TB/s) generates tokens faster than an H100 PCIe (2 TB/s) even though their pure compute specs are similar.
>
> **Architecture Takeaway:** When evaluating GPUs for LLM serving, prioritise memory bandwidth (GB/s) alongside VRAM capacity. The spec that matters most for token generation throughput is often not the one highlighted in vendor marketing. For architectural decisions: quantisation improves throughput by reducing bytes per operation, not just by reducing model size — a useful property when throughput, not just memory, is the constraint.

---

**Question 5 — Self-hosted total cost**

A business case for deploying a self-hosted Llama-3 70B model quotes GPU cost of £3.50/hr and expects to handle 50 requests/minute. Is this a complete cost model for presenting to a finance stakeholder? What is missing?

> **Detailed Answer:** Incomplete — GPU hardware is only one component. Missing costs: (1) Redundancy: production systems need at least 2 instances for high availability — double the GPU cost. (2) Engineering/ops overhead: operating a self-hosted LLM requires monitoring, incident response, updates, and capacity management — typically 0.25–0.5 FTE of MLOps time. (3) Storage: model weights (140GB at FP16, or 35GB at INT4), plus logging and monitoring data. (4) Networking: data transfer costs for ingress/egress, especially if GPU instances are in a different region from the application. (5) Development cost: initial setup (vLLM configuration, load balancer, monitoring, CI/CD for model updates) is typically 2–4 weeks of engineering time. (6) Model refresh cost: when a newer model version improves quality, migration requires testing and deployment effort. Compare to API pricing which includes all of the above as part of the service. A complete model presents: (total GPU cost × redundancy factor) + (ops FTE cost) + (amortised setup cost) vs API cost at expected volume.
>
> **Simple Explanation:** Quoting only the GPU cost for a self-hosted model is like quoting only the hardware cost for an on-premises data centre — leaving out rack space, power, cooling, network, support staff, and maintenance. The GPU rate is the smallest part of the real cost. The complete cost includes redundancy (double the GPUs), the engineer who keeps it running (0.25–0.5 FTE), the setup and migration work (weeks of engineering), and the ongoing model upgrade cost. Without these, the business case understates the true total cost of ownership.
>
> **Architecture Takeaway:** Always present a Total Cost of Ownership (TCO) comparison for self-hosted vs API: (GPU cost × 2 for redundancy) + (ops FTE monthly cost) + (amortised setup cost over 12 months) vs (API cost at expected volume). At 50 req/min (72K/day) for a 7B model, API is almost always cheaper when TCO is calculated honestly. The crossover to self-hosted typically requires 500K+ requests/day before the GPU cost saving outweighs the ops overhead.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers PagedAttention internals, knowledge distillation, and financial cost modelling in depth. It is safe to skip on a first pass and return here later.

### 8.1 PagedAttention: How vLLM Manages Memory

The KV cache — the memory storing attention computations for all processed tokens — is the primary memory consumer during inference. Naïvely, each request pre-allocates a contiguous block of memory equal to its maximum sequence length. This wastes memory (most requests are shorter than maximum) and causes fragmentation (free memory scattered in unusable gaps).

**PagedAttention** manages KV cache like OS virtual memory:
- Memory is divided into fixed-size **pages** (blocks of 16–32 tokens)
- Each request is allocated pages on demand, not upfront
- Pages for a single sequence need not be contiguous in physical memory — a mapping table tracks which pages belong to which sequence
- When a sequence completes, its pages are immediately freed and available for other sequences

**The result:** GPU memory utilisation increases from ~55% (naïve contiguous allocation) to ~95%. For a given GPU, this means 2–4× more concurrent requests can be served — directly multiplying throughput without adding hardware.

### 8.2 Knowledge Distillation and Pruning

When you need a smaller, faster model with quality close to a larger one, two techniques apply:

**Knowledge Distillation:** train a small "student" model to mimic the output distribution of a large "teacher" model. The student learns not just the correct labels but the teacher's full probability distribution — which encodes more information than hard labels alone. GPT-4o-mini is (reportedly) a distilled version of GPT-4o.

For architects: distillation is relevant when you want to fine-tune a custom model for your domain that is small enough to self-host cheaply, but trained with the quality signal of a much larger model.

**Structured Pruning:** systematically remove entire attention heads, neurons, or layers that contribute least to model quality. A pruned model has fewer parameters and is genuinely faster — unlike quantisation which keeps the same computation in lower precision.

For architects: pruning is less commonly needed in deployment decisions (quantisation usually suffices), but you may encounter it in model cards ("this model uses structured pruning to reduce from 70B to 40B parameters").

**In a vendor conversation:** If a vendor claims their 7B model performs comparably to a 70B model, ask: distilled from which teacher model? On which benchmark tasks? Evaluated against which baseline? Distillation is legitimate — but the claim needs specifics to be meaningful.

### 8.3 The Token Budget: A Financial Model

For any production AI system, build a token budget at design time:

```
Monthly token budget:

Workload: customer service assistant
Queries/day:          50,000
Input tokens/query:    1,200  (system prompt 800 + user message 400)
Output tokens/query:     300
Days/month:               30

Monthly input tokens:  50,000 × 1,200 × 30 = 1,800,000,000 (1.8B)
Monthly output tokens: 50,000 × 300 × 30   =   450,000,000 (450M)

At Claude Sonnet pricing (£1.50/M input, £6.00/M output):
Input cost:  1,800M × £1.50/M = £2,700/month
Output cost:   450M × £6.00/M = £2,700/month
Total:                          £5,400/month

With prefix caching (800-token system prompt cached, 60% discount on cached portion):
Cached input: 800/1,200 × 1,800M × £0.60/M = £720/month
Uncached input: 400/1,200 × 1,800M × £1.50/M = £900/month
Output: £2,700/month
Total with caching: £4,320/month (20% saving)

With 10% semantic cache hit rate (avoids entire LLM call):
Effective queries: 50,000 × 0.90 = 45,000/day
Adjusted total: £4,320 × 0.90 = £3,888/month
```

Building this model before deployment surfaces the cost sensitivity to each variable — output token length has 4× the price impact of input token length, so controlling output length (max_tokens parameter, concise prompting) has high leverage.

---

## 9. Key Takeaways (5 Bullets)

- **GPU VRAM is the primary constraint for LLM deployment — everything else follows from it.** Model weights must fit in VRAM before any inference happens. A 70B model at FP16 needs 140GB; quantised to INT4 it needs 35GB. Know the memory requirement before choosing hardware or deciding between self-hosted and API.

- **Quantisation is the highest-leverage optimisation for self-hosted models.** Going from FP16 to AWQ/GPTQ 4-bit reduces memory 4×, enabling larger models on smaller hardware with typically < 2% quality degradation on most tasks. Always evaluate on your specific task — benchmark averages may not represent your use case.

- **LLM inference is memory-bandwidth-bound, not compute-bound.** The bottleneck is moving data between VRAM and compute cores, not arithmetic. This means memory bandwidth (GB/s) matters more than FLOPS for serving throughput, and quantisation helps throughput not just by reducing size but by reducing bytes moved per operation.

- **The self-hosted vs API decision is a volume and ops-capability threshold.** Below ~50–100K requests/day for a mid-tier model, API is almost always cheaper once ops overhead is included. Above that threshold — or with strict data residency requirements — self-hosted pays off. Run the break-even analysis with your actual numbers, not generic estimates.

- **Caching (prefix, semantic, KV) is cost reduction that requires no hardware change.** Prefix caching saves 50–80% on static system prompt tokens. Semantic caching eliminates entire LLM calls for repeated similar queries. Prompt caching is available from most API providers at 50–90% discount on cached tokens. Implement caching before considering infrastructure changes — it typically delivers 20–40% cost reduction with minimal engineering effort.
