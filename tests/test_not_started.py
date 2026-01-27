from pathlib import Path
import pytest
from helpers.not_started import not_started_list


class TestNotStarted:
    def test_not_started_list_with_invalid_path(self):
        result = not_started_list(Path("nonexistent.csv"))
        assert result == {}

    def test_not_started_list_returns_dict(self):
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        assert isinstance(result, dict)

    def test_not_started_list_with_string_path(self):
        result = not_started_list("")
        assert result == {}