# meeting_to_xmind/__main__.py
import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        from meeting_to_xmind.gui import main as gui_main
        gui_main()
    else:
        from meeting_to_xmind.cli import main as cli_main
        cli_main()

if __name__ == "__main__":
    main()
