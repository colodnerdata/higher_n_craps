# higher_n_craps

`higher_n_craps` is a lightweight idle progression framework for craps-style
games that can scale to an arbitrary number of dice. The project models the odds
of producing each total, exposes the exact probability math, and gives a small
state container for progression systems that reward players for improving their
odds over time.

## Start working

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
uv sync --locked
uv run --locked poe check
```

## Use the project

```python
from higher_n_craps import IdleCrapsGame, probability_of_total

print(probability_of_total(2, 7))
print(probability_of_total(3, 10))

game = IdleCrapsGame(num_dice=3, target_total=10)
print(game.tick(1.0))
```

The package provides exact and approximate total probabilities for any dice
count, plus a simple idle game state that accrues bankroll and training gains.

## Find your place

- [Development](docs/DEVELOPMENT.md): commands, tests, review, and releases.
- [Decisions](docs/DECISIONS.md): why important choices were made.
- [Next steps](docs/NEXT.md): the current goal and the next useful action.
- [Agent instructions](AGENTS.md): shared rules for coding assistants.
