from dataclasses import dataclass

@dataclass
class Operator:
    # Arithmetic operators are numeric (+, -, *, /, %)
    _ARITH_OPS = {"+", "-", "*", "/", "%"}
    # Comparison operators produce BOOL
    _CMP_OPS   = {"==", "!=", "<", ">", "<=", ">="}
    # Logical operators require BOOL operands, produce BOOL
    _LOGIC_OPS = {"&&", "||"}

