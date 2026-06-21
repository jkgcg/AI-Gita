# AI Gita — Platform Glossary
### 20 terms that recur across multiple learning modules

> These terms appear throughout the platform. If you encounter one before it's explained in a module, this is the place to look. Each definition is written for Solution Architects and Enterprise Architects — not for ML engineers.

---

## A

**Autoregressive**
A generation strategy where each word (token) is produced one at a time, with each new word depending on everything that came before it. All the text-generating AI you interact with (ChatGPT, Claude, Gemini) works this way. You don't need to understand the mechanics — what matters is that it means the model cannot "go back and edit" what it already generated, which is why prompts need to be precise upfront.

---

## B

**BM25**
A keyword-matching algorithm used in search systems. It scores documents by how many times your search terms appear in them, weighted by rarity (rare words score higher). In AI systems, BM25 is often combined with semantic (vector) search to get the best of both: exact term matching for product codes, identifiers, and names, plus meaning-based matching for conceptual queries. You will encounter it in RAG and search architecture discussions. *See also: RAG, Vector search.*

---

## C

**Context window**
The "working memory" of a language model — everything the model can see and process in a single conversation or API call. If you send a 10-page document plus a question, all of that counts against the context window limit. Once the limit is exceeded, the model cannot access the earlier content. Context windows are measured in tokens (roughly ¾ of a word each). GPT-4o's window is around 128,000 tokens (~100 pages); Claude's is up to 200,000 tokens. Architects care about this because it directly affects cost, latency, and what architectures are feasible (RAG vs long-context). *See also: Token, RAG.*

**Cross-encoder reranker**
A model that takes a query and a candidate document together and produces a single relevance score. This is more accurate than fast vector search but much slower. In a RAG pipeline, a cross-encoder is typically applied to the top 20–50 candidates from vector search to rerank them more precisely before sending the best 3–5 to the language model. Think of it as a specialist reviewer who carefully reads both the question and each answer before deciding which is most relevant — you wouldn't ask them to read 10,000 answers, but the top 20 is feasible. *See also: RAG, BM25.*

---

## D

**DPA (Data Processing Agreement)**
A legally binding contract between an organisation and a vendor specifying how personal data will be handled, stored, and protected. Required under GDPR when personal data is processed by a third party (including a cloud AI provider). Enterprise architects must ensure a signed DPA is in place before sending any personal data to an AI API. Not signing one is a GDPR violation, not just a risk — it is an immediate compliance failure.

---

## H

**HITL (Human-in-the-Loop)**
A design pattern where a human approves, reviews, or overrides an AI decision before it becomes an action. The degree of HITL ranges from full automation (AI acts without review) to full human control (AI only proposes, human always decides). Architects design HITL gates by risk level: a customer email draft may need no approval; a £50,000 refund or a contract amendment requires human sign-off. *See also: Blast radius, Governance tiers.*

---

## I

**i.i.d. (independently and identically distributed)**
A statistical assumption that each data point was drawn randomly from the same distribution, with no relationship between points. Most classical machine learning algorithms assume i.i.d. data. Time series data violates this (tomorrow's sales depend on today's). This matters architecturally when you choose the wrong model family for a problem — using an i.i.d.-assuming model for a forecasting problem will produce misleading results regardless of how much data you have. *See also: ML Fundamentals, RecSys/TS/Tabular.*

---

## L

**LLM judge (LLM-as-judge)**
A quality evaluation pattern where a second language model call is used to score the output of the first. Instead of checking whether the output exactly matches an expected string (which fails for generated text), you ask a capable model: "Given this question, does this answer correctly address it? Rate 1–5." LLM judges are used in evaluation harnesses, regression testing, and production quality monitoring. They are not perfect (they can be fooled), but they scale far better than human review for large output volumes. *See also: Evaluation harness.*

---

## M

**MCP (Model Context Protocol)**
An open protocol (published by Anthropic, 2024) that standardises how AI agents connect to external tools and data sources. Before MCP, every agent system had its own bespoke integration layer. MCP provides a standard interface: a server exposes capabilities, an agent queries them using a common protocol. Architecturally it is analogous to what REST did for web APIs — not the only way to do it, but rapidly becoming the standard way. Enterprise architects should treat MCP as they would any integration standard: assess adoption, compliance requirements, and vendor support before committing.

