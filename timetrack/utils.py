"""
Utility functions for TimeTrack CLI.
"""

from datetime import datetime, timedelta
from typing import Optional


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "2h 30m 15s"
    """
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


def format_duration_short(seconds: int) -> str:
    """Format duration in seconds to short string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "02:30:15"
    """
    if seconds is None or seconds < 0:
        return "00:00:00"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_datetime(dt_str: str) -> str:
    """Format datetime string to human-readable format.

    Args:
        dt_str: Datetime string from database

    Returns:
        Formatted string like "2024-01-15 14:30"
    """
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return dt_str


def format_date(dt_str: str) -> str:
    """Format date string to human-readable format.

    Args:
        dt_str: Date string from database

    Returns:
        Formatted string like "2024-01-15"
    """
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return dt_str


def parse_date(date_str: str) -> Optional[str]:
    """Parse date string to ISO format.

    Args:
        date_str: Date string in various formats

    Returns:
        ISO format date string or None if invalid
    """
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def get_relative_date(relative: str) -> Optional[str]:
    """Get relative date string.

    Args:
        relative: Relative date string like "today", "yesterday", "week"

    Returns:
        ISO format date string or None
    """
    today = datetime.now().date()

    if relative.lower() in ('today', 't'):
        return today.isoformat()
    elif relative.lower() in ('yesterday', 'y'):
        return (today - timedelta(days=1)).isoformat()
    elif relative.lower() in ('week', 'w'):
        return (today - timedelta(days=7)).isoformat()
    elif relative.lower() in ('month', 'm'):
        return (today - timedelta(days=30)).isoformat()

    return None


def calculate_duration(start_time: str, end_time: Optional[str] = None) -> int:
    """Calculate duration between two timestamps.

    Args:
        start_time: Start timestamp
        end_time: End timestamp (defaults to now)

    Returns:
        Duration in seconds
    """
    try:
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))

        if end_time:
            end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        else:
            end = datetime.now()

        return int((end - start).total_seconds())
    except (ValueError, AttributeError):
        return 0


def truncate_string(s: str, max_length: int = 50) -> str:
    """Truncate string to maximum length.

    Args:
        s: Input string
        max_length: Maximum length

    Returns:
        Truncated string with ellipsis if needed
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."
