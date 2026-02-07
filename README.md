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

# See history (WIP)
logit report week
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
- **Local-First**: All data stays on your machine.
- **Terminal-Native**: Built for developers who live in the CLI.
- **Tagging Support**: Organize your entries with custom tags.
- **Reporting**: Generate daily, weekly, or monthly summaries.
- **Lightweight**: Zero fluff, just tracking.

---

## 🏗️ Architecture
```mermaid
.
├── README.md
├── logit
│   ├── __init__.py
│   └── cli.py
├── pyproject.toml
├── requirements.txt
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

### Track Activity
Start a new session with optional tags:
```bash
logit start "Refactoring UI" --tags frontend -t design
```

### Stop Session
End the current active session:
```bash
logit stop
```

### Generate Reports
View your logged time over different periods:
```bash
logit report day
logit report week
logit report month
```

---

## 🗺️ Roadmap
- [ ] Persistent storage (JSON / JSONL)
- [ ] `logit status` command
- [ ] Config file support (`~/.config/logit/`)
- [ ] Rich terminal output (tables, colors)
- [ ] Export to CSV / ICS
- [ ] Comprehensive test suite with `pytest`

---

## 🧠 Philosophy
- **Local-first**: Your data is yours. No cloud, no sync, no accounts.
- **Plain files**: Human-readable storage (Planned).
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
