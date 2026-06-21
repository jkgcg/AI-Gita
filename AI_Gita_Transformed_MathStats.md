# Math & Stats for Architects
### AI Gita — Transformed Learning Module

---

## 1. What Is It (Plain English)

Math and statistics are the language that machine learning models use internally. You do not need to speak this language fluently to be an effective AI architect. You need to be able to read it well enough to understand what someone is telling you, to catch when something does not make sense, and to ask the right questions.

Think of it this way: you do not need to know how an internal combustion engine works at the level of thermodynamic cycles to drive a car well. But if you know that a car engine converts fuel into motion through controlled explosions in cylinders, you understand why it overheats, why it needs oil, and why a diesel engine behaves differently from a petrol one. That level of understanding is what this module gives you for AI math.

The math behind AI lives in three clusters:

- **Linear algebra** — how information is represented and compared (vectors, matrices, dot products, cosine similarity)
- **Probability and statistics** — how uncertainty is modelled and decisions are made under uncertainty (distributions, Bayes' theorem, entropy)
- **Calculus/Optimisation** — how models learn by improving themselves over time (gradient descent, loss functions)

You will encounter all three when working with AI systems. This module tells you what you need to understand intuitively, when you will encounter it, and what you can safely leave to the data scientists on your team.

---

## 2. Why Should I Care

### For Solution Architects

When you are selecting a vector database, configuring a similarity search, or evaluating why a recommendation engine is surfacing the wrong products, you are working with linear algebra — specifically cosine similarity and dot products. You do not need to derive these formulas. You need to understand that "similarity" in AI is not the same as "equality", and that two things can be close in meaning while having no words in common.

When a data scientist says "the model is overfitting" or "the loss is not converging", you are in the territory of gradient descent and loss functions. Understanding what these mean at a conceptual level lets you make better trade-off decisions: more training time, more data, different architecture.

When your AI system gives you confidence scores — "this customer has a 73% probability of churning" — you are reading the output of a probability model. Knowing what that means (and what it does not mean) helps you set thresholds, handle false positives, and explain outputs to business stakeholders.

### For Enterprise Architects

The language of AI governance is the language of probability and statistics. Model bias, fairness metrics, calibration, distributional shift — all of these are statistical concepts. If you are responsible for AI governance policies, you need enough statistical literacy to evaluate whether a vendor's claims about their model are credible, whether an evaluation framework is measuring the right thing, and whether a model's confidence scores can be trusted.

Linear algebra appears in your architecture decisions when you are dealing with embedding-based systems: semantic search, RAG pipelines, recommendation engines, knowledge graphs. The dimension of an embedding space, the choice of similarity metric, and the cost of indexing millions of vectors are all architecture-level concerns with mathematical underpinnings.

Gradient descent matters to you primarily as a training-time concern: it determines how long training takes, how expensive it is, and whether a fine-tuned model is likely to degrade on your specific data distribution.

---

## 3. Think About It Like This

Imagine your enterprise knowledge base as a vast library where every book has been assigned a GPS coordinate in a 1,000-dimensional space. Books about the same topic cluster together, even if they use completely different words. Finding "similar" books is not about keyword matching — it is about finding the nearest GPS coordinates.

This is exactly what embedding spaces do. Every piece of text, every product image, every customer profile gets converted into a set of coordinates. "Similarity" means "nearby in this coordinate space." The mathematical operation that measures closeness between two sets of coordinates is the dot product — and when you normalise it so that the size of the vectors does not matter, only the direction, you get cosine similarity.

Gradient descent is what happens when you imagine standing on a hilly landscape in thick fog, trying to reach the lowest valley. You cannot see the whole landscape. You can only feel which direction the ground slopes under your feet right now. You take a small step downhill, check again, take another step. Over millions of steps, you reach the bottom. That "checking which direction is downhill" is what the gradient is — it is the slope of the error landscape, and descent is the process of following it down.

**For probability and Bayes:** Think of a weather forecaster. They don't say 'it will rain' — they say '70% chance of rain.' That number reflects their prior belief (it's usually dry this time of year) updated by new evidence (a pressure system moving in). When AI models output probabilities, they're doing the same thing: combining what they learned during training with the specific evidence in your prompt.

---

## 4. Step-by-Step Walkthrough

### 4.1 Linear Algebra Intuitions

