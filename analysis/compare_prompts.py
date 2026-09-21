import json
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

V1_FILE = RESULTS_DIR / "run_20260919_104338.jsonl"
V2_FILE = RESULTS_DIR / "run_20260919_160502.jsonl"


def load_results(path):
    results = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                item = json.loads(line)
                results[item["id"]] = item

    return results


def distribution(scores):
    return {
        score: scores.count(score)
        for score in range(1, 6)
    }


def main():
    v1 = load_results(V1_FILE)
    v2 = load_results(V2_FILE)

    test_ids = [
        item_id
        for item_id in v1
        if v1[item_id]["split"] == "test"
    ]

    v1_scores = [v1[item_id]["score"] for item_id in test_ids]
    v2_scores = [v2[item_id]["score"] for item_id in test_ids]

    v1_mean = mean(v1_scores)
    v2_mean = mean(v2_scores)

    print("=" * 60)
    print("V1 VS V2 TEST-SET COMPARISON")
    print("=" * 60)

    print(f"Test items: {len(test_ids)}")
    print()

    print("MEAN SCORE")
    print("-" * 60)
    print(f"v1 mean score: {v1_mean:.3f}")
    print(f"v2 mean score: {v2_mean:.3f}")
    print(f"Change: {v2_mean - v1_mean:+.3f}")
    print()

    print("SCORE DISTRIBUTION")
    print("-" * 60)

    v1_dist = distribution(v1_scores)
    v2_dist = distribution(v2_scores)

    print("Score | v1 | v2")
    for score in range(1, 6):
        print(f"  {score}   | {v1_dist[score]:2d} | {v2_dist[score]:2d}")

    print()

    changed = 0

    for item_id in test_ids:
        if v1[item_id]["score"] != v2[item_id]["score"]:
            changed += 1

    print(f"Items with changed scores: {changed}")
    print(f"Items unchanged: {len(test_ids) - changed}")


if __name__ == "__main__":
    main()