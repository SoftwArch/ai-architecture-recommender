from typing import Dict, Any
import httpx
from config import settings
from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    async def generate_completion(self, prompt: str, temperature: float = 0.7) -> str:
        pass

class DeepSeekClient(BaseLLMClient):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_base = settings.DEEPSEEK_API_BASE
        self.model = settings.DEEPSEEK_MODEL_NAME
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_completion(self, prompt: str, temperature: float = 0.7) -> str:
        """
        使用DeepSeek R1 API生成文本补全
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def analyze_requirements(self, description: str) -> Dict[str, Any]:
        """
        分析软件需求(需求解析Agent)
        """
        prompt = f"""请分析以下软件需求，并提取关键特征、非功能性需求和约束：
        
                    需求描述：
                    {description}

                    请以JSON格式返回，包含以下字段：
                    - key_features: 关键特征列表
                    - non_functional_requirements: 非功能性需求字典
                    - constraints: 约束列表
                    - analysis_summary: 分析总结
                """
        response = await self.generate_completion(prompt, temperature=0.3)
        return eval(response)  # 注意：实际生产环境中应该使用更安全的JSON解析方法

    async def recommend_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        推荐软件架构(架构匹配Agent)
        """
        prompt = f"""基于以下需求分析结果，推荐合适的软件架构风格：

                    需求分析：
                    {requirements}

                    请以JSON格式返回，包含以下字段：
                    - recommended_styles: 推荐的架构风格列表
                    - comparison_matrix: 架构风格比较矩阵
                    - final_recommendation: 最终推荐的架构风格
                    - reasoning: 推荐理由
                """
        response = await self.generate_completion(prompt, temperature=0.3)
        return eval(response)

    async def evaluate_architecture(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估软件架构(评估生成Agent)
        """
        prompt = f"""请对以下软件架构进行全面评估：

                    架构信息：
                    {architecture}

                    请以JSON格式返回，包含以下字段：
                    - overall_score: 总体评分
                    - metrics: 评估指标列表
                    - strengths: 优势列表
                    - weaknesses: 劣势列表
                    - improvement_suggestions: 改进建议列表
                    - risk_assessment: 风险评估字典
                """
        response = await self.generate_completion(prompt, temperature=0.3)
        return eval(response)

class LLMFactory:
    @staticmethod
    def create_llm_client(llm_type: str = "deepseek") -> BaseLLMClient:
        if llm_type == "deepseek":
            return DeepSeekClient()
        # 可以在这里添加其他LLM的实现
        raise ValueError(f"Unsupported LLM type: {llm_type}")

# 创建默认的LLM客户端实例
default_llm_client = LLMFactory.create_llm_client() 