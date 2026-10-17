# QSimCompass — Project Status

**Status date:** 2026-10-17  
**Overall status:** **RESEARCH PROTOTYPE IMPLEMENTED; official competition-rule verification remains blocked** — the missing `qiskit-aer` native dependency chain was resolved by installing the official Microsoft Visual C++ 2022 x64 redistributable, and a compact spin-chain benchmark implementation was created and validated locally. The workspace still does not contain an authoritative competition guide, so all competition-specific values remain explicitly labeled as assumptions rather than verified official rules.  
**Registered track:** PS-S-OI — “Open Innovation: Custom Quantum Simulation” (reported by the user; not independently verified).

## Stage and handoff

- **Workspace audit:** Complete for the current files and environment; no preexisting project sources or scientific report were present.
- **Official-rule verification:** Blocked pending an authoritative rule/problem-statement source and deadline/submission details. No official Master Guide or PDF was found in the workspace or project state.
- **Environment validation:** Resolved. `qiskit-aer` imports successfully after installing the official Microsoft VC++ 2022 x64 runtime, which provides the missing `vcomp140.dll` dependency.
- **Experiment implementation:** Complete as a local research prototype: exact dense evolution, Trotterized product formulas, processor map definitions, and a benchmark pipeline are implemented and tested.
- **Next single action:** When an official guide is available, replace the assumed Hamiltonian, topology, and noise settings with exact competition values and align the implementation to the formal specification.

A later session must read this file and `CLAUDE.md` before substantial work. Preserve this one workspace as the canonical project. Competition-specific constants remain unverified unless an authoritative brief is explicitly inspected.

## Current work: noisy benchmark repair

- Fixed the real Aer noise-model bug in `src/qsimcompass/benchmark.py`: `depolarizing_error` now receives integer qubit counts (`1` or `2`) rather than a gate name string, matching the actual qiskit-aer API.
- Restored the noisy expectation path to execute a measured circuit and raise clear exceptions if Aer returns no counts, instead of silently returning `None` and hiding invalid/noisy results.
- Added a regression test in `tests/test_qsimcompass.py` that exercises a valid noisy measurement and asserts a finite expectation value is returned.

### Changed files
- `src/qsimcompass/benchmark.py`
- `tests/test_qsimcompass.py`

### Commands actually run
- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe -c "from src.qsimcompass.processors import load_processor_config; from src.qsimcompass.problem import SpinChainProblem; from src.qsimcompass.trotter import build_trotter_circuit; from src.qsimcompass.benchmark import noisy_total_z_expectation; p=load_processor_config('processors/processor_A.json'); c=build_trotter_circuit(SpinChainProblem(), 0.5, 2, order=2); v=noisy_total_z_expectation(p, c, shots=256); print(type(v).__name__, v)"`
- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe -m pytest tests/test_qsimcompass.py -q -k 'noisy_expectation_uses_valid_noise_model or default_experiment_runs'`

### Observed results
- Minimal noisy Aer execution produced a finite value: `float 0.5953125`.
- The benchmark was validated at the actual noise-model layer; the previous silent-`None` behavior is fixed.

### Unresolved issue
- A full end-to-end benchmark run remains computationally slow in this environment, but the underlying scientific path is now valid and measured instead of hidden behind a swallowed exception.

## Completed work this stage

- Built a compact Python package under `src/qsimcompass` with modules for the problem definition, exact solver, Trotter circuit builder, processor config, benchmark orchestration, and plotting.
- Added processor configuration files under `processors/` for Processor A and B, plus a top-level `experiment_config.json`.
- Added executable project entrypoint `qsimcompass.py` and supporting project docs (`README.md`, `report.md`, `main.ipynb`).
- Added validation tests under `tests/test_qsimcompass.py` and generated benchmark artifacts in `results/`.

### Changed files

- `src/qsimcompass/__init__.py`
- `src/qsimcompass/problem.py`
- `src/qsimcompass/exact.py`
- `src/qsimcompass/trotter.py`
- `src/qsimcompass/processors.py`
- `src/qsimcompass/benchmark.py`
- `src/qsimcompass/metrics.py`
- `src/qsimcompass/visualization.py`
- `qsimcompass.py`
- `requirements.txt`
- `processors/processor_A.json`
- `processors/processor_B.json`
- `experiment_config.json`
- `README.md`
- `report.md`
- `main.ipynb`
- `tests/test_qsimcompass.py`

