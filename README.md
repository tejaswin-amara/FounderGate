# FounderGate: Adversarial Mom-Test Agent

> **Don't trust AI. Audit your startup idea.**
>
> A frugal, adversarial customer-discovery and go-to-market engine that tests founder hypotheses against interview evidence, stops for explicit human judgment, and generates decision records only after founder sign-off.

<p align="center">
  <a href="https://foundergate-hetic26.vercel.app">Live Demo</a> ·
  <a href="https://github.com/tejaswin-amara/FounderGate">Source Repository</a> ·
  <a href="https://github.com/tejaswin-amara/FounderGate/blob/main/workflows/n8n-foundergate-workflow.json">n8n Workflow Export</a>
</p>

> **Repository status:** The GitHub repository was empty when this README was prepared. This document captures the project specification and Devpost story supplied by the team; it does not independently verify that the application source, automated tests, Docker setup, or n8n export have been committed. The run instructions below describe the intended project setup and should be checked against the final source tree before judging or release.

## About the project

**FounderGate** is a frugal, adversarial multi-agent Customer Discovery and Go-To-Market (GTM) engine. It takes raw customer-interview transcripts and competitor context, extracts evidence, challenges optimistic interpretations using the principles of *The Mom Test*, and then stops at a mandatory human judgment checkpoint.

The system is designed around one principle: **AI should not decide a founder's strategy. It should reduce repetitive synthesis and expose confirmation bias so the founder can make a better-informed decision.**

| Project detail | Information |
|---|---|
| Challenge | AI Agents for Founders Challenge — HETIC 2026 |
| Project name | FounderGate: Adversarial Mom-Test Agent |
| Elevator pitch | Frugal multi-agent customer discovery and GTM engine that audits founder hypotheses against raw evidence, halts at a human judgment gate to log strategic ADRs, and runs on free-tier or local AI. |
| Live demo | https://foundergate-hetic26.vercel.app |
| Repository | https://github.com/tejaswin-amara/FounderGate |
| Workflow export | https://github.com/tejaswin-amara/FounderGate/blob/main/workflows/n8n-foundergate-workflow.json |

**Built with:** Python, FastAPI, Next.js, React, TypeScript, Tailwind CSS, Gemini, Mistral, Groq, Ollama, Hugging Face, n8n, and Docker.

---

## Inspiration

### The sycophancy trap killing early-stage startups

Founders lose hours every week synthesizing messy customer-discovery interviews, competitor reviews, and market-research notes. The problem is not only the time required; it is also the risk of drawing the wrong conclusion from the evidence.

When a founder pastes interview transcripts into a conventional LLM chatbot and asks, *“Does this validate my startup idea?”*, the model can become a confirmation-bias amplifier. Polite compliments such as *“Your UI looks sleek!”* and hypothetical promises such as *“I'd definitely pay €29/month when you launch!”* can be summarized as strong market validation—even though neither statement demonstrates that a customer has experienced the problem, changed their behavior, or spent money to solve it.

Rob Fitzpatrick's *The Mom Test* emphasizes asking about people's lives and past behavior rather than inviting compliments or hypothetical promises. FounderGate applies that evidence-first mindset to an AI-assisted workflow.

We built FounderGate for the **AI Agents for Founders Challenge — HETIC 2026** around a simple conviction: **AI should never make a founder's strategic decision. It should challenge weak evidence, surface contradictions, and give the founder more time to think.**

---

## What it does

FounderGate turns raw customer-discovery material into an auditable decision workflow with four principal stages.

### 1. GDPR-oriented privacy and prompt-injection gate

Before input is sent to an external language model, the safety layer (identified in the design as **safety_gate.py**) applies regular-expression and heuristic checks.

- Redacts email addresses as **[REDACTED_EMAIL_GDPR]**.
- Redacts phone numbers as **[REDACTED_PHONE_GDPR]**.
- Redacts IBANs as **[REDACTED_IBAN_GDPR]**.
- Checks untrusted transcripts and competitor material for prompt-injection attempts.
- Records security-gate actions for later inspection.

