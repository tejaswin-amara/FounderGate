# 04 — AI Disclosure Statement and Time-Saved Audit

## 1. Equal Access AI policy

FounderGate is designed to use free-tier hosted inference, local open-weight inference, or a built-in deterministic sandbox. “€0.00” refers to the intended model-inference charge when a free allowance or local execution is used; it does not mean all hosting, storage, networking, or operational costs are zero.

Provider plans, model identifiers, free quotas, and terms can change. Verify current eligibility and access before each submission or judging event.

## 2. Runtime provider and model ledger

| Provider / component | Model identifier | Plan / execution mode in project specification | Workflow role | Calls per run | Estimated tokens per run | Inference-cost target |
|---|---|---|---|---:|---:|---:|
| **Built-in Sandbox** | Deterministic Mom-Test Engine | Local deterministic logic | Default zero-key judge mode | 1 local pass | 0 external tokens | **€0.00** |
| **Google AI Studio** | `gemini-2.5-flash` | Free tier | Extractor + Skeptic + SDR synthesis | 2 calls | ~920 | **€0.00 within free limits** |
| **Mistral AI** | `mistral-small-latest` | Free experimentation plan, as stated in project notes | Extractor + Skeptic + SDR synthesis | 2 calls | ~910 | **€0.00 within free limits** |
| **Groq Cloud** | `llama-3.3-70b-versatile` | Free developer tier, subject to quota | Extractor + Skeptic + SDR synthesis | 2 calls | ~890 | **€0.00 within free limits** |
| **Ollama (local)** | `qwen2.5:7b` / `llama3.2` | Local inference | Offline/NDA-sensitive workflow option | 2 local calls | ~850 local tokens | **€0.00 provider inference cost** |
| **OpenRouter** | `meta-llama/llama-3.3-70b-instruct:free` | Free route, subject to availability | Extractor + Skeptic + SDR synthesis | 2 calls | ~920 | **€0.00 within free limits** |
| **Hugging Face** | `Qwen/Qwen2.5-72B-Instruct` | Free inference access, subject to current limits | Extractor + Skeptic + SDR synthesis | 2 calls | ~920 | **€0.00 within free limits** |

### Required disclosure fields for a real run

Where available, record:

- Provider and exact model identifier/version.
- Plan or execution mode.
- Request count and token usage.
- Input size and output size.
- Latency and retries.
- Fallback events and reason.
- Estimated inference charge and quota assumptions.
- Whether inference was local or sent to a third party.

Never record or publish API keys.

## 3. Frugality engineering and token targets

The proposed design batches the Extractor and Skeptic into one structured JSON request, rather than using a long multi-turn conversation. A separate synthesis request runs only after the human gate.

The project estimate is approximately 850–920 tokens per full sprint depending on provider and scenario. This is a target estimate, not a provider-independent guarantee. Actual usage depends on transcript length, output length, model tokenizer, prompt version, and retry behavior.

The supplied notes state an 84% reduction in one comparison and approximately 920 tokens versus more than 15,000 tokens in another. These are different baselines:

- 920 versus 15,000 is approximately **93.9% fewer tokens**.
- An **84%** reduction would require a different baseline and must be accompanied by that baseline.

Do not publish a single reduction percentage without recording its comparison method.

## 4. Time-saved methodology

The project planning notes describe a manual baseline as a function of transcript word count \(W\):

\[
T_{\text{manual}} =
\max\left(75,\left\lfloor\frac{W}{120}\times18+65\right\rfloor\right)
\]

The notes also identify claim count \(C\) as a tracked variable. The formula above does not currently use \(C\); either keep it as a separately reported workload measure or revise the model using a benchmarked relationship.

Net time saved is defined as:

\[
T_{\text{saved}} = T_{\text{manual}} - T_{\text{assisted}}
\]

For the supplied scenario estimates, assisted time includes the focused human checkpoint and is approximately 4–5 minutes. Machine processing time alone is not a fair comparison because the founder still has to review and decide.

