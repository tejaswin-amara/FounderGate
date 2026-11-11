import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

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

    def resolve_checkpoint(self, owner_id: str, current_time: datetime.datetime, request: "CheckpointResolveRequest"):
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
    def validate_pivoted_hypothesis(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("pivoted_hypothesis cannot be blank")
        return v

    @field_validator("decisions")
    @classmethod
    def validate_decisions(cls, v: list[EvidenceClaim]) -> list[EvidenceClaim]:
        for decision in v:
            if decision.founder_decision is None:
                raise ValueError("All claims must have a founder_decision")
        return v

class CheckpointResolveResponse(BaseModel):
    status: SessionState
    telemetry: dict
    adr_report: str

@app.get("/api/v1/scenarios")
async def get_scenarios() -> list[str]:
    return [
        "b2b_invoice_ai",
        "edtech_campus_copilot",
        "greentech_packaging"
    ]

@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    return AnalyzeResponse(
        session_id="FG-EXAMPLE",
        status=SessionState.HALTED_AT_HUMAN_GATE,
        claims=[],
        telemetry={},
        audit_log=[]
    )

@app.post("/api/v1/checkpoint-resolve", response_model=CheckpointResolveResponse)
async def checkpoint_resolve(request: CheckpointResolveRequest):
    return CheckpointResolveResponse(
        status=SessionState.COMPLETED_HUMAN_VERIFIED,
        telemetry={},
        adr_report="# Strategic Decision Record"
    )
