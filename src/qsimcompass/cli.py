from __future__ import annotations

import argparse
import json
from pathlib import Path

from .advisor import choose_best_strategy
from .benchmark import run_default_experiment
from .budget import Budget
from .pareto import pareto_summary
from .security import ensure_within_project, sanitize_filename, validate_numeric

ROOT = Path(__file__).resolve().parents[2]


def _load_rows(path: str | Path) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data.get("rows", [])
    return list(data)


def validate_command(args: argparse.Namespace) -> int:
    import qiskit
    import qiskit_aer

    print(f"qiskit={qiskit.__version__} aer={qiskit_aer.__version__}")
    return 0


def benchmark_command(args: argparse.Namespace) -> int:
    result = run_default_experiment()
    print(json.dumps({"status": result["status"], "rows": len(result["rows"])}, indent=2))
    return 0


def recommend_command(args: argparse.Namespace) -> int:
    path = Path(args.result_file)
    rows = _load_rows(path)
    budgets = {
        "max_depth": args.max_depth,
        "max_two_qubit_gates": args.max_cx,
        "max_total_shots": args.max_shots,
    }
    recommendation = choose_best_strategy(rows, Budget.from_dict(budgets), use_predictive=args.predictive)
    print(json.dumps(recommendation, indent=2, default=str))
    return 0


def analyze_command(args: argparse.Namespace) -> int:
    rows = _load_rows(args.result_file)
    front = pareto_summary(rows, ["ideal_error", "cx_count", "compiled_depth"])
    print(json.dumps(front, indent=2, default=str))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="QSimCompass local benchmark and advisor CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Check environment compatibility")
    validate.set_defaults(func=validate_command)

    benchmark = subparsers.add_parser("benchmark", help="Execute the default local benchmark")
    benchmark.set_defaults(func=benchmark_command)

    recommend = subparsers.add_parser("recommend", help="Recommend a feasible strategy")
    recommend.add_argument("result_file", nargs="?", default=str(ROOT / "results" / "tables" / "benchmark_summary.json"))
    recommend.add_argument("--max-depth", type=int, default=None)
    recommend.add_argument("--max-cx", type=int, default=None)
    recommend.add_argument("--max-shots", type=int, default=None)
    recommend.add_argument("--predictive", action="store_true")
    recommend.set_defaults(func=recommend_command)

    analyze = subparsers.add_parser("analyze", help="Inspect Pareto front information")
    analyze.add_argument("result_file", nargs="?", default=str(ROOT / "results" / "tables" / "benchmark_summary.json"))
    analyze.set_defaults(func=analyze_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
