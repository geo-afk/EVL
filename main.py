import uvicorn
import structlog


logger = structlog.get_logger("api")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    log_level = "info"

    uvicorn.run(
        "app.api.app:app",
        host= host,
        port= port,
        reload=True,  # Development only
        log_level=log_level,
    )


    logger.info(f"API server started on http://{host}:{port}")