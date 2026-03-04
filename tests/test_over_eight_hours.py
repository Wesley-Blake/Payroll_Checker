"""Tests for over_eight_hours function.

Validates filtering of employees with >8 hours (union >7.5),
union/non-union logic, and correct manager-employee grouping.
"""
from pathlib import Path
import pytest
from helpers.over_eight_hours import over_eight_hours

class TestOverEightHours:
    """Test suite for over_eight_hours function."""

    # Input validation
    def test_over_eight_hours_with_invalid_paths(self):
        """Test that invalid paths return empty dict"""
        result = over_eight_hours(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_over_eight_hours_with_missing_email_file(self):
        """Test that missing email file returns empty dict"""
        result = over_eight_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}

    def test_over_eight_hours_with_missing_hours_file(self):
        """Test that missing hours file returns empty dict"""
        result = over_eight_hours(
            Path("nonexistent.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert result == {}

    # Output format and threshold filtering
    def test_over_eight_hours_returns_dict(self):
        """Test that valid files return a dict"""
        result = over_eight_hours(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_over_eight_hours_filters_non_reg_earn_code(self, tmp_path):
        """Test that non-REG earn codes are filtered out"""
        # Create hours CSV with only OT codes
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,OT,2026-01-01,1,10"
        hours_file.write_text(hours_content)
        
        # Create emails CSV
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert result == {}

    def test_over_eight_hours_union_below_threshold(self, tmp_path):
        """Test union employees below 7.5 hours are filtered"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,REG,2026-01-01,1,7"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert result == {}

    def test_over_eight_hours_non_union_below_threshold(self, tmp_path):
        """Test non-union employees below 8 hours are filtered"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,7.5"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert result == {}

    def test_over_eight_hours_union_uu_above_threshold(self, tmp_path):
        """Test union UU employees above 7.5 hours are included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,REG,2026-01-01,1,8"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert isinstance(result, dict)
        assert "mgr@mail.com" in result
        assert "emp@mail.com" in result["mgr@mail.com"]

    def test_over_eight_hours_union_vv_above_threshold(self, tmp_path):
        """Test union VV employees above 7.5 hours are included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,VV,REG,2026-01-01,1,8"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert isinstance(result, dict)
        assert "mgr@mail.com" in result

    def test_over_eight_hours_non_union_above_threshold(self, tmp_path):
        """Test non-union employees above 8 hours are included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,XX,REG,2026-01-01,1,8.5"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert isinstance(result, dict)
        assert "mgr@mail.com" in result

    # Data aggregation
    def test_over_eight_hours_multiple_employees_same_manager(self, tmp_path):
        """Test multiple employees grouped under same manager"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test1,UU,REG,2026-01-01,1,8\n2,Test2,UU,REG,2026-01-01,1,8"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp1@mail.com,mgr@mail.com\n2,emp2@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert "mgr@mail.com" in result
        assert len(result["mgr@mail.com"]) == 2
        assert "emp1@mail.com" in result["mgr@mail.com"]
        assert "emp2@mail.com" in result["mgr@mail.com"]

    def test_over_eight_hours_multiple_managers(self, tmp_path):
        """Test multiple managers with their respective employees"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test1,UU,REG,2026-01-01,1,8\n2,Test2,UU,REG,2026-01-01,1,8"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp1@mail.com,mgr1@mail.com\n2,emp2@mail.com,mgr2@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert "mgr1@mail.com" in result
        assert "mgr2@mail.com" in result

    def test_over_eight_hours_invalid_manager_email(self, tmp_path):
        """Test that invalid manager email returns empty dict"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,REG,2026-01-01,1,8"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,invalid_manager"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert result == {}

    def test_over_eight_hours_no_matching_employees_in_email_file(self, tmp_path):
        """Test that employees not in email file are not included"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n999,Test,UU,REG,2026-01-01,1,8"
        hours_file.write_text(hours_content)
        
        emails_file = tmp_path / "emails.csv"
        emails_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com"
        emails_file.write_text(emails_content)
        
        result = over_eight_hours(hours_file, emails_file)
        assert result == {}
