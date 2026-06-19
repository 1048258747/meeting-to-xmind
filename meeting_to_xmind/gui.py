# meeting_to_xmind/gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import sys
from pathlib import Path

class MeetingToXmindGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("会议记录转 XMind")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self._create_widgets()
    
    def _create_widgets(self):
        pass

def main():
    root = tk.Tk()
    app = MeetingToXmindGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
