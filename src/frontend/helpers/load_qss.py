from pathlib import Path

def load_qss(*paths: Path, variables: dict[str, str] | None = None) -> str:
    chunks: list[str] = []

    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            chunks.append(f.read())

    qss = "\n\n".join(chunks)

    if variables:
        for key, value in variables.items():
            qss = qss.replace(f"{{{{{key}}}}}", value)

    return qss
