from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit


def absolute_error(reference: complex, estimate: complex) -> float:
    return float(abs(reference - estimate))


def mean_z_error(reference: complex, estimate: complex) -> float:
    return absolute_error(reference, estimate)


def transpile_cost(transpiled: QuantumCircuit) -> dict[str, int]:
    counts = transpiled.count_ops()
    cx_count = int(counts.get("cx", 0))
    swap_count = int(counts.get("swap", 0))
    depth = transpiled.depth()
    return {
        "depth": int(depth),
        "total_gates": int(sum(counts.values())),
        "cx_count": cx_count,
        "one_qubit_gates": int(sum(counts.get(name, 0) for name in ("u", "u1", "u2", "u3", "rx", "ry", "rz", "sx", "x", "y", "z"))),
        "two_qubit_gates": cx_count + swap_count,
        "swap_count": swap_count,
    }


def circuit_fidelity(reference_state: np.ndarray, candidate_state: np.ndarray) -> float:
    ref = reference_state / np.linalg.norm(reference_state)
    cand = candidate_state / np.linalg.norm(candidate_state)
    overlap = np.vdot(ref, cand)
    return float(abs(overlap) ** 2)
