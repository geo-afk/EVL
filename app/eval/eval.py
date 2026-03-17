from antlr4 import InputStream
from antlr4.CommonTokenStream import CommonTokenStream
import structlog

from app.analyzer.semantic_analyzer import SemanticAnalyzer
from app.eval.error_listener import EVALErrorListener
from app.models.CustomError import ErrorResponse
from app.models.Response import AnalysisResponse
from generated.EVALLexer import EVALLexer
from generated.EVALParser import EVALParser

structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            }
        ),
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class EVALAnalyzer:
    """
    Orchestrates the three-phase analysis pipeline:
      1. Lexical analysis   — tokenise the source code.
      2. Syntax analysis    — build a parse tree.
      3. Semantic analysis  — type-check, resolve names, record execution steps.

    Returns an ``AnalysisResponse`` in all cases so the FastAPI route always
    has a consistent, typed object to return to the frontend.

    Unrecoverable internal failures (Python exceptions from the analyzer itself)
    are re-raised so FastAPI can return an appropriate 500 response.
    """

    def analyze(self, eval_code: str) -> AnalysisResponse:
        tokens, lex_errors = self._lexical_analysis(eval_code)
        if lex_errors:
            return AnalysisResponse.from_errors_only(lex_errors)

        parse_tree, parse_errors = self._syntax_analysis(tokens)
        if parse_errors:
            return AnalysisResponse.from_errors_only(parse_errors)

        return self._semantic_analysis(parse_tree)

    # ── Phase 1: lexical analysis ─────────────────────────────────────────────

    @staticmethod
    def _lexical_analysis(eval_code: str) -> tuple[CommonTokenStream | None, list[ErrorResponse]]:
        logger.info("lexical_analysis_started")
        try:
            input_stream = InputStream(eval_code)
            lexer        = EVALLexer(input_stream)
            lexer.removeErrorListeners()
            error_listener = EVALErrorListener()
            lexer.addErrorListener(error_listener)
            stream = CommonTokenStream(lexer)
            stream.fill()
            return stream, error_listener.errors
        except Exception as e:
            logger.error("lexical_analysis_failed", error=str(e))
            return None, [ErrorResponse(
                message=f"Lexical analysis failed: {e}",
                line_number=0,
                column_number=0,
            )]

    # ── Phase 2: syntax analysis ──────────────────────────────────────────────

    @staticmethod
    def _syntax_analysis(
        token_stream: CommonTokenStream,
    ) -> tuple[EVALParser.ProgramContext | None, list[ErrorResponse]]:
        logger.info("syntax_analysis_started")
        try:
            parser = EVALParser(token_stream)
            parser.removeErrorListeners()
            error_listener = EVALErrorListener()
            parser.addErrorListener(error_listener)
            tree = parser.program()
            return tree, error_listener.errors
        except Exception as e:
            logger.error("syntax_analysis_failed", error=str(e))
            return None, [ErrorResponse(
                message=f"Syntax analysis failed: {e}",
                line_number=0,
                column_number=0,
            )]

    # ── Phase 3: semantic analysis ────────────────────────────────────────────

    @staticmethod
    def _semantic_analysis(parse_tree: EVALParser.ProgramContext) -> AnalysisResponse:
        logger.info("semantic_analysis_started")
        analyzer = SemanticAnalyzer()
        try:
            analyzer.visit(parse_tree)
        except Exception as e:
            # An unexpected Python exception means the analyzer itself crashed —
            # re-raise so FastAPI returns a 500 rather than swallowing it.
            # logger.error("semantic_analysis_failed", error=str(e), exc_info=True)
            logger.error("semantic_analysis_failed", error=str(e))
            # raise

        return AnalysisResponse.from_analysis(
            steps    = analyzer.recorder.steps,
            output   = analyzer.recorder.final_output,
            errors   = analyzer.errors,
            warnings = analyzer.warnings,
        )