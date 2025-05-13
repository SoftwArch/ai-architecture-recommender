# 需求解析 Agent
from typing import Dict, Any
from llm_client import default_llm_client

class RequirementAgent:
    """
    Agent responsible for analyzing software requirements.
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client if llm_client else default_llm_client

    async def analyze(self, description: str) -> Dict[str, Any]:
        """
        Analyzes the software requirement description using the LLM.

        Args:
            description: The textual description of the software requirements.

        Returns:
            A dictionary containing the analysis of the requirements,
            including key features, non-functional requirements, constraints,
            and an analysis summary.
        """
        return await self.llm_client.analyze_requirements(description)