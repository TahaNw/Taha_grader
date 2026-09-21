import json
from .schema import JudgeResult

def parse_judge_result(raw_response: str) -> JudgeResult:

    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise ValueError("Judge returned invalid JSON.") from error

    return JudgeResult.model_validate(data)