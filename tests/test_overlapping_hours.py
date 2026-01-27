from pathlib import Path
import pytest
from helpers.overlapping_hours import overlapping_hours


class TestOverlappingHours:
    def test_overlapping_hours_with_invalid_path(self):
        result = overlapping_hours(Path("nonexistent.csv"))
        assert result == {}

    def test_overlapping_hours_returns_dict(self):
        result = overlapping_hours(Path("Payroll-Checker\\tests\\data_examples\\overlapping_hours.csv"))
        assert isinstance(result, dict)
        assert result == {'manager1@mail.com': ['1@mail.com'], 'manager2@mail.com': ['2@mail.com']}

    def test_overlapping_hours_with_string_path(self):
        result = overlapping_hours("")
        assert result == {}
