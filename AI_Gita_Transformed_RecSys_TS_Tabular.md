# Recommendation Systems, Time Series, and Tabular Prediction
### AI Gita — Transformed Learning Module

---

## 1. What Is It (Plain English)

Three types of AI problems appear constantly in enterprise data products, and they look superficially similar — all three take data and make predictions — but each models a fundamentally different kind of structure in the world.

**Structured prediction (tabular)**: you have a table of facts about an entity, and you want to predict a property of that entity. Will this customer churn? What is the likely basket size for this transaction? Is this order likely to be returned? The data is structured, the prediction is about a single point in isolation.

**Time series forecasting**: you have a sequence of measurements over time, and you want to predict what comes next. How many units of SKU-9823 will be sold next week? What will server load be at 3pm tomorrow? The key is that time ordering matters — the pattern is sequential, and yesterday's value tells you something about tomorrow's.

**Collaborative filtering (recommendation systems)**: you have a sparse matrix of interactions between users and items, and you want to predict which items a user would like that they have not yet seen. The key is that the signal comes not from the user's own properties in isolation, nor from the item's properties in isolation, but from the pattern of who-liked-what across the whole population.

These are three different problem structures, and they call for different approaches. A time series approach applied to a recommendation problem will fail because it cannot capture the cross-user interaction signal. A collaborative filtering approach applied to demand forecasting will fail because it cannot capture temporal trends. The decision framework is: what is the structure of the signal you are trying to exploit?

---

## 2. Why Should I Care

### For Solution Architects

When a business asks for "an AI system that predicts demand and personalises promotions", you are actually looking at at least two distinct AI problems: demand forecasting (time series) and promotion personalisation (recommendation). They may share data infrastructure but they have different modelling requirements, different latency requirements, different retraining cadences, and different evaluation metrics.

Conflating them into a single "AI system" creates a specification that is impossible to build coherently. Your job as an architect is to decompose the problem correctly before the team starts building.

The cascade pipeline pattern — retrieval then ranking then filtering — is the most important structural concept in production recommendation systems. It determines how you partition the problem into compute tiers, how you balance latency and quality, and where different types of models plug in. Understanding this pattern lets you design the system architecture without needing to understand the specific ML models in detail.

### For Enterprise Architects

Recommendation systems are high-visibility AI systems — customers interact with them directly, and their quality (or poor quality) is immediately visible. Enterprise risk in recommendation systems typically comes from three sources:

1. **Filter bubbles and reinforcing loops**: recommendation systems that optimise for engagement tend to show users more of what they already like, gradually narrowing their exposure. In a retail context, this can reduce basket diversity and stall cross-sell.

2. **Cold start**: new users and new items cannot be recommended effectively because there is no interaction history. This is a known structural limitation that must be designed around.

3. **Feedback loop contamination**: if only recommended items are ever purchased, the training data reflects what was recommended, not what customers would have chosen in an unbiased environment. This can cause the model to reinforce its own biases over time.

For time series, the enterprise risk is primarily forecast accuracy at scale — a 5% error in a single store's demand forecast is a minor inefficiency, but a 5% systematic error across a 2,000-store network is a supply chain crisis.

---

## 3. Think About It Like This

Imagine a large city department store — the physical kind, with many floors — and think about how three different staff members use knowledge to help customers:

**The tabular prediction person** is the customer service agent who looks at a single customer's purchase history and account details and makes a decision: "This customer is a VIP member, they have not shopped in 60 days, and their last purchase was a full-price item. Probability of churn: high. Send the retention offer." They make decisions about individuals based on their factual profile.

**The time series person** is the stock room manager who watches the weekly sales pattern for each item and predicts how many to order. They know that umbrellas spike when it rains, that chocolate gift boxes peak in the two weeks before Valentine's Day, and that summer sportswear starts climbing in mid-April regardless of the weather. They exploit temporal patterns in the data.

**The recommendation system person** is the experienced sales associate who has watched thousands of customers and has noticed that customers who buy the Italian espresso machine almost always come back for the stainless steel milk frother and the single-origin beans — not because the products are similar, but because a certain type of person buys all three. They exploit the pattern of human taste across the population.

These three people use completely different knowledge to help customers. Asking the stock room manager to recommend personalised products, or asking the sales associate to forecast umbrella demand, would produce poor results. Same with their algorithmic counterparts.

---

