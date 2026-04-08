from typing import Dict, Any, List
from .base_agent import BaseAgent
import json
import re


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Orchestrator", model="claude-3-5-sonnet-20241022")
        self.available_agents = {}
        self.execution_log = []
    
    def register_agent(self, agent_name: str, agent):
        """Register sub-agent"""
        self.available_agents[agent_name] = agent
    
    async def process(self, user_request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate multi-step workflows
        1. Parse user intent
        2. Plan workflow steps
        3. Execute through appropriate agents
        4. Synthesize results
        """
        
        # Step 1: Analyze user intent
        analysis_prompt = f"""
        Analyze this user request and determine:
        1. Main objective
        2. Required tools (calendar, tasks, notes)
        3. Sub-tasks needed
        4. Order of execution
        
        Request: {user_request}
        
        Respond in JSON format:
        {{
            "objective": "...",
            "required_agents": ["task_agent", "schedule_agent", ...],
            "subtasks": ["...", "..."],
            "order": 1, 2, 3, ...
        }}
        """
        
        analysis = await self.think(analysis_prompt)
        workflow = self._parse_json(analysis)
        self.execution_log.append({"stage": "analysis", "result": workflow})
        
        # Step 2: Execute workflow through appropriate agents
        results = {}
        for agent_name in workflow.get("required_agents", []):
            if agent_name in self.available_agents:
                agent = self.available_agents[agent_name]
                task = self._get_agent_task(agent_name, workflow)
                results[agent_name] = await agent.process(task, context)
                self.execution_log.append({
                    "stage": "execution",
                    "agent": agent_name,
                    "result": results[agent_name]
                })
        
        # Step 3: Synthesize final response
        synthesis_prompt = f"""
        Synthesize these results into a final user-friendly summary:
        
        Original request: {user_request}
        Workflow plan: {workflow}
        Execution results: {json.dumps(results, indent=2, default=str)}
        
        Provide a clear summary of what was accomplished.
        """
        
        final_response = await self.think(synthesis_prompt)
        
        return {
            "status": "success",
            "user_request": user_request,
            "workflow": workflow,
            "results": results,
            "final_response": final_response,
            "execution_log": self.execution_log
        }
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text response"""
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        return {"required_agents": [], "subtasks": []}
    
    def _get_agent_task(self, agent_name: str, workflow: Dict[str, Any]) -> str:
        """Extract specific task for agent from workflow"""
        if agent_name == "task_agent":
            return f"Handle task-related subtasks from: {workflow.get('subtasks', [])}"
        elif agent_name == "schedule_agent":
            return f"Handle scheduling subtasks from: {workflow.get('subtasks', [])}"
        else:
            return str(workflow.get('subtasks', []))
