def strip_margin(text: str, separator: str = "|") -> str:
    return "".join(line.partition(separator)[2] for line in text.splitlines(keepends=True))
