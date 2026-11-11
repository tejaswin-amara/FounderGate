# FounderGate // Adversarial Mom-Test & GTM Discovery Agent

> **Submitted to:** AI Agents for Founders Challenge — HETIC 2026  
> **Runtime inference target:** €0.00 when using the built-in sandbox, local inference, or eligible free-tier allowances  
> **Core mission:** Give founders back their most valuable asset—**time to think**—by automating repetitive interview synthesis while forcing critical human judgment on confirmation bias.

<p align="center">
  <a href="https://foundergate-hetic26.vercel.app">Live Demo</a> ·
  <a href="https://github.com/tejaswin-amara/FounderGate">GitHub Repository</a>
</p>

### 🌍 English Overview & 🇫🇷 Résumé en Français

### 🇬🇧 English Summary

Early-stage founders lose hours every week manually tagging customer-discovery interviews and competitor reviews. Worse, standard chatbots can act as **sycophancy engines**—turning polite compliments such as “Your mockup looks sleek!” and hypothetical promises such as “I'd pay €29/month when you launch!” into false market validation.

**FounderGate** is a frugal, adversarial multi-agent Customer Discovery and Go-To-Market (GTM) engine. It:

1. **Screens privacy and security risks:** redacts supported personal identifiers (emails, phone numbers, and IBANs) before external model calls and checks untrusted input for prompt-injection patterns.
2. **Runs an adversarial dual-agent audit:** pits an **Optimistic Evidence Extractor** against a **Mom-Test Skeptic** to distinguish compliments, hypothetical future promises, and leading founder questions from evidence of past behavior and actual spending.
3. **Enforces a mandatory human checkpoint:** halts at `HALTED_AT_HUMAN_GATE` and blocks strategic synthesis until the founder adjudicates every claim as **Accept**, **Discard**, or **Log Assumption Debt**, then records a pivoted hypothesis.
4. **Generates bilingual strategic artifacts:** after sign-off, prepares an English/French Strategic Decision Record (ADR/SDR), Assumption Debt Ledger, next five non-leading interview questions, and Investor Pre-Emptive Objection Matrix.

**The principle:** AI audits evidence and reduces repetitive work; the founder retains strategic authority.

### 🇫🇷 Résumé exécutif

Les fondateurs de startups en phase de démarrage perdent des heures à analyser leurs entretiens clients et les avis concurrents. Pire encore, les assistants IA classiques peuvent amplifier le **biais de confirmation** en transformant des compliments polis et des promesses hypothétiques en fausse validation du marché.

**FounderGate** structure la découverte client autour du jugement critique humain :

1. **Protection des données et sécurité :** anonymisation des données personnelles prises en charge (e-mails, téléphones et IBAN) et détection des injections de prompt avant tout appel à un modèle externe.
2. **Audit adversarial :** un Extracteur de preuves confronte ses interprétations à un Sceptique appliquant les principes du *Mom Test*.
3. **Point de contrôle humain obligatoire :** l'exécution s'arrête à `HALTED_AT_HUMAN_GATE`. Le fondateur doit accepter, écarter ou inscrire chaque affirmation dans le registre de dette d'hypothèses avant de débloquer la synthèse stratégique.
4. **Synthèse bilingue :** après validation humaine, FounderGate prépare un ADR/SDR, un registre de dette d'hypothèses, cinq questions d'entretien non orientées et une matrice des objections des investisseurs en anglais et en français.

**Principe fondamental :** l'IA aide à examiner les preuves ; le fondateur prend la décision stratégique.

---

### ⚡ 30-Second Judge Verification

### Option 1: Docker Compose

The following commands describe the intended setup once the application source, Docker Compose file, and environment template have been committed:

~~~bash
git clone https://github.com/tejaswin-amara/FounderGate.git
cd FounderGate
cp .env.example .env
docker compose up --build
~~~

- **Frontend workspace:** http://localhost:3000
- **FastAPI interactive docs:** http://localhost:8000/docs

### Option 2: Local manual run

**Backend (Python 3.11+):**

~~~bash
cd backend
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
~~~

**Frontend (Node.js 20+):**

~~~bash
cd frontend
npm install
npm run dev
~~~

### Option 3: Automated tests

~~~bash
cd backend
pytest -v
~~~

The intended test suite should verify:

1. PII redaction, including `[REDACTED_EMAIL_GDPR]`, `[REDACTED_PHONE_GDPR]`, and `[REDACTED_IBAN_GDPR]`.
2. Prompt-injection blocking with HTTP 400.
3. Hard human-checkpoint enforcement, including HTTP 422 when any claim is unadjudicated or the pivoted hypothesis is missing.

