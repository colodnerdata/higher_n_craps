# Decisions

Record the choices future-you or a coding assistant might otherwise repeat.
Add an entry when a decision affects interfaces, architecture, dependencies,
data formats, verification, or a meaningful constraint. Keep entries short.

Preserve the original reasoning when a decision changes. Mark the old entry
superseded and link to the new one. Record rejected alternatives when the
reason is likely to be useful again. Search by mechanism before proposing a
design change.

## Entry pattern

- **Date and title:** YYYY-MM-DD — the decision in a few words.
- **Status:** accepted, rejected, deferred, or superseded (with a link).
- **Context:** the problem and constraint.
- **Decision:** what we chose.
- **Why:** the tradeoff and important alternative.
- **Revisit when:** evidence or a changed condition that would alter the choice.

## 2026-10-16 — Arbitrary-dice probability model

- **Status:** accepted
- **Context:** the project needs an idle progression game for craps-style
  tables, but the rules should work for any number of dice rather than only a
  classic 2-dice model.
- **Decision:** keep the probability logic in a separate `odds` module and make
  the progression state reference those values instead of embedding rules in the
  UI or save layer.
- **Why:** this keeps the math transparent, allows exact rational probabilities,
  and keeps future upgrades or rule variants easy to add without reworking the
  whole game loop.
- **Revisit when:** the game needs more complex rules, such as point-based bets,
  multiple tables, or nonstandard dice faces.
