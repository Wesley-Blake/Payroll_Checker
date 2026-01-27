from pathlib import Path
import pytest
from helpers.over_eight_hours import over_eight_hours


class TestOverEightHours:
    def test_over_eight_hours_with_invalid_paths(self):
        result = over_eight_hours(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_over_eight_hours_returns_dict(self):
        result = over_eight_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_over_eight_hours_with_missing_file(self):
        result = over_eight_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}
