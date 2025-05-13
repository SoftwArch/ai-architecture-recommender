# 评估生成 Agent
from typing import Dict, Any
from llm_client import default_llm_client

class EvaluationAgent:
    """
    Agent responsible for evaluating a given software architecture.
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client if llm_client else default_llm_client

    async def evaluate(self, architecture_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a given software architecture.

        Args:
            architecture_info: A dictionary containing information about the architecture to be evaluated.

        Returns:
            A dictionary containing the evaluation results, including an overall score,
            metrics, strengths, weaknesses, improvement suggestions, and a risk assessment.
        """
        return await self.llm_client.evaluate_architecture(architecture_info)
