import os

html_path = r'c:\Users\girijyo\OneDrive - adidas\Desktop\Work\AI Learning\AI_Gita.html'

with open(html_path, encoding='utf-8') as f:
    html = f.read()

platform_glossary_html = """
<div class="ibox" style="border-left-color:#7c3aed;background:#f5f3ff;margin-bottom:20px">
  <strong style="color:#4c1d95">&#128218; Architect Platform Glossary</strong> &mdash; 20 terms that appear across multiple learning modules, each defined for Solution Architects and Enterprise Architects. If you encounter one of these terms before it is explained in a module, look it up here.
</div>

<div class="sh">Architect Platform Glossary &mdash; 20 Cross-Module Terms</div>

<div class="g2">
<div class="card ai">
  <div class="ch ai">A &mdash; Autoregressive</div>
  <p style="font-size:12px;line-height:1.7">A generation strategy where each word (token) is produced one at a time, with each new word depending on everything before it. All text-generating AI (ChatGPT, Claude, Gemini) works this way. Architecturally: the model cannot go back and edit what it already generated, which is why prompts need to be precise upfront.</p>
</div>
<div class="card b">
  <div class="ch b">B &mdash; BM25</div>
  <p style="font-size:12px;line-height:1.7">A keyword-matching algorithm that scores documents by how many times your search terms appear, weighted by rarity. In AI systems, BM25 is often combined with semantic (vector) search: exact term matching for product codes and identifiers, plus meaning-based matching for conceptual queries. <em>See also: RAG, Vector search.</em></p>
</div>
</div>

<div class="g2">
<div class="card ai">
  <div class="ch ai">C &mdash; Context Window</div>
  <p style="font-size:12px;line-height:1.7">The working memory of a language model &mdash; everything it can see in a single conversation or API call. Measured in tokens (~3/4 of a word each). GPT-4o: ~128,000 tokens; Claude: up to 200,000 tokens. Directly affects cost, latency, and which architectures are feasible (RAG vs long-context). <em>See also: Token, RAG.</em></p>
</div>
<div class="card b">
  <div class="ch b">C &mdash; Cross-Encoder Reranker</div>
  <p style="font-size:12px;line-height:1.7">A model that takes a query and a candidate document together and produces a single relevance score. More accurate than vector search but slower. In a RAG pipeline, applied to the top 20-50 candidates before sending the best 3-5 to the language model. Think of a specialist reviewer who carefully reads both the question and each answer. <em>See also: RAG, BM25.</em></p>
</div>
</div>

<div class="g2">
<div class="card g">
  <div class="ch g">D &mdash; DPA (Data Processing Agreement)</div>
  <p style="font-size:12px;line-height:1.7">A legally binding contract between an organisation and a vendor specifying how personal data will be handled, stored, and protected. Required under GDPR when personal data is processed by a third party (including a cloud AI provider). Enterprise architects must ensure a signed DPA is in place before sending any personal data to an AI API. Not signing one is a GDPR violation, not just a risk.</p>
</div>
<div class="card g">
  <div class="ch g">H &mdash; HITL (Human-in-the-Loop)</div>
  <p style="font-size:12px;line-height:1.7">A design pattern where a human approves, reviews, or overrides an AI decision before it becomes an action. Architects design HITL gates by risk level: a customer email draft may need no approval; a large refund or a contract amendment requires human sign-off.</p>
</div>
</div>

<div class="g2">
<div class="card a">
  <div class="ch a">I &mdash; i.i.d.</div>
  <p style="font-size:12px;line-height:1.7"><strong>Independently and identically distributed.</strong> A statistical assumption that each data point was drawn randomly from the same distribution with no relationship between points. Time series data violates this (tomorrow's sales depend on today's). This matters architecturally when choosing the wrong model family for a problem. <em>See also: ML Fundamentals, RecSys/TS/Tabular.</em></p>
</div>
<div class="card a">
  <div class="ch a">L &mdash; LLM Judge</div>
  <p style="font-size:12px;line-height:1.7">A quality evaluation pattern where a second language model call scores the output of the first. Instead of checking exact string matches, you ask a capable model: "Given this question, does this answer correctly address it? Rate 1-5." Used in evaluation harnesses, regression testing, and production quality monitoring. Scales far better than human review. <em>See also: Evaluation harness.</em></p>
</div>
</div>

<div class="g2">
<div class="card t">
  <div class="ch t">M &mdash; MCP (Model Context Protocol)</div>
  <p style="font-size:12px;line-height:1.7">An open protocol (Anthropic, 2024) that standardises how AI agents connect to external tools and data sources. Before MCP, every agent system had its own bespoke integration layer. MCP provides a standard interface. Architecturally analogous to what REST did for web APIs. Enterprise architects should treat it as they would any integration standard: assess adoption, compliance requirements, and vendor support.</p>
</div>
<div class="card t">
  <div class="ch t">O &mdash; OTel / OpenTelemetry</div>
  <p style="font-size:12px;line-height:1.7">The open-source industry standard for collecting observability data (traces, metrics, logs) from distributed systems. If you have Datadog, Grafana, Dynatrace, or Azure Monitor, it almost certainly ingests OTel data. AI-specific extensions (GenAI semantic conventions) add standard attributes for LLM traces: model name, token counts, prompt/completion text, latency. Your existing observability infrastructure can monitor AI systems with minor instrumentation.</p>
</div>
</div>

<div class="g2">
<div class="card ai">
  <div class="ch ai">Q &mdash; QLoRA</div>
  <p style="font-size:12px;line-height:1.7">A memory-efficient variant of fine-tuning combining quantisation (reducing model weight precision) with LoRA (training only a small set of added parameters). Fine-tuning a 70B-parameter model normally requires 8-10 A100 GPUs; QLoRA can do it on a single A100. Architects encounter QLoRA when evaluating whether self-hosted fine-tuning is feasible vs. using a managed fine-tuning service. <em>See also: Fine-tuning, LoRA.</em></p>
</div>
<div class="card b">
  <div class="ch b">R &mdash; RAG (Retrieval-Augmented Generation)</div>
  <p style="font-size:12px;line-height:1.7">An architecture pattern where a language model is given relevant documents retrieved from a knowledge base at query time, rather than relying solely on training data. Solves the knowledge cutoff problem and reduces hallucination risk. Three components: retrieval system (vector + keyword search), injection mechanism (retrieved text added to the prompt), and the language model. Standard pattern for enterprise knowledge assistants. <em>See also: Vector search, Context window.</em></p>
</div>
</div>

<div class="g2">
<div class="card g">
  <div class="ch g">R &mdash; RLHF</div>
  <p style="font-size:12px;line-height:1.7"><strong>Reinforcement Learning from Human Feedback.</strong> A training technique used to align language models with human preferences. Human raters indicate which of two outputs is better; a reward model learns to predict human preference; the language model is then trained to score highly on this reward. All major frontier models (GPT-4, Claude, Gemini) use some form of RLHF. Architects encounter it when evaluating vendor safety claims and understanding why model behaviour changed between versions. <em>See also: Fine-tuning.</em></p>
</div>
<div class="card g">
  <div class="ch g">T &mdash; Token</div>
  <p style="font-size:12px;line-height:1.7">The unit of text a language model processes. Roughly 3/4 of an English word. API pricing is per token (input + output). Context window limits are in tokens. A rough rule: 1,000 tokens = 750 words = 1.5 pages of text. Architects need token awareness for cost modelling, latency budgeting, and context window architecture decisions.</p>
</div>
</div>

<div class="card ai" style="margin-bottom:20px">
  <div class="ch ai">V &mdash; Vector Search / Semantic Search</div>
  <p style="font-size:12px;line-height:1.7">A search technique where text (or images) is converted into a list of numbers (a vector or embedding) that encodes its meaning. Two pieces of text with similar meaning will have vectors that are close together in mathematical space, even if they share no exact words. This enables search-by-meaning. Vector search is the retrieval mechanism inside RAG systems and powers semantic similarity calculations. <em>See also: RAG, BM25, Embedding.</em></p>
</div>

<div class="sh">Quick Reference &mdash; Abbreviations</div>
<table class="t">
<tr><th>Term</th><th>Full form</th><th>One-line meaning</th></tr>
<tr><td><strong>BM25</strong></td><td>Best Match 25</td><td>Keyword relevance scoring algorithm</td></tr>
<tr><td><strong>DPA</strong></td><td>Data Processing Agreement</td><td>GDPR-required vendor data contract</td></tr>
<tr><td><strong>HITL</strong></td><td>Human-in-the-Loop</td><td>Human approval gate before AI action</td></tr>
<tr><td><strong>i.i.d.</strong></td><td>Independently and identically distributed</td><td>Statistical assumption violated by time series</td></tr>
<tr><td><strong>LLM</strong></td><td>Large Language Model</td><td>Transformer model trained on internet-scale text</td></tr>
<tr><td><strong>MCP</strong></td><td>Model Context Protocol</td><td>Standard for AI agent and tool integration</td></tr>
<tr><td><strong>OTel</strong></td><td>OpenTelemetry</td><td>Open standard for traces, metrics, logs</td></tr>
<tr><td><strong>QLoRA</strong></td><td>Quantised Low-Rank Adaptation</td><td>Memory-efficient fine-tuning technique</td></tr>
<tr><td><strong>RAG</strong></td><td>Retrieval-Augmented Generation</td><td>Architecture pattern: retrieve then generate</td></tr>
<tr><td><strong>RLHF</strong></td><td>Reinforcement Learning from Human Feedback</td><td>Training technique for aligning model behaviour</td></tr>
</table>

<div class="ibox" style="border-left-color:#6b7280;font-size:11.5px;margin-top:4px">
  <em>This section covers cross-platform terms. Each learning module also defines topic-specific terms inline at point of first use.</em>
</div>

<div class="sh">A&ndash;Z Platform Glossary</div>
"""

glossary_tag = '<div id="tab-glossary" class="panel">'
glossary_start = html.find(glossary_tag)
if glossary_start < 0:
    print('ERROR: glossary panel not found')
else:
    insert_pos = glossary_start + len(glossary_tag)
    html = html[:insert_pos] + '\n' + platform_glossary_html + html[insert_pos:]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Platform Glossary injected. New file size: {len(html)} chars ({len(html)//1024} KB)')
