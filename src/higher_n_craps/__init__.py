"""Idle progression framework for arbitrary-dice craps odds."""

from .game import GameState, IdleCrapsGame
from .odds import (
    cumulative_probability,
    outcome_distribution,
    probability_fraction,
    probability_of_total,
)

__all__ = [
    "GameState",
    "IdleCrapsGame",
    "cumulative_probability",
    "outcome_distribution",
    "probability_fraction",
    "probability_of_total",
]
