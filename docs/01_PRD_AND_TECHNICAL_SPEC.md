# 01 — Product Requirements Document and Technical Specification

## 1. Product summary

**FounderGate** is an adversarial Customer Discovery and Go-To-Market (GTM) discovery agent for early-stage founders. It reviews raw interview transcripts and competitor context, extracts evidence, challenges optimistic interpretations using *The Mom Test*, and stops for explicit human adjudication before generating strategic artifacts.

**Core principle:** AI may organize and challenge evidence; only the human founder decides what the evidence means for company strategy.

## 2. Problem statement

Founders conduct customer-discovery interviews and collect competitor reviews, then spend substantial time manually coding notes. Conventional LLM summaries can amplify confirmation bias by treating compliments and hypothetical promises as evidence of demand.

FounderGate aims to reduce repetitive synthesis while preserving evidence provenance and a mandatory human judgment step.

## 3. Target users and jobs to be done

**Primary users**

- Early-stage startup founders.
- Student entrepreneurs.
- Product and go-to-market leaders conducting customer discovery.

**Core job to be done**

Turn raw customer-discovery transcripts and competitor notes into a bias-audited Strategic Decision Record (SDR), Assumption Debt Ledger, and testable GTM wedge—without delegating strategic judgment to an AI model.

## 4. Scope

### In scope

- Three synthetic founder scenarios.
- Custom transcript and competitor-context input.
- PII redaction and prompt-injection pre-flight checks.
- Evidence extraction with verbatim quotes and line references.
- Adversarial Mom-Test classification.
- A mandatory human checkpoint for every extracted claim.
- Pivot hypothesis and target GTM wedge entry.
- English/French strategic outputs.
- Provider and token telemetry.
- Deterministic zero-key sandbox and local inference option.

### Out of scope

- Autonomous product-market-fit certification.
- Automated investment decisions or fundraising recommendations presented as facts.
- Automatic approval of evidence by an LLM.
- Claims of complete GDPR compliance based only on text sanitization.
- Market-size estimates presented as validated by a small interview sample.

## 5. Functional requirements and proposed judging weights

The following weights are supplied project-planning values and must be checked against the official HETIC 2026 rubric before submission.

| ID | Requirement | Target judging criterion | Planning weight |
|---|---|---|---:|
| **FR-01** | Automate transcript PII screening, quote extraction, line citation, and Mom-Test bias classification. | Business value and time saved | **25%** |
| **FR-02** | Halt at `HALTED_AT_HUMAN_GATE` and require human adjudication of 100% of extracted claims before GTM synthesis. | Human judgment by design | **20%** |
| **FR-03** | Enforce structured schema validation, prompt-injection checks, and safe deterministic fallback behavior. | Agent design and reliability | **20%** |
| **FR-04** | Support configured free-tier and local providers with a target under 1,000 tokens per discovery run where feasible. | Frugality and accessibility | **15%** |
| **FR-05** | Provide one-click synthetic scenarios and a low-friction split-pane interface. | User experience | **10%** |
| **FR-06** | Provide token telemetry, time-saved methodology, redaction counts, and bilingual decision records. | Documentation and responsible AI | **10%** |

## 6. User workflow

1. The founder selects a synthetic scenario or supplies custom transcripts, a hypothesis, and competitor context.
2. The backend applies the safety gate.
3. The model router selects the chosen provider or deterministic sandbox.
4. The Extractor returns candidate evidence claims with verbatim quotes and source-line references.
5. The Mom-Test Skeptic challenges each claim and classifies likely bias patterns.
6. The backend stores the discovery session in `HALTED_AT_HUMAN_GATE`.
7. The founder adjudicates every claim as Accept, Discard, or Log Assumption Debt.
8. The founder records a pivoted hypothesis and target wedge.
9. The backend validates the entire decision set and only then generates the bilingual strategic artifacts.

## 7. State machine

~~~text
[IDLE]
  |
  | POST /api/v1/analyze
  v
[SAFETY_GATE]
  |-- Injection detected --------------------> [HTTP 400 BLOCKED]
  |-- Input rejected / invalid --------------> [4xx VALIDATION ERROR]
  |
  | Sanitized evidence accepted
  v
[ADVERSARIAL_ANALYSIS]
  |-- Extractor + Mom-Test Skeptic
  v
[HALTED_AT_HUMAN_GATE]
  |-- Any claim unresolved ------------------> [HTTP 422]
  |-- Missing pivot hypothesis -------------> [HTTP 422]
  |-- Invalid / unauthorized session -------> [4xx]
  |
  | POST /api/v1/checkpoint-resolve
  | all claims adjudicated + pivot supplied
  v
[COMPLETED_HUMAN_VERIFIED]
  |
  v
[Bilingual SDR + Assumption Debt Ledger
 + Next 5 Mom-Test Questions
 + Investor Objection Matrix]
~~~

A model response must never transition a session from `HALTED_AT_HUMAN_GATE` to `COMPLETED_HUMAN_VERIFIED`. That transition is reserved for an authorized human checkpoint action.

## 8. Synthetic scenario catalog

The intended built-in scenario keys are:

| Scenario key | Scenario | Example discovery domain |
|---|---|---|
| `b2b_invoice_ai` | B2B Invoice Recovery SaaS | Invoice follow-up, failed payments, receivables workflow. |
| `edtech_campus_copilot` | Student Alternance Copilot | Student placement, alternance search, campus workflows. |
| `greentech_packaging` | D2C GreenTech Packaging | Packaging compliance and sustainable-material workflows. |

