# QSimCompass technical report

## 1. Selected problem statement

QSimCompass: Physics-Aware Strategy Selection for Noisy, Resource-Constrained Hamiltonian Simulation — PS-S-OI, Open Innovation: Custom Quantum Simulation.

This repository implements the project as a local research prototype under that objective. It does not claim official challenge compliance because no authoritative Master Guide or judging clarification was found in this workspace.

## 2. Motivation and formulation

The project investigates whether ideal Trotter error and compiled-circuit resource metrics are reliable predictors of observable-level accuracy on two explicit processor topologies. The benchmark compares exact dense evolution against product-formula evolution for a compact spin-chain system under a simple depolarizing noise model and fixed shot budgets.

## 3. Model and parameters

The implemented model is a four-qubit open XXZ chain:

H = \sum_{i=0}^{N-2}(0.5 J_xy (X_i X_{i+1} + Y_i Y_{i+1}) + J_zz Z_i Z_{i+1}) + h_field \sum_i Z_i

with:
- N = 4
- J_xy = 1.0
- J_zz = 0.8
- h_field = 0.4
- initial state = |0000>
- observable = total magnetization Z_total = \sum_i Z_i

These values are explicit local assumptions used in the project and are documented as such. They are not presented as official organizer values unless the official guide is inspected.

## 4. Exact-reference method

The exact evolution is computed by dense matrix exponentiation using SciPy `expm` on the full Hamiltonian matrix. The exact observable is computed from the resulting state vector and the total-Z operator. This serves as the reference for evaluating ideal Trotter error and noisy expectation error.

## 5. Trotter methods

The implementation includes both first-order and symmetric second-order Trotter product formulas. Circuit construction is in `src/qsimcompass/trotter.py`, and the exact/Trotter comparison is validated in the unit tests. The current code distinguishes ideal Trotter error from noisy expectation error and finite-shot sampling effects by keeping the exact reference separate from the measured noisy path.

## 6. Processor A and B

Processor A is a five-qubit linear chain with a compact coupling map.
Processor B is a nine-qubit sparse graph with richer connectivity than Processor A.

The actual config definitions are in:
- `processors/processor_A.json`
- `processors/processor_B.json`

The project compiles the same logical benchmark instances against both processors with fixed seeds and comparable transpilation settings.

## 7. Experimental protocol

The benchmark uses:
- times = [0.5, 1.0, 1.5]
- steps = [1, 2, 4, 8]
- orders = [1, 2]
- shots = 2048 (for the noisy execution path)
- compiler optimization level = 1
- fixed seed values per processor

The surrounding benchmark pipeline is orchestrated in `src/qsimcompass/benchmark.py`.

## 8. Results and evidence

The generated results are stored in:
- `results/tables/benchmark_summary.json`
- `results/metadata/experiment_config.json`
- `results/metadata/manifest.json`
- `results/figures/processor_a_second_order_error.png`

The project has validated:
- Hamiltonian Hermiticity
- Exact state norm preservation
- Trotter convergence on a small system
- Processor config parsing
- Budget-feasibility and advisor selection logic
- Minimal known-good noisy Aer execution

The earlier silent-`None` noisy path defect was fixed by using the correct Qiskit Aer API signature and measurement-based execution path.

## 9. Budget-aware advisor and trade-offs

The project includes budget filtering, Pareto-front analysis, regret calculations, and evidence-based recommendation logic. These modules are intentionally conservative: they avoid recommending infeasible or failed candidates and they report the active constraint set transparently.

## 10. Limitations and threats to validity

- No official guide was available in the repo, so the challenge-specific problem definition remains a locally documented research assumption.
- The project is not a formal official competition submission.
- The noisy model is a simple local depolarizing model, not a claimed hardware calibration.
- The notebook and full benchmark workflow are reproducible in the local environment but should be interpreted as research evidence, not as certified judging artifacts.

## 11. Security and reproducibility

The code enforces basic path containment and numeric validation for configuration and outputs. The project also stores a manifest with file hashes, but a checksum alone does not prove scientific correctness. The workspace is a local research prototype and should be treated as such.

## 12. Conclusion

This project demonstrates a working local scientific workflow for exact and Trotterized Hamiltonian simulation, realistic processor-aware transpilation metrics, and a budget-aware recommendation layer. It is a credible research prototype with real generated artifacts and a validated noisy Aer measurement path, but it remains explicitly limited by the absence of an official competition guide or unambiguous rule source.
