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
        
        # 输出配置框架
        output_frame = ttk.LabelFrame(self.root, text="输出配置", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 输出目录选择
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill=tk.X)
        
        ttk.Label(dir_frame, text="输出目录：").pack(side=tk.LEFT)
        
        self.output_dir_var = tk.StringVar(value=str(Path.cwd()))
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.dir_browse_btn = ttk.Button(dir_frame, text="浏览...", command=self._browse_output_dir)
        self.dir_browse_btn.pack(side=tk.LEFT)
        
        # 拆分选项
        self.split_var = tk.BooleanVar(value=False)
        self.split_check = ttk.Checkbutton(output_frame, text="按主题拆分为多个文件", variable=self.split_var)
        self.split_check.pack(anchor=tk.W, pady=(10, 0))

    def _browse_file(self):
        filetypes = [
            ("文本文件", "*.txt"),
            ("Markdown", "*.md"),
            ("所有文件", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)

    def _browse_output_dir(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir_var.set(dirname)

def main():
    root = tk.Tk()
    app = MeetingToXmindGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
