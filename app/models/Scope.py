from typing import Dict, Any

from pydantic import BaseModel



class Scope(BaseModel):
    parent: Any
    symbol: Dict[str, str]


class Symbol(BaseModel):
    name: str
    type: str
    scope: Scope
