#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/logging/test_logger.py

"""Tests for scitex_core.logging logger functionality."""

import pytest
import logging
import sys

# Try to import, but mark tests as skipped if dependencies aren't available
try:
    from scitex_core.logging._logger import SciTeXLogger, setup_logger_class
    from scitex_core.logging._levels import SUCCESS, FAIL
    LOGGING_AVAILABLE = True
except ImportError as e:
    LOGGING_AVAILABLE = False
    skip_reason = f"Logging dependencies not available: {e}"

skip_if_no_logging = pytest.mark.skipif(
    not LOGGING_AVAILABLE,
    reason=skip_reason if not LOGGING_AVAILABLE else ""
)


@skip_if_no_logging
class TestSciTeXLogger:
    """Test SciTeXLogger class."""

    def test_scitex_logger_is_logger(self):
        """Test that SciTeXLogger extends logging.Logger."""
        assert issubclass(SciTeXLogger, logging.Logger)

    def test_logger_has_success_method(self):
        """Test that logger has success method."""
        setup_logger_class()
        logger = logging.getLogger("test_success")
        assert hasattr(logger, "success")
        assert callable(logger.success)

    def test_logger_has_fail_method(self):
        """Test that logger has fail method."""
        setup_logger_class()
        logger = logging.getLogger("test_fail")
        assert hasattr(logger, "fail")
        assert callable(logger.fail)

    def test_success_method_logs(self, caplog):
        """Test that success method logs messages."""
        setup_logger_class()
        logger = logging.getLogger("test_success_log")
        logger.setLevel(logging.DEBUG)

        with caplog.at_level(logging.DEBUG):
            logger.success("Success message")

        # Check if message was logged
        assert any("Success message" in record.message for record in caplog.records)

    def test_fail_method_logs(self, caplog):
        """Test that fail method logs messages."""
        setup_logger_class()
        logger = logging.getLogger("test_fail_log")
        logger.setLevel(logging.DEBUG)

        with caplog.at_level(logging.DEBUG):
            logger.fail("Failure message")

        # Check if message was logged
        assert any("Failure message" in record.message for record in caplog.records)

    def test_standard_log_methods_available(self):
        """Test that standard logging methods are available."""
        setup_logger_class()
        logger = logging.getLogger("test_standard")

        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")


@skip_if_no_logging
class TestSetupLoggerClass:
    """Test setup_logger_class function."""

    def test_setup_logger_class_callable(self):
        """Test that setup_logger_class is callable."""
        assert callable(setup_logger_class)

    def test_setup_logger_class_sets_scitex_logger(self):
        """Test that setup makes future loggers SciTeXLogger."""
        setup_logger_class()
        logger = logging.getLogger("test_class_setup")
        assert isinstance(logger, SciTeXLogger)

    def test_setup_logger_class_idempotent(self):
        """Test that calling setup multiple times is safe."""
        setup_logger_class()
        setup_logger_class()
        logger = logging.getLogger("test_idempotent")
        assert isinstance(logger, SciTeXLogger)


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
