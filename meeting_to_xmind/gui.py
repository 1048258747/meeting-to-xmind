# meeting_to_xmind/gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import asyncio
import sys
from pathlib import Path
from meeting_to_xmind.config import Config
from meeting_to_xmind.analyzer import MeetingAnalyzer
from meeting_to_xmind.xmind_generator import XMindGenerator

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
        
        # 操作按钮框架
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill=tk.X)
        
        self.generate_btn = ttk.Button(btn_frame, text="生成 XMind 文件", command=self._on_generate)
        self.generate_btn.pack()
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

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

    def _on_generate(self):
        # 获取输入内容
        content = self.text_input.get("1.0", tk.END).strip()
        file_path = self.file_path_var.get()
        
        if not content and not file_path:
            messagebox.showwarning("警告", "请输入会议记录内容或选择文件")
            return
        
        # 如果有文件，读取文件内容
        if file_path and not content:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败：{e}")
                return
        
        # 禁用按钮，更新状态
        self.generate_btn.config(state="disabled")
        self.status_var.set("正在分析会议记录...")
        
        # 在新线程中执行
        thread = threading.Thread(target=self._generate_worker, args=(content,), daemon=True)
        thread.start()

    def _generate_worker(self, content):
        try:
            # 加载配置
            config_path = Path("config.json")
            if config_path.exists():
                config = Config.from_file(config_path)
            else:
                config = Config.from_env()
            
            # 分析内容
            analyzer = MeetingAnalyzer(config)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(analyzer.analyze(content))
            loop.run_until_complete(analyzer.close())
            
            # 生成 XMind
            generator = XMindGenerator()
            output_dir = Path(self.output_dir_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if self.split_var.get():
                files_data = MeetingAnalyzer.split_for_output(result)
                generator.generate_multiple(files_data, output_dir)
                self.root.after(0, lambda: self.status_var.set(f"生成完成！共 {len(files_data)} 个文件"))
            else:
                filename = f"{result.get('title', 'meeting')}.xmind"
                output_file = output_dir / filename
                generator.generate(result, output_file)
                self.root.after(0, lambda: self.status_var.set(f"生成完成：{output_file}"))
            
            self.root.after(0, lambda: messagebox.showinfo("完成", "XMind 文件生成成功！"))
        
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"错误：{e}"))
            self.root.after(0, lambda: messagebox.showerror("错误", f"生成失败：{e}"))
        
        finally:
            self.root.after(0, lambda: self.generate_btn.config(state="normal"))

def main():
    root = tk.Tk()
    app = MeetingToXmindGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
