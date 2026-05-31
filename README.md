<div align="center">

# ⏱️ DevTime CLI

**A powerful command-line time tracking tool for developers**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
# 🇺🇸 English

## 🎉 Introduction

DevTime CLI is a powerful yet simple command-line time tracking tool designed specifically for developers. Track time spent on projects and tasks directly from your terminal without switching contexts or opening heavy GUI applications.

### Why DevTime CLI?

- 🚀 **Stay in Flow**: No context switching - track time without leaving your terminal
- 💾 **Privacy First**: All data stored locally in SQLite - no cloud, no accounts
- ⚡ **Lightning Fast**: Built with performance in mind, starts instantly
- 🎨 **Beautiful Output**: Rich terminal UI with colors, tables, and progress indicators
- 📤 **Export Freedom**: Export your data to CSV or JSON anytime

## ✨ Core Features

| Feature | Description | Emoji |
|---------|-------------|-------|
| **Project Management** | Organize work into multiple projects | 📁 |
| **Task Tracking** | Track time for individual tasks within projects | 📋 |
| **Simple Timer** | Start/stop timers with single commands | ⏱️ |
| **Rich Reports** | View detailed statistics and time analytics | 📊 |
| **Data Export** | Export to CSV and JSON formats | 📤 |
| **Local Storage** | SQLite database - your data stays on your machine | 💾 |
| **Cross-Platform** | Works on Linux, macOS, and Windows | 🖥️ |

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install devtime-cli

# Or install from source
git clone https://github.com/gitstq/devtime-cli.git
cd devtime-cli
pip install -e .
```

### Requirements

- Python 3.8 or higher
- pip package manager

### Basic Usage

```bash
# Create your first project
devtime project create "My Awesome Project" --description "Building something cool"

# Add tasks to your project
devtime task create "My Awesome Project" "Feature Development"
devtime task create "My Awesome Project" "Bug Fixes"

# Start tracking time
devtime start "My Awesome Project" "Feature Development"

# Check timer status
devtime status

# Stop tracking
devtime stop

# View reports
devtime report projects
devtime report tasks
devtime report daily
```

## 📖 Detailed Usage Guide

### Project Commands

```bash
# Create a new project
devtime project create "Project Name" --description "Optional description"

# List all projects
devtime project list

# Delete a project (with confirmation)
devtime project delete "Project Name"
```

### Task Commands

```bash
# Create a task in a project
devtime task create "Project Name" "Task Name" --description "Optional description"

# List all tasks (optionally filter by project)
devtime task list
devtime task list "Project Name"

# Delete a task
devtime task delete "Project Name" "Task Name"
```

### Timer Commands

```bash
# Start tracking time for a task
devtime start "Project Name" "Task Name" --notes "Optional notes"

# Check current timer status
devtime status

# Stop the current timer
devtime stop
```

### Report Commands

```bash
# View time entries with filters
devtime report entries --project "Project Name" --from 2025-01-01 --to 2025-01-31

# View project statistics
devtime report projects

# View task statistics
devtime report tasks "Project Name"

# View daily statistics
devtime report daily --days 30
```

### Export Commands

```bash
# Export to CSV
devtime export csv ~/timetrack_data.csv --project "Project Name"

# Export to JSON
devtime export json ~/timetrack_data.json --from 2025-01-01
```

## 💡 Design Philosophy

DevTime CLI was built with these principles:

1. **Developer-First**: Designed for developers who live in the terminal
2. **Zero Friction**: Minimal commands to start tracking
3. **Data Ownership**: Your data stays local, always
4. **Unix Philosophy**: Do one thing well - track time

## 📦 Development

### Setup Development Environment

```bash
git clone https://github.com/gitstq/devtime-cli.git
cd devtime-cli
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
# 🇨🇳 简体中文

## 🎉 项目介绍

DevTime CLI 是一款专为开发者设计的强大而简洁的命令行时间追踪工具。无需切换上下文或打开笨重的 GUI 应用，直接在终端中追踪项目和任务的时间消耗。

