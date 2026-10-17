from __future__ import annotations

from dataclasses import dataclass

import numpy as np


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_list(ops: list[np.ndarray]) -> np.ndarray:
    result = np.array([[1.0]], dtype=complex)
    for op in ops:
        result = np.kron(result, op)
    return result


@dataclass(frozen=True)
class SpinChainProblem:
    n_qubits: int = 4
    j_xy: float = 1.0
    j_zz: float = 0.8
    h_field: float = 0.4
    final_time: float = 1.0

    def __post_init__(self) -> None:
        if self.n_qubits < 2:
            raise ValueError("n_qubits must be at least 2 for a spin chain")
        if not np.isfinite(self.j_xy):
            raise ValueError("j_xy must be finite")
        if not np.isfinite(self.j_zz):
            raise ValueError("j_zz must be finite")
        if not np.isfinite(self.h_field):
            raise ValueError("h_field must be finite")

    def dense_hamiltonian(self) -> np.ndarray:
        n = self.n_qubits
        H = np.zeros((2**n, 2**n), dtype=complex)

        for i in range(n - 1):
            xx = kron_list([X if q in (i, i + 1) else I2 for q in range(n)])
            yy = kron_list([Y if q in (i, i + 1) else I2 for q in range(n)])
            zz = kron_list([Z if q in (i, i + 1) else I2 for q in range(n)])
            H += 0.5 * self.j_xy * (xx + yy) + self.j_zz * zz

        for i in range(n):
            z_op = kron_list([Z if q == i else I2 for q in range(n)])
            H += self.h_field * z_op

        return H

    def initial_state(self) -> np.ndarray:
        psi = np.zeros(2**self.n_qubits, dtype=complex)
        psi[0] = 1.0
        return psi

    def hermiticity_error(self) -> float:
        H = self.dense_hamiltonian()
        return float(np.linalg.norm(H - H.conj().T))

    @property
    def total_z_observable(self) -> np.ndarray:
        n = self.n_qubits
        z_total = np.zeros((2**n, 2**n), dtype=complex)
        for i in range(n):
            op = kron_list([Z if q == i else I2 for q in range(n)])
            z_total += op
        return z_total

    def as_dict(self) -> dict[str, float | int]:
        return {
            "n_qubits": self.n_qubits,
            "j_xy": self.j_xy,
            "j_zz": self.j_zz,
            "h_field": self.h_field,
            "final_time": self.final_time,
        }
