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
        # 输入区域框架
        input_frame = ttk.LabelFrame(self.root, text="输入会议记录", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 文本输入框
        ttk.Label(input_frame, text="粘贴会议记录内容：").pack(anchor=tk.W)
        self.text_input = tk.Text(input_frame, height=10, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # 文件选择区域
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(file_frame, text="或选择文件：").pack(side=tk.LEFT)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly")
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.browse_btn = ttk.Button(file_frame, text="浏览...", command=self._browse_file)
        self.browse_btn.pack(side=tk.LEFT)

    def _browse_file(self):
        filetypes = [
            ("文本文件", "*.txt"),
            ("Markdown", "*.md"),
            ("所有文件", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)

def main():
    root = tk.Tk()
    app = MeetingToXmindGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
