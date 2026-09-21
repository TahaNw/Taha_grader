import json
from pathlib import Path
from sklearn.metrics import cohen_kappa_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "golden.jsonl"

def load_dataset() -> list[dict]:

    items = []

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                items.append(json.loads(line))

    return items

def main():

    items = load_dataset()

    labeler_1_scores = []
    labeler_2_scores = []

    disagreements = []

    for item in items:
        score_1 = item["labeler_1"]["score"]
        score_2 = item["labeler_2"]["score"]

        labeler_1_scores.append(score_1)
        labeler_2_scores.append(score_2)

        if score_1 != score_2:
            disagreements.append({
                "id": item["id"],
                "labeler_1": score_1,
                "labeler_2": score_2,
                "reason_1": item["labeler_1"]["reason"],
                "reason_2": item["labeler_2"]["reason"]
            })

    total_items = len(items)
    agreements = total_items - len(disagreements)

    agreement_percentage = (
        agreements / total_items * 100
        if total_items > 0
        else 0
    )

    kappa = cohen_kappa_score(
        labeler_1_scores,
        labeler_2_scores
    )

    print("=" * 50)
    print("HUMAN AGREEMENT ANALYSIS")
    print("=" * 50)

    print(f"Total items: {total_items}")
    print(f"Agreements: {agreements}")
    print(f"Disagreements: {len(disagreements)}")
    print(f"Agreement: {agreement_percentage:.2f}%")
    print(f"Cohen's Kappa: {kappa:.3f}")

    print()
    print("DISAGREEMENTS")
    print("-" * 50)

    if not disagreements:
        print("No disagreements found.")
    else:
        for disagreement in disagreements:
            print(f"\n{disagreement['id']}")
            print(
                f"Labeler 1: {disagreement['labeler_1']} "
                f"- {disagreement['reason_1']}"
            )
            print(
                f"Labeler 2: {disagreement['labeler_2']} "
                f"- {disagreement['reason_2']}"
            )


if __name__ == "__main__":
    main()