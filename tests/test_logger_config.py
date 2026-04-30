import os
import pytest
from helpers.logger_config import setup_logger
from helpers.pay_detection import make_df


class TestLoggerConfig:
    def test_make_df_with_valid_file(self, tmp_path):
        """Test make_df with valid CSV file"""
        csv_file = tmp_path / "test.csv"
        csv_content = "payno,other_col\n1,value\n"
        csv_file.write_text(csv_content)
        result = make_df(csv_file, 1)
        assert result is not None

    def test_make_df_with_invalid_pay_period(self, tmp_path):
        """Test make_df raises error with wrong pay period"""
        csv_file = tmp_path / "test.csv"
        csv_content = "payno,other_col\n1,value\n"
        csv_file.write_text(csv_content)
        with pytest.raises(ValueError):
            make_df(csv_file, 999)

    def test_setup_logger_returns_object(self, tmp_path):
        logger = setup_logger(str(tmp_path / "test.log"))
        assert logger is not None

    def test_setup_logger_is_logger(self, tmp_path):
        import logging
        logger = setup_logger(str(tmp_path / "test.log"))
        assert isinstance(logger, logging.Logger)

    def test_setup_logger_with_different_names(self, tmp_path):
        logger1 = setup_logger(str(tmp_path / "test1.log"))
        logger2 = setup_logger(str(tmp_path / "test2.log"))
        assert logger1 is not None
        assert logger2 is not None
