# ⏱️ logit

**logit** is a terminal-first, open-source time tracking tool written in Python.
Designed to be simple, local-first, and developer-friendly.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start

If you just want to start tracking:

```bash
# Start tracking
logit start "coding" --tags canary

# Stop tracking
logit stop

# Generate report for today
logit report

# Deep productivity analysis (last 30 days)
logit analyze --days 30
```

---

## 📑 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Requirements](#-requirements)
- [Installation](#-installation)
    - [Global Installation (Recommended)](#global-installation-recommended)
    - [Development Setup](#development-setup)
- [Usage Guide](#-usage-guide)
- [Roadmap](#-roadmap)
- [Philosophy](#-philosophy)

---

## ✨ Features
- **Local-First**: All data stays on your machine (stored in `~/.logit_data.jsonl`).
- **Terminal-Native**: Built for developers who live in the CLI.
- **Tagging Support**: Organize your entries with custom tags.
- **Floating Duration**: Running activities show real-time duration in reports.
- **Visual Reports**: Project-centric summaries with tracked intervals and task details.
- **Productivity Analysis**: Insightful metrics like "Deep Work Score" and "Session Distribution."
- **Lightweight**: Zero fluff, just tracking.

---

## 🏗️ Architecture
```text
src/
└── logit/
    ├── cli.py                        # Entry point & Command registration
    ├── control_commands/             # Start/Stop logic
    │   ├── control_commands_helper.py
    │   └── control_commands_service.py
    ├── report_commands/              # Reporting logic
    │   ├── report_commands_helper.py
    │   └── report_commands_service.py
    ├── data_storage/                 # Persistence layer (JSONL)
    │   └── data_store.py
    ├── utilities/                    # Shared infrastructure
    │   ├── models.py                 # Dataclasses & Enums
    │   └── display_utils.py          # Color & Formatting helpers
    └── __init__.py
```

---

## 🛠️ Requirements
- **OS**: macOS or Linux
- **Python**: 3.10+
- **Tools**: pip, pipx (recommended)

---

## 📦 Installation

### Global Installation (Recommended)
To run `logit` from anywhere without affecting your system Python:

1. **Install pipx** (if not already installed):
   ```bash
   brew install pipx
   pipx ensurepath
   ```
2. **Install logit**:
   ```bash
   pipx install -e .
   ```

### Development Setup
If you want to contribute or modify the code:

1. **Clone & Enter**:
   ```bash
   git clone https://github.com/YashRevannavar/logit.git
   cd logit
   ```
2. **Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install Editable**:
   ```bash
   pip install -e .
   ```

---

## 📖 Usage Guide

> Refer to the [User Guide](user_guide.md) for detailed instructions on how to use the available commands.
---

## 🧠 Philosophy
- **Local-first**: Your data is yours. No cloud, no sync, no accounts.
- **Plain files**: Human-readable storage (JSONL).
- **Simplicity**: No complex UI, just simple commands.
- **Developer-focused**: Integration with your existing workflow.

---

## 🗑️ Uninstall

**Via pipx**:
```bash
pipx uninstall logit
```

**Via virtualenv**:
```bash
deactivate
rm -rf .venv
```

---

**Happy logging! ⏱️**
