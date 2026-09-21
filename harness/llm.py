import time
import ollama
from .config import MODEL_NAME


def generate_response(prompt: str) -> tuple[str, float]:

    start_time = time.perf_counter()

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    end_time = time.perf_counter()
    latency = end_time - start_time
    answer = response["message"]["content"]

    return answer, latency