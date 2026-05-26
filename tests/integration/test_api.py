from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_email_success():
    mock_result = {
        "email_id": "msg-001",
        "intent": "positive",
        "next_action": "reply",
        "compliance_approved": True,
        "draft_reply": "Hi John, happy to help!",
        "actions_taken": ["email_sent", "crm_logged"],
        "error": None,
    }

    with patch("api.routes.email_graph") as mock_graph:
        mock_graph.ainvoke = AsyncMock(return_value=mock_result)

        response = client.post("/api/v1/process-email", json={
            "email_id": "msg-001",
            "user_id": "user@company.com",
            "lead_id": "lead-123",
        })

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "positive"
    assert data["next_action"] == "reply"
    assert data["compliance_approved"] is True
    assert "email_sent" in data["actions_taken"]


def test_process_email_no_action_for_negative_intent():
    mock_result = {
        "email_id": "msg-002",
        "intent": "negative",
        "next_action": "no_action",
        "compliance_approved": False,
        "draft_reply": None,
        "actions_taken": [],
        "error": None,
    }

    with patch("api.routes.email_graph") as mock_graph:
        mock_graph.ainvoke = AsyncMock(return_value=mock_result)

        response = client.post("/api/v1/process-email", json={
            "email_id": "msg-002",
            "user_id": "user@company.com",
            "lead_id": "lead-456",
        })

    assert response.status_code == 200
    data = response.json()
    assert data["next_action"] == "no_action"
    assert data["draft_reply"] is None


def test_process_email_missing_fields_returns_422():
    response = client.post("/api/v1/process-email", json={"email_id": "msg-001"})
    assert response.status_code == 422


def test_process_email_graph_error_returns_500():
    with patch("api.routes.email_graph") as mock_graph:
        mock_graph.ainvoke = AsyncMock(side_effect=Exception("Graph error"))

        response = client.post("/api/v1/process-email", json={
            "email_id": "msg-001",
            "user_id": "user@company.com",
            "lead_id": "lead-123",
        })

    assert response.status_code == 500
