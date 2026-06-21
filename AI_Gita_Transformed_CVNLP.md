# Computer Vision and NLP for Architects
### AI Gita — Transformed Learning Module

---

## 1. What Is It (Plain English)

Computer vision (CV) and natural language processing (NLP) are the two oldest and most mature branches of AI applied to unstructured data. CV processes images and video. NLP processes text and language. As an architect working with LLMs today, you already work in the NLP tradition — the transformer architecture that powers GPT-4 and Claude originated in NLP. Understanding CV and NLP together lets you see where the LLMs you already know come from, what they share with image models, and where the two domains are merging.

Both CV and NLP models are built on neural networks — the same foundation as the LLMs you already know. The difference is in what they process: images (CV) or sequences of words (NLP), and the architectural adaptations that makes each effective for its domain.

The connection is closer than you might think:

- A CNN (convolutional neural network) that classifies product images is doing the visual equivalent of what an embedding model does for text: compressing raw input into a dense representation that captures semantically meaningful features.
- Object detection in images (finding and labelling every product in a shelf photo) is the visual equivalent of named entity recognition in text (finding and labelling every entity — person, organisation, date — in a customer message).
- Transfer learning — taking a model trained on a massive general dataset and adapting it to your specific task with a small fine-tuning dataset — is the same principle whether you are working with images or text.
- Vision-language models (like GPT-4V, Gemini, and PaliGemma) now process images and text together in a single model, collapsing the boundary between CV and NLP for many enterprise use cases.

This module builds the conceptual bridge from the LLM world you already know to the broader CV and NLP landscape, and shows you which architectural patterns appear in both domains.

---

## 2. Why Should I Care

### For Solution Architects

Many enterprise AI opportunities involve visual data: product catalogues, invoice processing, quality control inspection, compliance documentation, retail shelf monitoring, identity verification. When a business brings you a use case involving images or documents, you need to know whether the task calls for a classification model (put this image in a category), a detection model (find and locate all instances of X in this image), an embedding model (represent this image so it can be searched), or a vision-language model (read this document and extract structured data).

Getting this wrong is expensive. A classification model cannot detect multiple items in an image. A detection model overkills a simple categorisation task. A vision-language model provides the richest capability but is the most expensive to run and the hardest to explain.

For text tasks, architects increasingly face a choice between a large general-purpose LLM (GPT-4, Claude) and a task-specific smaller NLP model (a fine-tuned BERT classifier, a named entity recognition model). Understanding the underlying NLP task structure tells you when a specialised smaller model is better: cheaper, faster, more predictable, and often more accurate on a narrow task.

### For Enterprise Architects

The practical consequence of vision and language AI converging is that enterprise automation tasks that previously required separate systems — one for document ingestion, one for field extraction, one for classification, one for routing — can increasingly be handled by a single vision-language model. This changes the integration architecture, the cost model, and the governance requirements.

For governance: NLP models, particularly classification and NER models, are more explainable and auditable than large generative models. A BERT-based sentiment classifier's predictions can be attributed to specific input tokens. An LLM's sentiment assessment cannot be traced to a specific weight or layer in a meaningful way for audit purposes. In regulated industries, task-specific NLP models may be preferred over general LLMs precisely because their behaviour is more constrained and auditable.

For CV: image-based AI systems processing customer data (faces, identity documents, body images) attract specific regulatory attention in the EU and elsewhere. The architecture must include data minimisation, retention controls, and bias testing (particularly for demographic representation) as explicit requirements, not afterthoughts.

---

## 3. Think About It Like This

Imagine the challenge of hiring a brilliant all-rounder who has never encountered your industry versus hiring a team of specialists who know your domain deeply.

The all-rounder (an LLM or a large vision-language model) has read or seen almost everything. They understand context, nuance, ambiguity. They can handle tasks they have never seen before. But they are expensive, slow compared to specialists, and their reasoning process is opaque — you cannot easily verify why they gave a particular answer.

The specialist team (task-specific NLP or CV models) is deeply trained on one type of task. Your invoice extraction specialist can process 10,000 invoices a minute, never makes a random error about field format, and you can test exactly what it knows and does not know. But ask it to handle a task outside its training and it fails immediately.

The transfer learning principle is what makes hiring the all-rounder practical: you do not hire them as a generalist and start from scratch. You hire them for their general knowledge and then spend a few weeks training them in your industry's specifics. This is fine-tuning — taking a model with enormous general capabilities and adapting it to your specific task with a small amount of task-specific training.

In CV: ImageNet pre-training (training on 1.2 million general images) gives a model that understands shapes, textures, edges, objects. Fine-tuning on your 10,000 product images takes that general visual understanding and adapts it to your catalogue.

In NLP: BERT pre-training (training on the entire Wikipedia and a book corpus) gives a model that understands language structure, word relationships, context. Fine-tuning on your 5,000 labelled customer reviews adapts it to your sentiment classification task.

Same principle. Different inputs. The architectural pattern is identical.

---

## 4. Step-by-Step Walkthrough

