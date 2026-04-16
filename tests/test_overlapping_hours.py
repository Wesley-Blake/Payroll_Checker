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

    def test_overlapping_hours_filters_white_list(self, tmp_path):
        """Test that earn_codes in white list are filtered out"""
        csv_file = tmp_path / "test_filter.csv"
        csv_content = "earn_code,Empl_Email,Appr_Email\nREG,emp1@mail.com,mgr@mail.com\nOT,emp2@mail.com,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = overlapping_hours(csv_file)
        # Only OT should remain, REG filtered
        assert "mgr@mail.com" in result
        assert result["mgr@mail.com"] == ["emp2@mail.com"]

    def test_overlapping_hours_groups_by_manager(self, tmp_path):
        """Test that employees are grouped by manager"""
        csv_file = tmp_path / "test_group.csv"
        csv_content = "earn_code,Empl_Email,Appr_Email\nOT,emp1@mail.com,mgr1@mail.com\nVAC,emp2@mail.com,mgr1@mail.com\nOT,emp3@mail.com,mgr2@mail.com\n"
        csv_file.write_text(csv_content)
        result = overlapping_hours(csv_file)
        assert len(result) == 2
        assert "mgr1@mail.com" in result
        assert "mgr2@mail.com" in result
        assert set(result["mgr1@mail.com"]) == {"emp1@mail.com", "emp2@mail.com"}
        assert result["mgr2@mail.com"] == ["emp3@mail.com"]

    def test_overlapping_hours_invalid_manager_email(self, tmp_path):
        """Test that invalid manager email returns empty dict"""
        csv_file = tmp_path / "test_invalid_mgr.csv"
        csv_content = "earn_code,Empl_Email,Appr_Email\nOT,emp1@mail.com,not_email\n"
        csv_file.write_text(csv_content)
        result = overlapping_hours(csv_file)
        assert result == {}

    def test_overlapping_hours_invalid_employee_email(self, tmp_path):
        """Test that invalid employee email returns empty dict"""
        csv_file = tmp_path / "test_invalid_emp.csv"
        csv_content = "earn_code,Empl_Email,Appr_Email\nOT,not_email,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = overlapping_hours(csv_file)
        assert result == {}

    def test_overlapping_hours_empty_after_filter(self, tmp_path):
        """Test that empty df after filtering returns empty dict"""
        csv_file = tmp_path / "test_empty.csv"
        csv_content = "earn_code,Empl_Email,Appr_Email\nREG,emp1@mail.com,mgr@mail.com\nSHF,emp2@mail.com,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = overlapping_hours(csv_file)
        assert result == {}
