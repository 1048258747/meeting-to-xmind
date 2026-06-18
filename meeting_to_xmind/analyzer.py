from pathlib import Path
from typing import Any, Dict, List
from meeting_to_xmind.config import Config
from meeting_to_xmind.llm_client import LLMClient

class MeetingAnalyzer:
    def __init__(self, config: Config):
        self.config = config
        self.llm_client = LLMClient(config)
    
    async def analyze(self, content: str, custom_prompt: str = None) -> Dict[str, Any]:
        prompt = custom_prompt or self._load_default_prompt()
        result = await self.llm_client.analyze(content, prompt)
        self.validate_result(result)
        return result
    
    @staticmethod
    def validate_result(result: Dict[str, Any]) -> bool:
        if "title" not in result:
            raise ValueError("Analysis result must contain 'title'")
        if "topics" not in result:
            raise ValueError("Analysis result must contain 'topics'")
        if "action_items" not in result:
            result["action_items"] = []
        return True
    
    @staticmethod
    def split_for_output(result: Dict[str, Any], threshold: int = 5) -> List[Dict[str, Any]]:
        topics = result.get("topics", [])
        if len(topics) <= threshold:
            return [result]
        
        files = []
        for i, topic in enumerate(topics):
            file_data = {
                "title": f"{result['title']} - {topic['name']}",
                "date": result.get("date", ""),
                "topics": [topic],
                "action_items": result.get("action_items", []) if i == 0 else []
            }
            files.append(file_data)
        
        return files
    
    def _load_default_prompt(self) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / "analysis.txt"
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return self.llm_client._default_prompt()
    
    async def close(self):
        await self.llm_client.close()
