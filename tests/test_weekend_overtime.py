from pathlib import Path
import pytest
from helpers.weekend_overtime import weekend_overtime

class TestWeekendOvertime:
    """Test cases for weekend_overtime function"""

    def test_weekend_overtime_with_invalid_paths(self):
        """Test that invalid paths return empty dict"""
        result = weekend_overtime(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_weekend_overtime_returns_dict(self):
        """Test that valid files return a dict"""
        result = weekend_overtime(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_weekend_overtime_with_missing_email_file(self):
        """Test that missing email file returns empty dict"""
        result = weekend_overtime(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}