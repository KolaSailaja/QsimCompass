from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any


def validate_numeric(value: Any, *, allow_zero: bool = True, nonnegative: bool = False, name: str = "value") -> float:
    if value is None or isinstance(value, str) and value.strip() == "":
        raise ValueError(f"{name} cannot be empty")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if math.isnan(number) or math.isinf(number):
        raise ValueError(f"{name} must be finite")
    if nonnegative and number < 0:
        raise ValueError(f"{name} must be non-negative")
    if not allow_zero and number == 0:
        raise ValueError(f"{name} must be non-zero")
    return number


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return cleaned.strip("._") or "result"


def ensure_within_project(base_dir: str | Path, candidate: str | Path) -> Path:
    base = Path(base_dir).resolve()
    target = Path(candidate).resolve()
    try:
        target.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"Output path escapes the project directory: {candidate!r}") from exc
    return target


def validate_result_record(record: dict[str, Any]) -> None:
    required = ["processor", "time", "steps", "order", "error"]
    missing = [key for key in required if key not in record]
    if missing:
        raise ValueError(f"Result record missing required keys: {missing}")
    validate_numeric(record["time"], nonnegative=True, name="time")
    validate_numeric(record["steps"], nonnegative=True, name="steps")
    validate_numeric(record["order"], nonnegative=True, name="order")
    validate_numeric(record["error"], nonnegative=True, name="error")
