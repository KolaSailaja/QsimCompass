from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]


def plot_ideal_error_summary(results_path: str | Path, output_path: str | Path | None = None) -> Path:
    summary_path = Path(results_path)
    rows = json.loads(summary_path.read_text(encoding="utf-8"))

    filtered = [row for row in rows if row["order"] == 2 and row["processor"] == "Processor A"]
    steps = sorted({row["steps"] for row in filtered})
    time_map: dict[float, list[float]] = {t: [] for t in sorted({row["time"] for row in filtered})}
    for row in filtered:
        time_map[row["time"]].append(row["ideal_error"])

    fig, ax = plt.subplots(figsize=(8, 5))
    for time, errors in time_map.items():
        ax.plot(steps, errors, marker="o", label=f"t={time}")
    ax.set_xlabel("Trotter steps")
    ax.set_ylabel("|\u03C3_z^exact - \u03C3_z^trotter|")
    ax.set_title("Second-order Trotter error for Processor A")
    ax.legend()
    ax.grid(alpha=0.3)

    target = Path(output_path) if output_path else ROOT / "results" / "figures" / "processor_a_second_order_error.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(target, dpi=200)
    plt.close(fig)
    return target
