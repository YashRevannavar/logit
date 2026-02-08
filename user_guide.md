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
- **Total Duration** (formatted as `HH:MM:SS`)

---

### 3. `logit report`
Generate a summary of your tracked time over a specific period. *(Note: Reports are currently a work in progress).*

**Usage:**
```bash
logit report [day|week|month]
```

**Examples:**
```bash
logit report day
logit report week
```

---

### 4. `logit --help`
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