### Reported workflow breakdown

| Workflow sub-task | Manual baseline | FounderGate + human checkpoint | Reported net saved |
|---|---:|---:|---:|
| GDPR PII scrubbing and quote tagging | ~30 min | ~0.2 sec | ~29.8 min |
| Mom-Test confirmation-bias audit | ~25 min | ~2.5 sec | ~24.9 min |
| Contradiction resolution and pivot formulation | ~20 min | ~3.5 min | ~16.5 min |
| ADR/SDR, ledger, and next five questions | ~20 min | ~1.0 sec | ~19.9 min |
| **Total per sprint** | **95 min** | **~5 min** | **~90 min (94.7%)** |

The component estimates are rounded. The total should be recomputed from raw timestamps for each run instead of summing rounded task-level figures.

### Three-scenario benchmark supplied by the project

| Scenario | Manual baseline | Assisted time | Net time saved | Reduction |
|---|---:|---:|---:|---:|
| A — B2B Invoice Recovery SaaS | 95 min | 5 min | 90 min | 94.7% |
| B — Student Alternance Copilot | 88 min | 4.5 min | 83.5 min | 94.9% |
| C — D2C Packaging Compliance Auditor | 85 min | 4 min | 81 min | 95.3% |

At two sprints per week for four weeks, the first scenario's 90-minute saving yields a projected **12 hours** over eight sprints. This is an extrapolation, not a separately measured four-week field study.

## 5. Reproducible benchmarking protocol

For every benchmark run, store:

1. Scenario identifier and dataset version.
2. Transcript word count and interview count.
3. Number of extracted claims.
4. Manual baseline method and measured manual duration.
5. Automated processing start/end timestamps.
6. Human checkpoint start/end timestamps.
7. Provider, model, prompt version, calls, tokens, and retries.
8. Number of quotes whose source lines were verified.
9. Errors, fallback events, and incomplete outputs.
10. Final time-saved calculation.

Use the same task definition and evidence set for manual and assisted workflows. Report median and range across repeated trials where possible. Keep benchmark transcripts synthetic or appropriately authorized.

## 6. AI-assisted development and open-source disclosure

**AI-assisted coding:** Cursor and Google Gemini were used to assist with TypeScript/FastAPI boilerplate and French translation phrasing. The project notes state that agent prompts, Mom-Test rubrics, lifecycle gate logic, and PII-redaction rules were human-designed and verified.

**Declared frameworks and references:**

- FastAPI, Pydantic, Next.js, and Tailwind CSS are standard upstream dependencies.
- `affaan-m/ecc` (Everything Claude Code, MIT as identified in project notes) informed adversarial evaluator/generator and discovery-document patterns.
- `engineering-pipeline` v3.1.0 (MIT as identified in project notes) informed safety checks, hard lifecycle gates, debt tracking, and ADR structure.
- `DietrichGebert/ponytail` (MIT as identified in project notes) informed debt and gain/audit telemetry concepts.
- `multica-ai/andrej-karpathy-skills` (MIT as identified in project notes) informed explicit, minimalist state-machine practices.

Verify current upstream licenses and preserve required notices before distribution. Inspired patterns do not imply endorsement by the upstream authors.

## 7. Equal Access and responsible disclosure checklist

- [ ] No paid-only model is required for the judge path.
- [ ] The zero-key sandbox is clearly identified as deterministic.
- [ ] Local inference is clearly distinguished from hosted inference.
- [ ] Current free-tier quotas and provider terms are checked.
- [ ] Provider and model identifiers are visible to users.
- [ ] Token counts and cost estimates are labeled as estimates where appropriate.
- [ ] Fallbacks are disclosed rather than hidden.
- [ ] No API keys or private data appear in logs or reports.
- [ ] Benchmark claims have scripts, raw timings, and a defined baseline.
