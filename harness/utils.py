from pathlib import Path

def load_text_file(path: Path) -> str:

    return path.read_text(encoding="utf-8")


def build_prompt(
    template: str,
    customer_message: str,
    policy: str
) -> str:

    return template.format(
        customer_message=customer_message,
        policy=policy
    )