### Commands actually run

- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe -m pip install --force-reinstall qiskit-aer==0.17.2`
- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe -c "import qiskit, qiskit_aer; print('qiskit', qiskit.__version__); print('aer', qiskit_aer.__version__)"`
- `& 'C:\Users\SAILAJA\Desktop\QSimCompass\vc_redist_2022_x64.exe' /install /quiet /norestart`
- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe -m pytest tests/test_qsimcompass.py -q`
- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe qsimcompass.py`
- `cd "C:\Users\SAILAJA\Desktop\QSimCompass"; .\.venv\Scripts\python.exe -c "from src.qsimcompass.visualization import plot_ideal_error_summary; print(plot_ideal_error_summary('results/tables/benchmark_summary.json'))"`

### Observed results

- `qiskit` and `qiskit_aer` import successfully after installing the VC++ 2022 x64 runtime.
- `pytest` passed: `5 passed in 6.39s`.
- Project entrypoint completed successfully and generated 48 benchmark rows.
- Plot artifact created at `results/figures/processor_a_second_order_error.png`.

### Unresolved issues

- There is still no authoritative competition guide or problem statement in the workspace; the current implementation is an explicitly documented research prototype rather than a verified competition submission.
- The Hamiltonian and processor assumptions are chosen to be scientifically consistent and reproducible, but they must be replaced with formal rules if they become available.

### One next action

- Obtain the official Master Guide and align the model, observables, noise model, and processor assumptions to the published values before claiming competition compliance.

## What was inspected

- Workspace root: `C:\Users\SAILAJA\Desktop\QSimCompass`, including hidden entries and files/directories through depth 4.
- The initial workspace contained only `.venv`; this session's full file inventory (excluding `.venv` contents) contains only `PROJECT_STATUS.md` and `CLAUDE.md`. No source, tests, notebook, configuration, results, README, research report, or official guide is present.
- Global Python: `C:\Python314\python.exe`, Python 3.14.4. It was the resolved `python` in the inspected PowerShell process; `VIRTUAL_ENV` was unset.
- Workspace interpreter: `.venv\Scripts\python.exe`, also Python 3.14.4. It is not the active interpreter in that process.
- `.venv` package inventory: `pip==26.0.1` only; no quantum-computing packages.
- `git status --short --branch` failed because the workspace is not a Git repository.
- The user supplied `Pasted text #1.txt`, which contains project instructions and assertions about the competition, but it is not itself the official Master Guide or research report. Its asserted processor budgets, track scope, and October 14, 2026 deadline remain unverified.
- A web search found an IBM Qiskit Fall Fest 2026 host-application announcement, but not an authoritative Phase 1 competition guide or submission deadline. The exact track search returned no result. This does not verify the attachment's competition-specific assertions.
- PyPI JSON metadata was queried for Python requirements and release wheel files. This is package metadata, not an installation or import test. The runtime dependency set remains unvalidated.

## Evidence and requirements register

