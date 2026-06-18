import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class Config:
    api_key: str
    api_base: str
    model: str
    llm_provider: str = "openai_compatible"
    
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("api_key cannot be empty")
        if not self.api_base:
            raise ValueError("api_base cannot be empty")
        if not self.model:
            raise ValueError("model cannot be empty")
    
    @classmethod
    def from_file(cls, path: Path) -> "Config":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            api_key=data.get("api_key", ""),
            api_base=data.get("api_base", ""),
            model=data.get("model", ""),
            llm_provider=data.get("llm_provider", "openai_compatible")
        )
    
    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            api_key=os.getenv("LLM_API_KEY", ""),
            api_base=os.getenv("LLM_API_BASE", ""),
            model=os.getenv("LLM_MODEL", ""),
            llm_provider=os.getenv("LLM_PROVIDER", "openai_compatible")
        )