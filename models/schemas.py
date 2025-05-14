from pydantic import BaseModel
from typing import List, Dict

class RequirementAnalysis(BaseModel):
    key_features: List[str]
    non_functional_requirements: Dict[str, str]
    constraints: List[str]
    analysis_summary: str

class ArchitectureRecommendation(BaseModel):
    recommended_styles: List[str]
    comparison_matrix: Dict[str, Dict[str, List[str]]]
    final_recommendation: str
    reasoning: str

class ArchitectureEvaluation(BaseModel):
    overall_score: float
    metrics: List[str]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    risk_assessment: Dict[str, str]