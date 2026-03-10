from typing import Any

class Evaluator:


    @staticmethod
    def evaluate(target_text: Any) -> int | float:

        if type(target_text) is int:
            return float(target_text)

        if type(target_text) is float:
            return int(target_text)

        elif type(target_text) is str:
            return target_text

        return -1
