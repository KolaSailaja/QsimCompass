from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .budget import Budget, find_feasible_candidates


@dataclass
class CandidateEvidence:
    strategy: str
    processor: str
    steps: int
    order: int
    error: float
    compiled_depth: int
    cx_count: int
    shots: int = 2048
    feasible: bool = True
    noise_error: float | None = None
    theoretical_error: float | None = None
    total_gates: int | None = None
    notes: str = ""

    def to_row(self) -> dict[str, Any]:
        return asdict(self)


def _normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item.setdefault("error", item.get("ideal_error", item.get("noisy_error", float("inf"))))
        item.setdefault("compiled_depth", item.get("compiled_depth", 0))
        item.setdefault("cx_count", item.get("cx_count", 0))
        item.setdefault("shots", item.get("shots", 2048))
        item.setdefault("order", 1)
        item.setdefault("strategy", f"{item.get('processor','processor')}-{item.get('order',1)}")
        normalized.append(item)
    return normalized


def evidence_based_selection(rows: list[dict[str, Any]], budget: Budget | dict[str, Any] | None = None) -> dict[str, Any]:
    working = _normalize_rows(rows)
    feasible = find_feasible_candidates(working, budget)
    if not feasible:
        return {
            "recommended_strategy": None,
            "mode": "evidence-based",
            "feasible_candidates": [],
            "reason": "No feasible candidate satisfies the active budgets.",
            "best_feasible_error": None,
            "budget": budget,
            "limitations": ["The active constraint set eliminated every candidate."],
        }

    best = min(feasible, key=lambda row: float(row.get("error", float("inf"))))
    all_errors = [float(row.get("error", float("inf"))) for row in feasible]
    alt = min(
        (row for row in feasible if row is not best),
        key=lambda row: float(row.get("error", float("inf"))),
        default=None,
    )

    return {
        "recommended_strategy": best.get("strategy", best.get("processor", "unknown")),
        "mode": "evidence-based",
        "recommended_candidate": best,
        "best_feasible_error": float(best.get("error", float("inf"))),
        "strongest_alternative": alt,
        "feasible_candidates": feasible,
        "reason": "Selected the lowest observed error among all admissible candidates under the current budget.",
        "mean_error": float(np.mean(all_errors)) if all_errors else None,
        "limitations": ["This recommendation is evidence-based and depends on the completed scenario set."],
        "budget": budget,
    }


def predictive_selection(rows: list[dict[str, Any]], budget: Budget | dict[str, Any] | None = None) -> dict[str, Any]:
    working = _normalize_rows(rows)
    feasible = find_feasible_candidates(working, budget)
    if len(feasible) < 6:
        return evidence_based_selection(rows, budget)

    x = np.array(
        [
            [1.0, float(row.get("compiled_depth", 0)), float(row.get("cx_count", 0)), float(row.get("shots", 0)), float(row.get("order", 1))]
            for row in feasible
        ],
        dtype=float,
    )
    y = np.array([float(row.get("error", float("inf"))) for row in feasible], dtype=float)
    coef, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    preds = x @ coef
    candidate_scores = list(zip(feasible, preds))
    best = min(candidate_scores, key=lambda pair: float(pair[1]))[0]
    return {
        "recommended_strategy": best.get("strategy", best.get("processor", "unknown")),
        "mode": "predictive",
        "recommended_candidate": best,
        "predicted_error": float(np.min(preds)),
        "model_coefficients": {"intercept": float(coef[0]), "depth": float(coef[1]), "cx_count": float(coef[2]), "shots": float(coef[3]), "order": float(coef[4])},
        "feasible_candidates": feasible,
        "reason": "A simple linear predictor was trained on completed evaluations and used only because the dataset is large enough to justify predictive mode.",
        "budget": budget,
    }


def choose_best_strategy(rows: list[dict[str, Any]], budget: Budget | dict[str, Any] | None = None, use_predictive: bool = False) -> dict[str, Any]:
    if use_predictive:
        return predictive_selection(rows, budget)
    return evidence_based_selection(rows, budget)


def random_feasible_choice(rows: list[dict[str, Any]], budget: Budget | dict[str, Any] | None = None, seed: int = 0) -> dict[str, Any]:
    feasible = find_feasible_candidates(_normalize_rows(rows), budget)
    if not feasible:
        return {"recommended_strategy": None, "reason": "No feasible candidates for random selection."}
    rng = random.Random(seed)
    choice = rng.choice(feasible)
    return {"recommended_strategy": choice.get("strategy", choice.get("processor", "unknown")), "recommended_candidate": choice, "method": "random-feasible"}
