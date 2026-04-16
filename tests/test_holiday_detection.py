from pathlib import Path
import pytest
from helpers.holiday_detection import holiday_detection_type, holiday_detection_date, no_holiday_detection, return_dict, holidays_input


class TestHolidayDetection:
    """Test cases for holiday detection functions"""

    def test_holiday_detection_type_invalid_files(self):
        """Test invalid file paths return empty dict"""
        result = holiday_detection_type(Path("nonexistent.csv"), Path("nonexistent.csv"), [])
        assert result == {}

    def test_holiday_detection_type_with_holiday_work(self, tmp_path):
        """Test detection of work on holidays"""
        # Create hours file with HOL on holiday date
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,REG,2024-01-01,123,8\n"
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com\n"
        email_file.write_text(email_content)

        result = holiday_detection_type(hours_file, email_file, ["2024-01-01"])
        # Should find REG work on holiday
        assert "mgr@mail.com" in result
        assert result["mgr@mail.com"] == ["emp@mail.com"]

    def test_holiday_detection_type_no_dates_in_holiday_list(self, tmp_path):
        """Test when no dates match the holiday list"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,REG,2024-01-02,123,8\n"
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com\n"
        email_file.write_text(email_content)

        result = holiday_detection_type(hours_file, email_file, ["2024-01-01"])
        # No dates in holiday list, so filtered_df empty
        assert result == {}

    def test_holiday_detection_date_invalid_files(self):
        """Test invalid file paths return empty dict"""
        result = holiday_detection_date(Path("nonexistent.csv"), Path("nonexistent.csv"), [])
        assert result == {}

    def test_holiday_detection_date_with_holiday_pay(self, tmp_path):
        """Test detection of holiday pay on non-holiday dates"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,HOL,2024-01-02,123,8\n"
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com\n"
        email_file.write_text(email_content)

        result = holiday_detection_date(hours_file, email_file, ["2024-01-01"])
        # HOL on non-holiday date
        assert "mgr@mail.com" in result
        assert result["mgr@mail.com"] == ["emp@mail.com"]

    def test_no_holiday_detection_invalid_files(self):
        """Test invalid file paths return empty dict"""
        result = no_holiday_detection(Path("nonexistent.csv"), Path("nonexistent.csv"))
        assert result == {}

    def test_no_holiday_detection_with_holiday_pay(self, tmp_path):
        """Test detection of all holiday pay"""
        hours_file = tmp_path / "hours.csv"
        hours_content = "Empl_ID,LastName,JobECLS,earn_code,ts_entry_date,appr_id,earning_hours\n1,Test,UU,HOL,2024-01-01,123,8\n"
        hours_file.write_text(hours_content)

        email_file = tmp_path / "emails.csv"
        email_content = "EmplID,PacificEmail,SupervisorEmail\n1,emp@mail.com,mgr@mail.com\n"
        email_file.write_text(email_content)

        result = no_holiday_detection(hours_file, email_file)
        assert "mgr@mail.com" in result
        assert result["mgr@mail.com"] == ["emp@mail.com"]

    def test_return_dict_valid(self, tmp_path):
        """Test return_dict with valid data"""
        import pandas as pd
        df = pd.DataFrame({
            'PacificEmail': ['emp1@mail.com', 'emp2@mail.com'],
            'SupervisorEmail': ['mgr@mail.com', 'mgr@mail.com']
        })
        result = return_dict(df)
        assert result == {'mgr@mail.com': ['emp1@mail.com', 'emp2@mail.com']}

    def test_return_dict_invalid_manager_email(self, tmp_path):
        """Test return_dict with invalid manager email"""
        import pandas as pd
        df = pd.DataFrame({
            'PacificEmail': ['emp1@mail.com'],
            'SupervisorEmail': ['not_email']
        })
        result = return_dict(df)
        assert result == {}

    def test_return_dict_invalid_employee_email(self, tmp_path):
        """Test return_dict with invalid employee email"""
        import pandas as pd
        df = pd.DataFrame({
            'PacificEmail': ['not_email'],
            'SupervisorEmail': ['mgr@mail.com']
        })
        result = return_dict(df)
        assert result == {}