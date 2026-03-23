from __future__ import annotations

from app.models.Steps import Steps
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.models.SyntaxError import ErrorResponse, WarningResponse


# ── Scope ─────────────────────────────────────────────────────────────────────

class ScopeEntry(BaseModel):
    """
    A single variable captured in the scope snapshot at the moment a step was
    recorded.
    """
    type:  str
    value: Any
    const: bool

    model_config = {"frozen": True}


# ── Step ──────────────────────────────────────────────────────────────────────

class StepModel(BaseModel):
    """
    One recorded execution step produced by the semantic analyzer.

    Fields
    ──────
    id          Sequential step number (1-based).
    phase       Broad category: ``"analysis"`` | ``"declaration"`` |
                ``"assignment"`` | ``"output"`` | ``"control_flow"`` |
                ``"scope"``.
    title       Short human-readable label shown in the step list.
    description Full sentence explaining what happened at this step.
    line        Source line number this step refers to (0 when not applicable).
    changed     Name of the variable that was created or modified at this step,
                or an empty string when no variable changed.
    details     Extra context string (type/value annotations, error tags, etc.).
    scope       Snapshot of every variable visible at the moment this step was
                recorded, keyed by variable name.
    output      Ordered list of all ``print()`` outputs produced up to and
                including this step.
    """

    id:          int
    phase:       str
    title:       str
    description: str
    line:        int
    changed:     str
    details:     str
    scope:       Dict[str, ScopeEntry] = Field(default_factory=dict)
    output:      List[str]             = Field(default_factory=list)

    @classmethod
    def from_step(cls, step: Steps) -> "StepModel":
        scope: Dict[str, ScopeEntry] = {}
        if step.scope:
            for name, entry in step.scope.items():
                scope[name] = ScopeEntry(
                    type=str(entry.get("type", "")),
                    value=entry.get("value"),
                    const=bool(entry.get("const", False)),
                )

        return cls(
            id=step.id,
            phase=step.phase,
            title=step.title,
            description=step.description,
            line=step.line,
            changed=step.changed or "",
            details=step.details or "",
            scope=scope,
            output=[str(o) for o in (step.output or [])],
        )


# ── Diagnostics ───────────────────────────────────────────────────────────────

class DiagnosticModel(BaseModel):
    """
    A single error or warning produced during analysis.

    ``severity`` maps directly to Monaco Editor's ``MarkerSeverity`` values:
        8 = Error  |  4 = Warning  |  2 = Info  |  1 = Hint
    """

    message:       str
    line_number:   int
    column_number: int
    severity:      int

    @classmethod
    def from_error(cls, error: ErrorResponse) -> "DiagnosticModel":
        return cls(
            message=error.message,
            line_number=error.line_number,
            column_number=error.column_number,
            severity=int(error.error_code),
        )

    @classmethod
    def from_warning(cls, warning: WarningResponse) -> "DiagnosticModel":
        return cls(
            message=warning.message,
            line_number=warning.line_number,
            column_number=warning.column_number,
            severity=int(warning.warning_code),
        )


# ── Top-level response ────────────────────────────────────────────────────────

class AnalysisResponse(BaseModel):
    """
    The complete result of one analysis run, ready to be sent to the frontend.

    Fields
    ──────
    steps     Ordered list of every action the analyzer took.  The frontend
              can step through these to animate program execution.
    output    Ordered list of all values produced by ``print()`` statements.
              Mirrors the ``output`` field on the last step, provided here at
              the top level for convenience.
    errors    Semantic / syntactic errors.  Non-empty means the program has a
              problem the frontend should highlight.
    warnings  Non-fatal notices (unreachable code, implicit widening, etc.).
    has_errors
              Convenience flag so the frontend does not have to check
              ``len(errors) > 0``.
    """

    steps:      List[StepModel]      = Field(default_factory=list)
    output:     List[str]            = Field(default_factory=list)
    errors:     List[DiagnosticModel] = Field(default_factory=list)
    warnings:   List[DiagnosticModel] = Field(default_factory=list)
    has_errors: bool                 = False

    @classmethod
    def from_analysis(
        cls,
        steps:    List[Steps],
        output:   List[Any],
        errors:   List[ErrorResponse],
        warnings: List[WarningResponse],
    ) -> "AnalysisResponse":
        """
        Build an AnalysisResponse from the raw objects produced by
        SemanticAnalyzer and StepRecorder.

        Usage
        ─────
            return AnalysisResponse.from_analysis(
                steps    = analyzer.recorder.steps,
                output   = analyzer.recorder.final_output,
                errors   = analyzer.errors,
                warnings = analyzer.warnings,
            )
        """
        return cls(
            steps    = [StepModel.from_step(s) for s in steps],
            output   = [str(o) for o in output],
            errors   = [DiagnosticModel.from_error(e) for e in errors],
            warnings = [DiagnosticModel.from_warning(w) for w in warnings],
            has_errors = len(errors) > 0,
        )

    @classmethod
    def from_errors_only(cls, errors: List[ErrorResponse]) -> "AnalysisResponse":
        """
        Shortcut for the early-exit paths in EVALAnalyzer (lex / parse failures)
        where there are no steps or output to report.
        """
        return cls(
            errors     = [DiagnosticModel.from_error(e) for e in errors],
            has_errors = True,
        )