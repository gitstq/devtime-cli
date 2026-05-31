# TimeTrack CLI

A powerful command-line time tracking tool for developers.

TimeTrack CLI helps you track time spent on projects and tasks directly from your terminal. It's lightweight, fast, and designed specifically for developers who want to stay productive without leaving their command line.

## Features

- 📁 **Project Management**: Organize your work into projects
- 📋 **Task Tracking**: Track time for individual tasks within projects
- ⏱️ **Simple Timer**: Start and stop timers with simple commands
- 📊 **Rich Reports**: View detailed statistics and reports
- 📤 **Export Data**: Export your time entries to CSV or JSON
- 💾 **Local Storage**: All data stored locally in SQLite database
- 🎨 **Beautiful UI**: Rich terminal output with colors and tables

## Installation

```bash
pip install timetrack-cli
```

Or install from source:

```bash
git clone https://github.com/yourusername/timetrack-cli.git
cd timetrack-cli
pip install -e .
```

## Quick Start

```bash
# Create a project
timetrack project create "My Project" --description "A cool project"

# Create a task
timetrack task create "My Project" "Feature X"

# Start tracking time
timetrack start "My Project" "Feature X"

# Check status
timetrack status

# Stop tracking
timetrack stop

# View reports
timetrack report entries
timetrack report projects
timetrack report tasks
```

## Commands

### Project Commands

- `timetrack project create <name>` - Create a new project
- `timetrack project list` - List all projects
- `timetrack project delete <name>` - Delete a project

### Task Commands

- `timetrack task create <project> <name>` - Create a new task
- `timetrack task list [project]` - List tasks
- `timetrack task delete <project> <name>` - Delete a task

### Timer Commands

- `timetrack start <project> <task>` - Start tracking time
- `timetrack stop` - Stop the current timer
- `timetrack status` - Show current timer status

### Report Commands

- `timetrack report entries` - Show time entries
- `timetrack report projects` - Show project statistics
- `timetrack report tasks` - Show task statistics
- `timetrack report daily` - Show daily statistics

### Export Commands

- `timetrack export csv <filepath>` - Export to CSV
- `timetrack export json <filepath>` - Export to JSON

## License

MIT License
