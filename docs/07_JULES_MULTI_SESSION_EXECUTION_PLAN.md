# 07 — Google Jules Multi-Session Execution Plan

Project: FounderGate  
Repository: https://github.com/tejaswin-amara/FounderGate  
Planning window: November 16–December 18, 2026

## Purpose

Use multiple bounded Jules sessions to implement FounderGate, with isolated branches, explicit dependencies, plan approval, tests, independent security review, and human-controlled merges. Do not ask one session to build the entire application.

## Baseline

The repository currently contains the product and engineering documentation. The first session must inspect the live repository tree and confirm what code exists before scaffolding. If code has been added since this plan was written, extend it; do not overwrite it.

## Operating rules

1. Follow AGENTS.md, CONTRIBUTING.md, and SECURITY.md.
2. One session owns one bounded deliverable and a clearly defined set of paths.
3. Each implementation session uses its own branch and submits a PR.
4. Review Jules' plan before code execution.
5. No direct commits to main and no automatic merging.
6. Do not start dependent work until prerequisite PRs are merged.
7. No real keys, credentials, private interview transcripts, or third-party personal data in Git, prompts, setup scripts, or logs.
8. No external model call before input sanitization.
9. No GTM/Investor synthesis before every claim is adjudicated by a human.
10. Do not report tests, benchmarks, provider availability, GDPR compliance, or deployment status without evidence.

## Jules setup

1. Open https://jules.google/ and connect only the tejaswin-amara/FounderGate GitHub repository.
2. Confirm main is the default branch and AGENTS.md is visible.
3. For each task, select the branch named in its session card, paste its prompt, choose Give me a plan, review every step, and approve only when the scope and tests are correct.
4. Once manifests exist, configure Jules Initial Setup to install pinned backend/frontend dependencies and run lint, type checks, tests, and builds without requiring secrets. Validate the setup and create an environment snapshot.
5. Review every diff and PR manually; merge only when required CI checks pass.

### Concurrency

Use three concurrent sessions as the default. Google's published Jules limits currently list 3 concurrent tasks on the base plan, 15 on Pro, and 60 on Ultra; verify the live limits before scheduling more. Keep concurrency lower if branches share files or interfaces.

References: https://jules.google/docs/usage-limits and https://jules.google/docs/environment/

## Session sequence

| ID | Session | Dependencies | Main ownership |
|---|---|---|---|
| J00 | Read-only repository audit | None | No code edits; return baseline, architecture questions, gaps, and acceptance tests. |
| J01 | Foundation and API contract freeze | J00 approved | Workspace manifests, lockfiles, .gitignore, .env.example, app skeleton, shared contracts. |
| J02 | Backend domain and session state | J01 merged | Pydantic models, session lifecycle, allowed human decisions, state validation, unit tests. |
| J03 | Privacy and security gate | J01 merged | PII sanitizer, injection checks, safe audit events, security tests. |
| J04 | Provider router and deterministic sandbox | J01 merged | Provider interface, zero-key sandbox, provider adapters, timeouts, fallback, tests. |
| J05 | Adversarial agents and evidence grounding | J02–J04 merged | Extractor, Mom-Test Skeptic, prompt contracts, quote/line verification, fixtures. |
| J06 | FastAPI orchestration and synthesis | J02–J05 merged | Analyze/resolve APIs, lifecycle enforcement, ADR/SDR and post-gate outputs. |
| J07 | Frontend shell and design system | J01 merged | Next.js shell, routes, styles, reusable primitives, mocked screens. |
| J08 | Human checkpoint UI/API integration | J06 and J07 merged | Evidence cards, accept/discard/debt, pivot form, report UI, API tests. |
| J09 | n8n workflow export | J06 merged | Importable workflow JSON, credential placeholders, safe human-gate behavior. |
| J10 | Integration/E2E evaluation | J08 and J09 merged | Cross-stack tests, synthetic evaluation corpus, Playwright full workflow. |
| J11 | Docker, CI, and security automation | J06–J10 merged | Compose, GitHub Actions, secret scanning, dependency checks. |
| J12 | Independent security audit | J10/J11 merged | Read-only adversarial review and severity-ranked findings. |
| J13 | Remediation and regression closure | J12 findings triaged | Focused fixes for accepted findings, regression tests. |
| J14 | Release readiness and docs reconciliation | J13 merged | README/docs reconciled to actual code, final runbook and checklist. |

