from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_classify_positive(sample_state):
    sample_state["email"]["subject"] = "I want to buy"
    sample_state["email"]["body"]["content"] = "Please send me a quote."

    mock_response = MagicMock()
    mock_response.content = "positive"

    with patch("agents.intent_agent.agent._llm") as mock_llm:
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)

        from agents.intent_agent.agent import classify_intent_node
        result = await classify_intent_node(sample_state)

    assert result["intent"] == "positive"


@pytest.mark.asyncio
async def test_classify_negative(sample_state):
    mock_response = MagicMock()
    mock_response.content = "negative"

    with patch("agents.intent_agent.agent._llm") as mock_llm:
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)

        from agents.intent_agent.agent import classify_intent_node
        result = await classify_intent_node(sample_state)

    assert result["intent"] == "negative"


@pytest.mark.asyncio
async def test_invalid_llm_response_defaults_to_neutral(sample_state):
    # LLM returns something unexpected — should default to neutral
    mock_response = MagicMock()
    mock_response.content = "excited!!!"

    with patch("agents.intent_agent.agent._llm") as mock_llm:
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)

        from agents.intent_agent.agent import classify_intent_node
        result = await classify_intent_node(sample_state)

    assert result["intent"] == "neutral"


@pytest.mark.asyncio
async def test_classify_no_reply(sample_state):
    sample_state["email"]["subject"] = "Out of Office"
    sample_state["email"]["body"]["content"] = "I am out of office until Monday."

    mock_response = MagicMock()
    mock_response.content = "no_reply"

    with patch("agents.intent_agent.agent._llm") as mock_llm:
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)

        from agents.intent_agent.agent import classify_intent_node
        result = await classify_intent_node(sample_state)

    assert result["intent"] == "no_reply"
