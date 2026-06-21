"""
inject_go_deeper.py  — v2
Inserts a "Go Deeper" section before the Key Takeaways heading in each
content tab of AI_Gita.html.

Strategy: for each tab, find the tab's id="tab-XXX" open marker, then find
the FIRST 'class="sh"' line containing "Takeaway" after it, and insert
the Go Deeper block immediately before that line.
"""

import re, shutil, pathlib

HTML = pathlib.Path(r"c:\Users\girijyo\OneDrive - adidas\Desktop\Work\AI Learning\AI_Gita.html")
BACKUP = HTML.with_name("AI_Gita_pre_gd_v2.html")

# ── Resource definitions per tab-id ─────────────────────────────────────────

RESOURCES = {
    "tab-math": [
        {"type":"YouTube","name":"3Blue1Brown — Essence of Linear Algebra","meta":"Playlist · ~3 h · best visual intro to vectors & matrices","url":"https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"},
        {"type":"YouTube","name":"3Blue1Brown — Neural Networks series","meta":"Playlist · ~3.5 h · backprop from first principles","url":"https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"},
        {"type":"YouTube","name":"StatQuest — Statistics & ML playlist","meta":"Josh Starmer · intuition-first explanations","url":"https://www.youtube.com/@statquest"},
        {"type":"Blog","name":"Seeing Theory — Visual Probability & Stats","meta":"Brown University · interactive probability concepts","url":"https://seeing-theory.brown.edu"},
        {"type":"Paper","name":"Attention Is All You Need (Vaswani et al.)","meta":"2017 · the Transformer paper — read §3 on attention","url":"https://arxiv.org/abs/1706.03762"},
    ],
    "tab-llm": [
        {"type":"YouTube","name":"Andrej Karpathy — Intro to Large Language Models","meta":"1 h lecture · best conceptual overview available","url":"https://www.youtube.com/watch?v=zjkBMFhNj_g"},
        {"type":"YouTube","name":"Andrej Karpathy — Let's build GPT from scratch","meta":"2 h · builds a full GPT in Python, step by step","url":"https://www.youtube.com/watch?v=kCc8FmEb1nY"},
        {"type":"Blog","name":"The Illustrated Transformer (Jay Alammar)","meta":"Best visual walkthrough of the Transformer architecture","url":"https://jalammar.github.io/illustrated-transformer/"},
        {"type":"Course","name":"fast.ai — Practical Deep Learning for Coders","meta":"Free · Part 1 covers LLM foundations practically","url":"https://course.fast.ai"},
        {"type":"Docs","name":"OpenAI Tokenizer","meta":"Interactive tool — see how text becomes tokens","url":"https://platform.openai.com/tokenizer"},
    ],
    "tab-landscape": [
        {"type":"Docs","name":"Anthropic — Model Overview & Pricing","meta":"Claude model tiers, context lengths, pricing","url":"https://docs.anthropic.com/en/docs/about-claude/models/overview"},
        {"type":"Docs","name":"OpenAI — Models Overview","meta":"GPT-4o, o1, o3 capabilities and API pricing","url":"https://platform.openai.com/docs/models"},
        {"type":"Blog","name":"Artificial Analysis — AI Benchmarks","meta":"Live model comparison — quality, speed, price","url":"https://artificialanalysis.ai"},
        {"type":"Blog","name":"LMSYS Chatbot Arena Leaderboard","meta":"ELO-ranked model quality via blind human voting","url":"https://lmarena.ai"},
        {"type":"YouTube","name":"AI Explained — State of AI updates","meta":"Concise landscape updates — YouTube channel","url":"https://www.youtube.com/@aiexplained-official"},
    ],
    "tab-ml": [
        {"type":"Course","name":"Google ML Crash Course","meta":"Free · structured ML fundamentals with exercises","url":"https://developers.google.com/machine-learning/crash-course"},
        {"type":"YouTube","name":"StatQuest — Machine Learning playlist","meta":"Best intuition-first ML explanations on YouTube","url":"https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF"},
        {"type":"Course","name":"fast.ai — Practical Deep Learning","meta":"Free · starts from tabular ML and builds up","url":"https://course.fast.ai"},
        {"type":"Docs","name":"scikit-learn User Guide","meta":"Canonical reference for classical ML in Python","url":"https://scikit-learn.org/stable/user_guide.html"},
        {"type":"Paper","name":"XGBoost: A Scalable Tree Boosting System","meta":"Chen & Guestrin 2016 · the dominant tabular ML model","url":"https://arxiv.org/abs/1603.02754"},
    ],
    "tab-dl": [
        {"type":"Course","name":"Deep Learning Specialisation — Coursera (Andrew Ng)","meta":"5 courses · the most comprehensive DL curriculum","url":"https://www.coursera.org/specializations/deep-learning"},
        {"type":"YouTube","name":"Andrej Karpathy — Neural Networks: Zero to Hero","meta":"Playlist · builds everything from scratch in Python","url":"https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ"},
        {"type":"Blog","name":"Distill.pub","meta":"Research journal with exceptional interactive ML visuals","url":"https://distill.pub"},
        {"type":"Blog","name":"The Illustrated BERT (Jay Alammar)","meta":"Visual guide to BERT and contextual embeddings","url":"https://jalammar.github.io/illustrated-bert/"},
        {"type":"Docs","name":"PyTorch — Learn the Basics (official tutorial)","meta":"Best starting point for deep learning in PyTorch","url":"https://pytorch.org/tutorials/beginner/basics/intro.html"},
    ],
    "tab-genai": [
        {"type":"YouTube","name":"Andrej Karpathy — Intro to Large Language Models","meta":"1 h · best conceptual overview of generative AI","url":"https://www.youtube.com/watch?v=zjkBMFhNj_g"},
        {"type":"Blog","name":"What Is ChatGPT Doing? (Stephen Wolfram)","meta":"Long-form intuition piece — no equations required","url":"https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/"},
        {"type":"Course","name":"DeepLearning.AI — Generative AI for Everyone","meta":"Free · non-technical intro, ideal for architects","url":"https://www.deeplearning.ai/courses/generative-ai-for-everyone/"},
        {"type":"Blog","name":"The Illustrated Stable Diffusion (Jay Alammar)","meta":"Visual walkthrough of how diffusion models work","url":"https://jalammar.github.io/illustrated-stable-diffusion/"},
        {"type":"Docs","name":"Hugging Face Diffusers — Documentation","meta":"Official library for diffusion model pipelines","url":"https://huggingface.co/docs/diffusers/index"},
    ],
    "tab-finetune": [
        {"type":"Blog","name":"The Illustrated RLHF (Hugging Face)","meta":"Visual guide to RLHF and alignment fine-tuning","url":"https://huggingface.co/blog/rlhf"},
        {"type":"Course","name":"DeepLearning.AI — Finetuning Large Language Models","meta":"Short course · practical fine-tuning walkthrough","url":"https://www.deeplearning.ai/short-courses/finetuning-large-language-models/"},
        {"type":"Docs","name":"Hugging Face PEFT — Documentation","meta":"Official docs for LoRA, QLoRA, and related PEFT methods","url":"https://huggingface.co/docs/peft/index"},
        {"type":"Blog","name":"LoRA Insights (Sebastian Raschka)","meta":"Best practical breakdown of LoRA fine-tuning","url":"https://lightning.ai/pages/community/lora-insights/"},
        {"type":"Paper","name":"LoRA: Low-Rank Adaptation of LLMs (Hu et al.)","meta":"2021 · the original LoRA paper","url":"https://arxiv.org/abs/2106.09685"},
    ],
    "tab-longctx": [
        {"type":"Paper","name":"Lost in the Middle (Liu et al. 2023)","meta":"The key paper on mid-context recall degradation","url":"https://arxiv.org/abs/2307.03172"},
        {"type":"Paper","name":"FlashAttention: Fast, Memory-Efficient Exact Attention","meta":"Dao et al. 2022 · the memory-efficient attention algorithm","url":"https://arxiv.org/abs/2205.14135"},
        {"type":"Paper","name":"Mamba: Linear-Time Sequence Modelling","meta":"Gu & Dao 2023 · the SSM architecture paper","url":"https://arxiv.org/abs/2312.00752"},
        {"type":"Blog","name":"RULER: What's the Real Context Window of LLMs?","meta":"Benchmark that tests true usable context length","url":"https://arxiv.org/abs/2404.06654"},
        {"type":"Docs","name":"Anthropic — Long Context Tips & Best Practices","meta":"Official practical guidance for using Claude with long context","url":"https://docs.anthropic.com/en/docs/build-with-claude/long-context-tips"},
    ],
    "tab-rag": [
        {"type":"Course","name":"DeepLearning.AI — Building and Evaluating Advanced RAG","meta":"Short course · production RAG patterns and evaluation","url":"https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/"},
        {"type":"Blog","name":"Pinecone — What is a Vector Database?","meta":"Best practical intro to vector search and RAG architecture","url":"https://www.pinecone.io/learn/vector-database/"},
        {"type":"Docs","name":"LangChain — RAG Tutorial (official)","meta":"End-to-end RAG pipeline in Python","url":"https://python.langchain.com/docs/tutorials/rag/"},
        {"type":"Docs","name":"RAGAS — RAG Evaluation Framework","meta":"Open-source evaluation for RAG pipeline quality","url":"https://docs.ragas.io/en/stable/"},
        {"type":"Paper","name":"REALM: Retrieval-Augmented LM Pre-Training","meta":"Google 2020 · the paper that introduced the RAG concept","url":"https://arxiv.org/abs/2002.08909"},
    ],
    "tab-agents": [
        {"type":"Blog","name":"Anthropic — Building Effective Agents","meta":"Canonical guide to agentic system design patterns","url":"https://www.anthropic.com/research/building-effective-agents"},
        {"type":"Course","name":"DeepLearning.AI — AI Agents in LangGraph","meta":"Short course · multi-step agentic workflows in practice","url":"https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/"},
        {"type":"Docs","name":"Model Context Protocol (MCP) — Specification","meta":"Anthropic · official MCP docs and quickstart","url":"https://modelcontextprotocol.io/introduction"},
        {"type":"Docs","name":"OpenAI — Prompt Engineering Guide","meta":"Official prompting strategies with worked examples","url":"https://platform.openai.com/docs/guides/prompt-engineering"},
        {"type":"Paper","name":"ReAct: Synergising Reasoning and Acting","meta":"Yao et al. 2022 · the paper that introduced the ReAct agent pattern","url":"https://arxiv.org/abs/2210.03629"},
    ],
    "tab-infra": [
        {"type":"Docs","name":"vLLM — Documentation","meta":"Most widely used open-source LLM inference server","url":"https://docs.vllm.ai/en/latest/"},
        {"type":"Blog","name":"Hugging Face — LLM Inference Optimisation","meta":"Practical guide to GPU serving, batching, quantisation","url":"https://huggingface.co/blog/optimize-llm"},
        {"type":"Blog","name":"Tim Dettmers — LLM.int8() and Quantisation","meta":"Best intuition piece for INT8/INT4/GPTQ quantisation","url":"https://timdettmers.com/2022/08/17/llm-int8-and-emergent-features/"},
        {"type":"Paper","name":"FlashAttention-2: Faster Attention","meta":"Dao 2023 · v2 improvements relevant for production inference","url":"https://arxiv.org/abs/2307.08691"},
        {"type":"Docs","name":"NVIDIA TensorRT-LLM — Documentation","meta":"NVIDIA's optimised LLM inference library","url":"https://nvidia.github.io/TensorRT-LLM/"},
    ],
    "tab-mlops": [
        {"type":"Course","name":"DeepLearning.AI — LLMOps","meta":"Short course · CI/CD, evals, and monitoring for LLMs","url":"https://www.deeplearning.ai/short-courses/llmops/"},
        {"type":"Blog","name":"Chip Huyen — Real-time ML Challenges","meta":"Production ML system design — practitioner perspective","url":"https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html"},
        {"type":"Docs","name":"MLflow — Documentation","meta":"Open-source ML lifecycle management platform","url":"https://mlflow.org/docs/latest/index.html"},
        {"type":"Blog","name":"Evidently AI — ML Monitoring in Production","meta":"Drift detection, data quality, production metrics guide","url":"https://www.evidentlyai.com/ml-in-production/monitoring-ml-models-in-production"},
        {"type":"Docs","name":"Weights & Biases — Guides","meta":"Experiment tracking, model registry, monitoring","url":"https://docs.wandb.ai/guides"},
    ],
    "tab-sysdesign": [
        {"type":"Blog","name":"ByteByteGo — System Design Newsletter","meta":"LLM and AI system design patterns — highly visual","url":"https://blog.bytebytego.com"},
        {"type":"Blog","name":"Eugene Yan — System Design for Discovery","meta":"Production ML system design from a practitioner","url":"https://eugeneyan.com/writing/system-design-for-discovery/"},
        {"type":"Course","name":"DeepLearning.AI — Building Systems with the ChatGPT API","meta":"Short course · chaining LLM calls in production","url":"https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/"},
        {"type":"Docs","name":"AWS Well-Architected — Machine Learning Lens","meta":"Official enterprise ML system design guidance","url":"https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html"},
        {"type":"Blog","name":"Lilian Weng — Autonomous Agents Survey","meta":"Comprehensive system-design-level agent architecture review","url":"https://lilianweng.github.io/posts/2023-06-23-agent/"},
    ],
    "tab-safety": [
        {"type":"Docs","name":"OWASP LLM Top 10 (2025)","meta":"Canonical LLM application security threat taxonomy","url":"https://owasp.org/www-project-top-10-for-large-language-model-applications/"},
        {"type":"Paper","name":"Constitutional AI: Harmlessness from AI Feedback","meta":"Anthropic 2022 · the alignment technique behind Claude","url":"https://arxiv.org/abs/2212.08073"},
        {"type":"Docs","name":"EU AI Act — Official Full Text","meta":"EUR-Lex · the regulation architects must understand","url":"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689"},
        {"type":"Course","name":"DeepLearning.AI — Red Teaming LLM Applications","meta":"Short course · adversarial testing and safety evaluation","url":"https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/"},
        {"type":"Docs","name":"NIST AI Risk Management Framework","meta":"US Government AI governance and risk management standard","url":"https://www.nist.gov/artificial-intelligence"},
    ],
    "tab-cvnlp": [
        {"type":"Blog","name":"The Illustrated BERT (Jay Alammar)","meta":"Visual guide to transformer-based NLP and embeddings","url":"https://jalammar.github.io/illustrated-bert/"},
        {"type":"Course","name":"fast.ai — Practical Deep Learning Part 1 (Vision)","meta":"Free · CNNs, transfer learning, vision fine-tuning","url":"https://course.fast.ai/Lessons/lesson1.html"},
        {"type":"Docs","name":"Hugging Face Transformers — Vision Models","meta":"ViTs, CLIP, multimodal models in practice","url":"https://huggingface.co/docs/transformers/index"},
        {"type":"Blog","name":"The Illustrated Word2Vec (Jay Alammar)","meta":"How word embeddings and semantic similarity work","url":"https://jalammar.github.io/illustrated-word2vec/"},
        {"type":"Paper","name":"An Image is Worth 16×16 Words (ViT paper)","meta":"Dosovitskiy et al. 2020 · Vision Transformer original paper","url":"https://arxiv.org/abs/2010.11929"},
    ],
    "tab-akp": [
        {"type":"Docs","name":"Anthropic — Multi-agent Orchestration","meta":"Official patterns for building multi-agent systems","url":"https://docs.anthropic.com/en/docs/build-with-claude/tool-use/multi-agent-orchestration"},
        {"type":"Blog","name":"Anthropic — Building Effective Agents","meta":"Canonical agentic design patterns guide","url":"https://www.anthropic.com/research/building-effective-agents"},
        {"type":"Docs","name":"LangGraph — Documentation","meta":"Graph-based agent orchestration framework","url":"https://langchain-ai.github.io/langgraph/"},
        {"type":"Docs","name":"AutoGen — Microsoft Multi-Agent Framework","meta":"Conversation-based multi-agent orchestration","url":"https://microsoft.github.io/autogen/"},
        {"type":"Paper","name":"A Survey on LLM-based Autonomous Agents","meta":"Xi et al. 2023 · comprehensive agent architecture survey","url":"https://arxiv.org/abs/2309.07864"},
    ],
    "tab-recsys": [
        {"type":"Course","name":"fast.ai — Practical Deep Learning (Tabular & RecSys)","meta":"Free · gradient boosting and collaborative filtering","url":"https://course.fast.ai/Lessons/lesson6.html"},
        {"type":"Blog","name":"Eugene Yan — System Design for Discovery","meta":"Netflix/Spotify-style recommendation system design","url":"https://eugeneyan.com/writing/system-design-for-discovery/"},
        {"type":"Docs","name":"FAISS — Getting Started (Facebook ANN Search)","meta":"ANN search library used in production rec systems","url":"https://faiss.ai/index.html"},
        {"type":"Paper","name":"Neural Collaborative Filtering (He et al.)","meta":"2017 · foundational recommendation systems paper","url":"https://arxiv.org/abs/1708.05031"},
        {"type":"Blog","name":"Nixtla — TimeGPT and Modern Forecasting","meta":"State-of-the-art time series forecasting overview","url":"https://nixtlaverse.nixtla.io/nixtla/docs/getting-started/introduction.html"},
    ],
    "tab-datasci": [
        {"type":"Course","name":"Coursera — A/B Testing by Google","meta":"Free audit · experiment design and causal inference","url":"https://www.coursera.org/learn/ab-testing"},
        {"type":"Blog","name":"Causal Inference for The Brave and True","meta":"Free online textbook — causal ML for practitioners","url":"https://matheusfacure.github.io/python-causality-handbook/"},
        {"type":"Blog","name":"Trustworthy Online Controlled Experiments","meta":"Kohavi — first chapter free · definitive A/B testing book","url":"https://www.exp-platform.com/Documents/guidecontrolledexperiments.pdf"},
        {"type":"Docs","name":"Microsoft EconML — Causal ML Library","meta":"Uplift modelling, heterogeneous treatment effects in Python","url":"https://econml.azurewebsites.net"},
        {"type":"YouTube","name":"Mixtape Sessions — Causal Inference lectures","meta":"Free · econometrics and causal inference for data scientists","url":"https://www.youtube.com/@scotcunningham"},
    ],
    "tab-gov2": [
        {"type":"Docs","name":"EU AI Act — Official Full Text (EUR-Lex)","meta":"The regulation architects must understand","url":"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689"},
        {"type":"Docs","name":"NIST AI Risk Management Framework","meta":"US government AI governance standard","url":"https://www.nist.gov/artificial-intelligence"},
        {"type":"Blog","name":"AI Now Institute — Annual Report","meta":"Critical review of the AI governance landscape","url":"https://ainowinstitute.org/research"},
        {"type":"Docs","name":"ISO/IEC 42001 — AI Management System","meta":"International AI governance standard overview","url":"https://www.iso.org/standard/81230.html"},
        {"type":"Blog","name":"Google PAIR — People + AI Research Guidebook","meta":"Practical UX and ethics guidance for AI product teams","url":"https://pair.withgoogle.com/guidebook/"},
    ],
    "tab-agentops": [
        {"type":"Docs","name":"LangSmith — LLM Observability Platform","meta":"Tracing, evaluation, and monitoring for LLM applications","url":"https://docs.smith.langchain.com"},
        {"type":"Blog","name":"Hamel Husain — Your AI Product Needs Evals","meta":"Practitioner's guide to eval design and automated scoring","url":"https://hamel.dev/blog/posts/evals/"},
        {"type":"Docs","name":"OpenLLMetry — OpenTelemetry for LLMs","meta":"Open-source LLM observability via standard OTel","url":"https://www.traceloop.com/docs/openllmetry/introduction"},
        {"type":"Docs","name":"Weights & Biases — Prompt Tracking","meta":"Prompt versioning and LLM experiment tracking","url":"https://docs.wandb.ai/guides/prompts"},
        {"type":"Blog","name":"Anthropic — Building Effective Agents","meta":"Canonical agentic system design and ops patterns","url":"https://www.anthropic.com/research/building-effective-agents"},
    ],
    "tab-devexp": [
        {"type":"Docs","name":"OpenAI — Prompt Engineering Best Practices","meta":"Official prompt engineering guide with worked examples","url":"https://platform.openai.com/docs/guides/prompt-engineering"},
        {"type":"Course","name":"DeepLearning.AI — Prompt Engineering for Developers","meta":"Short course · structured prompting techniques","url":"https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/"},
        {"type":"Blog","name":"Hamel Husain — Evals: Your AI Product's Foundation","meta":"Practical evaluation design from a practitioner","url":"https://hamel.dev/blog/posts/evals/"},
        {"type":"Docs","name":"Braintrust — LLM Evaluation Platform","meta":"CI/CD and testing infrastructure for LLM applications","url":"https://www.braintrust.dev/docs"},
        {"type":"Docs","name":"Cursor AI — Documentation","meta":"AI-native IDE — developer experience benchmark for the space","url":"https://docs.cursor.com"},
    ],
    "tab-people": [
        {"type":"Blog","name":"McKinsey — The State of AI (Annual Report)","meta":"Enterprise AI adoption data and case studies","url":"https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"},
        {"type":"Course","name":"Coursera — AI For Everyone (Andrew Ng)","meta":"Free · non-technical AI literacy for all employees","url":"https://www.coursera.org/learn/ai-for-everyone"},
        {"type":"Blog","name":"Prosci — ADKAR Model Overview","meta":"The change management framework referenced in this tab","url":"https://www.prosci.com/methodology/adkar"},
        {"type":"Blog","name":"Kotter — 8-Step Change Model","meta":"The organisational change framework referenced in this tab","url":"https://www.kotterinc.com/methodology/8-steps/"},
        {"type":"Blog","name":"HBR — Collaborative Intelligence: Humans and AI","meta":"Enterprise AI adoption strategy with practitioner cases","url":"https://hbr.org/2018/07/collaborative-intelligence-humans-and-ai-are-joining-forces"},
    ],
    "tab-emerging": [
        {"type":"YouTube","name":"Andrej Karpathy — Deep Dive into LLM Reasoning","meta":"1 h · reasoning model mechanics (o1 / o3) explained","url":"https://www.youtube.com/watch?v=7xTGNNLPyMI"},
        {"type":"Blog","name":"Artificial Analysis — Frontier Model Tracker","meta":"Live comparisons of reasoning and frontier models","url":"https://artificialanalysis.ai"},
        {"type":"Blog","name":"Hugging Face — Mixture of Experts Explained","meta":"Visual guide to MoE architectures (Mixtral, Grok)","url":"https://huggingface.co/blog/moe"},
        {"type":"Blog","name":"Anthropic — Computer Use Technical Overview","meta":"Official overview of computer use capability","url":"https://www.anthropic.com/news/3-5-models-and-computer-use"},
        {"type":"Blog","name":"Lilian Weng — LLM-Powered Autonomous Agents","meta":"Comprehensive deep-dive into emerging agent architectures","url":"https://lilianweng.github.io/posts/2023-06-23-agent/"},
    ],
    "tab-cloud": [
        {"type":"Docs","name":"AWS Bedrock — Getting Started Guide","meta":"Managed LLM service · official quickstart","url":"https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html"},
        {"type":"Docs","name":"Azure OpenAI Service — Documentation","meta":"Enterprise LLM deployment on Azure","url":"https://learn.microsoft.com/en-us/azure/ai-services/openai/"},
        {"type":"Docs","name":"Google Vertex AI — Generative AI Quickstart","meta":"GCP's managed AI platform — Gemini and open models","url":"https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts"},
        {"type":"Blog","name":"Artificial Analysis — Cloud Provider Comparison","meta":"Live benchmark: latency, cost, throughput across providers","url":"https://artificialanalysis.ai/providers"},
        {"type":"Docs","name":"AWS Well-Architected — Machine Learning Lens","meta":"Official enterprise ML system design on AWS","url":"https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html"},
    ],
}