### 4.1 Computer Vision: Task Types and When Each Applies

**Image Classification**: the simplest CV task. Assign a single label to an entire image. Input: image. Output: one category label (and optionally a confidence score).

Use cases: product category classification (is this image apparel, footwear, or accessories?), quality control pass/fail (is this manufactured part defective?), document type classification (is this an invoice, a purchase order, or a delivery note?).

Architecture: a CNN (convolutional neural network) or a Vision Transformer (ViT). At deployment time, the model is a fast, stateless function: image in, category out. Latency is typically milliseconds on GPU.

**Object Detection**: find and localise all instances of one or more object classes within an image. Output: a set of bounding boxes, each labelled with a class and a confidence score. More complex than classification because the model must answer both "what is in this image?" and "where exactly in this image is it?"

Use cases: retail shelf monitoring (detect all products, detect gaps, detect misplaced items), quality inspection (locate all defects in a manufactured component), document layout parsing (locate all tables, headers, figures in a scanned document), vehicle detection in car park management.

Architecture: YOLO (You Only Look Once) family models are the standard choice for real-time object detection — they process the full image in a single forward pass, making them extremely fast. Faster R-CNN and its variants are slower but historically more accurate; for applications where latency is less critical, they remain relevant.

**Image Segmentation**: instead of bounding boxes, predict a class label for every pixel in the image. More precise than detection because it tells you exactly which pixels belong to each object, not just the bounding box region.

Use cases: medical imaging (segment the tumour from healthy tissue), autonomous vehicle perception (segment road, pedestrian, vehicle per pixel), quality inspection where the exact defect area matters.

Architecture: U-Net (especially in medical imaging), Mask R-CNN, Segment Anything Model (SAM from Meta).

**Image Embedding / Visual Search**: convert an image into a dense vector that captures its semantic content, enabling similarity search over a catalogue of images.

Use cases: "find similar products" (show me more items like this one the customer photographed), duplicate product detection in a catalogue, visual quality comparison (how similar is this manufactured part to the reference standard?).

Architecture: a CNN or ViT encoder trained with contrastive learning (CLIP, SigLIP). The training objective teaches the model to embed similar images close together and dissimilar images far apart in the embedding space — exactly analogous to how text embedding models are trained.

> **Before you read Sections 4.2 and 4.3 — a 30-second primer:**
> A neural network is a chain of mathematical transformations. Each "layer" applies a transformation to the data it receives, learning the right transformation during training. "Weights" are the numbers that define those transformations. "Forward pass" means running data through all the layers from input to output. You do not need to know the math — just that these terms refer to the internal mechanics of how the model processes information.

> **Explain Like I'm an Architect**
>
> A CNN processes images the way a quality inspector scans a factory floor: they move a spotlight methodically across the surface, detecting local patterns in each small region (edges, textures, corners), then combine those local observations into higher-level assessments ("that cluster of edge-detections in the corner means 'defect'"). The inspector doesn't need to see the whole floor simultaneously — local patterns are enough.
>
> A Vision Transformer does it differently: it cuts the image into a grid of tiles (like a mosaic), then lets every tile "talk to" every other tile simultaneously. The tile in the top-left can directly factor in what the tile in the bottom-right looks like, without relaying information through everything in between. This is slower to learn (you need far more training images before the all-tiles-communicate approach works well), but it catches complex spatial relationships that local scanning misses.
>
> **Why this matters architecturally:** CNNs are more data-efficient and run faster on edge devices (mobile phones, embedded hardware). ViTs are better for complex visual understanding and integrate naturally with language models — making them the foundation for vision-language models. The choice affects deployment cost, hardware requirements, and whether your model can run at the edge or requires cloud inference.

### 4.2 The CNN and ViT Architectures — Intuition Level

**CNNs (Convolutional Neural Networks)**: the dominant CV architecture for over a decade. The key insight: process images using local filters that slide across the image, detecting local features (edges, textures, corners) at different scales. Early layers detect low-level features (edges, gradients). Deeper layers combine these into higher-level features (shapes, objects, scenes).

Why local filters work: an edge detector that works in the top-left corner of an image works equally well in the bottom-right corner. Parameters are shared across the entire image — this makes CNNs parameter-efficient compared to a fully connected network that would have a separate weight for every pixel position.

Pooling layers progressively reduce spatial resolution while increasing the receptive field (the area of the original image each neuron "sees"). By the final layers, each neuron encodes information from a large area of the image.

**Vision Transformers (ViT)**: apply the transformer architecture directly to images. The image is divided into fixed-size patches (e.g., 16x16 pixels). Each patch is linearly projected into an embedding vector. These patch embeddings are then processed by transformer self-attention layers — each patch can attend to every other patch, capturing long-range spatial dependencies that CNNs struggle with.

ViTs need more training data than CNNs to work well (their lack of spatial inductive bias is both a weakness and an asset — they can learn arbitrary spatial relationships but need more data to do so). Pre-trained on massive datasets (ImageNet-21K, JFT-300M), ViTs match or exceed CNN performance.

