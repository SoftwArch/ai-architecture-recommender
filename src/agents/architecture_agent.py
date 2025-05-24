from pathlib import Path
import json
import logging
from typing import Dict, List, Optional
from models.schemas import ArchitectureRecommendation
from config.settings import settings
from src.clients.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

class ArchitectureAgent:
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.knowledge = self._load_architecture_knowledge()
        self.min_candidates = 3

    def _load_architecture_knowledge(self) -> Dict:
        """加载本地架构知识库"""
        try:
            knowledge_path = Path(__file__).parent.parent / "knowledge" / "architecture_knowledge.json"
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"加载知识库失败: {str(e)}")
            return {}

    def _rule_based_filter(self, analysis_data: Dict) -> List[str]:
        """基于多维度规则的架构风格初步筛选"""
        candidates = []
        
        # 根据非功能性需求筛选
        nfr = analysis_data.get('non_functional_requirements', {})
        if nfr.get('performance'):
            candidates.extend(['事件驱动架构', '微服务架构'])
        if nfr.get('scalability'):
            candidates.append('微服务架构')
        if nfr.get('reliability'):
            candidates.append('分层架构')

        # 根据约束条件筛选
        constraints = analysis_data.get('constraints', [])
        if '低成本运维' in constraints:
            candidates.append('单体架构')

        return list(set(candidates))

    async def _llm_based_ranking(self, candidates: List[str], analysis_data: Dict) -> ArchitectureRecommendation:
        """使用LLM进行最终排序和推荐"""
        prompt = f"""
        根据以下需求分析结果和候选架构列表，请：
        1. 推荐最适合的3种架构风格（按优先级排序）
        2. 生成比较矩阵 
        3. 给出最终推荐理由

        需求分析：
        {json.dumps(analysis_data, indent=2, ensure_ascii=False)}

        候选架构：
        {candidates}

        知识库信息：
        {json.dumps(self.knowledge, ensure_ascii=False)}

        请使用严格JSON格式返回，包含以下字段：
        - recommended_styles (按优先级排序的架构列表) (List[str])
        - comparison_matrix (架构对比矩阵) (Dict[str, Dict[str, str(理由，格式类似于“优秀/良好/一般/差/达标/风险/>=70%(详细原因)”)])
        - final_recommendation (最终推荐架构) (str)
        - reasoning (推荐理由) (str: "1) 第一点; 2); 第二点; 3) 第三点")
        注意：用中文回答。
        """
        
        try:
            response = await self.llm.generate_completion(prompt, temperature=0.5)
            if not response:
                raise ValueError("LLM响应为空")
            
            # 提取JSON内容
            json_str = response.split("```json")[1].split("```")[0].strip()
            result = json.loads(json_str)
                
            return ArchitectureRecommendation(**result)
        except (IndexError, json.JSONDecodeError, KeyError) as e:
            logger.error(f"解析LLM响应失败: {str(e)}")
            return ArchitectureRecommendation(
                recommended_styles=['微服务架构', '事件驱动架构', '分层架构'],
                final_recommendation='微服务架构',
                reasoning="默认推荐：适用于大多数分布式系统场景",
                comparison_matrix={}
            )

    async def recommend(self, analysis_data: Dict) -> ArchitectureRecommendation:
        rule_based_candidates = ['批处理架构', '主程序-子过程架构', '面向对象架构', '分层架构', '进程间通信架构', '隐式调用架构', '显式调用架构', '管道-过滤器架构', '仓库架构', '黑板架构', '解释器架构', '基于规则的系统架构']
        
        return await self._llm_based_ranking(
            candidates=list(set(rule_based_candidates)),
            analysis_data=analysis_data
        )