import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcpapp.agent.agent import BedrockAgent
from mcpapp.agent.message import AssistantMessage


@pytest.fixture
def agent():
    mcp_session = AsyncMock()
    llm_client = MagicMock()
    agent = BedrockAgent(mcp_session, llm_client)
    # Mock the tool config
    agent._tool_config = MagicMock()
    agent._tool_config.dump_to_converse_dict.return_value = {"tools": []}
    return agent


@pytest.mark.asyncio
@patch("mcpapp.agent.agent.AssistantMessage")
async def test_multiple_tool_results_preserved(mock_assistant_message, agent):
    # Setup mock responses for multiple tool uses
    first_assistant_msg = MagicMock(spec=AssistantMessage)
    first_assistant_msg.contents = [
        {"toolUse": {"name": "tool1", "toolUseId": "id1", "input": {}}}
    ]
    first_assistant_msg.find_tool_uses.return_value = [
        {"name": "tool1", "toolUseId": "id1", "input": {}}
    ]

    second_assistant_msg = MagicMock(spec=AssistantMessage)
    second_assistant_msg.contents = [{"text": "Final response"}]

    # Setup mock responses for converse API
    agent.llm_client.converse.side_effect = [
        {
            "output": {"message": {"role": "assistant", "content": []}},
            "stopReason": "tool_use",
        },
        {
            "output": {
                "message": {
                    "role": "assistant",
                    "content": [{"text": "Final response"}],
                }
            },
            "stopReason": "end_turn",
        },
    ]

    # Setup mock for _call_bedrock_converse
    mock_assistant_message.side_effect = [first_assistant_msg, second_assistant_msg]

    # Setup mock for _acall_tool
    agent._acall_tool = AsyncMock()
    agent._acall_tool.return_value = {
        "toolUseId": "id1",
        "content": [{"text": "Tool result"}],
    }

    # Call ainvoke
    results = []
    async for action in agent.ainvoke("test query"):
        results.append(action)

    # Verify that multiple tool results are preserved in history
    # The second call should include the original user message and all tool results
    calls = agent.llm_client.converse.call_args_list
    assert len(calls) == 2

    # First call should have only the user message
    first_call_messages = calls[0][1]["messages"]
    assert len(first_call_messages) == 1
    assert first_call_messages[0]["role"] == "user"

    # Second call should have the user message, assistant and tool result messages
    second_call_messages = calls[1][1]["messages"]
    assert len(second_call_messages) == 3  # user + assistant + tool result
    assert second_call_messages[0]["role"] == "user"  # Original user message
    assert second_call_messages[1]["role"] == "assistant"  # Assistant message
    assert second_call_messages[2]["role"] == "user"  # Tool result message


@pytest.mark.asyncio
@patch("mcpapp.agent.agent.AssistantMessage")
async def test_multiple_tools_in_single_response(mock_assistant_message, agent):
    # Setup mock response with multiple tool uses in a single response
    assistant_msg = MagicMock(spec=AssistantMessage)
    assistant_msg.contents = [
        {"toolUse": {"name": "tool1", "toolUseId": "id1", "input": {}}},
        {"toolUse": {"name": "tool2", "toolUseId": "id2", "input": {}}},
    ]
    assistant_msg.find_tool_uses.return_value = [
        {"name": "tool1", "toolUseId": "id1", "input": {}},
        {"name": "tool2", "toolUseId": "id2", "input": {}},
    ]

    final_msg = MagicMock(spec=AssistantMessage)
    final_msg.contents = [{"text": "Final response"}]

    # Setup mock responses for converse API
    agent.llm_client.converse.side_effect = [
        {
            "output": {"message": {"role": "assistant", "content": []}},
            "stopReason": "tool_use",
        },
        {
            "output": {
                "message": {
                    "role": "assistant",
                    "content": [{"text": "Final response"}],
                }
            },
            "stopReason": "end_turn",
        },
    ]

    # Setup mock for _call_bedrock_converse
    mock_assistant_message.side_effect = [assistant_msg, final_msg]

    # Setup mock for _acall_tool
    agent._acall_tool = AsyncMock()
    agent._acall_tool.side_effect = [
        {"toolUseId": "id1", "content": [{"text": "Tool 1 result"}]},
        {"toolUseId": "id2", "content": [{"text": "Tool 2 result"}]},
    ]

    # Call ainvoke
    results = []
    async for action in agent.ainvoke("test query with multiple tools"):
        results.append(action)

    # Verify that both tool results are preserved in history
    calls = agent.llm_client.converse.call_args_list
    assert len(calls) == 2

    # First call should have only the user message
    first_call_messages = calls[0][1]["messages"]
    assert len(first_call_messages) == 1
    assert first_call_messages[0]["role"] == "user"

    # Second call should have user message, assistant and both tool results
    second_call_messages = calls[1][1]["messages"]
    assert len(second_call_messages) == 4  # user + assistant + 2 tool results
    assert second_call_messages[0]["role"] == "user"  # Original user message
    assert second_call_messages[1]["role"] == "assistant"  # Assistant message
    assert second_call_messages[2]["role"] == "user"  # First tool result
    assert second_call_messages[3]["role"] == "user"  # Second tool result

    # Verify that we got 3 actions (2 tool uses + 1 text response)
    assert len(results) == 3