## Dependency waves

- Wave 0: J00 only.
- Wave 1: J01 only.
- Wave 2: J02 + J03 + J04 (three concurrent sessions).
- Wave 3: J05 + J07 (two concurrent sessions).
- Wave 4: J06 only.
- Wave 5: J08 + J09 (two concurrent sessions).
- Wave 6: J10 + J11 (two concurrent sessions, provided path ownership is respected).
- Wave 7: J12 only.
- Wave 8: J13 (parallelize only if audit findings are independent and each has a separate path owner).
- Wave 9: J14 only.

All dependent sessions start from the latest main after prerequisite PRs are merged. Parallel work is allowed only when paths and interfaces are independent.

## Global prompt preamble

Paste this preamble at the start of every implementation-session prompt:

> Read AGENTS.md, CONTRIBUTING.md, SECURITY.md, and the relevant docs before editing. Inspect the current main branch and reuse existing code. Work only within the session's stated path ownership. Do not overwrite another session's files or duplicate existing abstractions. Do not commit secrets or personal data. Do not bypass the safety gate or human checkpoint. Do not change architecture/dependencies without an ADR and maintainer approval. Add tests for every behavior change. Run the relevant test, lint, type-check, and build commands. Report exact commands and actual results. Create a focused branch and PR; never push directly to main or merge your own PR.

## Session prompts

### J00 — Read-only repository audit

Branch: main. No code changes or PR.

~~~text
Audit the complete FounderGate repository in read-only mode. Read all existing
documentation and inspect the actual repository tree. Distinguish implemented
code from planned requirements. Return: exact tree, requirements-to-files
matrix, missing components, documentation conflicts, recommended minimum
architecture, decisions requiring human approval (session persistence,
authentication/ownership, deployment topology, provider secrets), proposed
directory structure, shared API contracts, highest risks, and release
acceptance tests. Do not edit files or claim that planned features exist.
~~~

### J01 — Foundation and API contracts

Branch: feat/jules-foundation. Depends on J00 approval.

~~~text
Create the smallest maintainable monorepo foundation for FastAPI/Pydantic
(Python 3.11+) and Next.js/React/TypeScript/Tailwind. Prefer uv and pnpm if
there is no established repository convention. Add pinned manifests and
lockfiles, .gitignore, blank-placeholder .env.example, app skeletons, and a
lightweight Jules setup path. Freeze API contracts for GET /api/v1/scenarios,
POST /api/v1/analyze, POST /api/v1/checkpoint-resolve, EvidenceClaim,
founder-decision enums, and lifecycle states. Do not implement business logic,
providers, agents, or product screens. Do not introduce a database, auth
vendor, or orchestration framework without an approved ADR. Validate clean
installation and baseline commands. Open a PR.
~~~

### J02 — Backend domain and session state

Branch: feat/backend-domain-state. Depends on J01.

~~~text
Implement strict Pydantic schemas, EvidenceClaim, allowed decisions
ACCEPT_VERIFIED/DISCARD_BIASED/LOG_ASSUMPTION_DEBT, explicit lifecycle states,
session ownership/expiry validation, and checkpoint decision validation.
Reject unresolved claims, invalid enums, missing/blank pivot hypotheses,
unknown/expired/wrong-owner sessions, and illegal state transitions.
Do not implement provider calls, safety screening, API routes, or frontend.
Do not silently add database/auth infrastructure; follow the approved J00/J01
decision. Add unit tests for all validation and lifecycle cases. Open a PR.
~~~

### J03 — Privacy and security gate

Branch: feat/backend-safety-gate. Depends on J01.

