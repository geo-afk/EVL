from fastapi import APIRouter, Request
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def load_system_prompt() -> str:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()


SYSTEM_PROMPT = load_system_prompt()


def normalize_source(code: str) -> str:
    lines = code.splitlines()
    return "\n".join(lines) + "\n"


@router.post("/complete")
async def ai_complete(req: Request):
    body = await req.json()
    line = body["line"].rstrip() + "\n"

    res = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Complete the following EVAL line.\n"
                    "Return ONLY the continuation text.\n\n"
                    f"{line}"
                ),
            },
        ],
        temperature=0,
        max_tokens=40,
    )

    return {"completion": res.choices[0].message.content.strip()}


@router.post("/insights")
async def ai_insights(req: Request):
    body = await req.json()
    code = normalize_source(body["code"])

    res = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": code},
        ],
        temperature=0,
    )

    return {"content": res.choices[0].message.content}