For architects: CNNs are faster, more data-efficient for small datasets, and easier to deploy on edge devices (mobile phones, embedded systems). ViTs are more flexible, better for high-resolution inputs and fine-grained recognition, and architecturally compatible with the transformer-based LLMs — making them the natural backbone for vision-language models.

### 4.3 NLP: Task Types and When Each Applies

**Text Classification**: assign a label to an entire text input. Binary (positive/negative sentiment), multiclass (which of 10 product categories does this review discuss?), or multi-label (which of 20 compliance flags does this contract trigger?).

Use cases: customer review sentiment, email routing by topic, support ticket urgency scoring, contract clause categorisation, content moderation.

Architecture: fine-tuned BERT-class model (BERT, RoBERTa, DistilBERT) for shorter texts. For very long documents, use a hierarchical approach (classify sections, then aggregate) or a long-context model.

**Named Entity Recognition (NER)**: identify and classify named entities within text — people, organisations, dates, monetary amounts, product names, locations.

Use cases: extracting supplier names and invoice dates from unstructured invoice text, identifying parties and obligations in contract review, extracting patient information from clinical notes, populating structured databases from unstructured reports.

Architecture: fine-tuned BERT-class model with a token classification head (each token is labelled as B-entity, I-entity, or O-outside). Standard NER models label each token's entity type as it reads the text left-to-right.

**Information Extraction**: extracting structured information from unstructured text — filling a template or a database record from a free-text document.

Use cases: extracting order details from email confirmations, populating product attributes from catalogue descriptions, reading semi-structured documents (invoices, purchase orders, shipping manifests).

Architecture: this is increasingly handled by instruction-tuned LLMs or vision-language models for complex documents. For simpler, well-defined extraction tasks, a combination of NER + regex post-processing is faster, cheaper, and more reliable.

**Semantic Search / Embeddings**: convert text into dense vectors that capture meaning, enabling search by semantic similarity rather than keyword matching.

Use cases: product search that understands "casual blue summer dress" even if no product uses exactly those words, enterprise knowledge base search, finding similar support tickets, contract clause retrieval.

Architecture: BERT-class encoder trained with contrastive objectives (Sentence-BERT, E5, text-embedding-ada-002). The model learns to embed sentences with similar meaning close together in vector space.

**Question Answering and Extraction**: find the answer to a question in a provided passage of text.

Use cases: internal knowledge base Q&A, reading comprehension over policy documents, structured extraction from specific document types.

Architecture: this is the native capability of instruction-tuned LLMs in a RAG (retrieval-augmented generation) pattern. For narrow, predictable extraction tasks, fine-tuned BERT with an extractive QA head is faster and cheaper.

> **Explain Like I'm an Architect**
>
> Before a model can read text, it must convert words into numbers — models only understand maths. Tokenisation is the strategy for that conversion.
>
> Imagine a filing system for documents. You could number every individual letter (a=1, b=2…) — simple, but "customer" becomes 8 separate numbers, which is inefficient. Or you could number every complete word — but then "unstructured", "unstructures", and "unstructuredness" all need separate entries, and technical vocabulary bloats the dictionary infinitely.
>
> BPE (Byte-Pair Encoding) is the practical middle ground: it assigns single numbers to common whole words ("the", "and", "product"), breaks uncommon words into recognisable parts ("un" + "structured"), and ensures any text — even words the model never encountered in training — can be represented. The result: common language is compact, rare or technical vocabulary costs more tokens.
>
> **Why this matters architecturally:** Every token consumed is a token paid for. The same content tokenises differently across languages — a 10-page policy document might cost 3,000 tokens in English but 6,000 tokens in Arabic or Korean, because English-optimised tokenisers split non-Latin scripts less efficiently. At 100,000 documents per month, this is a direct cost and context-window budget line item that must appear in your architecture estimates.

### 4.4 Tokenisation: How Text Becomes Numbers

Before any NLP model can process text, it must be converted into numbers. Tokenisation is the process of splitting text into units (tokens) and mapping each unit to a number.

**Byte-Pair Encoding (BPE)**: the most common tokenisation algorithm in modern LLMs (used in GPT-2/3/4, RoBERTa, and most transformers). It starts with individual characters and iteratively merges the most frequent character pairs into a single token, until a target vocabulary size is reached.

The result: common words are single tokens ("the", "and", "product"). Common subword units are also tokens ("##ing", "##ness", "un##"). Rare words are split into subword tokens ("unstructured" → "un", "structured"). Any character sequence can be tokenised, even words not in the training vocabulary.

Why architects care: tokenisation determines context window consumption. "Please process this invoice and extract: supplier name, invoice date, total amount, and line items." — this prompt consumes approximately 20 tokens in GPT-4's tokeniser. A 10-page PDF might consume 2,000–5,000 tokens. At $0.01 per 1K tokens (illustrative pricing), processing 100,000 such documents per month has a direct cost implication that flows from tokenisation choices.

