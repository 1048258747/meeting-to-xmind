import pytest
from meeting_to_xmind.analyzer import MeetingAnalyzer
from meeting_to_xmind.config import Config

def test_analyzer_init():
    config = Config(
        api_key="test-key",
        api_base="https://test.com/v1",
        model="test-model"
    )
    analyzer = MeetingAnalyzer(config)
    assert analyzer.config == config

def test_validate_analysis_result_valid():
    result = {
        "title": "Test Meeting",
        "topics": [
            {"name": "Topic 1", "subtopics": [{"name": "Sub 1", "content": "Content"}]}
        ],
        "action_items": [
            {"task": "Task 1", "assignee": "Alice", "deadline": "2026-06-20"}
        ]
    }
    assert MeetingAnalyzer.validate_result(result) is True

def test_validate_analysis_result_missing_title():
    result = {"topics": [], "action_items": []}
    with pytest.raises(ValueError, match="title"):
        MeetingAnalyzer.validate_result(result)

def test_validate_analysis_result_missing_topics():
    result = {"title": "Test", "action_items": []}
    with pytest.raises(ValueError, match="topics"):
        MeetingAnalyzer.validate_result(result)

def test_split_by_topic_count():
    result = {
        "title": "Meeting",
        "topics": [
            {"name": f"Topic {i}", "subtopics": []} for i in range(6)
        ],
        "action_items": []
    }
    files = MeetingAnalyzer.split_for_output(result)
    assert len(files) == 6

def test_single_file_for_few_topics():
    result = {
        "title": "Meeting",
        "topics": [
            {"name": "Topic 1", "subtopics": []},
            {"name": "Topic 2", "subtopics": []}
        ],
        "action_items": []
    }
    files = MeetingAnalyzer.split_for_output(result)
    assert len(files) == 1
