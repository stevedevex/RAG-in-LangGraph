# RAG-in-LangGraph

## 项目描述

这是一个基于 LangGraph 实现 RAG (Retrieval Augmented Generation) 的项目。它旨在通过结合检索和生成模型，提供更准确和信息丰富的回答。

## 安装

1. 克隆项目到本地：

   ```bash
   git clone https://github.com/kuhung/RAG-in-LangGraph.git
   cd RAG-in-LangGraph
   ```
2. 安装 `uv` (如果尚未安装)：

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # 或者通过 pipx 安装：pipx install uv
   ```
3. 安装 Python 依赖：

   ```bash
   uv sync
   ```
4. 配置环境变量：
   复制 `.env.example` 文件并重命名为 `.env`，然后根据您的实际情况填写 API 密钥等信息。

## 使用

目前项目包含 `rag_tools.py` 文件，用于定义 RAG 相关的工具函数。后续将添加更多关于如何运行和与 RAG 系统交互的说明。

## 联系方式

- **昵称**: kuhung
- **邮箱**: hi@kuhung.me