> **Explain Like I'm an Architect**
>
> Imagine your enterprise knowledge base as a vast library where every book has been given a GPS coordinate in a 1,000-dimensional space. Books about the same topic cluster together, even if they use completely different words. Finding "similar" books is not about keyword matching — it's about finding the nearest GPS coordinates. This is what vectors and cosine similarity do: they give every piece of information a location in a shared coordinate space, so "how similar are these two things?" becomes "how close are these two coordinates?" You encounter this every time you work with a vector database, semantic search, or embedding-based recommendation system.
>
> **Why this matters architecturally:** When you configure a vector database's distance metric (cosine vs inner product vs Euclidean), you're making a decision about how "closeness" is measured. Cosine similarity compares direction, not magnitude — it's robust to document length variation and is the right default for semantic search.

**Vectors** are ordered lists of numbers. In AI, almost everything becomes a vector: a word, an image, a product, a customer. The numbers capture features or properties of the thing, placed in a shared coordinate system so that similar things end up with similar numbers.

A word embedding might look like: `[0.23, -0.71, 0.55, 0.08, ...]` across 768 dimensions. You will never read these numbers directly. What matters is that words used in similar contexts — "king" and "monarch", "quick" and "fast" — end up with coordinates that are numerically close to each other.

**Dot product** is the operation that takes two vectors and returns a single number representing how aligned they are. Mathematically it is the sum of element-wise products. Intuitively: if two vectors point in the same direction, their dot product is large and positive. If they point in opposite directions, it is large and negative. If they are perpendicular (completely unrelated), it is zero.

This is the core of attention in transformers. When a model decides how much a word "attends to" another word, it is computing a dot product between their vector representations.

**Cosine similarity** is the dot product normalised so that the magnitude (length) of the vectors does not affect the result — only the angle between them. This matters because longer texts naturally produce larger vectors. By normalising, you compare direction, not size. Cosine similarity of 1.0 means identical direction (perfectly similar). 0 means perpendicular (unrelated). -1 means opposite.

For architects: most vector databases (Pinecone, Weaviate, pgvector) use cosine similarity or inner product as their default distance metric. The choice of metric affects what "nearest neighbour" means and, therefore, the quality of your semantic search results.

### 4.2 Probability Basics

> **Explain Like I'm an Architect**
>
> Think of a fraud detection model as a weather forecaster. It doesn't say "this transaction is fraud" — it says "73% probability of fraud." That number combines what the model learned during training (how common fraud is, what patterns indicate it) with the specific evidence in this transaction. The critical insight for architects: a "73% confidence" score is only meaningful if the model has been *calibrated* — that is, when it says 73%, it should actually be right about 73% of the time. Many models are not calibrated out of the box. And when fraud is rare (0.5% of transactions), even a 92% confidence fraud flag may have more false positives than true positives — because the base rate dominates.
>
> **Why this matters architecturally:** Never accept model accuracy as the sole metric in imbalanced domains (fraud, medical diagnosis, rare events). Always ask for precision and recall at your operating threshold, and verify that confidence scores have been calibrated on a validation set.

**Probability distributions** describe how likely different outcomes are. The two you encounter most in AI:

- **Normal (Gaussian) distribution**: the bell curve. Values cluster around a mean, taper off symmetrically. Many natural quantities follow this distribution, which is why so many ML algorithms assume it.
- **Bernoulli/Categorical distribution**: probability of discrete outcomes. A binary classifier produces a Bernoulli distribution — probability of class A vs class B. A multiclass classifier produces a categorical distribution over all classes.

**Bayes' theorem** states that your updated belief about something (after seeing evidence) equals your prior belief multiplied by how likely you were to see that evidence if your belief were true, divided by how likely you were to see the evidence at all.

**Quick example:** Your fraud detection model has 99% accuracy. But only 1 in 1,000 transactions is genuinely fraudulent. If the model flags a transaction, the probability it is actually fraud is still only ~9% — because the base rate of fraud is so low that false positives dominate. This is why base rate always matters, regardless of model accuracy.

For architects: Bayesian reasoning is the conceptual foundation for how AI systems handle uncertainty. When a fraud detection model returns "92% probability of fraud", it has combined a prior (how common fraud is in your customer base) with the likelihood of the specific transaction pattern. If your business has very low fraud rates, even a 92% score may have many false positives — this is why base rate matters more than model accuracy in imbalanced domains.

**Entropy** measures uncertainty or information content. High entropy means high uncertainty — the probability is spread across many outcomes. Low entropy means you are confident — one outcome dominates. This concept underpins loss functions (cross-entropy), decision trees (information gain), and token sampling strategies in LLMs (temperature and top-p are entropy-controlling parameters).

