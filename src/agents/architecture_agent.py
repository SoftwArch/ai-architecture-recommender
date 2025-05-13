# 架构匹配 Agent
from typing import Dict, Any
from llm_client import default_llm_client

class ArchitectureAgent:
    """
    Agent responsible for recommending software architectures based on requirements.
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client if llm_client else default_llm_client

    async def recommend(self, requirements_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommends software architecture styles based on the provided requirements analysis.

        Args:
            requirements_analysis: A dictionary containing the analyzed software requirements.

        Returns:
            A dictionary containing recommended architecture styles, a comparison matrix,
            a final recommendation, and the reasoning behind it.
        """
        return await self.llm_client.recommend_architecture(requirements_analysis)