~~~text
Implement verify_and_sanitize_input() in the dedicated backend safety module.
Redact supported email, phone, and IBAN identifiers to the documented
placeholders before any external model request is constructed. Add prompt
injection checks and safe reason codes/audit events without raw input.
Test formats, punctuation, multiple occurrences, false positives, attack
phrases, and absence of seeded personal identifiers from sanitized output.
Do not claim regex checks guarantee GDPR compliance or solve all prompt
injection. Do not edit domain schemas, provider router, API routes, or UI.
Open a PR with exact test results.
~~~

### J04 — Model router and zero-key sandbox

Branch: feat/llm-router-sandbox. Depends on J01.

~~~text
Implement a narrow structured-JSON provider interface and deterministic
sandbox_zero_key using synthetic fixtures. Add adapters only for configured
Gemini, Mistral, Groq, Ollama, OpenRouter, and Hugging Face options. Read
credentials server-side only. Add schema validation, bounded timeouts/retries,
observable provider/model/latency/token/fallback telemetry, and explicit
fallback behavior. Never label sandbox output as a live LLM response. Do not
claim free-tier quotas are permanent. Test no-key mode, missing config,
malformed JSON, timeout, HTTP 429, provider errors, and secret-safe logging.
Do not edit domain, safety, API, or frontend modules. Open a PR.
~~~

### J05 — Adversarial agents and evidence grounding

Branch: feat/adversarial-agent-engine. Depends on J02–J04.

~~~text
Implement Agent 1 Evidence Extractor and Agent 2 Mom-Test Skeptic using the
approved domain, safety, and provider interfaces. Extract atomic candidate
claims with verbatim quotes, source interview IDs, and exact line references.
Skeptic must flag compliments, hypothetical future promises, leading founder
questions, missing context, sarcasm, contradictions, and sample bias. Verify
each quote/line against the source; reject fabricated or mismatched citations.
Neither agent may set founder_decision or generate post-gate GTM outputs.
Add synthetic English/French evaluation cases. Do not edit API routes or UI.
Open a PR with prompt versions and test results.
~~~

### J06 — FastAPI orchestration

Branch: feat/fastapi-orchestration. Depends on J02–J05.

~~~text
Integrate the approved domain, safety, provider, and agent modules into
GET /api/v1/scenarios, POST /api/v1/analyze, and
POST /api/v1/checkpoint-resolve. Analyze must sanitize first, block
prompt injection before provider calls, run the audit, and halt at
HALTED_AT_HUMAN_GATE. Resolve must validate session/owner/expiry, require
every claim decision and the pivot hypothesis, return HTTP 422 otherwise,
record human sign-off, and only then generate bilingual ADR/SDR, assumption
debt ledger, next five non-leading questions, and investor objection matrix.
Never expose raw PII or keys in logs. No model tool may call resolve. Add
full API lifecycle and bypass tests. Do not rewrite the modules you integrate.
Open a PR.
~~~

### J07 — Frontend shell and design system

Branch: feat/frontend-shell. Depends on J01.

~~~text
Build the Next.js/React/TypeScript/Tailwind frontend shell only. Create a
premium, precise dark interface: near-black base, restrained cyan telemetry,
clear typography/hierarchy, deliberate spacing, and accessible contrast.
Avoid generic AI-dashboard styling and decorative non-functional controls.
Create app layout/navigation, scenario and hypothesis surface, split-pane
evidence-review shell, human-gate status, claim-card states, telemetry/report
shell, and responsive/mobile behavior. Use isolated typed mock data only;
do not fake live metrics or provider status. Do not edit backend or shared
manifests. Add component/accessibility tests and screenshots. Open a PR.
~~~

### J08 — Human checkpoint frontend integration

Branch: feat/frontend-human-checkpoint. Depends on J06 and J07.

