from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

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
    founder_decision: FounderDecision | None = None
    founder_note: str | None = None

class SessionState(str, Enum):
    IDLE = "IDLE"
    SAFETY_GATE = "SAFETY_GATE"
    ADVERSARIAL_ANALYSIS = "ADVERSARIAL_ANALYSIS"
    HALTED_AT_HUMAN_GATE = "HALTED_AT_HUMAN_GATE"
    COMPLETED_HUMAN_VERIFIED = "COMPLETED_HUMAN_VERIFIED"

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
