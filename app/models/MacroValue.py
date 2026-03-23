import math
from datetime import datetime
from typing import Dict, Union, NamedTuple, Optional


class MacroInfo(NamedTuple):
    value: Union[float, int]
    title: str
    description: str


class MacroValue:
    macro_info: Dict[str, MacroInfo] = {}

    @staticmethod
    def get_macro_info(key: str) -> Optional["MacroInfo"]:

        if not MacroValue.macro_info:
            now = datetime.now()

            MacroValue.macro_info = {
                "DAYS_IN_WEEK": MacroInfo(
                    value=now.weekday(),
                    title="Macro: DAYS_IN_WEEK",
                    description=f"DAYS_IN_WEEK expanded to current weekday: {now.weekday()} (0=Mon … 6=Sun).",
                ),
                "HOURS_IN_DAY": MacroInfo(
                    value=now.hour,
                    title="Macro: HOURS_IN_DAY",
                    description=f"HOURS_IN_DAY expanded to current hour: {now.hour}."
                ),
                "YEAR": MacroInfo(
                    value=now.year,
                    title="Macro: YEAR",
                    description=f"YEAR expanded to current year: {now.year}."
                ),
                "PI": MacroInfo(
                    value=math.pi,
                    title="Macro: PI",
                    description=f"PI expanded to current PI: {math.pi!r}."
                )
            }

        return MacroValue.macro_info.get(key)