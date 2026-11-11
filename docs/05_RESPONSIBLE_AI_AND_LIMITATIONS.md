# 05 — Responsible AI, Data Privacy, Bias, and Failure Modes

## 1. Responsible-use principle

FounderGate is a decision-support system. It can organize evidence and challenge interpretations, but it cannot establish product-market fit, certify market size, or make the founder's strategic choice.

The founder remains responsible for:
- Reviewing each source quote and its context.
- Deciding whether an observation is relevant.
- Distinguishing verified past behavior from weak intent.
- Choosing the target market and GTM wedge.
- Deciding which assumptions require further testing.

## 2. Data provenance and synthetic-data policy

### Synthetic scenarios

The project design specifies three built-in synthetic founder scenarios:

1. **B2B Invoice Recovery SaaS** — invoice follow-up and failed-payment recovery workflows.
2. **Student Alternance Copilot** — student placement and alternance discovery.
3. **D2C GreenTech Packaging** — packaging compliance and sustainable-material workflows.

Preloaded transcripts must be fictional and must not contain real or identifiable third-party personal data. Document the source and generation method for every fixture.

### Custom user data

Custom interview transcripts may contain personal, confidential, or commercially sensitive information. The application should:
- Warn users not to upload data they are not authorized to process.
- Minimize collection and retention.
- Redact supported identifiers before hosted model calls.
- Explain which provider receives data and under what plan/terms.
- Offer a local inference route for appropriate sensitive workflows.
- Provide deletion and retention controls consistent with the deployment's obligations.

## 3. Privacy safeguards and GDPR limitations

The planned sanitizer, `verify_and_sanitize_input()`, should detect and replace supported email, phone, and IBAN patterns using:

- `[REDACTED_EMAIL_GDPR]`
- `[REDACTED_PHONE_GDPR]`
- `[REDACTED_IBAN_GDPR]`

Regex-based detection can miss names, addresses, identifiers in unusual formats, indirect identifiers, and contextually identifying details. It may also redact non-personal strings by mistake.

**Do not claim GDPR compliance solely because the application performs regex redaction.** The controller/operator must assess lawful basis, notice and transparency, purpose limitation, minimization, retention, access controls, processor terms, international transfers, data-subject rights, incident response, and other applicable obligations.

## 4. Known limitations and failure modes

### 4.1 Irony, sarcasm, and cultural politeness

**Failure mode:** An interviewee may say “That's an interesting approach” as a polite rejection, or use dry irony that a lightweight model interprets literally.

**Mitigation:**
- Treat unquantified praise as a weak signal.
- Show the exact verbatim quote and surrounding context.
- Show both Extractor and Skeptic interpretations.
- Let the founder override any classification.
- Track uncertainty rather than presenting confidence scores as calibrated probabilities without evaluation.

### 4.2 Survivorship and selection bias

**Failure mode:** Interviews with friends, existing fans, or highly engaged early adopters may not represent cold prospects or the intended buying segment.

**Mitigation:**
- Record interview recruitment context where available.
- Flag sample-selection assumptions in the Assumption Debt Ledger.
- Generate non-leading questions for cold-prospect falsification.
- Avoid generalizing from a small interview sample to an entire market.

### 4.3 Hallucinated quotes and citations

**Failure mode:** A generative model may paraphrase a quote, invent a line number, or combine multiple statements.

**Mitigation:**
- Cross-check every quote against the source transcript.
- Verify source-line references programmatically where possible.
- Display the raw sanitized transcript next to the extracted quote.
- Reject claims whose quote cannot be located exactly.
- Do not let schema-valid JSON substitute for source verification.

### 4.4 Small-sample fallacy

**Failure mode:** Two interviews may demonstrate a problem for two people, but do not establish a large addressable market or repeatable willingness to pay.

**Mitigation:**
- Keep market-size claims in the Assumption Debt Ledger until independently researched.
- Record the sample size and participant context.
- Define falsification experiments and measurable thresholds.
- Do not label a market validated solely from interview sentiment.

### 4.5 Provider/model variability

**Failure mode:** Providers may change model versions, quotas, response formats, or availability. Different models may classify the same evidence differently.

**Mitigation:**
- Record provider/model identifiers and prompt versions.
- Validate structured output.
- Keep source evidence visible.
- Offer sandbox/local alternatives.
- Disclose when fallback behavior occurs.

### 4.6 Prompt injection and malicious content

**Failure mode:** A transcript or competitor review contains instructions intended to override the model's system behavior or the human checkpoint.

**Mitigation:**
- Treat all user-provided content as untrusted data.
- Separate trusted instructions from transcript text.
- Use pre-flight pattern checks and strict tool permissions.
- Never grant an LLM the ability to adjudicate claims or invoke checkpoint resolution.
- Test direct and indirect prompt-injection examples.

## 5. Human oversight and contestability

Every claim must be displayed with:
- Verbatim source quote.
- Source interview and line reference.
- Extractor interpretation.
- Skeptic challenge.
- Bias type and severity.
- Confidence estimate, clearly labeled as model-generated.
- Founder decision and optional rationale.

The founder must be able to accept, discard, or log assumption debt. The system must not hide disagreement or silently overwrite a human decision.

## 6. Synthetic evaluation policy

The evaluation set should include:
- Compliments and vague praise.
- Hypothetical future promises.
- Leading questions.
- Concrete past behavior and actual spending.
- Sarcasm and culturally polite rejection.
- Contradictory or incomplete evidence.
- Prompt-injection attempts embedded in otherwise plausible transcripts.
- English and French examples.
- Fabricated quote and line-reference traps.

Report false positives, false negatives, citation accuracy, and uncertainty behavior. Avoid optimizing only for the expected answer in the three demo scenarios.

## 7. Responsible-AI release checklist

- [ ] Synthetic fixtures are fictional and reviewed for accidental personal data.
- [ ] Custom-data warnings and provider disclosures are visible.
- [ ] Supported PII redaction is tested before outbound calls.
- [ ] Quote and line-reference verification is tested.
- [ ] Bias categories and uncertainty are explained in the UI.
- [ ] Human adjudication is mandatory and auditable.
- [ ] No model can approve its own evidence.
- [ ] Fallback and model limitations are disclosed.
- [ ] Data retention, deletion, and access policies are documented.
- [ ] Benchmark and market claims are scoped to the evidence available.
