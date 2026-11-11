import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

from app.safety_gate import verify_and_sanitize_input

app = FastAPI(title="FounderGate API", version="0.1.0")


class FounderDecision(str, Enum):
    ACCEPT_VERIFIED = "ACCEPT_VERIFIED"
    DISCARD_BIASED = "DISCARD_BIASED"
    LOG_ASSUMPTION_DEBT = "LOG_ASSUMPTION_DEBT"


class EvidenceClaim(BaseModel):
    id: str
    quote: str
    source_interview: str
    source_line: str | int
    extractor_reading: str
    skeptic_challenge: str
    bias_type: str
    severity: str
    confidence_score: float
    context_needed: str | None = None
    founder_decision: FounderDecision | None = None
    founder_note: str | None = None


class SessionState(str, Enum):
    IDLE = "IDLE"
    SAFETY_GATE = "SAFETY_GATE"
    ADVERSARIAL_ANALYSIS = "ADVERSARIAL_ANALYSIS"
    HALTED_AT_HUMAN_GATE = "HALTED_AT_HUMAN_GATE"
    COMPLETED_HUMAN_VERIFIED = "COMPLETED_HUMAN_VERIFIED"


class Session(BaseModel):
    id: str
    owner_id: str
    status: SessionState
    expires_at: datetime.datetime

    def resolve_checkpoint(
        self,
        owner_id: str,
        current_time: datetime.datetime,
        request: "CheckpointResolveRequest",
    ) -> None:
        if self.owner_id != owner_id:
            raise ValueError("Unauthorized owner")
        if current_time > self.expires_at:
            raise ValueError("Session expired")
        if self.status != SessionState.HALTED_AT_HUMAN_GATE:
            raise ValueError("Invalid session state transition")

        self.status = SessionState.COMPLETED_HUMAN_VERIFIED


class AnalyzeRequest(BaseModel):
    scenario_key: str | None = None
    hypothesis: str
    competitor_context: str | None = None
    raw_evidence: str | None = None
    provider: str
    api_key: str | None = None


class AnalyzeResponse(BaseModel):
    session_id: str
    status: SessionState
    claims: list[EvidenceClaim]
    telemetry: dict
    audit_log: list


class CheckpointResolveRequest(BaseModel):
    session_id: str
    decisions: list[EvidenceClaim]
    pivoted_hypothesis: str
    target_wedge: str | None = None
    language: str = "bilingual"

    @field_validator("pivoted_hypothesis")
    @classmethod
    def validate_pivoted_hypothesis(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("pivoted_hypothesis cannot be blank")
        return value

    @field_validator("decisions")
    @classmethod
    def validate_decisions(
        cls, decisions: list[EvidenceClaim]
    ) -> list[EvidenceClaim]:
        for decision in decisions:
            if decision.founder_decision is None:
                raise ValueError("All claims must have a founder_decision")
        return decisions


class CheckpointResolveResponse(BaseModel):
    status: SessionState
    telemetry: dict
    adr_report: str


@app.get("/api/v1/scenarios")
async def get_scenarios() -> list[str]:
    return [
        "b2b_invoice_ai",
        "edtech_campus_copilot",
        "greentech_packaging",
    ]


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    # Sanitize inputs before any model requests.
    safe_hypothesis = verify_and_sanitize_input(request.hypothesis)

    safe_competitor_context = None
    if request.competitor_context:
        safe_competitor_context = verify_and_sanitize_input(
            request.competitor_context
        )

    safe_raw_evidence = None
    if request.raw_evidence:
        safe_raw_evidence = verify_and_sanitize_input(request.raw_evidence)

    audit_log = []

    # Reject prompt injection without storing the raw input in logs.
    if (
        safe_hypothesis == "[PROMPT_INJECTION_DETECTED]"
        or safe_competitor_context == "[PROMPT_INJECTION_DETECTED]"
        or safe_raw_evidence == "[PROMPT_INJECTION_DETECTED]"
    ):
        audit_log.append(
            {
                "event": "SAFETY_GATE_REJECTED",
                "reason": "prompt_injection",
            }
        )
        return AnalyzeResponse(
            session_id="FG-EXAMPLE",
            status=SessionState.SAFETY_GATE,
            claims=[],
            telemetry={},
            audit_log=audit_log,
        )

    audit_log.append(
        {
            "event": "SAFETY_GATE_PASSED",
            "details": "Input sanitized for PII",
        }
    )

    return AnalyzeResponse(
        session_id="FG-EXAMPLE",
        status=SessionState.HALTED_AT_HUMAN_GATE,
        claims=[],
        telemetry={},
        audit_log=audit_log,
    )


@app.post(
    "/api/v1/checkpoint-resolve",
    response_model=CheckpointResolveResponse,
)
async def checkpoint_resolve(request: CheckpointResolveRequest):
    return CheckpointResolveResponse(
        status=SessionState.COMPLETED_HUMAN_VERIFIED,
        telemetry={},
        adr_report="# Strategic Decision Record",
    )
