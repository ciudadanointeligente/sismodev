import httpx
from django.conf import settings


class LlamaParseService:
    def __init__(self):
        self.api_key = settings.LLAMAPARSE_API_KEY
        self.base_url = "https://api.cloud.llamaparse.com"

    async def parse_document(self, file_url: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/parse",
                json={"url": file_url},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=60.0,
            )
            response.raise_for_status()
            return response.json()

    async def analyze_content(self, content: str, parameters: dict) -> dict:
        prompt = self._build_analysis_prompt(parameters)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/analyze",
                json={"content": content, "prompt": prompt},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json()

    def _build_analysis_prompt(self, parameters: dict) -> str:
        return """
Analiza el siguiente documento según criterios de derechos humanos y democráticos.
Devuelve en JSON: human_rights_score, democratic_score, violations_detected, concerns, recommendations.
"""
