from __future__ import annotations

from typing import Any


def dominates(a: dict[str, Any], b: dict[str, Any], objective_names: list[str], minimize: bool = True) -> bool:
    if a == b:
        return False
    a_values = [float(a.get(name, 0.0)) for name in objective_names]
    b_values = [float(b.get(name, 0.0)) for name in objective_names]
    better_or_equal = True
    strictly_better = False
    for av, bv in zip(a_values, b_values):
        if minimize:
            if av > bv:
                better_or_equal = False
                break
            if av < bv:
                strictly_better = True
        else:
            if av < bv:
                better_or_equal = False
                break
            if av > bv:
                strictly_better = True
    return better_or_equal and strictly_better


def pareto_front(rows: list[dict[str, Any]], objective_names: list[str]) -> list[dict[str, Any]]:
    front: list[dict[str, Any]] = []
    for candidate in rows:
        dominated = False
        for other in rows:
            if other is candidate:
                continue
            if dominates(other, candidate, objective_names):
                dominated = True
                break
        if not dominated:
            front.append(candidate)
    return front


def pareto_summary(rows: list[dict[str, Any]], objective_names: list[str]) -> dict[str, Any]:
    front = pareto_front(rows, objective_names)
    dominated_count = len(rows) - len(front)
    return {"front": front, "front_size": len(front), "dominated_count": dominated_count}
