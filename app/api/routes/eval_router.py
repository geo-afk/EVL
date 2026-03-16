from fastapi import APIRouter

from pydantic import BaseModel
from app.eval.eval import EVALAnalyzer
from app.models.Response import AnalysisResponse

eval_router = APIRouter()



class RunCodeRequest(BaseModel):
    code: str

@eval_router.post("/run_code")
def run_code(request: RunCodeRequest) -> AnalysisResponse:
    return EVALAnalyzer().analyze(request.code)