#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/test_errors.py

"""Comprehensive tests for scitex_core.errors module."""

import pytest
import warnings
import tempfile
import os
from scitex_core.errors import *


class TestSciTeXError:
    """Test the base SciTeXError class."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = SciTeXError("Test error message")
        assert "Test error message" in str(error)
        assert error.message == "Test error message"
        assert error.context == {}
        assert error.suggestion is None

    def test_error_with_context(self):
        """Test error with context information."""
        context = {"file": "test.py", "line": 42}
        error = SciTeXError("Test error", context=context)

        assert error.message == "Test error"
        assert error.context == context
        assert "file: test.py" in str(error)
        assert "line: 42" in str(error)

    def test_error_with_suggestion(self):
        """Test error with suggestion."""
        suggestion = "Try fixing this"
        error = SciTeXError("Test error", suggestion=suggestion)

        assert error.suggestion == suggestion
        assert "Suggestion: Try fixing this" in str(error)

    def test_error_with_all_params(self):
        """Test error with all parameters."""
        context = {"key": "value"}
        suggestion = "Fix it"
        error = SciTeXError("Message", context=context, suggestion=suggestion)

        error_str = str(error)
        assert "Message" in error_str
        assert "key: value" in error_str
        assert "Suggestion: Fix it" in error_str


class TestConfigurationErrors:
    """Test configuration-related error classes."""

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Config issue")
        assert isinstance(error, SciTeXError)
        assert "Config issue" in str(error)

    def test_config_file_not_found_error(self):
        """Test ConfigFileNotFoundError."""
        filepath = "./config/missing.yaml"
        error = ConfigFileNotFoundError(filepath)

        assert isinstance(error, ConfigurationError)
        assert filepath in str(error)
        assert "not found" in str(error).lower()
        assert error.context["filepath"] == filepath
        assert error.suggestion is not None

    def test_config_key_error(self):
        """Test ConfigKeyError without available keys."""
        error = ConfigKeyError("missing_key")

        assert "missing_key" in str(error)
        assert "not found" in str(error).lower()
        assert error.context["missing_key"] == "missing_key"

    def test_config_key_error_with_available_keys(self):
        """Test ConfigKeyError with available keys."""
        available = ["key1", "key2", "key3"]
        error = ConfigKeyError("missing", available_keys=available)

        assert "missing" in str(error)
        assert error.context["available_keys"] == available


class TestIOErrors:
    """Test IO-related error classes."""

    def test_io_error_base(self):
        """Test base IOError."""
        error = IOError("IO issue")
        assert isinstance(error, SciTeXError)

    def test_file_format_error_basic(self):
        """Test FileFormatError with basic info."""
        error = FileFormatError("test.txt")
        assert "test.txt" in str(error)
        assert error.context["filepath"] == "test.txt"

    def test_file_format_error_with_formats(self):
        """Test FileFormatError with format information."""
        error = FileFormatError(
            "test.txt",
            expected_format="json",
            actual_format="txt"
        )

        error_str = str(error)
        assert "expected: json" in error_str
        assert "got: txt" in error_str
        assert error.context["expected_format"] == "json"
        assert error.context["actual_format"] == "txt"

    def test_save_error(self):
        """Test SaveError."""
        error = SaveError("output.pkl", "Permission denied")

        assert "output.pkl" in str(error)
        assert "Permission denied" in str(error)
        assert error.context["filepath"] == "output.pkl"
        assert error.context["reason"] == "Permission denied"

    def test_load_error(self):
        """Test LoadError."""
        error = LoadError("input.pkl", "File corrupted")

        assert "input.pkl" in str(error)
        assert "File corrupted" in str(error)
        assert error.context["filepath"] == "input.pkl"


class TestScholarErrors:
    """Test scholar module error classes."""

    def test_scholar_error_base(self):
        """Test base ScholarError."""
        error = ScholarError("Scholar issue")
        assert isinstance(error, SciTeXError)

    def test_search_error(self):
        """Test SearchError."""
        error = SearchError("machine learning", "PubMed", "API timeout")

        error_str = str(error)
        assert "machine learning" in error_str
        assert "PubMed" in error_str
        assert error.context["query"] == "machine learning"
        assert error.context["source"] == "PubMed"
        assert error.context["reason"] == "API timeout"

    def test_enrichment_error(self):
        """Test EnrichmentError."""
        error = EnrichmentError("Paper Title", "Journal not found")

        assert "Paper Title" in str(error)
        assert error.context["paper_title"] == "Paper Title"

    def test_pdf_download_error(self):
        """Test PDFDownloadError."""
        url = "https://example.com/paper.pdf"
        error = PDFDownloadError(url, "404 Not Found")

        assert url in str(error)
        assert error.context["url"] == url

    def test_doi_resolution_error(self):
        """Test DOIResolutionError."""
        doi = "10.1234/example"
        error = DOIResolutionError(doi, "Invalid DOI")

        assert doi in str(error)
        assert error.context["doi"] == doi

    def test_pdf_extraction_error(self):
        """Test PDFExtractionError."""
        error = PDFExtractionError("paper.pdf", "Encrypted")

        assert "paper.pdf" in str(error)
        assert error.context["filepath"] == "paper.pdf"

    def test_bibtex_enrichment_error(self):
        """Test BibTeXEnrichmentError."""
        error = BibTeXEnrichmentError("refs.bib", "Invalid entry")

        assert "refs.bib" in str(error)
        assert error.context["bibtex_file"] == "refs.bib"

    def test_translator_error(self):
        """Test TranslatorError."""
        error = TranslatorError("PubMed Translator", "JS error")

        assert "PubMed Translator" in str(error)
        assert error.context["translator"] == "PubMed Translator"

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Google Scholar", "Invalid credentials")

        assert "Google Scholar" in str(error)
        assert error.context["provider"] == "Google Scholar"


class TestPlottingErrors:
    """Test plotting-related error classes."""

    def test_plotting_error_base(self):
        """Test base PlottingError."""
        error = PlottingError("Plotting issue")
        assert isinstance(error, SciTeXError)

    def test_figure_not_found_error_int(self):
        """Test FigureNotFoundError with integer ID."""
        error = FigureNotFoundError(1)

        assert "Figure 1" in str(error)
        assert error.context["figure_id"] == 1

    def test_figure_not_found_error_str(self):
        """Test FigureNotFoundError with string ID."""
        error = FigureNotFoundError("main_plot")

        assert "main_plot" in str(error)
        assert error.context["figure_id"] == "main_plot"

    def test_axis_error_basic(self):
        """Test AxisError without axis info."""
        error = AxisError("Subplot index out of range")

        assert "Subplot index" in str(error)

    def test_axis_error_with_info(self):
        """Test AxisError with axis info."""
        axis_info = {"index": (0, 1), "shape": (2, 2)}
        error = AxisError("Invalid axis", axis_info=axis_info)

        assert error.context["axis_info"] == axis_info


class TestDataErrors:
    """Test data processing error classes."""

    def test_data_error_base(self):
        """Test base DataError."""
        error = DataError("Data issue")
        assert isinstance(error, SciTeXError)

    def test_shape_error(self):
        """Test ShapeError."""
        expected = (10, 5)
        actual = (5, 10)
        error = ShapeError(expected, actual, "matrix multiplication")

        error_str = str(error)
        assert "matrix multiplication" in error_str
        assert error.context["expected_shape"] == expected
        assert error.context["actual_shape"] == actual
        assert error.context["operation"] == "matrix multiplication"

    def test_dtype_error(self):
        """Test DTypeError."""
        error = DTypeError("float32", "int64", "neural network input")

        error_str = str(error)
        assert "float32" in error_str
        assert "int64" in error_str
        assert "neural network input" in error_str
        assert error.context["expected_dtype"] == "float32"
        assert error.context["actual_dtype"] == "int64"


class TestPathErrors:
    """Test path-related error classes."""

    def test_path_error_base(self):
        """Test base PathError."""
        error = PathError("Path issue")
        assert isinstance(error, SciTeXError)

    def test_invalid_path_error(self):
        """Test InvalidPathError."""
        path = "/absolute/path"
        reason = "Must be relative"
        error = InvalidPathError(path, reason)

        assert path in str(error)
        assert reason in str(error)
        assert error.context["path"] == path
        assert error.context["reason"] == reason

    def test_path_not_found_error(self):
        """Test PathNotFoundError."""
        path = "./nonexistent/file.txt"
        error = PathNotFoundError(path)

        assert path in str(error)
        assert error.context["path"] == path


class TestTemplateErrors:
    """Test template-related error classes."""

    def test_template_error_base(self):
        """Test base TemplateError."""
        error = TemplateError("Template issue")
        assert isinstance(error, SciTeXError)

    def test_template_violation_error(self):
        """Test TemplateViolationError."""
        filepath = "./script.py"
        violation = "Missing timestamp"
        error = TemplateViolationError(filepath, violation)

        error_str = str(error)
        assert filepath in error_str
        assert violation in error_str
        assert error.context["filepath"] == filepath
        assert error.context["violation"] == violation


class TestNeuralNetworkErrors:
    """Test neural network error classes."""

    def test_nn_error_base(self):
        """Test base NNError."""
        error = NNError("NN issue")
        assert isinstance(error, SciTeXError)

    def test_model_error(self):
        """Test ModelError."""
        error = ModelError("ResNet50", "Invalid input shape")

        assert "ResNet50" in str(error)
        assert "Invalid input shape" in str(error)
        assert error.context["model_name"] == "ResNet50"


class TestStatisticsErrors:
    """Test statistics error classes."""

    def test_stats_error_base(self):
        """Test base StatsError."""
        error = StatsError("Stats issue")
        assert isinstance(error, SciTeXError)

    def test_test_error(self):
        """Test TestError."""
        error = TestError("t-test", "Insufficient samples")

        assert "t-test" in str(error)
        assert "Insufficient samples" in str(error)
        assert error.context["test_name"] == "t-test"


class TestWarningFunctions:
    """Test warning functions."""

    def test_warn_deprecated_basic(self):
        """Test warn_deprecated without version."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecated("old_func", "new_func")

            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "old_func" in str(w[0].message)
            assert "new_func" in str(w[0].message)

    def test_warn_deprecated_with_version(self):
        """Test warn_deprecated with version."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_deprecated("old_func", "new_func", version="2.0")

            assert len(w) == 1
            assert "2.0" in str(w[0].message)

    def test_warn_performance(self):
        """Test warn_performance."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_performance("data loading", "Use memory mapping")

            assert len(w) == 1
            assert issubclass(w[0].category, SciTeXWarning)
            assert "data loading" in str(w[0].message)
            assert "Use memory mapping" in str(w[0].message)

    def test_warn_data_loss(self):
        """Test warn_data_loss."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn_data_loss("type conversion", "Precision loss")

            assert len(w) == 1
            assert issubclass(w[0].category, SciTeXWarning)
            assert "type conversion" in str(w[0].message)
            assert "Precision loss" in str(w[0].message)


class TestValidationHelpers:
    """Test validation helper functions."""

    def test_check_path_valid_relative_current(self):
        """Test check_path with valid './' path."""
        # Should not raise
        check_path("./data/file.txt")

    def test_check_path_valid_relative_parent(self):
        """Test check_path with valid '../' path."""
        # Should not raise
        check_path("../config/settings.yaml")

    def test_check_path_invalid_absolute(self):
        """Test check_path with invalid absolute path."""
        with pytest.raises(InvalidPathError) as exc_info:
            check_path("/absolute/path")

        assert "relative" in str(exc_info.value).lower()

    def test_check_path_invalid_type(self):
        """Test check_path with non-string type."""
        with pytest.raises(InvalidPathError) as exc_info:
            check_path(123)

        assert "must be a string" in str(exc_info.value).lower()

    def test_check_file_exists_valid(self):
        """Test check_file_exists with existing file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            temp_path = tf.name

        try:
            # Should not raise
            check_file_exists(temp_path)
        finally:
            os.unlink(temp_path)

    def test_check_file_exists_missing(self):
        """Test check_file_exists with missing file."""
        with pytest.raises(PathNotFoundError) as exc_info:
            check_file_exists("/nonexistent/file.txt")

        assert "/nonexistent/file.txt" in str(exc_info.value)

    def test_check_shape_compatibility_matching(self):
        """Test check_shape_compatibility with matching shapes."""
        # Should not raise
        check_shape_compatibility((10, 5), (10, 5), "addition")

    def test_check_shape_compatibility_mismatching(self):
        """Test check_shape_compatibility with mismatching shapes."""
        with pytest.raises(ShapeError) as exc_info:
            check_shape_compatibility((10, 5), (5, 10), "addition")

        error = exc_info.value
        assert error.context["expected_shape"] == (10, 5)
        assert error.context["actual_shape"] == (5, 10)
        assert error.context["operation"] == "addition"


