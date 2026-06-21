# People & Adoption — Transformed Learning Module
### Chief Learning Experience Designer Edition

> **Target audience:** Solution Architects, Enterprise Architects, Integration Architects, Technical Leads, and Developers new to AI
> **Validation test:** Could a Solution Architect with no AI background understand this without watching a YouTube video? ✅ Yes — this module was designed for that person.

---

## 1. What Is It (Plain English)

AI adoption is the process of moving an organisation from "we're experimenting with AI" to "AI is embedded in how we operate and delivers measurable value."

The technical side — choosing models, building pipelines, deploying infrastructure — is typically 30–40% of the challenge. The remaining 60–70% is people, process, and organisation:

- Do people understand what AI can and cannot do?
- Do they trust it enough to use it and flag issues honestly?
- Are workflows redesigned around AI capabilities, or is AI bolted onto broken processes?
- Is there leadership commitment to absorb the inevitable early failures?
- Are the right skills in place — or actively being built?

> **What is RAG?** RAG (Retrieval-Augmented Generation) means: instead of relying on the model's built-in training knowledge, you retrieve relevant documents from your own systems at query time and feed them to the model alongside the question. The model answers from *your data*, not from what it memorised during training. Think of it as giving the model a cheat-sheet of relevant pages from your internal wiki before asking it a question.

This matters for architects specifically because architects are frequently asked to lead or co-lead AI adoption programmes — not just design the technical architecture. An architect who designs a perfect RAG system that nobody uses has not delivered value.

**The three adoption failure modes architects need to know:**

1. **Technical success, adoption failure:** the AI system works as designed but users don't trust it, don't use it, or use it incorrectly. Common cause: users were not involved in design; the system solves the problem the architect thought they had, not the one they actually have.

2. **Pilot success, scale failure:** a 12-week pilot with 20 enthusiastic users produces glowing results. The enterprise rollout to 2,000 sceptical users produces nothing. Common cause: the pilot cherry-picked enthusiastic adopters; the change management programme was not designed for the majority.

3. **Adoption without governance:** rapid ad-hoc AI tool adoption across teams, with no visibility into what's being used, what data is being shared, or what decisions are being made. Common cause: governance frameworks were built for the pilot but not for scale.

---

## 2. Why Should I Care

### For Solution Architects

Every AI system you build has an adoption dimension. Questions to answer at design time:

- Who will use this system and how confident are they with AI tools?
- What happens when it makes a mistake — is there a clear path for users to report errors and have them corrected?
- Does the UI communicate uncertainty (e.g., "this answer is based on 3 retrieved documents — here are the sources") or present AI output as authoritative fact?
- What training do users need before they're effective with this tool?
- How will you measure whether adoption is succeeding (usage rate, task completion rate, quality metrics)?

Architects who treat adoption as someone else's problem ship systems that get used 15% as much as projected — and get blamed for "the AI not working."

### For Enterprise Architects

AI adoption is an operating model change, not a technology deployment. The enterprise architecture implications:

- **Workforce implications:** some roles will be augmented (more output, higher quality); some workflows will change significantly; some roles may be reduced in scope. These transitions require planning, communication, and support — not just access to a new tool.
- **Skills inventory:** the skills required to work effectively with AI (prompt design, output validation, knowing when to escalate to human judgement) are not evenly distributed today. Upskilling programmes are a prerequisite for effective adoption, not an optional add-on.
- **Operating model (the combination of ownership, decision rights, processes, and capabilities that determine how AI delivers value day-to-day — who approves what, who builds what, who monitors what):** who owns AI tools? Who approves new use cases? Who monitors for safety issues? Who resolves disputes about AI-generated decisions? These are operating model questions with no default answers.
- **ROI measurement:** AI investments are significant. Finance and leadership will ask for ROI evidence. Building measurement into the adoption programme from day one is the only way to answer that question credibly.

---

## 3. Think About It Like This (Analogy)

**The Transition to Spreadsheets (1985–1995)**

When spreadsheet software (Lotus 1-2-3, then Excel) arrived, organisations faced a strikingly similar adoption challenge to what AI presents today.

**The technology worked.** Spreadsheets could do calculations in minutes that had taken accountants days. The productivity gain was real and measurable.

**But adoption was not automatic:**
- Experienced accountants resisted: "I've been doing this for 20 years. I don't trust a computer to get it right."
- Early adopters made errors that were hard to detect (formula mistakes, referenced wrong cells) — reinforcing sceptics.
- Organisations that tried to mandate immediate adoption without training saw errors multiply, not reduce.
- Some roles genuinely were displaced — not eliminated, but changed significantly.

**What successful adopters did differently:**
- Started with enthusiastic early adopters who demonstrated concrete wins
- Invested in training before mandating use
- Maintained parallel processes (manual checks alongside automated outputs) during the transition period
- Built validation steps into the workflow to catch spreadsheet errors before they propagated
- Had senior leadership visibly using the tools — not just mandating them for others
- Set realistic timelines: 2–3 years for full adoption, not 3 months

