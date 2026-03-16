from typing import List, Any

from app.models.Steps import Steps


class StepRecorder:
    def __init__(self):
        self._steps:  List[Steps] = []
        self._id: int = 0
        self._output: List[Any] = []

    def record(self, phase: str, title: str, description: str,
               line: int=0, scope=None, detail=None,
               changed: str="", is_output=False,
               output_line=None
    ):

        if is_output and output_line is not None:
            self._output.append(output_line)

        self._id += 1
        temp_steps = Steps(
            id=self._id,
            phase=phase,
            title=title,
            description=description,
            line=line,
            scope=scope,
            changed=changed,
            details=detail,
            output=list(self._output)
        )

        self._steps.append(temp_steps)


    @property
    def steps(self):
        return self._steps

    @property
    def final_output(self):
        return list(self._output)