## 4. Step-by-Step Walkthrough

### 4.1 Decision Framework: Which Approach Applies When

Before choosing a model, identify the structure of the problem. Use these questions:

| Question | If Yes → |
|---|---|
| Is the data a table of entity attributes with a target label? | Tabular (XGBoost, logistic regression) |
| Does the historical sequence of values over time matter for the prediction? | Time Series (ARIMA, LightGBM on lags, Temporal Fusion Transformer) |
| Does the prediction depend on patterns of interaction across many users/items? | Collaborative Filtering (Matrix Factorisation, Two-Tower) |
| Do you have rich content features (text, image) for items AND interaction data? | Hybrid: content features + collaborative filtering (Two-Tower with side features) |
| Do you have very little interaction data (cold start) but rich item content? | Content-based filtering (item embeddings from text/image, no collaboration needed) |

In practice, production systems often need more than one approach — for example, tabular prediction of "will this user click?" combined with collaborative filtering of "what items are most likely to be clicked?" combined with time series of "what items are trending this week?"

### 4.2 Tabular Prediction — The Structured Foundation

Tabular prediction is the most common ML task in enterprise settings. The input is a row in a database: a vector of features. The output is a label or a number.

Key characteristics:
- Features are hand-engineered from domain knowledge (days since last purchase, category preference ratios, engagement scores)
- Missing values are common and must be handled explicitly
- Feature relationships may be non-linear and involve interactions (the combination of "high value customer" and "recent engagement drop" matters more than either alone)
- Gradient-boosted trees (XGBoost, LightGBM) are the default choice

When tabular prediction feeds into a recommendation system: you can compute a "propensity score" for each user-item pair (how likely is user U to buy item I?) using tabular features about both the user and the item. This is essentially building a regression model per item — it scales only if you have a small item catalogue. For large catalogues, collaborative filtering is more efficient.

### 4.3 Time Series Forecasting

> **Explain Like I'm an Architect**
>
> In most ML tasks, the order your data was collected doesn't matter — a customer who bought trainers in January is just as useful for training as one who bought in December. Time series breaks this assumption completely: yesterday's sales tell you something about today's, and last year's November tells you something about this year's November. If you ignore the order and train a model on randomly shuffled dates, it would learn patterns that are literally impossible to observe in production (because the future won't be in your training data at serving time). This is why time series has its own model families, its own train/test split rules, and its own failure modes.
>
> **Why this matters architecturally:** Never let a data scientist use random train/test splits on time series data. Always split by time. This is not a best practice — it's a correctness requirement. A model evaluated with random splits will show optimistic metrics that collapse in production.

Time series problems have one structural property that distinguishes them from all other ML: **the order of data points is meaningful**. Last week's sales affect this week's sales. Yesterday's server load tells you something about today's. This temporal dependence violates the standard ML assumption that examples are i.i.d. (independently and identically distributed — a statistical assumption that each data point is drawn randomly with no dependency on others; time series data violates this, which is why specialist models are needed).

**Key concepts for architects**:

**Seasonality**: recurring patterns at fixed periods — daily (server load peaks at 9am), weekly (retail sales peak on weekends), annual (holiday demand spikes). Identifying and modelling seasonality correctly is the difference between a useful forecast and a dangerously wrong one.

**Trend**: the long-term direction of a time series — growing, shrinking, or stable. A trend component must be separated from seasonality to model each correctly.

**Lag features**: the most powerful features for time series models are simply the historical values of the target variable at various time offsets. Yesterday's sales, the same day last week's sales, the same day last year's sales — these are lag features, and they capture temporal dependence in a form that tree-based models can use.

**Approaches by scale**:
- Single series, statistical approach: ARIMA, Holt-Winters exponential smoothing. Fast, interpretable, no ML required. Good for forecasting one or a few series.
- Many series, ML approach: train one model (LightGBM + lag features) on all series simultaneously. The model learns cross-series patterns — for example, that items in the "sports" category all follow similar seasonal patterns. This is sometimes called a "global" forecasting model.
- Many series, complex dependencies: Temporal Fusion Transformer (TFT) or N-BEATS — deep learning models designed for multi-series forecasting with covariates. High complexity, high investment, justified only at scale or when covariates (weather, promotions, price) are important.

**Train/test split for time series**: never use random splits. Always split by time. Train on all data up to date T, test on data from T onwards. This prevents the model from "seeing the future" during training.