**The AI parallel is direct.** AI tools today are roughly where spreadsheets were in 1987 — genuinely powerful, real productivity gains for early adopters, but requiring significant organisational change to realise value at scale. The organisations that invested in structured adoption programmes during the spreadsheet era realised dramatically more value, and faster, than those that treated it as "just install the software."

The one difference: AI adoption moves faster (the capability is improving monthly, not yearly) and the error modes are different (spreadsheet errors were numerical; AI errors are semantic — harder to detect without domain knowledge).

---

## 4. Step-by-Step Walkthrough — The Core Concepts

### 4.1 The AI Adoption Maturity Model

> **Explain Like I'm an Architect**
>
> Every organisation adopts new technology in waves — spreadsheets, email, ERP, cloud. AI follows the same pattern, but faster and with more organisational risk if you skip stages. The maturity model below is not a progress report — it's a diagnostic tool. Architects are often brought in at Level 2 (piloting) and asked to design a Level 4 (enterprise platform) solution. That gap causes failure. The most valuable thing you can do with this model is identify where your organisation actually is, and prescribe the right *next* step — not the ultimate destination.
>
> **Why this matters architecturally:** An architecture that's right for a Level 3 organisation (dedicated AI CoE, approved vendor catalogue, MLOps maturity) will fail at Level 1. The architecture must match the organisational readiness, not just the technical requirements.

Organisations move through recognisable stages. Knowing where you are determines what to do next.

**Level 0 — Unaware / Resistant**
- State: AI is discussed but not used, or actively avoided
- Signals: "we're not ready for AI", "our data isn't clean enough", "it's a privacy risk"
- What's needed: executive sponsorship, a small visible win, education to separate AI myth from reality
- Architect's role: identify the highest-value, lowest-risk use case and build a time-boxed proof of concept

**Level 1 — Experimenting**
- State: individuals or small teams using AI tools (ChatGPT, Copilot, Claude) in ad-hoc ways, not coordinated
- Signals: scattered pilots, no shared learnings, no governance, growing shadow AI usage
- What's needed: visibility into what's being used (usage audit), a lightweight governance framework, a community of practice to share learnings
- Architect's role: document what's being used and for what, identify the patterns that are working, build the governance scaffold

**Level 2 — Piloting**
- State: structured pilots with defined use cases, success metrics, and a governance framework
- Signals: 2–5 active pilots, exec sponsor, a dedicated AI team or CoE forming
- What's needed: rigorous pilot-to-production evaluation criteria, skills-building programme, responsible AI principles
- Architect's role: design scalable reference architectures based on pilot learnings, establish evaluation frameworks

**Level 3 — Scaling**
- State: AI embedded in 5+ core workflows, dedicated AI operating model, active measurement
- Signals: AI CoE operational, approved model/vendor catalogue, AI literacy training in progress, ROI being measured
- What's needed: platform standardisation (avoid N different AI stacks), MLOps maturity, cost governance
- Architect's role: define the AI platform architecture, establish standards for model selection, cost tracking, and security

**Level 4 — Optimising**
- State: AI is a default consideration in process improvement discussions, not a special initiative
- Signals: AI use cases in annual planning, finance tracks AI ROI alongside other investments, AI skills in job descriptions
- What's needed: continuous improvement culture, AI risk management integrated into enterprise risk framework
- Architect's role: ensure the AI platform evolves with the model landscape; governance keeps pace with new capabilities

**The trap at each level:**
- Level 1→2: jumping straight to large enterprise rollout without a structured pilot
- Level 2→3: scaling before the governance framework is ready
- Level 3→4: measuring activity (number of use cases) instead of outcomes (business value delivered)

### 4.2 Building the Business Case: ROI Framework

AI investments must be justified to finance and leadership with a credible ROI model. This is not just a finance exercise — it shapes which use cases to prioritise and how to design for measurement.

**The four ROI categories:**

**1. Efficiency gains (most measurable)**
Time saved × fully-loaded cost per hour × volume
```
Example: AI-assisted document review
  Before: 2 lawyers × 4 hours per contract review × £150/hr = £1,200/contract
  After:  AI first pass (30 min review) + 1 lawyer (1 hour validation) = £375/contract
  Saving: £825/contract
  Volume: 200 contracts/year
  Annual saving: £165,000
  AI cost: £3,000/year (API + tooling)
  ROI: 54× in year 1
```

**2. Quality improvements (require measurement infrastructure)**
Defect rate reduction, rework reduction, customer complaint reduction
```
Example: AI-assisted order exception handling
  Before: 8% of orders require manual exception handling
  After:  4% of orders require manual exception handling
  Volume: 500,000 orders/year × 4% reduction = 20,000 fewer manual exceptions
  Each exception: 25 min handling × £30/hr labour = £12.50
  Annual saving: 20,000 × £12.50 = £250,000
```