> **Repository readiness note:** This repository currently contains the documentation suite. The application source, Docker Compose configuration, environment template, test suite, and n8n workflow export must be added and verified before the commands above can be treated as runnable instructions. No API keys should be committed.

---

### 📚 Documentation Index

| File | Purpose |
|---|---|
| [AGENTS.md](./AGENTS.md) | AI coding and runtime governance: explicit state, hard lifecycle gates, evidence grounding, token frugality, and secret handling. |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Student-team roles, branch and pull-request workflow, quality checks, and secret-leak prevention. |
| [SECURITY.md](./SECURITY.md) | Privacy controls, prompt-injection defense, STRIDE threat model, and security verification requirements. |
| [docs/01_PRD_AND_TECHNICAL_SPEC.md](./docs/01_PRD_AND_TECHNICAL_SPEC.md) | Product requirements, state machine, data contracts, and API schemas. |
| [docs/02_AGENT_PROMPTS_AND_RUBRICS.md](./docs/02_AGENT_PROMPTS_AND_RUBRICS.md) | Extractor, Mom-Test Skeptic, and Synthesizer prompt contracts and classification rubric. |
| [docs/03_ADR_LOG.md](./docs/03_ADR_LOG.md) | Architecture Decision Records ADR-001 through ADR-003. |
| [docs/04_AI_DISCLOSURE_AND_TIME_SAVED_AUDIT.md](./docs/04_AI_DISCLOSURE_AND_TIME_SAVED_AUDIT.md) | Equal Access AI provider ledger, token accounting, and time-saved methodology. |
| [docs/05_RESPONSIBLE_AI_AND_LIMITATIONS.md](./docs/05_RESPONSIBLE_AI_AND_LIMITATIONS.md) | Data provenance, bias mitigation, failure modes, and synthetic-data policy. |
| [docs/06_DEVELOPMENT_ROADMAP_AND_RUNBOOK.md](./docs/06_DEVELOPMENT_ROADMAP_AND_RUNBOOK.md) | November 16–December 18, 2026 development roadmap, QA checklist, recovery guide, and judge runbook. |

### Repository layout

~~~text
FounderGate/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── SECURITY.md
└── docs/
    ├── 01_PRD_AND_TECHNICAL_SPEC.md
    ├── 02_AGENT_PROMPTS_AND_RUBRICS.md
    ├── 03_ADR_LOG.md
    ├── 04_AI_DISCLOSURE_AND_TIME_SAVED_AUDIT.md
    ├── 05_RESPONSIBLE_AI_AND_LIMITATIONS.md
    └── 06_DEVELOPMENT_ROADMAP_AND_RUNBOOK.md
~~~

---

## Inspiration

Early-stage founders need reliable evidence, not another chatbot that agrees with them. Customer interviews contain a mixture of real pain, polite encouragement, hypothetical buying intentions, and founder-led questions. Treating all of these as validation can send a team into months of building for a problem that customers have not demonstrated they will pay to solve.

Inspired by Rob Fitzpatrick's *The Mom Test*, FounderGate makes the AI challenge optimistic interpretations and forces a founder to confront each unresolved claim before strategy is generated.

## What it does

FounderGate accepts interview transcripts and competitor context, applies privacy and prompt-injection checks, runs an adversarial Extractor-versus-Skeptic review, and halts at `HALTED_AT_HUMAN_GATE`. The founder classifies every claim as `ACCEPT_VERIFIED`, `DISCARD_BIASED`, or `LOG_ASSUMPTION_DEBT`, and records a pivoted hypothesis and target wedge. Only then does the system prepare bilingual decision records, an assumption-debt ledger, five non-leading interview questions, and an investor objection matrix.

## How we built it

The intended stack is Python, FastAPI, Pydantic, Next.js, React, TypeScript, Tailwind CSS, n8n, and Docker, with configurable access to Gemini, Mistral, Groq, Ollama, OpenRouter, Hugging Face, and a deterministic zero-key sandbox. The architecture, API contracts, agent rubrics, and run instructions are documented in the files linked above.

### System Architecture

The intended application flow is illustrated below. The diagram describes the planned architecture; it is not a claim that every component is already implemented in this documentation-only repository.

