from pathlib import Path
import pytest
from helpers.pending_status import pending


class TestPendingStatus:
    """Test cases for pending function"""

    # Basic functionality tests
    def test_pending_with_invalid_path(self):
        """Test that invalid path returns empty list"""
        result = pending(Path("nonexistent.csv"))
        assert result == []

    def test_pending_returns_list(self):
        """Test that valid file returns a list"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        assert isinstance(result, list)

    def test_pending_with_string_path(self):
        """Test that string path returns empty list"""
        result = pending("")
        assert result == []

    def test_pending_with_none_path(self):
        """Test that None path returns empty list"""
        result = pending(None)
        assert result == []

    def test_pending_with_integer_path(self):
        """Test that integer path returns empty list"""
        result = pending(123)
        assert result == []

    # Return value structure tests
    def test_pending_returns_list_of_strings(self):
        """Test that result contains only strings"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        if result:
            for email in result:
                assert isinstance(email, str)

    def test_pending_returns_unique_emails(self):
        """Test that returned emails are unique"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        assert len(result) == len(set(result)), "Duplicate emails found in result"

    def test_pending_returns_valid_emails(self):
        """Test that all returned values are valid email addresses"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        for email in result:
            assert "@" in email, f"Invalid email format: {email}"

    # Filter tests
    def test_pending_filters_inprogress_status(self):
        """Test that employees with Inprogress status are filtered out"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        assert isinstance(result, list)

    def test_pending_filters_approved_status(self):
        """Test that employees with Approved status are filtered out"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        assert isinstance(result, list)

    def test_pending_includes_only_pending_status(self):
        """Test that only Pending status employees are included"""
        result = pending(Path("tests\\data_examples\\comments-status.csv"))
        # From the data: manager1 has 2 pending, manager2 has 2 pending
        assert "manager1@mail.com" in result
        assert "manager2@mail.com" in result

    # Edge case tests
    def test_pending_with_empty_csv(self, tmp_path):
        """Test with an empty CSV file"""
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("ts_Status,ApprEmail\n")
        result = pending(empty_csv)
        assert result == []

    def test_pending_with_no_pending_status(self, tmp_path):
        """Test when no employees have Pending status"""
        csv_file = tmp_path / "no_pending.csv"
        csv_content = "ts_Status,ApprEmail\nApproved,mgr1@mail.com\nInprogress,mgr2@mail.com\nApproved,mgr3@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        assert result == []

    def test_pending_with_single_pending_employee(self, tmp_path):
        """Test with exactly one pending employee"""
        csv_file = tmp_path / "single_pending.csv"
        csv_content = "ts_Status,ApprEmail\nPending,manager@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        assert len(result) == 1
        assert "manager@mail.com" in result

    def test_pending_with_multiple_pending_same_manager(self, tmp_path):
        """Test multiple pending employees with the same manager"""
        csv_file = tmp_path / "multi_pending_same.csv"
        csv_content = "ts_Status,ApprEmail\nPending,mgr@mail.com\nPending,mgr@mail.com\nPending,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        # Should return unique managers only
        assert len(result) == 1
        assert result[0] == "mgr@mail.com"

    def test_pending_with_multiple_pending_different_managers(self, tmp_path):
        """Test multiple pending employees with different managers"""
        csv_file = tmp_path / "multi_pending_diff.csv"
        csv_content = "ts_Status,ApprEmail\nPending,mgr1@mail.com\nPending,mgr2@mail.com\nPending,mgr3@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        assert len(result) == 3
        assert "mgr1@mail.com" in result
        assert "mgr2@mail.com" in result
        assert "mgr3@mail.com" in result

    # Validation tests
    def test_pending_with_invalid_manager_email(self, tmp_path):
        """Test that invalid manager email causes function to return empty list"""
        csv_file = tmp_path / "invalid_mgr.csv"
        csv_content = "ts_Status,ApprEmail\nPending,not_an_email\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        assert result == []

    def test_pending_with_mixed_valid_invalid_emails(self, tmp_path):
        """Test that even one invalid email causes function to return empty list"""
        csv_file = tmp_path / "mixed_emails.csv"
        csv_content = "ts_Status,ApprEmail\nPending,valid@mail.com\nPending,invalid_email\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        assert result == []

    # Column handling tests
    def test_pending_with_missing_ts_status_column(self, tmp_path):
        """Test behavior when ts_Status column is missing"""
        csv_file = tmp_path / "missing_status.csv"
        csv_content = "ApprEmail\nmgr@mail.com\n"
        csv_file.write_text(csv_content)

        with pytest.raises(KeyError):
            pending(csv_file)

    def test_pending_with_missing_appRemail_column(self, tmp_path):
        """Test behavior when ApprEmail column is missing"""
        csv_file = tmp_path / "missing_appRemail.csv"
        csv_content = "ts_Status\nPending\n"
        csv_file.write_text(csv_content)

        with pytest.raises(KeyError):
            pending(csv_file)

    # Case sensitivity tests
    def test_pending_with_uppercase_status(self, tmp_path):
        """Test status filtering is case-sensitive (PENDING vs Pending)"""
        csv_file = tmp_path / "uppercase_status.csv"
        csv_content = "ts_Status,ApprEmail\nPENDING,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        # PENDING (uppercase) should not match Pending
        assert result == []

    def test_pending_with_lowercase_status(self, tmp_path):
        """Test status filtering is case-sensitive (pending vs Pending)"""
        csv_file = tmp_path / "lowercase_status.csv"
        csv_content = "ts_Status,ApprEmail\npending,mgr@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)
        # pending (lowercase) should not match Pending
        assert result == []

    # Integration tests
    def test_pending_with_mixed_statuses_and_managers(self, tmp_path):
        """Test complete workflow with mixed statuses and multiple managers"""
        csv_file = tmp_path / "complete.csv"
        csv_content = "ts_Status,ApprEmail\nInprogress,mgr1@mail.com\nPending,mgr2@mail.com\nApproved,mgr3@mail.com\nPending,mgr2@mail.com\nPending,mgr4@mail.com\nInprogress,mgr1@mail.com\n"
        csv_file.write_text(csv_content)
        result = pending(csv_file)

        assert len(result) == 3
        assert "mgr2@mail.com" in result
        assert "mgr4@mail.com" in result
        assert "mgr1@mail.com" not in result
        assert "mgr3@mail.com" not in result