**3. Revenue enablement (harder to attribute)**
Faster time-to-market, increased conversion, personalisation uplift
```
Example: AI-generated product content
  Before: 6-week time-to-market for new product range (content bottleneck)
  After:  3-day time-to-market with AI content generation
  Uplift: 5.5 weeks earlier × £45,000/week average new range revenue
  Annual revenue uplift (across 4 product launches): 4 × £247,500 = £990,000
  (Caveat: attribution is shared with other factors — use conservative estimates)
```

**4. Risk reduction (present as expected value of risk avoided)**
```
Example: AI-powered compliance monitoring
  Before: manual spot-check covers 2% of transactions
  After:  AI monitors 100% of transactions
  Risk event avoided: regulatory fine of £2M, probability 8%/year without monitoring → 1%/year with
  Expected value of risk reduction: (8% - 1%) × £2M = £140,000/year
```

**The business case template:**

```
Use case: [name]
Current state cost/time: [baseline with evidence]
Future state cost/time: [projection with assumptions stated]
Annual saving / revenue / risk reduction: [£ figure]
AI implementation cost (one-time): [development + integration + training]
AI running cost (annual): [API + infrastructure + maintenance]
Payback period: [months]
Assumptions: [list all assumptions explicitly]
Measurement plan: [exactly how you will verify the ROI post-launch]
```

Never present a business case without a measurement plan. "We'll assess impact after 6 months" is not a measurement plan. Specify: which metric, what baseline, who measures it, on what cadence.

### 4.3 Change Management: The Architect's Practical Framework

> **Explain Like I'm an Architect**
>
> Change management sounds like HR's responsibility. It isn't — at least not for AI systems. As the architect, you design the feedback button that lets users report errors. You design the confidence indicators that tell users when to trust the output. You design the human review workflow for high-stakes decisions. You design the escalation path when something goes wrong. Every one of these is a system design decision that directly determines whether the system gets used, trusted, and improved. The architect who treats change management as "someone else's problem" ships systems that achieve 15% of projected adoption — and gets blamed for the AI "not working."
>
> **Why this matters architecturally:** The five resistance concerns in the table below each have a technical design response. "I'll be blamed for AI errors" → design human-in-the-loop review checkpoints. "I don't know when to trust it" → design confidence indicators and citation display. These are not soft considerations — they are system design requirements.

Architects don't need to become organisational psychologists. But understanding the change dynamics helps design systems that get used and avoid the most common adoption traps.

**The resistance spectrum:**

Most resistance to AI is not irrational. It comes from one of five real concerns:

| Concern | What people are actually thinking | How to address |
|---|---|---|
| **Job threat** | "This will replace me" | Be honest about role evolution; show augmentation examples; involve people in redesigning their own workflows |
| **Accuracy doubt** | "It makes mistakes; I'll be blamed" | Build in human review at appropriate checkpoints; measure AI accuracy publicly; make error reporting easy and blameless |
| **Skill gap** | "I don't know how to use this well" | Training before mandating; buddy systems; safe-to-fail practice environments |
| **Trust deficit** | "How do I know when to trust it?" | Design for explainability (show sources, confidence, alternatives); consistent calibration feedback |
| **Loss of control** | "I used to own this; now the machine does" | Involve users in design; maintain human authority over consequential decisions; make the AI a tool, not an authority |

**The Four Phases of adoption change management:**

**Phase 1 — Awareness (before launch)**
Goal: "I understand what this is and why we're doing it."
Actions:
- Executive communications explaining the rationale (business need, not just technology trend)
- Honest "what this will and won't change" communication — rumours fill information vacuums
- Early access programme for interested volunteers before mandatory rollout
- Showcase: 2–3 concrete examples from peer organisations, not abstract capability demos

**Phase 2 — Building Capability (at and after launch)**
Goal: "I know how to use this and feel confident doing so."
Actions:
- Role-specific training: not generic "here is what LLMs are" but "here is how you specifically will use this in your daily tasks"
- Hands-on practice with real (non-production) scenarios
- Quick reference guides for the 5 most common use cases
- Designated champions in each team who are trained first and support their peers

**Phase 3 — Embedding (months 2–6)**
Goal: "This is part of how I work, not a separate thing I do."
Actions:
- Manager reinforcement: managers visibly using AI tools and referencing AI outputs in team discussions
- Process integration: AI steps built into standard processes, not optional additions
- Feedback loops: regular (biweekly) sessions where users can report issues, confusions, and suggestions
- Recognition: celebrate early wins; share stories of AI-enabled successes

**Phase 4 — Sustaining (months 6+)**
Goal: "We continuously improve how we use AI as the capability evolves."
Actions:
- Community of practice: a channel/forum where best practices, prompt templates, and use case ideas are shared
- Regular review: quarterly review of which AI use cases are delivering value and which need redesign
- Skills progression: advanced training tracks for power users; integration of AI skills into career development frameworks
- Governance refresh: as AI capabilities evolve, revisit responsible AI guidelines and approved use case catalogue

