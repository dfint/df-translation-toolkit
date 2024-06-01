from __future__ import annotations

from enum import Enum, auto
from typing import NamedTuple


class ProblemSeverity(Enum):
    ERROR = auto()
    WARNING = auto()

    def __str__(self) -> str:
        return self.name.title()


class ValidationProblem(NamedTuple):
    text: str
    severity: ProblemSeverity = ProblemSeverity.ERROR

    def __str__(self) -> str:
        return f"{self.severity}: {self.text}"

    @staticmethod
    def contains_errors(problems: list[ValidationProblem]) -> bool:
        return any(problem.severity is ProblemSeverity.ERROR for problem in problems)


class ValidationException(Exception):
    def __init__(self, problems: list[ValidationProblem]) -> None:
        self.problems = problems

    def __str__(self) -> str:
        return "\n".join(str(error) for error in self.problems)
