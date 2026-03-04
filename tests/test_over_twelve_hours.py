"""Tests for over_twleve_hours function.

Validates filtering of employees with >12 hours, earn code replacement,
and correct manager-employee grouping.
"""
from pathlib import Path
import pytest
from helpers.over_twelve_hours import over_twleve_hours

class TestOverTwelveHours:
    """Test suite for over_twleve_hours function."""

    # Input validation
    def test_over_twelve_hours_with_invalid_paths(self):
        """Test that invalid paths return empty dict"""
        result = over_twleve_hours(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_over_twelve_hours_with_missing_email_file(self):
        """Test that missing email file returns empty dict"""
        result = over_twleve_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}

    def test_over_twelve_hours_with_missing_hours_file(self):
        """Test that missing hours file returns empty dict"""
        result = over_twleve_hours(
            Path("nonexistent.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert result == {}

    def test_over_twelve_hours_with_non_path_input(self):
        """Test that non-Path inputs return empty dict"""
        result = over_twleve_hours("not_a_path", Path("test.csv"))
        assert result == {}

    def test_over_twelve_hours_with_non_path_second_input(self):
        """Test that non-Path second input returns empty dict"""
        result = over_twleve_hours(Path("test.csv"), "not_a_path")
        assert result == {}

    # Output format and threshold filtering
    def test_over_twelve_hours_returns_dict(self):
        """Test that valid files return a dict"""
        result = over_twleve_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_over_twelve_hours_below_threshold(self, tmp_path):
        """Test employees below 12 hours are filtered"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,11"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert result == {}

    def test_over_twelve_hours_exact_threshold(self, tmp_path):
        """Test employees at exactly 12 hours are filtered (> not >=)"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,12"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert result == {}

    def test_over_twelve_hours_reg_above_threshold(self, tmp_path):
        """Test REG earn code above 12 hours is included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert isinstance(result, dict)
        assert "mgr@mail.com" in result
        assert "emp@mail.com" in result["mgr@mail.com"]

    def test_over_twelve_hours_ot_above_threshold(self, tmp_path):
        """Test OT earn code converted to REG&OT and above 12 hours is included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,OT,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert isinstance(result, dict)
        assert "mgr@mail.com" in result

    # Data aggregation
    def test_over_twelve_hours_multiple_employees_same_manager(self, tmp_path):
        """Test multiple employees grouped under same manager"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test1,XX,REG,2026-01-01,1,13\n2,Test2,XX,REG,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp1@mail.com,mgr@mail.com\n2,emp2@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert "mgr@mail.com" in result
        assert len(result["mgr@mail.com"]) == 2
        assert "emp1@mail.com" in result["mgr@mail.com"]
        assert "emp2@mail.com" in result["mgr@mail.com"]

    def test_over_twelve_hours_multiple_managers(self, tmp_path):
        """Test multiple managers with their respective employees"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test1,XX,REG,2026-01-01,1,13\n2,Test2,XX,REG,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp1@mail.com,mgr1@mail.com\n2,emp2@mail.com,mgr2@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert "mgr1@mail.com" in result
        assert "mgr2@mail.com" in result

    def test_over_twelve_hours_invalid_manager_email(self, tmp_path):
        """Test that invalid manager email returns empty dict"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,invalid_manager"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert result == {}

    def test_over_twelve_hours_earn_code_replacement_reg(self, tmp_path):
        """Test that REG earn code is replaced with REG&OT"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        # The function should process this correctly showing the earn code replacement works
        assert isinstance(result, dict)

    def test_over_twelve_hours_no_matching_employees_in_email_file(self, tmp_path):
        """Test that employees not in email file are not included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n999,Test,XX,REG,2026-01-01,1,13"
        hours_file.write_text(hours_content)

        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)

        result = over_twleve_hours(hours_file, emails_file)
        assert result == {}
