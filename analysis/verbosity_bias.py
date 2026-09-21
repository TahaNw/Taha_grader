import json
from pathlib import Path
import ollama

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "verbosity_bias_v1.txt"
MODEL_NAME = "qwen2.5:7b"

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

def create_padded_answer(answer):
    padding = """

Thank you for contacting our customer support team.

We understand that customer questions are important and we
appreciate you taking the time to contact us. We are always
happy to assist with questions and concerns.

Please note that customer satisfaction is important to us.
We appreciate your patience and understanding while reviewing
the information provided above.

If you have any other questions, please feel free to contact
our customer support team. We will be happy to assist you.

Thank you again for reaching out to us, and we appreciate
your business.

Best regards,
Customer Support
"""

    return answer + padding

def judge_answer(
    prompt_template,
    customer_message,
    policy,
    answer
):
    prompt = prompt_template.format(
        customer_message=customer_message,
        policy=policy,
        answer=answer
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
                "score": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5
                },
                "reason": {
                    "type": "string"
                }
            },
            "required": [
                "score",
                "reason"
            ]
        }
    )

    return json.loads(response["message"]["content"])


def main():

    result_path = find_latest_result_file()
    results = load_results(result_path)

    prompt_template = PROMPT_PATH.read_text(
        encoding="utf-8"
    )

    output_path = (
        RESULTS_DIR / "verbosity_bias_results.jsonl"
    )

    total = 0
    unchanged = 0
    increased = 0
    decreased = 0

    score_changes = []
    changed_items = []

    with open(output_path, "w", encoding="utf-8") as output_file:

        for index, result in enumerate(results, start=1):

            print(
                f"[{index}/{len(results)}] "
                f"Testing {result['id']}..."
            )

            original_answer = result["answer"]
            padded_answer = create_padded_answer(
                original_answer
            )

            original = judge_answer(
                prompt_template,
                result["customer_message"],
                result["policy"],
                original_answer
            )

            padded = judge_answer(
                prompt_template,
                result["customer_message"],
                result["policy"],
                padded_answer
            )

            original_score = original["score"]
            padded_score = padded["score"]

            score_change = padded_score - original_score

            total += 1
            score_changes.append(abs(score_change))

            if score_change == 0:
                unchanged += 1

            elif score_change > 0:
                increased += 1

                changed_items.append({
                    "id": result["id"],
                    "original_score": original_score,
                    "padded_score": padded_score,
                    "change": score_change
                })

            else:
                decreased += 1

                changed_items.append({
                    "id": result["id"],
                    "original_score": original_score,
                    "padded_score": padded_score,
                    "change": score_change
                })

            output = {
                "id": result["id"],

                "original": {
                    "score": original_score,
                    "reason": original["reason"]
                },

                "padded": {
                    "score": padded_score,
                    "reason": padded["reason"]
                },

                "score_change": score_change,

                "absolute_score_change": abs(
                    score_change
                )
            }

            output_file.write(
                json.dumps(
                    output,
                    ensure_ascii=False
                ) + "\n"
            )

            output_file.flush()

    increase_percentage = (
        increased / total * 100
        if total > 0
        else 0
    )

    decrease_percentage = (
        decreased / total * 100
        if total > 0
        else 0
    )

    unchanged_percentage = (
        unchanged / total * 100
        if total > 0
        else 0
    )

    average_absolute_change = (
        sum(score_changes) / len(score_changes)
        if score_changes
        else 0
    )

    print()
    print("=" * 60)
    print("VERBOSITY BIAS ANALYSIS")
    print("=" * 60)

    print(f"Total items: {total}")

    print()
    print("SCORE CHANGES")
    print("-" * 60)

    print(f"Unchanged: {unchanged}")
    print(
        f"Unchanged percentage: "
        f"{unchanged_percentage:.2f}%"
    )

    print(f"Increased after padding: {increased}")
    print(
        f"Increased percentage: "
        f"{increase_percentage:.2f}%"
    )

    print(f"Decreased after padding: {decreased}")
    print(
        f"Decreased percentage: "
        f"{decrease_percentage:.2f}%"
    )

    print()
    print(
        f"Average absolute score change: "
        f"{average_absolute_change:.3f}"
    )

    print()
    print("CHANGED ITEMS")
    print("-" * 60)

    if not changed_items:
        print("No score changes found.")

    else:
        for item in changed_items:
            print(
                f"{item['id']}: "
                f"{item['original_score']} -> "
                f"{item['padded_score']} "
                f"(change={item['change']})"
            )

    print()
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()