from fastapi import APIRouter

eval_router = APIRouter()


@eval_router.get("/run_code")
def run_code():
    ...