Prompt-injection patterns such as “Ignore previous instructions” and “Override human checkpoint” are intended to be rejected during pre-flight validation with **HTTP 400**. Redaction and input checks are privacy safeguards; they do not, by themselves, establish legal GDPR compliance.

### 2. Adversarial dual-agent audit

Two agents inspect the same discovery evidence from opposing perspectives.

**Agent 1 — Optimistic Evidence Extractor**

- Scans transcripts line by line.
- Extracts atomic, verbatim quotes that may support or inform the founder's hypothesis.
- Preserves exact source-line references so the founder can inspect the original context.

**Agent 2 — Mom-Test Skeptic**

- Cross-examines every extracted quote using *The Mom Test* principles.
- Flags compliments and conversational fluff.
- Flags hypothetical future promises.
- Identifies leading questions asked by the founder.
- Distinguishes these weak signals from verified past behavior and actual spending.

The result is a contradiction and evidence matrix—not an automatic declaration that the startup idea is validated.

### 3. Mandatory human judgment checkpoint

The workflow stops at **HALTED_AT_HUMAN_GATE**. The backend is designed to refuse GTM strategy and investor-material generation until the founder has reviewed and adjudicated every extracted claim.

For each claim, the founder must explicitly choose one of the following:

- **✓ Accept as Verified Behavior** — the evidence supports a behavioral claim.
- **✕ Discard Biased Fluff** — the statement is a compliment, weak signal, or unsupported claim.
- **⚠ Log to Assumption Debt Ledger** — the claim may matter but still needs to be tested.

The founder must also formulate the pivoted hypothesis and select the target GTM wedge. The checkpoint is designed as a hard lifecycle gate, not a suggested review step. The supplied implementation specification identifies **/api/v1/checkpoint-resolve** as the resolution endpoint and **HTTP 422** as the response when claims remain undecided.

### 4. Bilingual strategic decision and GTM synthesis

Only after the founder signs off does the system generate the post-gate outputs:

- A formal **Strategic Decision Record (ADR/SDR)**.
- An **Assumption Debt Ledger** containing unverified claims.
- The **next five non-leading Mom-Test interview questions**.
- A **Target GTM Wedge** grounded in accepted behavioral evidence.
- An **Investor Pre-Emptive Objection Matrix**.
- Bilingual English/French decision and GTM synthesis.

---

## Human judgment: what the agent does and what the founder decides

| Stage | What the AI agent does | What the human founder decides | Why human judgment is irreplaceable |
|---|---|---|---|
| **1. Evidence extraction and bias audit** | Tags verbatim quotes, links exact interview line numbers, and presents Optimistic vs. Skeptic interpretations. | Reviews both interpretations and corrects misread nuance, sarcasm, or context. | A model cannot reliably infer every emotional hesitation, relationship dynamic, or informal industry context from text alone. |
| **2. Claim adjudication gate** | The gate is designed to block **/api/v1/checkpoint-resolve** with **HTTP 422** until every extracted claim has a human decision. | Classifies each claim as Verified Past Behavior, Biased Fluff (Discard), or Assumption Debt (Needs Testing). | Prevents autopilot validation and requires the founder to confront contradictory evidence. |
| **3. Strategic pivot and wedge selection** | Proposes candidate wedges based strictly on accepted behavioral evidence. | Rewrites the Pivoted Hypothesis and selects the Target GTM Wedge before signing the decision record. | Choosing which market and customer segment a company should pursue is a high-stakes entrepreneurial judgment—not an AI output to accept blindly. |

---

## System architecture

The following diagram describes the intended flow from input sanitization through adversarial analysis, the mandatory human gate, and post-gate synthesis.

