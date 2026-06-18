import pytest
from meeting_to_xmind.cli import parse_args

def test_parse_args_with_text():
    args = parse_args(["--text", "Meeting about project X"])
    assert args.text == "Meeting about project X"

def test_parse_args_with_file():
    args = parse_args(["--file", "/path/to/meeting.txt"])
    assert args.file == "/path/to/meeting.txt"

def test_parse_args_with_output():
    args = parse_args(["--text", "content", "--output", "/output/dir"])
    assert args.output == "/output/dir"

def test_parse_args_with_config():
    args = parse_args(["--text", "content", "--config", "/path/to/config.json"])
    assert args.config == "/path/to/config.json"

def test_parse_args_with_split():
    args = parse_args(["--text", "content", "--split"])
    assert args.split is True

def test_parse_args_default_split():
    args = parse_args(["--text", "content"])
    assert args.split is False