---

## O

**OTel / OpenTelemetry**
An open-source industry standard for collecting observability data (traces, metrics, and logs) from distributed systems. If you have distributed systems monitoring in your enterprise stack, your platform almost certainly ingests OTel data — tools like Datadog, Grafana, Dynatrace, and Azure Monitor all support it. AI-specific extensions to OTel (called "GenAI semantic conventions") add standard attributes for LLM traces: model name, token counts, prompt/completion text, latency. This means your existing observability infrastructure can monitor AI systems with minor instrumentation rather than requiring a separate AI monitoring stack.

---

## Q

**QLoRA**
A memory-efficient variant of fine-tuning that combines quantisation (reducing model weight precision to use less GPU memory) with LoRA (training only a small set of added parameters, not the full model). In practice: fine-tuning a 70-billion-parameter model normally requires 8–10 A100 GPUs; QLoRA can do it on a single A100 or even a consumer GPU. Architects encounter QLoRA when evaluating whether self-hosted fine-tuning is feasible vs. using a managed fine-tuning service. You do not need to implement it — you need to know it is the standard technique for cost-effective fine-tuning of large open-weight models. *See also: Fine-tuning, LoRA.*

---

## R

**RAG (Retrieval-Augmented Generation)**
An architecture pattern where a language model is given relevant documents retrieved from a knowledge base at query time, rather than relying solely on what it learned during training. This solves the knowledge cutoff problem (the model only knows facts up to its training date) and the hallucination risk for specific factual queries (the model answers from retrieved evidence rather than from memory). The three components are: a retrieval system (usually vector search + keyword search), an injection mechanism (retrieved text is added to the prompt), and the language model. RAG is the standard pattern for enterprise knowledge assistants, document Q&A, and any system where fresh, organisation-specific information is needed. *See also: Vector search, Context window.*

**RLHF (Reinforcement Learning from Human Feedback)**
A training technique used to align language models with human preferences. After initial training on text, the model is shown pairs of outputs and human raters indicate which is better. A "reward model" learns to predict human preference, and the language model is then trained to produce outputs that score highly on this reward model. All major frontier models (GPT-4, Claude, Gemini) use some form of RLHF or its variants (RLAIF, DPO, Constitutional AI). As an architect, you encounter RLHF when: evaluating whether a vendor's safety claims are substantiated; understanding why model behaviour changed between versions; or designing a fine-tuning project that aims to change behaviour rather than add knowledge. *See also: Fine-tuning.*

---

## T

**Token**
The unit of text that a language model processes. Roughly ¾ of an English word — so "architect" is one token, "Hello, world!" is three tokens. API pricing is per token (input tokens + output tokens). Context window limits are in tokens. Long documents cost more to process. Short, precise prompts cost less. Architects need token awareness for cost modelling, latency budgeting, and context window architecture decisions. A rough rule: 1,000 tokens ≈ 750 words ≈ 1.5 pages of text.

---

## V

**Vector search / Semantic search**
A search technique where text (or images) is converted into a list of numbers (a "vector" or "embedding") that encodes its meaning. Two pieces of text with similar meaning will have vectors that are close together in mathematical space, even if they share no exact words. This enables search-by-meaning: "what are your return policies?" finds "customers may exchange items within 28 days" even though no query words appear in the document. Vector search is the retrieval mechanism inside RAG systems and powers semantic similarity calculations. *See also: RAG, BM25, Embedding.*

---

## Abbreviations Quick Reference

| Term | Full form | Where defined above |
|---|---|---|
| BM25 | Best Match 25 (retrieval algorithm) | ↑ B |
| DPA | Data Processing Agreement | ↑ D |
| HITL | Human-in-the-Loop | ↑ H |
| i.i.d. | Independently and identically distributed | ↑ I |
| LLM | Large Language Model | See LLMs module |
| MCP | Model Context Protocol | ↑ M |
| OTel | OpenTelemetry | ↑ O |
| QLoRA | Quantised Low-Rank Adaptation | ↑ Q |
| RAG | Retrieval-Augmented Generation | ↑ R |
| RLHF | Reinforcement Learning from Human Feedback | ↑ R |

---

*This glossary covers cross-platform terms. Each learning module also defines topic-specific terms inline at point of first use.*
