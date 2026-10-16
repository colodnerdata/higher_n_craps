"""Probability helpers for arbitrary-dice craps-style tables."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction


def _coerce_probability(probability: float | Fraction) -> Fraction:
    """Normalize a probability-like value into a reduced Fraction."""
    if isinstance(probability, Fraction):
        value = probability
    else:
        value = Fraction(str(probability)).limit_denominator()

    if not 0 <= value <= 1:
        raise ValueError("probability must be between 0 and 1 inclusive")
    return value


def probability_to_odds(probability: float | Fraction) -> tuple[int, int]:
    """Convert a success probability into inverse payout odds.

    Examples
    --------
    A 1/3 chance of success corresponds to 2:1 odds against the event, so the
    payout notation is expressed as a numerator and denominator pair with the
    losing side first.
    """
    value = _coerce_probability(probability)
    if value == 1:
        return (0, 1)
    if value == 0:
        return (1, 0)

    odds = (1 - value) / value
    reduced = odds.limit_denominator()
    return (reduced.numerator, reduced.denominator)


def format_probability_odds(probability: float | Fraction) -> str:
    """Format a probability as a payout-style inverse odds string."""
    numerator, denominator = probability_to_odds(probability)
    if denominator == 0:
        return "0:1"
    return f"{numerator}:{denominator}"


def odds_to_probability(odds: str | tuple[int, int]) -> Fraction:
    """Convert a payout-style odds string or pair back to a probability."""
    if isinstance(odds, str):
        text = odds.strip()
        if ":" not in text:
            raise ValueError("odds must be in 'A:B' format")
        numerator, denominator = (part.strip() for part in text.split(":", 1))
        left = int(numerator)
        right = int(denominator)
    else:
        left, right = odds

    if right < 0 or left < 0:
        raise ValueError("odds must be non-negative")
    if right == 0:
        return Fraction(1, 1)
    if left == 0:
        return Fraction(0, 1)

    return Fraction(right, left + right)


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
