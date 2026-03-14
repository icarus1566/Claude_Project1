import httpx

class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        
    async def generate_response(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300.0  # 첫 실행 시 모델 로드에 시간이 걸릴 수 있어 크게 설정
            )
            response.raise_for_status()
            return response.json().get("response", "")
