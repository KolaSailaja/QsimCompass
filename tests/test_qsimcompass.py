from __future__ import annotations

import math

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from src.qsimcompass.advisor import choose_best_strategy
from src.qsimcompass.benchmark import run_default_experiment
from src.qsimcompass.benchmark import noisy_total_z_expectation
from src.qsimcompass.budget import Budget
from src.qsimcompass.exact import exact_state, exact_z_total_expectation
from src.qsimcompass.pareto import pareto_front
from src.qsimcompass.problem import SpinChainProblem
from src.qsimcompass.processors import load_processor_config
from src.qsimcompass.regret import compute_regret
from src.qsimcompass.security import ensure_within_project, sanitize_filename, validate_numeric
from src.qsimcompass.trotter import build_trotter_circuit


def test_hamiltonian_hermitian() -> None:
    problem = SpinChainProblem()
    H = problem.dense_hamiltonian()
    np.testing.assert_allclose(H, H.conj().T, atol=1e-10)


def test_exact_state_norm_preserved() -> None:
    problem = SpinChainProblem()
    psi = exact_state(problem, 0.75)
    assert np.isclose(np.linalg.norm(psi), 1.0, atol=1e-9)


def test_trotter_matches_exact_reference_on_small_system() -> None:
    problem = SpinChainProblem()
    reference = exact_z_total_expectation(problem, 0.75)

    def trotter_error(steps: int) -> float:
        circuit = build_trotter_circuit(problem, 0.75, steps, order=2)
        state = Statevector.from_instruction(circuit).data
        estimate = np.vdot(state, problem.total_z_observable @ state)
        return abs(reference - complex(estimate))

    errors = [trotter_error(steps) for steps in (1, 2, 4, 8)]
    assert all(np.isfinite(error) for error in errors)
    assert max(errors) < 1e-10


def test_processor_file_parses() -> None:
    processor = load_processor_config("processors/processor_A.json")
    assert processor.num_qubits == 5
    assert processor.name == "Processor A"


def test_default_experiment_runs() -> None:
    results = run_default_experiment()
    assert results["status"] == "ok"
    assert len(results["rows"]) > 0


def test_noisy_expectation_uses_valid_noise_model() -> None:
    processor = load_processor_config("processors/processor_A.json")
    circuit = build_trotter_circuit(SpinChainProblem(), 0.5, 2, order=2)
    value = noisy_total_z_expectation(processor, circuit, shots=512)
    assert np.isfinite(value)
    assert value is not None


def test_budget_enforces_feasible_candidates() -> None:
    rows = [{"strategy": "A", "error": 0.01, "compiled_depth": 12, "cx_count": 10, "shots": 2000}, {"strategy": "B", "error": 0.05, "compiled_depth": 40, "cx_count": 80, "shots": 5000}]
    budget = Budget(max_depth=20, max_two_qubit_gates=50, max_total_shots=3000)
    feasible = budget.filter_feasible(rows)
    assert len(feasible) == 1
    assert feasible[0]["strategy"] == "A"


def test_advisor_recommends_lowest_error() -> None:
    rows = [{"strategy": "A", "error": 0.02, "compiled_depth": 10, "cx_count": 5, "shots": 1024}, {"strategy": "B", "error": 0.08, "compiled_depth": 8, "cx_count": 4, "shots": 1024}]
    recommendation = choose_best_strategy(rows)
    assert recommendation["recommended_strategy"] == "A"
    assert recommendation["best_feasible_error"] == 0.02


def test_regret_is_non_negative_and_zero_for_best_case() -> None:
    assert math.isclose(compute_regret(0.8, 0.5), 0.3, rel_tol=1e-12)
    assert compute_regret(0.5, 0.5) == 0.0


def test_pareto_front_is_correct() -> None:
    rows = [{"name": "A", "error": 0.1, "depth": 5}, {"name": "B", "error": 0.2, "depth": 4}, {"name": "C", "error": 0.11, "depth": 6}]
    front = pareto_front(rows, ["error", "depth"])
    names = {candidate["name"] for candidate in front}
    assert names == {"A", "B"}


def test_security_helpers_reject_invalid_values() -> None:
    with pytest.raises(ValueError):
        validate_numeric(float("nan"), name="bad")
    assert sanitize_filename("../evil.csv") == "evil.csv"
    assert ensure_within_project(".", ".").exists()
