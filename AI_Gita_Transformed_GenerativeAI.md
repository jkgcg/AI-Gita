# Generative AI — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

**Generative AI** is AI that produces new content — text, images, audio, video, code, structured data — rather than classifying or predicting from existing content.

The distinction matters architecturally:

| Discriminative AI (older pattern) | Generative AI (current wave) |
|---|---|
| Input: content → Output: label or score | Input: prompt/context → Output: new content |
| "Is this email spam?" | "Write a reply to this email" |
| "Which product category does this belong to?" | "Write a product description for this SKU" |
| "What is the sentiment of this review?" | "Summarise these 500 reviews into themes" |
| Trained to classify | Trained to generate |

Generative AI is not one technology — it's a family of architectures, each optimised for a different output modality:

- **Large Language Models (LLMs):** generate text, code, structured data (JSON/XML), conversations
- **Diffusion models:** generate images, video, audio from text descriptions
- **Multimodal models:** accept and produce combinations of text, image, audio, video
- **Embedding models:** generate vector representations of content (not visible output, but enable semantic search and similarity)

For architects, the key shift is that generative AI capabilities are now **accessible as APIs** — you do not need to train or host these models to use them. The architectural question is how to integrate them, not how to build them.

---

## 2. Why Should I Care

### For Solution Architects

Generative AI has unlocked enterprise use cases that previously required large specialised teams or were simply not feasible:

- **Content at scale:** generating product descriptions, personalised emails, knowledge base articles, report summaries — content that previously required human writers for every item
- **Document understanding:** extracting structured information from unstructured documents (contracts, invoices, technical specs, forms) with accuracy that approaches human-level for many document types
- **Code assistance:** generating boilerplate, explaining legacy code, writing tests, translating between languages — reducing developer time on mechanical tasks
- **Multimodal intake:** processing images, screenshots, scanned documents, diagrams alongside text — enabling use cases like automated invoice processing or visual product inspection

What's changed is not that these problems are new. It's that the cost and complexity of solving them has dropped by orders of magnitude. A use case that would have required 6 months of ML engineering in 2021 can now be prototyped in a week via API.

### For Enterprise Architects

Generative AI introduces new integration patterns and new risk categories:

> **What is a token?** A token is the basic unit of text that LLMs process — and the unit that APIs charge for. Roughly 3–4 characters or 0.75 words in English. "Hello world" = 2 tokens. 1,000 tokens ≈ 750 words ≈ 1.5 pages. APIs charge separately for **input tokens** (your prompt) and **output tokens** (the model's response). When you see pricing like "$2 per million tokens", that is the cost per million of these text chunks.

**New integration patterns:**
- Synchronous API calls to generative models (similar to calling a third-party service, but with much higher latency and variable output size)
- Streaming responses (models generate token-by-token; streaming is often required for interactive UX)
- Multimodal inputs (sending images, documents, audio alongside text)
- agentic patterns (where the AI model takes sequences of actions — calling tools, making decisions, looping — rather than just answering a single question; covered in the Agents & Prompting module)

**New risk categories:**
- **Output non-determinism:** the same input can produce different outputs — downstream systems cannot assume reproducibility
- **Hallucination:** generated content can be fluent, confident, and wrong — requires verification layers
- **Content moderation:** generated content requires output filtering (toxicity, PII, competitive sensitivity)
- **Intellectual property:** generated images and text may resemble training data — IP risk for customer-facing content
- **Cost variability:** output length is model-determined, not fixed — a single API call can cost £0.001 or £0.50 depending on what the model generates

---

## 3. Think About It Like This (Analogy)

**The Creative Professional Agency Analogy**

Imagine you have access to an agency staffed with an unlimited number of skilled creative professionals — writers, designers, audio engineers, video editors — all available instantly, at any time, for any request.

**Text generation (LLMs)** is like having a skilled writer who has read everything. You brief them: "Write a product description for this kitchen knife set, in our brand voice, under 150 words." They draft immediately. They can write in any style, format, or language. They occasionally get facts wrong (hallucination) — a human editor should review important content.

**Image generation (diffusion models)** is like having a graphic designer who has studied millions of images. You describe what you want: "A professional photograph of a modern kitchen with warm lighting and a knife set on a marble countertop." They produce it in seconds. They're creative, fast, and surprisingly competent — but they sometimes misread instructions (six-fingered hands, misspelled text, impossible geometry). Quality is high enough for concept art, internal use, and increasingly for commercial use with careful review.

**Multimodal models** are like a professional who can work across modalities — you hand them a scanned contract and ask them to extract the payment terms as a structured table. They read the document (even handwritten or poorly scanned), understand it, and produce structured output.

**Embedding models** are like a research librarian with perfect recall of every document in the library, who can tell you: "Here are the five most relevant documents to your question" — not by keyword but by meaning. They don't produce visible output; they produce semantic coordinates used to organise and retrieve information.

**The limits are real:** every creative professional makes mistakes. Generative AI makes different mistakes than humans do (hallucination, prompt injection, nonsensical output on edge cases) — but the direction of the analogy holds. The question for architects is: where in your workflow do you need a human in the loop to catch the mistakes?

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 The GenAI Modality Decision Framework

The first question is always: which generative AI modality does this use case require?

```
What does the system need to PRODUCE?

Text / code / structured data
    → LLM (GPT-4o, Claude, Gemini, Llama-3)
    → See: the LLMs & Foundation Models module (which covers model selection, sampling parameters, and the 2026 model landscape)

Images
    → Diffusion model API (DALL-E 3, Stable Diffusion, Midjourney, Flux)
    → Choose based on: quality/cost, commercial licensing, style consistency

Audio
    → TTS (text-to-speech): ElevenLabs, OpenAI TTS, AWS Polly
    → Speech-to-text (STT): Whisper, Deepgram, AssemblyAI
    → Music/sound: Suno, Udio, AudioCraft (niche, emerging)

Video
    → Text-to-video: Sora (OpenAI), Runway, Kling (2025-2026 maturing)
    → Still early-stage for enterprise production use

Semantic vectors (not visible output)
    → Embedding model: text-embedding-3-large (OpenAI), BGE, E5, Cohere Embed
    → For: vector search, semantic similarity, RAG retrieval, clustering

Combined input + output (multimodal)
    → Vision-language models: GPT-4V, Claude with vision, Gemini Vision
    → For: document understanding, image analysis, visual Q&A
```

**Secondary decision: API vs self-hosted?**

For most enterprise teams starting with generative AI: **API-first**. The infrastructure cost, ops burden, and capability gap between API models and self-hosted alternatives is large. Exceptions: strict data residency, extremely high volume economics, or specialised fine-tuning requirements. See the AI Infrastructure module (which covers GPU costs, quantisation, and serving decisions) for the break-even analysis.

### 4.2 Text Generation (LLMs): The Dominant Modality

LLMs are the most broadly applicable generative AI capability for enterprise use cases. Key characteristics covered in depth in the LLMs & Foundation Models module (which covers model selection, sampling parameters, and the 2026 model landscape) — brief summary here:

- **How they work:** predict the most likely next token, repeatedly, until done
- **Controlled by:** temperature (creativity vs consistency), max tokens (output length), stop sequences
- **Integrated via:** chat completions API (most common), function calling for structured output, streaming for interactive UX
- **Enterprise sweet spots:** customer service automation, internal knowledge assistants, document processing, code assistance, content generation pipelines

**The chat completions API pattern:**

```
POST /v1/chat/completions
{
  "model": "claude-sonnet-4-6",
  "messages": [
    {"role": "system", "content": "You are a supply chain analyst..."},
    {"role": "user", "content": "Summarise this purchase order: [PO text]"}
  ],
  "temperature": 0.2,
  "max_tokens": 500
}
```

This pattern — system prompt defining role/scope, user message with task — covers 80% of enterprise LLM integration patterns.

### 4.3 Image Generation: Diffusion Models

**What diffusion models do:**

> **Explain Like I'm an Architect**
>
> Imagine you take a beautiful photograph and photocopy it on a bad machine. Then photocopy the photocopy. Then photocopy that. After 1,000 iterations, you have pure static — the original image is completely destroyed. Now imagine training a model to run that process in reverse: given a piece of static, predict what the image looked like one step earlier. Then one step earlier again. And again.
>
> That's exactly what diffusion models learn. They're trained to "denoise" — to reverse the noise-addition process step by step. At generation time, you start from pure random noise (like the final, completely degraded photocopy) and apply the model 20–50 times, each pass removing a bit of noise and pulling the image toward something coherent. The text prompt guides each denoising step — it steers the image toward "a marble kitchen countertop" rather than anything else equally plausible.
>
> **Why this matters architecturally:** each "denoising step" is a model inference call. 50 steps = 50 inferences. This is why image generation takes 2–10 seconds and why accelerated samplers (fewer steps, same quality) are a significant engineering advance. It's also why image generation is inherently sequential, not parallelisable in the same way text generation is.

Diffusion models learn to generate images by being trained on the reverse of a noise-adding process. During training: take a real image, progressively add random noise until it's pure noise, teach the model to reverse each step. During generation: start from pure noise, iteratively denoise guided by a text prompt, until a coherent image emerges.

The key insight for architects: **you don't need to understand the math to use these models effectively.** What you need to understand is:

- Input: a text prompt (and optionally a reference image, style guidance, negative prompts)
- Output: one or more images at a specified resolution
- Quality levers: prompt quality, number of inference steps (more steps = better quality + more time), guidance scale (how closely to follow the prompt)
- Integration: REST API, identical pattern to LLM APIs

**The 2026 image generation API landscape:**

| Provider | API | Quality | Pricing | Licensing | Best for |
|---|---|---|---|---|---|
| **OpenAI DALL-E 3** | Simple, well-documented | High, consistent | £0.04–0.08/image | Commercial use allowed | General enterprise, prototyping |
| **Stability AI (SDXL, SD3)** | More config options | High | £0.003–0.013/image | Commercial (check terms) | Cost-sensitive, high volume |
| **Flux (Black Forest Labs)** | Modern, flexible | Very high | Varies by host | Commercial available | Highest quality requirements |
| **Midjourney API** | Emerging | Excellent artistic | Subscription-based | Commercial (Pro plan) | Creative/marketing |
| **Google Imagen** | Vertex AI | High | Per-image + compute | Commercial | GCP-native stacks |

**Prompt engineering for image generation:**

Image generation prompts differ from text prompts — specificity matters more, adjectives carry high weight:

```
Weak prompt:    "A product photo of headphones"
Strong prompt:  "Professional product photography of matte black wireless 
                 over-ear headphones on a white background, studio lighting,
                 soft shadows, 4K, commercial quality"
```

Negative prompts (what not to include) are equally important:
```
Negative:  "blurry, distorted, extra limbs, watermark, text overlay, 
            low quality, jpeg artifacts"
```

**Key limitations for enterprise use:**

- **Text in images:** diffusion models are notoriously poor at generating legible text. For images requiring accurate text (product labels, signage), use image generation + text overlay compositing.
- **Consistency:** generating the same character, product, or face consistently across multiple images requires additional techniques (ControlNet, IP-Adapter, or fine-tuning). Raw text-to-image will vary significantly between generations.
- **IP and legal review:** images generated from APIs trained on licensed content carry legal uncertainty in some jurisdictions. Check with legal before using generated images in commercial content.
- **Content moderation:** most API providers have content moderation — prompts producing NSFW content, specific real people's faces, or trademarked characters are rejected. Plan for this in your error handling.

**Integration pattern:**

```python
import requests

def generate_product_image(product_description: str) -> bytes:
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "dall-e-3",
            "prompt": f"Professional product photography: {product_description}. "
                      "White background, studio lighting, commercial quality.",
            "size": "1024x1024",
            "quality": "standard",
            "n": 1
        }
    )
    image_url = response.json()["data"][0]["url"]
    return requests.get(image_url).content
```

### 4.4 Multimodal Models: Seeing and Reading

Multimodal models accept both text and images (and increasingly audio and video) as input, and produce text output. As of 2026, the major frontier LLMs (GPT-4o, Claude 3.x, Gemini) are multimodal by default.

**Enterprise use cases that become accessible:**

| Use case | How multimodal enables it |
|---|---|
| Invoice / PO processing | Send scanned document image; model extracts structured fields |
| Technical diagram analysis | Send architecture diagrams; model explains or answers questions |
| Quality inspection | Send product images; model identifies defects against criteria |
| Accessibility | Describe images for screen readers; auto-generate alt text |
| Form processing | Extract data from handwritten or printed forms |
| Visual search | "Find me products that look like this" (with embedding models) |

**The key architectural shift:** documents that previously required OCR pipelines + custom extraction logic can now be processed end-to-end through a multimodal API call. The model handles OCR, layout understanding, and extraction in a single step.

**Integration pattern:**

```python
import anthropic, base64

def extract_invoice_fields(image_bytes: bytes) -> dict:
    client = anthropic.Anthropic()
    image_b64 = base64.b64encode(image_bytes).decode()
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg",
                               "data": image_b64}
                },
                {
                    "type": "text",
                    "text": "Extract invoice fields as JSON: invoice_number, "
                            "vendor_name, total_amount, due_date, line_items[]"
                }
            ]
        }]
    )
    return json.loads(response.content[0].text)
```

**Limitations:**
- Image resolution: most APIs accept images up to ~20MB; very high-res images are typically downsampled
- Multi-page documents: each page must be sent as a separate image, or use a PDF-capable API endpoint
- Handwriting accuracy: handwritten text is harder than printed; accuracy varies by model and handwriting quality
- Complex tables: multi-column layouts and merged cells are challenging; validate extraction for complex structures

### 4.5 Embedding Models: Semantic Understanding Without Visible Output

Embedding models convert text (or images) into a fixed-size vector of numbers — a point in high-dimensional space where semantically similar content is geometrically close.

> **Explain Like I'm an Architect**
>
> A "vector of numbers" sounds abstract. Here's the intuition: imagine placing every concept in the English language on a giant invisible map. Words with similar meanings are placed near each other. "Dog" and "puppy" are close. "Dog" and "cat" are nearby. "Dog" and "quantum physics" are far apart. "Bank account" and "bank loan" are close; "river bank" and "bank account" are much further apart despite sharing a word.
>
> An embedding model is a system that converts any piece of text into GPS coordinates on this map. Two texts that mean similar things get similar coordinates. Two texts with different meanings get different coordinates.
>
> **Why this is useful:** instead of searching for documents that contain exact keywords, you search for documents whose "map coordinates" are close to your query's coordinates. "How do I send something back?" has coordinates close to "Product Return Policy" even though the words are completely different. This is semantic search — search by meaning, not by words.
>
> **Common Misconception:** embeddings don't produce text output. You cannot chat with an embedding model or ask it questions. Its output is a list of numbers (coordinates), stored in a vector database and compared against other lists of numbers at query time. It is infrastructure — the backbone of semantic search and RAG retrieval — not a conversational AI.

**What this enables:**
- **Semantic search:** find documents relevant to a query by meaning, not keyword match. "delivery delay" finds results about "shipment late" even if those exact words don't appear.
- **Recommendation:** find products, articles, or items similar to a given example
- **Clustering:** group documents by topic without predefined categories
- **RAG retrieval:** the backbone of vector search in RAG systems (see RAG & Vector tab)
- **Deduplication:** detect near-duplicate records across large datasets

**They don't generate visible content** — their output is a vector (array of floats) that's stored in a vector database and queried via similarity search.

**Integration pattern:**

```python
def embed_text(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding  # list of 3072 floats
```

**Choosing an embedding model:**

| Model | Dimensions | Context | Cost | Best for |
|---|---|---|---|---|
| text-embedding-3-large (OpenAI) | 3072 | 8191 tokens | £0.13/M tokens | General purpose, high quality |
| text-embedding-3-small (OpenAI) | 1536 | 8191 tokens | £0.02/M tokens | Cost-sensitive, high volume |
| BGE-M3 (BAAI, open-weight) | 1024 | 8192 tokens | Self-hosted | Multi-language, self-hosted RAG |
| Cohere Embed v3 | 1024 | 512 tokens | £0.10/M tokens | Enterprise, multi-language |

**Key constraint:** once you embed your corpus with a specific model, you must use the same model to embed queries. Switching embedding models requires re-embedding your entire corpus. Choose and pin your embedding model early in the project.

### 4.6 The Content Moderation Layer: Non-Negotiable

For any customer-facing application that generates content, a content moderation layer is architecturally mandatory — not optional.

```
User Request
    │
    ▼
Input moderation
  (hate speech, PII, competitor names, off-topic requests)
    │
    ▼
Generative model
  (LLM / image model / multimodal)
    │
    ▼
Output moderation
  (toxicity, PII in output, factual grounding check)
    │
    ▼
User receives content
```

**Options for moderation:**
- Provider-built: OpenAI Moderation API (text), AWS Rekognition (image), Azure Content Safety
- LLM-as-judge: use a separate LLM call to evaluate the output against criteria ("does this response contain PII? yes/no")
- Custom classifiers: fine-tuned models for domain-specific prohibited content

**What to moderate for (typical enterprise checklist):**
- [ ] Personal data / PII in output (especially for customer service)
- [ ] Competitor mentions (varies by use case)
- [ ] Factual claims that cannot be verified (for knowledge-sensitive domains)
- [ ] Tone / brand voice violations
- [ ] Content that could trigger regulatory scrutiny (financial advice, medical claims, legal advice)
- [ ] Prompt injection attempts in user inputs

---

## 5. Enterprise Example

**Scenario: Retail Product Content Generation Pipeline**

A retail group sells 80,000 active SKUs. Their current process for product content:
- Copywriters write descriptions: 1.5 hrs/product = 120,000 hours for current catalogue
- Product photography: £80–200/product = £6.4M–16M for full catalogue
- Translation into 6 languages: £0.12/word × avg 150 words × 80K SKUs × 6 languages = £8.6M

The team wants to use generative AI to scale content production.

**Architecture decision: which generative AI modalities?**

| Content type | Current process | GenAI solution | Modality |
|---|---|---|---|
| Product descriptions (English) | Human copywriters | LLM generation from spec sheet | Text (LLM) |
| Product descriptions (5 other languages) | Translation agency | LLM translation with brand voice | Text (LLM) |
| Lifestyle imagery (new products) | Photography studio | Image generation from text prompt | Image (diffusion) |
| White-background product images | Photography studio | Existing photo + background removal | Image processing + LLM (not pure genAI) |
| Product spec extraction from supplier docs | Manual data entry | Multimodal extraction from PDFs/images | Multimodal |
| Semantic product search | Keyword-only search | Embedding + vector search | Embeddings |

**Implemented pipeline:**

```
1. Supplier sends product spec sheet (PDF or structured data)
           │
           ▼
2. Multimodal extraction (Claude Vision)
   → structured product attributes (JSON)
   → confidence scores per field
           │
           ▼
3. Human review gate for low-confidence fields (< 0.85 confidence)
           │
           ▼
4. LLM description generation (Claude Haiku, batch)
   → brand-voice description template with structured attributes
   → 6 language variants in parallel
           │
           ▼
5. Image generation (DALL-E 3, for products without photography)
   → "product photography of [description], white background, studio lighting"
   → Generates 3 variants, merchandising team selects one
           │
           ▼
6. Content moderation (OpenAI Moderation + custom LLM-as-judge)
   → factual claims check (does description match extracted attributes?)
   → brand voice check
   → prohibited claims check
           │
           ▼
7. Embedding generation (text-embedding-3-large)
   → description + attributes → vector stored in product search index
           │
           ▼
8. Human sign-off queue (sample-based, 5% review rate post-launch)
```

**Results after 6-month rollout:**

| Metric | Before | After | Change |
|---|---|---|---|
| Time to publish new product | 3–4 weeks | 2–3 days | 85% faster |
| Description production cost | £18/product (copywriter) | £0.04/product (LLM) | 99.8% reduction |
| Language localisation cost | £0.12/word × 6 languages | £0.006/word equivalent | 95% reduction |
| Image production cost (no-photo products) | £120–200/product | £0.06/product | 99.7% reduction |
| Search relevance (A/B test) | Baseline | +31% click-through | Embedding search |
| Human error in spec extraction | 4.2% error rate (manual) | 1.8% error rate (multimodal + review) | 57% reduction |

**Lessons learned (what they got wrong first):**

1. **Skipped content moderation on launch:** first 500 descriptions had 2% with claims like "best in market" and "clinically proven" — not factual, potential regulatory issue. Moderation layer added week 2.

2. **Image generation for complex products:** generated images of products with logos/text were unusable (distorted text). Switched to human photography for branded products; image gen reserved for unbranded lifestyle imagery.

3. **Translation without brand voice examples:** first translations were accurate but felt machine-translated. Added 10 examples of correct brand voice per language to the prompt. Quality improved significantly.

4. **Over-automated human review:** removed the 5% review gate in week 3 to reduce bottleneck. Quality degraded noticeably in specialist category (outdoor equipment — technical accuracy issues). Review gate reinstated.

---

## 6. Architecture Perspective

### The Generative AI Integration Stack

When adding generative AI to an enterprise system, the full integration stack has more layers than most teams initially plan for:

```
Application Layer
  (UI, user input, output display / rendering)
        │
        ▼
Orchestration Layer
  (LangChain, custom code, workflow engine)
  (Routing: which model for which request type?)
  (Context assembly: system prompt + retrieved context + user input)
        │
        ▼
Generative AI API Layer
  (LLM / image gen / multimodal / embedding APIs)
  (Model version pinning, retry logic, timeout handling)
        │
        ▼
Safety & Moderation Layer
  (Input filtering, output filtering, PII detection)
        │
        ▼
Observability Layer
  (Prompt logging, cost tracking, latency monitoring, quality metrics)
        │
        ▼
Knowledge Layer (if applicable)
  (Vector database, document store, embedding index)
```

Each layer is an architectural decision with build-vs-buy options. Most teams underinvest in the Safety & Moderation layer and the Observability layer relative to the Generative AI API layer.

### Key Architectural Properties of Generative AI Systems

**Non-determinism is a feature, not a bug — but must be designed for.** Generative AI is inherently probabilistic. The same prompt produces different outputs on different calls. Systems must handle this: validate output structure (don't assume format), build idempotent downstream processing, and design UX that accommodates variation.

**Streaming changes UX architecture.** For interactive text generation (chatbots, copilots), streaming (receiving tokens as they are generated) is almost always required for good UX — waiting 10 seconds for a full response is poor UX; seeing the response build in real-time is acceptable. Streaming requires server-sent events or WebSocket infrastructure, not a simple REST request/response pattern.

**Async is often better than sync for batch generation.** For non-interactive use cases (batch content generation, document processing), asynchronous processing (job queue + worker + result store) is more resilient than synchronous API calls. Individual calls may time out; a queue-based architecture retries transparently.

**Cost is variable and must be budgeted dynamically.** Unlike traditional compute where cost = requests × fixed_cost, generative AI cost = input_tokens × input_price + output_tokens × output_price. Output token count is model-determined and variable. Implement per-request cost tracking, per-user/per-workflow budgets, and alerts for unexpected cost spikes.

---

## 7. Check Yourself (3–5 Questions)

> These questions test understanding, not memorisation. A correct answer shows you understand the *why* and can apply it to a new situation.

---

**Question 1 — Scale, cost, and moderation**

A product manager wants to build a feature that generates personalised marketing emails for 2 million customers. The emails should mention recent purchase history and current promotions. Which generative AI modalities are involved, and what are the key architectural concerns?

> **Simple Explanation:** Generating 2 million personalised emails sounds like "call the API 2 million times." The real architecture questions are: how do you do that without timeouts (async queues), how do you keep it from costing a surprise £5,000 (token budgeting), and how do you ensure no customer accidentally gets someone else's purchase history in their email (prompt design and moderation).

> **What is the context window?** The context window is the maximum amount of text the model can hold in working memory at once — your prompt, conversation history, retrieved documents, and the model's response all count toward this limit. Think of it as a whiteboard: everything the model needs to reason with must be written on this whiteboard. When it fills up, earlier content falls off and the model can no longer see it. Current models support 128K–1M tokens (roughly 90,000–750,000 words), but long agent workflows with rich tool outputs fill this faster than you expect.

> **Detailed Answer:** Modality: text generation (LLM) for the email body; possibly image generation if the email includes product imagery. Key architectural concerns: (1) **Scale** — 2M emails is a batch job, not interactive — async processing via job queue is essential. Synchronous API calls will time out and leave no retry path. (2) **Personalisation** — purchase history and current promotions must be injected per-email as structured context in the prompt. Context window limits how much history can be included per call. (3) **Cost** — at 2M emails × avg 500 input + 300 output tokens = 1.6B tokens. At Claude Haiku pricing (~£0.25/M input, £1.25/M output): approximately £1,000 per batch. Needs budgeting and per-run cost tracking. (4) **Content moderation** — outputs must be screened for PII leakage (one customer's data appearing in another's email if prompts are constructed carelessly), off-brand claims, and unsubscribe compliance. (5) **Consistency** — 2M emails must follow the same tone and format. Temperature should be low (0.1–0.3), output format strictly specified. (6) **Data privacy** — purchase history is PII; GDPR/data residency review required before sending to an external API.
>
> **Architecture Takeaway:** Scale, cost, and safety are not features to add later — they are the primary design constraints for any batch generative AI pipeline. Sequence: define cost budget → define moderation requirements → design async pipeline → design prompts → test.

---

**Question 2 — Image generation consistency**

Your team wants to use a diffusion model API to generate product images for 500 products. A developer proposes using the same prompt template: "A photo of [product_name] on a white background." What are the quality and consistency risks, and how would you improve the approach?

> **Simple Explanation:** "A photo of [product_name]" is like telling a photographer "take a photo of the product" with no brief — they'll do something, but it won't be consistent, correctly styled, or necessarily accurate. Professional photography has a detailed brief. So should your prompt template.
>
> **Detailed Answer:** Risks: (1) **Inconsistency** — diffusion models have high variance per generation; the same prompt produces different lighting, angle, and composition each time. A product catalogue needs visual consistency that a bare prompt template cannot deliver. (2) **Under-specification** — "A photo" gives the model no guidance on lighting, angle, style, or quality. It will choose these randomly. (3) **Text rendering** — any product with brand names, labels, or text will be garbled; diffusion models cannot reliably render legible text. (4) **Colour and proportion accuracy** — AI-generated images may misrepresent product colour, scale, or texture. This matters for purchase decisions. Improvements: (1) Enrich the prompt template: "Professional e-commerce product photography, front-facing, white background, soft studio lighting, shadows at base, no models, accurate colour, commercial quality, 4K." (2) Add a negative prompt: "blurry, distorted, text overlay, watermark, extra objects, hands, low quality." (3) Generate 3–5 variants per product and have a human select the best — not all outputs are usable. (4) Establish a visual style reference by shooting 5–10 "gold standard" hero images and using style-locking techniques for consistency. (5) Budget for human QA: even a 5% defect rate on 500 images = 25 requiring replacement.
>
> **Architecture Takeaway:** Diffusion model quality is directly proportional to prompt quality. For any production image pipeline, invest in a prompt engineering phase (a few days of trial-and-error) before committing to the pipeline design. The prompt template is a design artifact, not an afterthought.

---

**Question 3 — Embedding vs generation**

Describe the architectural difference between an embedding model and a text generation LLM. Why can't you use GPT-4o to do semantic search?

> **Simple Explanation:** An embedding model is a coordinate system — it tells you where a piece of text lives on a meaning map. A generation LLM is a writer — it produces new text. You cannot do similarity search with a writer; you need coordinates. You cannot write a response with coordinates; you need the writer.
>
> **Detailed Answer:** An **embedding model** converts text into a fixed-size dense vector (e.g., 3072 floating-point numbers) that represents the text's meaning as a position in semantic space. Its output is deterministic — the same text always produces the same vector. It is trained with contrastive objectives (similar texts pulled together in vector space, different texts pushed apart), producing geometrically meaningful coordinates for similarity search. A **text generation LLM** (like GPT-4o) generates text token by token via autoregressive sampling. Its output is a sequence of tokens — not a fixed-size vector. You could ask GPT-4o to "produce an embedding for this text" — but it would output numbers as text, which: (a) is not trained to produce geometrically meaningful representations; (b) costs far more (many tokens vs a single embedding call); (c) cannot be indexed for approximate nearest-neighbour search. The reason semantic search uses embedding models specifically: they produce fixed-size vectors that can be indexed in HNSW data structures enabling millisecond-speed similarity search across millions of documents. GPT-4o and embedding models are complementary: embeddings retrieve the relevant passages, the LLM synthesises the answer from those passages.
>
> **Architecture Takeaway:** Embedding model and LLM are two different infrastructure components in a RAG system. They are not interchangeable. Choose them independently, pin each to a specific version, and treat switching either as a breaking infrastructure change that requires re-indexing or re-evaluating the downstream system.

---

**Question 4 — Output moderation retrofit**

A team has deployed a customer service chatbot using an LLM. Three months after launch, the legal team flags that some responses are making implied warranty claims. How do you architect a fix?

> **Simple Explanation:** The LLM was not told what it wasn't allowed to say, and nobody was checking what it actually said. The fix has two parts: tell it clearly what's off-limits (system prompt), and verify it's respecting those limits (output moderation). One without the other is insufficient.
>
> **Detailed Answer:** This is an output moderation failure — the LLM is generating legally risky claims. Root cause: (1) the system prompt likely doesn't explicitly prohibit warranty-like language; (2) no output moderation layer was implemented. Fix at three layers: (1) **System prompt** — add explicit prohibition: "Never make guarantees about product outcomes. Use only hedged language: 'may help', 'is designed to', 'many customers find'. Never use 'will', 'guaranteed', 'definitely' in relation to product outcomes." Include 3–5 examples of correct and prohibited phrasings. (2) **Output moderation layer** — add a classifier that scans every response before delivery. Use a fast regex pre-filter for obvious patterns ("guaranteed", "definitely solve") and an LLM-as-judge for nuanced claims. Block and regenerate (with stricter instructions) if a violation is detected. (3) **Monitoring** — 1% of conversations reviewed by legal/compliance weekly to catch drift as base model updates or user query patterns evolve. The architectural lesson: content moderation for legal and compliance risks must be designed in at launch, not retrofitted after an incident.
>
> **Architecture Takeaway:** Output moderation is not optional for customer-facing generative AI. It is a non-negotiable architectural layer with legal, compliance, and brand risk implications. Design it before launch. The cost of a post-incident retrofit — in legal risk, engineering time, and user trust — vastly exceeds the cost of building the moderation layer from day one.

---

**Question 5 — Build vs photography**

Your company is evaluating whether to build a product image generation pipeline (200 new products/month) or continue with photography. What information do you need to make this decision, and what factors favour each option?

> **Simple Explanation:** AI image generation is dramatically cheaper and faster. But cheaper and faster doesn't mean "the same quality" — especially for products where colour accuracy and proportion matter to the purchase decision. The right question is not "AI or photography?" but "which products need photography's accuracy and which ones can AI handle well enough?"
>
> **Detailed Answer:** Information needed: (1) Current photography cost per product (photographer, studio, editing): typically £80–300/product. (2) Product type: apparel, jewellery, and high-end goods require colour and proportion accuracy — harder for AI. Consumer goods and homeware are more forgiving. (3) Quality bar: luxury catalogue vs budget marketplace. (4) IP/legal clearance: check with legal team before using AI-generated images in commercial contexts. (5) Consistency requirement: does the catalogue need style-consistent imagery across categories? (6) Revision workflow: how many iterations are acceptable before approval? **Factors favouring image generation:** 99%+ cost reduction per image; images available in seconds vs weeks; unlimited low-cost variations (backgrounds, seasons, contexts); scales to high volume without proportional cost increase. **Factors favouring photography:** accuracy for complex products — photography captures actual colour, texture, and proportion; customer trust in high-expectation categories (luxury, fashion); clear IP status; existing workflow already established. **Pragmatic recommendation:** run a 50-product pilot with AI generation, have merchandising and legal review, measure return and complaint rate against photography-sourced products. Most teams find AI generation works well for standard products and poorly for hero imagery or accuracy-critical products — a hybrid approach is usually the right outcome.
>
> **Architecture Takeaway:** Run a controlled pilot before committing to a pipeline build. Measure business outcomes (return rate, customer complaints) not just image quality ratings. The pilot data, not the theoretical cost comparison, should drive the decision.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers diffusion model mathematics, GAN internals, and flow matching. The mathematical notation is not required to use or architect generative AI systems. It is safe to skip on a first pass and return here later.

### 8.1 How Diffusion Models Work

Diffusion models are trained via a two-phase process:

**Forward process (training only):** take a real image x₀. At each step t, add a small amount of Gaussian noise. Repeat for T steps (typically 1000) until the image is indistinguishable from pure noise xᴛ. This is a fixed, non-learned process.

**Reverse process (what the model learns):** train a neural network (the "denoiser" — typically a U-Net or DiT architecture) to predict, given a noisy image xₜ and the text prompt c, what noise was added at step t:

In plain terms: the model is trained to recognise exactly what noise was added to an image at each step, so it can learn to remove it. The formula below makes this precise — but the architectural implication is what matters: the model learns noise-removal, not image-generation directly.

```
Objective: minimise ||ε - ε_θ(xₜ, t, c)||²

Where:
  ε      = actual noise added at step t
  ε_θ    = model's prediction of that noise
  xₜ     = noisy image at step t
  t      = timestep
  c      = text conditioning (CLIP-encoded prompt)
```

**Generation:** start from pure Gaussian noise xᴛ. Iteratively apply the denoiser to predict and subtract the noise for T steps (or fewer with accelerated samplers like DDIM). At each step, the prediction is conditioned on the text prompt via cross-attention. After T steps: coherent image.

**Classifier-free guidance (CFG):** the key mechanism for prompt adherence. At each denoising step, run the model twice — once conditioned on the prompt (ε_θ(x,t,c)) and once unconditioned (ε_θ(x,t,∅)). The actual noise removal uses:

```
ε_guided = ε_θ(x,t,∅) + guidance_scale × (ε_θ(x,t,c) - ε_θ(x,t,∅))
```

Higher guidance scale → stronger prompt adherence → sometimes over-saturated or less natural results. Typical values: 5–12.

### 8.2 GANs vs Diffusion: Why Diffusion Won

**GANs (Generative Adversarial Networks)** were the dominant image generation approach from 2014–2022. They use two competing networks:
- **Generator:** takes random noise, produces an image
- **Discriminator:** tries to distinguish generated from real images
- Training: the generator improves until the discriminator can't tell the difference

**Why diffusion replaced GANs for most use cases:**
- **Training stability:** GAN training is notoriously unstable (mode collapse, where the generator produces limited variety; vanishing gradients). Diffusion models train stably.
- **Coverage:** GANs tend to produce sharp but limited distribution coverage. Diffusion models produce more diverse outputs covering the full distribution of training data.
- **Text conditioning:** cross-attention in the denoising network allows strong text-image alignment. GAN conditioning on text was harder to achieve at high quality.
- **Scalability:** diffusion models scale cleanly with more compute; GANs didn't scale as predictably.

GANs remain relevant for: real-time applications (inference is single-pass, not iterative), super-resolution, and domain-specific applications where small, fast models are needed.

### 8.3 Flow Matching: The Post-Diffusion Architecture

**Flow matching** (used in Stable Diffusion 3, Flux) is a conceptually simpler alternative to diffusion that trains the model to predict a straight-line path from noise to data, rather than predicting noise at each step:

```
Diffusion: learn to remove noise step-by-step (curved path)
Flow:       learn to transport data along straight paths from noise distribution to data distribution
```

In practice: faster inference (fewer steps needed), better training convergence, and often higher image quality. Most frontier image generation models in 2025–2026 use flow matching rather than classical diffusion. The user-facing behaviour is identical — prompt in, image out.

---

## 9. Key Takeaways (5 Bullets)

- **Generative AI is a family of modalities, not a single technology — match the modality to the output type.** Text/code/structured data → LLMs. Images → diffusion models. Semantic search/retrieval → embedding models. Multimodal understanding → vision-language models. Choosing the wrong modality is an architecture mistake, not a tuning problem.

- **The decisive question is always API vs self-hosted, and for most teams the answer is API-first.** The capability gap between leading API models and self-hosted alternatives for image and multimodal use cases is large. Start with API; self-host only when volume economics justify it or data residency requires it.

- **Content moderation is architecturally mandatory for customer-facing generative AI, not optional.** Every customer-facing system that generates content needs input moderation (catch harmful prompts), output moderation (catch harmful/incorrect/legally risky outputs), and human review sampling. The common failure mode is launching without this layer and retrofitting after an incident.

- **Diffusion models for images are powerful but have well-known failure modes that affect enterprise use.** Text in images is garbled, brand/style consistency across generations is hard without additional techniques, and colour/proportion accuracy for products requires validation. AI-generated images work best as a supplement to photography (lifestyle imagery, background variants), not a wholesale replacement for hero product shots in quality-sensitive contexts.

- **Embedding models are not generative — they are the infrastructure of semantic understanding.** Every RAG system, semantic search capability, and similarity-based recommendation is built on embeddings. Pin your embedding model choice early: switching models requires re-embedding your entire corpus. The embedding model is infrastructure, not an interchangeable API call.