# ── HTML generator ────────────────────────────────────────────────────────────

def gd_block(resources):
    type_icon = {"YouTube": "▶ YouTube", "Course": "🎓 Course", "Paper": "📄 Paper",
                 "Docs": "📖 Official Docs", "Blog": "✍ Article"}
    type_class = {"YouTube": "gd-yt", "Course": "gd-course", "Paper": "gd-paper",
                  "Docs": "gd-docs", "Blog": "gd-blog"}
    cards = ""
    for r in resources:
        tc = type_class.get(r["type"], "gd-docs")
        ti = type_icon.get(r["type"], r["type"])
        cards += (
            f'<a href="{r["url"]}" target="_blank" rel="noopener" class="gd-card {tc}">'
            f'<div class="gd-type">{ti}</div>'
            f'<div class="gd-name">{r["name"]}</div>'
            f'<div class="gd-meta">{r["meta"]}</div>'
            f'</a>\n'
        )
    return (
        '\n<div class="go-deeper">\n'
        '<div class="go-deeper-title">📚 Go Deeper</div>\n'
        '<div class="go-deeper-sub">Finished this tab? These are the best next resources — '
        'use them <em>after</em> reading the content above, not instead of it.</div>\n'
        '<div class="go-deeper-grid">\n'
        + cards +
        '</div>\n</div>\n'
    )

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    shutil.copy(HTML, BACKUP)
    print(f"Backup: {BACKUP.name}")

    src = HTML.read_text(encoding="utf-8")

    injected = 0
    for tab_id, resources in RESOURCES.items():
        # Find the tab opening
        tab_open = f'id="{tab_id}"'
        start = src.find(tab_open)
        if start == -1:
            print(f"  SKIP {tab_id}: tab id not found")
            continue

        # Find next tab opening or end of panels (to bound our search)
        next_tab = src.find('<div id="tab-', start + len(tab_open))
        search_region = src[start:next_tab] if next_tab != -1 else src[start:]

        # Find the Key Takeaways sh div within this tab
        # Patterns: 'class="sh">Key Takeaways' or 'class="sh">9. Key Takeaways'
        match = re.search(r'<div class="sh">[0-9. ]*Key Takeaways', search_region)
        if not match:
            print(f"  SKIP {tab_id}: Key Takeaways sh not found in tab")
            continue

        # Absolute position in src
        abs_pos = start + match.start()

        # Insert go-deeper block before the Key Takeaways heading
        block = gd_block(resources)
        src = src[:abs_pos] + block + src[abs_pos:]
        print(f"  OK {tab_id}")
        injected += 1

    HTML.write_text(src, encoding="utf-8")
    print(f"\nDone. {injected} Go Deeper sections injected.")

if __name__ == "__main__":
    main()
