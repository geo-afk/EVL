import structlog
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request


from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError

from app.api.routes.eval_router import eval_router
from app.api.routes.llm_router import llm_router
from app.utils.config import Config
from app.utils.log_config import setup_logging

setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(api: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    Handles client_db connections, cache, and other resources.
    """
    # Startup
    logger.info("application_starting")

    try:
        logger.info("metrics_initialized")

        yield  # Application is running

    finally:
        # Shutdown
        logger.info("application_shutting_down")


app = FastAPI(
    title="EVAL Compiler API",
    description="Arithmatic Evaluations Language Compiler with REST API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)




app.add_middleware(GZipMiddleware, minimum_size=1000)


# app.add_middleware(CSRFMiddleware)
# app.add_middleware(LoggingMiddleware)
# app.add_middleware(RateLimitMiddleware)
# app.add_middleware(ErrorHandlingMiddleware)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    """Handle validation errors with detailed messages."""
    logger.warning(
        "validation_error",
        path=request.url.path,
        errors=exc.errors()
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "body": exc.body
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(
        "unexpected_error",
        path=request.url.path,
        error=str(exc),
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config().get("CLIENT_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eval_router)
app.include_router(llm_router)
