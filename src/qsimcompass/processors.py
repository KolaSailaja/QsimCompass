from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from qiskit.transpiler import CouplingMap


@dataclass(frozen=True)
class ProcessorConfig:
    name: str
    num_qubits: int
    coupling_map: tuple[tuple[int, int], ...]
    basis_gates: tuple[str, ...]
    description: str
    optimization_level: int = 1
    seed: int = 42

    def validate(self) -> None:
        if self.num_qubits <= 0:
            raise ValueError("num_qubits must be positive")
        if any(a < 0 or b < 0 for a, b in self.coupling_map):
            raise ValueError("coupling map indices must be non-negative")
        if any(a >= self.num_qubits or b >= self.num_qubits for a, b in self.coupling_map):
            raise ValueError("coupling map indices must be within the qubit range")
        if len({(a, b) for a, b in self.coupling_map}) != len(self.coupling_map):
            raise ValueError("coupling map must not contain duplicate edges")

    def coupler(self) -> CouplingMap:
        return CouplingMap(list(self.coupling_map))


def load_processor_config(path: str | Path) -> ProcessorConfig:
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    config = ProcessorConfig(
        name=payload["name"],
        num_qubits=int(payload["num_qubits"]),
        coupling_map=tuple(tuple(edge) for edge in payload["coupling_map"]),
        basis_gates=tuple(payload["basis_gates"]),
        description=payload.get("description", ""),
        optimization_level=int(payload.get("optimization_level", 1)),
        seed=int(payload.get("seed", 42)),
    )
    config.validate()
    return config
