from antlr4.error.ErrorListener import ErrorListener
from app.models.CustomError import ErrorResponse, MarkerSeverity

class RPLErrorListener(ErrorListener):
    """
    Custom error listener that collects errors instead of printing them.
    """

    def __init__(self):
        super().__init__()
        self.errors: list[ErrorResponse] = []

    def syntaxError(self, recognizer, offender_symbol, line, column, msg, e):
        """Called when a syntax error occurs."""
        error = ErrorResponse(
            column_number = column,
            line_number = line,
            message = msg
        )
        self.errors.append(error)

    def reportAmbiguity(self, recognizer, dfa, start_index, stop_index,
                        exact, ambiguity_alts, configs):
        """Called when parser detects ambiguity."""
        token_stream = recognizer.getInputStream()
        token = token_stream.tokens[start_index]


        column = token.column
        msg = f"Ambiguity detected at indices {start_index}-{stop_index}"

        error = ErrorResponse(
            column_number=column,
            line_number=stop_index,
            message=f"ambiguity: {msg}"
        )

        self.errors.append(error)
        print(f"⚠️  {msg}")

    def reportAttemptingFullContext(self, recognizer, dfa, start_index,
                                    stop_index, conflicting_alts, configs):
        """Called when parser attempts full context."""
        pass  # Usually not critical

    def reportContextSensitivity(self, recognizer, dfa, start_index,
                                 stop_index, prediction, configs):
        """Called when parser detects context sensitivity."""
        pass  # Usually not critical

    def has_errors(self):
        """Check if any errors were collected."""
        return len(self.errors) > 0

    def get_error_report(self):
        """Get formatted error report."""
        if not self.errors:
            return "No errors found"

        report = f"Found {len(self.errors)} error(s):\n"
        for i, error in enumerate(self.errors, 1):
            if 'line' in error:
                report += f"  {i}. Line {error.line_number}:{error.column_number} - "
                report += f"{error.message}\n"
            else:
                report += f"  {i}. {error.message}\n"
        return report

