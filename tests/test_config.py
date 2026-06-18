import json
import pytest
from pathlib import Path
from meeting_to_xmind.config import Config

def test_load_config_from_file(tmp_path):
    config_data = {
        "llm_provider": "qwen",
        "api_key": "test-key",
        "api_base": "https://test.com/v1",
        "model": "test-model"
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data), encoding="utf-8")
    
    config = Config.from_file(config_file)
    assert config.llm_provider == "qwen"
    assert config.api_key == "test-key"
    assert config.api_base == "https://test.com/v1"
    assert config.model == "test-model"

def test_load_config_from_env(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "env-key")
    monkeypatch.setenv("LLM_API_BASE", "https://env.com/v1")
    monkeypatch.setenv("LLM_MODEL", "env-model")
    
    config = Config.from_env()
    assert config.api_key == "env-key"
    assert config.api_base == "https://env.com/v1"
    assert config.model == "env-model"

def test_config_validation():
    with pytest.raises(ValueError):
        Config(api_key="", api_base="https://test.com", model="test")