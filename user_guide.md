# LogIt User Guide ⏱️

Welcome to **LogIt**, your terminal-first time tracking companion. This guide explains how to use the available commands to track your productivity efficiently.

---

## 🚀 Commands Overview

### 1. `logit start`
Use this command to begin tracking a new activity.

**Usage:**
```bash
logit start "Project Name" [OPTIONS]
```

**Options:**
- `-t, --task TEXT`: Add a specific description of what you are working on.
- `-g, --tag TEXT`: Add one or more tags to categorize the session. You can use this multiple times.

**Examples:**
```bash
# Basic start
logit start "Website Redesign"

# Start with a task and tags
logit start "Client-X" --task "Homepage Layout" -g design -g "v1"
```

---

### 2. `logit stop`
Ends a currently running activity. By default, LogIt uses **FIFO (First-In, First-Out)** logic, meaning it will stop the oldest activity you started that is still running.

**Usage:**
```bash
logit stop [PROJECT] [OPTIONS]
```

**Optional Filtering:**
- **`PROJECT`**: Provide a project name to stop the oldest running session for that specific project.
- `-t, --task TEXT`: Target a specific task description to stop.

**Examples:**
```bash
# Stop the oldest active activity
logit stop

# Stop the oldest activity for "Project Name"
logit stop "Project Name"

# Stop a specific task
logit stop -t "Homepage Layout"
```

**What happens when you stop?**
LogIt will display a summary of the session:
- **Project & Task** details
- **Tags** used
- **Start & End** timestamps
- **Total Duration** (formatted as `Xh YYm`)

---

### 3. `logit report`
Generate a project-centric summary of your tracked time.

**Usage:**
```bash
logit report [OPTIONS]
```

**Options:**
- `-d, --days INTEGER`: Number of days to include in the report (default: 1).
- `--json`: Output report in JSON format.

**Examples:**
```bash
# Today's report
logit report

# Last 7 days
logit report --days 7
```

**Output Format:**
The report groups entries by project and lists tasks with their specific intervals and durations:

```text
📊 Time Tracking Report
========================

📁 Project-A: 2h 30m
   01. [2026-02-08] 09:00 - 11:00 (2h 00m) | design
   02. [2026-02-08] 14:00 - 14:30 (0h 30m) | refactor

📁 Project-B: 1h 00m
   01. [2026-02-08] 11:30 - Present (1h 00m) | coding

⏱️  Total: 3h 30m
```

---

### 4. `logit analyze`
Take a deep dive into your productivity patterns.

**Usage:**
```bash
logit analyze [OPTIONS]
```

**Options:**
- `-d, --days INTEGER`: Number of days to analyze (default: 7).
- `--json`: Output analysis in JSON format.

**What's inside?**
- **Deep Work Score**: Percentage of time spent in focused sessions ($\ge$ 45 min).
- **Average Session**: Your median session length.
- **Context Switching**: Average number of unique projects you switch between per day.
- **Session Distribution**: A visual bar chart showing your work intensity:
    - **Fragmented**: Short bursts or interruptions (<15m).
    - **Flow**: Solid blocks of consistent work (15m-1h).
    - **Deep Focus**: High-intensity long sessions (>1h).

**Example Output:**
```text
🧠 Productivity Analysis
══════════════════════════════════════════════════

Focus Quality
Deep Work Score:                    95.2%
██████████████████████████████████████░░
Avg Session:                    1h 12m
Context Switching:                2.7 projects/day

Session Distribution
Fragmented (<15m)  ████ 3
Flow (15m-1h)      ███████████ 8
Deep Focus (>1h)   ██████████████████████████████ 21
```

---

### 5. `logit --help`
Need a quick reminder? You can always use the help flag to see available commands and options directly in your terminal.

```bash
logit --help
# Or for a specific command
logit start --help
```

---

## � Where is my data?
Everything is stored locally on your machine in a human-readable format at:
`~/.logit_data.jsonl`
