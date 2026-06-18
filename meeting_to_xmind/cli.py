import argparse
import asyncio
import sys
from pathlib import Path
from typing import List, Optional
from meeting_to_xmind.config import Config
from meeting_to_xmind.analyzer import MeetingAnalyzer
from meeting_to_xmind.xmind_generator import XMindGenerator

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert meeting transcripts to XMind mind maps"
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--text",
        type=str,
        help="Direct text input of meeting transcript"
    )
    input_group.add_argument(
        "--file",
        type=str,
        help="Path to meeting transcript file"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=".",
        help="Output directory for XMind files (default: current directory)"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config.json",
        help="Path to config.json file"
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Split into multiple files by topic"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Custom analysis prompt file path"
    )
    
    return parser.parse_args(argv)

async def run(args: argparse.Namespace) -> int:
    try:
        config_path = Path(args.config)
        if config_path.exists():
            config = Config.from_file(config_path)
        else:
            config = Config.from_env()
        
        content = read_input(args)
        if not content:
            print("Error: No content provided", file=sys.stderr)
            return 1
        
        analyzer = MeetingAnalyzer(config)
        
        custom_prompt = None
        if args.prompt:
            custom_prompt = Path(args.prompt).read_text(encoding="utf-8")
        
        print("Analyzing meeting transcript...")
        result = await analyzer.analyze(content, custom_prompt)
        
        generator = XMindGenerator()
        output_dir = Path(args.output)
        
        if args.split:
            files_data = MeetingAnalyzer.split_for_output(result)
            print(f"Generating {len(files_data)} XMind files...")
            generator.generate_multiple(files_data, output_dir)
        else:
            filename = f"{result.get('title', 'meeting')}.xmind"
            output_file = output_dir / filename
            output_dir.mkdir(parents=True, exist_ok=True)
            generator.generate(result, output_file)
            print(f"Generated: {output_file}")
        
        await analyzer.close()
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    
    file_path = Path(args.file)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    encodings = ["utf-8", "gbk", "gb2312", "latin-1"]
    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"Unable to read file with any supported encoding: {file_path}")

def main(argv: Optional[List[str]] = None):
    args = parse_args(argv)
    exit_code = asyncio.run(run(args))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
