"""Idle progression framework for arbitrary-dice craps odds."""

from .game import GameState, IdleCrapsGame
from .odds import (
    cumulative_probability,
    format_probability_odds,
    odds_to_probability,
    outcome_distribution,
    probability_fraction,
    probability_of_total,
    probability_to_odds,
)

__all__ = [
    "GameState",
    "IdleCrapsGame",
    "cumulative_probability",
    "format_probability_odds",
    "odds_to_probability",
    "outcome_distribution",
    "probability_fraction",
    "probability_of_total",
    "probability_to_odds",
]
