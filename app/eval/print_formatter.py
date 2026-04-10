from __future__ import annotations


class PrintFormatter:
    @staticmethod
    def format_arg(value) -> str:
        if value is None:
            return ""

        if not isinstance(value, str):
            return str(value)

        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        elif len(value) >= 2 and value[0] == "'" and value[-1] == "'":
            value = value[1:-1]

        escape_sequences: dict[str, str] = {
            "\\n": "\n",
            "\\t": "\t",
            "\\r": "\r",
            "\\\\": "\\",
            '\\"': '"',
            "\\'": "'",
            "\\0": "\0",
        }

        result = value
        for escape, replacement in escape_sequences.items():
            result = result.replace(escape, replacement)

        return result