Different tokenisers produce different token counts for the same text. Multilingual text (particularly non-Latin scripts like Chinese, Arabic, Korean) is often tokenised less efficiently — more tokens per word — in English-optimised tokenisers. This means processing multilingual content costs more and consumes more context window than equivalent English content.

**WordPiece** (used in BERT) and **SentencePiece** (used in T5, LLaMA) are alternative tokenisation algorithms with similar properties. The specific algorithm matters less than understanding that tokenisation efficiency varies by language, domain, and vocabulary.

> **Explain Like I'm an Architect**
>
> Transfer learning is the "don't start from scratch" principle applied to AI models. Imagine hiring a new paralegal. You could train them from zero — teach them how to read, what contracts are, what legal terminology means, how to spot obligations — which takes years. Or you hire someone who already has a law degree and train them in your company's specific contract templates and risk priorities, which takes weeks.
>
> Pre-trained models have the equivalent of a degree: they have been trained on enormous datasets and have already learned general representations (for images: edges, textures, shapes; for text: grammar, word relationships, context). Fine-tuning is the few-weeks domain training — you take that general foundation and adapt it to your specific task and vocabulary.
>
> **Why this matters architecturally:** You almost never train a model from scratch. You start from a pre-trained foundation and fine-tune. This means the "how much training data do we need?" question has a much lower answer than you might expect — you need enough domain-specific labelled data to adapt the model, not enough to teach it language or vision from zero. Typically: hundreds to thousands of examples for task-specific fine-tuning, not millions.

### 4.5 Transfer Learning: The Shared Principle Across CV and NLP

Transfer learning is the practice of starting from a model pre-trained on a large general dataset and adapting it to a specific task with a smaller, task-specific dataset. It is the same principle in CV and NLP, with the same underlying reason: deep learning models learn hierarchical representations, and the lower-level representations (edges and textures in CV; syntax and word relationships in NLP) transfer across tasks better than the higher-level representations (specific object recognition; specific task semantics).

**The transfer learning workflow**:

1. Start with a pre-trained model (ResNet-50 trained on ImageNet for CV; BERT trained on Wikipedia for NLP)
2. Remove or modify the final task-specific layers (the classification head for CV; the masked language modelling head for NLP)
3. Add new task-specific layers for your target task (a new classification head for your product categories; a new token classification head for your NER labels)
4. Fine-tune: train the combined model (pre-trained backbone + new head) on your labelled dataset, typically with a small learning rate to avoid "forgetting" the pre-trained representations

**Full fine-tuning vs feature extraction**: in full fine-tuning, you update all the weights, including the pre-trained backbone. In feature extraction, you freeze the pre-trained backbone and only train the new task head. Feature extraction is faster and works better when your dataset is very small. Full fine-tuning produces better results with larger datasets but requires more compute and risks forgetting pre-trained representations if the learning rate is too high.

**Parameter-efficient fine-tuning (PEFT)**: for very large models (LLMs, large ViTs), full fine-tuning is prohibitively expensive. PEFT methods like LoRA, adapters, and prefix tuning update only a small number of additional parameters while keeping the original model frozen. The result is a fine-tuned model for your specific task at a fraction of the full fine-tuning compute cost.

### 4.6 CV vs NLP Task Mapping

| CV Task | NLP Equivalent | What it does |
|---|---|---|
| Image Classification | Text Classification | Assigns a single label to an entire input |
| Object Detection | Named Entity Recognition | Finds and labels multiple instances of specific types within an input |
| Image Segmentation | Semantic Role Labelling / Span Extraction | Labels every element of the input with its role or type |
| Image Embedding / Visual Search | Semantic Text Embedding / Semantic Search | Converts input into a dense vector for similarity comparison |
| Image Captioning | Text Summarisation | Generates text describing the content of an input |
| Image-to-Image Translation | Text-to-Text Generation / Translation | Converts one form of input to another |
| Visual Question Answering | Open-Domain Question Answering | Answers natural language questions about an input |

> **Common Misconception:** "Vision-language models (GPT-4V, Gemini) have made specialist CV and NLP models obsolete."
>
> Not for high-volume, well-defined tasks. A vision-language model can read an invoice, classify a product image, or analyse sentiment — but at 5–20× the inference cost of a fine-tuned specialist model doing the same task. For 85,000 sentiment classifications per month or 10,000 invoice extractions per day, the cost difference is the deciding factor, not capability. Vision-language models are the right choice when the task is ambiguous, complex, or low-volume. Specialist models win on cost and consistency at scale.

The mapping is not perfect — NLP and CV have domain-specific tasks that do not have clean equivalents. But the parallel structure reveals that the same architectural patterns (classification heads, encoder models, generative models with attention) appear in both domains.

---

## 5. Enterprise Example

Three connected examples across a retail and logistics context, each mapping to a different part of the CV/NLP landscape.

### Example A: Visual Product Catalogue Search (CV + Embedding)

**Scenario**: A global fashion retailer wants to allow customers to photograph a product they see in a magazine or on the street and find similar items in the retailer's catalogue.