### 4.4 AI Literacy: Skills Matrix by Role

Different roles need different AI knowledge. A "one-size-fits-all AI training programme" fails because it's either too technical for business users or too superficial for engineers. Design tiered literacy tracks.

**Tier 1 — AI-Aware (all employees)**
Everyone who uses AI tools in any capacity.

| Skill | Description |
|---|---|
| What AI can and cannot do | Understand capabilities, hallucination risk, data privacy |
| Responsible use | What is and isn't appropriate to submit to an AI model |
| Output validation | How to check AI output quality; when to trust vs verify |
| Prompt basics | How to give clear instructions; how to iterate when results are wrong |
| Escalation | Who to contact when AI behaves unexpectedly or makes a serious error |

Delivery: 2-hour workshop + quick reference card. Required before first use.

**Tier 2 — AI-Proficient (business users, product managers, team leads)**
People who design workflows involving AI or oversee AI-assisted work.

| Skill | Description |
|---|---|
| Prompt engineering fundamentals | Role, task, format, examples; iterative refinement |
| Workflow redesign | How to identify AI-suitable tasks; how to redesign handoffs |
| Output quality assessment | Domain-specific evaluation; knowing when AI output is good enough |
| Use case identification | Spotting automation and augmentation opportunities |
| Basic evaluation design | How to A/B test AI vs non-AI workflows |

Delivery: 1-day workshop + 4-week practice cohort with coaching.

**Tier 3 — AI-Builder (technical leads, developers, architects)**
People who design, build, or procure AI systems.

| Skill | Description |
|---|---|
| Model selection and evaluation | Capability tiers, cost modelling, benchmark interpretation |
| Prompt engineering advanced | Chain-of-thought, few-shot, structured output, system prompt design |
| RAG and knowledge integration | When and how to ground models in enterprise knowledge |
| AI system design patterns | Guardrails, evaluation, fallback, observability |
| Responsible AI technical implementation | Content moderation, fairness checks, audit logging |

Delivery: this platform (AI Gita) + hands-on labs + design review with senior architects.

**Tier 4 — AI-Expert (ML engineers, AI architects, data scientists)**
People who build and operate AI infrastructure.

Covers all technical content in this platform plus external resources (papers, frameworks, benchmarks).

### 4.5 Pilot to Enterprise Rollout: The Evaluation Criteria

> **Explain Like I'm an Architect**
>
> Pilots almost always succeed. They're designed to succeed: the team picked the most enthusiastic users, the use case was the clearest win, there was dedicated support throughout, and the sponsor was engaged. None of those conditions exist in the enterprise rollout. The architect's job is to design the *pilot* so it exposes what the rollout will actually face — not to make the pilot look good. Run it with a representative sample (including sceptics), measure outcomes not activity, apply the same support model you'll have at scale, and define ahead of time what "success" means for the full rollout.
>
> **Why this matters architecturally:** The pilot-to-production checklist below is not bureaucracy — it's a list of the most common reasons AI systems fail in production after successful pilots. Every unchecked box represents a real failure mode that has happened on someone else's project.

Most pilots succeed. Most enterprise rollouts underperform projections. The gap is not technology — it's that pilots are optimised for demonstration, not scale.

**The pilot design mistakes that cause scale failures:**

| Pilot design mistake | What happens at scale |
|---|---|
| Cherry-picked enthusiastic early adopters | Adoption stalls with mainstream users who have different concerns |
| Measured only usage (logins, sessions) not outcomes | Cannot prove value; budget cut at review |
| Skipped governance — "we'll add it later" | Shadow AI proliferates; security incident triggers programme halt |
| Used vendor demo environment, not production data | Real-world performance much lower than demo environment |
| No human-in-the-loop for edge cases | Errors compound; user trust collapses |
| 8-week pilot with dedicated support team | Support team not available at scale; adoption drops |

**The pilot-to-production checklist:**

Technical readiness:
- [ ] System tested with production-scale data volumes (not just demo data)
- [ ] Latency and availability SLAs defined and tested under load
- [ ] Fallback behaviour tested (what happens when AI is unavailable)
- [ ] Observability in place (logs, metrics, error rates visible to ops team)
- [ ] Security and data handling reviewed and signed off

Adoption readiness:
- [ ] Training programme designed for the full target audience (not just enthusiasts)
- [ ] Champions identified and trained in every affected team
- [ ] Escalation path clear (who users contact for problems)
- [ ] Feedback mechanism live before launch (not after)
- [ ] Manager briefing completed (managers understand what to expect and how to support)

Governance readiness:
- [ ] Responsible AI review completed for this use case
- [ ] Data handling and privacy review completed
- [ ] Approved use case documented in AI catalogue
- [ ] Success metrics defined with measurement plan and baseline established
- [ ] Review gate scheduled (e.g., 90-day review with defined "go/no-go" criteria)

