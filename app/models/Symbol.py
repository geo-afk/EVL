from dataclasses import dataclass

from app.models.Types import EvalType


@dataclass
class Symbol:
    name:      str
    eval_type: EvalType
    is_const:  bool      = False
    line:      int       = 0
    column:    int       = 0

