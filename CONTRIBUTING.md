# Contributing

Read `AGENTS.md` and `skills/damaged-qr-recovery/SKILL.md` before making changes.

## Rules

- keep observations, mathematical recovery, and external constraints separate;
- add regression tests for behavior changes;
- prefer synthetic or redacted fixtures;
- do not hard-code one vendor's ticket format into generic recovery logic;
- document shortcuts and known ceilings;
- update the relevant reference when an algorithmic rule changes.

## Pull requests

Describe the recovery stage changed, the validation added, and any new dependency. For solver/performance changes, include benchmark evidence.
