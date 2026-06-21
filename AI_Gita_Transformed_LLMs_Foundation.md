# LLMs & Foundation Models — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

A **Large Language Model (LLM)** is a software system trained on an enormous amount of text — books, websites, code, research papers, conversations — that has learned to predict what text should come next given any input. The "large" refers to the number of parameters (weights): a current mid-range model has 7–70 billion parameters; frontier models have hundreds of billions.

The surprising result: a system trained purely to predict the next word develops the ability to reason, follow instructions, write code, summarise documents, answer questions, and engage in multi-turn dialogue. Nobody explicitly taught it these capabilities — they emerged from the scale of the training task.

A **Foundation Model** is the base model that comes out of this training process — a general-purpose capability engine. When a provider like Anthropic or OpenAI applies additional training (instruction tuning, safety alignment, RLHF (Reinforcement Learning from Human Feedback — a training process where human raters score model outputs and those scores are used to shape the model's behaviour toward helpful, harmless responses)) to make the model useful in a conversation, it becomes a **chat model** (Claude, GPT-4o, Gemini, etc.).

**What this means for architects:**

> **What is the context window?** The context window is the maximum amount of text the model can hold in working memory at once — your prompt, conversation history, retrieved documents, and the model's response all count toward this limit. Think of it as a whiteboard: everything the model needs to reason with must be written on this whiteboard. When it fills up, earlier content falls off and the model can no longer see it. Current models support 128K–1M tokens (roughly 90,000–750,000 words), but long agent workflows with rich tool outputs fill this faster than you expect.

You almost never interact with a raw foundation model. You work with instruction-tuned, safety-aligned derivatives. But understanding the foundation — what the model actually is, how it processes text, what its fundamental limits are — is what allows you to:
- Set correct expectations for what the model can and cannot do
- Diagnose failures ("this is a knowledge limit, not a reasoning limit")
- Choose the right model for the right task and cost point
- Configure model parameters (temperature, context window, sampling) correctly
- Design systems that work with the model's nature rather than against it

---

## 2. Why Should I Care

### For Solution Architects

> **What is a token?** A token is the basic unit of text that LLMs process — and the unit that APIs charge for. Roughly 3–4 characters or 0.75 words in English. "Hello world" = 2 tokens. 1,000 tokens ≈ 750 words ≈ 1.5 pages. APIs charge separately for **input tokens** (your prompt) and **output tokens** (the model's response). When you see pricing like "$2 per million tokens", that is the cost per million of these text chunks.

Every LLM-based system you design sits on a model choice. That choice determines:

- **Capability ceiling:** what the model can reliably do (complex multi-step reasoning? structured output? long document analysis?)
- **Context window:** how much text you can feed in a single call (8K? 128K? 1M tokens?) — directly determines your RAG architecture and document handling strategy
- **Cost:** from £0.0003/1K tokens (small models) to £0.015/1K tokens (frontier models) — 50× range
- **Latency:** from 200ms to 30+ seconds depending on model size and output length
- **Data residency:** which cloud provider hosts the model — affects compliance posture
- **Availability and rate limits:** what burst capacity the model supports

Choosing the wrong model for a use case is one of the most common and expensive architectural mistakes in AI systems. Choosing GPT-4o for a task that GPT-4o-mini handles equally well costs 15× more. Choosing a small model for complex reasoning produces unreliable outputs regardless of prompt quality.

### For Enterprise Architects

> **Explain Like I'm an Architect**
>
> You've managed software vendor risk for years — you know how to handle a database upgrade, a messaging platform EOL, or an ERP pricing change. LLMs introduce a new category of vendor risk that doesn't fit any of those playbooks.
>
> Imagine a critical third-party API that: (a) changes its response format without a deprecation notice, (b) cannot guarantee it will return the same answer to the same question twice, (c) has a "knowledge expiry date" where its answers become increasingly stale, and (d) charges you per word of every conversation. Now imagine that API is embedded in dozens of enterprise workflows. That's the risk profile you're governing.

Foundation models represent a new category of enterprise software dependency: **opaque, probabilistic, and vendor-controlled**. Unlike a database or a messaging system, an LLM:
- Updates without your consent (model versions change; behaviour changes)
- Cannot be fully specified in a contract (you cannot guarantee "the model will always output X")
- Has a knowledge cutoff that creates temporal drift between model capabilities and world state
- Is subject to vendor pricing decisions that can change your operating cost

Enterprise architects need a model governance strategy: which providers are approved, how model version changes are managed, what evaluation gates exist before a model update reaches production, and what fallback exists if a provider has an outage.

---

## 3. Think About It Like This (Analogy)

**The Compression Library Analogy**

Imagine an extraordinarily sophisticated compression algorithm that has been trained on the entire written output of human civilisation. It has compressed all that knowledge — not into bits and bytes, but into a 70-billion-parameter mathematical structure that captures the patterns, relationships, and conditional probabilities of human language.

When you send a prompt, you're not "asking a question" in the way you'd query a database. You're providing a starting context and asking the compression library to "decompress" the most probable continuation, given everything it learned during training.

This analogy explains several things that confuse people about LLMs:

**Why does it hallucinate?** A compression algorithm optimises for plausible continuations, not verified facts. If the training data contained patterns where "the capital of X is Y" was followed by confident answers, the model continues that pattern — even if the specific answer wasn't in the training data and the model fills in a plausible-sounding but wrong answer.

**Why does prompting work?** Changing the context changes what "decompress" means. "Continue this story" produces narrative. "Answer this question factually" produces different patterns. "Output valid JSON" constrains the decompression to match JSON-shaped patterns.

**Why do bigger models do more?** More parameters = more expressive compression = more nuanced patterns captured = better ability to generalise to novel combinations. A 7B model has captured broad patterns; a 70B model has captured finer-grained structure that enables more reliable multi-step reasoning.

**Why is the context window a hard limit?** The decompression works over the tokens provided. Beyond the context window, the model has no memory of earlier text — it can only continue from what's in the window right now.

**The instruction-tuned model = a specialised interface.** The foundation model (the raw compression library) is hard to use directly. Instruction tuning applies a layer of fine-tuning that teaches the model to respond to natural language instructions — "answer my question, don't just predict text." The safety alignment layer adds further training to prevent harmful outputs. What you use in production is this layered product, not the raw foundation.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 How an LLM Processes Text: The Minimal Model

> **Explain Like I'm an Architect**
>
> Imagine the world's most sophisticated autocomplete — not the basic autocomplete on your phone, but one that has read every book, article, website, code repository, and research paper ever written. When you type a prompt, it predicts the most statistically likely next piece of text, then the next, then the next — building up a response one small chunk at a time.
>
> Each chunk is called a **token** (roughly a word or part of a word). This matters because everything about how you use and pay for the model is counted in tokens: your cost, your speed, your context limit — all tokens, not words or characters.
>
> The "one token at a time" generation process is called **autoregressive**. Think of a chef building a dish ingredient by ingredient — each addition is informed by everything already in the pot, and you can't go back. The model generates sequentially: token 1, then token 2 (knowing token 1), then token 3 (knowing tokens 1 and 2), and so on. This is why longer outputs take proportionally longer, and why you pay for every single output token produced.

You need enough of a mental model to diagnose failures and make configuration decisions. You don't need to understand backpropagation or attention math.

**Step 1 — Tokenisation.** Your text is broken into tokens. A token is roughly 0.75 words in English — "the quick brown fox" becomes ["the", " quick", " brown", " fox"] — 4 tokens. Non-English languages and code often have larger token-to-character ratios (more tokens per word). This matters because:
- The context window limit is in tokens, not words
- Input and output pricing is per token
- Unusual encodings (tables, special characters, non-Latin scripts) cost more tokens than you'd expect

**Step 2 — Embedding.** Each token is converted to a vector of numbers — think of it as a set of coordinates that places the token in a vast conceptual map, where similar concepts end up physically close to each other. "King" and "Queen" are nearby; "King" and "Tax" are far apart. This vector representation is how the model encodes meaning mathematically.

> **Common Misconception:** Embeddings are not a lookup table. The model doesn't store a fixed definition for "bank" — it assigns coordinates dynamically based on context. "Bank" in "river bank" gets different coordinates than "bank" in "bank account." This is what makes the model context-aware.

**Step 3 — Transformer layers.** The vectors pass through N layers (32 layers in Llama-3 8B; 80 layers in Llama-3 70B). Each layer applies **attention** — each token's vector is updated based on all other tokens in the context — and a **feed-forward network**. By layer 80, the original token vectors have been transformed to encode rich contextual meaning: the word "bank" now knows whether it means riverbank or financial institution, based on context.

**Step 4 — Output prediction.** The final layer produces a probability distribution over the vocabulary (~32,000–128,000 tokens) for the next token. The model doesn't generate a word — it generates a probability distribution. "The capital of France is ___" might give 98% probability to "Paris", 0.5% to "Lyon", 0.3% to "Bordeaux".

> **Explain Like I'm an Architect — Why This Is Important**
>
> Picture a weather forecaster who doesn't say "it will rain" — they say "70% chance of rain, 20% chance of clouds, 10% chance of sun." The model does the same for every single word in its response. It never "knows" an answer with certainty — it produces its best probability estimate for what should come next.
>
> This is the root cause of hallucination. If the training data had confident-sounding answers to factual questions, the model learned to produce confident-sounding text — even when filling in a gap it never actually learned. It confidently picks the most probable-sounding token, not the most correct one.

**Step 5 — Sampling.** The next token is selected from this distribution according to the sampling parameters you configure (temperature, top-p). This is repeated for each output token until the model generates a stop token.

**The key architectural insight:** LLMs are **autoregressive** — each output token is generated one at a time, and each depends on all previous tokens (input + previously generated output). This is why longer outputs take proportionally longer, and why generation can't be trivially parallelised beyond a certain point.

### 4.2 The Transformer Architecture: What Architects Need to Know

> **Explain Like I'm an Architect**
>
> Imagine you're reading a contract and you hit the word "it" — you immediately look back through the document to figure out what "it" refers to. Maybe it was "the supplier", three paragraphs ago. You didn't read the whole contract again — you quickly scanned for the most relevant antecedent.
>
> **Attention** is the mechanism that does exactly this, for every word, on every pass through the model. For each token, the model asks: "Which other tokens in this context are most relevant to what I'm trying to predict next?" It scores all other tokens in the window, weights them by relevance, and pulls in their meaning proportionally.
>
> Why does this matter to architects? Because attention is what makes the model **context-aware** — it's why "Paris" comes out differently in "the city Paris" versus "Paris Hilton." But it also has a cost: computing relevance between all tokens means the computation grows with the square of context length. Double the context window, roughly quadruple the compute. This is why very large context windows are expensive and why long contexts can introduce subtle quality degradation.

**Attention** is the mechanism that makes Transformers powerful. For each token, the attention layer asks: "which other tokens in this context are most relevant for predicting the next token?" It computes a weighted combination of all context vectors, where the weights are learned during training.

This is why:
- The model can resolve "it" in "the customer called the supplier and asked it to reschedule" — attention connects "it" to "supplier" based on the pattern learned during training
- Performance degrades for very long contexts — with 100K tokens in context, attention must compute relationships between all 100K tokens, which is computationally expensive and can become noisy
- "Lost in the Middle" is a real phenomenon — models attend more strongly to tokens near the beginning and end of the context window, information buried in the middle is less reliably accessed

**What architects don't need to know:** the exact attention formula (Q×K^T / √d_k), the self-attention vs cross-attention distinction (relevant for encoders, mostly irrelevant for decoder-only LLMs), or the implementation details of multi-head attention.

### 4.3 Sampling Parameters: Architect-Relevant Configuration

> **Explain Like I'm an Architect**
>
> Remember that weather forecaster producing a probability distribution — 70% rain, 20% clouds, 10% sun? Now imagine you have a dial that controls how that forecaster behaves:
>
> - **Dial at 0 (Temperature = 0):** The forecaster always announces whatever has the highest probability. No surprises, maximum consistency. Every day, same answer given the same inputs.
> - **Dial at 1 (Temperature = 1):** The forecaster picks randomly according to the actual probabilities. Most days rain (70% chance), but sometimes clouds or sun. Natural variation.
> - **Dial past 1 (Temperature > 1):** The forecaster flattens the odds — treats rain, clouds, and sun as nearly equally likely. Very surprising, creative, unpredictable outputs. Often wrong.
> - **Dial below 1 (Temperature < 1):** The forecaster becomes even more conservative — sharpens the probabilities so the most likely option wins even more often.
>
> For enterprise systems doing extraction or classification, you always want the dial at or near zero. You're not asking for creativity — you're asking for the right answer, consistently. For a brainstorming chatbot, dial it up.
>
> **Common Misconception:** Temperature = 0 does not mean the model is "less intelligent" or more restricted. It means the model always picks its best answer, every time. For tasks with a right answer, that's exactly what you want.

When you call an LLM API, you configure parameters that control how the model selects tokens from the output probability distribution. These are not abstract — they directly control the reliability and character of model outputs.

**Temperature**

Temperature scales the probability distribution before sampling:
- **Temperature = 0:** always pick the highest probability token (greedy decoding). Maximum consistency, minimum creativity. The same input will produce the same output every time (approximately — some variance from hardware).
- **Temperature = 1:** sample from the raw probability distribution. Balanced.
- **Temperature > 1:** flatten the distribution — tokens with lower probability become more likely. More creative, more diverse, more variable, more prone to error.
- **Temperature < 1:** sharpen the distribution — high-probability tokens become even more likely. More consistent, less surprising, more conservative.

**When to use each:**

| Task | Temperature | Reason |
|---|---|---|
| Data extraction (fields from documents) | 0.0–0.1 | Consistency is everything; creativity harmful |
| Classification | 0.0–0.1 | Deterministic output required |
| Q&A with factual answers | 0.1–0.3 | Mostly consistent, slight variation acceptable |
| Summarisation | 0.3–0.5 | Some variation acceptable, accuracy important |
| Chatbot / conversation | 0.5–0.8 | Natural variation, engaging |
| Creative writing / brainstorming | 0.8–1.2 | Diversity desired |

**Top-p (nucleus sampling)**

> **Explain Like I'm an Architect:** Instead of picking from all 100,000 possible next tokens, top-p says "only pick from the tokens that together account for at least p% of the probability." At top-p = 0.9, you're only ever choosing from the model's "reasonable shortlist" for the next word — ignoring the long tail of unlikely garbage tokens entirely. This prevents the occasional incoherent output without killing variety the way Temperature = 0 does.

Instead of sampling from the full vocabulary distribution, restrict to the smallest set of tokens whose cumulative probability exceeds p:
- top-p = 0.9: consider only the tokens that together account for 90% of the probability mass
- Prevents the model from selecting very low probability, incoherent tokens
- Works together with temperature; most production systems set both

**Top-k**

Restrict to the top-k highest probability tokens regardless of their probabilities. Less commonly used in production than top-p; top-p is generally preferred.

**Max tokens (max_new_tokens)**

Hard limit on output length. Critical for:
- Cost control: output tokens are often 2–4× more expensive than input tokens
- Latency control: output length directly determines generation time
- Pipeline safety: unbounded output lengths cause downstream parsing failures

**Stop sequences**

Strings that cause generation to stop when produced. Use for: structured output (stop when you see "}" to prevent over-generation), multi-turn loops (stop when agent outputs a specific marker), safety (stop when specific patterns appear).

**Frequency and presence penalties**

Reduce the probability of tokens the model has already output:
- Frequency penalty: scales with how many times a token has appeared — discourages repetitive text
- Presence penalty: flat penalty for any token that has appeared — discourages reuse

Use for: long-form generation where repetition is a problem. For structured tasks, leave at zero.

### 4.4 Model Selection Framework: The 2026 Landscape

> **Explain Like I'm an Architect**
>
> Think of LLM tiers like hiring contractors for a building project:
>
> - **Tier 1 (Frontier)** is your top-tier specialist architect — brilliant, expensive, slow to produce output, worth it for the complex design decisions only they can handle.
> - **Tier 2 (Capable general)** is a strong senior contractor — handles most work well, reasonable cost, your default choice for most enterprise projects.
> - **Tier 3 (Efficient)** is a skilled tradesperson — fast, cheap, excellent for well-defined, repeatable tasks. Don't ask them to redesign the building; do ask them to install 10,000 light fittings.
>
> The most expensive mistake in enterprise AI is using the top-tier architect to install light fittings. The second most expensive is using the tradesperson to design a load-bearing structure.
>
> **The rule:** always start at the cheapest tier that might work, test it on real data, and only step up if quality genuinely requires it.

The frontier model landscape changes every few months. Rather than memorising specific models (which will be deprecated), learn the selection framework and apply it to current options.

**Tier 1 — Frontier reasoning models** (GPT-4o, Claude Opus, Gemini Ultra, o3)
- Strongest multi-step reasoning, complex instruction following, code generation
- Most expensive: £10–30/M input tokens, £30–60/M output tokens
- Highest latency: 10–30+ seconds for long outputs
- Use when: the task genuinely requires complex reasoning that smaller models fail at, or you need the best available quality regardless of cost
- Enterprise sweet spot: high-stakes, low-volume tasks (legal analysis, complex document review, architectural design assistance)

**Tier 2 — Capable general models** (Claude Sonnet, GPT-4o-mini, Gemini Pro, Llama-3 70B)
- Strong reasoning, good instruction following, broad capability
- Mid-range cost: £1–5/M input tokens, £3–15/M output tokens
- Latency: 3–15 seconds for typical outputs
- Use when: quality matters but cost or latency are also constraints
- Enterprise sweet spot: customer-facing applications, internal tools, high-volume workflows where frontier quality is unnecessary

**Tier 3 — Efficient models** (Claude Haiku, GPT-4o-mini, Gemini Flash, Llama-3 8B)
- Good at well-defined, narrow tasks: classification, extraction, summarisation, formatting
- Low cost: £0.10–0.50/M input tokens, £0.30–1.50/M output tokens
- Low latency: sub-second to 3 seconds
- Use when: task is well-scoped, volume is high, latency matters
- Enterprise sweet spot: real-time applications, high-volume pipelines, cost-optimised workflows

**Tier 4 — Specialised models**
- Embedding models (text-embedding-3-large, BGE, E5) — for vector search, semantic similarity
- Vision-language models (GPT-4V, Claude with vision, Gemini Vision) — for image/document understanding
- Code-specialised (CodeLlama, DeepSeek-Coder) — for code generation and review
- Reasoning-specialised (o1, o3, DeepSeek-R1) — extended thinking for mathematical/logical tasks

**Model selection decision framework:**

```
Step 1: What is the task type?
  Narrow + well-defined (classification, extraction, formatting) → start at Tier 3
  General + medium complexity (Q&A, summarisation, chat) → start at Tier 2
  Complex reasoning, code generation, analysis → start at Tier 1 or 2

Step 2: What is the volume and cost sensitivity?
  < 10K requests/day, cost not primary → start higher tier, optimise later
  > 100K requests/day, cost is a constraint → start at lowest tier that meets quality

Step 3: Evaluate on your task before committing
  Run 100 representative examples through your top 2 model candidates
  Score with an LLM judge on your task-specific criteria
  Fail fast: if Tier 3 meets quality bar, don't pay for Tier 2

Step 4: Consider operational constraints
  Data residency → which cloud providers are approved?
  Context window → is 128K sufficient or do you need 1M tokens?
  Rate limits → does the model support your peak throughput?
  API stability → is the model available with an SLA you can commit to?
```

**The context window as a model selection criterion:**

| Use case | Context window needed | Suitable models |
|---|---|---|
| Chat, Q&A, short documents | 8K–32K | All models |
| Long documents, books, contracts | 128K | Most current models |
| Full codebases, entire contract libraries | 1M+ | Gemini 1.5 Pro, Llama 3.1 (128K), Claude 3.7 Sonnet |
| Real-time short interactions | Any | Latency matters more |

### 4.5 Understanding Model Limitations: What Never Changes

> **Explain Like I'm an Architect**
>
> Regardless of how smart a model appears, it has four hard constraints baked into the architecture. These are not bugs to be fixed in a future version — they are properties of how LLMs work. Knowing them before you design saves you from building systems that fail in production.
>
> Think of it like knowing the load limits of a bridge: not a reason to avoid bridges, but essential knowledge before you design the traffic plan.

**1. Knowledge cutoff.**

> **Explain Like I'm an Architect:** An LLM is a snapshot of the internet, not a live connection to it. It's like a highly educated person who has read everything published before a certain date but has been completely offline ever since. Ask about the financial crisis of 2008 — brilliant answer. Ask about the acquisition that closed last month — blank stare. For anything time-sensitive, you must bring the current information to the model (via RAG or tool use); the model cannot go and get it itself. The model's training data has a cutoff date. Events after that date are unknown to the model. For time-sensitive enterprise use cases, this means RAG (or web search tools) are required to ground the model in current information.

**2. Context window = working memory.**

> **Explain Like I'm an Architect:** Every time you call the LLM API, it's like waking the model from complete amnesia. It has no idea who you are, what you discussed last time, or what happened earlier in this session — unless you include all of that in your current message. The context window is literally everything the model can "see" at this moment. It's the equivalent of a brilliant consultant who, every time they walk into the meeting room, needs to be handed a complete briefing document from scratch — because they remember nothing from the last meeting. This fundamentally shapes how you design multi-turn conversations, how you handle long documents, and how you manage cost (because that briefing document costs tokens every single call).

The model has no persistent memory across calls. Each API call is stateless — the model has only what you put in the context window. Everything the model "knows" for your task must be in the prompt. This is why multi-turn conversation requires passing the full conversation history on each call, and why long conversations eventually hit context limits.

**3. Probabilistic, not deterministic.**

> **Explain Like I'm an Architect:** Even when you set temperature = 0 and ask the exact same question twice, you are not guaranteed to get bit-for-bit identical output. Hardware-level floating-point rounding differences, request batching, and parallelisation effects introduce tiny variations that can cascade into different output paths. For systems that must produce identical outputs for auditing or regulatory purposes, this matters: you need to capture and store outputs, not re-run calls and compare.

Even at temperature=0, LLMs are not fully deterministic in production (hardware non-determinism, batching effects). For workflows requiring 100% reproducibility, the architecture must handle this — don't rely on "same input always gives same output."

**4. Hallucination is inherent, not a bug to be fixed.**

> **Explain Like I'm an Architect:** This one surprises most architects the first time they hear it. Hallucination — the model confidently stating something false — is not a mistake, a bug, or something a future model version will eliminate. It is a direct consequence of how LLMs work: they generate the most plausible-sounding next token, not the most verified next token. They have no internal "fact-checker." Think of an extremely confident new hire who was never taught to say "I don't know" — they'll always give you an answer, sometimes fabricating details to fill gaps, because that's the pattern they learned.
>
> **Common Misconception:** "We just need a better model to fix hallucinations." Every generation of models hallucinates. Better models hallucinate less frequently, but on high-stakes enterprise use cases, even rare hallucinations are unacceptable. The architectural answer is to design systems that verify outputs — RAG for grounding, structured output with validation, human-in-the-loop for high-stakes paths, and monitoring pipelines that catch anomalies before they reach users.

LLMs generate plausible continuations — they don't verify facts. Hallucination is a property of the architecture, not a failure of a specific model. It can be mitigated (RAG, structured prompting, verification steps) but not eliminated. Systems must be designed assuming some fraction of outputs will contain errors.

---

## 5. Enterprise Example

**Scenario: Model Selection for a Retail Group's AI Platform**

A retail group is building a central AI platform to serve three internal teams. The architecture team must select models for each workload, balancing quality, cost, and operational constraints.

**Workload 1: Product description enrichment**
- Task: take raw supplier product data (name, SKU, basic specs) and generate a structured, customer-facing product description in brand voice
- Volume: 50,000 products/month (batch, not real-time)
- Quality requirement: descriptions must be on-brand, accurate to the spec data, and follow a specific format
- Data: all internal (no sensitive PII)

Model selection analysis:
- Task is narrow and well-defined → start at Tier 3
- Test: GPT-4o-mini vs Claude Haiku on 100 sample products, scored by brand team
- Result: Haiku scores 4.2/5, GPT-4o-mini scores 4.0/5 on brand voice; both pass format compliance at 99%+
- Cost at volume: 50K products × avg 600 input tokens × avg 300 output tokens = 30M input + 15M output tokens/month
  - Claude Haiku: 30M × £0.25/M + 15M × £1.25/M = £7.50 + £18.75 = **£26.25/month**
  - Claude Sonnet: 30M × £3/M + 15M × £15/M = £90 + £225 = **£315/month**
- Decision: **Claude Haiku**. 12× cost saving; quality meets the bar.

**Workload 2: Customer service email triage and draft response**
- Task: classify incoming customer emails (10 categories), extract key information, draft a response for human review
- Volume: 8,000 emails/day, real-time (< 5 second SLA for classification + draft)
- Quality requirement: classification accuracy > 95%; draft quality must reduce agent editing time by 50%+
- Data: contains customer PII — EU data residency required (Azure OpenAI or Anthropic EU)

Model selection analysis:
- Task has two parts: classification (Tier 3 suitable) and draft generation (needs Tier 2 quality for good drafts)
- Design decision: use a two-call pattern — fast Tier 3 model for classification, Tier 2 model for draft only on emails that pass certain routing criteria
- Data residency: Anthropic EU endpoint available; Azure OpenAI GPT-4o-mini available in EU regions
- Test: GPT-4o-mini for classification (97.8% accuracy on 500 test emails — passes bar); Claude Haiku vs Claude Sonnet for draft quality
- Draft quality test: Sonnet drafts rated by agents as requiring "minor edits" 71% of the time; Haiku drafts 49% — meaningful gap for agent satisfaction
- Cost: 8K emails/day × 30 days = 240K emails/month
  - Classification (Haiku, 500 tokens): 240K × 500 tokens = 120M tokens/month @ £0.25/M = **£30/month**
  - Draft (Sonnet, 1K input + 400 output): 240K × 1.4K tokens = 336M tokens/month @ blended £5/M = **£1,680/month**
- Decision: **Haiku for classification + Claude Sonnet for draft generation.** Data residency satisfied. Total: £1,710/month.

**Workload 3: Supplier contract risk analysis**
- Task: review supplier contracts (average 40 pages), identify non-standard clauses, flag risk areas, summarise obligations
- Volume: 200 contracts/month (batch, 24-hour SLA)
- Quality requirement: legal team must approve — cannot miss material risks
- Data: commercially sensitive contracts — strict data handling required

Model selection analysis:
- Task requires complex reasoning over long documents → Tier 1 or high-end Tier 2
- 40 pages ≈ 24,000 tokens average input; needs 128K+ context window
- Risk tolerance is low (legal team sign-off required) → quality over cost
- Test: Claude Opus vs Claude Sonnet on 20 contracts reviewed by legal
  - Legal team rates Opus analysis as "complete" 94% of time; Sonnet 81%
  - Gap is material for legal risk — 19% miss rate on Sonnet is not acceptable
- Cost: 200 contracts × avg 24K input + 3K output = 200 × 27K tokens
  - Claude Opus: 200 × 27K × £15/M blended = **£81/month** (low volume saves this)
- Decision: **Claude Opus**. Volume is low enough that the quality premium costs only £81/month.

**Total platform cost: £1,817/month.** A naive "use GPT-4o for everything" approach would cost £12,400/month. The model selection strategy delivers 85% cost reduction by matching model capability to task requirements.

---

## 6. Architecture Perspective

### Model as a Dependency: What Changes in Your Architecture

> **Explain Like I'm an Architect**
>
> Every dependency you take in an enterprise system has a risk profile. Databases are deterministic and versioned. Message queues are reliable and auditable. REST APIs are stateless but predictable. LLMs are **none of these things** in the traditional sense.
>
> They behave more like an expert consultant on retainer: brilliant, fast, probabilistic, occasionally wrong, sometimes unavailable, subject to cost renegotiation, and operating on knowledge that gets stale over time. Everything about how you architect for them — versioning, latency, cost, caching, error handling — needs a different mental model than your standard integration dependency.
>
> **Common Misconceptions About LLMs as Dependencies:**
> - *"I can cache the output like any other API call."* — Sometimes yes, but only for identical inputs. LLM outputs vary even for the same input; cache design must account for this.
> - *"I can retry on failure the same way."* — Yes, but retried LLM calls may return different outputs. Idempotency cannot be assumed.
> - *"The contract is the API spec."* — The API spec only covers shape (inputs/outputs). It says nothing about quality, accuracy, or consistency of content — those are your responsibility to evaluate and monitor.

When you introduce an LLM as a dependency, several architecture patterns shift:

**Idempotency breaks.** Traditional systems design around idempotent operations — the same input produces the same output. LLMs are not idempotent by default. Design downstream systems to handle variability: validate output schema, don't assume format consistency, build parsing that degrades gracefully.

**Latency profiles change.** LLM calls range from 500ms to 30+ seconds. This fundamentally changes UI/UX design (streaming is often required for interactive applications), timeout strategy (traditional 5-second HTTP timeouts will fail), and synchronous vs asynchronous architectural patterns.

**Token budget replaces data volume.** Cost modelling shifts from "compute per request" to "tokens per request × token price." Build token budgets into system design: know the expected input token count (system prompt + context + user message) and output token count for each use case before selecting a model. As a rough anchor: a 2,000-token system prompt at 10,000 API calls per day costs approximately £15–30/day at typical frontier model pricing — before any user input or output tokens. Budget both input and output token volumes, not just output.

**Model versioning is a deployment concern.** When a provider updates a model (even a minor version), behaviour can change. Production systems need: explicit model version pinning in API calls, evaluation gates triggered by model version changes, and a fallback to the previous version if regressions are detected.

**Context window = API contract.** The context window is not just a technical constraint — it's an architectural boundary. Systems that need to process documents larger than the context window require chunking, summarisation, or RAG strategies. Design for this explicitly; don't treat the context window as "big enough."

### The Architecture Evolution of LLMs

For architects who want the historical context:

| Architecture | Era | Key capability | Limitation |
|---|---|---|---|
| RNNs / LSTMs | 2014–2017 | Sequential text modelling | Short-range dependencies only; slow training |
| Transformers (BERT/GPT) | 2017–2020 | Long-range attention; parallelisable training | Fixed context window; quadratic attention cost |
| GPT-3 class (175B) | 2020–2022 | In-context learning; few-shot prompting | Expensive; limited instruction following |
| InstructGPT / ChatGPT | 2022–2023 | RLHF alignment; instruction following | Hallucination; limited context |
| GPT-4 / Claude 2 | 2023 | Multimodal; 128K context; better reasoning | Cost |
| 2024–2026 frontier | 2024–2026 | 1M+ context; tool use; reasoning models; multimodal | Ongoing |

The key lesson for architects: the pace of capability improvement is high, but the fundamental limitations (hallucination, context window as working memory, knowledge cutoff, probabilistic output) have not changed across generations. Design systems around these constants, not around the capabilities of a specific model at a point in time.

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* behind each concept and can apply it to a new situation.

---

**Question 1 — Knowledge currency**

A business stakeholder asks why the customer service chatbot "doesn't know about the supplier announcement that happened last week." What is the root cause, and what two architectural mechanisms resolve it?

> **Simple Explanation:** The model is like an expert who read everything up to a specific date and has been offline ever since. The answer is not to retrain the expert — that would take months and cost millions. The answer is to hand them a briefing document before each meeting, containing everything relevant that has happened since they went offline.
>
> **Detailed Answer:** The root cause is the model's **knowledge cutoff**. LLMs are trained on data with a specific end date; events after that date are unknown to the model. This is not a bug or a failure of the specific model — it's a fundamental property of every LLM. The two architectural mechanisms are: (1) **RAG (Retrieval-Augmented Generation)** — connect the model to a knowledge base that is kept current, and retrieve relevant information to include in the context on each query; (2) **Tool use / function calling** — for very recent structured information (stock prices, order status, announcements), allow the model to call a live API or database at inference time and incorporate the result. In both cases, the model itself doesn't need to be retrained; the system provides the current information to the model's context on each call.
>
> **Architecture Takeaway:** Never assume the model knows anything recent. For any enterprise application touching time-sensitive information (prices, policies, announcements, incidents), a live knowledge retrieval mechanism is not optional — it is a structural requirement.

---

**Question 2 — Context window cost and quality**

Your team is designing a document analysis system. The average document is 15,000 tokens. A developer proposes using the full document as context in every API call. What are the cost, latency, and quality implications — and what alternatives exist?

> **Simple Explanation:** Sending the entire document every time is like faxing a 200-page manual to a consultant for every question, even when the answer is in the first two pages. It's expensive, slow, and the consultant loses focus in the middle anyway. Smarter design sends them only the relevant pages.
>
> **Detailed Answer:** **Cost:** at 15K input tokens per call, and assuming Claude Sonnet pricing (£3/M), each call costs £0.045 on input alone. At 10,000 queries/day, that's £450/day = £13,500/month in input costs alone — before any output tokens. **Latency:** processing 15K tokens adds significant time-to-first-token; the model must process the entire input before producing its first output word. For interactive applications this is a user-experience problem. **Quality:** the "Lost in the Middle" effect is real — if the relevant passage is buried in the middle of a 15K-token document, the model attends less reliably to it compared to information near the start or end. **Alternatives:** (1) **RAG** — chunk the document, embed, retrieve only the 3–5 most relevant chunks per query, reducing input from 15K to ~2K tokens — 7× cost reduction, better latency, maintained quality for most queries. (2) **Document pre-processing** — summarise the document once and cache the summary; serve most queries against the summary, fall back to the full document only for detailed clause-level queries. (3) **Hybrid** — classify the query first (cheap, fast) and include the full document only for queries that genuinely require full-document context.
>
> **Architecture Takeaway:** Context window size is a cost and quality dial, not just a capability limit. Never default to "full document in context." Design explicitly for what context is required per query type, and measure the token cost before you commit to an architecture.

---

**Question 3 — Temperature misconfiguration**

A developer sets temperature=1.2 for a product data extraction pipeline that pulls SKU codes, prices, and category names from supplier invoices. Six months later, operations reports intermittent wrong prices in the system. What is the likely cause and what is the fix?

> **Simple Explanation:** Temperature > 1 is the "be creative" dial. For extraction there is no creativity to be done — the price is either right or wrong. You would never ask an accountant to "be creative" when copying figures from an invoice. Turn the creativity dial all the way down for any task that has a right answer.
>
> **Detailed Answer:** Temperature > 1.0 flattens the probability distribution — tokens with lower probability become more likely to be selected. For a data extraction task, this is directly harmful: the model may select incorrect field values (a wrong price, a different SKU), output inconsistent formats, or generate plausible-sounding but wrong data more frequently than it would at lower temperature. Extraction tasks require the model to pick the most probable (most accurate) token, every time, not to explore lower-probability alternatives. The correct setting is temperature = 0 (greedy decoding — always pick the highest-probability token) or very close to zero (0.0–0.1). The "intermittent" nature is characteristic of temperature-induced variance: most of the time the highest-probability token is correct, but occasionally the flattened distribution allows an incorrect token to win. Fix: set temperature = 0 on the extraction calls, run a retrospective evaluation pass on a sample of recent outputs, and add schema validation to catch format anomalies at the output boundary.
>
> **Architecture Takeaway:** Temperature is not set once and forgotten. Every AI pipeline component needs explicit temperature configuration matching its task type: 0–0.1 for extraction/classification, 0.3–0.7 for generation/summarisation. Default settings from SDK examples are often 0.7 or 1.0 — tuned for demos, not production extraction pipelines.

---

**Question 4 — Model selection cost-quality trade-off**

You are comparing two models for a classification task: Model A costs £0.15/M tokens and achieves 91% accuracy on your test set. Model B costs £3/M tokens and achieves 94% accuracy. The system processes 500K classifications/day at an average of 850 tokens per request. Which model should you use?

> **Simple Explanation:** The question is never "which model is better" in isolation. It is always "which model produces the best outcome per pound spent." A 3% accuracy improvement sounds small — but at 500K calls per day, 3% is 15,000 corrections per day. Whether those corrections are worth £1,200/day depends entirely on what those errors cost you in the real world.
>
> **Detailed Answer:** First, calculate actual costs. Per request: 850 tokens = 0.00085M tokens. **Model A:** £0.15 × 0.00085 × 500K = **£63.75/day = £1,912/month**. **Model B:** £3 × 0.00085 × 500K = **£1,275/day = £38,250/month**. Monthly cost difference: £36,338. The quality difference is 3 percentage points (91% vs 94%). At 500K/day, that's 15,000 additional correct classifications per day, or 450,000 per month. **The decision is: what does a misclassification cost?** If each incorrect classification costs £1 downstream (manual rework, wrong routing): Model B saves 450K × £1 = £450K/month in errors — easily justifies the £36K premium. If each incorrect classification costs £0.05 (minor inconvenience, auto-corrected downstream): Model B saves £22.5K but costs £36K extra — Model A wins. **Don't answer "use the cheaper model" or "use the better model" without this calculation.** Also consider: can you achieve 94%+ on Model A through better prompting or a hybrid escalation strategy (use Model A for high-confidence cases, escalate uncertain cases to Model B)?
>
> **Architecture Takeaway:** Define the cost-of-error for every AI pipeline before selecting a model. This is a business metric, not a technical one — it requires input from operations or product owners. Without it, model selection is guesswork. With it, it's an engineering calculation.

---

**Question 5 — Model version management**

A colleague proposes using the floating alias `gpt-4o` (which always points to the latest version) instead of a specific version string like `gpt-4o-2024-08-06`. They argue it means you automatically benefit from improvements. Do you agree, and how should this be handled in a production system?

> **Simple Explanation:** Using a floating alias is like subscribing to "whatever version of your ERP is released today" in production — without testing it first. You would never accept that for an SAP upgrade. Treat a model version change as a deployment event: it needs evaluation, testing, and a rollback plan.
>
> **Detailed Answer:** Disagree for production systems. Using the latest alias means model behaviour can change without any action on your part — when the provider releases a new version and updates the alias, your system silently starts using a different model. LLM outputs are probabilistic; even minor model changes can shift output distributions in ways that break downstream JSON parsing, violate format assumptions, alter tone or length, or change accuracy characteristics on your specific task. The risk is a silent production change that only surfaces in monitoring — potentially after thousands of affected requests. **Version pinning ensures:** (1) behaviour stability — the system behaves identically to how it did at last evaluation; (2) controlled upgrades — model version changes go through an evaluation gate before reaching production; (3) rollback — if a new version causes regressions, revert to the pinned version in a single config change. **Tradeoff:** you must track provider deprecation schedules and plan upgrade cycles. Most providers give 6–12 months of notice before retiring a specific version. This is standard dependency management overhead. **Valid use of floating aliases:** in development/staging environments or personal tools where stability is not critical and getting improvements automatically is desirable.
>
> **Architecture Takeaway:** Model version is a production dependency, not a configuration detail. Add it to your dependency management process: pin in production, track deprecation notices on a calendar, treat model upgrades as minor deployments with their own evaluation gate.

---

## 8. Advanced Deep Dive

> **Optional depth** — Section 8.1 covers attention mathematics which requires comfort with matrix notation. If you prefer to skip the math, jump directly to **8.2 (Scaling Laws)** and **8.3 (Tokenisation Edge Cases)** which are practical and do not require mathematical background.

### 8.1 Attention Math: A Concrete 3-Token Walkthrough

> **Explain Like I'm an Architect — Q/K/V Attention**
> Think of Q/K/V like a corporate directory search. Every word (token) in a sentence has three things: a **search query** (Q — what this word is looking for right now to understand itself), a **business card headline** (K — the short summary of what this word offers to others), and a **full CV** (V — the complete information this word can contribute). When the word "bank" wants to know whether it means "river bank" or "financial bank", it broadcasts its search query and checks every other word's business card headline. Whoever scores highest on the match gets their full CV pulled in. That weighted blend of CVs becomes the word's updated meaning, carrying context forward into the next layer. Run this process for every word simultaneously — in parallel — across 80-plus layers, and you get a model that deeply understands context across an entire document.
>
> **Why this matters architecturally:** You do not need to memorise the formula. What you need to know is that attention is the mechanism that lets the model connect "it" to "the animal" three sentences earlier, or connect "bank" to "river" from context. The quality of this mechanism is why transformer-based models outperform everything that came before — and why the size of the context window (how much text the model can hold in working memory) is a primary cost and capability variable in your architecture decisions. The math below is just this mechanism expressed as matrix multiplication — you can read it or skip it.

For those who want to understand what happens inside each Transformer layer:

Given input tokens ["The", "cat", "sat"], the attention mechanism computes:

**Step 1: Project each token vector into Query (Q), Key (K), Value (V) vectors**
Each token gets three learned projections:
- Q: "what am I looking for?"
- K: "what do I contain?"
- V: "what information do I contribute?"

**Step 2: Compute attention scores**
```
Score(token_i, token_j) = Q_i · K_j / √d_k

For "sat" attending to all tokens:
  sat→The:  Q_sat · K_The  / √d_k = some score
  sat→cat:  Q_sat · K_cat  / √d_k = some score
  sat→sat:  Q_sat · K_sat  / √d_k = some score
```

**Step 3: Softmax to normalise scores to probabilities**
```
Attention weights = softmax([score_sat→The, score_sat→cat, score_sat→sat])
                  = e.g., [0.1, 0.7, 0.2]
```
"sat" attends most strongly to "cat" (0.7 weight) — it needs to know who sat.

**Step 4: Weighted sum of Value vectors**
```
Output_sat = 0.1 × V_The + 0.7 × V_cat + 0.2 × V_sat
```
The output vector for "sat" now contains information from "cat" — capturing the subject-verb relationship.

**Multi-head attention** runs this process in parallel with H different Q/K/V projection matrices, each learning to attend to different aspects of the relationship (syntax, semantics, co-reference). The outputs of all heads are concatenated and projected.

**Why this matters architecturally:** attention is O(n²) in sequence length — doubling the context window quadruples the compute. This is why Flash Attention (a memory-efficient attention implementation) is critical for long contexts, and why very long context windows are expensive.

### 8.2 Scaling Laws: What They Tell Architects

Scaling laws (Kaplan et al., 2020; Hoffmann et al., 2022 "Chinchilla") describe how model quality improves with scale:

- **Model quality scales predictably** with the number of parameters, training tokens, and compute budget — roughly as power laws
- **Chinchilla scaling:** for a given compute budget, the optimal model is smaller and trained on more data than previous models. Llama-3 70B outperforms earlier 175B models partly because it was trained on 15 trillion tokens (vs 1T for earlier models)
- **The implication for architects:** "bigger model = better" is not always true. A well-trained 8B model on the right data can outperform a poorly-trained 70B model on specific tasks. Benchmark scores on a *specific task* matter more than parameter count.

What scaling laws don't tell you: they describe average performance across benchmarks. Your specific task may not follow the average. Always evaluate on your task.

### 8.3 Tokenisation: Practical Edge Cases

Tokenisation affects cost and context window consumption in non-obvious ways:

- **Code** tokenises efficiently (keywords and symbols are common tokens)
- **Non-English languages** often tokenise less efficiently — Japanese, Arabic, and Chinese may use 3–5× more tokens per word than English
- **Numbers** tokenise inconsistently — "2024" might be 1 token, "20240921" might be 4 tokens
- **Special characters, emojis, rare symbols** often require multiple tokens per character
- **Repeated whitespace or formatting** consumes tokens without semantic content
- **Tables and structured data** in plain text are often inefficient — each cell, separator, and newline consumes tokens

Rule of thumb for cost estimation: 1 token ≈ 0.75 English words ≈ 4 characters. For non-English or technical content, measure empirically with the provider's tokeniser.

---

## 9. Key Takeaways (5 Bullets)

- **An LLM generates plausible continuations, not verified facts — this is architectural, not a defect.** The model predicts what text should come next based on patterns learned during training. Hallucination is an inherent consequence of this design. Systems must be architected to verify, ground, and constrain model outputs rather than trusting them uncritically.

- **Model selection is a cost-quality-latency engineering decision, not a vendor preference.** The 2026 landscape has a 50× cost range from efficient Tier 3 models to frontier Tier 1 models. Match model capability to task requirements: Tier 3 for classification and extraction, Tier 2 for general generation, Tier 1 only when complex reasoning is genuinely required. Always evaluate on your specific task before committing.

- **Context window = working memory — everything the model knows must be in the prompt.** LLMs are stateless between calls. There is no persistent memory, no session state, no background knowledge of your previous interactions unless you put it in the context. This drives RAG architecture, conversation history management, and document handling strategies.

- **Temperature is the single most impactful configuration parameter for output consistency.** Temperature = 0 for extraction, classification, and structured output. Temperature 0.3–0.7 for conversational and generative tasks. Temperature > 1.0 is almost never appropriate for enterprise production systems. Getting this wrong silently degrades output quality at scale.

- **Pin model versions in production — never use a floating alias.** Model providers update aliases (like `gpt-4o`) to new versions without warning. A provider-side model update can change output distributions, break format assumptions, and introduce silent regressions. Version-pin all production API calls and treat model version changes as a deployment event requiring evaluation gates.
