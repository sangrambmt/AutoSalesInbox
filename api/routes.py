from fastapi import APIRouter, HTTPException

from api.models import ProcessEmailRequest, ProcessEmailResponse
from orchestrator.graph import email_graph

router = APIRouter(prefix="/api/v1", tags=["email-agent"])


@router.post("/process-email", response_model=ProcessEmailResponse)
async def process_email(request: ProcessEmailRequest) -> ProcessEmailResponse:
    initial_state = {
        "email_id": request.email_id,
        "user_id": request.user_id,
        "lead_id": request.lead_id,
        "email": {},
        "lead": {},
        "intent": "",
        "next_action": "",
        "compliance_approved": False,
        "draft_reply": None,
        "error": None,
        "actions_taken": [],
    }

    try:
        result = await email_graph.ainvoke(initial_state)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return ProcessEmailResponse(
        email_id=request.email_id,
        intent=result.get("intent", ""),
        next_action=result.get("next_action", ""),
        compliance_approved=result.get("compliance_approved", False),
        draft_reply=result.get("draft_reply"),
        actions_taken=result.get("actions_taken", []),
        error=result.get("error"),
    )


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
