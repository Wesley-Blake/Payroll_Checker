from pathlib import Path
import pytest
from helpers.working.weekend_overtime import weekend_overtime

class TestWeekendOvertime:
    """Test cases for weekend_overtime function"""

    def test_weekend_overtime_with_invalid_paths(self):
        """Test that invalid paths return empty dict"""
        result = weekend_overtime(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_weekend_overtime_returns_dict(self):
        """Test that valid files return a dict"""
        result = weekend_overtime(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("Payroll-Checker\\tests\\data_examples\\emails.csv")
        )
        assert isinstance(result, dict)

    def test_weekend_overtime_with_missing_email_file(self):
        """Test that missing email file returns empty dict"""
        result = weekend_overtime(
            Path("Payroll-Checker\\tests\\data_examples\\hours-breakdown.csv"),
            Path("nonexistent.csv")
        )
        assert result == {}

    def test_weekend_overtime_with_weekend_work(self, tmp_path):
        """Test processing with actual weekend work and multiple weeks"""
        # Create hours with weekend work and dates before/after
        hours_file = tmp_path / "hours.csv"
        hours_content = """ts_year,ts_payno,ts_payid,ts_seq_no,Campus,Empl_ID,LastName,FirstName,JobECLS,posn_suff,JobTitle,TS_org,ts_org_name,earn_code,ts_entry_date,time_in,time_out,time_in_am_pm,time_out_am_pm,earning_hours,appr_id,appr_name
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-03,1100,1530,0,0,8,0,0
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-08,1100,1530,0,0,8,0,0
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-09,1100,1530,0,0,8,0,0
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-15,1100,1530,0,0,8,0,0
"""
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "Campus,JobLocation,EmplID,LastName,FirstName,EmplStatus,PacificEmail,SupervisorEmail\n0,0,0001,Weekend,Test,0,1@mail.com,manager1@mail.com\n"
        email_file.write_text(email_content)

        result = weekend_overtime(hours_file, email_file)
        # First weekend is Feb 8, so dates < Feb 8 should be included if worked weekend
        assert "manager1@mail.com" in result
        assert result["manager1@mail.com"] == ["1@mail.com"]

    def test_weekend_overtime_invalid_manager_email(self, tmp_path):
        """Test that invalid manager email returns empty dict"""
        hours_file = tmp_path / "hours.csv"
        hours_content = """ts_year,ts_payno,ts_payid,ts_seq_no,Campus,Empl_ID,LastName,FirstName,JobECLS,posn_suff,JobTitle,TS_org,ts_org_name,earn_code,ts_entry_date,time_in,time_out,time_in_am_pm,time_out_am_pm,earning_hours,appr_id,appr_name
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-03,1100,1530,0,0,8,0,0
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-08,1100,1530,0,0,8,0,0
"""
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "EmplID,PacificEmail,SupervisorEmail\n0001,1@mail.com,not_email\n"
        email_file.write_text(email_content)

        result = weekend_overtime(hours_file, email_file)
        assert result == {}

    def test_weekend_overtime_invalid_employee_email(self, tmp_path):
        """Test that invalid employee email returns empty dict"""
        hours_file = tmp_path / "hours.csv"
        hours_content = """ts_year,ts_payno,ts_payid,ts_seq_no,Campus,Empl_ID,LastName,FirstName,JobECLS,posn_suff,JobTitle,TS_org,ts_org_name,earn_code,ts_entry_date,time_in,time_out,time_in_am_pm,time_out_am_pm,earning_hours,appr_id,appr_name
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-03,1100,1530,0,0,8,0,0
0,1,0,0,0,0001,Weekend,Test,UU,378447-00,Test,0,0,REG,2026-02-08,1100,1530,0,0,8,0,0
"""
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "EmplID,PacificEmail,SupervisorEmail\n0001,not_email,manager1@mail.com\n"
        email_file.write_text(email_content)

        result = weekend_overtime(hours_file, email_file)
        assert result == {}