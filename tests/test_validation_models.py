import pytest

from df_translation_toolkit.validation.validation_models import ProblemSeverity, ValidationException, ValidationProblem


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (ProblemSeverity.ERROR, "Error"),
        (ProblemSeverity.WARNING, "Warning"),
    ],
)
def test_problem_severity_str(test_data: ProblemSeverity, expected: str) -> None:
    assert str(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (ValidationProblem("Error message"), "Error: Error message"),
        (ValidationProblem("Warning message", ProblemSeverity.WARNING), "Warning: Warning message"),
    ],
)
def test_validation_problem_str(test_data: ValidationProblem, expected: str) -> None:
    assert str(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ([ValidationProblem("Error")], True),
        ([ValidationProblem("Warning", ProblemSeverity.WARNING)], False),
    ],
)
def test_validation_problem_contains_errors(test_data: list[ValidationProblem], expected: bool) -> None:  # noqa: FBT001
    assert ValidationProblem.contains_errors(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            [ValidationProblem("Error message"), ValidationProblem("Warning message", ProblemSeverity.WARNING)],
            "Error: Error message\nWarning: Warning message",
        ),
        ([ValidationProblem("Warning message", ProblemSeverity.WARNING)], "Warning: Warning message"),
    ],
)
def test_validation_exception_str(test_data: list[ValidationProblem], expected: str) -> None:
    assert str(ValidationException(test_data)) == expected
