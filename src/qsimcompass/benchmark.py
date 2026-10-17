from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from qiskit import transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from .exact import exact_z_total_expectation
from .metrics import absolute_error, transpile_cost
from .problem import SpinChainProblem
from .processors import ProcessorConfig, load_processor_config
from .trotter import build_trotter_circuit


ROOT = Path(__file__).resolve().parents[2]


def _counts_to_total_z_expectation(counts: dict[str, int], n_qubits: int) -> float:
    shots = sum(counts.values())
    total = 0.0
    for bitstring, count in counts.items():
        z_value = 0.0
        for bit in bitstring:
            z_value += 1.0 if bit == "0" else -1.0
        total += z_value * count
    return float(total / shots / n_qubits)


def _noise_model_for_processor(processor: ProcessorConfig) -> NoiseModel:
    noise_model = NoiseModel()
    for gate in ("rz", "sx", "x"):
        noise_model.add_all_qubit_quantum_error(depolarizing_error(0.002, 1), gate)
    noise_model.add_all_qubit_quantum_error(depolarizing_error(0.01, 2), "cx")
    return noise_model


def noisy_total_z_expectation(processor: ProcessorConfig, circuit, shots: int = 2048) -> float:
    sim = AerSimulator(
        coupling_map=processor.coupler(),
        basis_gates=list(processor.basis_gates),
        noise_model=_noise_model_for_processor(processor),
        seed_simulator=processor.seed,
    )
    measured = circuit.copy()
    measured.measure_all()
    transpiled = transpile(
        measured,
        coupling_map=processor.coupler(),
        basis_gates=list(processor.basis_gates),
        optimization_level=processor.optimization_level,
        seed_transpiler=processor.seed,
    )
    result = sim.run(transpiled, shots=shots).result()
    counts = result.get_counts()
    if not counts:
        raise ValueError("Aer simulation returned no counts; the configured noise model did not produce a valid measurement result.")
    return _counts_to_total_z_expectation(counts, processor.num_qubits)


def compare_processor_results(problem: SpinChainProblem, processor: ProcessorConfig, times: list[float], steps_list: list[int]) -> list[dict]:
    rows: list[dict] = []
    for time in times:
        exact_value = exact_z_total_expectation(problem, time)
        for steps in steps_list:
            for order in (1, 2):
                circuit = build_trotter_circuit(problem, time, steps, order=order)
                state = Statevector.from_instruction(circuit).data
                trotter_expectation = complex(np.vdot(state, problem.total_z_observable @ state))
                error = absolute_error(exact_value, trotter_expectation)
                transpiled = transpile(circuit, coupling_map=processor.coupler(), basis_gates=list(processor.basis_gates), optimization_level=processor.optimization_level, seed_transpiler=processor.seed)
                compiled = transpile_cost(transpiled)
                noisy_value = noisy_total_z_expectation(processor, circuit)
                noisy_error = None if noisy_value is None else absolute_error(exact_value, noisy_value)
                rows.append(
                    {
                        "processor": processor.name,
                        "time": time,
                        "steps": steps,
                        "order": order,
                        "strategy": f"{processor.name}-order{order}-steps{steps}",
                        "exact": exact_value.real,
                        "trotter": trotter_expectation.real,
                        "ideal_error": error,
                        "error": error,
                        "compiled_depth": compiled["depth"],
                        "cx_count": compiled["cx_count"],
                        "total_gates": compiled["total_gates"],
                        "swap_count": compiled["swap_count"],
                        "shots": 2048,
                        "total_executions": 1,
                        "noisy_value": None if noisy_value is None else noisy_value,
                        "noisy_error": noisy_error,
                    }
                )
    return rows


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: path.read_bytes()[0:65536], b""):
        digest.update(chunk)
    return digest.hexdigest()


def run_default_experiment() -> dict:
    problem = SpinChainProblem(n_qubits=4, j_xy=1.0, j_zz=0.8, h_field=0.4, final_time=1.0)
    processor_a = load_processor_config(ROOT / "processors" / "processor_A.json")
    processor_b = load_processor_config(ROOT / "processors" / "processor_B.json")

    times = [0.5, 1.0, 1.5]
    steps_list = [1, 2, 4, 8]

    rows = []
    rows.extend(compare_processor_results(problem, processor_a, times, steps_list))
    rows.extend(compare_processor_results(problem, processor_b, times, steps_list))

    results_dir = ROOT / "results"
    table_path = results_dir / "tables" / "benchmark_summary.json"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    table_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    metadata_dir = results_dir / "metadata"
    config_path = metadata_dir / "experiment_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(
            {
                "problem": problem.as_dict(),
                "processors": {
                    "A": processor_a.__dict__,
                    "B": processor_b.__dict__,
                },
                "times": times,
                "steps": steps_list,
                "noise_model": "depolarizing_gate_noise",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    manifest = {
        "run_id": "default-benchmark",
        "files": {
            "benchmark_summary.json": _sha256_file(table_path),
            "experiment_config.json": _sha256_file(config_path),
        },
        "rows": len(rows),
        "status": "ok",
    }
    manifest_path = metadata_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {"status": "ok", "rows": rows, "table_path": str(table_path), "config_path": str(config_path), "manifest_path": str(manifest_path)}