### 4.3 Gradient Descent Intuition

> **Explain Like I'm an Architect**
>
> Imagine standing in a mountain range at night in thick fog, trying to reach the lowest valley. You can't see more than a step ahead. Your only tool: you can feel which direction the ground slopes under your feet. So you take a small step downhill, check again, take another step. Over millions of steps, you reach the bottom. That's gradient descent: the model takes a small step in whatever direction reduces its error, repeating until it converges. The *learning rate* is how large each step is — too large and you overshoot the valley (the model never converges), too small and you never get there (training takes forever or gets stuck).
>
> **Why this matters architecturally:** When a fine-tuning project fails silently — loss doesn't decrease, or oscillates — the first question is almost always "is the learning rate wrong?" Fine-tuning LLMs requires careful learning rate selection; it's the most consequential hyperparameter and the most common point of failure in internal model training projects.

Training a model means finding the settings (weights) that produce the least error on your training data. The error is measured by a **loss function** — a formula that takes the model's predictions and the actual answers, and produces a single number representing how wrong the model is.

Gradient descent is the algorithm that iteratively adjusts the model's weights to reduce this loss. Each iteration:

1. Make predictions on a batch of training examples
2. Calculate the loss (how wrong the predictions are)
3. Calculate the gradient (which direction each weight needs to move to reduce loss)
4. Adjust each weight by a small amount in that direction (the **learning rate** controls how small)
5. Repeat

For architects: the learning rate is the most consequential hyperparameter. Too large and the model overshoots — it bounces around the loss landscape and never settles. Too small and training takes forever and may get stuck in a local minimum. This is why fine-tuning LLMs requires careful learning rate selection, and why it is a common point of failure in internal model training projects.

**Stochastic gradient descent (SGD)** and **Adam** are variants that estimate the gradient from small batches rather than the full dataset, and add momentum to avoid getting stuck. Adam is the default for most deep learning. SGD with momentum is often preferred for fine-tuning.

### 4.4 The Attention Formula (Intuition Level)

The attention mechanism, the core of transformers, computes a weighted average of values based on the similarity between queries and keys.

Concretely: for every word in a sentence, attention asks "which other words are most relevant to understanding this word right now?" It computes dot-product similarities between the current word (the query) and every other word (the keys), converts these similarities into weights using softmax (so they sum to 1), and then takes a weighted average of the value representations.

The formula is: `Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V`

What this means in plain English:
- Compute similarity scores between every query and every key (QK^T)
- Scale down by the square root of dimension to prevent the dot products from getting too large (/ sqrt(d_k))
- Convert scores to probabilities that sum to 1 (softmax)
- Use these probabilities as weights to blend the value vectors (multiply by V)

For architects: the "quadratic scaling" problem you hear about — why attention is expensive for long contexts — comes from the QK^T step. Every word must be compared to every other word, so the cost scales as sequence length squared. This is why techniques like sliding window attention, sparse attention, and linear attention approximations exist.

### 4.5 Softmax vs Sigmoid — Decision Guide

**Sigmoid** maps any number to a value between 0 and 1. Use it for **binary classification** — one output neuron, one decision (yes/no, fraud/not-fraud, click/no-click). The output is the probability of the positive class.

**Softmax** takes a vector of numbers and converts them into a probability distribution that sums to 1. Use it for **multiclass classification** — multiple output neurons, one winner (which of these 10 product categories does this item belong to?).

The rule of thumb for architects evaluating model outputs:
- Single probability score (0–1): sigmoid output, binary decision
- Vector of probabilities summing to 1: softmax output, multiclass decision
- Multiple independent probabilities that do not sum to 1: sigmoid applied independently to each output, multi-label decision (an item can belong to multiple categories simultaneously)

---

## 5. Enterprise Example: Cosine Similarity for Product Matching in a Retail Catalogue

**Scenario**: A global retail group runs a product catalogue of 4.2 million items across 18 categories. Product teams from acquired brands need to map their local catalogue items to the global master catalogue. Manual mapping takes 3–4 weeks per brand integration. The target: automate 80% of matches with high confidence.

**The architecture**: Each product in both catalogues is embedded using a fine-tuned multilingual embedding model. The embedding captures product name, description, category, and key attributes. Each embedding is a 768-dimensional vector stored in a vector database (Weaviate, chosen for its native multi-tenancy).

