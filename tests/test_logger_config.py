import os
import pytest
from helpers.logger_config import setup_logger


class TestLoggerConfig:
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
