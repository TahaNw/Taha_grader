import json
from pathlib import Path
import ollama

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "golden.jsonl"
RESULTS_DIR = PROJECT_ROOT / "results"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "position_bias_v1.txt"

MODEL_NAME = "qwen2.5:7b"

def load_dataset():
    dataset = {}

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                item = json.loads(line)
                dataset[item["id"]] = item

    return dataset

def find_latest_result_file():
    result_files = list(RESULTS_DIR.glob("run_*.jsonl"))

    if not result_files:
        raise FileNotFoundError(
            "No evaluation result files were found."
        )

    return max(
        result_files,
        key=lambda path: path.stat().st_mtime
    )

def load_results(path):
    results = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                results.append(json.loads(line))

    return results

def judge_pair(
    prompt_template,
    customer_message,
    policy,
    answer_a,
    answer_b
):
    prompt = prompt_template.format(
        customer_message=customer_message,
        policy=policy,
        answer_a=answer_a,
        answer_b=answer_b
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format={
            "type": "object",
            "properties": {
                "score_a": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5
                },
                "score_b": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5
                },
                "reason_a": {
                    "type": "string"
                },
                "reason_b": {
                    "type": "string"
                }
            },
            "required": [
                "score_a",
                "score_b",
                "reason_a",
                "reason_b"
            ]
        }
    )

    return json.loads(response["message"]["content"])

def main():

    dataset = load_dataset()

    result_path = find_latest_result_file()
    results = load_results(result_path)

    prompt_template = PROMPT_PATH.read_text(
        encoding="utf-8"
    )

    output_path = (
        RESULTS_DIR / "position_bias_results.jsonl"
    )

    total = 0
    unchanged = 0
    changed = 0

    score_changes = []
    changed_items = []

    with open(output_path, "w", encoding="utf-8") as output_file:

        for index, result in enumerate(results, start=1):

            item_id = result["id"]

            if item_id not in dataset:
                continue

            item = dataset[item_id]

            answer_a = result["answer"]

            answer_b = item["candidate_answer"]

            print(
                f"[{index}/{len(results)}] "
                f"Testing {item_id}..."
            )

            original = judge_pair(
                prompt_template,
                item["customer_message"],
                item["policy"],
                answer_a,
                answer_b
            )

            swapped = judge_pair(
                prompt_template,
                item["customer_message"],
                item["policy"],
                answer_b,
                answer_a
            )

            original_a_score = original["score_a"]
            original_b_score = original["score_b"]

            swapped_a_score = swapped["score_b"]
            swapped_b_score = swapped["score_a"]

            a_changed = (
                original_a_score != swapped_a_score
            )

            b_changed = (
                original_b_score != swapped_b_score
            )

            item_changed = a_changed or b_changed

            if item_changed:
                changed += 1
            else:
                unchanged += 1

            total += 1

            score_change_a = abs(
                original_a_score - swapped_a_score
            )

            score_change_b = abs(
                original_b_score - swapped_b_score
            )

            score_changes.extend([
                score_change_a,
                score_change_b
            ])

            if item_changed:

                changed_items.append({
                    "id": item_id,
                    "original_a": original_a_score,
                    "swapped_a": swapped_a_score,
                    "original_b": original_b_score,
                    "swapped_b": swapped_b_score
                })

            output = {
                "id": item_id,

                "original": {
                    "answer_a_score": original_a_score,
                    "answer_b_score": original_b_score,
                    "reason_a": original["reason_a"],
                    "reason_b": original["reason_b"]
                },

                "swapped": {
                    "answer_b_score": swapped_b_score,
                    "answer_a_score": swapped_a_score,
                    "reason_b": swapped["reason_a"],
                    "reason_a": swapped["reason_b"]
                },

                "answer_a_score_change": (
                    original_a_score - swapped_a_score
                ),

                "answer_b_score_change": (
                    original_b_score - swapped_b_score
                ),

                "position_changed": item_changed
            }

            output_file.write(
                json.dumps(
                    output,
                    ensure_ascii=False
                ) + "\n"
            )

            output_file.flush()

    position_change_percentage = (
        changed / total * 100
        if total > 0
        else 0
    )

    average_score_change = (
        sum(score_changes) / len(score_changes)
        if score_changes
        else 0
    )

    print()
    print("=" * 60)
    print("POSITION BIAS ANALYSIS")
    print("=" * 60)

    print(f"Total items: {total}")
    print(f"Unchanged items: {unchanged}")
    print(f"Changed items: {changed}")

    print(
        f"Position-dependent verdicts: "
        f"{position_change_percentage:.2f}%"
    )

    print(
        f"Average absolute score change: "
        f"{average_score_change:.3f}"
    )

    print()
    print("CHANGED ITEMS")
    print("-" * 60)

    if not changed_items:
        print("No position-dependent score changes found.")
    else:
        for item in changed_items:
            print(
                f"{item['id']}: "
                f"A {item['original_a']} -> "
                f"{item['swapped_a']}, "
                f"B {item['original_b']} -> "
                f"{item['swapped_b']}"
            )

    print()
    print(f"Results saved to: {output_path}")

if __name__ == "__main__":
    main()