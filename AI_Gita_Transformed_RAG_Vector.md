# RAG & Vector Search — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

Every LLM has a knowledge cutoff — a date after which it knows nothing. GPT-4o's training ended in early 2024. It doesn't know about your company's products, your internal policies, last quarter's results, or the contract your legal team signed yesterday.

**RAG (Retrieval-Augmented Generation)** solves this. Instead of expecting the model to "know" your information, you retrieve the relevant pieces of information at query time and hand them directly to the model as context. The model reads the retrieved information and answers from it — not from its training weights.

The name explains the pattern:
- **Retrieval** — find the most relevant documents or passages for the query
- **Augmented** — add those passages to the context before asking the model
- **Generation** — the model generates its answer grounded in what was retrieved

**Vector search** is the retrieval mechanism that makes this work at scale. Rather than matching keywords, it converts text into numerical vectors (embeddings) that capture semantic meaning — so "What is your returns policy?" and "How do I send something back?" find the same documents, even though they share no words.

RAG is the single most widely deployed AI pattern in enterprise in 2026. If you're integrating AI into a system that needs to answer questions about your organisation's information — products, policies, contracts, knowledge base, support history — RAG is almost certainly the right starting point.

---

## 2. Why Should I Care

### For Solution Architects

RAG changes the integration model for AI completely. Without RAG, the model's knowledge is fixed at training time — you can't update it without retraining, which is expensive and slow. With RAG, the model's effective knowledge is your retrieval index — which you can update instantly by updating the documents in the index.

The decisions you need to make when designing a RAG system:

- **What goes in the index?** Product catalogues, policy documents, support ticket history, contracts, FAQs — all are candidates. But each has different freshness requirements, different sensitivity levels, and different chunking challenges.
- **How fresh does it need to be?** A nightly index refresh is cheap and simple. Near-real-time indexing (document changed → available for retrieval in minutes) requires an event-driven pipeline and is significantly more complex.
- **What retrieval quality is good enough?** If your retriever misses the right document 20% of the time, 20% of your AI answers will be wrong or hallucinated — regardless of how good the LLM is. Retrieval quality is the ceiling on answer quality.
- **RAG or long context?** For small, stable document sets (< 50K tokens), stuffing everything into context is simpler. For large, changing, or sensitive document sets, RAG is almost always better.

### For Enterprise Architects

RAG is where AI meets your knowledge architecture. The decisions your organisation has already made — how documents are stored, how they're structured, who can access what, how they're versioned — all directly affect the quality of a RAG system built on top.

Three enterprise-wide implications:

1. **Knowledge quality is AI quality.** If your internal documentation is inconsistent, outdated, or poorly structured, your RAG system will retrieve and surface that inconsistency, outdatedness, and poor structure — at scale, to every user. RAG is a forcing function for knowledge management improvement.

2. **Access control surfaces in retrieval.** A RAG system that retrieves documents from a shared knowledge base must enforce the same access controls that governed direct document access. A user who can't see a confidential policy document shouldn't get answers based on it. This is a retrieval design problem, not just an application security problem.

3. **PII and sensitive data flow through the LLM.** Every retrieved document chunk passes through the LLM context window. If your documents contain PII, trade secrets, or commercially sensitive data, you need a data handling strategy at the retrieval boundary — not just at the application layer.

---

## 3. Think About It Like This (Analogy)

**The Open-Book Exam Analogy**

Imagine two ways to sit an exam:

**Closed-book (standard LLM):** The student memorises everything during training. On exam day, they answer entirely from memory. They're very good at things they studied intensively. But if the exam includes questions about events that happened after they stopped studying, or about your company's specific internal processes, they're guessing.

**Open-book (RAG):** The student walks in with a well-organised reference library. When a question comes up, they scan the index, find the relevant pages, read them, and write their answer based on what's in front of them. They don't need to have memorised your specific policies — they look them up. The quality of their answer depends on two things: how well-organised the library is (retrieval quality) and how well they can synthesise what they read (LLM quality).

**The vector search part:** in a traditional library, you search by keyword — you know the exact term to look up in the index. Vector search is like a librarian who understands what you mean, not just what you said. You ask "what's the rule about returning damaged goods?" and the librarian retrieves the relevant policy section even though it's titled "Product Return Conditions" and doesn't contain the word "damaged."

**The enterprise insight:** the quality of the open-book exam is only as good as the library. A disorganised library with outdated books produces bad answers, even with a brilliant student. Investing in knowledge quality — clean documents, consistent structure, regular updates — is investing in RAG quality.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 The RAG Pipeline: End to End

The production RAG pipeline has two phases — build time (happens once, or on a schedule) and query time (happens on every user request):

