# QSimCompass Continuation Rules

## Before work

- Read `PROJECT_STATUS.md`, this file, and the relevant existing source/tests before any substantial task. Inspect before editing; preserve working code and user changes.
- Treat this workspace as the one canonical project. Do not create a second project folder, duplicate implementation, or parallel architecture.
- Check the status file's blockers and next action. Work in one stage at a time; verify and update the handoff record before moving on.
- The registered track and any rule/parameter not supported by an official source are unverified. Record each material requirement as VERIFIED, UNVERIFIED, or ASSUMED with its source.

## Scientific and implementation integrity

- Do not implement the quantum experiment until the official problem statement/rules have been inspected and the plan and gaps have been reported. If official material is unavailable, ask for it; an assumption may support an explicitly labeled research prototype but cannot establish competition alignment.
- Keep the solution small, modular, and beginner-readable. `qsimcompass.py` is the proposed single source of truth; the notebook should call it rather than duplicate calculations.
- Never invent data, numerical results, device properties, official constants, citations, test results, plots, notebook execution, installation success, or quantum-advantage claims.
- Separate exact reference, ideal product-formula error, noise, and finite-shot effects. Persist seeds/configuration and derive every table/figure/report result from an executable run.
- Do not silently substitute defaults for unknown official settings. Surface blockers and assumptions explicitly.

## Environment and changes

- The inspected `.venv` uses Python 3.14.4 and has only pip installed. Do not install packages or change interpreters without first reporting the reason and proposed action.
- Candidate package pins in `PROJECT_STATUS.md` are metadata-checked only; verify dependency resolution, imports, and runtime compatibility before treating them as validated.
- Make precise, scoped changes. Inspect every existing file before overwriting it. Do not remove or revert unrelated user changes.
- Use the smallest relevant tests/build/notebook execution checks. State exact commands and observed outcomes; never claim a check was run when it was not.

## Handoff

After each completed stage, update `PROJECT_STATUS.md` with the stage status, completed work, exact changed files, commands actually run, observed test results, unresolved issues, and one next action. If a blocker remains, mark the stage BLOCKED; do not label it complete.
