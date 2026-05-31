"""Tests for utils module."""

import unittest
from timetrack.utils import (
    format_duration, format_duration_short, parse_date,
    get_relative_date, calculate_duration
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def test_format_duration(self):
        """Test duration formatting."""
        self.assertEqual(format_duration(0), "0s")
        self.assertEqual(format_duration(30), "30s")
        self.assertEqual(format_duration(60), "1m")
        self.assertEqual(format_duration(90), "1m 30s")
        self.assertEqual(format_duration(3600), "1h")
        self.assertEqual(format_duration(3661), "1h 1m 1s")

    def test_format_duration_short(self):
        """Test short duration formatting."""
        self.assertEqual(format_duration_short(0), "00:00:00")
        self.assertEqual(format_duration_short(3661), "01:01:01")
        self.assertEqual(format_duration_short(3600), "01:00:00")

    def test_parse_date(self):
        """Test date parsing."""
        self.assertEqual(parse_date("2024-01-15"), "2024-01-15")
        self.assertEqual(parse_date("2024/01/15"), "2024-01-15")
        self.assertEqual(parse_date("15-01-2024"), "2024-01-15")
        self.assertIsNone(parse_date("invalid"))

    def test_get_relative_date(self):
        """Test relative date parsing."""
        today = get_relative_date("today")
        self.assertIsNotNone(today)

        yesterday = get_relative_date("yesterday")
        self.assertIsNotNone(yesterday)

        week = get_relative_date("week")
        self.assertIsNotNone(week)

    def test_calculate_duration(self):
        """Test duration calculation."""
        from datetime import datetime, timedelta
        now = datetime.now()
        past = now - timedelta(hours=1, minutes=30)

        duration = calculate_duration(past.isoformat())
        self.assertGreaterEqual(duration, 5400)  # At least 1.5 hours in seconds


if __name__ == '__main__':
    unittest.main()
