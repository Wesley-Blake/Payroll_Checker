from pathlib import Path
import pytest
from helpers.pending_status import pending


class TestPendingStatus:
    def test_pending_with_invalid_path(self):
        result = pending(Path("nonexistent.csv"))
        assert result == []

    def test_pending_returns_list(self):
        result = pending(Path("data_examples/comments-status.csv"))
        assert isinstance(result, list)

    def test_pending_with_string_path(self):
        result = pending("")
        assert result == []
