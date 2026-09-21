import json
import time
import ollama
from .config import JUDGE_PROMPT, MODEL_NAME
from .schema import JudgeResult
from .utils import load_text_file


def judge_answer(
    customer_message: str,
    policy: str,
    answer: str
) -> tuple[JudgeResult, float]:

    prompt_template = load_text_file(JUDGE_PROMPT)

    prompt = prompt_template.format(
        customer_message=customer_message,
        policy=policy,
        answer=answer
    )

    start_time = time.perf_counter()

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=JudgeResult.model_json_schema()
    )

    end_time = time.perf_counter()

    latency = end_time - start_time

    data = json.loads(response["message"]["content"])

    result = JudgeResult.model_validate(data)

    return result, latency