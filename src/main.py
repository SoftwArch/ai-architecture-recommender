from fastapi import FastAPI
from agents.requirement_agent import RequirementAgent
from agents.architecture_agent import ArchitectureAgent
from agents.evaluation_agent import EvaluationAgent

app = FastAPI()

@app.post("/recommend")
async def recommend(request: dict):
    req_agent = RequirementAgent()
    arch_agent = ArchitectureAgent()
    eval_agent = EvaluationAgent()
    
    features = req_agent.analyze(request["text"])
    candidates = arch_agent.match(features)
    report = eval_agent.generate_report(candidates)
    
    return {
        "features": features,
        "recommendations": report
    }