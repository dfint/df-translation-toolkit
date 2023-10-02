import pytest

from df_translation_toolkit.validation.validation_models import ProblemSeverity, ValidationProblem, ValidationException


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (ProblemSeverity.ERROR, "Error"),
        (ProblemSeverity.WARNING, "Warning"),
    ]
)
def test_problem_severity_str(test_data, expected):
    assert str(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (ValidationProblem("Error message"), "Error: Error message"),
        (ValidationProblem("Warning message", ProblemSeverity.WARNING), "Warning: Warning message"),
    ]
)
def test_validation_problem_str(test_data, expected):
    assert str(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ([ValidationProblem("Error")], True),
        ([ValidationProblem("Warning", ProblemSeverity.WARNING)], False),
    ]
)
def test_validation_problem_contains_errors(test_data, expected):
    assert ValidationProblem.contains_errors(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ([ValidationProblem("Error message")], "Error: Error message"),
        ([ValidationProblem("Warning message", ProblemSeverity.WARNING)], "Warning: Warning message"),
    ]
)
def test_validation_problem_contains_errors(test_data, expected):
    assert str(ValidationException(test_data)) == expected
