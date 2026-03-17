import structlog
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.ai import router as ai_router

#from app.eval.eval import EVALAnalyzer

load_dotenv()

logger = structlog.get_logger("api")

app = FastAPI()

# CORS — REQUIRED FOR BROWSER REQUESTS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Register AI routes
app.include_router(ai_router, prefix="/api/ai")

@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    log_level = "info"

    uvicorn.run(
        "app.app:app",
        host=host,
        port=port,
        reload=True,  # Development only
        log_level=log_level,
    )

    logger.info(f"API server started on http://{host}:{port}")