"""
Command-line interface for TimeTrack CLI.

Main entry point for the application.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from typing import Optional

from .database import Database
from .utils import (
    format_duration, format_duration_short, format_datetime,
    format_date, parse_date, get_relative_date, truncate_string
)
from .export import Exporter

console = Console()

# Custom context object
class Context:
    def __init__(self):
        self.db = Database()

pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.version_option(version="1.0.0", prog_name="timetrack")
@click.pass_context
def cli(ctx):
    """TimeTrack CLI - A powerful command-line time tracking tool for developers.

    Track time spent on projects and tasks with ease.

    Examples:
        timetrack project create "My Project" --description "A cool project"
        timetrack task create "My Project" "Feature X"
        timetrack start "My Project" "Feature X"
        timetrack stop
        timetrack status
        timetrack report
    """
    ctx.obj = Context()


# Project commands
@cli.group()
def project():
    """Manage projects."""
    pass


@project.command(name="create")
@click.argument("name")
@click.option("--description", "-d", default="", help="Project description")
@pass_context
def project_create(ctx, name: str, description: str):
    """Create a new project."""
    try:
        project_id = ctx.db.create_project(name, description)
        console.print(f"✅ [green]Project '[bold]{name}[/bold]' created successfully (ID: {project_id})[/green]")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            console.print(f"❌ [red]Project '[bold]{name}[/bold]' already exists[/red]")
        else:
            console.print(f"❌ [red]Error: {e}[/red]")


@project.command(name="list")
@pass_context
def project_list(ctx):
    """List all projects."""
    projects = ctx.db.list_projects()

    if not projects:
        console.print("📭 [yellow]No projects found. Create one with: timetrack project create <name>[/yellow]")
        return

    table = Table(title="📁 Projects", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", min_width=20)
    table.add_column("Description", min_width=30)
    table.add_column("Created", style="dim")

    for proj in projects:
        table.add_row(
            str(proj['id']),
            proj['name'],
            truncate_string(proj.get('description', ''), 40),
            format_date(proj['created_at'])
        )

    console.print(table)


@project.command(name="delete")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete this project?")
@pass_context
def project_delete(ctx, name: str):
    """Delete a project and all its data."""
    proj = ctx.db.get_project_by_name(name)
    if not proj:
        console.print(f"❌ [red]Project '[bold]{name}[/bold]' not found[/red]")
        return

    if ctx.db.delete_project(proj['id']):
        console.print(f"✅ [green]Project '[bold]{name}[/bold]' deleted successfully[/green]")
    else:
        console.print(f"❌ [red]Failed to delete project '[bold]{name}[/bold]'[/red]")


# Task commands
@cli.group()
def task():
    """Manage tasks."""
    pass


@task.command(name="create")
@click.argument("project_name")
@click.argument("task_name")
@click.option("--description", "-d", default="", help="Task description")
@pass_context
def task_create(ctx, project_name: str, task_name: str, description: str):
    """Create a new task in a project."""
    proj = ctx.db.get_project_by_name(project_name)
    if not proj:
        console.print(f"❌ [red]Project '[bold]{project_name}[/bold]' not found[/red]")
        return

    try:
        task_id = ctx.db.create_task(proj['id'], task_name, description)
        console.print(f"✅ [green]Task '[bold]{task_name}[/bold]' created in project '[bold]{project_name}[/bold]' (ID: {task_id})[/green]")
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")


@task.command(name="list")
@click.argument("project_name", required=False)
@pass_context
def task_list(ctx, project_name: Optional[str]):
    """List tasks. Optionally filter by project."""
    project_id = None
    if project_name:
        proj = ctx.db.get_project_by_name(project_name)
        if not proj:
            console.print(f"❌ [red]Project '[bold]{project_name}[/bold]' not found[/red]")
            return
        project_id = proj['id']

    tasks = ctx.db.list_tasks(project_id)

    if not tasks:
        console.print("📭 [yellow]No tasks found.[/yellow]")
        return

    table = Table(title="📋 Tasks", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Project", style="blue")
    table.add_column("Task", min_width=20)
    table.add_column("Description", min_width=30)

    for t in tasks:
        proj = ctx.db.get_project(t['project_id'])
        table.add_row(
            str(t['id']),
            proj['name'] if proj else "Unknown",
            t['name'],
            truncate_string(t.get('description', ''), 40)
        )

    console.print(table)


@task.command(name="delete")
@click.argument("project_name")
@click.argument("task_name")
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
@pass_context
def task_delete(ctx, project_name: str, task_name: str):
    """Delete a task and all its time entries."""
    proj = ctx.db.get_project_by_name(project_name)
    if not proj:
        console.print(f"❌ [red]Project '[bold]{project_name}[/bold]' not found[/red]")
        return

    t = ctx.db.get_task_by_name(proj['id'], task_name)
    if not t:
        console.print(f"❌ [red]Task '[bold]{task_name}[/bold]' not found in project '[bold]{project_name}[/bold]'[/red]")
        return

    if ctx.db.delete_task(t['id']):
        console.print(f"✅ [green]Task '[bold]{task_name}[/bold]' deleted successfully[/green]")
    else:
        console.print(f"❌ [red]Failed to delete task '[bold]{task_name}[/bold]'[/red]")


# Timer commands
@cli.command()
@click.argument("project_name")
@click.argument("task_name")
@click.option("--notes", "-n", default="", help="Notes for this time entry")
@pass_context
def start(ctx, project_name: str, task_name: str, notes: str):
    """Start tracking time for a task."""
    # Check if there's already a running timer
    running = ctx.db.get_running_timer()
    if running:
        console.print(f"⚠️  [yellow]Timer already running for '[bold]{running['task_name']}[/bold]' in '[bold]{running['project_name']}[/bold]'[/yellow]")
        console.print(f"   Started at: {format_datetime(running['start_time'])}")
        console.print(f"   Run 'timetrack stop' first to start a new timer.")
        return

    proj = ctx.db.get_project_by_name(project_name)
    if not proj:
        console.print(f"❌ [red]Project '[bold]{project_name}[/bold]' not found[/red]")
        console.print(f"   Create it first with: timetrack project create \"{project_name}\"")
        return

    t = ctx.db.get_task_by_name(proj['id'], task_name)
    if not t:
        console.print(f"❌ [red]Task '[bold]{task_name}[/bold]' not found in project '[bold]{project_name}[/bold]'[/red]")
        console.print(f"   Create it first with: timetrack task create \"{project_name}\" \"{task_name}\"")
        return

    entry_id = ctx.db.start_timer(t['id'], notes)
    console.print(f"⏱️  [green]Timer started for '[bold]{task_name}[/bold]' in '[bold]{project_name}[/bold]'[/green]")
    if notes:
        console.print(f"   Notes: {notes}")


@cli.command()
@pass_context
def stop(ctx):
    """Stop the running timer."""
    running = ctx.db.get_running_timer()
    if not running:
        console.print("📭 [yellow]No timer is currently running[/yellow]")
        return

    entry = ctx.db.stop_timer(running['id'])
    if entry:
        duration = entry.get('duration', 0)
        console.print(f"⏹️  [green]Timer stopped for '[bold]{running['task_name']}[/bold]'[/green]")
        console.print(f"   Duration: [bold]{format_duration(duration)}[/bold]")
        console.print(f"   Started: {format_datetime(entry['start_time'])}")
        console.print(f"   Ended: {format_datetime(entry['end_time'])}")
    else:
        console.print("❌ [red]Failed to stop timer[/red]")


@cli.command()
@pass_context
def status(ctx):
    """Show current timer status."""
    running = ctx.db.get_running_timer()

    if not running:
        console.print("📭 [yellow]No timer is currently running[/yellow]")
        return

    duration = calculate_duration(running['start_time'])

    panel = Panel(
        f"[bold cyan]Project:[/bold cyan] {running['project_name']}\n"
        f"[bold cyan]Task:[/bold cyan] {running['task_name']}\n"
        f"[bold cyan]Started:[/bold cyan] {format_datetime(running['start_time'])}\n"
        f"[bold cyan]Running for:[/bold cyan] [bold green]{format_duration(duration)}[/bold green]\n"
        f"[bold cyan]Notes:[/bold cyan] {running.get('notes', 'N/A')}",
        title="⏱️  Current Timer",
        border_style="green"
    )
    console.print(panel)


# Report commands
@cli.group()
def report():
    """Generate reports."""
    pass


@report.command(name="entries")
@click.option("--project", "-p", help="Filter by project name")
@click.option("--task", "-t", help="Filter by task name")
@click.option("--from", "from_date", help="Start date (YYYY-MM-DD)")
@click.option("--to", "to_date", help="End date (YYYY-MM-DD)")
@click.option("--limit", "-l", type=int, default=50, help="Maximum entries to show")
@pass_context
def report_entries(ctx, project: Optional[str], task: Optional[str], from_date: Optional[str], to_date: Optional[str], limit: int):
    """Show time entries."""
    project_id = None
    task_id = None

    if project:
        proj = ctx.db.get_project_by_name(project)
        if not proj:
            console.print(f"❌ [red]Project '[bold]{project}[/bold]' not found[/red]")
            return
        project_id = proj['id']

        if task:
            t = ctx.db.get_task_by_name(project_id, task)
            if not t:
                console.print(f"❌ [red]Task '[bold]{task}[/bold]' not found[/red]")
                return
            task_id = t['id']

    # Parse date filters
    if from_date:
        parsed = parse_date(from_date) or get_relative_date(from_date)
        if not parsed:
            console.print(f"❌ [red]Invalid date format: {from_date}[/red]")
            return
        from_date = parsed

    if to_date:
        parsed = parse_date(to_date) or get_relative_date(to_date)
        if not parsed:
            console.print(f"❌ [red]Invalid date format: {to_date}[/red]")
            return
        to_date = parsed

    entries = ctx.db.list_time_entries(task_id, project_id, from_date, to_date, limit)

    if not entries:
        console.print("📭 [yellow]No time entries found.[/yellow]")
        return

    table = Table(title="📊 Time Entries", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Project", style="blue")
    table.add_column("Task")
    table.add_column("Start", style="dim")
    table.add_column("End", style="dim")
    table.add_column("Duration", justify="right", style="green")
    table.add_column("Notes", style="dim")

    total_seconds = 0
    for entry in entries:
        duration = entry.get('duration', 0) or 0
        total_seconds += duration

        table.add_row(
            str(entry['id']),
            entry.get('project_name', ''),
            entry.get('task_name', ''),
            format_datetime(entry['start_time']),
            format_datetime(entry['end_time']) if entry.get('end_time') else "[yellow]Running...[/yellow]",
            format_duration(duration) if entry.get('end_time') else "-",
            truncate_string(entry.get('notes', ''), 20)
        )

    console.print(table)
    console.print(f"\n[bold]Total Duration:[/bold] [green]{format_duration(total_seconds)}[/green]")


@report.command(name="projects")
@pass_context
def report_projects(ctx):
    """Show time statistics by project."""
    stats = ctx.db.get_project_stats()

    if not stats:
        console.print("📭 [yellow]No data found. Start tracking time first![/yellow]")
        return

    table = Table(title="📈 Project Statistics", show_header=True, header_style="bold cyan")
    table.add_column("Project", style="blue")
    table.add_column("Tasks", justify="right")
    table.add_column("Entries", justify="right")
    table.add_column("Total Time", justify="right", style="green")

    total_seconds = 0
    for stat in stats:
        total_seconds += stat.get('total_seconds', 0)
        table.add_row(
            stat['name'],
            str(stat.get('task_count', 0)),
            str(stat.get('entry_count', 0)),
            format_duration(stat.get('total_seconds', 0))
        )

    console.print(table)
    console.print(f"\n[bold]Total Time Across All Projects:[/bold] [green]{format_duration(total_seconds)}[/green]")


@report.command(name="tasks")
@click.argument("project_name", required=False)
@pass_context
def report_tasks(ctx, project_name: Optional[str]):
    """Show time statistics by task."""
    project_id = None
    if project_name:
        proj = ctx.db.get_project_by_name(project_name)
        if not proj:
            console.print(f"❌ [red]Project '[bold]{project_name}[/bold]' not found[/red]")
            return
        project_id = proj['id']

    stats = ctx.db.get_task_stats(project_id)

    if not stats:
        console.print("📭 [yellow]No data found. Start tracking time first![/yellow]")
        return

    table = Table(title="📈 Task Statistics", show_header=True, header_style="bold cyan")
    table.add_column("Project", style="blue")
    table.add_column("Task")
    table.add_column("Entries", justify="right")
    table.add_column("Total Time", justify="right", style="green")

    total_seconds = 0
    for stat in stats:
        total_seconds += stat.get('total_seconds', 0)
        table.add_row(
            stat.get('project_name', ''),
            stat['name'],
            str(stat.get('entry_count', 0)),
            format_duration(stat.get('total_seconds', 0))
        )

    console.print(table)
    console.print(f"\n[bold]Total Time:[/bold] [green]{format_duration(total_seconds)}[/green]")


@report.command(name="daily")
@click.option("--days", "-d", type=int, default=14, help="Number of days to show")
@pass_context
def report_daily(ctx, days: int):
    """Show daily time statistics."""
    stats = ctx.db.get_daily_stats(days)

    if not stats:
        console.print("📭 [yellow]No data found. Start tracking time first![/yellow]")
        return

    table = Table(title=f"📅 Daily Statistics (Last {days} Days)", show_header=True, header_style="bold cyan")
    table.add_column("Date", style="blue")
    table.add_column("Entries", justify="right")
    table.add_column("Total Time", justify="right", style="green")

    total_seconds = 0
    for stat in stats:
        total_seconds += stat.get('total_seconds', 0)
        table.add_row(
            stat['date'],
            str(stat.get('entry_count', 0)),
            format_duration(stat.get('total_seconds', 0))
        )

    console.print(table)
    console.print(f"\n[bold]Total Time:[/bold] [green]{format_duration(total_seconds)}[/green]")


# Export commands
@cli.group()
def export():
    """Export data."""
    pass


@export.command(name="csv")
@click.argument("filepath")
@click.option("--project", "-p", help="Filter by project name")
@click.option("--from", "from_date", help="Start date (YYYY-MM-DD)")
@click.option("--to", "to_date", help="End date (YYYY-MM-DD)")
@pass_context
def export_csv(ctx, filepath: str, project: Optional[str], from_date: Optional[str], to_date: Optional[str]):
    """Export time entries to CSV."""
    project_id = None

    if project:
        proj = ctx.db.get_project_by_name(project)
        if not proj:
            console.print(f"❌ [red]Project '[bold]{project}[/bold]' not found[/red]")
            return
        project_id = proj['id']

    if from_date:
        parsed = parse_date(from_date) or get_relative_date(from_date)
        if parsed:
            from_date = parsed

    if to_date:
        parsed = parse_date(to_date) or get_relative_date(to_date)
        if parsed:
            to_date = parsed

    entries = ctx.db.list_time_entries(None, project_id, from_date, to_date)

    if not entries:
        console.print("📭 [yellow]No data to export.[/yellow]")
        return

    formatted = Exporter.format_time_entries_for_export(entries)

    try:
        exported_path = Exporter.to_csv(formatted, filepath)
        console.print(f"✅ [green]Exported {len(entries)} entries to: [bold]{exported_path}[/bold][/green]")
    except Exception as e:
        console.print(f"❌ [red]Export failed: {e}[/red]")


@export.command(name="json")
@click.argument("filepath")
@click.option("--project", "-p", help="Filter by project name")
@click.option("--from", "from_date", help="Start date (YYYY-MM-DD)")
@click.option("--to", "to_date", help="End date (YYYY-MM-DD)")
@pass_context
def export_json(ctx, filepath: str, project: Optional[str], from_date: Optional[str], to_date: Optional[str]):
    """Export time entries to JSON."""
    project_id = None

    if project:
        proj = ctx.db.get_project_by_name(project)
        if not proj:
            console.print(f"❌ [red]Project '[bold]{project}[/bold]' not found[/red]")
            return
        project_id = proj['id']

    if from_date:
        parsed = parse_date(from_date) or get_relative_date(from_date)
        if parsed:
            from_date = parsed

    if to_date:
        parsed = parse_date(to_date) or get_relative_date(to_date)
        if parsed:
            to_date = parsed

    entries = ctx.db.list_time_entries(None, project_id, from_date, to_date)

    if not entries:
        console.print("📭 [yellow]No data to export.[/yellow]")
        return

    formatted = Exporter.format_time_entries_for_export(entries)

    try:
        exported_path = Exporter.to_json(formatted, filepath)
        console.print(f"✅ [green]Exported {len(entries)} entries to: [bold]{exported_path}[/bold][/green]")
    except Exception as e:
        console.print(f"❌ [red]Export failed: {e}[/red]")


# Helper function
def calculate_duration(start_time: str) -> int:
    """Calculate duration from start time to now."""
    try:
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        return int((datetime.now() - start).total_seconds())
    except (ValueError, AttributeError):
        return 0


# Main entry point
def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
