import json
from pathlib import Path
from sklearn.metrics import cohen_kappa_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "golden.jsonl"
RESULTS_DIR = PROJECT_ROOT / "results"

def load_dataset() -> dict:

    dataset = {}

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                item = json.loads(line)
                dataset[item["id"]] = item

    return dataset

def find_latest_result_file() -> Path:

    result_files = list(RESULTS_DIR.glob("run_*.jsonl"))

    if not result_files:
        raise FileNotFoundError(
            "No evaluation result files were found."
        )

    return max(
        result_files,
        key=lambda path: path.stat().st_mtime
    )

def load_results(path: Path) -> list[dict]:

    results = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                results.append(json.loads(line))

    return results

def main():

    dataset = load_dataset()

    result_path = find_latest_result_file()
    results = load_results(result_path)

    reference_scores = []
    judge_scores = []

    human_disagreements = []
    judge_disagreements = []

    for result in results:

        item_id = result["id"]

        if item_id not in dataset:
            print(
                f"Warning: {item_id} was not found "
                "in the golden dataset."
            )
            continue

        item = dataset[item_id]

        human_score_1 = item["labeler_1"]["score"]
        human_score_2 = item["labeler_2"]["score"]

        if human_score_1 != human_score_2:

            human_disagreements.append({
                "id": item_id,
                "labeler_1": human_score_1,
                "labeler_2": human_score_2,
                "reason_1": item["labeler_1"]["reason"],
                "reason_2": item["labeler_2"]["reason"]
            })

            continue

        reference_score = human_score_1

        judge_score = result["score"]

        reference_scores.append(reference_score)
        judge_scores.append(judge_score)

        if reference_score != judge_score:

            judge_disagreements.append({
                "id": item_id,
                "reference": reference_score,
                "judge": judge_score,
                "reason": result["reason"]
            })

    total_resolved = len(reference_scores)

    agreements = total_resolved - len(judge_disagreements)

    agreement_percentage = (
        agreements / total_resolved * 100
        if total_resolved > 0
        else 0
    )

    if total_resolved > 0:
        kappa = cohen_kappa_score(
            reference_scores,
            judge_scores
        )
    else:
        kappa = 0.0

    print("=" * 60)
    print("LLM JUDGE RELIABILITY")
    print("=" * 60)

    print(f"Result file: {result_path.name}")
    print(f"Total evaluated items: {len(results)}")

    print()
    print("HUMAN LABEL AGREEMENT")
    print("-" * 60)

    print(
        f"Human disagreements: "
        f"{len(human_disagreements)}"
    )

    print(
        f"Resolved items: "
        f"{total_resolved}"
    )

    print()
    print("JUDGE VS HUMAN REFERENCE")
    print("-" * 60)

    print(f"Agreements: {agreements}")
    print(f"Disagreements: {len(judge_disagreements)}")
    print(
        f"Exact agreement: "
        f"{agreement_percentage:.2f}%"
    )
    print(f"Cohen's Kappa: {kappa:.3f}")

    print()
    print("SCORE DISTRIBUTION")
    print("-" * 60)

    print("Score | Human Reference | Judge")

    for score in range(1, 6):

        reference_count = reference_scores.count(score)
        judge_count = judge_scores.count(score)

        print(
            f"  {score}   |"
            f"       {reference_count:3d}       |"
            f"  {judge_count:3d}"
        )


    print()
    print("HUMAN DISAGREEMENTS")
    print("-" * 60)

    if not human_disagreements:

        print("No human disagreements found.")

    else:

        for disagreement in human_disagreements:

            print(
                f"\n{disagreement['id']}: "
                f"labeler 1={disagreement['labeler_1']}, "
                f"labeler 2={disagreement['labeler_2']}"
            )

            print(
                f"Labeler 1 reason: "
                f"{disagreement['reason_1']}"
            )

            print(
                f"Labeler 2 reason: "
                f"{disagreement['reason_2']}"
            )

    print()
    print("JUDGE DISAGREEMENTS")
    print("-" * 60)

    if not judge_disagreements:

        print("No judge disagreements found.")

    else:

        for disagreement in judge_disagreements:

            print(
                f"\n{disagreement['id']}: "
                f"reference={disagreement['reference']}, "
                f"judge={disagreement['judge']}"
            )

            print(
                f"Judge reason: "
                f"{disagreement['reason']}"
            )


if __name__ == "__main__":
    main()