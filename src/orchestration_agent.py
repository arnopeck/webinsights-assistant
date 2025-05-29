"""
WebInsights Assistant - Orchestration Agent

This module implements the Orchestration Agent that coordinates the workflow
between all other agents in the WebInsights Assistant system.
"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import Field

from google.adk import Agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OrchestrationAgent")

class OrchestrationAgent(Agent):
    """
    Orchestration Agent that coordinates the workflow between all other agents.
    
    This agent:
    1. Receives user requests
    2. Coordinates the execution of other agents
    3. Manages the flow of data between agents
    4. Personalizes output based on user needs
    """
    
    # Define fields explicitly for Pydantic compatibility
    registered_agents: Dict[str, Agent] = Field(default_factory=dict)
    
    def __init__(self):
        """Initialize the Orchestration Agent."""
        super().__init__(name="OrchestrationAgent")
        logger.info("Orchestration Agent initialized")
    
    def register_agent(self, name: str, agent: Agent) -> None:
        """
        Register an agent with the Orchestration Agent.
        
        Args:
            name: Name of the agent
            agent: Instance of the agent
        """
        self.registered_agents[name] = agent
        logger.info(f"Agent '{name}' registered with Orchestration Agent")
    
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request in the agent's context.
        
        Args:
            state: Current state containing the request data
            
        Returns:
            Dict[str, Any]: Updated state with orchestration results
        """
        logger.info("Orchestration Agent processing request")
        
        # Extract request data
        request_data = state.get("request_data", {})
        
        # Log the request
        logger.info(f"Received request: {request_data}")
        
        # Add orchestration metadata to the state
        state["orchestration"] = {
            "workflow_id": "analytics_workflow",
            "start_time": state.get("timestamp", ""),
            "status": "in_progress"
        }
        
        logger.info("Orchestration Agent completed processing")
        return state


def create_orchestration_agent() -> OrchestrationAgent:
    """
    Create and configure an instance of the Orchestration Agent.
    
    Returns:
        OrchestrationAgent: Configured instance of the Orchestration Agent
    """
    agent = OrchestrationAgent()
    logger.info("Orchestration Agent created and configured")
    return agent