**Architecture**: Each product image in the catalogue is pre-computed into a 768-dimensional embedding using a fine-tuned CLIP-based model. CLIP (Contrastive Language-Image Pre-Training) is trained to embed images and text into a shared embedding space — the text "red running shoe" and an image of a red running shoe will have similar embeddings. The catalogue embeddings are stored in a vector database (Weaviate).

At query time: the user uploads a photo. The photo is encoded by the same CLIP image encoder. An approximate nearest-neighbour search retrieves the 50 most similar catalogue items by cosine similarity. A re-ranking stage applies business filters (stock availability, correct size range, price band preferences) and returns the top 10 results.

**The CV architecture in use**: the CLIP image encoder is a Vision Transformer (ViT-B/32) pre-trained on 400 million image-text pairs. It was fine-tuned on the retailer's own product catalogue (120,000 product images) using a contrastive objective — pushing images of the same product close together in embedding space and images of different products apart.

**Key architecture decision**: the separate offline embedding of catalogue items means that search at query time is just a vector lookup — millisecond latency at scale. The expensive encoder runs only when new items are added to the catalogue, not at query time.

### Example B: Automated Invoice Field Extraction (Vision-Language Model as NLP Task)

**Scenario**: A logistics company receives 40,000 supplier invoices per month in diverse formats — PDF, scanned paper, structured Excel exports, email body text. The accounts payable team manually extracts: supplier name, invoice number, invoice date, line items (description, quantity, unit price), and total amount. This takes 3.5 FTE.

**Architecture**: For structured PDFs and digital formats, a traditional NLP pipeline (text extraction + NER + regex for amounts/dates) handles 60% of volumes with 98%+ accuracy.

For scanned and non-standard documents (the remaining 40%), a vision-language model (GPT-4V or an equivalent fine-tuned model) handles the full extraction in a single step. The document image is passed directly to the model with a structured extraction prompt: "Extract from this invoice: supplier_name, invoice_number, invoice_date, line_items (array of description, quantity, unit_price), subtotal, tax, total. Return as JSON."

The model understands the visual layout of the document — it can identify that text in the top-right is a date, that a two-column table is a line item list, and that the bold number at the bottom is the total — without needing explicit layout parsing rules.

**Why this is an NLP task**: even though the input is a document image, the task is fundamentally one of information extraction — filling a structured schema from unstructured input. The vision component is the mechanism (reading the image), but the task is NLP (extracting named entities and their values in a structured form).

**Governance note**: invoice data contains supplier payment information — any errors in extraction have direct financial consequences. Human review of low-confidence extractions (where the model returns a confidence score below a threshold, or where extracted amounts do not sum correctly) is a mandatory guardrail in the architecture.

### Example C: Customer Review Sentiment Pipeline (NLP Classification)

**Scenario**: A retail group receives 85,000 product reviews per month across 12 platforms in 6 languages. The customer experience team needs to identify: sentiment (positive/neutral/negative), product aspect discussed (quality, sizing, delivery, design, pricing), and urgency (does this review indicate a quality issue that needs investigation?).

**Why not an LLM**: an LLM could perform this analysis but at €0.01 per 1K tokens, processing 85,000 reviews at an average of 200 words each would cost approximately €3,400 per month. More importantly, LLM responses to classification prompts are less consistent than fine-tuned classifier outputs — the same review submitted twice might receive different aspect labels.

**Architecture**: three separate fine-tuned models on a shared multilingual backbone (XLM-RoBERTa, chosen for its strong multilingual performance):
1. Sentiment classifier: 3-class (positive/neutral/negative), fine-tuned on 25,000 labelled reviews
2. Aspect classifier: multi-label, fine-tuned on 15,000 reviews with aspect labels
3. Urgency classifier: binary (urgent/not-urgent), fine-tuned on 3,000 reviews labelled by quality specialists

All three models run in parallel. The sentiment and aspect models run on a shared batch inference service. The urgency model runs on real-time review submission to trigger immediate alerts.

**Cost**: inference for all three models costs approximately €120/month on GPU cloud infrastructure. One-tenth the LLM cost, with more consistent and auditable outputs.

---

## 6. Architecture Perspective

**CV and NLP tasks are converging through vision-language models, but task-specific models remain cost-competitive.** GPT-4V and similar models can do almost all the CV and NLP tasks described in this module. But for high-volume, well-defined tasks (invoice extraction, product classification, sentiment analysis), fine-tuned specialist models are 5–20x cheaper per inference and more predictable in their outputs. The architecture decision is: use vision-language models for complex, ambiguous, or low-volume tasks where flexibility matters; use task-specific fine-tuned models for high-volume, well-defined tasks where cost and consistency matter.

**Embedding models need domain-specific fine-tuning for reliable similarity search.** A general CLIP model will produce reasonable visual similarity results, but for domain-specific visual search (product matching, defect detection, medical imaging), fine-tuning on domain-specific data significantly improves embedding quality. The investment in fine-tuning pays off when: the domain has specific visual vocabulary not well represented in general training data, the volume of similarity searches is high, or the cost of false matches is significant.