**How cosine similarity works here**: When a new product arrives ("Men's Lightweight Trail Running Shoe, Breathable Mesh Upper, EU 42"), its embedding is computed and compared against every product in the master catalogue using cosine similarity. Products with similarity > 0.92 are auto-matched. Products with similarity 0.82–0.92 are flagged for human review. Below 0.82, the item is treated as a new unique product.

**What the architects had to decide**:
- Embedding model: domain-specific fine-tuned model outperformed generic sentence transformers by 8% on internal evaluation — but required a fine-tuning pipeline and labelled match data
- Similarity threshold: set through analysis of the precision-recall tradeoff on a held-out set of known matches; 0.92 gave 96% precision at 70% recall for auto-matching
- Vector index: HNSW (Hierarchical Navigable Small World) index for approximate nearest neighbour search, giving millisecond search over 4.2M items
- Re-ranking: a lightweight cross-encoder re-ranked the top-20 cosine similarity candidates before the final decision, improving precision by 4%

**The outcome**: 83% of mappings automated at 96% precision. Brand integration time reduced from 3–4 weeks to 3–4 days.

---

## 6. Architecture Perspective

**Embedding pipelines are infrastructure, not an afterthought.** Cosine similarity only works as well as the quality of the embeddings. The embedding model, the data fed into it, the preprocessing pipeline, and the re-embedding strategy when items change are all architecture concerns. A brittle embedding pipeline is as damaging as a brittle data pipeline.

**Dimensionality is a scaling decision.** 768-dimensional embeddings are standard for BERT-class models. 1536-dimensional embeddings are standard for OpenAI text-embedding-ada-002. Higher dimensionality generally means better semantic capture, but higher storage cost, higher compute cost for similarity search, and higher memory requirement for the vector index. For a 10M-item catalogue with 1536-dimensional float32 embeddings, the raw vector storage alone is ~60GB.

**Normalise before you index.** Most vector databases can apply cosine similarity natively, but if you normalise your embeddings to unit length before insertion, cosine similarity becomes equivalent to inner product — which is faster to compute on most hardware (no square root needed). This is a standard production pattern.

**Gradient descent failure modes you need to recognise**:
- *Loss not decreasing*: learning rate is too low, data quality issue, or wrong loss function
- *Loss oscillating wildly*: learning rate is too high
- *Loss decreasing on training but not validation*: overfitting — the model is memorising training data
- *NaN loss*: numerical instability, often from too-large learning rate or unscaled inputs

**Probability calibration matters for decisions.** A model that says "73% confidence" should be right 73% of the time when it says that. Many models are not calibrated — they are overconfident or underconfident. If your AI system is making decisions based on probability thresholds, verify that the model has been calibrated (Platt scaling, isotonic regression) on a held-out validation set.

---

## 7. Check Yourself

**Question 1 — Interpreting cosine similarity scores**

You are comparing two product descriptions using cosine similarity and get a score of 0.31. A colleague says "that's basically zero — they're unrelated." Is your colleague correct? What does a score of 0.31 actually mean?

> **Detailed Answer:** Not necessarily. Cosine similarity ranges from -1 to 1. In practice, for text embeddings comparing different topics, 0.31 is on the lower end but not zero. Two truly unrelated documents often score 0.1–0.3 because their embeddings share some general-language components. The correct interpretation requires knowing the distribution of scores in your specific embedding space. A score that is low *relative to known-similar pairs in your domain* is more informative than any absolute threshold. The colleague is applying a naive interpretation — context and calibration always matter.
>
> **Simple Explanation:** A score of 0.31 is like saying two cities are "not that close" without knowing whether you're measuring in metres or light-years. Without the distribution of scores for your domain, a raw cosine similarity number tells you little.
>
> **Architecture Takeaway:** Never set similarity thresholds based on absolute values alone. Calibrate them against a labelled set of known-similar and known-dissimilar pairs in your specific domain before deploying.

**Question 2 — Diagnosing overfitting from loss curves**

Your fine-tuned model has a training loss that decreases smoothly from 2.1 to 0.3 over 10 epochs. The validation loss decreases from 2.1 to 0.8, then stops improving and begins rising from epoch 7 onward. What is happening and what should you do?

