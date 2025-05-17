from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import uvicorn
from src.services.assistant_service import AssistantService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """初始化"""
    app.state.assistant_service = AssistantService()
    yield


app = FastAPI(title="软件架构风格智能助手",
             description="基于大模型的软件架构风格智能助手",
             version="1.0.0",
             lifespan=lifespan
    )

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    description: str
    user_level: str = "expert"  # expert/normal

class ArchitectureDetailRequest(BaseModel):
    style_name: str

@app.post("/api/v1/recommend", 
          summary="获取架构推荐",
          tags=["核心服务"],
          response_model=dict)
async def get_recommendation(request: RecommendationRequest):
    """
    架构推荐主入口：
    - description: 自然语言需求描述
    - user_level: 用户专业级别（expert/normal）
    """
    try:
        result = await app.state.assistant_service.process_request(
            request.description
        )
        return {
            "status": "success",
            "data": result,
            "meta": {"user_level": request.user_level}
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"推荐服务异常: {str(e)}"
        )

@app.post("/api/v1/architecture/detail",
          summary="获取架构详情",
          tags=["架构知识库"],
          response_model=dict)
async def get_architecture_detail(request: ArchitectureDetailRequest):
    """获取指定架构风格的详细信息"""
    try:
        detail = await app.state.assistant_service.get_architecture_details(
            request.style_name
        )
        return {
            "status": "success",
            "data": detail,
            "style": request.style_name
        }
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"未找到架构风格: {request.style_name}"
        )

@app.get("/health", 
         summary="健康检查",
         tags=["运维接口"])
async def health_check():
    """服务健康检查端点"""
    return {
        "status": "healthy",
        "services": {
            "recommendation": "active",
            "knowledge_base": "active"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=False,
        workers=4
    )