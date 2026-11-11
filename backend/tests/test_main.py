import datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import (
    CheckpointResolveRequest,
    EvidenceClaim,
    Session,
    SessionState,
    app,
)

client = TestClient(app)

def test_get_scenarios():
    response = client.get("/api/v1/scenarios")
    assert response.status_code == 200
    assert "b2b_invoice_ai" in response.json()

def test_analyze():
    response = client.post(
        "/api/v1/analyze",
        json={
            "scenario_key": "b2b_invoice_ai",
            "hypothesis": "Test",
            "provider": "sandbox_zero_key"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == SessionState.HALTED_AT_HUMAN_GATE

def test_checkpoint_resolve():
    response = client.post(
        "/api/v1/checkpoint-resolve",
        json={
            "session_id": "FG-EXAMPLE",
            "decisions": [],
            "pivoted_hypothesis": "Test Pivot"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == SessionState.COMPLETED_HUMAN_VERIFIED

def test_checkpoint_resolve_request_blank_hypothesis():
    with pytest.raises(ValidationError, match="pivoted_hypothesis cannot be blank"):
        CheckpointResolveRequest(
            session_id="FG-EXAMPLE",
            decisions=[],
            pivoted_hypothesis="   \t \n  "
        )

def test_checkpoint_resolve_request_missing_decision():
    with pytest.raises(ValidationError, match="All claims must have a founder_decision"):
        CheckpointResolveRequest(
            session_id="FG-EXAMPLE",
            decisions=[
                EvidenceClaim(
                    id="CLM-01",
                    quote="quote",
                    source_interview="int-01",
                    source_line=1,
                    extractor_reading="reading",
                    skeptic_challenge="challenge",
                    bias_type="COMPLIMENT_FLUFF",
                    severity="LOW",
                    confidence_score=0.9,
                    founder_decision=None
                )
            ],
            pivoted_hypothesis="Valid hypothesis"
        )

def test_session_resolve_checkpoint_success():
    session = Session(
        id="sess-01",
        owner_id="owner-01",
        status=SessionState.HALTED_AT_HUMAN_GATE,
        expires_at=datetime.datetime(2050, 1, 1, tzinfo=datetime.UTC)
    )
    request = CheckpointResolveRequest(
        session_id="sess-01",
        decisions=[],
        pivoted_hypothesis="Valid hypothesis"
    )
    session.resolve_checkpoint(
        owner_id="owner-01",
        current_time=datetime.datetime(2023, 1, 1, tzinfo=datetime.UTC),
        request=request
    )
    assert session.status == SessionState.COMPLETED_HUMAN_VERIFIED

def test_session_resolve_checkpoint_unauthorized():
    session = Session(
        id="sess-01",
        owner_id="owner-01",
        status=SessionState.HALTED_AT_HUMAN_GATE,
        expires_at=datetime.datetime(2050, 1, 1, tzinfo=datetime.UTC)
    )
    request = CheckpointResolveRequest(
        session_id="sess-01",
        decisions=[],
        pivoted_hypothesis="Valid hypothesis"
    )
    with pytest.raises(ValueError, match="Unauthorized owner"):
        session.resolve_checkpoint(
            owner_id="owner-02",
            current_time=datetime.datetime(2023, 1, 1, tzinfo=datetime.UTC),
            request=request
        )

def test_session_resolve_checkpoint_expired():
    session = Session(
        id="sess-01",
        owner_id="owner-01",
        status=SessionState.HALTED_AT_HUMAN_GATE,
        expires_at=datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC)
    )
    request = CheckpointResolveRequest(
        session_id="sess-01",
        decisions=[],
        pivoted_hypothesis="Valid hypothesis"
    )
    with pytest.raises(ValueError, match="Session expired"):
        session.resolve_checkpoint(
            owner_id="owner-01",
            current_time=datetime.datetime(2023, 1, 1, tzinfo=datetime.UTC),
            request=request
        )

def test_session_resolve_checkpoint_invalid_state():
    session = Session(
        id="sess-01",
        owner_id="owner-01",
        status=SessionState.IDLE,
        expires_at=datetime.datetime(2050, 1, 1, tzinfo=datetime.UTC)
    )
    request = CheckpointResolveRequest(
        session_id="sess-01",
        decisions=[],
        pivoted_hypothesis="Valid hypothesis"
    )
    with pytest.raises(ValueError, match="Invalid session state transition"):
        session.resolve_checkpoint(
            owner_id="owner-01",
            current_time=datetime.datetime(2023, 1, 1, tzinfo=datetime.UTC),
            request=request
        )
