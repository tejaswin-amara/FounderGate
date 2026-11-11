from fastapi.testclient import TestClient
from main import app, SessionState

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