~~~text
Connect the frontend to the actual FastAPI schemas. Implement scenario
loading, analyze request, Extractor/Skeptic evidence cards, source lines,
Accept/Discard/Log Assumption Debt for every claim, founder notes, pivot
hypothesis, target wedge, sign-off, bilingual output, and telemetry/fallback
states. Backend is the source of truth; frontend state must never unlock
synthesis. Do not expose provider keys in browser code. Handle 422, expired
sessions, duplicate submissions, provider failures, and empty/error states.
Add tests for incomplete claims, empty pivot, keyboard accessibility, and
the successful full workflow. Do not change backend contracts. Open a PR.
~~~

### J09 — n8n workflow export

Branch: feat/n8n-workflow-export. Depends on J06.

~~~text
Create workflows/n8n-foundergate-workflow.json using the real API contract.
The workflow may submit sanitized analysis input and return the halted
human-gate result. It must never auto-approve claims or resolve the checkpoint
without explicit authorized human decisions. Do not hardcode credentials;
use n8n credential references/placeholders. Avoid logging raw transcript
content. Add import/configuration documentation and validate JSON and node
structure. Do not modify application code or API contracts. Open a PR.
~~~

### J10 — Integration, evaluation, and E2E

Branch: test/integration-and-e2e. Depends on J08 and J09.

~~~text
Build cross-stack tests and a synthetic evaluation corpus. Verify the complete
flow from scenario/input through safety, provider, Extractor/Skeptic,
HALTED_AT_HUMAN_GATE, human claim decisions, checkpoint resolution, and
bilingual outputs. Test PII absent from outbound payloads/logs, prompt
injection before inference, quote/line fidelity, unresolved claim HTTP 422,
invalid decisions, empty pivot, wrong-owner/expired/replayed sessions,
no model bypass, no pre-gate synthesis, provider timeout/429/malformed JSON,
and no-key sandbox. Add Playwright coverage for the complete UI workflow.
Do not rewrite production code to make tests pass; report defects to owners.
Use synthetic data only. Report actual results. Open a PR.
~~~

### J11 — Docker, CI, and repository security

Branch: chore/docker-ci-security. Depends on core app and test PRs.

~~~text
Add Dockerfiles and Docker Compose for frontend/backend, health checks,
non-root runtime users, pinned dependencies, safe environment handling, and
an optional n8n profile only if needed. Add GitHub Actions for backend tests,
frontend tests, lint, type checks, builds, and stable E2E checks. Add secret
scanning and appropriate dependency checks. Use least-privilege workflow
permissions and reviewed/pinned actions. Never copy .env into images; never
add deployment credentials. Validate Compose and CI. Do not change business
logic. Open a PR with evidence.
~~~

### J12 — Independent security audit

Branch: main, read-only. Depends on J10/J11.

~~~text
Act as an independent application security reviewer. Do not edit files.
Audit the actual implementation against SECURITY.md and the technical spec.
Try to break PII redaction, prompt-injection boundaries, quote provenance,
session ownership/expiry/replay, the mandatory human gate, post-gate synthesis,
assumption-debt isolation, provider fallback, secrets in browser/logs/workflows,
Docker and CI permissions, and accessibility/error handling. Report only
reproducible findings with Critical/High/Medium/Low severity, exact file/line,
attack or failure scenario, reproduction, impact, and remediation. Separate
confirmed vulnerabilities from concerns. End with a release recommendation.
~~~

### J13 — Remediation

Branch: fix/security-and-release-findings. Depends on human triage of J12.

~~~text
Fix only J12 findings explicitly accepted by the maintainer. Reproduce each
issue, add a regression test, make the smallest correction, run targeted and
full affected tests, and report residual risk. Do not broad-refactor, suppress
tests, or weaken controls. Reference finding IDs in commits and PRs. Open
focused PRs; do not merge.
~~~

### J14 — Release documentation

Branch: docs/release-readiness. Depends on J13 merged.

~~~text
Reconcile README and all docs against actual source, merged PRs, test evidence,
OpenAPI, Docker commands, n8n export, and deployed behavior. Preserve the
seven required top-level Project Story headings in README. Remove placeholders
and unsupported claims. Verify links and provider/model disclosures. Label
time/token benchmark estimates unless raw reproducible evidence exists.
Do not invent URLs, tests, team details, deployments, or challenge rules.
Produce a Verified/Not Verified/Not Applicable release-readiness matrix.
Docs-only PR. 
~~~