~~~mermaid
flowchart TB
    subgraph Input["1. Input and GDPR / Security Gate"]
        A["Synthetic founder scenario or custom transcripts and competitor notes"]
        B["safety_gate.py: PII redaction, prompt-injection checks, action log"]
        A --> B
    end

    subgraph Router["2. Equal-access AI Router"]
        R{"Zero-cost / local model router"}
        R1["Google AI Studio: gemini-2.5-flash"]
        R2["Mistral: mistral-small-latest"]
        R3["Groq: llama-3.3-70b-versatile"]
        R4["Ollama: qwen2.5:7b / llama3.2"]
        R5["OpenRouter / Hugging Face free models"]
        R -.-> R1
        R -.-> R2
        R -.-> R3
        R -.-> R4
        R -.-> R5
    end

    subgraph Audit["3. Adversarial Discovery Loop"]
        C["Agent 1: Evidence and Market Extractor"]
        D["Agent 2: Mom-Test Skeptic"]
        E["Contradiction and Evidence Matrix"]
        C -->|"Verbatim quotes and line citations"| D
        D -->|"Compliments, promises, leading questions, competitor gaps"| E
    end

    subgraph Gate["4. Mandatory Human Checkpoint"]
        F{"HALTED_AT_HUMAN_GATE"}
        G["Founder adjudicates every claim: Accept, Discard, or Log Debt"]
        H["Pivoted hypothesis and target GTM wedge"]
        F --> G --> H
    end

    subgraph Synthesis["5. Post-gate Synthesis and Telemetry"]
        I["Agent 3: GTM and Investor Synthesizer"]
        J["ADR / SDR, Assumption Debt Ledger, next five interview questions"]
        K["Investor objection matrix in English and French"]
        L["AI disclosure and time-saved report"]
        I --> J
        I --> K
        I --> L
    end

    B --> C
    E --> F
    H --> I
    R --> C
    R --> D
    R --> I
~~~

### Architecture notes

- **Input layer:** accepts one-click synthetic founder scenarios or custom interview transcripts and competitor notes.
- **Safety layer:** sanitizes personal identifiers and checks untrusted input before model processing.
- **Model router:** supports configured free-tier providers and local inference options.
- **Adversarial loop:** pairs an evidence extractor with a skeptical reviewer to expose conflicting interpretations.
- **Human gate:** blocks downstream synthesis until all claims have been adjudicated and the founder has recorded a pivot hypothesis.
- **Synthesis layer:** generates decision records, assumption debt, interview questions, and investor objections after sign-off.

---

## How we built it

### Technology stack

| Layer | Technologies / components |
|---|---|
| Backend API | Python, FastAPI, Pydantic |
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| AI providers | Google Gemini, Mistral, Groq, Ollama, OpenRouter, Hugging Face |
| Workflow automation | n8n |
| Local / container runtime | Docker and Docker Compose |
| Safety and governance | PII redaction, prompt-injection checks, explicit lifecycle gate, action logging |
| Decision artifacts | ADR/SDR template, Assumption Debt Ledger, investor objection matrix |

### Frugal model orchestration

FounderGate is designed to avoid long, conversational multi-agent loops. The Extractor and Mom-Test Skeptic are batched into a structured JSON pass where supported, with a separate post-gate synthesis call. The supplied token estimates are approximately **920 tokens per full sprint** for the Gemini configuration, rather than a long multi-turn agent conversation.