**Build time — indexing pipeline:**
```
Document sources (SharePoint, Confluence, PDFs, databases)
    │
    ▼
Document ingestion
  → format normalisation (PDF → text, HTML → text)
  → metadata extraction (title, author, date, category, access level)
    │
    ▼
Chunking
  → split documents into retrievable segments
  → target: 300–800 tokens per chunk, with overlap
    │
    ▼
Embedding
  → each chunk → embedding model → dense vector (e.g., 1536 dimensions)
    │
    ▼
Indexing
  → vectors stored in vector database (Pinecone, Weaviate, pgvector, Qdrant)
  → metadata stored alongside for filtering
  → BM25 index built for keyword search (a keyword relevance algorithm — explained in Section 4.3)
```

**Query time — retrieval and generation pipeline:**
```
User query
    │
    ▼
Query embedding
  → same embedding model as indexing
    │
    ▼
Hybrid retrieval (semantic + keyword)
  → vector search: top-K semantically similar chunks
  → BM25 search: top-K keyword-matching chunks
  → RRF fusion: merge and re-score the two result sets
    │
    ▼
Reranking
  → cross-encoder reranker (a precision reranker — explained in Section 4.4) scores each retrieved chunk
    against the query for precision
  → top 3–5 chunks selected
    │
    ▼
Context assembly
  → retrieved chunks formatted and injected into the prompt
  → source metadata included for citation
    │
    ▼
LLM generation
  → model answers from the retrieved context
  → instructed to cite sources and say "I don't know" if
    context is insufficient
    │
    ▼
Output + citations → user
    │
    ▼
Evaluation (async, on sample)
  → RAGAS or LLM judge scores answer quality
```

**The 2026 production standard:** hybrid retrieve → rerank → generate → evaluate. Any simpler pipeline (semantic-only retrieval, no reranking, no evaluation) is leaving quality on the table.

### 4.2 Chunking Strategy: Why It Matters

A chunk is the unit of retrieval — the piece of text that gets stored as a vector and retrieved as a result. Getting chunking right is one of the highest-leverage decisions in a RAG system.

**Why chunking matters:**
- Too small: each chunk lacks context. "The penalty is 2% of order value" retrieved without knowing what penalty or what condition triggers it is useless.
- Too large: each chunk contains multiple topics. Retrieving a 2,000-token chunk because one sentence is relevant means the model gets 1,900 tokens of noise. This inflates cost and can confuse the model.
- Wrong boundaries: splitting a document at page boundaries may split a sentence across chunks. Splitting a table by row may split header context from data rows.

Think of chunking like copying pages from a reference manual: you could copy it page-by-page (small chunks, high granularity) or chapter-by-chapter (large chunks, more context per piece). Too small and you lose context; too large and retrieval becomes imprecise. The right chunk size depends on how your users ask questions.

**Five chunking strategies:**

| Strategy | How it works | Best for |
|---|---|---|
| **Fixed-size with overlap** | Split at N tokens, overlap by M tokens | Simple documents, consistent prose, fast to implement |
| **Sentence-based** | Split at sentence boundaries, group into chunks of ~N tokens | Conversational text, FAQs, where sentence integrity matters |
| **Semantic chunking** | Embed sentences, split where embedding similarity drops (topic change) | Mixed-topic documents, research papers, policy documents |
| **Hierarchical (parent-child)** | Store both large "parent" chunks and small "child" chunks; retrieve by child but return parent for context | Long structured documents where local context is small but surrounding context matters |
| **Document-structure-aware** | Split by markdown headers, HTML sections, PDF headings | Structured documents (wikis, technical docs, contracts with sections) |

**The overlap trick:** when splitting at fixed size, include the last 10–20% of the previous chunk at the start of the next. This ensures that a concept mentioned at the end of one chunk is also findable from the next chunk's query — preventing boundary miss.

**Practical guidance for architects:**
- For a pilot: start with fixed-size (512 tokens, 50-token overlap). It's imperfect but implementable in a day.
- For production: invest in document-structure-aware chunking for your primary document types. The quality improvement is significant, especially for policy and process documents.
- Review chunking quality by inspection: take 20 random chunks and ask "is this a self-contained unit of information?" If the answer is often no, your chunking strategy needs adjustment.

### 4.3 Hybrid Search: Why You Need Both Semantic and Keyword

**Semantic search (vector similarity)** finds documents that mean the same thing as the query, regardless of exact wording. It handles synonyms, paraphrases, and conceptual similarity. "How do I return a product?" finds "Product Return Conditions."

**Keyword search (BM25)** finds documents that contain the exact terms in the query. It handles proper nouns, product codes, technical terms, and jargon that semantic search often misses. "Return policy for SKU-ABC123" finds documents containing "SKU-ABC123."

