import os
import pytest
from helpers.logger_config import setup_logger


class TestLoggerConfig:
    def test_setup_logger_returns_object(self):
        logger = setup_logger("test.log")
        assert logger is not None

    def test_setup_logger_is_logger(self):
        import logging
        logger = setup_logger("test.log")
        assert isinstance(logger, logging.Logger)

    def test_setup_logger_with_different_names(self):
        logger1 = setup_logger("test1.log")
        logger2 = setup_logger("test2.log")
        assert logger1 is not None
        assert logger2 is not None