class TestErrorInheritance:
    """Test error class inheritance hierarchy."""

    def test_all_errors_inherit_from_scitex_error(self):
        """Test that all custom errors inherit from SciTeXError."""
        error_classes = [
            ConfigurationError, ConfigFileNotFoundError, ConfigKeyError,
            IOError, FileFormatError, SaveError, LoadError,
            ScholarError, SearchError, EnrichmentError,
            PlottingError, FigureNotFoundError, AxisError,
            DataError, ShapeError, DTypeError,
            PathError, InvalidPathError, PathNotFoundError,
            TemplateError, TemplateViolationError,
            NNError, ModelError,
            StatsError, TestError,
        ]

        for error_class in error_classes:
            # Create instance with minimal args
            if error_class == ConfigFileNotFoundError:
                instance = error_class("test.yaml")
            elif error_class == ConfigKeyError:
                instance = error_class("key")
            elif error_class == FileFormatError:
                instance = error_class("file.txt")
            elif error_class in [SaveError, LoadError]:
                instance = error_class("file.txt", "reason")
            elif error_class == SearchError:
                instance = error_class("query", "source", "reason")
            elif error_class == EnrichmentError:
                instance = error_class("title", "reason")
            elif error_class == FigureNotFoundError:
                instance = error_class(1)
            elif error_class == AxisError:
                instance = error_class("message")
            elif error_class == ShapeError:
                instance = error_class((1,), (2,), "op")
            elif error_class == DTypeError:
                instance = error_class("int", "float", "op")
            elif error_class == InvalidPathError:
                instance = error_class("path", "reason")
            elif error_class == PathNotFoundError:
                instance = error_class("path")
            elif error_class == TemplateViolationError:
                instance = error_class("file", "violation")
            elif error_class == ModelError:
                instance = error_class("model", "reason")
            elif error_class == TestError:
                instance = error_class("test", "reason")
            else:
                instance = error_class("message")

            assert isinstance(instance, SciTeXError)
            assert isinstance(instance, Exception)


class TestSciTeXWarning:
    """Test SciTeX warning class."""

    def test_scitex_warning_is_user_warning(self):
        """Test that SciTeXWarning inherits from UserWarning."""
        assert issubclass(SciTeXWarning, UserWarning)

    def test_scitex_warning_can_be_raised(self):
        """Test that SciTeXWarning can be raised."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.warn("Test warning", SciTeXWarning)

            assert len(w) == 1
            assert issubclass(w[0].category, SciTeXWarning)


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