### 4.4 Collaborative Filtering — The Recommendation Core

> **Explain Like I'm an Architect**
>
> Collaborative filtering is the "people like you also bought..." mechanism. It doesn't need to understand why users like what they like — it just observes patterns. If 10,000 customers who bought espresso machines also bought stainless steel milk frothers, the system recommends frothers to the next espresso machine buyer — even though frothers and espresso machines share no obvious product attributes. The signal comes entirely from the aggregate behaviour of the population, not from any individual's profile or the product's description. This is fundamentally different from "find products with similar features" (content-based filtering) and "predict whether this specific customer will churn" (tabular prediction).
>
> **Why this matters architecturally:** Collaborative filtering requires interaction data (purchases, clicks, ratings) — you can't use it for a new product with no history (cold start problem). It also creates feedback loops: if the model only recommends popular items, popular items get more clicks, which makes the model recommend them even more. Design the system with deliberate exploration and diversity constraints from day one.

Collaborative filtering makes recommendations based on the pattern of interactions across many users and items. The core insight: if User A and User B have similar interaction patterns, and User B has interacted with Item X while User A has not, then Item X may be relevant to User A.

**Matrix factorisation**: the classic approach. Represent each user and each item as a vector of latent factors. The predicted interaction score is the dot product of the user vector and the item vector. Training finds the user and item vectors that best explain the observed interaction matrix. The vectors capture latent characteristics — a user vector with high values in certain dimensions might implicitly represent "prefers premium products in the outdoor category."

**Two-Tower model**: a deep learning evolution of matrix factorisation. Instead of learning a single flat vector per user/item, two separate neural networks (towers) process user features and item features respectively to produce embeddings. The similarity between embeddings predicts interaction. The towers allow rich feature inputs: user demographics, purchase history, contextual signals for the user tower; item text, images, metadata for the item tower.

**Why Two-Tower matters for architects**: the two towers can be computed separately and independently. User embeddings can be pre-computed once per hour or day. Item embeddings can be pre-computed for the entire catalogue. At serving time, the only operation needed is a nearest-neighbour lookup in embedding space — extremely fast and scalable. This architectural separation is what makes large-scale recommendation feasible.

**Cold start problem**: new users have no interaction history; their tower input is thin (only demographics, no behavioural signals). New items have no interactions; they can only be retrieved through content features. Mitigation strategies:
- For new users: start with popularity-based recommendations or content-based matching on demographics
- For new items: ensure the item tower uses rich content embeddings (text, image) so new items can be retrieved even without interaction history

### 4.5 The Production Recommendation Cascade Pipeline

> **Explain Like I'm an Architect**
>
> A retailer with 500,000 products cannot score every product for every user at the moment they visit the homepage — at even 1 microsecond per scoring, that would take 500 seconds. The cascade pipeline solves this with the same pattern you'd use for any high-volume narrowing problem: a fast, rough filter followed by a slower, precise scorer. Think of it like hiring for a senior role: first HR screens 10,000 CVs quickly using keywords (retrieval — fast, approximate), then the hiring manager interviews the best 20 in detail (ranking — slower, richer), then the business applies constraints like budget and start date (filtering — rules, not ML). Each stage is independently owned, independently deployable, and has its own latency budget.
>
> **Why this matters architecturally:** The three stages have different update cadences (retrieval indices rebuild when the catalogue changes; ranking models retrain weekly; business rules update instantly) and different ownership (ML team owns retrieval + ranking; operations team owns filtering). Designing them as separate microservices from the start — not as one monolithic recommendation service — is the correct call.

This is the most important architectural pattern in recommendation systems. In a large-scale system, you cannot score every item for every user at request time — if you have 1 million users and 500,000 items, full scoring at even 1 microsecond per pair would take 500 seconds per user.

The cascade pipeline solves this with three stages:

**Stage 1: Retrieval (Candidate Generation)**
Goal: reduce from the full item catalogue to a manageable set of candidates (hundreds to low thousands).
Method: fast, approximate nearest-neighbour search in embedding space. The Two-Tower model generates user embeddings and item embeddings. An ANN (Approximate Nearest Neighbour search — a fast technique for finding the closest matches in a large item catalogue without scanning every entry; see also: FAISS (Facebook AI Similarity Search) and ScaNN (Google's scalable nearest neighbour library)) index retrieves the 500–2000 items whose embeddings are closest to the user embedding.
Latency budget: 5–15ms. Optimise for recall (do not miss good candidates), tolerate low precision.

**Stage 2: Ranking**
Goal: score and rank the candidates from retrieval.
Method: a more expensive model (often a gradient-boosted tree or small neural network) that takes rich features for each user-item pair and predicts interaction probability. This model can use features that are too expensive to compute for the full catalogue: joint user-item features, recent interaction signals, contextual features (time of day, device, current session behaviour).
Latency budget: 30–80ms for 500–2000 candidates. Optimise for precision and business metrics (not just click probability — also consider revenue, margin, diversity).

**Stage 3: Filtering and Business Rules**
Goal: apply constraints that the ML models do not know about.
Method: rule-based post-processing. Remove out-of-stock items. Apply legal restrictions (age-gated products). Enforce diversity (do not show 10 items from the same brand). Apply business rules (boost promoted items by a configurable factor). Deduplicate against recently shown items.
Latency budget: 1–5ms.

**Why this matters architecturally**: the three stages have different scaling properties, different update cadences, and different ownership. Retrieval indices need to be rebuilt when the item catalogue changes (potentially many times per day). Ranking models can be retrained on a daily or weekly basis. Business rules can be updated by operations teams without model retraining. Designing these as separate, independently deployable components is the correct architectural approach.

**The cascade pipeline:**

User Request
     │
     ▼
┌─────────────────────────────────────────┐
│  RETRIEVAL STAGE                        │
│  Millions of items → ~2,000 candidates  │
│  Method: ANN vector search + BM25       │
│  Target latency: 5–15ms                 │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  RANKING STAGE                          │
│  2,000 candidates → 20 candidates       │
│  Method: ML ranker (XGBoost / Two-Tower)│
│  Target latency: 30–80ms                │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  FILTERING STAGE                        │
│  20 candidates → 10 final results       │
│  Method: Business rules (stock, promo)  │
│  Target latency: 1–5ms                  │
└─────────────────────────────────────────┘
     │
     ▼
Response to User

---

## 5. Enterprise Example: Retail Group Personalised Promotion System

**Scenario**: A European retail group operates 340 stores and an online channel across 8 countries. They want to deliver personalised promotional offers to their 6.2 million loyalty members — the right promotion, to the right customer, at the right time. The business has three questions:

1. **What should we offer?** (Collaborative filtering — what items/promotions have similar customers responded to?)
2. **When should we send it?** (Time series — when is this customer most likely to be in-market?)
3. **Which customers are worth promoting to?** (Tabular prediction — which customers have high propensity to respond AND high lifetime value?)

**The combined architecture**:

**Collaborative filtering — "what to offer"**: A Two-Tower model trained on 18 months of purchase and promotion interaction history. User tower inputs: purchase category history, promotion response history, country, loyalty tier, demographic segment. Item/promotion tower inputs: product category, discount depth, promotion mechanics (BOGO vs percentage vs fixed amount), campaign creative type.

At serving time, each customer's embedding is pre-computed nightly. For each communication event, the retrieval stage uses approximate nearest-neighbour search to find the 200 most relevant promotion candidates. The ranking stage uses a LightGBM model to score each candidate with richer contextual features (time since last purchase in that category, current inventory pressure, promotion budget remaining).

**Time series — "when to send"**: For each customer, a LightGBM model trained on lag features of purchase history predicts the probability distribution of purchase timing. Features include: days since last purchase, historical inter-purchase interval (mean and variance), seasonal index for this customer's typical purchase categories, and day-of-week purchase probability. The output is a "send window" — a 7-day period within which the customer has the highest predicted probability of being in-market.

**Tabular prediction — "who to target"**: A customer value score and a campaign response propensity score are computed daily for all active members using XGBoost. Features: historical campaign response rate, average order value, purchase frequency trend (improving/stable/declining), loyalty tier, and channel preference. Only customers who meet both a minimum value score and a minimum propensity score threshold enter the promotion funnel.

**The pipeline**: Daily batch job → compute customer embeddings → rank eligible customers by composite score → retrieve promotion candidates → rank candidates → apply business rules (budget, inventory, legal, recency) → generate personalised promotion assignments → trigger communication platform.

**Results**: compared to the prior approach (segment-based blanket promotions), the personalised system delivered 2.3x higher click-through rate, 1.8x higher conversion rate, and 22% reduction in promotional budget consumed per incremental sale.

---

## 6. Architecture Perspective

**Decompose multi-objective AI products into their constituent problem types.** A "personalisation system" is rarely one AI problem. Map the business objectives to problem types (collaborative filtering, time series, tabular) before designing the architecture. Conflating them into a single model increases complexity without increasing capability.

**The cascade pipeline is the right architecture for any large-item-catalogue recommendation system.** Retrieval → Ranking → Filtering is not just a nice pattern — it is the only practical approach at scale. Attempting to score all user-item pairs at request time is computationally impossible beyond ~10K items. Design the three stages as independent microservices with separate SLAs, update cadences, and ownership.

**Pre-computation is the key to recommendation latency.** User embeddings and item embeddings should be pre-computed asynchronously. At serving time, the only real-time operation should be the ANN lookup and the ranking pass over a small candidate set. Anything that requires real-time computation over the full catalogue will not meet production latency requirements.

**Time series models require temporal train/test discipline.** Random splits are invalid. Feature engineering must respect causality — you cannot use future values as inputs. When deploying time series models, the feature computation pipeline must produce features with the same time-lag assumptions as training. A common failure: the training lag feature is "sales yesterday" but the serving pipeline computes "sales at midnight on the day of serving" — these are not the same when serving happens at 2pm.

**Cold start is a product problem, not just an ML problem.** New users and new items require dedicated strategies: onboarding flows that gather preference signals quickly, content-based fallbacks, popularity-based bootstrapping. The architecture must include these fallback paths explicitly, not treat them as edge cases.

**Feedback loop monitoring is non-negotiable for recommendation systems.** Log not just what was recommended and what was clicked, but also the counterfactual — what would have been recommended if the system had not been deployed? This requires an exploration strategy (occasionally surfacing non-top-ranked items to gather unbiased data) and a logging infrastructure that captures both the recommendation context and the outcome. Without this, the training data for the next model iteration is systematically biased by the current model's choices.

---

## 7. Check Yourself

**Question 1 — Decomposing a multi-model AI product request**

A product manager asks for "an AI system that forecasts demand and personalises promotions." Before agreeing to build it, what architectural decomposition do you perform, and why does it matter?

> **Simple Explanation:** Asking one system to both predict "how many units do we need in the warehouse?" and "which customer should see which promotion?" is like asking one employee to be both your warehouse logistics manager and your marketing director. Both roles need different skills, different data, and different reporting lines.
>
> **Detailed Answer:** The request contains at least two distinct AI problem types. Demand forecasting is a time series problem — it exploits temporal patterns in sales history to predict future demand at the SKU/store level. Promotion personalisation is a recommendation system problem (collaborative filtering) combined with tabular prediction for response propensity. These problems have different data requirements, different model families, different retraining cadences, and different serving architectures. Treating them as one system forces compromises that make neither work well. The decomposition also matters for ownership: demand forecasting typically belongs to supply chain; promotion personalisation belongs to marketing.
>
> **Architecture Takeaway:** When a business asks for "an AI system that does X and Y", decompose X and Y into their constituent problem types before agreeing to any design. Misclassifying the problem type (treating a time series problem as tabular) is one of the most common causes of AI project failure.

**Question 2 — Diagnosing cascade pipeline latency**

Your recommendation system is retrieving candidates very quickly (8ms for 2,000 candidates) but the end-to-end latency is 450ms — far above the 150ms SLA. Where in the cascade pipeline is the likely bottleneck, and what do you investigate first?

> **Simple Explanation:** You've confirmed that finding the 2,000 candidates is fast. The bottleneck is the detailed evaluation of those 2,000 candidates — the expensive "interview" stage is taking too long. Either make the interviews shorter (smaller ranking model) or send fewer candidates to interview (retrieval returns 200, not 2,000).
>
> **Detailed Answer:** The cascade pipeline has three stages: retrieval, ranking, and filtering. With retrieval at 8ms, the bottleneck is almost certainly the ranking stage, which must score 2,000 candidates with rich features. Investigate: is the ranking model running on CPU vs GPU? Is feature computation for the 2,000 candidates done in real time or pre-computed? Can the retrieval stage be configured to return fewer candidates (200 instead of 2,000 reduces ranking load by 10x with manageable quality impact)? Can the ranking model be quantised or distilled? Also check whether the 450ms includes network round trips that could be parallelised or cached.
>
> **Architecture Takeaway:** The ranking stage is the primary latency lever in a recommendation cascade. Design it with explicit CPU/GPU options, configurable candidate set size, and a model complexity dial — you will need to tune all three in production.

**Question 3 — Cold start for sparse users**

Your collaborative filtering model works well for your top 20% of customers (those with rich purchase history) but gives poor recommendations for the other 80% (infrequent purchasers). What is the problem called, and what strategies address it?

> **Simple Explanation:** Collaborative filtering is like asking a librarian to recommend books based on what "people like you" read — but if the librarian has only ever seen you borrow one book, they have almost nothing to go on. The fix is to give the librarian other signals about you (your job, your location, what you said you enjoy) so they're not starting blind.
>
> **Detailed Answer:** This is the cold start problem for sparse users — users with few interactions have thin signals for the collaborative filtering model; their user embedding is weak because there is little interaction history to learn from. Strategies: (1) Supplement the user tower with content features available for all users regardless of purchase history — demographics, region, loyalty signup answers, browsing behaviour. (2) Below an interaction threshold, fall back to popularity-based or content-based recommendations. (3) Design onboarding flows that capture preference signals explicitly (preference surveys, quick category ratings). (4) Train a separate model specifically for sparse users with different feature sets than the full-history model.
>
> **Architecture Takeaway:** Cold start is a structural limitation that must be designed around explicitly — not handled as an edge case. Architect explicit fallback paths (content-based, popularity-based, onboarding) and define the interaction threshold at which the system switches between them.

**Question 4 — Why random cross-validation is invalid for time series**

A data scientist proposes using random cross-validation to evaluate the time series demand forecasting model. Why is this incorrect, and what is the right approach?

> **Simple Explanation:** It's like practising for a history exam by answering questions about events that haven't happened yet. The model would appear to do well in evaluation, then fail completely in the real world where it can only know the past.
>
> **Detailed Answer:** Random cross-validation violates temporal causality. If data is split randomly, month-12 data can appear in the training set while month-6 data appears in the test set — the model learns from data that would be "in the future" relative to what it's predicting. This produces optimistic evaluation metrics that collapse in production, because in deployment the model always predicts forward from the present. The correct approach is temporal cross-validation (walk-forward validation): train on months 1–12, test on months 13–14; then train on months 1–14, test on months 15–16; and so on. This exactly simulates the production scenario.
>
> **Architecture Takeaway:** For any time series model, temporal train/test splits are a correctness requirement, not a best practice. Include this as a mandatory review criterion in your ML project governance checklist.

**Question 5 — New item cold start in ANN-indexed recommendations**

Your Two-Tower recommendation model retrieves item embeddings from an ANN index. A new collection of 8,000 items goes live on the website. How long until these items appear in recommendations, and what determines that timeline?

> **Simple Explanation:** New items are invisible to the recommendation system until they've been "catalogued" — given a GPS coordinate in the embedding space and added to the searchable map. The speed at which that happens depends entirely on how often you run the cataloguing pipeline.
>
> **Detailed Answer:** New items will not appear in recommendations until they have embeddings in the ANN index. The timeline depends on the item embedding computation pipeline. If embeddings are computed from static item features (title, description, category, image), new items can be embedded as soon as they are ingested — potentially within minutes to an hour on a short batch cadence. Then the ANN index must be rebuilt or incrementally updated. FAISS supports online insertion but batch rebuilds are often faster and produce better index quality. The practical timeline is: item ingestion time + embedding computation time + index rebuild time + serving tier cache refresh time. For a daily batch pipeline: 12–24 hours. For a near-real-time pipeline: potentially under an hour.
>
> **Architecture Takeaway:** Agree the maximum acceptable cold start window for new items with the business before designing the embedding pipeline cadence. For seasonal or fast-fashion retail (where new items go from launch to peak demand within days), near-real-time embedding is a business requirement, not an optimisation.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers matrix factorisation vs two-tower architectures, Temporal Fusion Transformer internals, and recommendation metrics. It is safe to skip on a first pass and return here when evaluating specific model architectures with your data science team.

### 8.1 Matrix Factorisation vs Two-Tower — Choosing Between Them

**Matrix Factorisation (MF)** trains directly on the interaction matrix. It only uses implicit feedback (clicks, purchases) or explicit ratings. No content features. This makes it extremely fast to implement and effective when you have dense interaction data. It cannot handle cold start (new users/items have no embeddings until they accumulate interactions).

**Two-Tower** is strictly more flexible: it can use content features, it handles cold start better (item tower uses content even for new items), and it supports contextual signals (add a context tower for time of day, device, current session). The trade-off is higher complexity — two separate neural networks to train, feature pipelines for both towers, more hyperparameters to tune.

**When to choose MF**: catalogue is relatively stable, users are mostly existing (low cold start pressure), team is small, and you need something working quickly.

**When to choose Two-Tower**: large or frequently changing catalogue, significant new user or new item volume, contextual personalisation is important, or content features carry significant signal (which they usually do in retail).

### 8.2 Temporal Fusion Transformer for Multi-Series Forecasting

The Temporal Fusion Transformer (TFT) is a deep learning architecture specifically designed for multi-horizon forecasting with mixed input types. Unlike simple lag-feature models, TFT can handle:
- Multiple time series simultaneously (e.g., all SKUs across all stores)
- Static features per series (e.g., store size, product category — does not change over time)
- Known future covariates (e.g., promotion schedule, holiday calendar — you know these in advance)
- Unknown future covariates (e.g., past weather, sales — only known historically)

TFT uses a combination of LSTM layers (for sequential processing), gated mechanisms (to select relevant temporal features), and multi-head attention (to capture long-range dependencies). It also outputs quantile forecasts rather than point forecasts — giving you a range of likely outcomes rather than a single number, which is critical for supply chain planning where you need to reason about risk.

For architects: TFT is appropriate when the scale of the forecasting problem (thousands of series with rich covariates) justifies the investment. For simple demand forecasting with a small SKU set, LightGBM with lag features will perform comparably with a fraction of the operational complexity.

### 8.3 Recommendation Metrics

Evaluating recommendation system quality requires domain-specific metrics:

**Precision@K**: of the K items recommended, what fraction is relevant (clicked, purchased)? Measures the quality of the top-K list.

**Recall@K**: of all items the user would eventually interact with, what fraction appeared in the top-K recommendations? Measures coverage of the user's preferences.

**NDCG@K (Normalised Discounted Cumulative Gain at K — a ranking quality metric that rewards putting the most relevant items at the top of a recommendation list, with diminishing credit for lower positions)**: measures whether relevant items appear near the top of the ranking list, penalising relevant items that appear lower in the list. The "discounted" part applies a logarithmic penalty based on position — relevant items at position 1 are worth much more than relevant items at position 10.

**Coverage**: what fraction of all available items ever appear in recommendations? Low coverage means the system creates a popularity feedback loop — the same popular items are repeatedly recommended, while the long tail never gets exposure.

**Diversity**: how different are the items in a single user's recommendation list from each other? High diversity reduces filter bubble effects. Often traded off against precision.

**The offline/online evaluation gap**: offline metrics (precision@K on held-out interactions) often predict online performance (click-through rate in A/B test) poorly. This is because offline evaluation uses historical interactions that were themselves shaped by the previous recommendation system. The only reliable way to evaluate a new recommendation system is an online A/B test with randomised exposure.

---

## 9. Key Takeaways

- Three distinct AI problem types — tabular prediction, time series forecasting, and collaborative filtering — require different model families, different data structures, and different evaluation approaches; decomposing a business request into the correct problem types before designing is the most important architectural move.

- The cascade pipeline (retrieval → ranking → filtering) is the canonical architecture for production recommendation systems at scale — it partitions the problem into a fast approximate retrieval stage over millions of items and a slower, richer ranking stage over hundreds of candidates, making both quality and latency simultaneously achievable.

- Time series models require temporal train/test splits without exception — using random splits allows future data to leak into training and produces optimistic evaluation metrics that collapse in production.

- Cold start is a structural limitation of collaborative filtering that must be designed around explicitly, not treated as an edge case — new users and new items require dedicated fallback strategies (content-based, popularity-based, or onboarding flows) that are part of the system architecture.

- Recommendation system feedback loops are a governance risk, not just a technical problem — without deliberate exploration (occasionally surfacing non-top-ranked items) and unbiased logging, the training data for future model iterations will be systematically shaped by the current model's biases, causing the system to progressively narrow its own recommendations.
