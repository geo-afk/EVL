from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Steps:
    id:          int
    phase:       str
    title:       str
    description: str
    line:        int
    output:      List[Any]
    details:     str
    changed:     str
    scope:       Optional[Dict[str, Any]] = None   # None = no scope context attached