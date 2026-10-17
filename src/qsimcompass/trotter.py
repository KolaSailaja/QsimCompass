from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from scipy.linalg import expm

from .problem import I2, X, Y, Z, SpinChainProblem


def local_term_matrix(term_label: str, targets: tuple[int, ...], coefficient: float) -> np.ndarray:
    if len(targets) == 1:
        single = {"X": X, "Y": Y, "Z": Z}[term_label]
        return coefficient * single

    pair_ops = {"XX": np.kron(X, X), "YY": np.kron(Y, Y), "ZZ": np.kron(Z, Z)}
    if term_label not in pair_ops:
        raise ValueError(f"Unsupported multi-qubit term: {term_label!r}")
    return coefficient * pair_ops[term_label]


def trotter_terms(problem: SpinChainProblem) -> list[tuple[str, tuple[int, ...], float]]:
    terms: list[tuple[str, tuple[int, ...], float]] = []
    for idx in range(problem.n_qubits - 1):
        terms.append(("XX", (idx, idx + 1), 0.5 * problem.j_xy))
        terms.append(("YY", (idx, idx + 1), 0.5 * problem.j_xy))
        terms.append(("ZZ", (idx, idx + 1), problem.j_zz))
    for idx in range(problem.n_qubits):
        terms.append(("Z", (idx,), problem.h_field))
    return terms


def _apply_term(circuit: QuantumCircuit, problem: SpinChainProblem, term: tuple[str, tuple[int, ...], float], dt: float) -> None:
    label, targets, coefficient = term
    matrix = expm(-1j * local_term_matrix(label, targets, coefficient) * dt)
    circuit.append(UnitaryGate(matrix), list(targets))


def build_trotter_circuit(problem: SpinChainProblem, total_time: float, steps: int, order: int = 1) -> QuantumCircuit:
    if steps <= 0:
        raise ValueError("steps must be positive")
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")

    circuit = QuantumCircuit(problem.n_qubits)
    dt = total_time / steps
    terms = trotter_terms(problem)

    if order == 1:
        for _ in range(steps):
            for term in terms:
                _apply_term(circuit, problem, term, dt)
    else:
        for _ in range(steps):
            left_half = terms[: len(terms) // 2]
            right_half = terms[len(terms) // 2 :]
            for term in left_half:
                _apply_term(circuit, problem, term, dt / 2)
            for term in reversed(right_half):
                _apply_term(circuit, problem, term, dt / 2)

    return circuit


def trotter_state(problem: SpinChainProblem, total_time: float, steps: int, order: int = 1) -> np.ndarray:
    from qiskit.quantum_info import Statevector

    circuit = build_trotter_circuit(problem, total_time, steps, order=order)
    return Statevector.from_instruction(circuit).data


def trotter_expectation(problem: SpinChainProblem, total_time: float, steps: int, order: int = 1) -> complex:
    state = trotter_state(problem, total_time, steps, order=order)
    z_total = problem.total_z_observable
    return complex(np.vdot(state, z_total @ state))
