from __future__ import annotations

from dataclasses import dataclass, field
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


@dataclass
class ProblemInfo:
    original: str
    translation: str
    problems: list[ValidationProblem] = field(default_factory=list)

    def __str__(self) -> str:
        problems_text = "\n".join(str(problem) for problem in self.problems)
        return f"Problematic tag pair: {self.original!r}, {self.translation!r}\nProblems:\n{problems_text}"

    def contains_errors(self) -> bool:
        return ValidationProblem.contains_errors(self.problems)


class Diagnostics:
    problems: list[ProblemInfo]

    def __init__(self) -> None:
        self.problems = []

    def add(self, problem_info: ProblemInfo) -> None:
        self.problems.append(problem_info)

    def __bool__(self) -> bool:
        return bool(self.problems)

    def contains_errors(self) -> bool:
        return any(problem.contains_errors() for problem in self.problems)
