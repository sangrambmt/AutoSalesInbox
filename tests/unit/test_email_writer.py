from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_write_email_returns_draft(sample_state):
    sample_state["intent"] = "positive"
    sample_state["next_action"] = "reply"

    mock_response = MagicMock()
    mock_response.content = "Hi John, thanks for reaching out. Let's set up a call!"

    with patch("agents.email_writer.agent._llm") as mock_llm:
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)

        from agents.email_writer.agent import write_email_node
        result = await write_email_node(sample_state)

    assert result["draft_reply"] == "Hi John, thanks for reaching out. Let's set up a call!"


@pytest.mark.asyncio
async def test_write_email_strips_whitespace(sample_state):
    sample_state["intent"] = "neutral"
    sample_state["next_action"] = "reply"

    mock_response = MagicMock()
    mock_response.content = "  Hello there.  "

    with patch("agents.email_writer.agent._llm") as mock_llm:
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)

        from agents.email_writer.agent import write_email_node
        result = await write_email_node(sample_state)

    assert result["draft_reply"] == "Hello there."