### 为什么选择 DevTime CLI？

- 🚀 **保持专注**：无需切换上下文 - 在终端内即可完成时间追踪
- 💾 **隐私优先**：所有数据存储在本地 SQLite 中 - 无云端，无需账户
- ⚡ **极速启动**：以性能为核心设计，瞬间启动
- 🎨 **美观输出**：富文本终端界面，支持颜色、表格和进度指示器
- 📤 **自由导出**：随时将数据导出为 CSV 或 JSON 格式

## ✨ 核心特性

| 特性 | 描述 | 图标 |
|---------|-------------|-------|
| **项目管理** | 将工作组织到多个项目中 | 📁 |
| **任务追踪** | 追踪项目内各个任务的时间 | 📋 |
| **简单计时器** | 使用单条命令启动/停止计时 | ⏱️ |
| **丰富报告** | 查看详细的统计和时间分析 | 📊 |
| **数据导出** | 支持 CSV 和 JSON 格式导出 | 📤 |
| **本地存储** | SQLite 数据库 - 数据始终保存在您的设备上 | 💾 |
| **跨平台** | 支持 Linux、macOS 和 Windows | 🖥️ |

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装（推荐）
pip install devtime-cli

# 或从源码安装
git clone https://github.com/gitstq/devtime-cli.git
cd devtime-cli
pip install -e .
```

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 基本用法

```bash
# 创建您的第一个项目
devtime project create "我的项目" --description "构建酷炫的东西"

# 为项目添加任务
devtime task create "我的项目" "功能开发"
devtime task create "我的项目" "Bug 修复"

# 开始追踪时间
devtime start "我的项目" "功能开发"

# 查看计时器状态
devtime status

# 停止追踪
devtime stop

# 查看报告
devtime report projects
devtime report tasks
devtime report daily
```

## 📖 详细使用指南

### 项目命令

```bash
# 创建新项目
devtime project create "项目名称" --description "可选描述"

# 列出所有项目
devtime project list

# 删除项目（带确认）
devtime project delete "项目名称"
```

### 任务命令

```bash
# 在项目中创建任务
devtime task create "项目名称" "任务名称" --description "可选描述"

# 列出所有任务（可选按项目筛选）
devtime task list
devtime task list "项目名称"

# 删除任务
devtime task delete "项目名称" "任务名称"
```

### 计时器命令

```bash
# 开始追踪任务时间
devtime start "项目名称" "任务名称" --notes "可选备注"

# 查看当前计时器状态
devtime status

# 停止当前计时器
devtime stop
```

### 报告命令

```bash
# 查看时间条目（带筛选）
devtime report entries --project "项目名称" --from 2025-01-01 --to 2025-01-31

# 查看项目统计
devtime report projects

# 查看任务统计
devtime report tasks "项目名称"

# 查看每日统计
devtime report daily --days 30
```

### 导出命令

```bash
# 导出为 CSV
devtime export csv ~/timetrack_data.csv --project "项目名称"

# 导出为 JSON
devtime export json ~/timetrack_data.json --from 2025-01-01
```

## 💡 设计理念

DevTime CLI 遵循以下原则构建：

1. **开发者优先**：为生活在终端中的开发者设计
2. **零摩擦**：用最少的命令开始追踪
3. **数据所有权**：您的数据始终保存在本地
4. **Unix 哲学**：把一件事做好 - 追踪时间

## 📦 开发

### 设置开发环境

```bash
git clone https://github.com/gitstq/devtime-cli.git
cd devtime-cli
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### 运行测试

```bash
python -m pytest tests/
```

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'feat: 添加某个 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 开源协议

本项目采用 MIT 协议 - 详情请参见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
# 🇹🇼 繁體中文

## 🎉 專案介紹

DevTime CLI 是一款專為開發者設計的強大而簡潔的命令列時間追蹤工具。無需切換上下文或開啟笨重的 GUI 應用，直接在終端機中追蹤專案和任務的時間消耗。

### 為什麼選擇 DevTime CLI？