> **Explain Like I'm an Architect**
>
> Think of two types of librarians:
>
> **Librarian A (semantic search)** understands what you mean. You ask "how do I get my money back?" and they bring you everything related to refunds, returns, and cancellations — even though you never said those words. But if you ask for "document reference SK-7723-B", they look confused — that specific code doesn't connect to anything meaningful in their mental map of the library.
>
> **Librarian B (BM25 keyword search)** is a precise index reader. They find exactly what contains the words you wrote. "SK-7723-B"? Found it immediately. But ask them "how do I get my money back?" and they'll hand you only documents with the exact phrase "money back" — missing anything titled "Refund Policy" or "Return Conditions."
>
> You need both librarians working together. For conceptual questions, Librarian A wins. For exact terms, codes, and jargon, Librarian B wins. RRF fusion (described below) is the mechanism that merges both their answers into one ranked list.

**Why you need both:**

| Query type | Semantic handles it? | BM25 handles it? |
|---|---|---|
| Conceptual: "How do I get a refund?" | ✅ | ❌ (word mismatch) |
| Exact term: "SKU-ABC123 return" | ❌ (rare term, may not embed well) | ✅ |
| Mixed: "How do I return SKU-ABC123?" | Partial | Partial |
| Typo: "retrun policy" | ✅ (embedding robust to typos) | ❌ (exact match fails) |
| Acronym: "What is the OMS integration spec?" | ❌ (OMS may not embed distinctively) | ✅ |

**Neither alone achieves the quality of both together.**

**Reciprocal Rank Fusion (RRF)** is the standard algorithm for merging the two result sets:

```
For each document d in the combined result set:
  RRF_score(d) = Σ 1 / (k + rank(d, result_set_i))
  
where k = 60 (empirically tuned constant)
      rank(d, result_set_i) = rank of d in each individual result set
```

RRF gives high combined scores to documents that rank highly in both result sets — and reasonable scores to documents that rank highly in only one. It's parameter-free and robust across different retrieval configurations.

### 4.4 Reranking: Precision After Recall

Retrieval optimises for **recall** — get the right document in the top-K results, even if some noise comes with it. Reranking optimises for **precision** — from those top-K results, identify the 3–5 that most precisely answer the query.

> **Explain Like I'm an Architect**
>
> Retrieval is a net cast wide — its job is to ensure the right documents are somewhere in the top-20 results, even if some irrelevant ones come along too. It's fast (milliseconds across millions of documents) but coarse.
>
> Reranking is a careful second opinion — it takes those top-20 candidates and reads each one properly against the specific question, producing a fine-grained relevance score. It's slow (150ms across 20 documents) but precise.
>
> The analogy: think of hiring for a senior role. Retrieval is your recruiter screening 500 CVs to a shortlist of 20 that roughly match the job spec. Reranking is the hiring manager reading all 20 CVs carefully and picking the 5 to interview. You need both steps. If the recruiter misses the best candidate (recall failure), the hiring manager never sees them. If the hiring manager picks randomly from the 20 (no reranking), you get a suboptimal hire despite having the right candidates available.
>
> **Common Misconception:** "Better embedding models remove the need for reranking." Embedding models produce a single vector per document — they compress a whole passage into coordinates. Rerankers read the full text of the query and document together, scoring their interaction directly. They're structurally more precise; no embedding model fully replaces them for high-stakes retrieval.

**Why not just use retrieval for both?**

Vector search uses dot product or cosine similarity between two vectors — fast (milliseconds for millions of documents) but coarse. A **cross-encoder reranker** takes the query and each candidate document together, runs them through a model jointly, and produces a fine-grained relevance score. Much more precise, but too slow to run on millions of documents — so you run it only on the top 20–50 retrieval results.

```
Vector search: 10M documents → top 50 in 50ms
Cross-encoder reranker: top 50 → top 5 in 150ms
LLM generation: top 5 chunks as context → answer
```

**When reranking matters most:**
- Queries where multiple documents are superficially similar but only one is actually relevant
- Multi-hop questions where the relevant chunk needs to match the full question, not just part of it
- High-precision domains (legal, medical, compliance) where retrieval noise in the context causes hallucination

**Popular reranker models:** Cohere Rerank, BGE Reranker, Jina Reranker. All expose an API or can be self-hosted.

### 4.5 RAG Evaluation: Measuring What Actually Matters

