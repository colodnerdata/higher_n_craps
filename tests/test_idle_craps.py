"""Tests for arbitrary-dice craps odds and idle progression mechanics."""

from fractions import Fraction

import pytest

from higher_n_craps import (
    GameState,
    IdleCrapsGame,
    cumulative_probability,
    outcome_distribution,
    probability_fraction,
    probability_of_total,
)


def test_outcome_distribution_two_dice() -> None:
    assert outcome_distribution(2) == {
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 5,
        9: 4,
        10: 3,
        11: 2,
        12: 1,
    }


def test_probability_of_total_for_arbitrary_dice() -> None:
    assert probability_of_total(3, 10) == pytest.approx(27 / 216)
    assert probability_of_total(1, 6) == pytest.approx(1 / 6)
    assert cumulative_probability(2, 4, 7) == pytest.approx(1 / 2)


def test_exact_probability_fraction() -> None:
    assert probability_fraction(2, 7) == Fraction(1, 6)
    assert probability_fraction(3, 9) == Fraction(25, 216)


def test_game_state_tracks_progression() -> None:
    state = GameState(num_dice=3, target_total=10, bankroll=50.0)

    assert state.hit_probability == pytest.approx(27 / 216)
    assert state.income_rate == pytest.approx((27 / 216) * 1.0 * 1.0)

    claim = state.buy_upgrade("odds", 10.0)
    assert claim is True
    assert state.bankroll == pytest.approx(40.0)
    assert state.upgrades["odds"] == 1

    profit = state.advance(2.0)
    assert profit > 0.0
    assert state.fortune == pytest.approx(profit)
    assert state.training == 2
    assert state.level == 3


def test_idle_game_exposes_tick_and_upgrades() -> None:
    game = IdleCrapsGame(num_dice=2, target_total=7)

    assert game.state.hit_probability == pytest.approx(1 / 6)
    assert game.upgrade_odds(0.0) is True
    assert game.upgrade_training(0.0) is True

    tick_profit = game.tick(3.0)
    assert tick_profit > 0.0
