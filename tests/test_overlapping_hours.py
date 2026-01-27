from pathlib import Path
import pytest
from helpers.overlapping_hours import overlapping_hours


class TestOverlappingHours:
    def test_overlapping_hours_with_invalid_path(self):
        result = overlapping_hours(Path("nonexistent.csv"))
        assert result == {}

    def test_overlapping_hours_returns_dict(self):
        result = overlapping_hours(Path("data_examples/overlapping_hours.csv"))
        assert isinstance(result, dict)

    def test_overlapping_hours_with_string_path(self):
        result = overlapping_hours("")
        assert result == {}