> **Explain Like I'm an Architect**
>
> RAG quality is easy to measure wrong. The naive approach is to ask users "is the answer good?" — but users can only evaluate the final output, not whether the retrieval was correct or whether the model faithfully used what it retrieved. These failures look similar to users but require completely different fixes.
>
> Imagine a restaurant where dishes are sometimes wrong. You could measure customer satisfaction (end-to-end quality). But if the kitchen is sometimes sending wrong ingredients to the chef, and the chef is sometimes using the right ingredients to make the wrong dish, and the waiter is sometimes serving the right dish to the wrong table — these are three independent failure points requiring three independent fixes. Measuring only customer satisfaction tells you something is wrong but not where.
>
> RAG has the same structure: retrieval can fail (wrong documents fetched), faithfulness can fail (model ignores what was retrieved), and relevance can fail (answer doesn't address the question). Measure all three independently so you know where to invest your optimisation effort.

RAG quality breaks down into three independent dimensions that must all be measured:

**Dimension 1 — Retrieval quality**
Did the retriever find the right documents?
- **Recall@K**: of the relevant documents, what fraction were in the top K results?
- **Precision@K**: of the top K results, what fraction were actually relevant?
- **MRR (Mean Reciprocal Rank)**: how highly was the first relevant document ranked on average?

**Dimension 2 — Answer quality given the retrieved context**
Given what was retrieved, did the model produce a good answer?
- **Faithfulness (RAGAS)**: is every claim in the answer supported by the retrieved context? (Measures hallucination)
- **Answer relevance (RAGAS)**: does the answer address the question that was asked? (Measures instruction following)

**Dimension 3 — End-to-end quality**
Does the full pipeline produce answers that are useful to users?
- **Context relevance (RAGAS)**: are the retrieved chunks actually relevant to the question? (Measures retrieval precision)
- **Human evaluation**: for a sample of queries, do actual users find the answer correct and complete?

**RAGAS** (Retrieval-Augmented Generation Assessment) is the open-source framework that automates measurement of faithfulness, answer relevance, and context relevance using an LLM judge. It produces a score between 0 and 1 for each dimension.

**The failure mode quadrant — what goes wrong and where:**

| Symptom | Likely cause | Fix |
|---|---|---|
| Correct topic, wrong detail | Retrieval precision problem — right document, wrong chunk | Improve chunking or reranking |
| Completely off-topic answer | Retrieval recall problem — wrong documents retrieved | Improve embedding model or add keyword search |
| Answer contradicts retrieved content | LLM faithfulness failure — model ignores context | Stronger grounding instruction; faithfulness guardrail |
| Answer is vague / non-committal | Retrieved content insufficient | Expand knowledge base; improve document coverage |
| Correct answer, wrong citation | Metadata problem — chunks not tagged with source correctly | Fix metadata pipeline |

### 4.6 RAG in 2026: What Changed

> **Optional depth** — These are advanced variants used once a baseline RAG pipeline is running well. If this is your first RAG system, note the section titles and return here later. The core pipeline from Sections 4.1–4.5 is what you need first.

The basic RAG pattern (embed → store → retrieve → generate) has been extended significantly since the original 2020 paper. Here's what the production landscape looks like in 2026:

**Late interaction models (ColBERT / ColPali)**
Instead of a single vector per document, late interaction models store a vector for every token in the document. At query time, each query token scores against each document token, and the final relevance score is the sum of max-similarity scores. Much higher precision than bi-encoder models — at the cost of larger index size.
Use when: precision is critical and you can afford 10–20× the storage.

**GraphRAG**
Microsoft's extension adds a knowledge graph extraction step: before indexing, an LLM extracts entities and relationships from all documents and builds a graph. Queries can traverse the graph before retrieval — enabling multi-hop reasoning ("what are the dependencies of the system that processes returns?") that vector similarity alone cannot handle.
Use when: your knowledge base has dense entity relationships and users ask multi-hop questions.

**HyDE (Hypothetical Document Embedding)**
Before searching, generate a hypothetical answer to the query using the LLM, then use the hypothetical answer's embedding to search — instead of the query's embedding. Works because the hypothetical answer looks more like the documents you want to retrieve than the short query does.
Use when: queries are short and retrieval recall is poor.

**Contextual retrieval**
Before chunking, use an LLM to prepend a brief context summary to each chunk: "This chunk is from the Returns Policy document, section 3, discussing conditions for refunds on perishable items." This dramatically improves retrieval precision because each chunk now carries its own context — it can be understood even without the surrounding document.
Use when: your documents have chunks that make sense in context but are ambiguous in isolation.

**Long context as RAG fallback**
For critical queries where RAG retrieval might miss something, use a two-stage approach: RAG for the fast path (95% of queries), long context for the escalation path (queries where the model's confidence in the retrieved context is low). This hybrid gives the cost efficiency of RAG with the coverage of long context for edge cases.

---

## 5. Enterprise Example

**Scenario: Product Knowledge RAG for a Retail Customer Service Platform**

Your retail organisation has 45,000 SKUs, 12 product category guides, a 180-page returns policy, carrier-specific shipping guides for 8 carriers, and a loyalty programme FAQ — all maintained in Confluence and SharePoint. Customer service agents spend 40% of their time searching for this information. You want to deploy a RAG-powered assistant that answers agent questions in real time.

**Index architecture decisions:**

| Content type | Chunking strategy | Refresh frequency | Access scope |
|---|---|---|---|
| Product specifications | Document-structure-aware (by attribute section) | Nightly (product data changes daily) | All agents |
| Returns policy | Semantic chunking (policy sections are variable length) | Weekly (policy changes monthly) | All agents |
| Carrier guides | Fixed-size with overlap (structured prose) | Monthly | Logistics-trained agents only |
| Loyalty FAQ | Sentence-based (Q&A pairs) | Weekly | All agents |

**Retrieval configuration:**

- Embedding model: text-embedding-3-large (OpenAI) — higher precision for product terminology
- Hybrid search: semantic (weight 0.7) + BM25 (weight 0.3) — heavier semantic weight because agents phrase queries conversationally, not with exact SKU codes
- Reranker: Cohere Rerank — reduced context noise from 20 candidate chunks to 5
- Top-K to reranker: 20; top-K to LLM: 5

**Access control implementation:**

Carrier guides are restricted to logistics-trained agents. Implementation: every chunk in the carrier guides index is tagged with `access_group: logistics`. Every retrieval query is filtered by the authenticated user's access groups — the metadata filter is enforced at the vector database query layer, not in application code.

```python
results = vector_db.query(
    embedding=query_embedding,
    filter={"access_group": {"$in": user.access_groups}},
    top_k=20
)
```

**Evaluation results at 8 weeks post-launch:**

| Metric | Week 1 | Week 8 | Target |
|---|---|---|---|
| Retrieval Recall@5 | 71% | 89% | > 85% |
| RAGAS Faithfulness | 0.81 | 0.93 | > 0.90 |
| RAGAS Answer Relevance | 0.76 | 0.88 | > 0.85 |
| Agent satisfaction (CSAT) | 3.4/5 | 4.2/5 | > 4.0/5 |
| Query resolution time | 45s → AI | 12s → AI | < 15s |

**What improved Recall@5 from 71% to 89%:**
- Week 2: added BM25 hybrid search (was semantic-only at launch) — +8% recall for SKU-specific queries
- Week 4: switched from fixed-size chunking to document-structure-aware for product specs — +6% precision, fewer irrelevant chunks in top-5
- Week 6: added contextual retrieval (LLM-prepended context summaries) for the returns policy — +4% on policy-related queries

**What improved RAGAS Faithfulness from 0.81 to 0.93:**
- Stronger grounding instruction in system prompt: "Answer only from the retrieved documents. If the answer is not in the documents, say 'I don't have information about that.'"
- Reduced top-K from 8 to 5 — fewer noise chunks reduced instances of the model synthesising across irrelevant context

---

## 6. Architecture Perspective

### RAG vs Fine-Tune vs Long Context: The Decision Matrix

This is the most common design decision architects face when deploying knowledge-based AI:

| Signal | RAG | Fine-tune | Long context |
|---|---|---|---|
| Knowledge changes frequently | ✅ Best | ❌ Expensive to update | ✅ If docs fit |
| Knowledge is large (> 200K tokens) | ✅ | ✅ | ❌ Cost-prohibitive |
| Need to cite sources | ✅ Native | ❌ Hard | ✅ If structured well |
| Domain language is highly specialised | ✅ + fine-tune | ✅ | ✅ |
| Low query volume, high value | ✅ or long context | ✅ | ✅ |
| High query volume, cost sensitive | ✅ | ✅ | ❌ |
| Cross-document reasoning | Partial (GraphRAG) | ✅ | ✅ Best |
| Data is sensitive / can't send to LLM | ✅ (retrieve only relevant) | ❌ (full corpus in training) | ❌ (full corpus in context) |

**Rule of thumb:** start with RAG. Add fine-tuning if domain language adaptation is needed. Add long context only for specific high-value, low-volume queries where cross-document reasoning matters. The most common production pattern is RAG + fine-tuning on domain language, not RAG vs fine-tuning.

### RAG Pipeline in Your Enterprise Architecture

```
Document Sources                    Query Path
(SharePoint, Confluence,       User / Agent query
 PDFs, databases)                     │
      │                               ▼
      ▼                        Query embedding
Ingestion pipeline                    │
(scheduled or event-driven)    Hybrid retrieval
      │                        (vector + BM25 + RRF)
      ▼                               │
Chunking + embedding           Reranking
      │                               │
      ▼                        Context assembly
Vector DB + BM25 index                │
(with access metadata)         LLM generation
      │                               │
      ▼                        Output + citations
Evaluation pipeline                   │
(RAGAS on sample)              Evaluation (async)
```

**Integration points with enterprise stack:**

| Component | Enterprise integration |
|---|---|
| Document sources | SharePoint connector, Confluence connector, S3 listener, database change feed |
| Identity / access | AAD groups → retrieval metadata filters; enforced at vector DB query layer |
| Observability | OTel traces per retrieval call; RAGAS scores in metrics pipeline; cost per query |
| Knowledge governance | Document freshness tracking; stale document alerting; content review workflow |
| Data residency | Vector embeddings are derived data, not raw PII — but check with legal; on-prem vector DB option if required |

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — Retrieval failure for exact terms**

Your knowledge assistant is returning correct-sounding but wrong answers for queries about product codes (e.g., "SKU-AB7723"). The product code is in your documents. What is the most likely retrieval failure, and how would you fix it?

> **Detailed Answer:** Product codes are rare tokens — they don't appear frequently enough in training data for an embedding model to represent them as semantically meaningful content. The embedding vector for "SKU-AB7723" doesn't sit in a meaningful position in semantic space relative to other product-related concepts. Vector similarity search will not reliably surface documents containing that exact code. This is the classic failure mode of semantic-only retrieval for exact terms. Fix: add BM25 keyword search alongside semantic search (hybrid retrieval with RRF fusion). BM25 is exact-term matching — it will reliably find documents containing the literal product code. The hybrid approach handles both conceptual queries (semantic wins) and exact-term queries (BM25 wins).
>
> **Simple Explanation:** Semantic search finds things by meaning. A product code like "SKU-AB7723" has no inherent meaning — it's just an arbitrary string. Semantic search doesn't know what to do with it. You need a second retrieval method that does exact string matching. That's BM25 — the "Ctrl+F" of the retrieval world.
>
> **Architecture Takeaway:** Semantic-only retrieval is insufficient for any knowledge base containing product codes, reference numbers, order IDs, technical standards, or any domain-specific identifiers. Hybrid search (semantic + BM25 + RRF) is the production standard, not an optimisation — plan for it from day one.

---

**Question 2 — Retrieval vs generation failure diagnosis**

A business stakeholder says "the AI gave wrong information about our returns policy — it said the return window is 14 days but it's 30 days." Walk through the diagnostic steps to identify whether this is a retrieval problem or a generation problem.

> **Detailed Answer:** The diagnostic splits into two branches. First, run the same query through the retrieval pipeline in isolation and inspect the top-5 retrieved chunks. (1) **If the correct 30-day policy is NOT in the top-5**: retrieval failure. The retriever failed to surface the right section. Investigation: is the returns policy document in the index? Was the relevant chunk created correctly (did a boundary split the key sentence)? Check retrieval recall metrics. Fix: improve chunking, add BM25 if semantic alone is missing it, review index freshness. (2) **If the correct 30-day policy IS in the top-5**: generation failure. The model ignored or misread the retrieved context. Investigation: check RAGAS faithfulness — is the model grounding its answer in the retrieved content? Check whether another retrieved chunk contained a 14-day figure (perhaps an old version of the policy still in the index — two contradictory chunks confuse the model). Fix: remove stale document versions; add stronger grounding instruction ("answer only from retrieved context, prefer the most recent document if dates conflict"). The distinction is critical because retrieval failures and generation failures have completely different fixes.
>
> **Simple Explanation:** Before blaming the AI for being "wrong," find out at which step it went wrong. Did it find the right answer and then ignore it? Or did it never find the right answer in the first place? The diagnostic is to check what was retrieved. If the right document was there and ignored, that's a generation problem. If it wasn't there, that's a retrieval problem.
>
> **Architecture Takeaway:** Always build a retrieval inspection tool into your RAG system. You need to be able to see, for any query, exactly what the top-5 retrieved chunks were. Without this, every quality investigation is guesswork. The tool that shows you "what was retrieved" is as important as the tool that generates the answer.

---

**Question 3 — Chunk size tradeoffs**

Your team is debating whether to use 256-token chunks or 1024-token chunks for your product specification knowledge base. What are the tradeoffs and what would you recommend?

> **Detailed Answer:** 256-token chunks are small and precise — each retrieved chunk is focused, with less noise per result, better for queries needing a specific fact. But product specifications have attributes that depend on each other for meaning ("operating temperature: -10°C to 60°C" without knowing which attribute this is becomes meaningless). Small chunks risk splitting related attributes across boundaries. 1024-token chunks preserve more context per chunk — each retrieval result is more self-contained. But larger chunks mean more noise in the LLM's context (irrelevant attributes from the same spec alongside the one being asked about), increasing cost and potentially degrading focus. **Recommendation:** hierarchical (parent-child) chunking. Index small child chunks (256 tokens) for retrieval precision — these find the right product and the right section quickly. When returning context to the LLM, return the parent chunk (the full product specification section, ~1024 tokens) so the model has full surrounding context. The principle: retrieve small, generate with large. This is the highest-leverage chunking decision for structured product data.
>
> **Simple Explanation:** Small chunks are easy to find but hard to understand without context. Large chunks are easy to understand but harder to find precisely and contain more irrelevant content. The solution is to use small chunks as search targets but return large chunks as reading material — like using a precise index to find the right page, then reading the whole page.
>
> **Architecture Takeaway:** Chunk size is a retrieval precision vs context quality dial. For any knowledge base with structured documents (specifications, policies, contracts), invest in hierarchical chunking — it's a few days of implementation effort that pays off in significantly better retrieval precision and answer quality. Don't default to a single chunk size without evaluating on your actual document types.

---

**Question 4 — Event-driven indexing**

Six weeks after deploying your RAG knowledge assistant, a new product range is launched with 2,000 new SKUs. How would you ensure the assistant can answer questions about new products immediately, and what are the risks if the indexing pipeline isn't designed for this?

> **Detailed Answer:** The assistant can only answer questions about products that are in the index. If the indexing pipeline runs nightly on a schedule, there is a gap of up to 24 hours between product launch and assistant availability. For a product launch, 24 hours of "I don't have information about that" responses is a customer experience failure at exactly the highest-visibility moment. **Design requirements:** (1) Event-driven indexing — when a new product is added to the PIM/catalogue, trigger an ingestion event immediately; the product documentation is chunked, embedded, and indexed within minutes. (2) Deletion handling — when a product is discontinued, remove its chunks from the index atomically; stale chunks cause hallucination about discontinued products. (3) Version management — when a specification is updated, delete old chunks and add new ones atomically; partial updates leave contradictory information in the index. **Risks without event-driven indexing:** stale responses during launch day when accuracy matters most; outdated information persisting long after product changes; users losing trust in the assistant precisely when it needs to be most useful.
>
> **Simple Explanation:** A knowledge base that is only updated once a night is not a real-time knowledge base — it's a delayed snapshot. For a product catalogue assistant, "knowledge last updated last night" means customers asking about new products on launch day get "I don't know." Event-driven indexing means the knowledge base updates within minutes of changes. The architecture question is: does your indexing pipeline listen for change events, or does it only run on a schedule?
>
> **Architecture Takeaway:** Design your indexing pipeline for event-driven updates from day one, even if you start with scheduled batch ingestion. The decision to treat the knowledge base as append-only (batch) vs event-sourced (near-real-time) affects every downstream architecture decision: document store choice, deletion handling, conflict resolution, and latency SLAs. Retrofitting event-driven indexing after launch is significantly more expensive than designing for it upfront.

---

**Question 5 — RAGAS faithfulness**

What is RAGAS faithfulness, why is it the most important RAG quality metric for an enterprise deployment, and what score threshold would you set as a production gate?

> **Detailed Answer:** RAGAS faithfulness measures whether every factual claim in the model's answer is supported by the retrieved context. Score 1.0 = every claim traces back to a retrieved document. Score 0.7 = 30% of claims are not grounded in retrieved context — the model is either hallucinating or relying on its parametric training weights instead of the documents. For enterprise deployment, faithfulness is the most critical metric because it directly measures hallucination risk — the failure mode with the highest harm potential (wrong information delivered confidently to employees or customers). Other metrics (answer relevance, context relevance) measure whether you're asking the right questions of the right documents; faithfulness measures whether the model is actually using the answers it found. **Production thresholds:** ≥0.90 for general knowledge assistants; ≥0.95 for domains where accuracy is regulated or high-stakes (legal, compliance, medical, financial). Measurement: build a golden test set of 100–200 curated queries with known correct answers. In production, monitor RAGAS on a 10% random sample with automated scoring, alert when the rolling 7-day average drops below threshold.
>
> **Simple Explanation:** Faithfulness asks: "Did the model actually use the documents it retrieved, or did it make something up?" A model can retrieve the exact right document and then completely ignore it, producing a confident wrong answer from its training memory instead. Faithfulness catches this. It's the metric that most directly measures the hallucination risk you're governing.
>
> **Architecture Takeaway:** Set a faithfulness threshold as a deployment gate before any RAG system reaches production. Run RAGAS evaluation on a curated golden test set during development. Automate RAGAS monitoring on a production sample. Treat a faithfulness drop as a production incident requiring root cause investigation — not just a quality metric to note in a report.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers advanced RAG patterns (ColBERT, GraphRAG, HyDE, FLARE). You do not need these for a first production RAG deployment. Return here once your baseline pipeline is stable.

### 8.1 HNSW: How Vector Search Works at Scale

A naïve vector search compares the query vector against every document vector in the index — an O(N) operation. At 10 million documents, this is too slow for real-time retrieval.

**HNSW (Hierarchical Navigable Small World)** is the algorithm used by most production vector databases (Pinecone, Weaviate, Qdrant, pgvector with HNSW extension). It builds a hierarchical graph structure that enables approximate nearest neighbour search in O(log N) — fast enough for real-time retrieval at any scale.

**The intuition:**
HNSW builds multiple layers of graphs. The top layer is sparse — only the most "important" nodes (vectors), connected to a small number of neighbours. Each lower layer is denser. Search starts at the top layer: navigate toward the query by hopping to whichever neighbour is closest. When you can't get closer, descend to the next layer and navigate again — with more nodes available. Repeat until you reach the bottom layer.

**The tradeoff:** HNSW returns *approximate* nearest neighbours — not guaranteed exact nearest neighbours. The approximation is controlled by two parameters:
- `M`: number of bidirectional connections per node (higher → better recall, more memory)
- `ef_construction`: beam width during index construction (higher → better index quality, slower build)
- `ef_search`: beam width during query (higher → better recall, slower query)

For most enterprise RAG systems, default HNSW parameters give > 99% recall on standard benchmarks — the approximation is not practically relevant.

### 8.2 BM25: The Keyword Search Algorithm

**BM25 (Best Match 25)** is the standard probabilistic keyword search algorithm used by Elasticsearch, OpenSearch, and most vector databases for their keyword search component.

It extends TF-IDF (term frequency × inverse document frequency) with two improvements:

**Term frequency saturation:** TF-IDF scores increase linearly with term frequency — a document that mentions "return" 100 times scores much higher than one that mentions it 10 times. BM25 saturates: the score increase for each additional mention diminishes. The 11th mention adds less than the 1st.

**Document length normalisation:** shorter documents that mention a term are scored higher than longer documents that mention it the same number of times — because in a shorter document, the term represents a larger proportion of the content.

```
BM25(q, d) = Σ IDF(t) × (TF(t,d) × (k1+1)) / (TF(t,d) + k1 × (1-b + b×|d|/avgdl))

where:
  IDF(t) = log((N - df(t) + 0.5) / (df(t) + 0.5) + 1)
  k1 = 1.2 (term frequency saturation parameter)
  b = 0.75 (length normalisation parameter)
  |d| = document length; avgdl = average document length
```

For architects: you don't need to know this formula. You need to know that BM25 is the right choice for keyword retrieval alongside semantic search — it handles exact terms that embedding models miss.

### 8.3 Advanced RAG Patterns in Production

**Query decomposition:** complex multi-part queries ("What is our return policy for electronics purchased in December, and does it differ from our standard policy?") are decomposed into sub-queries by an LLM before retrieval. Each sub-query retrieves separately; results are merged before generation. Better recall for complex questions.

**Step-back prompting:** before the user query, generate a more abstract "step-back" version ("What are the general principles governing seasonal return policy exceptions?") and retrieve on that. The abstract retrieval surfaces foundational context that the specific query might miss.

**Iterative RAG (FLARE):** the model generates forward, identifies when it's about to make a low-confidence claim, pauses, retrieves relevant context, and continues. Rather than retrieving once at the start, retrieval is interleaved with generation — better for long, complex answers.

**RAG + structured data:** many enterprise questions require both document retrieval and database lookup ("What are the latest return statistics for Product X, and what does our policy say about that category?"). The architecture: agent with two tools — vector search for documents, SQL query for analytics. The orchestrator assembles context from both before generation.

---

## 9. Key Takeaways (5 Bullets)

- **RAG is the solution to the LLM knowledge cutoff problem — and the most widely deployed AI pattern in enterprise.** It doesn't require retraining. Knowledge is updated by updating the index. The model answers from what was retrieved, not from what it memorised. This makes AI systems maintainable in a way that pure parametric models are not.

- **Retrieval quality is the ceiling on answer quality.** The best LLM in the world cannot give a correct answer if the right document wasn't retrieved. Invest in retrieval quality — hybrid search (semantic + BM25), reranking, and document-structure-aware chunking — before optimising the generation step.

- **Hybrid search (semantic + BM25 + RRF) is the production standard — not semantic-only.** Semantic search misses exact terms (product codes, proper nouns, technical jargon). BM25 misses conceptual matches. RRF fusion gets the best of both. Semantic-only RAG is a common first implementation that almost always needs to be upgraded.

- **Measure all three dimensions of RAG quality independently.** Retrieval recall (did we get the right documents?), faithfulness (did the model answer from the documents?), and answer relevance (did the answer address the question?) can fail independently. A high faithfulness score with low retrieval recall means the model faithfully answers the wrong question. Diagnose which layer is failing before optimising.

- **RAG is a forcing function for knowledge quality.** A disorganised, inconsistent, or outdated knowledge base produces a disorganised, inconsistent, and outdated RAG system — at scale. Deploying RAG surfaces the quality of your organisation's knowledge management. Treating knowledge governance as a prerequisite to RAG deployment, not a follow-on, dramatically reduces post-launch quality issues.
