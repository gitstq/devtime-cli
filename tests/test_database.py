"""Tests for database module."""

import unittest
import os
import tempfile
from timetrack.database import Database


class TestDatabase(unittest.TestCase):
    """Test cases for Database class."""

    def setUp(self):
        """Set up test database."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_file.close()
        self.db = Database(self.temp_file.name)

    def tearDown(self):
        """Clean up test database."""
        os.unlink(self.temp_file.name)

    def test_create_project(self):
        """Test project creation."""
        project_id = self.db.create_project("Test Project", "Test Description")
        self.assertIsNotNone(project_id)
        self.assertIsInstance(project_id, int)

        project = self.db.get_project(project_id)
        self.assertEqual(project['name'], "Test Project")
        self.assertEqual(project['description'], "Test Description")

    def test_create_duplicate_project(self):
        """Test creating duplicate project fails."""
        self.db.create_project("Test Project")
        with self.assertRaises(Exception):
            self.db.create_project("Test Project")

    def test_create_task(self):
        """Test task creation."""
        project_id = self.db.create_project("Test Project")
        task_id = self.db.create_task(project_id, "Test Task", "Test Description")

        task = self.db.get_task(task_id)
        self.assertEqual(task['name'], "Test Task")
        self.assertEqual(task['project_id'], project_id)

    def test_timer_operations(self):
        """Test timer start/stop operations."""
        project_id = self.db.create_project("Test Project")
        task_id = self.db.create_task(project_id, "Test Task")

        # Start timer
        entry_id = self.db.start_timer(task_id, "Test notes")
        self.assertIsNotNone(entry_id)

        # Check running timer
        running = self.db.get_running_timer()
        self.assertIsNotNone(running)
        self.assertEqual(running['task_id'], task_id)

        # Stop timer
        entry = self.db.stop_timer(entry_id)
        self.assertIsNotNone(entry)
        self.assertIsNotNone(entry['end_time'])
        self.assertIsNotNone(entry['duration'])

        # Check no running timer
        running = self.db.get_running_timer()
        self.assertIsNone(running)

    def test_list_projects(self):
        """Test listing projects."""
        self.db.create_project("Project 1")
        self.db.create_project("Project 2")

        projects = self.db.list_projects()
        self.assertEqual(len(projects), 2)

    def test_delete_project(self):
        """Test project deletion."""
        project_id = self.db.create_project("Test Project")
        result = self.db.delete_project(project_id)
        self.assertTrue(result)

        project = self.db.get_project(project_id)
        self.assertIsNone(project)


if __name__ == '__main__':
    unittest.main()
