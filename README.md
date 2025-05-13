# Python FastAPI AI 架构推荐器

本项目是一个基于 Python 和 FastAPI 构建的 AI 驱动的软件架构推荐系统。它利用大型语言模型（LLM）分析用户输入的软件需求，并结合预定义的知识库，推荐合适的软件架构模式。

## 项目特性

*   **AI驱动的需求分析**：使用 LLM 理解和提取复杂软件需求中的关键特征。
*   **架构匹配**：根据分析出的需求特征，从知识库中匹配最合适的架构风格。
*   **评估与报告**：能够对推荐的架构进行初步评估，并生成推荐报告。
*   **微服务友好**：基于 FastAPI 构建，易于作为微服务部署和集成。
*   **可扩展知识库**：通过 JSON 文件管理架构知识，方便扩展和维护。

## 技术选型

*   **框架**: Python, FastAPI
*   **LLM 客户端**: `httpx` (用于与 DeepSeek API 等 LLM 服务交互)
*   **核心逻辑**: 自定义 Agent 类（需求解析、架构匹配、评估生成）
*   **数据格式**: JSON

## 项目结构

ai-architecture-recommender  
├── src  
│   ├── __init__.py  
│   ├── config.py               # 配置文件，如 API 密钥等  
│   ├── llm_client.py           # LLM 客户端的实现 (例如 DeepSeekClient)  
│   ├── main.py                 # FastAPI 应用入口和 API 端点定义  
│   ├── agents                  # 包含各个智能体的目录  
│   │   ├── __init__.py  
│   │   ├── requirement_agent.py    # 需求解析智能体  
│   │   ├── architecture_agent.py   # 架构匹配智能体  
│   │   └── evaluation_agent.py     # 评估生成智能体  
│   └── data  
│       └── knowledge.json      # 模拟的架构知识库  
├── requirements.txt            # 项目依赖  
└── README.md                   # 项目说明文档  


## 安装与配置

1.  **克隆仓库**:
    ```bash
    git clone <repository-url>
    cd ai-architecture-recommender
    ```

2.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置环境变量/`config.py`**:
    项目可能需要配置 LLM API 密钥等敏感信息。请参照 `src/config.py` 中的说明或使用环境变量进行配置。例如，如果使用 DeepSeek API，您需要设置 `DEEPSEEK_API_KEY`。

## 核心组件说明

*   **`src/config.py`**: 用于管理应用的配置，例如 API 密钥、模型名称等。
*   **`src/llm_client.py`**: 封装了与大型语言模型（如 DeepSeek API）交互的逻辑。它提供了调用 LLM 生成文本、分析需求等基础方法。
*   **`src/agents/`**:
    *   **`RequirementAgent`**: 负责接收用户输入的原始需求文本，调用 LLM 服务进行分析，提取关键技术特征、非功能性需求和约束。
    *   **`ArchitectureAgent`**: 根据 `RequirementAgent` 的分析结果，结合 `data/knowledge.json` 中的架构知识（或调用 LLM），匹配并推荐合适的软件架构。
    *   **`EvaluationAgent`**: 对 `ArchitectureAgent` 推荐的架构方案进行评估，分析其优缺点，并生成评估报告。
*   **`src/data/knowledge.json`**: 一个 JSON 文件，用作简易的知识库，存储不同软件架构模式的特征、适用场景、优缺点等信息。在更复杂的系统中，这可能被替换为真正的知识图谱或数据库。
*   **`src/main.py`**: FastAPI 应用的入口文件，定义了 API 端点（如 `/recommend`），并编排各个 Agent 的调用流程，处理 HTTP 请求和响应。

## 使用方法

1.  **启动服务**:
    在项目根目录下运行以下命令启动 FastAPI 应用：
    ```bash
    uvicorn src.main:app --reload
    ```
    服务默认将在 `http://localhost:8000` 启动。

2.  **API 端点**:
    *   **`POST /recommend`**: 接收软件需求描述，返回分析结果和架构推荐。

    **请求体**:
    ```json
    {
      "text": "您的软件需求描述文本，例如：开发一个支持高并发的在线购物平台，需要保证数据一致性和系统可扩展性。"
    }
    ```

    **请求示例 (使用 curl)**:
    ```bash
    curl -X POST "http://localhost:8000/recommend" \
    -H "Content-Type: application/json" \
    -d '{"text":"开发跨平台即时通讯系统，支持万人同时在线，需保证消息实时可靠，后期可能扩展视频功能"}'
    ```

    **预期响应结构 (示例)**:
    ```json
    {
      "features": { // 由 RequirementAgent 分析得出的特征
        "key_features": ["跨平台", "即时通讯", "万人同时在线", "消息实时可靠", "视频功能扩展"],
        "non_functional_requirements": {
          "concurrency": "high (万人同时在线)",
          "reliability": "high (消息实时可靠)",
          "scalability": "high (后期可能扩展视频功能)"
        },
        "constraints": [],
        "analysis_summary": "系统是一个高并发、高可靠、可扩展的跨平台即时通讯应用。"
      },
      "recommendations": { // 由 ArchitectureAgent 和 EvaluationAgent 生成的推荐和评估
        "recommended_styles": ["微服务架构", "事件驱动架构"],
        "comparison_matrix": { /* ... 比较细节 ... */ },
        "final_recommendation": "微服务架构",
        "reasoning": "微服务架构能够很好地支持模块化、独立部署和扩展，适合该即时通讯系统的需求...",
        "evaluation_report": {
            "overall_score": 8.5,
            "strengths": ["高内聚低耦合", "技术栈灵活"],
            "weaknesses": ["分布式系统复杂性高", "运维成本增加"],
            // ... 更多评估细节
        }
      }
    }
    ```
    *(注意: 上述响应结构是一个更详细的示例，请根据您 `main.py` 中实际返回的结构进行调整。)*

## 贡献

欢迎对此项目进行贡献！如果您有任何建议或想要改进代码，请：

1.  Fork 本仓库。
2.  创建您的特性分支 (`git checkout -b feature/AmazingFeature`)。
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4.  推送到分支 (`git push origin feature/AmazingFeature`)。
5.  开启一个 Pull Request。

## 许可证

本项目采用 MIT 许可证。详情请参阅 `LICENSE` 文件（如果项目中有）。