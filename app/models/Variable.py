from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass()
class Position:
    line: int
    column: int


@dataclass
class Variable:
    name:     str
    type:     str
    value:    Any
    position: Position
    constant: bool = False
