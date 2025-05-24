from typing import Optional
import json
import logging
from models.schemas import RequirementAnalysis
from src.clients.deepseek_client import DeepSeekClient
logger = logging.getLogger(__name__)
class RequirementAgent:
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client

    async def analyze(self, description: str) -> Optional[RequirementAnalysis]:
        """
        分析软件需求
        """
        prompt = f"""请分析以下软件需求，并提取关键特征、非功能性需求和约束：
        
                    需求描述：
                    {description}

                    请以JSON格式返回，包含以下字段：
                    - key_features: 关键特征列表
                    - non_functional_requirements: 非功能性需求字典
                    - constraints: 约束列表
                    - analysis_summary: 分析总结
                    注意：所有字段均用中文回答。
                """
        response = await self.llm.generate_completion(prompt)
        return self._parse_response(response) if response else None

    def _parse_response(self, response: str) -> RequirementAnalysis:
        try:
            json_str = response.split("```json")[1].split("```")[0].strip()
            return RequirementAnalysis(**json.loads(json_str))
        except (IndexError, json.JSONDecodeError) as e:
            raise ValueError("解析响应失败") from e