**The tokenisation boundary is where text enters the model and architectural decisions become cost decisions.** Token counts drive context window consumption and inference cost. For high-volume NLP pipelines, optimise prompt length aggressively, batch requests where latency allows, and consider whether smaller context windows (with shorter prompts) can achieve the same task quality at lower cost.

**Transfer learning via LoRA is the standard for fine-tuning large models at reasonable cost.** Full fine-tuning of a 7B+ parameter model requires significant GPU memory and compute. LoRA (Low-Rank Adaptation) adds trainable matrices of much smaller dimension to the model's attention layers, reducing the number of trainable parameters by 100–1000x while achieving most of the performance of full fine-tuning. For enterprise deployments where data privacy requires on-premise fine-tuning, LoRA makes fine-tuning large models feasible on commodity GPU hardware.

**For multilingual NLP, embedding models and backbone choice matter.** English-optimised tokenisers and embedding models perform significantly worse on non-Latin scripts and lower-resource languages. For a multinational enterprise, specify multilingual-first models (XLM-RoBERTa, mBERT, mT5, or multilingual-capable embedding models like multilingual-e5) rather than English-primary models that handle other languages poorly.

---

## 7. Check Yourself

**Question 1 — CV task selection**

A product manager asks for a "product image search" feature. They want customers to be able to upload a photo of any product and find similar items in the catalogue. They also want the system to automatically categorise newly uploaded supplier product images into the correct product taxonomy. Are these the same AI problem? What is each and how do they differ architecturally?

> **Simple Explanation:** "Shopping by photo" is "find the closest match in our catalogue" — a nearest-neighbour search with no fixed categories. "Auto-categorising supplier images" is "which bin does this belong in?" — classification with a fixed taxonomy. Same camera input, completely different AI task, different model heads, different serving infrastructure.
>
> **Detailed Answer:** No, these are different CV tasks. The "find similar items" feature is a visual embedding and nearest-neighbour search task. It requires a model that encodes images into embeddings such that visually and semantically similar images are near each other in embedding space. The serving architecture requires pre-computed catalogue embeddings and a vector search index. There is no classification — no fixed set of labels; the output is "similar to this query image." The "auto-categorise supplier images" feature is an image classification task. It requires a model trained to output one of a fixed set of taxonomy labels. The output is a discrete label (or a ranked list of labels with confidence scores). These two features may share the same backbone architecture (a ViT or CNN encoder) but have different task heads and different serving patterns. Building one does not give you the other automatically.
>
> **Architecture Takeaway:** Identify the CV task type before designing the system — embedding+search and classification require different model heads, different evaluation approaches, and different serving patterns. Building one does not give you the other.

**Question 2 — Hybrid vs single-model for invoice extraction**

You need to extract structured data (supplier name, invoice date, total amount) from 10,000 invoices per day. The invoices arrive as scanned PDFs and range from simple single-page standard formats to complex multi-page custom layouts. Should you use a vision-language model for all of them, or a hybrid approach? Justify your answer.

> **Simple Explanation:** Use the cheap specialist tool for the 70% of cases it handles well; call in the expensive generalist for the complex 30%. It is how every professional services firm staffs a project — you do not send a senior partner to answer a standard question.
>
> **Detailed Answer:** A hybrid approach is almost always more cost-efficient and operationally robust. Segment the invoice population by complexity. For standard formats (say, 60–70% of volume) that have consistent layouts and can be handled by template-based extraction or a fine-tuned NER model on extracted text, use the cheaper, faster specialist approach. Reserve the vision-language model for complex or non-standard invoices where layout understanding is required and template matching fails. This reduces vision-language model API costs by 60–70% while maintaining the same overall extraction quality. The classification of "standard vs complex" can itself be automated using a simple document classifier trained on layout features. The hybrid architecture also provides a fallback: if the specialist model's confidence is below a threshold, escalate to the vision-language model, then to human review if confidence remains low.
>
> **Architecture Takeaway:** Segment your workload by complexity before choosing a model. Design a confidence threshold and escalation path: specialist model → vision-language model → human review. The classification of "standard vs complex" is itself automatable with a simple document classifier.

**Question 3 — Model selection for multilingual technical text**

An engineer proposes using a general-purpose BERT model (trained on English Wikipedia) for extracting product attributes from supplier product descriptions, which are often in German and contain highly technical textile terminology. What risks does this approach carry?

