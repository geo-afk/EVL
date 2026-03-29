from antlr4 import InputStream
from antlr4.CommonTokenStream import CommonTokenStream
import structlog
from app.analyzer.semantic_analyzer import SemanticAnalyzer
from app.eval.error_listener import EVALErrorListener
from app.models.SyntaxError import ErrorResponse
from app.models.Response import AnalysisResponse
from generated.EVALLexer import EVALLexer
from generated.EVALParser import EVALParser





logger = structlog.get_logger(__name__)


class EVALAnalyzer:

    def analyze(self, eval_code: str) -> AnalysisResponse:
        tokens, lex_errors = self._lexical_analysis(eval_code)
        if lex_errors:
            return AnalysisResponse.from_errors_only(lex_errors)

        parse_tree, parse_errors = self._syntax_analysis(tokens)
        if parse_errors:
            print(parse_errors)
            return AnalysisResponse.from_errors_only(parse_errors)

        return self._semantic_analysis(parse_tree)


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
            # logger.error("syntax_analysis_failed", error=str(e))
            logger.error("syntax_analysis_failed", error=str(e), exc_info=True)
            return None, [ErrorResponse(
                message=f"Syntax analysis failed: {e}",
                line_number=0,
                column_number=0,
            )]


    @staticmethod
    def _semantic_analysis(parse_tree: EVALParser.ProgramContext) -> AnalysisResponse| ErrorResponse:
        logger.info("semantic_analysis_started")
        analyzer = SemanticAnalyzer()
        try:
            analyzer.visit(parse_tree)

            return AnalysisResponse.from_analysis(
                steps=analyzer.recorder.steps,
                output=analyzer.recorder.final_output,
                errors=analyzer.errors,
                warnings=analyzer.warnings,
            )

        except Exception as e:
            # logger.error("semantic_analysis_failed", error=str(e), exc_info=True)
            logger.error("semantic_analysis_failed", error=str(e), exc_info=True)

            return ErrorResponse(
                message=f"Syntax analysis failed: {e}",
                line_number=0,
                column_number=0,
            )

