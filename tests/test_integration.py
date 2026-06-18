import json
import pytest
from pathlib import Path
from meeting_to_xmind.config import Config
from meeting_to_xmind.xmind_generator import XMindGenerator

def test_full_workflow_without_llm(tmp_path):
    test_data = {
        "title": "Project Weekly Meeting",
        "date": "2026-06-18",
        "topics": [
            {
                "name": "Project Progress",
                "subtopics": [
                    {"name": "Frontend", "content": "80% complete"},
                    {"name": "Backend", "content": "API integration done"}
                ]
            },
            {
                "name": "Issues & Risks",
                "subtopics": [
                    {"name": "Third-party API delay", "content": "Need to follow up"},
                    {"name": "Design pending", "content": "Waiting for final assets"}
                ]
            },
            {
                "name": "Next Week Plan",
                "subtopics": [
                    {"name": "Complete unit tests", "content": ""},
                    {"name": "Prepare deployment", "content": ""}
                ]
            }
        ],
        "action_items": [
            {"task": "Fix login bug", "assignee": "Zhang San", "deadline": "2026-06-20"},
            {"task": "Provide design assets", "assignee": "Li Si", "deadline": "2026-06-22"}
        ]
    }
    
    generator = XMindGenerator()
    output_file = tmp_path / "meeting.xmind"
    generator.generate(test_data, output_file)
    
    assert output_file.exists()
    
    import zipfile
    with zipfile.ZipFile(output_file, "r") as zf:
        content = zf.read("content.xml").decode("utf-8")
        assert "Project Weekly Meeting" in content
        assert "Project Progress" in content
        assert "Issues &amp; Risks" in content
        assert "Fix login bug" in content
        assert "@Zhang San" in content

def test_split_workflow(tmp_path):
    test_data = {
        "title": "Big Meeting",
        "topics": [
            {"name": f"Topic {i}", "subtopics": [{"name": f"Sub {i}", "content": f"Content {i}"}]}
            for i in range(7)
        ],
        "action_items": [
            {"task": "Task 1", "assignee": "Alice", "deadline": None}
        ]
    }
    
    files_data = MeetingAnalyzer.split_for_output(test_data)
    assert len(files_data) == 7
    
    generator = XMindGenerator()
    output_dir = tmp_path / "split_output"
    generator.generate_multiple(files_data, output_dir)
    
    xmind_files = list(output_dir.glob("*.xmind"))
    assert len(xmind_files) == 7

from meeting_to_xmind.analyzer import MeetingAnalyzer
