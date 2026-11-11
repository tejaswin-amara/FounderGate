# 06 — Development Roadmap (November 16–December 18, 2026) and Operational Runbook

> **Planning window:** November 16 to December 18, 2026.  
> **Submission deadline in the supplied project brief:** December 18, 2026 at 5:00 PM CET.  
> Confirm all dates and rules against the official HETIC 2026 challenge communication before relying on them.

## 1. Sprint plan and milestones

### November 16, 2026 — Kick-off and Sprint 1: Core engine and safety gate

- Initialize application repository structure, `.gitignore`, and sanitized `.env.example`.
- Implement the safety boundary: supported PII redaction and prompt-injection checks.
- Define strict request/response schemas and the evidence-claim model.
- Implement the provider router with configured free-tier/local options and a zero-key sandbox.
- Add unit tests for redaction, injection rejection, and schema validation.
- Record initial architecture decisions in `docs/03_ADR_LOG.md`.

**Exit criteria:**
- Safety checks run before any external provider request.
- No secrets are committed.
- Synthetic scenarios load deterministically.
- Initial safety tests pass.

### November 23–30, 2026 — Sprint 2: Adversarial agents and hard human gate

- Calibrate Agent 1 (Evidence Extractor) and Agent 2 (Mom-Test Skeptic) structured prompts.
- Implement quote provenance and line-reference validation.
- Implement `POST /api/v1/analyze`.
- Implement `POST /api/v1/checkpoint-resolve`.
- Enforce HTTP 422 for unresolved claims or a missing pivot hypothesis.
- Ensure model output cannot approve claims or invoke checkpoint resolution.
- Add tests for session ownership, invalid decisions, and lifecycle transitions.

**Exit criteria:**
- Analysis halts at `HALTED_AT_HUMAN_GATE`.
- Every claim requires an explicit founder decision.
- No strategic synthesis occurs before successful human resolution.

### December 1–10, 2026 — Sprint 3: Split-pane UI and bilingual artifacts

- Build the Next.js human-checkpoint interface.
- Implement side-by-side Extractor/Skeptic evidence cards.
- Add one-click synthetic scenario presets.
- Provide accessible Accept / Discard / Log Assumption Debt controls.
- Capture pivot hypothesis and target GTM wedge.
- Add bilingual EN/FR Strategic Decision Record and report export.
- Display provider, model, token, latency, and fallback telemetry where available.

**Visual direction in project notes:** dark interface (`#080808`) with cyan telemetry (`#22D3EE`). Treat these as design tokens, not mandatory accessibility choices; verify contrast and keyboard operation.

**Exit criteria:**
- All claims can be adjudicated.
- Human gate state is clear and accessible.
- Post-gate outputs are generated only after valid sign-off.
- English and French artifacts are reviewed.

### December 11–18, 2026 — Sprint 4: QA, demo, and submission

- Run the complete backend and frontend test suites.
- Test the zero-key sandbox without provider credentials.
- Test local Ollama mode where hardware permits.
- Test hosted-provider failure, rate limits, malformed output, and fallback.
- Export and validate `workflows/n8n-foundergate-workflow.json`.
- Verify the public repository, live demo, and documentation links.
- Record a demo video under three minutes, showing the human checkpoint.
- Review the official challenge rules and complete the Devpost submission before the stated deadline.

**Exit criteria:**
- Critical tests pass and results are recorded.
- No secrets or unauthorized third-party data are present.
- Demo video shows the complete human-gated workflow.
- All links and claims are checked against the actual release.

## 2. Quality assurance checklist

### Backend and API

- [ ] Pydantic schemas reject malformed inputs.
- [ ] PII redaction runs before provider request construction.
- [ ] Prompt injection is rejected before external inference.
- [ ] Quotes and line references are checked against source evidence.
- [ ] Session state and ownership are validated.
- [ ] HTTP 422 is returned for unresolved claims.
- [ ] HTTP 422 is returned for a missing pivot hypothesis.
- [ ] LLM output cannot invoke the checkpoint resolver.
- [ ] Post-gate synthesis is impossible before human sign-off.
- [ ] Provider timeout, rate-limit, and malformed-output paths are tested.

### Frontend

- [ ] Claim cards show source evidence and both interpretations.
- [ ] Accept, Discard, and Log Assumption Debt are keyboard accessible.
- [ ] The status `HALTED_AT_HUMAN_GATE` is visible.
- [ ] Unresolved claims are clearly identified.
- [ ] The pivot hypothesis is required.
- [ ] Loading, error, fallback, and success states are distinct.
- [ ] EN/FR output is reviewed.
- [ ] Sensitive transcript content is not exposed in analytics or client error logs.

### Repository and release

- [ ] `.env` is ignored.
- [ ] `.env.example` has blank placeholders.
- [ ] Secret scanning is run.
- [ ] License and attribution notices are reviewed.
- [ ] README and all documentation links resolve.
- [ ] n8n export is present and opens as valid JSON.
- [ ] Benchmark claims have a documented method and raw data.
- [ ] Demo recording contains no real personal data or credentials.

## 3. Operational troubleshooting runbook