- 🚀 **保持專注**：無需切換上下文 - 在終端機內即可完成時間追蹤
- 💾 **隱私優先**：所有資料儲存在本地 SQLite 中 - 無雲端，無需帳戶
- ⚡ **極速啟動**：以效能為核心設計，瞬間啟動
- 🎨 **美觀輸出**：富文字終端機介面，支援顏色、表格和進度指示器
- 📤 **自由匯出**：隨時將資料匯出為 CSV 或 JSON 格式

## ✨ 核心特性

| 特性 | 描述 | 圖示 |
|---------|-------------|-------|
| **專案管理** | 將工作組織到多個專案中 | 📁 |
| **任務追蹤** | 追蹤專案內各個任務的時間 | 📋 |
| **簡單計時器** | 使用單條命令啟動/停止計時 | ⏱️ |
| **豐富報告** | 檢視詳細的統計和時間分析 | 📊 |
| **資料匯出** | 支援 CSV 和 JSON 格式匯出 | 📤 |
| **本地儲存** | SQLite 資料庫 - 資料始終儲存在您的裝置上 | 💾 |
| **跨平台** | 支援 Linux、macOS 和 Windows | 🖥️ |

## 🚀 快速開始

### 安裝

```bash
# 從 PyPI 安裝（推薦）
pip install devtime-cli

# 或從原始碼安裝
git clone https://github.com/gitstq/devtime-cli.git
cd devtime-cli
pip install -e .
```

### 環境要求

- Python 3.8 或更高版本
- pip 套件管理器

### 基本用法

```bash
# 建立您的第一個專案
devtime project create "我的專案" --description "建構酷炫的東西"

# 為專案新增任務
devtime task create "我的專案" "功能開發"
devtime task create "我的專案" "Bug 修復"

# 開始追蹤時間
devtime start "我的專案" "功能開發"

# 檢視計時器狀態
devtime status

# 停止追蹤
devtime stop

# 檢視報告
devtime report projects
devtime report tasks
devtime report daily
```

## 📖 詳細使用指南

### 專案命令

```bash
# 建立新專案
devtime project create "專案名稱" --description "可選描述"

# 列出所有專案
devtime project list

# 刪除專案（帶確認）
devtime project delete "專案名稱"
```

### 任務命令

```bash
# 在專案中建立任務
devtime task create "專案名稱" "任務名稱" --description "可選描述"

# 列出所有任務（可選按專案篩選）
devtime task list
devtime task list "專案名稱"

# 刪除任務
devtime task delete "專案名稱" "任務名稱"
```

### 計時器命令

```bash
# 開始追蹤任務時間
devtime start "專案名稱" "任務名稱" --notes "可選備註"

# 檢視目前計時器狀態
devtime status

# 停止目前計時器
devtime stop
```

### 報告命令

```bash
# 檢視時間條目（帶篩選）
devtime report entries --project "專案名稱" --from 2025-01-01 --to 2025-01-31

# 檢視專案統計
devtime report projects

# 檢視任務統計
devtime report tasks "專案名稱"

# 檢視每日統計
devtime report daily --days 30
```

### 匯出命令

```bash
# 匯出為 CSV
devtime export csv ~/timetrack_data.csv --project "專案名稱"

# 匯出為 JSON
devtime export json ~/timetrack_data.json --from 2025-01-01
```

## 💡 設計理念

DevTime CLI 遵循以下原則建構：

1. **開發者優先**：為生活在終端機中的開發者設計
2. **零摩擦**：用最少的命令開始追蹤
3. **資料所有權**：您的資料始終儲存在本地
4. **Unix 哲學**：把一件事做好 - 追蹤時間

## 📦 開發

### 設定開發環境

```bash
git clone https://github.com/gitstq/devtime-cli.git
cd devtime-cli
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### 執行測試

```bash
python -m pytest tests/
```

## 🤝 貢獻指南

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 本倉庫
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'feat: 新增某個 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 開源協議

本專案採用 MIT 協議 - 詳情請參見 [LICENSE](LICENSE) 檔案。
