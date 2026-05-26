import pytest


@pytest.fixture
def sample_state() -> dict:
    return {
        "email_id": "msg-001",
        "user_id": "user@example.com",
        "lead_id": "lead-123",
        "email": {
            "subject": "Interested in your product",
            "body": {"content": "Hi, I'd like to learn more about your solution."},
            "from": {"emailAddress": {"address": "lead@company.com", "name": "John Doe"}},
        },
        "lead": {
            "leadqualitycode": 1,
            "donotbulkemail": False,
            "donotemail": False,
            "emails_this_week": 0,
            "description": "Interested in Product A",
        },
        "intent": "",
        "next_action": "",
        "compliance_approved": False,
        "draft_reply": None,
        "error": None,
        "actions_taken": [],
    }


@pytest.fixture
def opted_out_lead() -> dict:
    return {"donotbulkemail": True, "donotemail": False, "emails_this_week": 0}


@pytest.fixture
def hot_lead() -> dict:
    return {"leadqualitycode": 1, "donotbulkemail": False, "donotemail": False, "emails_this_week": 0}


@pytest.fixture
def cold_lead() -> dict:
    return {"leadqualitycode": 3, "donotbulkemail": False, "donotemail": False, "emails_this_week": 0}