~~~mermaid
flowchart TB
    subgraph Input["1. Input and GDPR / Security Gate"]
        A["Synthetic founder scenario or custom transcripts and competitor notes"]
        B["Safety gate: PII redaction, prompt-injection checks, action log"]
        A --> B
    end
    subgraph Router["2. Equal-access AI Router"]
        R{"Zero-cost / local model router"}
        R1["Google AI Studio: Gemini"]
        R2["Mistral"]
        R3["Groq"]
        R4["Ollama local"]
        R5["OpenRouter / Hugging Face"]
        R -.-> R1
        R -.-> R2
        R -.-> R3
        R -.-> R4
        R -.-> R5
    end
    subgraph Audit["3. Adversarial Discovery Loop"]
        C["Agent 1: Evidence Extractor"]
        D["Agent 2: Mom-Test Skeptic"]
        E["Contradiction and Evidence Matrix"]
        C -->|"Verbatim quotes and line citations"| D
        D --> E
    end
    subgraph Gate["4. Mandatory Human Checkpoint"]
        F{"HALTED_AT_HUMAN_GATE"}
        G["Founder adjudicates every claim"]
        H["Pivoted hypothesis and target GTM wedge"]
        F --> G --> H
    end
    subgraph Synthesis["5. Post-gate Synthesis"]
        I["Agent 3: GTM and Investor Synthesizer"]
        J["ADR / SDR and Assumption Debt Ledger"]
        K["Next five interview questions and investor objection matrix"]
        I --> J
        I --> K
    end
    B --> C
    E --> F
    H --> I
    R --> C
    R --> D
    R --> I
~~~


## Challenges we ran into

The central challenges are resisting AI sycophancy, preserving exact quote provenance, enforcing the human checkpoint at the backend rather than only in the UI, handling sarcasm and culturally polite phrasing, and remaining usable when free-tier providers are rate-limited. Regex redaction and prompt-pattern checks are safeguards, not guarantees; provider quotas, model behavior, and privacy obligations must be reviewed for each deployment.

## Accomplishments that we're proud of

- A two-perspective evidence audit instead of one-sided transcript summarization.
- A mandatory lifecycle gate that requires a founder decision for every extracted claim.
- Verbatim quote and source-line traceability.
- Privacy-oriented preprocessing and prompt-injection checks.
- A zero-key sandbox and local-inference design for low-friction evaluation.
- Post-gate strategic artifacts in English and French.
- A benchmark methodology that makes manual baseline, human-review time, and claimed time savings explicit.

### Reported time-saved benchmark

The supplied benchmark notes describe three synthetic discovery scenarios:

| Scenario | Manual baseline | FounderGate + human checkpoint | Reported time saved | Reduction |
|---|---:|---:|---:|---:|
| B2B Invoice Recovery SaaS | 95 min | 5 min | 90 min | 94.7% |
| Student Alternance Copilot | 88 min | 4.5 min | 83.5 min | 94.9% |
| D2C Packaging Compliance Auditor | 85 min | 4 min | 81 min | 95.3% |

These figures are project-reported estimates. Publish raw timings and benchmark scripts before describing them as independently reproduced measurements.

## What we learned

- Customer enthusiasm is not the same as verified past behavior or willingness to pay.
- Opposing agent interpretations are more useful when both remain visible and grounded in source evidence.
- A meaningful human-in-the-loop design must be enforced by backend state and endpoint validation.
- Synthetic data makes demos safer and repeatable, but does not prove real-world market demand.
- Token and time-saved claims need explicit baselines, repeatable methods, and raw measurements.
- Redaction and prompt-injection filters reduce risk but cannot guarantee complete privacy or security.

## What's next for FounderGate: Adversarial Mom-Test & GTM Discovery Agent

1. Commit and test the FastAPI backend, Next.js frontend, provider adapters, safety gate, and human checkpoint.
2. Publish the n8n workflow export and verify that it matches the documented workflow.
3. Add a repeatable evaluation corpus for compliments, promises, leading questions, past behavior, sarcasm, multilingual language, and prompt injection.
4. Harden PII handling, retention controls, provider disclosures, and local-first inference.
5. Version founder hypotheses, adjudications, ADR/SDR records, and assumption-debt experiments.
6. Reproduce the token and time-saved benchmarks with scripts, raw measurements, and documented baselines.
7. Complete QA, the three-minute judge demo, and the HETIC 2026 submission checklist by December 18, 2026, 5:00 PM CET.

> **Accuracy and compliance note:** This documentation describes the intended design and team-supplied specifications. GDPR compliance, security effectiveness, free-tier availability, benchmark results, and implementation status must be verified against the actual code, provider terms, test evidence, and applicable legal requirements. PII scrubbing alone does not establish GDPR compliance.

*FounderGate — Smarter decisions. Less hype.*
