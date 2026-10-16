"""Probability helpers for arbitrary-dice craps-style tables."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction


def outcome_distribution(num_dice: int, faces: int = 6) -> dict[int, int]:
    """Return the count of each sum for a pool of identically-sized dice.

    Parameters
    ----------
    num_dice : int
        Number of dice in the pool.
    faces : int, default=6
        Number of faces on each die.

    Returns
    -------
    dict[int, int]
        Mapping from total to the number of equally likely outcomes that
        produce that total.
    """
    if num_dice < 1:
        raise ValueError("num_dice must be at least 1")
    if faces < 1:
        raise ValueError("faces must be at least 1")

    counts: dict[int, int] = {0: 1}
    for _ in range(num_dice):
        next_counts: defaultdict[int, int] = defaultdict(int)
        for total, count in counts.items():
            for value in range(1, faces + 1):
                next_counts[total + value] += count
        counts = dict(next_counts)
    return dict(sorted(counts.items()))


def probability_of_total(num_dice: int, total: int, faces: int = 6) -> float:
    """Return the probability of a specific total."""
    outcomes = outcome_distribution(num_dice, faces)
    total_outcomes = faces**num_dice
    return outcomes.get(total, 0) / total_outcomes


def probability_fraction(
    num_dice: int,
    total: int,
    faces: int = 6,
) -> Fraction:
    """Return the exact rational probability of a specific total."""
    outcomes = outcome_distribution(num_dice, faces)
    return Fraction(outcomes.get(total, 0), faces**num_dice)


def cumulative_probability(
    num_dice: int,
    minimum_total: int,
    maximum_total: int | None = None,
    faces: int = 6,
) -> float:
    """Return the probability that a roll lands in a total range."""
    if maximum_total is not None and minimum_total > maximum_total:
        raise ValueError("minimum_total must be <= maximum_total")

    outcomes = outcome_distribution(num_dice, faces)
    if maximum_total is None:
        maximum_total = num_dice * faces

    total = sum(
        count
        for total_value, count in outcomes.items()
        if minimum_total <= total_value <= maximum_total
    )
    return total / (faces**num_dice)
