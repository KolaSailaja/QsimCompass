from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from .problem import SpinChainProblem


def exact_state(problem: SpinChainProblem, time: float) -> np.ndarray:
    psi0 = problem.initial_state()
    H = problem.dense_hamiltonian()
    return expm(-1j * H * time) @ psi0


def exact_expectation(problem: SpinChainProblem, time: float, observable: np.ndarray | None = None) -> complex:
    psi = exact_state(problem, time)
    obs = observable if observable is not None else problem.total_z_observable
    value = np.vdot(psi, obs @ psi)
    return complex(value)


def exact_z_total_expectation(problem: SpinChainProblem, time: float) -> complex:
    return exact_expectation(problem, time, problem.total_z_observable)


def exact_state_norm(problem: SpinChainProblem, time: float) -> float:
    psi = exact_state(problem, time)
    return float(np.linalg.norm(psi))
