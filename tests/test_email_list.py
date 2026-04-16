import pytest
from helpers.email_list import EmailList, EmailError


class TestEmailList:
    """Test cases for EmailList class"""

    def test_email_list_init_empty(self):
        """Test that EmailList initializes with empty list"""
        el = EmailList()
        assert el.email_list == []

    def test_email_list_append_valid_string(self):
        """Test appending a valid email string"""
        el = EmailList()
        el.append("test@mail.com")
        assert el.email_list == ["test@mail.com"]

    def test_email_list_append_invalid_string(self):
        """Test appending an invalid email string raises EmailError"""
        el = EmailList()
        with pytest.raises(EmailError):
            el.append("not_an_email")

    def test_email_list_append_valid_list(self):
        """Test appending a list of valid emails"""
        el = EmailList()
        el.append(["test1@mail.com", "test2@mail.com"])
        assert el.email_list == ["test1@mail.com", "test2@mail.com"]

    def test_email_list_append_mixed_list(self):
        """Test appending a list with invalid email raises EmailError"""
        el = EmailList()
        with pytest.raises(EmailError):
            el.append(["test@mail.com", "not_email"])

    def test_email_list_append_invalid_type(self):
        """Test appending non-string non-list does nothing"""
        el = EmailList()
        el.append(123)
        assert el.email_list == []

    def test_email_list_property_readonly(self):
        """Test that email_list property returns a copy or is read-only"""
        el = EmailList()
        el.append("test@mail.com")
        # Should not be able to modify through property
        emails = el.email_list
        emails.append("another@mail.com")
        assert el.email_list == ["test@mail.com"]  # Should not have changed