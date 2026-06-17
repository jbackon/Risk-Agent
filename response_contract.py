from pydantic import BaseModel
import json

class SummaryResponse(BaseModel):
    summary: str

def parse_response(response: str) -> SummaryResponse:
    if not response or not response.strip():
        raise ValueError("LLM returned an empty response — check the gateway URL and model ID.")
    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0]
    data = json.loads(cleaned)
    return SummaryResponse(**data)

def validate_response(response: SummaryResponse) -> bool:
    return bool(response.summary and response.summary.strip())
