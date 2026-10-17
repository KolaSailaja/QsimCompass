# QSimCompass

This project evaluates whether ideal Trotter error and compiled circuit costs are reliable proxies for observable error under a small open-boundary XXZ spin-chain benchmark on Processor A and Processor B. The selected Phase 1 scope is a transparent local research prototype: Processor A and Processor B only; no Processor C/D implementation or scoring claims are included.

## Selected problem statement

QSimCompass: Physics-Aware Strategy Selection for Noisy, Resource-Constrained Hamiltonian Simulation — PS-S-OI, Open Innovation: Custom Quantum Simulation.

The current repository is a research prototype aligned to that statement, not a verified official competition submission. The underlying Hamiltonian, coefficients, and processor assumptions are locally documented and scientifically defensible, but they remain unverified against an authoritative guide in the workspace.

## Technical challenge and contribution

The project studies how first- and second-order Trotter product formulas compare to an exact dense reference for a compact four-qubit XXZ spin chain under explicit processor connectivity constraints and a simple depolarizing noise model. The contribution is a reproducible benchmark and advisor pipeline for comparing ideal and compiled-resource trade-offs under budget constraints.

## Supported Phase 1 scope

- Processor A: 5-qubit line topology
- Processor B: 9-qubit sparse connectivity graph
- Exact dense evolution and Trotterized evolution
- Ideal error, compiled circuit metrics, and a budget-aware advisor
- No Processor C/D implementation or Phase 2 work

## Scientific model

The local benchmark uses an open-boundary XXZ chain:

H = sum_{i=0}^{N-2} [0.5 * J_xy (X_i X_{i+1} + Y_i Y_{i+1}) + J_zz Z_i Z_{i+1}] + h_field * sum_i Z_i

with N = 4, J_xy = 1.0, J_zz = 0.8, h_field = 0.4, initial state |0000>, and total magnetization observable Z_total = sum_i Z_i.

This is not claimed to be the official organizer Hamiltonian unless a governing guide is later inspected. All values are explicit local assumptions, and the project remains honest about that limitation.

## Main validated results

- Exact dense evolution and Trotter comparison pass numeric validation.
- Default benchmark generation succeeds for the implemented local experiment.
- Noisy Aer execution is validated at the measurement layer with a finite expectation value rather than a silent None result.
- Full official-guide compliance remains blocked by the absence of an authoritative problem statement / Master Guide in the workspace.

## Reproduction

From a clean checkout on Windows PowerShell:

```powershell
cd C:\path\to\QSimCompass
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest tests/test_qsimcompass.py -q
python qsimcompass.py validate
python qsimcompass.py benchmark
python -m jupyter nbconvert --to notebook --execute main.ipynb --inplace
```

The benchmark writes:
- `results/tables/benchmark_summary.json`
- `results/metadata/experiment_config.json`
- `results/metadata/manifest.json`
- `results/figures/processor_a_second_order_error.png`

## Repository layout

- `src/qsimcompass/problem.py`: Hamiltonian construction and validation
- `src/qsimcompass/exact.py`: exact-reference evolution
- `src/qsimcompass/trotter.py`: Trotterized circuits
- `src/qsimcompass/processors.py`: processor config validation
- `src/qsimcompass/benchmark.py`: ideal/noisy benchmark orchestration
- `src/qsimcompass/advisor.py`: budget-aware strategy recommendation
- `src/qsimcompass/budget.py`: feasibility checks
- `src/qsimcompass/pareto.py`: Pareto-front logic
- `src/qsimcompass/security.py`: input and path validation
- `src/qsimcompass/cli.py`: CLI entrypoint
- `processors/processor_A.json`: Processor A definition
- `processors/processor_B.json`: Processor B definition
- `tests/test_qsimcompass.py`: validation suite
- `report.md`: technical narrative
- `main.ipynb`: benchmark notebook

## Architecture flow

```text
SpinChainProblem
      |
      v
exact reference + Trotter circuit builder
      |
      v
processor A / processor B transpilation
      |
      v
ideal error + compiled metrics + noisy Aer measurement
      |
      v
budget filter + advisor + Pareto analysis
      |
      v
JSON tables / metadata / plots
```

## Current limitations

- No official Master Guide or judging clarification was found in the repository, so all challenge-specific values remain explicitly labeled as local assumptions rather than verified official settings.
- The project is a transparent research prototype, not a guarantee of competition selection.
- The notebook and full end-to-end benchmark are valid but should be treated as reproducible local evidence, not certified official submission artifacts.