**The phased rollout model:**

```
Week 1–4:     Champions cohort (5–10 per team, self-selected)
              → identify real-world issues not caught in pilot

Week 5–8:     Early majority (30% of target users)
              → stress test support model; refine training based on feedback

Week 9–16:    Full rollout (remaining 70%)
              → mandatory onboarding; manager reinforcement active

Month 6:      First ROI review
              → compare against business case; adjust or expand

Month 12:     Programme review
              → which use cases delivered; what to expand; what to retire
```

---

## 5. Enterprise Example

**Scenario: AI Adoption Programme at a European Retail Distribution Group**

A retail distribution group (8,000 employees, 12 countries) wants to adopt AI across three initial use cases:
1. Customer service: AI-assisted email triage and response drafting
2. Supply chain: AI-powered demand forecasting exception handling
3. Internal knowledge: AI search across internal documentation and policy

**Where they started: Level 1 (Experimenting)**

Prior to the programme, 340 employees were using ChatGPT individually — discovered in a security audit. No governance, no visibility, some uploading of supplier contracts and customer data.

**Programme design choices:**

The transformation team (2 business change managers + 1 solution architect + 1 product owner) made three deliberate decisions:

*Decision 1: Address shadow AI before launching approved tools.* Rather than ignoring the 340 users and launching a new platform, they started by communicating clearly about the shadow AI findings: "We know you're using AI. Here's how to do it safely while we build the proper platform." This built trust and reduced the adversarial dynamic.

*Decision 2: Start with the customer service use case despite it being the riskiest.* It had the highest executive visibility, the largest potential saving (£2.1M/year in productivity estimates), and the most engaged business sponsor. A smaller, "safer" first use case would have produced a smaller win and less credibility for the programme.

*Decision 3: Design the human-in-the-loop before designing the AI.* The customer service team's concern was: "If the AI drafts a bad response and I send it, who is responsible?" The programme answered this before building: agents review every AI draft before sending; a dedicated feedback button in the UI sends errors directly to the QA team; incorrect drafts are used to improve the system within 48 hours. Trust was designed in, not assumed.

**Rollout timeline (customer service use case):**

| Phase | Period | Users | Key metric | Result |
|---|---|---|---|---|
| Champions cohort | Months 1–2 | 18 agents (self-selected) | Draft acceptance rate | 52% of drafts used with minor edits |
| Early majority | Months 3–4 | 80 agents | Draft acceptance rate, handling time | 61% acceptance; 22% handling time reduction |
| Full rollout | Months 5–6 | 340 agents | All metrics | 58% acceptance; 19% handling time reduction |
| Stabilisation | Months 7–12 | 340 agents | Quality metrics, CSAT | Handling time -19%; CSAT unchanged (critical) |

**The resistance pattern they encountered:**

Month 3: a senior team lead (15 years experience) publicly stated in a team meeting that the AI "was making the team dumber — they're not learning how to handle complex cases anymore." This was a legitimate concern, not just resistance.

Response: added a "learning mode" flag in the UI — agents could tag cases they wanted to handle without AI assistance for skill development. Usage data showed experienced agents voluntarily handling ~30% of cases without AI, newer agents using AI for all cases. Team lead became an internal advocate after this change. The concern was valid; addressing it honestly was more effective than dismissing it.

**18-month outcomes across all three use cases:**

| Use case | Target saving | Actual saving | Adoption rate | Primary learning |
|---|---|---|---|---|
| Customer service | £2.1M/year | £1.7M/year | 81% active users | Handling time saving real; CSAT neutral (not improved) |
| Supply chain exceptions | £0.8M/year | £1.2M/year | 94% active users | Exceeded target; supply chain team were most engaged adopters |
| Internal knowledge search | £0.4M/year | £0.1M/year | 31% active users | Documentation quality too poor for RAG; use case paused |

Total 18-month savings: £3.0M vs £3.3M target. The internal knowledge failure was important: the AI system worked technically but the documentation corpus was inconsistent, poorly structured, and outdated. AI search amplified the documentation quality problem rather than hiding it. The remediation (documentation quality programme) is underway; knowledge search relaunched in month 24.