| Item | Status | Source / note |
|---|---|---|
| Workspace path and contents described above | VERIFIED | Local inspection, 2026-10-17 |
| Global and workspace Python versions and current activation state | VERIFIED | Local interpreter checks, 2026-10-17 |
| No quantum packages in `.venv` | VERIFIED | `.venv` package inventory, 2026-10-17 |
| No implementation, tests, research report, or official guide in the current workspace | VERIFIED | Full workspace file inventory, 2026-10-17 |
| Workspace is not a Git repository | VERIFIED | `git status --short --branch` returned fatal: not a git repository |
| Registered track label | UNVERIFIED | User-provided; no official entry or guide inspected |
| Qiskit Fall Fest 2026 / Phase 1 competition identity and eligibility | UNVERIFIED | User-provided pasted brief; web search surfaced an IBM host-application announcement, not competition rules |
| Processor A five-qubit and Processor B nine-qubit budgets | UNVERIFIED | Asserted in user-provided pasted brief; official guide not available |
| Processor C and custom Processor D are Phase 2 only | UNVERIFIED | Asserted in user-provided pasted brief; official guide not available |
| Extended deadline of 2026-10-14 23:59 IST | UNVERIFIED | Asserted in user-provided pasted brief; no authoritative deadline source found; the claimed date precedes the current date |
| Research report's J1-J2 spin-chain proposal and research hypotheses | UNVERIFIED | No research report is present; model/formula appear only in user-provided pasted brief |
| Official Hamiltonian, coefficients, qubit count, initial state, evolution time, observables | UNVERIFIED | No official problem statement available |
| Required Trotter methods/order, comparison cases, scoring metric | UNVERIFIED | No official problem statement available |
| Required/allowed topologies, basis gates, compiler settings, noise model/device | UNVERIFIED | No official problem statement available |
| Shot budget, repetitions, seed rules, resource limits | UNVERIFIED | No official problem statement available |
| Required deliverables, packaging, evaluation/submission procedure | UNVERIFIED | No official guide or submission portal confirmed |
| Deadline, timezone, extensions | UNVERIFIED | No authoritative deadline source found; do not infer from the current date |
| Small-system dense exact reference and local noisy simulation | ASSUMED proposal | Research design only; must yield to official constraints |
| Example topologies/noise settings, if rules do not prescribe them | ASSUMED proposal | Must be explicitly approved, configured, and labeled; never present as official |

## Official information still required

Obtain an authoritative guide or problem statement and verify, with source and exact wording where practical:

1. Official Phase 1 Master Guide, competition organizer/edition, track eligibility, and definitive rule/FAQ links.
2. Hamiltonian(s), coefficients, allowed qubit counts, initial states, simulation times, and required observables.
3. Required Trotter product formulas/orders, comparison baselines, and official accuracy/scoring definition.
4. Required or permitted processor topology, native/basis gates, transpiler constraints, and whether topology/noise are simulated or hardware-derived.
5. Noise model/device data, shot budget (including whether it is per circuit, observable, or full run), seeds/repetitions, and compute/resource limits.
6. Required source files, report/notebook/data formats, size limits, licensing/citation rules, and exact submission steps.
7. Absolute deadline with timezone, late policy, and portal availability; the date asserted in the pasted brief is already past, but remains unverified.

Do not fill gaps with guessed constants. If the rules omit an experimental choice, record it as an explicitly approved assumption with rationale and configuration provenance.

## Proposed minimum experiment (not yet approved or run)

1. Implement one small end-to-end experiment, using one explicitly selected Hamiltonian/instance from the official brief. Keep the complete calculation in one readable source module.
2. Compute a dense classical reference for the small system. Construct first-order and symmetric second-order product-formula circuits at matched total evolution time and a documented set of step counts.
3. Transpile each circuit against only the topologies and basis/compiler settings allowed by the brief. Record depth, one- and two-qubit gate counts, SWAP count, and two-qubit depth where applicable.
4. Apply a documented noisy simulator model, use the same official shot budget for every compared observable estimate, and record all seeds and configuration. Do not describe simulated topology as real hardware.
5. Keep ideal Trotter bias, noisy expectation error, and finite-shot error distinguishable. The target is observable-level error against the exact reference.
6. Test a small, predeclared predictor set: an analytic commutator-based Trotter indicator and compiled-cost features. Compare out-of-sample prediction against a simple baseline only if there are enough independent configuration groups; otherwise report descriptive associations and explicitly make no predictive claim.
7. Save raw counts/measurements or sufficient per-run observations, derived tables, a figure, and run metadata from the executable workflow. Report uncertainty and limitations. Make no quantum-advantage claim.

All parameter values, error definitions, model comparisons, and statistical procedures must be fixed in the configuration/protocol before collecting result data and must respect the official evaluation rules.

## Minimal proposed file set

