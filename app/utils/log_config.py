import sys
import logging
import structlog


def setup_logging(log_level: str = "INFO"):
    """
    Configure structured JSON logging using structlog.
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        force=True,
        level=getattr(logging, log_level.upper())
    )

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),  # Adds stack information
            structlog.processors.format_exc_info,  # Formats exception info

            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.MODULE,
                ]
            ),

            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