> **Simple Explanation:** Using an English-trained model on German technical text is like asking someone fluent in British English to read a German engineering manual — they will recognise some words but miss the domain meaning entirely. Language mismatch and vocabulary mismatch are two separate problems that require two separate fixes.
>
> **Detailed Answer:** Two significant risks. First, English-trained BERT is not designed for German text. While BERT has some multilingual capability due to shared subwords, its German language understanding is substantially weaker than its English understanding. For German-language extraction, use a multilingual model (mBERT, XLM-RoBERTa) or a German-specific model (BERT-German). Second, general Wikipedia text contains almost no textile or fashion industry vocabulary. Technical terms like "merino superwash", "tencel lyocell", "DWR coating", or "Strickfleece" will be tokenised into subword fragments that the model has seen rarely or never, and the embeddings for these tokens will not capture their semantic meaning. The model will perform poorly on domain-specific entity extraction without fine-tuning on domain-relevant labelled data. The remedy: use XLM-RoBERTa as the backbone (strong multilingual) and fine-tune it on a labelled dataset of German product descriptions with attribute annotations.
>
> **Architecture Takeaway:** Match model backbone to both language and domain. For multilingual technical text, specify a multilingual backbone (XLM-RoBERTa) AND domain-specific fine-tuning on representative labelled examples. Neither fix alone is sufficient.

**Question 4 — LLM vs fine-tuned specialist for high-volume classification**

Your team is building a sentiment analysis pipeline for 85,000 customer reviews per month across 6 languages. A colleague suggests using GPT-4 for all of them because "it understands context better." You propose a fine-tuned multilingual model instead. What is your quantitative and qualitative argument?

> **Simple Explanation:** A specialist who knows your subject cold is faster, cheaper, and more consistent than a brilliant generalist working from first principles each time — for a well-defined task with a fixed output schema. Use the generalist when the task is ambiguous or requires broad world knowledge.
>
> **Detailed Answer:** Quantitative: at approximately 150 tokens per review on average, 85,000 reviews represent 12.75 million tokens. At GPT-4 pricing, this costs approximately €400–600/month at current rates, depending on whether you batch or use real-time API calls. A fine-tuned multilingual model running on GPU cloud inference (e.g., a quantised XLM-RoBERTa on A10G instances) costs approximately €80–150/month for the same volume. Additionally, fine-tuned models can be scaled horizontally for peak loads without increasing per-token costs. Qualitative: for a well-defined classification task (positive/neutral/negative sentiment), a fine-tuned task-specific model is more consistent — the same review submitted twice will always receive the same label, whereas LLM outputs can vary due to sampling. The fine-tuned model is also more auditable: you can inspect which tokens drive the classification decision using attribution methods (SHAP, integrated gradients). For enterprise governance, this auditability may be required. GPT-4 would be the right choice if the task were more ambiguous (nuanced emotional analysis, detecting sarcasm, cross-language cultural nuance) where the general model's breadth outweighs the cost and consistency advantages of a specialist model.
>
> **Architecture Takeaway:** For high-volume, well-defined classification with a fixed output schema, fine-tuned specialist models beat general LLMs on cost (3–5×), consistency (deterministic output), and auditability (token attribution). Reserve LLMs for tasks where flexibility and world knowledge outweigh those advantages.

**Question 5 — ViT vs CNN spatial processing**

Explain how the ViT (Vision Transformer) architecture applies the transformer attention mechanism to images, and what this means for how it processes spatial information differently from a CNN.

> **Simple Explanation:** A CNN reads an image like a spotlight scanning a stage — sequentially covering small areas, building up the big picture through many passes. A ViT cuts the image into tiles and lets every tile have a conversation with every other tile simultaneously — global context from the start, but it needs a lot of training examples before those conversations are meaningful.
>
> **Detailed Answer:** A ViT divides an image into fixed-size patches (typically 16x16 pixels) and linearly projects each patch into an embedding vector. These patch embeddings, along with a learnable position embedding (to encode spatial location), are treated as a sequence — analogous to word tokens in a text transformer. Multi-head self-attention is then applied across all patches: each patch can attend to every other patch in the image. This means a ViT can, in principle, model global spatial relationships from the very first layer — a patch in the top-left corner can directly attend to a patch in the bottom-right corner without information having to flow through intermediate layers. A CNN, by contrast, uses local convolutional filters whose receptive field grows only as you go deeper — the top-left and bottom-right corners cannot communicate until the filter has been applied many times across many layers. The practical implication: ViTs are better at tasks requiring global context understanding (detecting an object based on its relationship to the rest of the image) and work well with high-resolution inputs where long-range spatial dependencies matter. CNNs are more data-efficient (the local inductive bias helps them learn with less data) and faster to run on small inputs.
>
> **Architecture Takeaway:** ViTs are better for global spatial reasoning and integrate naturally with language models (making them the foundation for vision-language models). CNNs are faster and more data-efficient for edge deployment. Choose based on whether global context or deployment efficiency is the binding constraint.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers contrastive learning theory, production CV engineering patterns, and LLM-era NLP guidance in depth. Section 8.3 (LLM-era NLP) is the most immediately applicable for architects. It is safe to read only 8.3 on a first pass.

### 8.1 Contrastive Learning: The Bridge Between CV and NLP Embeddings

Contrastive learning is the training paradigm that underpins both modern image embedding models (CLIP, SigLIP) and modern text embedding models (Sentence-BERT, E5, text-embedding-ada-002). Understanding it shows why the same architectural principle works for both modalities.

