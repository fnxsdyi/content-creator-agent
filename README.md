# AI Content Creator Agent

基于 agno 框架的多 Agent 内容创作助手，使用 Streamlit 构建 UI。

## 功能特点

- **多 Agent 协作**：Web Researcher、Copywriter、Social Media Expert、SEO Expert
- **多平台支持**：微信公众号、小红书、抖音、知乎、微博、LinkedIn、Twitter
- **内容类型**：产品介绍、技术博客、营销文案、教程指南、行业分析、新闻稿
- **热点分析**：实时搜索行业热点
- **内容日历**：自动生成发布计划

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Web       │  │  Copywriter │  │ Social Media│     │
│  │  Researcher │→ │             │→ │   Expert    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │              │
│         └────────────────┼────────────────┘              │
│                          ↓                              │
│                 ┌─────────────┐                         │
│                 │  SEO Expert │                         │
│                 └─────────────┘                         │
│                          ↓                              │
│                 ┌─────────────┐                         │
│                 │   SQLite    │                         │
│                 │   (Memory)  │                         │
│                 └─────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

## 安装

```bash
cd content-creator-agent
pip install -r requirements.txt
```

## 运行

```bash
streamlit run app.py
```

## 环境要求

- Python 3.10+
- OpenAI API Key

## 使用示例

1. 输入 OpenAI API Key
2. 选择目标平台和内容类型
3. 输入主题和补充信息
4. 点击"开始创作"
5. 等待 AI Agent 团队协作完成

## 项目结构

```
content-creator-agent/
├── app.py              # 主应用
├── requirements.txt    # 依赖
└── README.md          # 说明文档
```

## 技术栈

- **agno** - Agent 编排框架
- **openai** - LLM API
- **streamlit** - Web UI
- **duckduckgo-search** - 搜索工具
- **sqlite** - 持久化存储
