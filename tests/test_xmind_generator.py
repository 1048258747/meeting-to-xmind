import zipfile
from pathlib import Path
import pytest
from meeting_to_xmind.xmind_generator import XMindGenerator

def test_generate_single_file(tmp_path):
    data = {
        "title": "Test Meeting",
        "date": "2026-06-18",
        "topics": [
            {
                "name": "Topic 1",
                "subtopics": [
                    {"name": "Sub 1", "content": "Content 1"}
                ]
            }
        ],
        "action_items": []
    }
    
    output_file = tmp_path / "test.xmind"
    generator = XMindGenerator()
    generator.generate(data, output_file)
    
    assert output_file.exists()
    assert output_file.suffix == ".xmind"
    
    with zipfile.ZipFile(output_file, "r") as zf:
        assert "content.xml" in zf.namelist()
        assert "META-INF/manifest.xml" in zf.namelist()
        assert "meta.xml" in zf.namelist()

def test_content_xml_structure(tmp_path):
    data = {
        "title": "Test Meeting",
        "topics": [
            {
                "name": "Topic 1",
                "subtopics": [
                    {"name": "Sub 1", "content": "Content 1"}
                ]
            }
        ],
        "action_items": [
            {"task": "Task 1", "assignee": "Alice", "deadline": "2026-06-20"}
        ]
    }
    
    output_file = tmp_path / "test.xmind"
    generator = XMindGenerator()
    generator.generate(data, output_file)
    
    with zipfile.ZipFile(output_file, "r") as zf:
        content = zf.read("content.xml").decode("utf-8")
        assert "Test Meeting" in content
        assert "Topic 1" in content
        assert "Sub 1" in content
        assert "Task 1" in content
        assert "Alice" in content

def test_generate_multiple_files(tmp_path):
    files_data = [
        {
            "title": "Meeting - Topic 1",
            "topics": [{"name": "Topic 1", "subtopics": []}],
            "action_items": []
        },
        {
            "title": "Meeting - Topic 2",
            "topics": [{"name": "Topic 2", "subtopics": []}],
            "action_items": []
        }
    ]
    
    output_dir = tmp_path / "output"
    generator = XMindGenerator()
    generator.generate_multiple(files_data, output_dir)
    
    assert output_dir.exists()
    xmind_files = list(output_dir.glob("*.xmind"))
    assert len(xmind_files) == 2
