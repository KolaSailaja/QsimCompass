from __future__ import annotations

import math
import random
from collections import defaultdict
from statistics import mean, median, pstdev
from typing import Any

import numpy as np

from .advisor import choose_best_strategy
from .budget import Budget, find_feasible_candidates


def compute_regret(selected_error: float, best_feasible_error: float) -> float:
    return max(float(selected_error) - float(best_feasible_error), 0.0)


def _scenario_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row.get("processor"),
        row.get("time"),
        row.get("order"),
        row.get("steps"),
    )


def evaluate_baselines(rows: list[dict[str, Any]], budget: Budget | dict[str, Any] | None = None, seed: int = 0) -> dict[str, Any]:
    scenarios: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        scenarios[_scenario_key(row)].append(row)

    policy_results: dict[str, list[float]] = {"random": [], "lowest_trotter_error": [], "lowest_resource_cost": [], "oracle": []}

    for scenario_rows in scenarios.values():
        feasible = find_feasible_candidates(scenario_rows, budget)
        if not feasible:
            continue
        oracle = min(feasible, key=lambda row: float(row.get("error", float("inf"))))
        oracle_error = float(oracle.get("error", float("inf")))

        random_choice = random.Random(seed).choice(feasible)
        policy_results["random"].append(compute_regret(float(random_choice.get("error", float("inf"))), oracle_error))

        lowest_theory = min(feasible, key=lambda row: float(row.get("ideal_error", row.get("error", float("inf")))))
        policy_results["lowest_trotter_error"].append(compute_regret(float(lowest_theory.get("error", float("inf"))), oracle_error))

        lowest_cost = min(feasible, key=lambda row: (int(row.get("compiled_depth", 0)), int(row.get("cx_count", 0)), int(row.get("shots", 0))))
        policy_results["lowest_resource_cost"].append(compute_regret(float(lowest_cost.get("error", float("inf"))), oracle_error))

        advisor = choose_best_strategy(feasible, budget=budget)
        selected = advisor["recommended_candidate"] if advisor.get("recommended_candidate") else oracle
        policy_results["oracle"].append(compute_regret(float(selected.get("error", float("inf"))), oracle_error))

    summary = {}
    for name, values in policy_results.items():
        if not values:
            summary[name] = {"mean_regret": None, "median_regret": None, "std_regret": None, "best_rate": 0.0}
            continue
        arr = np.array(values, dtype=float)
        summary[name] = {
            "mean_regret": float(np.mean(arr)),
            "median_regret": float(np.median(arr)),
            "std_regret": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
            "best_rate": float(np.mean(arr == 0.0)) if arr.size else 0.0,
        }

    return summary


def mean_regret(summary: dict[str, Any]) -> float:
    values = [item["mean_regret"] for item in summary.values() if item["mean_regret"] is not None]
    return float(np.mean(values)) if values else 0.0
