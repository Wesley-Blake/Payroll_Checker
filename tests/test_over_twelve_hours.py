from pathlib import Path
import pytest
from helpers.over_twelve_hours import over_twleve_hours

class TestOverTwelveHours:
    def test_over_twelve_hours_with_invalid_paths(self):
        result = over_twleve_hours(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_over_twelve_hours_returns_dict(self):
        result = over_twleve_hours(
            Path("tests\\data_examples\\hours-breakdown.csv"),
            Path("tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_over_twelve_hours_with_missing_file(self):
        result = over_twleve_hours(
            Path("tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}
