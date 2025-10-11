import pytest

from df_translation_toolkit.validation.validation_models import (
    Diagnostics,
    ProblemInfo,
    ProblemSeverity,
    ValidationException,
    ValidationProblem,
)


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


def test_diagnostics() -> None:
    diagnostics = Diagnostics()
    assert bool(diagnostics)
    assert diagnostics.contains_problems() is False
    diagnostics.add(ProblemInfo("text", "translation", problems=[]))
    assert diagnostics.contains_problems() is False
    diagnostics.add(
        ProblemInfo("text1", "translation1", problems=[ValidationProblem("Warning", ProblemSeverity.WARNING)]),
    )
    assert diagnostics.contains_problems() is True
    assert diagnostics.contains_errors() is False
    diagnostics.add(
        ProblemInfo("text2", "translation2", problems=[ValidationProblem("Error")]),
    )
    assert diagnostics.contains_errors() is True
