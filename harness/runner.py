import json
from datetime import datetime
from .config import GOLDEN_DATASET, RESULTS_DIR, SYSTEM_PROMPT
from .judge import judge_answer
from .llm import generate_response
from .utils import build_prompt, load_text_file

def load_dataset() -> list[dict]:

    items = []

    with open(GOLDEN_DATASET, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            items.append(json.loads(line))

    return items

def save_result(result: dict, output_file) -> None:

    output_file.write(
        json.dumps(result, ensure_ascii=False)
        + "\n"
    )


def run_evaluation() -> None:

    print("Loading dataset...")

    items = load_dataset()

    print(f"Loaded {len(items)} items.")

    system_prompt_template = load_text_file(SYSTEM_PROMPT)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = RESULTS_DIR / f"run_{timestamp}.jsonl"

    print(f"Results will be saved to: {output_path}")
    print()

    with open(output_path, "w", encoding="utf-8") as output_file:

        for index, item in enumerate(items, start=1):

            print(
                f"[{index}/{len(items)}] "
                f"Evaluating {item['id']}..."
            )

            system_prompt = build_prompt(
                system_prompt_template,
                item["customer_message"],
                item["policy"]
            )

            answer, generation_latency = generate_response(
                system_prompt
            )

            judge_result, judge_latency = judge_answer(
                item["customer_message"],
                item["policy"],
                answer
            )

            result = {
                "id": item["id"],
                "split": item["split"],
                "customer_message": item["customer_message"],
                "policy": item["policy"],
                "answer": answer,
                "score": judge_result.score,
                "reason": judge_result.reason,
                "generation_latency_seconds": round(
                    generation_latency,
                    3
                ),
                "judge_latency_seconds": round(
                    judge_latency,
                    3
                ),
                "total_latency_seconds": round(
                    generation_latency + judge_latency,
                    3
                ),
                "estimated_cost": 0.0
            }

            save_result(result, output_file)

            output_file.flush()

            print(
                f"  Score: {judge_result.score}/5"
            )

    print()
    print("Evaluation complete.")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    run_evaluation()