**Programme cost:**
- Technology (APIs, infrastructure): £380,000
- Implementation (development, integration): £420,000
- Change management and training: £180,000 (often the first budget cut — it wasn't here)
- Total 18-month investment: £980,000
- 18-month saving: £3.0M
- ROI: 3× in 18 months

---

## 6. Architecture Perspective

### The Operating Model for AI at Scale

Technical architecture alone is not enough. The operating model — who owns what, how decisions are made, how quality is maintained — determines whether AI delivers sustained value.

**Three operating model options:**

**Centralised (AI Centre of Excellence):**
- Single team owns all AI platforms, standards, and approvals
- Pros: consistency, quality control, no duplication, clear accountability
- Cons: bottleneck, distance from business needs, slow iteration
- When: early adoption stages (Levels 1–2); organisations with high risk sensitivity

**Federated (Distributed AI with Central Standards):**
- Each business unit has AI capability; central team sets standards, provides platforms, reviews high-risk use cases
- Pros: scale, domain expertise, faster iteration
- Cons: risk of divergence, duplication, inconsistent quality
- When: maturing organisations (Levels 3–4); established governance frameworks

**Embedded (AI as Default Engineering Practice):**
- AI capabilities are part of every product team; no separate AI team
- Pros: fastest iteration, closest to business need
- Cons: requires mature AI skills across all teams; governance is hardest to maintain
- When: highest maturity organisations; AI is not a special topic, it's standard engineering

Most enterprise organisations at Levels 2–3 use the federated model. The Centre of Excellence provides:
- Approved model/vendor catalogue (which models are approved for which data sensitivity levels)
- Reference architectures and reusable components
- Security and compliance review process for new AI use cases
- AI skills programme
- AI cost tracking and reporting to finance

### Measuring Adoption: The Right Metrics

**Leading indicators (predict future adoption success):**

| Metric | What it measures | Target |
|---|---|---|
| Training completion rate | Skills readiness | > 90% before full rollout |
| Champion engagement | Internal advocacy health | > 80% of champions active monthly |
| Feedback submission rate | Users reporting issues (sign of engagement) | > 5% of users/month |
| Time-to-first-use after onboarding | Friction in getting started | < 3 days |

**Lagging indicators (measure adoption outcomes):**

| Metric | What it measures | How to collect |
|---|---|---|
| Monthly active users / total eligible users | Sustained adoption rate | System logs |
| AI-assisted vs total task volume | Actual usage depth | Workflow metrics |
| Output acceptance rate (if human reviews AI output) | Quality and trust | UI feedback button |
| Task completion time (AI vs baseline) | Efficiency gain | Before/after comparison |
| Quality metric (relevant to use case) | Value delivered | Domain-specific |
| User-reported satisfaction (pulse survey) | Sentiment | Monthly 3-question survey |

**The vanity metric trap:** "number of AI tools deployed" and "number of use cases in pilot" are activity metrics, not outcome metrics. Finance and leadership eventually see through them. Build your measurement programme around the business outcome metrics from day one, even if they're harder to collect.

---

## 7. Check Yourself (3–5 Questions)

**Question 1 — Evaluating pilot-to-production readiness**

A pilot of an AI-assisted invoice processing tool achieved 94% accuracy and saved 35% processing time across 20 users over 8 weeks. Leadership wants to roll it out to 400 users in the next month. What are your key concerns, and what would you recommend?

> **Simple Explanation:** The pilot was like test-driving a car with a professional instructor. The enterprise rollout is handing the keys to 400 people with a 30-minute tutorial. The car didn't change — the support conditions did. Design the rollout around the average user with normal support, not the enthusiast with dedicated attention.
>
> **Detailed Answer:** Three key concerns: (1) Scale readiness — the pilot ran with 20 likely-enthusiastic early adopters; the remaining 380 users will include sceptics, less tech-comfortable people, and those whose workflows differ. Training and change management designed for 20 enthusiasts will not work for 400. Recommend: extend the rollout to 12–16 weeks with a phased approach. (2) Infrastructure readiness — at 20× the volume, API rate limits, latency, and error handling need load testing before full rollout. Single-tenant pilots rarely expose bottlenecks that surface at scale. (3) Accuracy at the tail — 94% sounds strong, but a 6% error rate on invoices feeding directly into payment flows is a material financial risk. Understand whether errors are random (benign) or concentrated in specific invoice types (systemic risk). Recommend a mandatory human review gate for high-value invoices for the first 90 days, plus a measurement plan that tracks the same metrics as the pilot at scale.
>
> **Architecture Takeaway:** Pilot governance must match the production support model. If dedicated pilot support won't be available at scale, don't use it in the pilot either — you're measuring conditions that won't exist in production.

**Question 2 — Communicating about job impacts honestly**

A business unit leader says: "Our team is worried about job losses — they think the AI will replace them. How should I communicate about this?" What advice would you give, and what communication mistakes should they avoid?

> **Simple Explanation:** When your company introduced email, "this won't change your job" wasn't reassuring — it was quickly proven wrong. Specific plans with timelines and feedback channels are more reassuring than optimistic promises, even when the facts are difficult.
>
> **Detailed Answer:** The concern is legitimate and deserves an honest answer, not reassurance that turns out to be wrong. Avoid three communication mistakes: (1) "AI won't replace anyone" — if workflows are changing, some roles will evolve significantly; empty reassurance destroys trust when reality diverges; (2) "We'll figure it out as we go" — uncertainty without a plan is more frightening than difficult facts with a plan; (3) Communicating only at launch — rumours fill information vacuums. What to do instead: be specific about what will change and what will not ("The AI will draft email responses; you will review and send them"); be honest about what you don't know yet with a committed date for the answer; focus on what people will gain (higher-judgement work, not routine drafting); and create a named feedback channel with a named person who responds.
>
> **Architecture Takeaway:** The feedback channel for user concerns is a system design requirement, not a communications deliverable. Build it into the product: a named escalation path, a visible error reporting button, a committed response SLA. These design decisions determine whether resistance is surfaced and addressed, or silently festers.

**Question 3 — Designing a tiered AI training programme**

You've been asked to design the training programme for an AI adoption rollout affecting 1,200 employees across 4 departments. Budget is limited to 2 days of training per person maximum. How would you structure it?

> **Simple Explanation:** Teaching everyone to drive at the same depth wastes time — someone who only needs to be a passenger doesn't need to learn how to change a tyre. Role-tiered training delivers depth where it adds value and breadth where it's all that's needed.
>
> **Detailed Answer:** A flat "2 days for everyone" wastes budget on capabilities people don't need and misses depth where it matters. Structure by role tier: (1) All 1,200: 2-hour AI Literacy — what AI is, responsible use, output validation, escalation. Mandatory, prerequisite for access, self-paced online. (2) ~800 frontline users: 4-hour role-specific workshop — how to use the tool for their specific tasks, 3 practice scenarios, how to report quality issues. Facilitated in groups of 20. (3) ~300 supervisors: 4-hour manager enablement — how to support adoption, handle resistance, measure progress. (4) ~80 champions: full-day advanced — prompt engineering, workflow redesign, peer training. Trained first, become internal support network. (5) ~20 technical/admin: system training — configuration, monitoring, escalation. Total: 7,600 person-hours. At 16 hours per person max, this fits comfortably while delivering far more targeted learning.
>
> **Architecture Takeaway:** The training programme is a prerequisite deliverable for the rollout, not an optional add-on. In the enterprise example in §5, change management and training (£180,000) was the first budget cut proposed — and the team that didn't cut it achieved 3× ROI. Design training as a required workstream from day one.

**Question 4 — Diagnosing a post-launch usage collapse**

An AI knowledge search system was deployed 6 months ago. Usage has dropped from 35% of eligible users in month 1 to 12% in month 6. What are the likely causes and how would you diagnose and address them?

> **Simple Explanation:** When a new tool goes unused, it's rarely because people are lazy — it's usually because it gives wrong answers, lives in the wrong place, shows no sign of improving, or isn't endorsed by anyone with authority. Check all four before assuming the technology failed.
>
> **Detailed Answer:** A 65% usage reduction after an initial peak is a classic adoption failure — not a technology failure. Four likely causes: (1) Output quality was never good enough — RAG systems amplify documentation quality problems; poor, outdated, or inconsistent docs produce wrong answers. Diagnostic: pull a sample of recent searches and evaluate results quality. Fix: document quality programme or scope limitation to high-quality segments only. (2) Workflow integration failure — if the tool lives at a separate URL while real work happens in Teams or email, friction is too high. Diagnostic: observe where users actually search for information (don't ask — observe). Fix: integrate where work already happens. (3) No visible improvement after feedback — if users reported problems and nothing changed, they stopped reporting and stopped using. Diagnostic: check the feedback log and what was done with it. Fix: public changelog of improvements made from user feedback. (4) No manager reinforcement — if managers don't reference the tool in team settings, team members don't either. Fix: explicit manager engagement and agenda integration.
>
> **Architecture Takeaway:** Adoption monitoring metrics must be built into the system design from day one, not retrospectively investigated after a usage collapse. Design in: feedback collection, quality sampling cadence, manager engagement tracking, and workflow integration review at the 30/60/90 day marks.

**Question 5 — Structuring ROI measurement for a supply chain AI system**

How would you structure the ROI measurement for an AI system that assists supply chain planners in identifying demand forecast exceptions? The business case claims £800K annual saving.

> **Simple Explanation:** You can't prove you saved £800K if you didn't measure what you were spending before. Baseline measurement before launch is not optional — it's the only thing that makes the ROI claim credible to finance 12 months later.
>
> **Detailed Answer:** The £800K saving needs a measurement plan credible to finance. Structure: (1) Baseline measurement before launch (30 days): measure current time per exception, current exception volume, and current error rate — or current forecast MAPE and its downstream inventory cost. Never launch without a baseline; you cannot prove improvement without one. (2) Attribution design: document other concurrent changes (new suppliers, seasonality, team changes) so you can credibly attribute metric changes to AI vs other factors. (3) Monthly tracking for the first 6 months, then quarterly. (4) Track: average time to resolve an exception, exception handling error rate, planner time on manual triage, and forecast accuracy / inventory cost impact. (5) 90-day review gate: compare to baseline trajectory. If not consistent with the £800K projection, identify the gap — adoption, quality, or baseline error in the original estimate — and reforecast before the 6-month executive review.
>
> **Architecture Takeaway:** The ROI measurement plan is a design artifact, not a finance report. It defines which metrics the system must instrument, what logging is required, and what the 90-day review gate criteria are. If the measurement plan is written after the system is built, the data often doesn't exist to answer the question finance will ask.

---

## 8. Advanced Deep Dive

> **Optional depth** — This section covers ADKAR and Kotter change management frameworks in detail. If you are not familiar with change management as a discipline, read the brief framing sentence below before the framework descriptions. It is safe to skim on a first pass.

### 8.1 Why Change Programmes Fail: The Research View

Change management is a professional discipline with established frameworks for understanding why people adopt or resist change. Two frameworks are practically useful for AI programmes — not as rigid recipes but as diagnostic lenses for understanding where adoption is stalling.

Several frameworks describe change management. Two are most practically useful for AI adoption:

**ADKAR (Prosci):** individual-level model. Change succeeds when each person moves through five stages:
- **A**wareness: why is the change happening?
- **D**esire: do I want to support it?
- **K**nowledge: do I know how to change?
- **A**bility: can I actually do the new behaviour?
- **R**einforcement: what keeps me using the new way?

Most AI programmes invest heavily in Knowledge (training) and underinvest in Desire (why should I bother?) and Reinforcement (what happens if I revert to the old way?). ADKAR explains why technically good training programmes don't drive sustained adoption: if Desire is missing, Knowledge is wasted.

**Kotter's 8-Step Model:** organisation-level model. Steps:
1. Create a sense of urgency
2. Build a guiding coalition
3. Form a strategic vision
4. Enlist a volunteer army
5. Enable action by removing barriers
6. Generate short-term wins
7. Sustain acceleration
8. Institute change

For AI programmes specifically, steps 5 and 6 are frequently underexecuted:
- Step 5 (remove barriers): common barriers include IT approval delays, data access restrictions, and manager scepticism — none of which are training problems
- Step 6 (short-term wins): a 12-month programme with no visible wins in the first 90 days loses momentum; design for quick, visible wins in the first 60 days even if they're small

### 8.2 Responsible AI Training: What It Actually Covers

"Responsible AI training" for employees is not just "don't use AI for bad things." It covers five practical areas:

**1. Data handling:** what data can and cannot be submitted to an AI model. Most enterprise AI policies prohibit: personal data above a defined sensitivity level, commercially sensitive information (unreleased product details, financial projections), customer-identifiable data without explicit consent.

**2. Output reliability:** how to calibrate trust in AI output. Domain-specific calibration: a model is more reliable at summarisation than at precise legal interpretation; more reliable at formatting than at factual recall; more reliable for common questions than for edge cases.

**3. Attribution and disclosure:** when must AI-assisted content be disclosed? Many companies are developing policies: disclosed to customers? In internal reports? In published content? The policy varies; employees need to know the policy for their context.

**4. Decision authority:** which decisions can AI assist with, which require human sign-off? A tiered framework (similar to the T0–T3 governance model in the Governance Deep Dive tab) defines escalation thresholds.

**5. Incident reporting:** how to report AI outputs that are harmful, incorrect, or unexpected. The feedback loop is how AI systems improve — employees who don't know how to report (or don't believe it matters) leave quality problems unresolved.

---

## 9. Key Takeaways (5 Bullets)

- **AI adoption is 60–70% people and process, 30–40% technology — design accordingly.** The most common cause of AI project failure is not technical. It's systems that work as designed but don't get used, don't get trusted, or don't have governance in place when something goes wrong. Architects must take ownership of the adoption dimension, not just the technical architecture.

- **Know which maturity level your organisation is at and prescribe the right next step, not the ultimate destination.** A Level 1 organisation (experimenting) trying to implement a Level 3 programme (enterprise platform, full governance) will fail. Match the intervention to the current state: at Level 1, a single visible win and a basic governance scaffold; at Level 2, rigorous pilot evaluation and skills building; at Level 3, platform standardisation and cost governance.

- **Build the ROI measurement plan before building the system — not after.** Baseline metrics must be captured before launch. ROI claims without baselines are unverifiable. Finance will eventually ask for evidence; designing measurement in from day one is the only way to provide it credibly. The measurement plan also sharpens thinking about which use cases are genuinely worth pursuing.

- **Resistance to AI is usually legitimate — address the real concern, not the surface behaviour.** "I don't trust it" means different things: accuracy doubt, job threat, skill gap, loss of control. Diagnose which concern is driving resistance in each stakeholder group and design a specific response. Generic reassurance ("AI is just a tool") doesn't resolve legitimate concerns about job evolution or accountability.

- **Pilots succeed; scale is hard — design your pilot for the mainstream, not the enthusiasts.** Successful pilots that fail to scale share a pattern: they were run with self-selected enthusiasts, measured activity not outcomes, skipped governance, and used dedicated support that isn't available at scale. Design pilots explicitly around the question: "will this work for the average user with normal support, not the early adopter with dedicated attention?"
