"""QSimCompass package."""

from .advisor import choose_best_strategy, evidence_based_selection, predictive_selection
from .benchmark import run_default_experiment
from .budget import Budget
from .pareto import pareto_front, pareto_summary
from .problem import SpinChainProblem

__all__ = [
    "SpinChainProblem",
    "run_default_experiment",
    "Budget",
    "choose_best_strategy",
    "evidence_based_selection",
    "predictive_selection",
    "pareto_front",
    "pareto_summary",
]
__version__ = "0.2.0"
