import pytest
from backend.agents.orchestrator import OrchestratorAgent
from backend.agents.task_agent import TaskAgent
from backend.agents.schedule_agent import ScheduleAgent


@pytest.mark.asyncio
async def test_orchestrator_process():
    """Test orchestrator workflow"""
    orchestrator = OrchestratorAgent()
    
    context = {"user_id": "test-user"}
    user_request = "Create a task called 'Design API' due next Friday, and schedule a meeting to discuss it on Thursday at 2pm"
    
    result = await orchestrator.process(user_request, context)
    
    assert result["status"] == "success"
    assert "workflow" in result
    assert "results" in result
    assert "final_response" in result


@pytest.mark.asyncio
async def test_task_agent():
    """Test task agent"""
    from unittest.mock import AsyncMock
    
    db_mock = AsyncMock()
    db_mock.create_task.return_value = "task_123"
    
    agent = TaskAgent(db_mock)
    result = await agent.process("Create task: Implement API endpoint", {})
    
    assert result["status"] == "created"
    assert "task_id" in result


@pytest.mark.asyncio
async def test_schedule_agent():
    """Test schedule agent"""
    from unittest.mock import AsyncMock
    
    db_mock = AsyncMock()
    calendar_mock = AsyncMock()
    calendar_mock.create_event.return_value = {"id": "event_123"}
    
    agent = ScheduleAgent(db_mock, calendar_mock)
    result = await agent.process("Schedule meeting tomorrow at 3pm", {})
    
    assert "event_id" in result or "status" in result
