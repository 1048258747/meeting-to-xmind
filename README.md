# Meeting to XMind

将会议记录通过 AI 分析自动转换为结构化的 XMind 思维导图文件。

## 功能特性

- 支持直接粘贴文本或读取文件
- 使用 LLM API 智能分析会议内容
- 自动生成结构化思维导图
- 支持按主题拆分为多个文件
- 支持多种 LLM 服务（通义千问、文心一言、DeepSeek 等）

## 安装

```bash
pip install -r requirements.txt
```

## 配置

创建 `config.json` 文件：

```json
{
  "llm_provider": "qwen",
  "api_key": "your-api-key",
  "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "model": "qwen-plus"
}
```

或通过环境变量配置：

```bash
export LLM_API_KEY="your-api-key"
export LLM_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
export LLM_MODEL="qwen-plus"
```

## 使用方法

### 直接输入文本

```bash
python -m meeting_to_xmind --text "会议记录内容..."
```

### 读取文件

```bash
python -m meeting_to_xmind --file meeting.txt
```

### 指定输出目录

```bash
python -m meeting_to_xmind --file meeting.txt --output ./output
```

### 按主题拆分

```bash
python -m meeting_to_xmind --file meeting.txt --split
```

### 使用自定义提示词

```bash
python -m meeting_to_xmind --file meeting.txt --prompt custom_prompt.txt
```

## 输出格式

### 单文件模式

```
meeting_title.xmind
├── 会议主题
    ├── 议题 1
    │   ├── 讨论要点
    │   └── 结论
    ├── 议题 2
    └── Action Items
        ├── @负责人: 任务描述 [截止日期]
```

### 多文件模式

```
output/
├── 01_议题1.xmind
├── 02_议题2.xmind
└── 03_议题3.xmind
```

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/ -v

# 运行带覆盖率的测试
pytest tests/ -v --cov=meeting_to_xmind
```

## License

MIT
