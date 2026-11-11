# 03 — Architecture Decision Records (ADR Log)

This log records architectural decisions and trade-offs. ADRs should be updated when superseded; do not silently rewrite history.

> **Date status:** The planning material schedules initial ADR review for November 16, 2026. As of November 11, 2026, that date is in the future. These records are therefore marked **Proposed**, not retrospectively marked Accepted. Update status and decision date only after the team has reviewed and approved each decision.

## ADR-001: Enforce a hard HTTP 422 lifecycle gate for human checkpoint resolution

- **Status:** Proposed — scheduled for review on 2026-11-16.
- **Date proposed:** 2026-11-11.
- **Decision owners:** Backend/Safety Lead and project maintainers.

### Context

FounderGate's differentiating requirement is that AI must not make the founder's strategic decision. A soft checkpoint—where the model generates the final strategy and merely asks a human to edit it afterward—does not satisfy this requirement.

### Proposed decision

Split analysis and human resolution into separate API operations:

- `/api/v1/analyze` performs safety checks and adversarial analysis, then ends in `HALTED_AT_HUMAN_GATE`.
- `/api/v1/checkpoint-resolve` requires an authorized human to submit a decision for every claim and a non-empty pivoted hypothesis.

Return **HTTP 422 Unprocessable Entity** if any claim lacks a valid `founder_decision`, the decision enum is invalid, or the pivoted hypothesis is missing.

### Consequences

**Positive**

- Makes human adjudication a server-side lifecycle requirement.
- Prevents post-gate synthesis from being unlocked by a frontend-only state change.
- Creates a clear testable acceptance criterion.

**Negative / trade-offs**

- Requires stateful session tracking and expiry behavior.
- Requires authentication/authorization or an equivalent trusted actor boundary.
- Adds a deliberate step before GTM synthesis.

### Verification required

- Test unresolved claim rejection.
- Test invalid decision rejection.
- Test empty pivot rejection.
- Test unknown, expired, and wrong-owner session rejection.
- Prove that model output cannot call the resolution endpoint.

---

## ADR-002: Use a single-pass batched JSON audit instead of a multi-turn agent conversation

- **Status:** Proposed — scheduled for review on 2026-11-16.
- **Date proposed:** 2026-11-11.
- **Decision owners:** Prompt/Evaluation Lead and Backend Lead.

### Context

Hosted free tiers can impose request-per-minute and token-per-minute limits. A long sequence of Extractor/Skeptic back-and-forth calls increases latency, cost uncertainty, and the chance of rate limiting.

### Proposed decision

Batch the Extractor and Mom-Test Skeptic roles into one structured JSON generation request where the provider supports it. Preserve their separate role instructions and separate output fields. Run GTM synthesis only after human checkpoint resolution.

### Consequences

**Positive**

- Reduces round trips and can reduce token usage.
- Makes the output easier to validate against a schema.
- Improves the chance of completing a judge demo within free-tier limits.

**Negative / trade-offs**

- The model must maintain two distinct perspectives within one completion.
- Very long transcripts may exceed context or output limits.
- Structured output must still be checked against the source; valid JSON can contain fabricated claims.

### Token and percentage accounting

The project notes contain two percentage/baseline statements: an initial **84% reduction** target and an approximate comparison of **920 tokens versus more than 15,000 tokens**. The latter arithmetic is approximately **93.9% fewer tokens**. These should not be conflated. Publish the exact baseline, prompt versions, transcript sizes, provider, and measured token counts before making a verified percentage claim.

### Verification required

- Compare batched and multi-turn outputs on a fixed evaluation corpus.
- Measure token usage and latency by provider.
- Validate schema compliance and quote/line fidelity.
- Test long input, truncation, and provider rate-limit behavior.

---

## ADR-003: Provide a deterministic zero-key sandbox for judge reliability

- **Status:** Proposed — scheduled for review on 2026-11-16.
- **Date proposed:** 2026-11-11.
- **Decision owners:** Backend Lead and Demo Lead.

### Context

Judges may not want to create or paste API keys to test a submission. Hosted free tiers may also be unavailable, rate-limited, or changed by providers.

### Proposed decision

Provide a `sandbox_zero_key` execution mode backed by deterministic, pre-authored Mom-Test evaluations for the three synthetic scenarios. Allow users to select hosted providers or local Ollama when configured.

### Consequences

**Positive**

- Enables a no-key demo path.
- Makes judge scenarios reproducible.
- Reduces dependence on external provider availability during a presentation.

**Negative / trade-offs**

- Deterministic sandbox output does not demonstrate live LLM reasoning.
- Scenario fixtures must be clearly labeled as pre-authored.
- A fallback must be observable; it must not pretend that a live provider executed.

### Verification required

- Confirm sandbox operation without credentials or network access.
- Test deterministic outputs for all three scenarios.
- Display the active provider/mode clearly.
- Test timeout, HTTP 429, and malformed-response fallback behavior.
- Never claim 100% uptime without operational evidence.

---

## Decision record template

Use this template for future entries:

~~~markdown
## ADR-NNN: Short decision title

- **Status:** Proposed | Accepted | Superseded | Rejected
- **Date proposed:**
- **Date decided:**
- **Decision owners:**

### Context

### Decision

### Alternatives considered

### Consequences

### Verification required

### References
~~~