> **Detailed Answer:** The model is overfitting — it is memorising the training data rather than learning generalisable patterns. The optimal stopping point is the epoch where validation loss was lowest (epoch 6–7). Remedies: use early stopping (halt training when validation loss stops improving), apply regularisation (dropout, weight decay), reduce model complexity, or increase training data volume. In production, save the checkpoint from epoch 6, not epoch 10.
>
> **Simple Explanation:** The model got so good at the practice exam that it memorised the answers instead of learning the subject. It then fails on any new exam. Early stopping is like saying "you've peaked — stop studying and take the test now."
>
> **Architecture Takeaway:** Always monitor validation loss during fine-tuning, not just training loss. Use early stopping and checkpoint the best-validation-loss epoch. A fine-tuning job that only reports training loss is a red flag.

**Question 3 — Why accuracy is misleading in imbalanced domains**

A vendor shows you a fraud detection model with 99.2% accuracy. Your fraud rate is 0.5% (5 in 1,000 transactions). Should you be impressed by this accuracy figure?

> **Detailed Answer:** No. A model that classifies every transaction as legitimate would achieve 99.5% accuracy with zero fraud detection. The 99.2% figure is essentially meaningless here — it tells you nothing about fraud detection quality. The relevant metrics are: precision (of all flagged fraud, what fraction is actually fraud), recall (of all actual fraud, what fraction is caught), and F1 or F-beta score. Ask for the model's performance at specific operating points — for example, at a threshold that catches 90% of fraud, how many false positives does it generate per day?
>
> **Simple Explanation:** In a room of 1,000 people where only 5 are guilty, a guard who arrests nobody achieves 99.5% accuracy. That's not a good guard. The same logic applies to fraud detection.
>
> **Architecture Takeaway:** For any AI system operating in an imbalanced domain (fraud, safety events, rare defects), require precision and recall at your operating threshold — not accuracy. Accuracy alone is a vendor red flag in these domains.

**Question 4 — Euclidean distance vs cosine similarity**

An engineer proposes using Euclidean distance instead of cosine similarity for your product matching system. In what scenario would Euclidean distance give worse results, and why?

> **Detailed Answer:** Euclidean distance is affected by the magnitude (length) of vectors, not just their direction. If your embedding model produces longer vectors for longer product descriptions, Euclidean distance would penalise a detailed description even if it is semantically identical to a shorter one. Cosine similarity measures only the angle between vectors, ignoring their length — making it more robust to description length variation. The practical workaround: normalising all vectors to unit length before indexing makes Euclidean distance equivalent to a monotonic transformation of cosine similarity, so both give the same ranking. Without normalisation, cosine similarity is almost always the better choice for semantic matching.
>
> **Simple Explanation:** Euclidean distance measures how far apart two points are in space. Cosine similarity measures the angle between them. For comparing meaning (not just position), angle is what matters — a detailed description and a short one about the same product should be "close" regardless of how long each is.
>
> **Architecture Takeaway:** Default to cosine similarity for semantic matching tasks. If using Euclidean distance, always normalise embeddings to unit length first — this is a standard production pattern and most vector databases support it natively.

**Question 5 — Softmax vs sigmoid for multi-label classification**

You are asked to review a model that uses softmax output for a product categorisation task. The product can belong to multiple categories simultaneously (a "running shoe" can also be "trail", "waterproof", and "sale"). Is softmax the right choice?

> **Detailed Answer:** No. Softmax is designed for mutually exclusive categories — it forces all outputs to sum to 1, meaning selecting one category reduces the probability mass available for all others. For multi-label classification (where multiple labels can be simultaneously true), you need independent sigmoid outputs for each label. Each output neuron independently predicts the probability of that label being present, and the probabilities do not need to sum to 1. The loss function also changes: from categorical cross-entropy (softmax case) to binary cross-entropy applied to each label independently (sigmoid multi-label case).
>
> **Simple Explanation:** Softmax is like a competition where only one winner is allowed. Sigmoid is like a checklist where any number of boxes can be ticked. A running shoe that is also trail-ready, waterproof, and on sale needs a checklist, not a competition.
>
> **Architecture Takeaway:** When reviewing ML model designs for classification tasks, always ask: are the categories mutually exclusive? If not, softmax is incorrect — use sigmoid with binary cross-entropy per label. Getting this wrong silently degrades model quality.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers cross-entropy loss, KL divergence, and information theory. These underpin LLM training and evaluation but are not required for most architecture decisions. It is safe to skip on a first pass and return here later.

### 8.1 Cross-Entropy Loss

Cross-entropy is the loss function used to train classifiers. It measures the difference between the model's predicted probability distribution and the true distribution.

For binary classification: `L = -(y * log(p) + (1-y) * log(1-p))`

