import pytest
from meeting_to_xmind.llm_client import LLMClient
from meeting_to_xmind.config import Config

def test_llm_client_init():
    config = Config(
        api_key="test-key",
        api_base="https://test.com/v1",
        model="test-model"
    )
    client = LLMClient(config)
    assert client.config == config

def test_build_headers():
    config = Config(
        api_key="test-key",
        api_base="https://test.com/v1",
        model="test-model"
    )
    client = LLMClient(config)
    headers = client._build_headers()
    assert headers["Authorization"] == "Bearer test-key"
    assert headers["Content-Type"] == "application/json"

@pytest.mark.asyncio
async def test_analyze_content_mock(monkeypatch):
    config = Config(
        api_key="test-key",
        api_base="https://test.com/v1",
        model="test-model"
    )
    client = LLMClient(config)
    
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": '{"title": "Test Meeting", "topics": []}'
                }
            }
        ]
    }
    
    async def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, data):
                self._data = data
                self.status_code = 200
            def json(self):
                return self._data
            def raise_for_status(self):
                pass
        return MockResponse(mock_response)
    
    monkeypatch.setattr(client._client, "post", mock_post)
    
    result = await client.analyze("Test meeting content")
    assert result["title"] == "Test Meeting"