| Symptom | Possible cause | Recovery action |
|---|---|---|
| **HTTP 400: Security Gate Blocked** | Input matches a configured prompt-injection pattern. | Inspect the input. Remove embedded instructions that are not part of the evidence. Do not disable the safety gate just to make the request pass. |
| **HTTP 422: Lifecycle Gate Blocked** | One or more claims remain unresolved, a decision enum is invalid, or the pivot hypothesis is empty. | Review every claim and select Accept, Discard, or Log Assumption Debt. Enter a non-empty pivot hypothesis and retry. |
| **Hosted provider HTTP 429** | Free-tier request or token quota has been reached. | Respect retry guidance and provider rate limits. Select another eligible provider, local Ollama, or the deterministic sandbox. Make fallback visible to the user. |
| **Hosted provider timeout / malformed JSON** | Provider latency, outage, or response-format mismatch. | Apply bounded retries only where safe, validate all outputs, and use a disclosed fallback. Never treat malformed output as approved evidence. |
| **Local Ollama connection refused** | Ollama is not running or the selected model is unavailable. | Start the Ollama service, verify the configured endpoint, pull the selected model if appropriate, or switch to the zero-key sandbox. |
| **Missing PII redaction** | Unsupported identifier format or regression in sanitizer. | Stop external transmission, preserve a synthetic reproduction, add a regression test, and fix the sanitizer before retrying. |
| **Quote or line reference mismatch** | Model paraphrase, hallucinated citation, or line-number normalization mismatch. | Reject the affected claim, compare it with the original source, and add a test case. Do not let the founder accept unverified text as a verbatim quote. |
| **Docker service fails to start** | Missing environment variable, dependency, port conflict, or invalid Compose configuration. | Inspect service logs, validate environment placeholders, confirm ports, and rerun the relevant service. Do not paste secrets into public issue logs. |

## 4. Thirty-second judge runbook

### Option A — Live web demo

1. Open the deployed demo URL supplied for the project: https://foundergate-hetic26.vercel.app
2. Select **Zero-Key Judge Sandbox (Instant)** for a no-key path, if available in the deployed build.
3. Select one of the three synthetic founder scenarios.
4. Click **Run Adversarial Discovery Audit**.
5. Verify that the workflow stops at `HALTED_AT_HUMAN_GATE`.
6. Inspect the Extractor quote, source line, and Skeptic challenge.
7. Use **Auto-Fill Recommended Decisions** or manually adjudicate every claim.
8. Review the pivoted hypothesis and sign off.
9. Inspect the bilingual Strategic Decision Record and Assumption Debt Ledger.

The judge path should not require a personal API key. If the live deployment does not expose the stated controls, use the actual deployed UI labels and document the difference.

### Option B — Local Docker run

Once the app and Compose files are committed:

~~~bash
git clone https://github.com/tejaswin-amara/FounderGate.git
cd FounderGate
cp .env.example .env
docker compose up --build
~~~

- Frontend: http://localhost:3000
- FastAPI docs: http://localhost:8000/docs

Run backend tests:

~~~bash
docker compose exec backend pytest -v
~~~

### Option C — Manual backend and frontend run

**Backend:**

~~~bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
~~~

**Frontend in a second terminal:**

~~~bash
cd frontend
npm install
npm run dev
~~~

Use the Windows virtual-environment activation command when running PowerShell.

## 5. Three-minute demo video outline

| Time | What to show | Key message |
|---|---|---|
| 0:00–0:20 | Problem and founder hypothesis | Conventional AI can mistake compliments for validation. |
| 0:20–0:55 | Select a synthetic scenario and run the audit | FounderGate screens input and extracts traceable evidence. |
| 0:55–1:30 | Extractor vs. Skeptic evidence cards | The system exposes conflicting interpretations and Mom-Test anti-patterns. |
| 1:30–2:10 | `HALTED_AT_HUMAN_GATE`; adjudicate every claim | AI cannot approve its own evidence or make the strategic decision. |
| 2:10–2:40 | Sign off and inspect ADR/SDR, debt ledger, five questions, and objection matrix | Useful strategy artifacts are generated only after human review. |
| 2:40–3:00 | Model options, privacy safeguards, and closing | Free-tier/local design; human judgment remains central. |

## 6. Submission checklist

- [ ] Video link is YouTube or Vimeo and no longer than 3:00 minutes.
- [ ] Video demonstrates the complete workflow including the mandatory human checkpoint.
- [ ] Team membership and student eligibility satisfy the official 2–4 member requirement.
- [ ] Public GitHub repository contains the application and documentation.
- [ ] `workflows/n8n-foundergate-workflow.json` is committed and validated.
- [ ] `.env` is ignored and `.env.example` contains no credentials.
- [ ] Provider/model and free-tier statements are current and accurately qualified.
- [ ] Benchmark data and time-saved claims are reproducible or labeled as estimates.
- [ ] The official HETIC rules and legal acceptance are reviewed.
- [ ] Submission is completed before the official deadline.

## 7. Schedule and incident contacts

- **Planning start:** November 16, 2026.
- **Final QA and submission window:** December 11–18, 2026.
- **Deadline stated in project notes:** December 18, 2026, 5:00 PM CET.

Maintain an internal team contact and escalation list outside this public document. Do not publish private phone numbers, API credentials, or sensitive access details here.