All preloaded examples must be synthetic and must not contain identifiable third-party personal data.

## 9. Data contracts

### EvidenceClaim — proposed schema

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | Yes | Stable claim identifier within a session. |
| `quote` | string | Yes | Exact verbatim quote from the source transcript. |
| `source_interview` | string | Yes | Interview identifier or source label. |
| `source_line` | string or integer | Yes | Exact source line reference. |
| `extractor_reading` | string | Yes | Extractor's interpretation of the quote. |
| `skeptic_challenge` | string | Yes | Skeptic's counter-interpretation or challenge. |
| `bias_type` | enum/string | Yes | Compliment, hypothetical promise, leading question, verified past behavior, or uncertain. |
| `severity` | enum | Yes | Risk / evidence-strength classification. |
| `confidence_score` | number | Yes | Model confidence estimate, not a calibrated probability unless validated. |
| `founder_decision` | enum or null | Null before review | `ACCEPT_VERIFIED`, `DISCARD_BIASED`, or `LOG_ASSUMPTION_DEBT`. |
| `founder_note` | string or null | No | Human rationale. |

### Allowed founder decisions

- `ACCEPT_VERIFIED`
- `DISCARD_BIASED`
- `LOG_ASSUMPTION_DEBT`

The backend must reject values outside this set.

## 10. REST API contract

The schemas below are illustrative contracts from the project specification. They must be reconciled with the actual implementation before being treated as deployed API documentation.

### `GET /api/v1/scenarios`

Returns the built-in synthetic scenarios:

- `b2b_invoice_ai`
- `edtech_campus_copilot`
- `greentech_packaging`

### `POST /api/v1/analyze`

**Illustrative request:**

~~~json
{
  "scenario_key": "b2b_invoice_ai",
  "hypothesis": "Freelance design agencies will pay €29/month for a unified AI analytics dashboard.",
  "competitor_context": "Example competitor notes and market context.",
  "raw_evidence": "[Interview #1 - Line 12] ...",
  "provider": "sandbox_zero_key",
  "api_key": null
}
~~~

**Expected successful response shape:**

~~~json
{
  "session_id": "FG-EXAMPLE",
  "status": "HALTED_AT_HUMAN_GATE",
  "claims": [],
  "telemetry": {},
  "audit_log": []
}
~~~

The real system must not return fabricated claims when no evidence supports them. API-key handling should avoid reflecting or logging submitted secrets; a safer deployment may configure credentials server-side instead of accepting them in request bodies.

### `POST /api/v1/checkpoint-resolve`

**Illustrative request:**

~~~json
{
  "session_id": "FG-EXAMPLE",
  "decisions": [
    {
      "id": "CLM-01",
      "quote": "Exact source quote copied verbatim.",
      "source_interview": "Interview #1",
      "source_line": 12,
      "extractor_reading": "The extractor interpretation.",
      "skeptic_challenge": "The skeptic's challenge.",
      "bias_type": "Hypothetical Future Promise",
      "severity": "HIGH_RISK",
      "confidence_score": 0.94,
      "founder_decision": "DISCARD_BIASED",
      "founder_note": "Future intention without demonstrated behavior or budget."
    }
  ],
  "pivoted_hypothesis": "A testable revised hypothesis grounded in accepted evidence.",
  "target_wedge": "A narrowly defined use case and initial customer segment.",
  "language": "bilingual"
}
~~~

**Expected success response shape:**

~~~json
{
  "status": "COMPLETED_HUMAN_VERIFIED",
  "telemetry": {},
  "adr_report": "# Strategic Decision Record"
}
~~~

**Required validation behavior:**

- HTTP 422 if one or more claims have no decision.
- HTTP 422 if a decision is outside the allowed enum.
- HTTP 422 if the pivoted hypothesis is empty.
- Reject unknown, expired, wrong-owner, or already-resolved sessions according to the authentication/session policy.
- Generate GTM and investor artifacts only after successful human resolution.

## 11. Non-functional requirements

- **Security:** strict input validation, safe output validation, bounded request size, timeouts, and no secret logging.
- **Privacy:** minimize collection and retention; redact supported identifiers before external inference.
- **Reliability:** handle provider timeouts, rate limits, malformed JSON, and local-provider unavailability.
- **Traceability:** retain source quote, source line, claim identifier, and human decision provenance.
- **Accessibility:** keyboard-operable claim decisions, clear focus states, and readable status messages.
- **Frugality:** structured batching and local or zero-key execution paths.
- **Internationalization:** English and French report generation with human-reviewable wording.

## 12. Acceptance criteria

- [ ] Sanitization occurs before the external model request is constructed.
- [ ] Extracted quotes match their source lines exactly.
- [ ] Both Extractor and Skeptic interpretations are visible.
- [ ] Analysis ends in `HALTED_AT_HUMAN_GATE`.
- [ ] Every claim requires an explicit founder decision.
- [ ] Missing decisions and missing pivot hypotheses produce HTTP 422.
- [ ] The model cannot invoke the resolve route or approve claims.
- [ ] Strategic outputs are unavailable before human sign-off.
- [ ] Provider, model, latency, token, fallback, and estimated-cost telemetry are recorded where available.
- [ ] Synthetic datasets are used in judge demos and automated tests.
