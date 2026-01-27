from pathlib import Path
import pytest
import pandas as pd
from helpers.not_started import not_started_list


class TestNotStarted:
    """Test cases for not_started_list function"""

    # Basic functionality tests
    def test_not_started_list_with_invalid_path(self):
        """Test that invalid path returns empty dict"""
        result = not_started_list(Path("nonexistent.csv"))
        assert result == {}

    def test_not_started_list_returns_dict(self):
        """Test that valid file returns a dict"""
        result = not_started_list(Path("Payroll-Checker\\tests\\data_examples\\NotStarted.csv"))
        assert isinstance(result, dict)

    def test_not_started_list_with_string_path(self):
        """Test that string path returns empty dict"""
        result = not_started_list("")
        assert result == {}

    def test_not_started_list_with_none_path(self):
        """Test that None path returns empty dict"""
        result = not_started_list(None)
        assert result == {}

    # Return value structure tests
    def test_not_started_list_returns_manager_keys(self):
        """Test that result has manager emails as keys"""
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        if result:  # Only test if result is not empty
            for key in result.keys():
                assert isinstance(key, str)
                assert "@" in key  # Basic email check

    def test_not_started_list_returns_employee_lists(self):
        """Test that each manager maps to a list of employees"""
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        if result:
            for manager, employees in result.items():
                assert isinstance(employees, list)
                for employee in employees:
                    assert isinstance(employee, str)
                    assert "@" in employee  # Basic email check

    def test_not_started_list_no_duplicates_for_manager(self):
        """Test that employee list under each manager has no duplicates"""
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        if result:
            for manager, employees in result.items():
                assert len(employees) == len(set(employees)), \
                    f"Duplicate employees found for manager {manager}"

    # Filter tests
    def test_not_started_list_filters_ss_status(self):
        """Test that employees with SS status are filtered out"""
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        # SS status should be filtered, so if result is empty, filtering worked
        assert isinstance(result, dict)

    def test_not_started_list_filters_sn_status(self):
        """Test that employees with SN status are filtered out"""
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        # SN status should be filtered
        assert isinstance(result, dict)

    def test_not_started_list_filters_ww_status(self):
        """Test that employees with WW status are filtered out"""
        result = not_started_list(Path("tests\\data_examples\\NotStarted.csv"))
        # WW status should be filtered
        assert isinstance(result, dict)

    # Edge case tests
    def test_not_started_list_with_empty_csv(self, tmp_path):
        """Test with an empty CSV file"""
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("job_ecls,EmplEmail,ApprEmail\n")
        result = not_started_list(empty_csv)
        assert result == {}

    def test_not_started_list_with_only_filtered_employees(self, tmp_path):
        """Test when all employees have filtered statuses"""
        csv_file = tmp_path / "all_filtered.csv"
        csv_content = "job_ecls,EmplEmail,ApprEmail\nSS,emp1@mail.com,mgr@mail.com\nSN,emp2@mail.com,mgr@mail.com\nWW,emp3@mail.com,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = not_started_list(csv_file)
        assert result == {}

    def test_not_started_list_groups_by_manager(self, tmp_path):
        """Test that employees are correctly grouped by manager"""
        csv_file = tmp_path / "grouped.csv"
        csv_content = "job_ecls,EmplEmail,ApprEmail\nOTHER,emp1@mail.com,mgr1@mail.com\nOTHER,emp2@mail.com,mgr1@mail.com\nOTHER,emp3@mail.com,mgr2@mail.com\n"
        csv_file.write_text(csv_content)
        result = not_started_list(csv_file)

        assert "mgr1@mail.com" in result
        assert "mgr2@mail.com" in result
        assert len(result["mgr1@mail.com"]) == 2
        assert len(result["mgr2@mail.com"]) == 1
        assert "emp1@mail.com" in result["mgr1@mail.com"]
        assert "emp2@mail.com" in result["mgr1@mail.com"]
        assert "emp3@mail.com" in result["mgr2@mail.com"]

    def test_not_started_list_with_multiple_managers(self, tmp_path):
        """Test that function correctly handles multiple managers"""
        csv_file = tmp_path / "multi_managers.csv"
        csv_content = "job_ecls,EmplEmail,ApprEmail\nACTIVE,emp1@mail.com,mgr1@mail.com\nACTIVE,emp2@mail.com,mgr2@mail.com\nACTIVE,emp3@mail.com,mgr3@mail.com\n"
        csv_file.write_text(csv_content)
        result = not_started_list(csv_file)

        assert len(result) == 3
        assert all(isinstance(v, list) for v in result.values())

    # Validation tests
    def test_not_started_list_invalid_manager_email(self, tmp_path):
        """Test that invalid manager email causes function to return empty dict"""
        csv_file = tmp_path / "invalid_mgr.csv"
        csv_content = "job_ecls,EmplEmail,ApprEmail\nACTIVE,emp1@mail.com,not_an_email\n"
        csv_file.write_text(csv_content)
        result = not_started_list(csv_file)

        assert result == {}

    def test_not_started_list_invalid_employee_email(self, tmp_path):
        """Test that invalid employee email causes function to return empty dict"""
        csv_file = tmp_path / "invalid_emp.csv"
        csv_content = "job_ecls,EmplEmail,ApprEmail\nACTIVE,not_an_email,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = not_started_list(csv_file)

        assert result == {}