from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
GOLDEN_DATASET = DATA_DIR / "golden.jsonl"

PROMPTS_DIR = PROJECT_ROOT / "prompts"
SYSTEM_PROMPT = PROMPTS_DIR / "system_v2.txt"
JUDGE_PROMPT = PROMPTS_DIR / "judge_v1.txt"

RESULTS_DIR = PROJECT_ROOT / "results"

MODEL_NAME = "qwen2.5:7b"

RESULTS_DIR.mkdir(exist_ok=True)