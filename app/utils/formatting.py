def normalize_source(code: str) -> str:
    """
    CRITICAL LANGUAGE RULE ENFORCEMENT

    - Preserve exact line boundaries
    - Ensure EVERY line ends with '\n'
    - NEVER fuse tokens across lines
    """

    lines = code.splitlines()
    return "\n".join(lines) + "\n"


def normalize_single_line(line: str) -> str:
    """
    Used for autocomplete:
    - Strip trailing whitespace
    - Ensure newline boundary
    """
    return line.rstrip() + "\n"