The structured response approach uses JSON output (for example, a provider's JSON response mode) to make extraction and review easier to validate. Exact request parameters vary by provider.

### Runtime model and provider disclosure

The project specification lists the following free-tier or local options. Free-tier eligibility, quotas, model identifiers, and provider terms can change; users should confirm current availability before a run. A zero-cost estimate assumes the selected provider remains within its free allowance, or that inference is local.

| Component / agent role | Model and provider | Plan / execution mode | Calls per run | Estimated tokens per run | Estimated runtime cost |
|---|---|---|---|---:|---:|
| **Zero-Key Judge Sandbox (default)** | Built-in deterministic Mom-Test rule engine | Open-source / local | 1 local pass | 0 external tokens | **€0.00** |
| **Option 1: Google AI Studio** | **gemini-2.5-flash** | Free tier | 1 batched JSON call (Extractor + Skeptic) + 1 synthesis call | ~580 Phase 1 + ~340 Phase 2 = **~920 total** | **€0.00 within free limits** |
| **Option 2: Mistral AI** | **mistral-small-latest** | Free experimentation plan, as listed in the project specification | 1 batched JSON call + 1 synthesis call | **~910 total** | **€0.00 within free limits** |
| **Option 3: Groq Cloud** | **llama-3.3-70b-versatile** | Free tier, subject to provider quotas | 1 batched JSON call + 1 synthesis call | **~890 total** | **€0.00 within free limits** |
| **Option 4: Local Ollama** | **qwen2.5:7b** or **llama3.2** | Local open-weight inference | 1 local JSON call + 1 local synthesis | **~850 local tokens** | **€0.00 provider inference cost** |
| **Option 5: OpenRouter** | **meta-llama/llama-3.3-70b-instruct:free** | Free model route, subject to availability | 1 batched JSON call + 1 synthesis call | **~920 total** | **€0.00 within free limits** |
| **Option 6: Hugging Face** | **Qwen/Qwen2.5-72B-Instruct** | Free inference availability, subject to current access limits | 1 batched JSON call + 1 synthesis call | **~920 total** | **€0.00 within free limits** |

**Cost statement:** The design target is **€0.00 in model-inference charges per run** when using the built-in sandbox, local Ollama, or provider free allowances. This does not imply that hosting, networking, storage, or usage beyond free provider quotas is always free.

### Frugality engineering and token accounting

Instead of spawning a chatty ten-turn multi-agent conversation estimated at more than 15,000 tokens, FounderGate batches the Extractor and Skeptic into one structured JSON pass and performs synthesis after human approval.

The project specification reports an approximately **920-token** Gemini run. Compared with a 15,000-token baseline, that is approximately **93.9% fewer tokens**. The originally stated **84%** reduction corresponds to a different baseline, so the comparison baseline should be recorded alongside benchmark logs before using the percentage as a measured result.

### AI-assisted development disclosure

Cursor and Google Gemini were used during development to assist with TypeScript/FastAPI boilerplate and French translation phrasing. The project specification states that the following were human-designed and verified by the team:

- Agent prompts and the Mom-Test rubrics.
- Lifecycle and human-gate logic.
- GDPR-oriented PII redaction patterns.
- The evidence-review and decision workflow.

### Pre-existing open-source libraries and adapted patterns

The following existing projects and frameworks informed the implementation. They are inspirations and dependencies, not original work by the FounderGate team.

| Project / library | License stated in project notes | How it informed FounderGate |
|---|---|---|
| FastAPI, Pydantic, Next.js, Tailwind CSS | Respective upstream licenses | Standard backend, validation, frontend, and styling foundations. |
| [affaan-m/ecc — Everything Claude Code](https://github.com/affaan-m/ecc) | MIT, as identified in project notes | Inspired the adversarial **gan-generator / gan-evaluator** pairing and the brand-discovery, market-research, and investor-material structures, including **70_founder-tension.md** and **90_SYNTHESIS.md**. |
| engineering-pipeline | v3.1.0, MIT, as identified in project notes | Inspired prompt-injection verification, the hard lifecycle gate, the assumption-debt ledger, and the ADR template structure. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT, as identified in project notes | Inspired assumption-debt tracking and token/time-saved telemetry patterns (**ponytail-debt**, **ponytail-gain**, and **ponytail-audit**). |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | MIT, as identified in project notes | Guided a minimalist, explicit state-machine architecture without unnecessary wrapper layers. |

Check each upstream repository's current license and include applicable attribution and notices in the source distribution before release.

---

## Challenges we ran into

### Avoiding AI confirmation bias

A conventional assistant is often optimized to produce a helpful-sounding answer. For customer discovery, that can turn weak signals into apparent validation. The challenge was to make the workflow question its own optimistic interpretation instead of merely producing a more persuasive summary.

### Making the human checkpoint a real system constraint

A human review prompt is not enough if downstream endpoints can still generate strategy without it. FounderGate's design therefore treats adjudication as a lifecycle requirement: every claim needs a decision before the post-gate synthesis stage can proceed.

### Preserving traceability

A conclusion is only useful when the founder can return to the source. The extractor therefore needs to preserve verbatim quotes and exact line references, while the skeptic must explain why a quote is weak, hypothetical, leading, or behaviorally meaningful.

### Handling sarcasm, politeness, and cultural nuance

Short or lightweight models can misread irony, indirect refusals, or culturally polite language. The system must keep the original quote and both agents' interpretations visible so that the human can correct the model.

### Staying frugal without hiding trade-offs

Free-tier model quotas and model availability vary. The project balances hosted free-tier providers with local Ollama inference and a zero-key deterministic sandbox, while disclosing that the free-tier options are subject to provider terms and limits.

---

## Accomplishments that we're proud of

- **Adversarial review rather than one-sided summarization:** an evidence extractor is explicitly challenged by a Mom-Test skeptic.
- **A mandatory human decision gate:** downstream GTM and investor synthesis is designed to remain blocked until every claim has been adjudicated.
- **Traceable evidence:** extracted claims retain verbatim quotes and exact source-line references.
- **Privacy and input safeguards:** the workflow includes PII redaction and prompt-injection checks before model processing.
- **Low-cost evaluation path:** a zero-key sandbox and local inference option reduce the barrier for judges and founders to try the workflow.
- **Actionable post-gate outputs:** the founder receives a decision record, assumption-debt ledger, five follow-up interview questions, and an investor objection matrix.
- **Bilingual output:** decision and GTM artifacts are designed for English and French.

### Time-saved report

The project specification reports a benchmark across **three startup discovery scenarios**, each containing three to four customer interviews and competitor-review notes of approximately 600–1,000 words per sprint. The figures below are the supplied before/after estimates; they should be accompanied by raw timing logs if presented as independently measured benchmark results.

| Workflow sub-task | Manual founder baseline | FounderGate + human checkpoint | Reported net time saved |
|---|---:|---:|---:|
| **1. GDPR PII scrubbing and verbatim quote tagging** | ~30 minutes | ~0.2 seconds | ~29.8 minutes |
| **2. Mom-Test confirmation-bias audit** | ~25 minutes | ~2.5 seconds | ~24.9 minutes |
| **3. Contradiction resolution and pivot formulation** | ~20 minutes | ~3.5 minutes | ~16.5 minutes |
| **4. ADR/SDR, assumption-debt ledger, and five interview questions** | ~20 minutes | ~1.0 second | ~19.9 minutes |
| **Total per discovery sprint** | **95 minutes** | **~5 minutes** | **~90 minutes (94.7% reduction)** |

At two sprints per week for four weeks, the reported estimate is **12 hours saved** (eight sprints × 90 minutes) on repetitive synthesis work. FounderGate is intended to reduce research overhead; it does not prove product-market fit or guarantee that a founder will avoid a poor investment decision.

---

## What we learned

- **Customer evidence is not customer enthusiasm.** Compliments and hypothetical intentions are weaker signals than documented past behavior, workarounds, and actual spending.
- **Contradiction is useful.** An optimistic interpretation and a skeptical interpretation should be visible together, not collapsed into one confident summary.
- **Human-in-the-loop must be enforced technically.** A meaningful checkpoint needs backend state and endpoint-level enforcement, not just a UI warning.
- **Traceability improves trust.** Verbatim quotes, line references, and explicit reasoning make it possible for users to challenge an agent's interpretation.
- **Frugality is an architectural decision.** Batching structured work, using local inference, and providing a deterministic sandbox can make an agent workflow more accessible.
- **Privacy controls have limits.** Regex-based redaction and prompt-injection patterns are useful safeguards, but they cannot guarantee that every identifier or attack will be detected.

---

## Responsible AI, privacy, and limitations

### Privacy and GDPR-oriented safeguards

- The project specification identifies **verify_and_sanitize_input()** as the sanitization function.
- Email addresses, phone numbers, and IBANs are intended to be redacted before payloads are sent to an external provider.
- For sensitive B2B or NDA-protected interviews, users can select local Ollama inference (for example, **qwen2.5:7b**) so model inference remains on the local machine.
- Three built-in synthetic founder scenarios are included in the design to let judges test the workflow without uploading real third-party personal data:
  1. B2B Invoice SaaS.
  2. Student Alternance EdTech.
  3. D2C GreenTech Packaging.

These safeguards do not, on their own, establish GDPR compliance. Teams must also assess lawful basis, transparency, retention, access controls, processor terms, hosting region, data-subject rights, and any other obligations applicable to their actual deployment.

### Prompt injection and untrusted input

Competitor reviews and customer transcripts are untrusted content. Patterns such as “Ignore previous instructions” and “Override human checkpoint” are intended to be blocked by the pre-flight safety gate with **HTTP 400**. Pattern matching is not a complete defense against prompt injection; downstream prompts and tools must continue to treat supplied content as data, not instructions.

### Known limitations and failure cases

**Sarcasm and cultural politeness**

Lightweight 7B–8B models can misclassify dry irony or culturally polite phrasing as literal intent.

**Mitigation:** Each evidence card should show the verbatim quote, exact line number, confidence score, and both agents' arguments. The founder can override the classification at the checkpoint.

**Small-sample fallacy**

Two interviews may indicate that a problem exists for those two people; they do not establish a €100M total addressable market.

**Mitigation:** The Assumption Debt Ledger tracks unverified market-sizing claims and records falsification experiments that should be completed before making fundraising claims.

**Model and provider variability**

Different providers and model versions can return different classifications, exhaust free quotas, or change availability.

**Mitigation:** Keep model/provider details visible, validate structured responses, retain source evidence, and make the deterministic sandbox or local inference path available where practical.

---

## French executive summary — Résumé exécutif en français

**Problématique :** Les fondateurs perdent des heures chaque semaine à synthétiser leurs entretiens clients et leurs analyses concurrentielles. Pire encore, un LLM classique peut agir comme une chambre d'écho et transformer des compliments polis — par exemple « Super maquette ! » — ou des promesses hypothétiques — « Je paierais 29 € par mois au lancement ! » — en fausse validation du marché.

**Notre solution — FounderGate :**

1. **Anonymisation RGPD et sécurité :** filtrage des données personnelles (e-mails, téléphones et IBAN) et détection des injections de prompt avant l'envoi des données à un fournisseur d'IA.
2. **Audit adversarial (Extracteur vs. Sceptique Mom Test) :** un premier agent extrait les citations importantes avec leurs numéros de ligne ; un second applique les principes du *Mom Test* pour signaler les compliments, les promesses hypothétiques et les questions orientées.
3. **Point de contrôle humain obligatoire — HALTED_AT_HUMAN_GATE :** le système s'arrête. Le fondateur doit examiner chaque contradiction et choisir de valider le comportement observé, d'écarter le signal biaisé ou de l'inscrire dans le registre des hypothèses à tester. Il reformule ensuite son hypothèse et choisit son segment GTM.
4. **Synthèse stratégique bilingue :** après validation humaine, FounderGate génère un ADR/SDR, un registre de dette d'hypothèses, cinq prochaines questions d'entretien non orientées et une matrice des objections des investisseurs.
5. **Accès frugal :** le projet est conçu pour fonctionner avec un mode Sandbox sans clé API, des offres gratuites de fournisseurs compatibles ou Ollama en local. Le coût d'inférence dépend des quotas et des conditions des fournisseurs.

**Principe fondamental :** l'IA ne choisit pas la stratégie du fondateur. Elle l'aide à examiner les preuves, à repérer les biais et à prendre une décision éclairée.

---

## What's next for FounderGate: Adversarial Mom-Test & GTM Discovery Agent

1. **Complete and publish the source tree:** commit the FastAPI backend, Next.js frontend, safety-gate implementation, model adapters, tests, Docker configuration, and n8n workflow export.
2. **Strengthen evaluation:** build a repeatable benchmark set covering compliments, hypothetical promises, leading questions, verified past behavior, sarcasm, multilingual phrasing, and prompt-injection attempts.
3. **Improve evidence quality:** add robust source provenance, confidence calibration, quote-level review, and clearer explanations for each skeptic flag.
4. **Harden privacy controls:** test redaction against varied formats and edge cases, document data retention, and review provider and deployment data-processing terms.
5. **Expand local-first workflows:** improve Ollama model selection, local resource checks, and graceful fallback behavior when hosted free tiers are unavailable.
6. **Improve decision traceability:** version the founder's hypotheses, adjudications, ADR/SDR records, and assumption-debt experiments.
7. **Validate the time-saved claims:** publish benchmark scripts, scenario data, raw run timings, token counts, and the exact manual-baseline methodology.

---

## How judges can test it

### Option A — Live web demo (zero setup)

1. Open the [FounderGate live demo](https://foundergate-hetic26.vercel.app).
2. Keep the engine on **Zero-Key Judge Sandbox (Instant)**, or select a supported provider and supply a key for its free tier.
3. Choose one of the three synthetic founder scenarios in the top-left dropdown.
4. Click **Run Adversarial Discovery Audit →**.
5. Confirm that the workflow stops at **HALTED_AT_HUMAN_GATE**.
6. Use **Auto-Fill Recommended Decisions (Judge Shortcut)** or manually classify every claim.
7. Review the pivoted hypothesis, then click **Sign Off Human Checkpoint & Generate Bilingual Strategic Decision Record →**.

### Option B — Local Docker run

The following is the intended one-command setup once the application source and Docker files are present in the repository.

~~~bash
git clone https://github.com/tejaswin-amara/FounderGate.git
cd FounderGate
docker compose up --build
~~~

| Service | Intended local URL |
|---|---|
| Frontend UI | http://localhost:3000 |
| FastAPI Swagger documentation | http://localhost:8000/docs |

Run the intended safety and human-gate tests with:

~~~bash
docker compose exec backend pytest
~~~

The repository must contain the relevant Docker Compose services and test suite for these commands to work. Do not commit real API keys; provide an **.env.example** with blank placeholder values and keep **.env** in **.gitignore**.

---

## Devpost submission readiness checklist

- [ ] **Demo video:** provide a YouTube or Vimeo video no longer than **3:00 minutes**. It should show a complete run, including **HALTED_AT_HUMAN_GATE**, human Accept/Discard/Debt decisions, and the unlocked Strategic Decision Record.
- [ ] **Team size:** confirm that **2–4 college student teammates aged 18+** are listed under Devpost **Manage Team**, as required by the challenge rules.
- [ ] **Secrets check:** ensure **.env** is ignored and only **.env.example** with blank keys is committed.
- [ ] **Public repository and workflow export:** keep the GitHub repository public and include the full-stack application and **workflows/n8n-foundergate-workflow.json**. The workflow link above will resolve once that file is committed.
- [ ] **Rules and legal agreement:** review and accept the official HETIC Paris challenge rules and the applicable governing-law agreement.
- [ ] **Final evidence review:** verify live URLs, provider/model availability, test results, benchmark evidence, and all claims in this story immediately before submission.

---

*FounderGate — Smarter decisions. Less hype.*
