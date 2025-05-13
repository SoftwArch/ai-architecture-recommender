class Settings(object):
    # DeepSeek R1 API配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL_NAME: str = "deepseek-r1"
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"

    class Config:
        case_sensitive = True

settings = Settings()