from fastapi import APIRouter

llm_router = APIRouter()


@llm_router.get("/insight")
def get_code_insight():
    ...




@llm_router.get("/code/results")
def get_code_results():
    pass