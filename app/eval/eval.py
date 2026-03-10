from antlr4 import InputStream
from antlr4.CommonTokenStream import CommonTokenStream

from app.analyzer.llm_analyzer import LLMAnalyzer
import structlog

from app.analyzer.semantic_analyzer import SemanticAnalyzer
from app.eval.error_listener import EVALErrorListener
from generated.EVALLexer import EVALLexer
from generated.EVALParser import EVALParser

structlog.configure(
    processors=[
        # Add line number and function name
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            }
        ),
        # Filter log levels
        structlog.stdlib.filter_by_level,
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Add log level
        structlog.stdlib.add_log_level,
        # Format the log message
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer()  # Pretty console output
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

class EVALAnalyzer:
    def __init__(self):
        self.llm_analyzer = LLMAnalyzer()


    def analyze(self, eval_code: str, use_llm: bool = False):

        tokens, lex_errors = self._lexical_analysis(eval_code)
        if not tokens:
            return {"errors": lex_errors}

        parse_tree, _, parse_errors = self._syntax_analysis(tokens)

        if not parse_tree:
            return {"errors": parse_errors}

        semantic_result = self._semantic_analysis(parse_tree)

        errors = semantic_result.get("errors")
        if errors:
            return {"errors": semantic_result["errors"]}

        # if use_llm:
        #     llm_result = self._llm_analysis(eval_code)
        #     return {
        #         "semantic_analysis": semantic_result["symbol_table"],
        #         "llm_analysis": llm_result
        #     }

        return semantic_result


    @staticmethod
    def _lexical_analysis(eval_code: str):
        logger.info("lexical_analysis_started")

        try:
            input_stream = InputStream(eval_code)
            lexer = EVALLexer(input_stream)


            lexer.removeErrorListeners()
            error_listener = EVALErrorListener()
            lexer.addErrorListener(error_listener)


            stream = CommonTokenStream(lexer)
            stream.fill()


            return stream, error_listener.errors

        except Exception as e:
            logger.error("Lexical_analysis_failed", error=str(e))
            return None, [f"Lexical analysis failed: {str(e)}"]



    @staticmethod
    def _syntax_analysis(token_stream: CommonTokenStream):
        logger.info("syntax_analysis_started")



        try:
            parser = EVALParser(token_stream)
            error_listener = EVALErrorListener()

            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)

            tree = parser.program()


            from antlr4.tree.Trees import Trees

            tree_string = Trees.toStringTree(tree, recog=parser)

            return tree, tree_string, error_listener.errors

        except Exception as e:
            logger.error("Syntax_analysis_failed", error=str(e))

            return None, "" ,[f"Syntax analysis failed: {str(e)}"]




    @staticmethod
    def _semantic_analysis(parse_tree: EVALParser.ProgramContext):
        logger.info("semantic_analysis_started")

        analyzer = SemanticAnalyzer()


        try:
            analyzer.visit(parse_tree)

            result = {}

            return result

        except Exception as e:
            # logger.error("Semantic_analysis_failed", error=str(e))
            logger.error("Semantic_analysis_failed", error=str(e), exc_info=True)

            return {}


    @staticmethod
    def _llm_analysis(self, rpl_code: str):
        logger.debug("llm_analysis_started")