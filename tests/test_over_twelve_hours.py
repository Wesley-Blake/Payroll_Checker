from pathlib import Path
import pytest
from helpers.over_twelve_hours import over_twleve_hours

class TestOverTwelveHours:
    def test_over_twelve_hours_with_invalid_paths(self):
        """Test that invalid paths return empty dict"""
        result = over_twleve_hours(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_over_twelve_hours_returns_dict(self):
        """Test that valid files return a dict"""
        result = over_twleve_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_over_twelve_hours_with_missing_file(self):
        """Test that missing email file returns empty dict"""
        result = over_twleve_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}

    def test_over_twelve_hours_with_non_path_input(self):
        """Test that non-Path inputs return empty dict"""
        result = over_twleve_hours("not_a_path", Path("test.csv"))
        assert result == {}
