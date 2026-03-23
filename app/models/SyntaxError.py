from dataclasses import dataclass, field
from enum import IntEnum

class MarkerSeverity(IntEnum):
    Error = 8
    Warning = 4
    Info = 2
    Hint = 1


@dataclass
class ErrorResponse:
    message: str
    line_number: int
    column_number: int
    error_code: MarkerSeverity = field(default=MarkerSeverity.Error)



@dataclass
class WarningResponse:
    message: str
    line_number: int
    column_number: int
    warning_code: MarkerSeverity = field(default=MarkerSeverity.Warning)
