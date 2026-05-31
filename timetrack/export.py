"""
Export functionality for TimeTrack CLI.

Supports exporting data to CSV and JSON formats.
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class Exporter:
    """Handles data export to various formats."""

    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filepath: str, fieldnames: List[str] = None) -> str:
        """Export data to CSV file.

        Args:
            data: List of dictionaries to export
            filepath: Output file path
            fieldnames: Column names (auto-detected if not provided)

        Returns:
            Absolute path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        if fieldnames is None:
            fieldnames = list(data[0].keys())

        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return str(Path(filepath).absolute())

    @staticmethod
    def to_json(data: List[Dict[str, Any]], filepath: str, indent: int = 2) -> str:
        """Export data to JSON file.

        Args:
            data: List of dictionaries to export
            filepath: Output file path
            indent: JSON indentation level

        Returns:
            Absolute path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        # Convert datetime objects to strings
        def json_serial(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=json_serial, ensure_ascii=False)

        return str(Path(filepath).absolute())

    @staticmethod
    def format_time_entries_for_export(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format time entries for export with human-readable durations.

        Args:
            entries: Raw time entries from database

        Returns:
            Formatted entries with additional fields
        """
        formatted = []
        for entry in entries:
            formatted_entry = {
                'id': entry.get('id'),
                'project': entry.get('project_name', ''),
                'task': entry.get('task_name', ''),
                'start_time': entry.get('start_time', ''),
                'end_time': entry.get('end_time', ''),
                'duration_seconds': entry.get('duration', 0),
                'duration_formatted': format_duration(entry.get('duration', 0)),
                'notes': entry.get('notes', ''),
            }
            formatted.append(formatted_entry)
        return formatted

    @staticmethod
    def format_project_stats_for_export(stats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format project statistics for export.

        Args:
            stats: Raw project statistics from database

        Returns:
            Formatted statistics with additional fields
        """
        formatted = []
        for stat in stats:
            formatted_stat = {
                'project_id': stat.get('id'),
                'project_name': stat.get('name', ''),
                'task_count': stat.get('task_count', 0),
                'entry_count': stat.get('entry_count', 0),
                'total_seconds': stat.get('total_seconds', 0),
                'total_time_formatted': format_duration(stat.get('total_seconds', 0)),
            }
            formatted.append(formatted_stat)
        return formatted


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds is None or seconds < 0:
        return "0s"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)
