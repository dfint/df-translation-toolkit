
from collections.abc import Iterator

from df_translation_toolkit.validation.validation_models import ValidationProblem


def validate(original: str, translation: str) -> Iterator[ValidationProblem]:
    """Draft for general validation."""
    _ = original, translation
    return iter(())
