import structlog
import uvicorn

from app.eval.eval import EVALAnalyzer

# setup_logging()
logger = structlog.get_logger("api")


if __name__ == "__main__":

    # with open("./grammer/test.eval") as f:
    #     data = f.read()
    #
    # code = data
    # value = EVALAnalyzer().analyze(code)
    # print(value)
    host = "127.0.0.1"
    port = 8000
    log_level = "info"

    uvicorn.run(
        "app.app:app",
        host= host,
        port= port,
        reload=True,  # Development only
        log_level=log_level,
    )


    logger.info(f"API server started on http://{host}:{port}")