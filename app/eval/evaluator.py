from typing import Any


class Evaluator:
    """
    Utility that coerces a raw Python value to its natural numeric form.
    Used primarily for cast() built-in return values.
    """

    @staticmethod
    def evaluate(target_text: Any) -> int | float | str | None:
        # BUG FIX: original code had int → float and float → int swapped
        if type(target_text) is int:
            return int(target_text)

        if type(target_text) is float:
            return float(target_text)

        if type(target_text) is str:
            return target_text

        # BUG FIX: returning None instead of -1 for unrecognised input
        return None