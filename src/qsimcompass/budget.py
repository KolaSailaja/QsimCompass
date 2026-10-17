from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Budget:
    max_depth: int | None = None
    max_two_qubit_gates: int | None = None
    max_total_shots: int | None = None
    max_total_executions: int | None = None
    max_total_gates: int | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "Budget":
        if payload is None:
            return cls()
        return cls(
            max_depth=int(payload["max_depth"]) if payload.get("max_depth") is not None else None,
            max_two_qubit_gates=int(payload["max_two_qubit_gates"]) if payload.get("max_two_qubit_gates") is not None else None,
            max_total_shots=int(payload["max_total_shots"]) if payload.get("max_total_shots") is not None else None,
            max_total_executions=int(payload["max_total_executions"]) if payload.get("max_total_executions") is not None else None,
            max_total_gates=int(payload["max_total_gates"]) if payload.get("max_total_gates") is not None else None,
        )

    @staticmethod
    def _to_float(value: Any, default: float | None = None) -> float | None:
        if value is None:
            return default
        try:
            number = float(value)
        except (TypeError, ValueError):
            return default
        return number

    def check_candidate(self, row: dict[str, Any]) -> tuple[bool, list[str]]:
        violations: list[str] = []
        if self.max_depth is not None and int(row.get("compiled_depth", 0)) > self.max_depth:
            violations.append(f"depth {int(row.get('compiled_depth',0))} exceeds max_depth={self.max_depth}")
        if self.max_two_qubit_gates is not None and int(row.get("cx_count", 0)) > self.max_two_qubit_gates:
            violations.append(f"cx_count {int(row.get('cx_count',0))} exceeds max_two_qubit_gates={self.max_two_qubit_gates}")
        if self.max_total_shots is not None and int(row.get("shots", 0)) > self.max_total_shots:
            violations.append(f"shots {int(row.get('shots',0))} exceeds max_total_shots={self.max_total_shots}")
        if self.max_total_executions is not None and int(row.get("total_executions", 0)) > self.max_total_executions:
            violations.append(f"total_executions {int(row.get('total_executions',0))} exceeds max_total_executions={self.max_total_executions}")
        if self.max_total_gates is not None and int(row.get("total_gates", 0)) > self.max_total_gates:
            violations.append(f"total_gates {int(row.get('total_gates',0))} exceeds max_total_gates={self.max_total_gates}")
        return (not violations, violations)

    def filter_feasible(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        feasible: list[dict[str, Any]] = []
        for row in rows:
            ok, _ = self.check_candidate(row)
            if ok:
                feasible.append(row)
        return feasible


def find_feasible_candidates(rows: list[dict[str, Any]], budget: Budget | dict[str, Any] | None) -> list[dict[str, Any]]:
    cfg = budget if isinstance(budget, Budget) else Budget.from_dict(budget)
    return cfg.filter_feasible(rows)
