from antlr4.error.ErrorListener import ErrorListener
from app.models.CustomError import ErrorResponse


class EVALErrorListener(ErrorListener):
    """
    Custom error listener that collects syntax / lexical errors instead of
    printing them, so callers can handle them programmatically.
    """

    def __init__(self):
        super().__init__()
        self.errors: list[ErrorResponse] = []

    def syntaxError(self, recognizer, offender_symbol, line, column, msg, e):
        """Called by ANTLR when a syntax error is detected."""
        self.errors.append(
            ErrorResponse(
                message=msg,
                line_number=line,
                column_number=column,
            )
        )

    def reportAmbiguity(self, recognizer, dfa, start_index, stop_index,
                        exact, ambiguity_alts, configs):
        """Called when the parser detects ambiguity."""
        token_stream = recognizer.getInputStream()
        token  = token_stream.tokens[start_index]
        column = token.column
        msg    = f"Ambiguity detected at token indices {start_index}–{stop_index}"

        self.errors.append(
            ErrorResponse(
                message=f"ambiguity: {msg}",
                line_number=token.line,
                column_number=column,
            )
        )

    def reportAttemptingFullContext(self, recognizer, dfa, start_index,
                                    stop_index, conflicting_alts, configs):
        pass  # Not critical for this language

    def reportContextSensitivity(self, recognizer, dfa, start_index,
                                 stop_index, prediction, configs):
        pass  # Not critical for this language

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_error_report(self) -> str:
        """Return a human-readable summary of all collected errors."""
        if not self.errors:
            return "No errors found"

        lines = [f"Found {len(self.errors)} error(s):"]
        for i, error in enumerate(self.errors, 1):
            lines.append(
                f"  {i}. Line {error.line_number}:{error.column_number} — {error.message}"
            )
        return "\n".join(lines)