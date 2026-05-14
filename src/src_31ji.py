from pathlib import Path
import json


def load_json(path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(data: dict, path, indent: int = 2) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=indent)

# 2026-05-14 04:44:58
