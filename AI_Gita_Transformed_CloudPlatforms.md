# Cloud Platforms — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

Cloud platforms for AI are the managed infrastructure services that make AI capabilities available at enterprise scale — without requiring you to build GPU clusters, manage model serving infrastructure, or procure frontier model access directly.

The three major cloud providers each offer an AI platform:

- **AWS Bedrock** — Amazon's managed LLM API layer, giving access to Anthropic Claude, Meta Llama, Cohere, Mistral, and Amazon Titan models through a unified API, with SageMaker for ML training and deployment
- **Azure OpenAI** — Microsoft's managed deployment of OpenAI's models (GPT-4o, GPT-4o-mini, embedding models) in Azure's infrastructure, with enterprise SLAs and EU data residency options
- **Google Cloud Vertex AI** — Google's unified ML platform, with access to Gemini models, custom model training, MLOps tools, and a model garden covering third-party models

Each platform also has an adjacent ecosystem: managed vector databases, MLOps tooling, data pipeline services, and monitoring infrastructure that integrate with the AI capabilities.

**For architects:** choosing a cloud AI platform is partly a capability decision (which models are available, which compliance certifications are held) and partly a lock-in decision (the deeper you integrate with one platform's managed services, the more expensive migration becomes). Most enterprises choose primarily on their existing cloud provider relationship and secondarily on AI-specific capability gaps.

---

## 2. Why Should I Care

### For Solution Architects

Cloud platform choice affects three concrete things:

1. **Which models are available** — Azure OpenAI has exclusive enterprise access to OpenAI's GPT-4o models with SLAs; AWS Bedrock has Anthropic Claude; GCP Vertex has Gemini. If your use case requires a specific model, the platform follows.

2. **Data residency and compliance** — Azure OpenAI offers EU-hosted endpoints critical for GDPR-sensitive workloads. AWS Bedrock has region-specific endpoints. GCP Vertex has EU/US/APAC regions. Know your data residency requirements before shortlisting platforms.

3. **Integration with existing infrastructure** — if your data lives in Snowflake on Azure, your pipelines run in Azure Data Factory, and your applications deploy to AKS, using Azure OpenAI is a lower-friction choice than building cross-cloud connectivity to AWS Bedrock.

### For Enterprise Architects

Cloud AI platforms introduce new vendor categories into enterprise procurement:

- **LLM API endpoints** with per-token pricing (new cost structure, different from traditional compute)
- **Managed model serving** with availability SLAs (different from self-managed model serving)
- **Data processing agreements** (DPA) required for models that process personal data — each cloud provider has a different DPA template

Enterprise architects also need to track: model deprecation policies (Azure OpenAI gives 6–12 months' notice; AWS Bedrock policies vary by model provider), version pinning options, and what happens to your system if a model is retired without a suitable replacement.

---

## 3. Think About It Like This (Analogy)

**The Managed Services Analogy**

Before cloud computing, companies ran their own data centres. Buying servers, maintaining them, replacing failed hardware, managing cooling — all in-house. The cloud's value proposition was: let us manage the infrastructure so you can focus on your applications.

Cloud AI platforms apply the same logic to model serving. Running a GPU cluster that serves LLM inference at enterprise scale requires: GPU procurement (6–12 week lead times), infrastructure engineers with GPU ops expertise, capacity planning, on-call rotation for outages, security hardening, and continuous software updates. The cloud AI platforms absorb all of that.

**Azure OpenAI** is like a managed database service — you get access to the database engine (GPT-4o) via a standard interface (REST API), in your cloud region, with enterprise SLAs, without managing the database server itself.

**AWS Bedrock** is like a managed message queue (SQS) — a choice of message queue engines (multiple LLM providers) through a unified API, with AWS handling scale, availability, and infrastructure.

**GCP Vertex AI** is the most comprehensive analogy — it's more like a managed ML platform than just a model API. Google integrates training pipelines, feature stores, model monitoring, and model serving into a unified product. The trade-off: more powerful, but more opinionated about how you structure your ML workflows.

**The HuggingFace Ecosystem** sits alongside all three — a community hub for open-weight models, datasets, and evaluation tools, with its own managed inference endpoints that work across cloud providers. It's the model library that all three cloud platforms draw from for their open-weight model support.

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 AWS Bedrock vs Azure OpenAI vs GCP Vertex: The Decision Framework

Rather than memorising every service detail (which changes quarterly), use this decision framework:

**Step 1: Existing cloud commitment**
- Already deep in AWS (Lambda, EKS, RDS, S3)? Start with Bedrock — lower integration friction.
- Microsoft enterprise agreement, Azure data estate? Start with Azure OpenAI.
- GCP data warehouse (BigQuery), Kubernetes (GKE), or Google Workspace? Start with Vertex.
- Multi-cloud or greenfield? Evaluate on capability and compliance first.

**Step 2: Model requirements**
```
Need GPT-4o or GPT-4o-mini?
  → Azure OpenAI (exclusive enterprise access with SLA)
  → OpenAI direct API also available but no Azure-tier SLA

Need Anthropic Claude?
  → AWS Bedrock (full Claude lineup including Opus)
  → Anthropic direct API also available
  → Azure has some Claude access but less comprehensive

Need Gemini?
  → GCP Vertex AI (Gemini 1.5 Pro, Gemini Flash)
  → Google AI Studio for development

Need open-weight (Llama, Mistral)?
  → All three platforms + HuggingFace Inference Endpoints + self-hosted
  → AWS Bedrock has strong Llama support
  → GCP Vertex model garden has broad selection
```

**Step 3: Compliance and data residency**
```
EU data residency required (GDPR, DPO requirement)?
  → Azure OpenAI EU regions (France Central, Sweden Central)
  → AWS eu-west-1 (Ireland), eu-central-1 (Frankfurt)
  → GCP europe-west (multiple)

Specific compliance certifications required?
  Check: ISO 27001, SOC 2 Type 2, HIPAA BAA, FedRAMP
  All three major providers hold most enterprise certifications
  Verify: does the specific AI service (not just the cloud platform) hold the cert?

Data never leaves your VPC?
  → All three offer VPC/Private Link options for API calls
  → Self-hosted on Kubernetes with open-weight model is most complete isolation
```

> **Common Misconception:** "Choosing a EU-region cloud endpoint satisfies our GDPR data residency requirement."
>
> EU region endpoint is necessary but not sufficient. GDPR compliance for AI processing requires all five of: (1) EU-region endpoint enabled, (2) Data Processing Agreement (DPA) signed with the provider, (3) cross-region data transfer explicitly disabled in API configuration, (4) sub-processor chain verified as EU-compliant, and (5) logging and monitoring data confirmed to stay in the EU region. Missing any one of these — particularly the DPA or the sub-processor check — leaves a compliance gap that your legal team and DPO will find in a review.

**Step 4: Operational integration**
- MLflow already in use? All three have MLflow integrations.
- Terraform for infrastructure? All three have providers.
- Existing monitoring (Datadog, Grafana)? Check native integration vs custom OTel.

### 4.2 AWS Bedrock: What Architects Need to Know

**What it is:** a managed API layer that gives access to multiple LLM providers (Anthropic, Meta, Cohere, Mistral, Amazon Titan) through a single AWS API, with unified authentication (IAM), logging (CloudWatch), and billing (consolidated with AWS account).

**Key architectural features:**

*Inference profiles:* pre-configured model deployments with guaranteed throughput — important when you need predictable latency and don't want to be subject to shared capacity fluctuations.

*Knowledge Bases for Bedrock:* managed RAG infrastructure — upload documents to S3, Bedrock handles chunking, embedding, and indexing into a managed vector store, and a retrieval API layer. Significantly reduces RAG build time; limits flexibility vs custom implementation.

*Agents for Bedrock:* managed agent runtime — define tools (Lambda functions) and orchestration logic; Bedrock handles the ReAct loop (Reason + Act — an agent pattern where the model alternates between reasoning about what to do and executing a tool call). Faster to set up than LangGraph; less flexible for complex state machines.

*Guardrails for Bedrock:* managed content filtering — configure topic blocking, PII detection, hate speech filtering. Applied at the API layer before and after model calls.

**When Bedrock is the right choice:**
- AWS is your primary cloud
- You need multi-provider model flexibility (today Claude, tomorrow Llama, without infrastructure change)
- You want to use Claude without direct Anthropic API management (AWS billing, IAM auth)
- You're building on AWS Lambda / Step Functions and want native integration

**Cost note:** Bedrock typically adds a small markup over direct provider API pricing. The trade-off is unified billing, AWS SLAs, and AWS-native security and compliance infrastructure.

> **Explain Like I'm an Architect**
>
> "Provisioned throughput" is one of the most counterintuitive concepts in cloud AI pricing — it is a capacity reservation, not a usage charge. Here is the analogy: shared cloud capacity is like riding a public bus. Cheap, flexible, usually fine — but you cannot guarantee a seat at peak hour, and you will occasionally be told to wait for the next one. Provisioned throughput is like booking a private minibus that is reserved exclusively for your team. You pay whether the seats are occupied or not, but when your team needs to travel, the seats are always there.
>
> For a customer service chatbot processing 2 million interactions per month, the bus analogy matters: a peak Monday morning surge that pushes shared capacity to its limit translates directly into users seeing a spinner. With provisioned throughput, you have reserved compute and guaranteed latency — the users see a response.
>
> **Why this matters architecturally:** For internal tools where occasional latency spikes are acceptable, shared capacity (pay-per-token) is the right choice. For any customer-facing application where your SLA includes a response time commitment, provisioned throughput is a mandatory cost of production. Design this in before launch — it is far cheaper than an incident post-mortem.

### 4.3 Azure OpenAI: What Architects Need to Know

**What it is:** Microsoft's managed deployment of OpenAI's model family within Azure's infrastructure. Unlike using the OpenAI API directly, Azure OpenAI:
- Runs in your chosen Azure region (including EU regions for data residency)
- Authenticates via Azure Active Directory / Managed Identity — no API key management
- Logs to Azure Monitor
- Comes with Microsoft enterprise SLAs (99.9% uptime SLA)
- Content filtering is on by default; can be configured

**Key architectural features:**

*Provisioned throughput:* reserve capacity (measured in "Provisioned Throughput Units" — PTU — reserved capacity that guarantees throughput regardless of platform load, as opposed to shared pay-per-token capacity) for predictable latency and guaranteed throughput — eliminates shared capacity variance. Critical for production customer-facing applications.

*Azure AI Content Safety:* content moderation as a separate managed service — hate speech, violence, sexual content, self-harm classification. Separate from the LLM call; can be applied to any text, not just model output.

*Prompt flow:* low-code/no-code pipeline builder for LLM workflows — useful for rapid prototyping; less suited for production engineering teams who want code-first control.

*Azure AI Search:* managed vector + keyword search service — integrates directly with Azure OpenAI for RAG patterns. Native hybrid search (vector + BM25 (a keyword relevance algorithm used alongside vector search — see Platform Glossary)) with managed index.

**When Azure OpenAI is the right choice:**
- Microsoft enterprise agreement in place
- GPT-4o specifically required (best reasoning, most tested in enterprise contexts)
- EU data residency required (strongest compliance story)
- Azure Active Directory already the identity provider (Managed Identity auth — no API key exposure)
- Existing Azure data estate (Azure SQL, Azure Blob, Azure Data Factory)

### 4.4 GCP Vertex AI: What Architects Need to Know

**What it is:** Google's most comprehensive AI platform — not just model API access, but a full ML lifecycle platform including training, feature stores, experiment tracking, model registry, and serving infrastructure, plus API access to Gemini models.

**Key architectural features:**

*Gemini access:* Gemini 1.5 Pro (1M context window), Gemini 1.5 Flash (fast, cheap), Gemini 2.0 Pro — Google's frontier models. Gemini 1.5 Pro's 1M token context window is the largest available and enables full-codebase or full-document-library analysis without chunking.

*Model Garden:* curated collection of open-weight and third-party models (Llama, Mistral, Falcon, Gemma) available as managed endpoints — similar to Bedrock's multi-provider model.

*Feature Store:* managed feature store for ML — centralises feature computation, storage, and serving. Reduces train-serve skew for traditional ML use cases.

*AutoML:* automated model training for tabular, text, image, and video tasks — low-code option for non-ML-engineer teams.

*BigQuery ML:* run ML models directly from BigQuery SQL — useful for data teams without Python ML expertise.

**When Vertex AI is the right choice:**
- GCP is your primary cloud
- Gemini's long context window (1M tokens) is required for your use case
- You have a significant traditional ML workload alongside LLM use cases (Vertex's MLOps tooling is more comprehensive than Bedrock's)
- BigQuery is your primary data warehouse (tight integration)
- Google Workspace is your productivity suite (Gemini integrations across Docs, Sheets, Gmail)

> **Explain Like I'm an Architect**
>
> The Build vs Buy vs Fine-tune vs Configure framework is analogous to how your organisation handles enterprise software. When you need CRM capability, you do not write it from scratch (Build) unless you have unique requirements that no product covers. You first check if Salesforce covers it (Buy/SaaS). If it covers 80% but needs your data, you configure it (Configure). If Salesforce does not exist for your use case, you build on an API or platform (Build). And if the off-the-shelf product needs domain-specific tuning to perform adequately, you fine-tune it.
>
> The AI-specific addition is "Configure": managed cloud platform services (Bedrock Knowledge Bases, Azure AI Search + Prompt Flow) sit between SaaS products and custom builds. They give you building blocks — managed chunking, managed vector search, managed agent runtimes — without the full overhead of building from scratch.
>
> **Why this matters architecturally:** "Configure" is the option most teams skip. Moving from SaaS directly to custom build adds months of engineering for problems that managed platform services already solve. The risk of Configure is vendor lock-in: design a clean abstraction over the managed service so migration is a configuration swap, not a rewrite.

### 4.5 The Build vs Buy vs Fine-tune Decision (Cloud Platform Lens)

Cloud platforms add a fourth option to the Build vs Buy vs Fine-tune framework: **configure**.

| Option | Description | Example |
|---|---|---|
| **Buy (SaaS)** | Use a pre-built AI product | Microsoft Copilot, Salesforce Einstein, ServiceNow Now Assist |
| **Configure** | Use cloud platform managed services (RAG, agents, guardrails) with your data | Azure AI Search + Azure OpenAI Prompt Flow |
| **Build (custom)** | Build on raw model APIs with your own orchestration, evaluation, storage | Direct API + LangGraph + custom eval harness |
| **Fine-tune** | Adapt a base model for your specific domain/task | QLoRA (a memory-efficient fine-tuning technique — see Fine-tuning module) on Llama-3 for domain-specific classification |

**The decision rule:**
```
Start with Buy: is there a SaaS product that covers 80%+ of your use case?
  → YES: use it; build only the integration to your data/systems

If not, start with Configure: do the cloud platform managed services cover your pattern?
  → YES: use them; custom code only where managed services don't reach

If not, Build: custom implementation with direct APIs
  → When: managed services add unnecessary constraints; need full control

Fine-tune adds to any of the above: when off-the-shelf models don't meet quality bar
```

**The hidden cost of Configure:** managed services (Knowledge Bases, Prompt Flow, Bedrock Agents) abstract complexity but add vendor lock-in. Migrating from Bedrock Knowledge Bases to a custom Weaviate + LlamaIndex implementation is expensive engineering work. If you might need to migrate, build on portable abstractions from the start.

### 4.6 Technical Debt in AI Systems

**Note for first-time readers:** This section provides important context about long-term AI system costs. If you are currently evaluating which platform to choose, complete Sections 4.1–4.5 first, then return here for the long-term view.

AI systems accumulate technical debt faster than traditional software systems because:

1. **Model dependencies** — code written for GPT-4 may need updating for GPT-4o; code written for GPT-4o may need updating for whatever comes next. Model updates are more frequent than database version updates.

2. **Prompt drift** — prompts that worked well 6 months ago may perform worse on newer model versions (and vice versa). Prompts without version control and evaluation gates accumulate silent quality debt.

3. **Data pipeline debt** — RAG systems are only as good as their knowledge base. Stale documents, inconsistent chunking, poor metadata — these degrade retrieval quality over time without visible failures.

4. **Evaluation debt** — AI systems without evaluation harnesses have no reliable way to detect quality regressions. Technical debt in evaluation infrastructure compounds: the longer you operate without it, the more production issues trace back to undetected model changes.

5. **Governance debt** — responsible AI controls added after deployment are much harder than those designed in. PII handling, audit logging, content moderation added retrospectively require touching every AI call in the codebase.

**Debt reduction strategy:** quarterly AI system reviews covering: model version currency, evaluation harness completeness, knowledge base freshness, governance control coverage, and cost-efficiency (have model pricing changes created better options?).

---

## 5. Enterprise Example

**Scenario: Cloud Platform Selection for a European Retail Bank**

A European retail bank is deploying three AI capabilities: a customer service chatbot (2M interactions/month), an internal document assistant (50K queries/month from staff), and a credit risk narrative generator (5K reports/month, highly sensitive).

**Existing infrastructure:** Azure is the primary cloud (Azure SQL, Azure Blob, Active Directory). The bank holds ISO 27001, SOC 2 Type 2, and is subject to EBA guidelines on AI in banking.

**Platform evaluation:**

| Criterion | Azure OpenAI | AWS Bedrock | GCP Vertex |
|---|---|---|---|
| EU data residency | ✅ France Central | ✅ eu-west-1 | ✅ europe-west |
| GPT-4o access | ✅ Native | ❌ Not available | ❌ Not available |
| Managed Identity auth | ✅ Azure AD native | ❌ (IAM, not Azure AD) | ❌ |
| Existing cloud spend | ✅ EA in place | ❌ separate billing | ❌ separate billing |
| Compliance (ISO 27001, SOC 2) | ✅ | ✅ | ✅ |
| EBA AI guidelines audit support | ✅ MS enterprise compliance | Partial | Partial |

**Decision: Azure OpenAI** — driven by existing cloud relationship, Azure AD native auth (no API key exposure risk), EU data residency, and GPT-4o access.

**Architecture decisions per use case:**

*Customer service chatbot:*
- Model: GPT-4o-mini (speed + cost; adequate for well-scoped customer service tasks)
- Serving: Provisioned Throughput (predictable latency for 2M interactions/month; shared capacity risk unacceptable for customer-facing)
- Knowledge: Azure AI Search (hybrid vector + BM25 on product and policy documents)
- Content safety: Azure AI Content Safety applied to all outputs
- Cost: provisioned throughput at 200 PTU capacity + Azure AI Search indexing = ~£8,000/month

*Internal document assistant:*
- Model: GPT-4o (staff tool; quality over cost)
- Knowledge: Azure AI Search with SharePoint connector (indexes internal documents, policies, procedures)
- Auth: Azure AD SSO — staff authenticate once; no additional credentials
- Cost: 50K × avg 2,000 tokens = 100M tokens/month at £3/M = £300/month (no provisioned needed at this volume)

*Credit risk narrative generator:*
- Model: GPT-4o (highest quality; legal review required before output used)
- Data classification: credit application data = most sensitive tier — requires DPA signed with Microsoft (already in EA)
- Output: structured narrative + supporting citations; not used autonomously — always reviewed by credit officer
- Audit trail: all prompts and completions logged to Azure Monitor with 7-year retention (EBA record-keeping requirement)
- Cost: 5K × 8,000 tokens (long context per report) = 40M tokens/month at £4/M blended = £160/month

**Total platform cost: ~£8,500/month** across three use cases. The bank's prior estimate for self-hosted GPU infrastructure to cover the same workloads: ~£45,000/month in capital + ops.

---

## 6. Architecture Perspective

### The ROI Template for AI Projects

Every AI project presented to finance requires a credible ROI model. Template:

```
Project: [Name]
Use case: [Brief description]
Baseline:
  Current process cost: [£/month or hours/month × rate]
  Current quality metric: [accuracy, cycle time, error rate]

AI-enabled future state:
  Projected process cost: [£/month]
  Projected quality metric: [improvement % with basis]

Implementation cost (one-time):
  Development: [person-weeks × rate]
  Integration: [infrastructure setup, data migration]
  Training and change management: [hours × rate]
  Total one-time: [£]

Running cost (annual):
  Cloud platform / API: [£/year]
  Maintenance (model updates, prompt management, eval): [hours × rate/year]
  Infrastructure: [£/year]
  Total annual: [£]

Annual benefit:
  Cost saving: [£/year]
  Quality improvement value: [£/year, show working]
  Revenue impact (if applicable): [£/year, show working]

Payback period: [months = one-time cost / (annual benefit - annual running cost) × 12]
3-year NPV: [calculate at your organisation's discount rate]

Assumptions: [list all assumptions explicitly]
Measurement plan: [exactly what metrics, what baseline, who measures, what cadence]
```

The most commonly missed line: **Measurement plan.** Without it, ROI claims are unverifiable and finance credibility is lost at the 12-month review.

**Illustrative example** (using the bank scenario from Section 5): Investment: £8,500/month managed AI services + £12,000 implementation. Efficiency gain: 3 FTE × £60,000 = £180,000/year. Quality improvement: 40% reduction in manual review errors, estimated £45,000/year avoided cost. Payback period: ~2 months.

---

## 7. Check Yourself (3–5 Questions)

**Question 1 — EU data residency verification**

Your organisation's legal team requires that all AI processing of customer personal data occurs within the EU. Which cloud platform options satisfy this requirement and what specifically needs to be verified?

> **Detailed Answer:** All three major platforms have EU regions, but "EU region" is not sufficient on its own. What must be verified: (1) The specific AI service (not just the cloud platform) has EU-region endpoints. Azure OpenAI has France Central and Sweden Central; AWS Bedrock has eu-west-1 (Ireland) and eu-central-1 (Frankfurt); GCP Vertex has europe-west regions. (2) The DPA (Data Processing Agreement) is signed with the provider — this is the contractual basis for processing personal data under GDPR Article 28. All three providers have standard DPAs. (3) Cross-region data transfer is explicitly disabled in your API configuration — some services default to load-balancing across regions; confirm your requests stay in the specified region. (4) Sub-processors: if the cloud provider uses sub-processors for the AI service (e.g., Azure OpenAI relies on OpenAI's compute), are those sub-processors also EU-compliant? Microsoft's DPA covers this; verify the sub-processor list. (5) Logging and monitoring data: does your request/response logging also stay in the EU region, or does it get replicated to a US region for centralised monitoring? The answer to your legal team: all three platforms satisfy EU data residency if properly configured with EU region endpoints and signed DPAs. Azure OpenAI has the strongest story for European enterprises because the entire stack (compute, networking, logging, identity) stays within Azure's EU infrastructure under Microsoft's enterprise agreement.
>
> **Simple Explanation:** Selecting a EU-region endpoint is like booking a hotel in Paris for GDPR compliance. You also need the contract (DPA), confirmation that the hotel staff processing your data are also Paris-based (sub-processors), and that your billing records do not get sent to a US address (logging). EU region is the first step, not the full answer.
>
> **Architecture Takeaway:** EU data residency for AI requires all five: EU endpoint, DPA signed, cross-region transfer disabled, sub-processor chain verified, logging in-region. Run this checklist with your DPO before any production deployment processing personal data.

**Question 2 — Managed RAG vs custom RAG trade-offs**

A developer proposes using AWS Bedrock's "Knowledge Bases" managed RAG service to avoid building a custom RAG pipeline. What are the advantages and what trade-offs should the architecture review consider?

> **Detailed Answer:** Advantages: (1) Speed to deployment — Knowledge Bases handles chunking, embedding, vector indexing, and retrieval in a managed service. A working RAG endpoint can be ready in hours vs weeks for a custom build. (2) Maintenance reduction — no vector database to operate, no embedding pipeline to maintain, no chunking configuration to manage. (3) Native AWS integration — S3 data source connectors, IAM authentication, CloudWatch logging. (4) Iterative improvement without re-engineering — AWS regularly improves the managed service; you benefit without code changes. Trade-offs: (1) Chunking control: managed services use opaque chunking strategies. If your content has specific structure (legal clauses, technical specifications, code) that requires custom chunking, the managed service may produce lower-quality retrieval. (2) Retrieval customisation: Bedrock Knowledge Bases offers hybrid search, but cannot implement advanced patterns like ColBERT late interaction, HyDE, or custom reranking models without custom code. (3) Vendor lock-in: migrating away from Bedrock Knowledge Bases to a custom stack (Weaviate + LlamaIndex) is a significant re-engineering project. If your RAG requirements evolve beyond what the managed service supports, migration is expensive. (4) Observability: managed services provide aggregate metrics but limited per-request retrieval debugging. When retrieval quality is poor on specific queries, diagnosing why is harder. Recommendation: use managed services for initial deployment and low-to-medium complexity use cases. Design the application layer to call the RAG endpoint via a clean interface abstraction, so the underlying implementation (managed vs custom) can be swapped if needed.
>
> **Simple Explanation:** Managed RAG services are like using a managed Kubernetes service versus self-hosting Kubernetes — massive setup savings, but you trade flexibility for convenience. The key discipline: design a clean interface over the managed service so the implementation can be swapped if requirements evolve.
>
> **Architecture Takeaway:** Use managed RAG for speed to value and reduced operational overhead. Abstract the retrieval interface from your application code so migration to a custom implementation is a configuration change, not a rewrite. Evaluate managed services against your actual chunking, retrieval, and observability requirements before committing.

**Question 3 — Cloud platform selection: MLOps tooling as a criterion**

An architect says "we should standardise on GCP Vertex AI because it has the most comprehensive MLOps tooling." A developer counters "but we don't need MLOps — we're just calling LLM APIs." Who is right?

> **Detailed Answer:** Both are partially right; neither is fully right. The developer is correct that for simple LLM API call patterns (prompt → model → response), the traditional MLOps tooling (training pipelines, feature stores, model registries) is largely irrelevant. If the entire AI system is API calls to a managed model, the heavy MLOps infrastructure is overhead that adds complexity without value. The architect is correct that as AI systems mature, MLOps-adjacent concerns become real: (1) Evaluation harnesses need to run on a schedule (eval pipeline = MLOps pipeline). (2) Model version tracking and regression testing are MLOps concerns applied to prompt + model version combinations. (3) If any fine-tuning or custom model training is planned (even fine-tuning open-weight models), a model registry and experiment tracking become valuable. The resolution: the right choice is not "Vertex because best MLOps" or "any provider because we're not doing MLOps." It's: evaluate on your actual requirements — which models do you need access to, what are your data residency requirements, what is your existing cloud commitment. MLOps tooling breadth is one factor, but not the deciding one for LLM-API-first teams.
>
> **Simple Explanation:** Choosing a cloud platform because it has the best MLOps tooling when you are only calling LLM APIs is like choosing a city to live in because it has the best hospital — relevant if you need it, but not the right primary criterion. Select on what you need now; MLOps tooling is there when you grow into it.
>
> **Architecture Takeaway:** Evaluate cloud AI platforms on: (1) which models you need access to, (2) data residency requirements, (3) existing cloud commitment. MLOps tooling depth is a secondary factor unless you already have active training workloads or plan fine-tuning in the near term.

**Question 4 — Claude Opus on AWS: access and governance**

Your organisation runs on AWS. A business unit wants to use Claude Opus for a complex legal document analysis use case. How do you provide access, and what governance controls do you implement?

> **Detailed Answer:** Access via AWS Bedrock — Bedrock provides managed access to Anthropic Claude (including Opus) through AWS IAM authentication, consolidated billing, and AWS-native logging. Implementation steps: (1) Enable Bedrock in the relevant AWS region (ensure eu-west-1 or eu-central-1 for EU data residency if required). (2) Create an IAM role for the application with least-privilege Bedrock invoke permissions scoped to Claude Opus model IDs only. (3) Configure VPC endpoints for Bedrock if the application runs in a private VPC (keeps traffic off the public internet). (4) Enable CloudWatch logging for all Bedrock API calls — log model ID, input/output token counts, request metadata (not the full prompt text if it contains sensitive data — log a sanitised version or a reference ID to the document). Governance controls: (1) Data classification check: legal documents likely contain commercially sensitive or personally sensitive information. Confirm the DPA with AWS covers this data category and that the Bedrock service endpoint stays in the required region. (2) Model version pinning: specify the exact model version (not "anthropic.claude-3-opus") to prevent unexpected behaviour from provider-side model updates. (3) Access logging: all invocations logged with the IAM principal (which service account / role made the call) for audit trail. (4) Cost controls: set AWS Budget alerts for Bedrock spend; Opus is expensive — a runaway loop would be costly. (5) Output governance: legal analysis is high-stakes — define the human review gate explicitly. The model output is a draft; a qualified legal professional reviews before any action is taken.
>
> **Simple Explanation:** Bedrock is to Claude what Azure is to OpenAI: you access the model's capability through your existing cloud's security, billing, and compliance infrastructure — no separate vendor relationship to manage. IAM authentication replaces API key management, CloudWatch replaces custom logging, AWS Budgets replaces manual cost monitoring.
>
> **Architecture Takeaway:** Model access decisions should be combined with cloud integration decisions. Using Claude via Bedrock gives IAM auth, consolidated billing, and AWS-native compliance tooling — removing three separate governance concerns. Always add: VPC endpoint, model version pinning, IAM scope restriction, cost budget alerts, and explicit human review gate for high-stakes output.

**Question 5 — Provisioned throughput vs shared capacity**

What is "provisioned throughput" in the context of Azure OpenAI or AWS Bedrock, and when should an architecture require it vs using shared capacity?

> **Detailed Answer:** Provisioned throughput (Azure OpenAI calls it "Provisioned Throughput Units" or PTU; Bedrock calls it "Provisioned Throughput") is a reserved compute allocation — you pay for dedicated capacity that guarantees a specified number of tokens per minute, rather than sharing capacity with other customers on a pay-per-use basis. Shared capacity (the default pay-per-token model) means your requests compete with all other customers' requests. During peak periods, this can cause: rate limit errors (429 responses) requiring retry logic, latency spikes (requests queued behind other customers' traffic), and unpredictable performance. Provisioned throughput eliminates these by reserving capacity exclusively for your workloads. When to require it: (1) Customer-facing applications with latency SLAs — a chatbot that must respond in < 3 seconds P95 cannot tolerate shared capacity variance. (2) High-volume predictable workloads — when you know you will use X tokens/minute consistently, provisioned is typically cheaper at that volume than pay-per-token. (3) Production applications where rate limit errors are unacceptable — shared capacity rate limits can cascade to user-facing errors if not carefully managed. When shared is fine: (1) Internal tools, batch workloads, and non-real-time use cases where occasional latency spikes are acceptable. (2) Low-volume or bursty workloads where reserved capacity would be idle most of the time. (3) Early-stage development and testing. Cost: provisioned throughput requires minimum commitments (typically monthly) regardless of actual usage — it is a fixed cost, not a variable cost. Only makes sense when utilisation will be high enough to justify the reservation.
>
> **Simple Explanation:** Shared capacity is the public motorway — usually fine, but traffic jams happen at peak and you have no control. Provisioned throughput is a dedicated lane — you pay whether you use it or not, but when your traffic arrives, latency is guaranteed.
>
> **Architecture Takeaway:** Provision capacity before launch for any customer-facing application with a latency SLA. For internal tools and batch workloads, shared capacity is acceptable. The decision point is whether occasional latency spikes and rate limit errors are tolerable — if they are user-facing, they are not.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers SageMaker Pipelines and HuggingFace Inference Endpoints at depth. It is safe to skip on a first pass and return here when evaluating specific platform capabilities.

### 8.1 SageMaker Pipelines: ML Orchestration on AWS

For organisations running traditional ML (not just LLM APIs), SageMaker Pipelines provides a managed DAG (directed acyclic graph) orchestrator for ML workflows:

```
SageMaker Pipeline components:
  ├── Processing Step: data preprocessing (Spark or Python)
  ├── Training Step: model training on managed compute
  ├── Evaluation Step: automated metrics computation
  ├── Condition Step: branch on evaluation results
  ├── Register Step: push to Model Registry if quality passes
  └── Deploy Step: update endpoint if approved
```

Each step runs in a managed container on transient compute — no persistent infrastructure required. The pipeline is versioned in SageMaker; execution history, logs, and artifacts are tracked automatically.

For LLM workflows, SageMaker Pipelines can orchestrate: dataset preparation, fine-tuning jobs, evaluation harness execution, and model registration — the same orchestration pattern applied to model training as to data engineering.

### 8.2 HuggingFace Ecosystem: The Model Library

HuggingFace is the de facto library and hosting platform for open-weight models:

- **Model Hub:** 500,000+ models available for download — base models, fine-tuned variants, embedding models, classification models
- **Datasets:** 100,000+ curated datasets for training and evaluation
- **Transformers library:** the standard Python library for loading and running models (`from transformers import AutoModelForCausalLM`)
- **PEFT library:** standard implementation of LoRA, QLoRA, and other PEFT methods
- **Evaluate library:** standardised evaluation metrics
- **Inference Endpoints:** managed GPU hosting for your chosen HuggingFace model — no self-managed GPU required, pay-per-second

For architects: HuggingFace is the source for most open-weight models regardless of which cloud you ultimately host them on. When evaluating an open-weight model for fine-tuning or self-hosting, the model card on HuggingFace is the authoritative documentation for: base model, training data, evaluation scores, intended use, and limitations.

---

## 9. Key Takeaways (5 Bullets)

- **Cloud platform selection is primarily driven by existing cloud commitment and data residency requirements — not AI capability differences.** Azure OpenAI for Microsoft shops with EU requirements, AWS Bedrock for AWS-first organisations, GCP Vertex for Google-heavy environments. The capability differences between platforms narrow quarterly; vendor integration and compliance are more durable differentiators.

- **"EU region" is necessary but not sufficient for GDPR compliance — verify the DPA, the specific AI service's region availability, and that cross-region data transfer is disabled.** A well-intentioned EU region selection can be undermined by default cross-region logging, sub-processor chains that include US entities, or a DPA that hasn't been signed.

- **Managed RAG services (Bedrock Knowledge Bases, Azure AI Search integration) are the right starting point, not a long-term compromise — but design clean interfaces so you can migrate.** Speed to deployment and reduced ops burden justify managed services. Design the application layer with an abstraction over the RAG endpoint, so the underlying implementation can be swapped without rewriting the application.

- **Provisioned throughput is mandatory for customer-facing AI applications, optional for internal tools.** Shared capacity rate limits and latency spikes are acceptable engineering problems for internal tools where occasional delays are tolerable. They are not acceptable for customer-facing applications where P95 latency is part of the SLA. Provision capacity before launch, not after the first customer complaint.

- **AI technical debt accumulates faster than traditional software debt — schedule quarterly AI system reviews.** Model deprecation, prompt drift, stale knowledge bases, and unevaluated governance controls compound silently. A quarterly review covering: model version currency, evaluation harness completeness, knowledge base freshness, and cost optimisation opportunities keeps the system from degrading invisibly.