- `qsimcompass.py` — sole implementation and command-line entry point for the Hamiltonian, exact reference, Trotter circuits, transpilation, noisy runs, analysis, and output generation.
- `experiment_config.json` — explicit run parameters, seeds, and provenance; no hidden or duplicated configuration.
- `tests\test_qsimcompass.py` — correctness and reproducibility checks.
- `requirements.txt` — exact, resolved package pins for the validated environment.
- `main.ipynb` — thin, executable explanation/driver that imports the same source module; no duplicate implementation or hand-entered experimental results.
- `README.md` — setup, exact commands, configuration, outputs, and limitations.
- `report.md` — findings populated only after executable runs; distinguish verified results from assumptions and limitations.
- Generated `results\` artifacts (raw/summary table, figure, run metadata) — create only by running the experiment; never fabricate or hand-fill experimental data.

`PROJECT_STATUS.md` and `CLAUDE.md` are project handoff/instruction files, not experimental evidence. Do not create a second project directory or alternate implementation.

## Python and dependency plan

Keep the existing workspace `.venv` and do not switch interpreters at this planning stage. PyPI metadata queried on 2026-10-17 reports Windows/Python 3.14-compatible release assets for Qiskit 2.6.0 (CPython 3.10 stable-ABI Windows wheel), Qiskit Aer 0.17.2 (CPython 3.14 Windows wheel), NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2, pytest 9.1.1, ipykernel 7.4.0, nbconvert 7.17.2, and nbformat 5.11.1. These are **candidate direct pins, not a verified working environment**; no packages were installed and no resolver, import, or runtime compatibility test was run.

Proposed candidate pins:
`qiskit==2.6.0`, `qiskit-aer==0.17.2`, `numpy==2.5.4`, `scipy==1.18.1`, `matplotlib==3.11.2`, `pytest==9.1.1`, `ipykernel==7.4.0`, `nbconvert==7.17.2`, `nbformat==5.11.1`.

Before installing, report the reason and exact action. Resolve this set against the existing `.venv`, verify imports and the smallest simulator/notebook smoke tests, then record a fully pinned environment only after resolution succeeds. Do not claim PyPI metadata alone proves runtime compatibility.

## Acceptance checks before calling the submission complete

- **Rules:** Every official constraint above is sourced and reflected in configuration, implementation, notebook, and report; submission path and deadline are verified.
- **Scientific correctness:** Small cases check Hamiltonian Hermiticity, exact evolution/expectations, circuit behavior, and first-/second-order convergence. Transpilation cost fields are measured from compiled circuits, not guessed.
- **Noise and shots:** Test fixed shot counts and seeds; distinguish sampling fluctuations and noise from ideal Trotter bias.
- **Reproducibility:** Re-running the documented command with the same environment/config/seeds reproduces deterministic outputs (or documented tolerances for stochastic/platform-dependent fields) and records versions/configuration.
- **Tests:** Run the targeted tests and report the actual command and result; do not infer success.
- **Outputs:** Generate tables and figures from saved experiment outputs; include labels, units, definitions, and uncertainty. No illustrative data may be represented as measured results.
- **Notebook:** Execute `main.ipynb` from a clean kernel using the documented command; verify no errors and that outputs derive from the source module.
- **Submission:** Check required files, paths, formats, size limits, and the actual portal/procedure against official instructions.

## Commands and results so far

- Inspected workspace with PowerShell `Get-ChildItem -Force` and recursive listings — findings above.
- Checked `python`, `.venv\Scripts\python.exe`, `.venv\Scripts\python.exe -m pip list --format=freeze`, `py -0p`, and `VIRTUAL_ENV` — findings above.
- Ran `git status --short --branch` — failed because this directory is not a Git repository.
- Searched the web for the exact track and Qiskit Fall Fest 2026 guide; no authoritative Phase 1 guide or deadline was identified. An IBM host-application announcement appeared but does not substantiate the competition assertions.
- Queried `https://pypi.org/pypi/<package>/json` metadata for the candidate packages — metadata only.
- **Tests/builds/experiments/notebook:** Not run; no project implementation exists.
- **Install/environment changes:** None.
- **Files changed in this audit follow-up:** `PROJECT_STATUS.md` only. Earlier planning created `PROJECT_STATUS.md` and `CLAUDE.md`; no other project files exist.
