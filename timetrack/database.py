"""
Database module for TimeTrack CLI.

Handles all database operations using SQLite.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


class Database:
    """SQLite database handler for TimeTrack."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Store in user's home directory
            home = Path.home()
            config_dir = home / ".timetrack"
            config_dir.mkdir(exist_ok=True)
            self.db_path = str(config_dir / "timetrack.db")
        else:
            self.db_path = db_path

        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_database(self):
        """Initialize database tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
                )
            """)

            # Time entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS time_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    duration INTEGER,  -- Duration in seconds
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
            """)

            # Create indexes for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_time_entries_task_id ON time_entries(task_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_time_entries_start_time ON time_entries(start_time)
            """)

            conn.commit()

    # Project operations
    def create_project(self, name: str, description: str = "") -> int:
        """Create a new project.

        Args:
            name: Project name
            description: Project description

        Returns:
            Project ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO projects (name, description) VALUES (?, ?)",
                (name, description)
            )
            conn.commit()
            return cursor.lastrowid

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_project_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get project by name."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE name = ?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def update_project(self, project_id: int, name: str = None, description: str = None) -> bool:
        """Update project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if not updates:
                return False

            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(project_id)

            cursor.execute(
                f"UPDATE projects SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_project(self, project_id: int) -> bool:
        """Delete project and all associated tasks and time entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            return cursor.rowcount > 0

    # Task operations
    def create_task(self, project_id: int, name: str, description: str = "") -> int:
        """Create a new task."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (project_id, name, description) VALUES (?, ?, ?)",
                (project_id, name, description)
            )
            conn.commit()
            return cursor.lastrowid

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get task by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_task_by_name(self, project_id: int, name: str) -> Optional[Dict[str, Any]]:
        """Get task by name within a project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE project_id = ? AND name = ?",
                (project_id, name)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_tasks(self, project_id: int = None) -> List[Dict[str, Any]]:
        """List all tasks, optionally filtered by project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if project_id:
                cursor.execute(
                    "SELECT * FROM tasks WHERE project_id = ? ORDER BY name",
                    (project_id,)
                )
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def update_task(self, task_id: int, name: str = None, description: str = None) -> bool:
        """Update task."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if not updates:
                return False

            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(task_id)

            cursor.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        """Delete task and all associated time entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    # Time entry operations
    def start_timer(self, task_id: int, notes: str = "") -> int:
        """Start a new time entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO time_entries (task_id, start_time, notes) VALUES (?, datetime('now'), ?)",
                (task_id, notes)
            )
            conn.commit()
            return cursor.lastrowid

    def stop_timer(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Stop a running time entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Calculate duration
            cursor.execute("""
                UPDATE time_entries
                SET end_time = datetime('now'),
                    duration = CAST((julianday('now') - julianday(start_time)) * 86400 AS INTEGER)
                WHERE id = ? AND end_time IS NULL
            """, (entry_id,))

            if cursor.rowcount == 0:
                return None

            cursor.execute("SELECT * FROM time_entries WHERE id = ?", (entry_id,))
            conn.commit()
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_running_timer(self) -> Optional[Dict[str, Any]]:
        """Get currently running time entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT te.*, t.name as task_name, t.project_id, p.name as project_name
                FROM time_entries te
                JOIN tasks t ON te.task_id = t.id
                JOIN projects p ON t.project_id = p.id
                WHERE te.end_time IS NULL
                ORDER BY te.start_time DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_time_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Get time entry by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM time_entries WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_time_entries(
        self,
        task_id: int = None,
        project_id: int = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """List time entries with optional filters."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            query = """
                SELECT te.*, t.name as task_name, p.name as project_name
                FROM time_entries te
                JOIN tasks t ON te.task_id = t.id
                JOIN projects p ON t.project_id = p.id
                WHERE 1=1
            """
            params = []

            if task_id:
                query += " AND te.task_id = ?"
                params.append(task_id)

            if project_id:
                query += " AND t.project_id = ?"
                params.append(project_id)

            if start_date:
                query += " AND date(te.start_time) >= date(?)"
                params.append(start_date)

            if end_date:
                query += " AND date(te.start_time) <= date(?)"
                params.append(end_date)

            query += " ORDER BY te.start_time DESC"

            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_time_entry(
        self,
        entry_id: int,
        start_time: str = None,
        end_time: str = None,
        notes: str = None
    ) -> bool:
        """Update time entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if start_time is not None:
                updates.append("start_time = ?")
                params.append(start_time)

            if end_time is not None:
                updates.append("end_time = ?")
                params.append(end_time)
                # Recalculate duration if end_time is set
                if start_time or end_time:
                    updates.append("duration = CAST((julianday(end_time) - julianday(start_time)) * 86400 AS INTEGER)")

            if notes is not None:
                updates.append("notes = ?")
                params.append(notes)

            if not updates:
                return False

            params.append(entry_id)

            cursor.execute(
                f"UPDATE time_entries SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_time_entry(self, entry_id: int) -> bool:
        """Delete time entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM time_entries WHERE id = ?", (entry_id,))
            conn.commit()
            return cursor.rowcount > 0

    # Statistics
    def get_project_stats(self, project_id: int = None) -> List[Dict[str, Any]]:
        """Get time statistics by project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if project_id:
                cursor.execute("""
                    SELECT
                        p.id,
                        p.name,
                        COUNT(DISTINCT te.id) as entry_count,
                        COUNT(DISTINCT t.id) as task_count,
                        COALESCE(SUM(te.duration), 0) as total_seconds
                    FROM projects p
                    LEFT JOIN tasks t ON p.id = t.project_id
                    LEFT JOIN time_entries te ON t.id = te.task_id AND te.end_time IS NOT NULL
                    WHERE p.id = ?
                    GROUP BY p.id
                """, (project_id,))
            else:
                cursor.execute("""
                    SELECT
                        p.id,
                        p.name,
                        COUNT(DISTINCT te.id) as entry_count,
                        COUNT(DISTINCT t.id) as task_count,
                        COALESCE(SUM(te.duration), 0) as total_seconds
                    FROM projects p
                    LEFT JOIN tasks t ON p.id = t.project_id
                    LEFT JOIN time_entries te ON t.id = te.task_id AND te.end_time IS NOT NULL
                    GROUP BY p.id
                    ORDER BY total_seconds DESC
                """)

            return [dict(row) for row in cursor.fetchall()]

    def get_task_stats(self, project_id: int = None) -> List[Dict[str, Any]]:
        """Get time statistics by task."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if project_id:
                cursor.execute("""
                    SELECT
                        t.id,
                        t.name,
                        p.name as project_name,
                        COUNT(te.id) as entry_count,
                        COALESCE(SUM(te.duration), 0) as total_seconds
                    FROM tasks t
                    JOIN projects p ON t.project_id = p.id
                    LEFT JOIN time_entries te ON t.id = te.task_id AND te.end_time IS NOT NULL
                    WHERE t.project_id = ?
                    GROUP BY t.id
                    ORDER BY total_seconds DESC
                """, (project_id,))
            else:
                cursor.execute("""
                    SELECT
                        t.id,
                        t.name,
                        p.name as project_name,
                        COUNT(te.id) as entry_count,
                        COALESCE(SUM(te.duration), 0) as total_seconds
                    FROM tasks t
                    JOIN projects p ON t.project_id = p.id
                    LEFT JOIN time_entries te ON t.id = te.task_id AND te.end_time IS NOT NULL
                    GROUP BY t.id
                    ORDER BY total_seconds DESC
                """)

            return [dict(row) for row in cursor.fetchall()]

    def get_daily_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get daily time statistics for the last N days."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    date(start_time) as date,
                    COUNT(*) as entry_count,
                    COALESCE(SUM(duration), 0) as total_seconds
                FROM time_entries
                WHERE end_time IS NOT NULL
                    AND date(start_time) >= date('now', ?)
                GROUP BY date(start_time)
                ORDER BY date(start_time) DESC
            """, (f'-{days} days',))

            return [dict(row) for row in cursor.fetchall()]
