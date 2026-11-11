# Contributing to FounderGate

Thank you for contributing. FounderGate is being developed for the AI Agents for Founders Challenge — HETIC 2026. Contributions should preserve evidence traceability, privacy safeguards, the mandatory human checkpoint, and low-cost access.

## 1. Team structure and responsibilities

The challenge submission is intended for a team of **2–4 college student teammates aged 18+**, subject to the official challenge rules.

Suggested responsibility areas (combine roles when the team has fewer than four members):

| Role | Ownership area | Typical responsibilities |
|---|---|---|
| Backend and Safety Lead | `backend/` | FastAPI routes, Pydantic schemas, `safety_gate.py`, model router, audit events, pytest coverage. |
| Frontend and Human Checkpoint UX Lead | `frontend/` | Next.js application, claim adjudication cards, accessibility, responsive UI, API integration. |
| Prompt Engineering and Evaluation Lead | Agent prompts and synthetic datasets | Extractor/Skeptic prompts, Mom-Test rubric, provider comparisons, EN/FR report quality, evaluation corpus. |
| Documentation, Telemetry, and Demo Lead | `docs/`, `workflows/` | Documentation, n8n workflow export, token/time-saved methodology, test evidence, and three-minute demo video. |

Role ownership does not remove the requirement for peer review on security-sensitive changes.

## 2. Development prerequisites

The planned application setup uses:

- Python 3.11 or newer for the backend.
- Node.js 20 or newer for the frontend.
- Docker and Docker Compose for containerized development.
- Git and a GitHub account.
- Optional provider credentials for hosted model testing.
- Ollama for local model testing.

Confirm the actual versions and commands against the committed package and environment files once the application is present.

## 3. Branching workflow

1. Update your local `main` branch.
2. Create a focused branch:

~~~bash
git checkout main
git pull --ff-only
git checkout -b feat/short-description
~~~

3. Make one coherent change at a time.
4. Add or update tests and documentation.
5. Run relevant checks locally.
6. Commit with a conventional commit message.
7. Open a pull request against `main`.

Suggested branch prefixes:

- `feat/` — user-visible feature.
- `fix/` — defect correction.
- `docs/` — documentation-only change.
- `test/` — tests and evaluation fixtures.
- `security/` — security or privacy hardening.
- `chore/` — tooling and maintenance.

## 4. Pull-request checklist

Every pull request should include:

- [ ] A concise problem statement and proposed solution.
- [ ] Linked issue or relevant ADR, where applicable.
- [ ] Tests for changed behavior.
- [ ] Confirmation that the human checkpoint cannot be bypassed.
- [ ] Confirmation that quotes and line references remain source-grounded.
- [ ] Privacy and prompt-injection impact assessment for input/model changes.
- [ ] Updated documentation and API schemas where necessary.
- [ ] No secrets, real personal data, or private transcripts in the diff.
- [ ] Test, lint, format, and type-check results (or a clear explanation if a check cannot run).
- [ ] Screenshots or a short recording for significant UI changes.

## 5. Backend verification

When the backend test suite exists, run:

~~~bash
cd backend
pytest -v
~~~

At minimum, tests should cover:

- PII redaction for supported email, phone, and IBAN formats.
- Prompt-injection rejection before external provider invocation.
- Correct transitions into `HALTED_AT_HUMAN_GATE`.
- HTTP 422 when any claim is unresolved or the pivoted hypothesis is missing.
- Rejection of stale, unknown, or already-resolved sessions.
- No post-gate synthesis before human sign-off.
- Structured-output validation and safe provider fallback.

## 6. Secret-leak prevention

Never commit:

- `.env` files or real API keys.
- GitHub, Vercel, cloud, or provider access tokens.
- Real customer interview transcripts or third-party personal data.
- Private customer or competitor exports.

Commit `.env.example` only with blank placeholders. Before committing, inspect staged files:

~~~bash
git diff --cached --name-only
git diff --cached
~~~

Use a secret scanner such as Gitleaks in local and CI workflows when configured. A simple pattern search is not a substitute for a secret scanner, and a clean scan does not guarantee that no secret exists.

If a secret is exposed:

1. Revoke or rotate it immediately at the issuing provider.
2. Remove it from the current source and configuration.
3. Follow the repository's history-remediation process if it was committed.
4. Check logs, CI artifacts, deployments, and forks for exposure.
5. Record the incident without pasting the secret into an issue or pull request.

## 7. Documentation and decision records

Changes to lifecycle behavior, provider routing, data retention, security boundaries, or architectural dependencies require an update to `docs/03_ADR_LOG.md`.

Prompt changes must update `docs/02_AGENT_PROMPTS_AND_RUBRICS.md` and relevant evaluation fixtures. Benchmark methodology changes must update `docs/04_AI_DISCLOSURE_AND_TIME_SAVED_AUDIT.md`.

## 8. License and third-party materials

Do not copy code, prompts, templates, or assets from another project without checking its license and attribution requirements. Keep upstream notices where required and document material adaptations in the repository.