**The idea**: train a model by showing it pairs of examples and teaching it to embed similar pairs close together and dissimilar pairs far apart in the embedding space.

**In CLIP**: the training data is 400 million image-text pairs from the internet. The model trains an image encoder and a text encoder simultaneously. The objective: the embedding of an image should be close to the embedding of its corresponding caption, and far from the embeddings of all other captions in the batch. This is a contrastive training objective (which teaches the model to pull similar examples together and push dissimilar ones apart in the embedding space).

The result: a shared embedding space where images and text about the same thing are close together. This is what enables zero-shot image classification (embed the class names as text, embed the image, find the nearest text embedding) and visual search (embed the query text, find the nearest image embeddings).

**In Sentence-BERT**: similar principle but for text-text pairs. Training data: sentence pairs with semantic similarity labels (same meaning, different meaning, related meaning). The model learns to embed sentences with similar meaning close together.

**Why contrastive learning generalised**: it does not require careful label engineering. Labels come for free from the natural pairing of data (image + its caption, two sentences from the same document, two augmentations of the same image). This is what allowed training on internet-scale data with minimal supervision.

### 8.2 Production CV Patterns

Three patterns that appear repeatedly in enterprise CV deployments:

**Sliding window inference for large images**: if you need to detect small objects in high-resolution images (defects in manufactured components, small text in scanned documents), process the image by sliding a window across it and running detection on each window. The detection results from all windows are then combined with non-maximum suppression (NMS) to remove duplicate detections.

**Test-time augmentation (TTA)**: run inference on multiple augmented versions of the same image (flipped, slightly rotated, colour-adjusted) and average the predictions. This reduces variance in edge cases. Used in production for high-stakes classification where accuracy is more important than throughput.

**Model ensembling**: run multiple models on the same image and combine predictions. Three models voting on a classification decision is more robust than any single model. Used in contexts where model errors are costly and inference can be done offline. Not appropriate for real-time applications where latency is critical.

**Edge vs cloud inference**: for real-time video processing (retail theft detection, manufacturing line inspection), cloud inference introduces unacceptable latency. Quantised models (INT8 or INT4) running on edge hardware (NVIDIA Jetson, Apple Neural Engine, Google Edge TPU) are the appropriate architecture. The trade-off: smaller models, lower accuracy, lower latency, no cloud cost, no cloud data egress.

### 8.3 NLP in the LLM Era: When to Use What

The explosion of instruction-tuned LLMs has created a genuine tension: for many NLP tasks, a general LLM can do the job adequately through prompting alone, while a fine-tuned specialist model does the job better for a specific task.

**Use a general LLM when**:
- The task is ambiguous or open-ended (summarisation, generation, complex reasoning)
- You need to handle multiple tasks with a single model (multi-task scenarios)
- Your labelled data is sparse (LLMs can do zero-shot and few-shot classification)
- The task requires world knowledge beyond what a small model contains
- Volume is low enough that per-token pricing is not prohibitive

**Use a fine-tuned specialist model when**:
- The task is well-defined with a fixed output schema (classification, NER, structured extraction)
- Volume is high (cost per inference matters)
- Consistency is required (same input must always produce same output)
- Latency is critical (sub-100ms inference in a synchronous user-facing pipeline)
- The domain vocabulary is highly specialised and poorly represented in general LLM training
- Auditability is required (regulated industries where token attribution is necessary)

**The hybrid pattern**: use an LLM to generate labelled training data for a specialist model. Label 100 examples manually, use the LLM to generate or augment to 10,000 examples (with human review of a sample for quality), train the specialist model on the augmented data. This "LLM as labeller" pattern is increasingly common and dramatically reduces the cost of building task-specific models for new domains.

---

## 9. Key Takeaways

- CV and NLP share the same fundamental architectural principles — CNNs for images are the visual equivalent of embedding models for text, object detection is the visual equivalent of named entity recognition, and transfer learning via fine-tuning works the same way in both domains because deep models learn transferable hierarchical representations.

- The cascade from pre-trained model to fine-tuned specialist is the dominant production pattern in both CV and NLP — start with a general pre-trained backbone, add a task-specific head, fine-tune on domain-labelled data; this works whether you are classifying product images, extracting invoice fields, or detecting customer sentiment.

- Tokenisation is a cost and context architecture concern: different tokenisers produce different token counts for the same input, multilingual and domain-specific text is often tokenised less efficiently, and the choice of embedding model and tokeniser directly determines context window consumption and API cost at scale.

- Vision-language models (GPT-4V and equivalents) collapse the CV/NLP boundary for complex document understanding tasks — but for high-volume, well-defined tasks like invoice extraction or sentiment classification, fine-tuned specialist models are 5–10x cheaper per inference and produce more consistent, auditable outputs.

- The "LLM as labeller" pattern makes fine-tuned specialist models accessible even without large existing labelled datasets: use an LLM to bootstrap label generation, review a sample for quality, and train a faster, cheaper, more consistent specialist model on the result — capturing the best of both worlds.