Where y is 0 or 1 (the true label) and p is the predicted probability of class 1.

Intuitively: if the true label is 1 and the model predicts p = 0.99, the loss is tiny (-log(0.99) ≈ 0.01). If the model predicts p = 0.01, the loss is huge (-log(0.01) ≈ 4.6). The logarithm creates an asymmetry that severely punishes confident wrong answers.

For architects: cross-entropy loss is why models learn to be well-calibrated when properly trained. The training signal pushes the model toward accurate probabilities, not just correct classifications. A model trained with cross-entropy that consistently gives 90% confidence when it is right 60% of the time has not been properly trained (or has been trained on a different distribution than you are evaluating on).

**Categorical cross-entropy** generalises this to multiple classes: `L = -sum(y_i * log(p_i))` where y is a one-hot vector and p is the softmax output vector. For a correct prediction, only the term for the true class contributes to the loss.

### 8.2 KL Divergence

Kullback-Leibler (KL) divergence measures how different one probability distribution is from another. It answers: "if I use distribution Q as an approximation of the true distribution P, how much information am I losing?"

`KL(P || Q) = sum(P(x) * log(P(x)/Q(x)))`

Key properties:
- KL divergence is not symmetric: KL(P || Q) ≠ KL(Q || P) in general
- KL divergence is zero when P and Q are identical
- KL divergence is non-negative (you always lose information by using an approximation)

Where architects encounter KL divergence:
- **RLHF and PPO**: the KL penalty term in reinforcement learning from human feedback keeps the fine-tuned model close to the original policy, preventing the model from "reward hacking" by producing nonsensical outputs that score highly on the reward model
- **VAEs (Variational Autoencoders — a type of generative model that learns compressed data representations; encountered when reviewing vendors offering image synthesis or anomaly detection pipelines)**: the training objective includes a KL divergence term between the latent distribution and a standard normal distribution — this is what forces the latent space to be smooth and interpolable
- **Knowledge distillation**: training a smaller student model to match the probability distribution of a larger teacher model uses KL divergence as the training signal

### 8.3 Information Theory Basics

Information theory (Claude Shannon, 1948) provides the mathematical foundation for understanding what "information" means quantitatively.

**Entropy** (Shannon entropy): `H(X) = -sum(p(x) * log2(p(x)))`

This measures the average information content (surprise) of a random variable. High entropy means outcomes are unpredictable (maximum uncertainty). Low entropy means one outcome is very likely (minimum uncertainty).

For architects, information theory explains:
- **Why LLM temperature works**: at temperature 0, the model always picks the highest-probability token (zero entropy in the sampling distribution — fully deterministic). At temperature 1, the model samples from its learned distribution (natural entropy). At temperature > 1, the distribution is flattened (higher entropy — more random, more creative).
- **Why decision trees split on information gain**: at each node, the tree picks the feature that most reduces entropy in the target variable — the feature that tells you the most about the outcome.
- **Why tokenisation efficiency matters**: BPE tokenisation is essentially a compression algorithm. More efficient tokenisation (fewer tokens per unit of meaning) means less context window consumption and lower inference cost. This is directly connected to information-theoretic compression principles.

**Mutual information** measures how much knowing one variable tells you about another. It is the information-theoretic equivalent of correlation, but captures non-linear dependencies. Used in feature selection (which features share the most information with the target variable?) and in evaluating whether two model representations have learned the same things.

---

## 9. Key Takeaways

- Cosine similarity measures the angle between two vectors, making it the right metric for semantic similarity — two things can be meaningfully similar even if they share no words, as long as their embeddings point in the same direction.

- Gradient descent is how models learn: repeatedly measuring the error (loss), computing which direction to adjust the weights, and taking a small step in that direction — the learning rate controls the step size and is the most critical hyperparameter to get right.

- Probability calibration is an architectural concern: a model's confidence score is only meaningful if the model has been calibrated — otherwise "73% confidence" is a number, not a reliable probability, and thresholds set against it will produce unpredictable system behaviour.

- Softmax is for one-of-many (mutually exclusive classes), sigmoid is for yes/no (binary or multi-label where categories are independent) — choosing the wrong output activation changes both the training objective and the interpretation of output scores.

- Cross-entropy loss and KL divergence both appear in LLM training workflows (RLHF, fine-tuning, distillation) and understanding them at the intuition level — "how far is this distribution from the target distribution?" — helps you reason about why fine-tuned models drift, why RLHF works, and how knowledge distillation compresses capability.
