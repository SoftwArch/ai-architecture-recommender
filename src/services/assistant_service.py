# 服务集成
import logging
from typing import Dict, Optional
from models.schemas import (
    RequirementAnalysis,
    ArchitectureRecommendation,
    ArchitectureEvaluation
)
from src.agents.requirement_agent import RequirementAgent
from src.agents.architecture_agent import ArchitectureAgent
from src.agents.evaluation_agent import EvaluationAgent
from src.clients.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self):
        # 初始化LLM客户端
        self.llm_client = DeepSeekClient()
        
        # 初始化智能体
        self.requirement_agent = RequirementAgent(self.llm_client)
        self.architecture_agent = ArchitectureAgent(self.llm_client)
        self.evaluation_agent = EvaluationAgent(self.llm_client)

    async def _handle_error(self, stage: str, error: Exception) -> Dict:
        """统一错误处理"""
        logger.error(f"{stage}阶段出错: {str(error)}")
        return {
            "error": {
                "stage": stage,
                "message": f"{type(error).__name__}: {str(error)}"
            },
            "recommendation": {
                "final_recommendation": "微服务架构",
                "reasoning": "默认推荐：系统出现异常时推荐通用架构"
            }
        }

    async def process_request(self, user_input: str) -> Dict:
        """端到端处理流程"""
        try:
            # 第一阶段：需求分析
            print("\n\n\n")
            print("第一阶段：需求分析: ")
            print("*******************************************************")
            requirement_analysis = await self.requirement_agent.analyze(user_input)
            if not requirement_analysis:
                raise ValueError("需求分析失败")

            # 第二阶段：架构推荐
            print("\n\n\n")
            print("第二阶段：架构推荐: ")
            print("*******************************************************")
            arch_recommendation = await self.architecture_agent.recommend(
                requirement_analysis.model_dump()
            )

            # 第三阶段：架构评估
            print("\n\n\n")
            print("第三阶段：架构评估: ")
            print("*******************************************************")
            evaluation = await self.evaluation_agent.evaluate(
                requirement_analysis.model_dump(), arch_recommendation.model_dump()
            )

            return {
                "analysis": requirement_analysis.model_dump(),
                "recommendation": arch_recommendation.model_dump(),
                "evaluation": evaluation.model_dump()
            }

        except Exception as e:
            return await self._handle_error("处理流程", e)

    async def get_architecture_details(self, style_name: str) -> Optional[Dict]:
        """获取架构风格详细信息"""
        try:
            return self.architecture_agent.knowledge.get(style_name)
        except AttributeError as e:
            logger.error(f"获取架构信息失败: {str(e)}")
            return None

    async def validate_recommendation(self, user_feedback: Dict) -> bool:
        """验证推荐结果（示例方法）"""
        try:
            required_keys = ['selected_style', 'satisfaction_level']
            if all(k in user_feedback for k in required_keys):
                logger.info(f"收到用户反馈: {user_feedback}")
                return True
            return False
        except Exception as e:
            logger.error(f"验证反馈失败: {str(e)}")
            return False