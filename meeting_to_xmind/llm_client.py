import json
from typing import Any, Dict
import httpx
from meeting_to_xmind.config import Config

class LLMClient:
    def __init__(self, config: Config):
        self.config = config
        self._client = httpx.AsyncClient(timeout=60.0)
    
    def _build_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
    
    async def analyze(self, content: str, prompt: str = None) -> Dict[str, Any]:
        if prompt is None:
            prompt = self._default_prompt()
        
        messages = [
            {"role": "system", "content": "You are a meeting analysis assistant. Analyze the meeting transcript and return structured JSON."},
            {"role": "user", "content": f"{prompt}\n\nMeeting transcript:\n{content}"}
        ]
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        
        response = await self._client.post(
            f"{self.config.api_base}/chat/completions",
            headers=self._build_headers(),
            json=payload
        )
        response.raise_for_status()
        
        data = response.json()
        return json.loads(data["choices"][0]["message"]["content"])
    
    def _default_prompt(self) -> str:
        return """Analyze this meeting transcript and return a JSON object with the following structure:
{
  "title": "Meeting title (extract from content or generate)",
  "date": "Meeting date (if mentioned)",
  "topics": [
    {
      "name": "Topic name",
      "subtopics": [
        {"name": "Subtopic name", "content": "Details"}
      ]
    }
  ],
  "action_items": [
    {"task": "Task description", "assignee": "Person name", "deadline": "Date if mentioned"}
  ]
}
Extract all main topics, discussion points, conclusions, and action items."""
    
    async def close(self):
        await self._client.aclose()