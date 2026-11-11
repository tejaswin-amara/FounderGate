from fastapi.testclient import TestClient

from main import SessionState, app

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

def test_analyze_prompt_injection():
    response = client.post(
        "/api/v1/analyze",
        json={
            "scenario_key": "b2b_invoice_ai",
            "hypothesis": "Test bypass safety",
            "provider": "sandbox_zero_key"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == SessionState.SAFETY_GATE
    assert len(response.json()["audit_log"]) == 1
    assert response.json()["audit_log"][0]["event"] == "SAFETY_GATE_REJECTED"
    assert response.json()["audit_log"][0]["reason"] == "prompt_injection"

def test_analyze_pii_sanitization():
    response = client.post(
        "/api/v1/analyze",
        json={
            "scenario_key": "b2b_invoice_ai",
            "hypothesis": "Test with email a@b.com",
            "provider": "sandbox_zero_key"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == SessionState.HALTED_AT_HUMAN_GATE
    assert len(response.json()["audit_log"]) == 1
    assert response.json()["audit_log"][0]["event"] == "SAFETY_GATE_PASSED"