## Pull-request gates

Every Jules implementation session must submit one focused PR with:

- Problem and scope.
- Exact files changed.
- Design decisions and trade-offs.
- Commands run and actual test results.
- Security/privacy impact.
- Screenshots for material UI work.
- Remaining limitations.
- ADR reference when architecture/dependencies change.

Before merge: inspect the full diff, scan for secrets, verify required checks, ensure no unrelated changes, and require human approval. After merge, verify CI on the merge commit before starting dependent tasks from updated main.

## Definition of done

### Product
- Three synthetic scenarios work.
- Input safety checks precede external inference.
- Extractor/Skeptic interpretations are separate.
- Quotes and source lines are verified.
- Analysis halts at HALTED_AT_HUMAN_GATE.
- Every claim requires an explicit human decision.
- HTTP 422 for unresolved claims, invalid decisions, or missing pivot.
- No model can approve claims or invoke checkpoint resolution.
- No synthesis before human sign-off.
- Bilingual decision report, assumption ledger, five questions, and investor matrix generate after sign-off.

### Engineering
- Backend unit/integration tests pass.
- Frontend tests and build pass.
- Playwright end-to-end flow passes.
- Docker Compose starts from a clean checkout.
- CI is green on the final merge commit.
- Provider failure and fallback paths are tested.
- Sandbox works without API keys and identifies itself as deterministic.
- n8n export imports and preserves the human gate.

### Security and release
- PII does not appear in outbound payload tests or logs.
- Prompt-injection and untrusted-input tests pass.
- Session ownership, expiry, and replay behavior are tested.
- Secrets are absent from Git and browser bundles.
- Security review findings are fixed or formally risk-accepted.
- README/docs match implementation and evidence.
- Live demo and three-minute judge video are manually verified.

## Jules tracking ledger

| ID | Session | Branch | Jules session URL/ID | PR | Status |
|---|---|---|---|---|---|
| J00 | Repository audit | main (read-only) | — | — | Not started |
| J01 | Foundation | feat/jules-foundation | — | — | Blocked by J00 |
| J02 | Backend domain | feat/backend-domain-state | — | — | Blocked by J01 |
| J03 | Safety gate | feat/backend-safety-gate | — | — | Blocked by J01 |
| J04 | Provider router | feat/llm-router-sandbox | — | — | Blocked by J01 |
| J05 | Adversarial agents | feat/adversarial-agent-engine | — | — | Blocked by J02–J04 |
| J06 | API orchestration | feat/fastapi-orchestration | — | — | Blocked by J02–J05 |
| J07 | Frontend shell | feat/frontend-shell | — | — | Blocked by J01 |
| J08 | Checkpoint UI | feat/frontend-human-checkpoint | — | — | Blocked by J06/J07 |
| J09 | n8n export | feat/n8n-workflow-export | — | — | Blocked by J06 |
| J10 | Integration/E2E | test/integration-and-e2e | — | — | Blocked by J08/J09 |
| J11 | Docker/CI | chore/docker-ci-security | — | — | Blocked by app/tests |
| J12 | Security audit | main (read-only) | — | — | Blocked by J10/J11 |
| J13 | Remediation | fix/security-and-release-findings | — | — | Blocked by J12 |
| J14 | Release docs | docs/release-readiness | — | — | Blocked by J13 |

## Official Jules references

- Getting started: https://jules.google/docs/
- Running tasks: https://jules.google/docs/running-tasks/
- Environment setup and snapshots: https://jules.google/docs/environment/
- Plan review: https://jules.google/docs/review-plan/
- Code review and PR publishing: https://jules.google/docs/code/
- Plans and limits: https://jules.google/docs/usage-limits
- REST API sessions: https://jules.google/docs/api/reference/sessions

**Operating principle:** one session, one responsibility, one branch, one reviewable PR. Build in dependency order, parallelize only independent work, and let automated tests plus human review—not agent confidence—decide whether a change is ready.
