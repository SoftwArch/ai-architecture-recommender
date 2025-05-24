# src/agents/evaluation_agent.py

import json
import logging
from typing import Dict, Optional
from models.schemas import ArchitectureEvaluation
from src.clients.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

class EvaluationAgent:
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.default_evaluation = ArchitectureEvaluation(
            overall_score=7.5,
            metrics=["可扩展性", "性能", "维护成本"],
            strengths=["默认架构的通用性", "技术社区支持"],
            weaknesses=["可能不完全匹配特定需求"],
            improvement_suggestions=["根据具体需求进行架构调整"],
            risk_assessment={
                "技术风险": "中等",
                "运维风险": "中等"
            }
        )

    async def evaluate(self, requirement: Dict, recommendation: Dict) -> ArchitectureEvaluation:
        """
        评估架构推荐方案，生成详细报告
        """
        try:
            prompt = self._build_evaluation_prompt(requirement, recommendation)
            response = await self.llm.generate_completion(prompt, temperature=0.3)
            return self._parse_response(response) if response else self.default_evaluation
        except Exception as e:
            logger.error(f"评估流程异常: {str(e)}")
            return self.default_evaluation

    def _build_evaluation_prompt(self, requirement: Dict, recommendation: Dict) -> str:
        """
        构建评估提示词模板
        """
        return f"""
        请对以下架构推荐方案进行全面技术评估：

        【推荐方案详情】
        关键特征：{requirement.get('key_features', [])}
        非功能性需求：{requirement.get('non_functional_requirements', {})}
        约束条件：{requirement.get('constraints', [])}
        需求分析结果：{requirement.get('analysis_summary')}
        最终推荐架构：{recommendation.get('final_recommendation')}
        候选架构列表：{recommendation.get('recommended_styles', [])}
        推荐理由：{recommendation.get('reasoning', '')}

        【评估要求】
        1. 分析5个该软件应重点和优先关注的质量属性及评分
        2. 给出0-10分的总体评分
        3. 列出主要优势和潜在缺陷
        4. 提出2-3条改进建议
        5. 评估主要技术风险

        请使用严格JSON格式返回，包含以下字段：
        - overall_score: 总体评分（浮点数）
        - metrics: 评估指标及分数列表（3项）
        - strengths: 优势列表（至少2项）
        - weaknesses: 劣势列表（至少2项）
        - improvement_suggestions: 改进建议列表
        - risk_assessment: 风险评估字典

        示例格式：
        ```json
        {{
            "metrics": ["可扩展性:8.8", "性能:7.9", "安全性:8.6", "可维护性:9.0", "易用性:7.5"],
            "overall_score": 8.5,
            "strengths": ["高并发处理能力", "模块解耦设计"],
            "weaknesses": ["运维复杂度高", "初期实施成本大"],
            "improvement_suggestions": [
                "增加缓存层设计",
                "实施自动化监控方案"
            ],
            "risk_assessment": {{
                "性能风险": "低",
                "扩展风险": "中等"
            }}
        }}
        ```
        """

    def _parse_response(self, response: str) -> ArchitectureEvaluation:
        """
        解析LLM响应并验证数据结构
        """
        try:
            # 提取JSON内容
            json_str = response.split("```json")[1].split("```")[0].strip()
            data = json.loads(json_str)

            # 数据校验和补全
            return ArchitectureEvaluation(
                overall_score=self._validate_score(data.get("overall_score", 7.0)),
                metrics=data.get("metrics", []),
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                improvement_suggestions=data.get("improvement_suggestions", []),
                risk_assessment=data.get("risk_assessment", {})
            )
        except (IndexError, json.JSONDecodeError, KeyError) as e:
            logger.warning(f"响应解析失败，使用默认评估: {str(e)}")
            return self.default_evaluation

    def _validate_score(self, score: float) -> float:
        """确保评分在合理范围内"""
        if score < 0: return 0.0
        if score > 10: return 10.0
        return round(score, 1)