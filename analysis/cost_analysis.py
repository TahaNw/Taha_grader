import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
DIRECT_COST_PER_REQUEST = 0.0
GPU_COST_PER_HOUR = 0.0

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

def main():

    result_path = find_latest_result_file()
    results = load_results(result_path)

    total_requests = len(results)

    total_generation_time = sum(
        result["generation_latency_seconds"]
        for result in results
    )

    total_judge_time = sum(
        result["judge_latency_seconds"]
        for result in results
    )

    total_harness_time = sum(
        result["total_latency_seconds"]
        for result in results
    )

    average_generation_time = (
        total_generation_time / total_requests
        if total_requests
        else 0
    )

    average_judge_time = (
        total_judge_time / total_requests
        if total_requests
        else 0
    )

    average_harness_time = (
        total_harness_time / total_requests
        if total_requests
        else 0
    )

    system_cost = (
        total_requests * DIRECT_COST_PER_REQUEST
    )

    cost_per_1000 = (
        DIRECT_COST_PER_REQUEST * 1000
    )

    generation_hours = total_generation_time / 3600

    operational_cost = (
        generation_hours * GPU_COST_PER_HOUR
    )

    operational_cost_per_1000 = (
        average_generation_time / 3600
        * GPU_COST_PER_HOUR
        * 1000
    )

    print("=" * 60)
    print("COST ANALYSIS")
    print("=" * 60)

    print(f"Result file: {result_path.name}")

    print()
    print("SYSTEM")
    print("-" * 60)

    print(f"Requests evaluated: {total_requests}")

    print(
        f"Total generation time: "
        f"{total_generation_time:.2f} seconds"
    )

    print(
        f"Average generation latency: "
        f"{average_generation_time:.2f} seconds/request"
    )

    print(
        f"Direct API cost: "
        f"${system_cost:.2f}"
    )

    print(
        f"Direct cost per 1,000 requests: "
        f"${cost_per_1000:.2f}"
    )

    print()
    print("JUDGE")
    print("-" * 60)

    print(
        f"Total judge time: "
        f"{total_judge_time:.2f} seconds"
    )

    print(
        f"Average judge latency: "
        f"{average_judge_time:.2f} seconds/request"
    )

    print()
    print("FULL HARNESS")
    print("-" * 60)

    print(
        f"Total harness inference time: "
        f"{total_harness_time:.2f} seconds"
    )

    print(
        f"Average total latency per item: "
        f"{average_harness_time:.2f} seconds"
    )

    print(
        "LLM calls per item: 2 "
        "(system + judge)"
    )

    print(
        f"Total LLM calls: "
        f"{total_requests * 2}"
    )

    print()
    print("100x SCALE")
    print("-" * 60)

    requests_100x = total_requests * 100

    estimated_system_time_100x = (
        average_generation_time
        * requests_100x
    )

    estimated_judge_time_100x = (
        average_judge_time
        * requests_100x
    )

    print(
        f"Requests: "
        f"{requests_100x:,}"
    )

    print(
        f"Estimated system generation time: "
        f"{estimated_system_time_100x / 3600:.2f} hours"
    )

    print(
        f"Estimated judge time: "
        f"{estimated_judge_time_100x / 3600:.2f} hours"
    )

    print(
        f"Direct system cost at 100x: "
        f"${cost_per_1000 * 100:.2f}"
    )

    print()
    print("OPTIONAL GPU OPERATING COST")
    print("-" * 60)

    print(
        f"GPU cost/hour configured: "
        f"${GPU_COST_PER_HOUR:.2f}"
    )

    print(
        f"Current run operational cost: "
        f"${operational_cost:.2f}"
    )

    print(
        f"Operational cost per 1,000 requests: "
        f"${operational_cost_per_1000:.2f}"
    )


if __name__ == "__main__":
    main()