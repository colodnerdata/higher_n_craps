"""Core idle progression model for arbitrary-dice craps games."""

from __future__ import annotations

from dataclasses import dataclass, field

from .odds import probability_of_total


@dataclass
class GameState:
    """Persistent progression data for an idle craps-style game."""

    num_dice: int = 2
    target_total: int = 7
    bankroll: float = 0.0
    fortune: float = 0.0
    level: int = 1
    training: int = 0
    upgrades: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.num_dice < 1:
            raise ValueError("num_dice must be at least 1")
        if self.target_total < self.num_dice:
            raise ValueError("target_total must be at least num_dice")
        self.upgrades.setdefault("odds", 0)
        self.upgrades.setdefault("training", 0)

    @property
    def hit_probability(self) -> float:
        return probability_of_total(self.num_dice, self.target_total)

    @property
    def income_rate(self) -> float:
        efficiency = 1.0 + self.training * 0.15
        odds_bonus = 1.0 + self.upgrades["odds"] * 0.2
        return self.hit_probability * odds_bonus * efficiency

    def buy_upgrade(self, name: str, cost: float) -> bool:
        """Buy an upgrade if enough bankroll is available."""
        if self.bankroll < cost:
            return False
        self.bankroll -= cost
        self.upgrades[name] = self.upgrades.get(name, 0) + 1
        return True

    def advance(self, dt: float = 1.0) -> float:
        """Advance the idle loop by time and pay out winnings."""
        if dt < 0:
            raise ValueError("dt must be non-negative")

        payout = self.income_rate * dt
        self.bankroll += payout
        self.fortune += payout
        self.training += int(dt)
        self.level = max(1, self.level + int(dt))
        return payout


class IdleCrapsGame:
    """Simple idle game wrapper around a progression state."""

    def __init__(self, num_dice: int = 2, target_total: int = 7) -> None:
        self.state = GameState(num_dice=num_dice, target_total=target_total)

    def tick(self, dt: float = 1.0) -> float:
        """Run the timer tick and return the earnings for this period."""
        return self.state.advance(dt)

    def upgrade_odds(self, cost: float) -> bool:
        """Improve the dice odds by buying a tier."""
        return self.state.buy_upgrade("odds", cost)

    def upgrade_training(self, cost: float) -> bool:
        """Improve the training multiplier by buying a tier."""
        return self.state.buy_upgrade("training", cost)
