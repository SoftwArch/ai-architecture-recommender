import httpx
import asyncio
import logging
from config.settings import settings
from typing import Optional

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        self.timeout = 60.0  # 超时时间从30秒增加到60秒
        self.max_retries = 5  # 最大重试次数增加到5次

    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> Optional[str]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(max_retries):
                try:
                    response = await client.post(
                        f"{settings.DEEPSEEK_API_BASE}/chat/completions",
                        headers=self.headers,
                        json={
                            "model": settings.DEEPSEEK_MODEL_NAME,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": temperature
                        }
                    )
                    response.raise_for_status()
                    print("Response content:", response.json()["choices"][0]["message"]["content"])
                    return response.json()["choices"][0]["message"]["content"]
                except httpx.ReadTimeout:  # 新增超时重试
                    if attempt < self.max_retries - 1:
                        logger.warning(f"API请求超时，第{attempt+1}次重试...")
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise