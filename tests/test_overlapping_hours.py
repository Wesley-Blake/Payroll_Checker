from pathlib import Path
import pytest
from helpers.overlapping_hours import overlapping_hours


class TestOverlappingHours:
    """Test cases for overlapping_hours function"""

    def test_overlapping_hours_with_invalid_path(self):
        """Test that invalid path returns empty dict"""
        result = overlapping_hours(Path("nonexistent.csv"))
        assert result == {}

    def test_overlapping_hours_returns_dict(self):
        """Test that valid file returns a dict"""
        result = overlapping_hours(Path("Payroll-Checker\\tests\\data_examples\\overlapping_hours.csv"))
        assert isinstance(result, dict)

    def test_overlapping_hours_with_string_path(self):
        """Test that string path returns empty dict"""
        result = overlapping_hours("")
        assert result == {}
