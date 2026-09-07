# Agent Contract

The Skill is a workflow contract, not a guarantee that every damaged QR is recoverable.

## Inputs

- one or more QR images;
- optional document text or printed identifiers;
- optional trusted intact QR from the same generator;
- optional vendor/schema constraints.

## Required behavior

- preserve originals;
- keep uncertainty explicit;
- use QR-native structure before semantic guesses;
- solve erasures before speculative substitutions;
- validate candidates by exact re-encoding and source-module comparison;
- use an independent decoder;
- report ambiguity instead of selecting a prettier candidate.

## Status values

`CONFIRMED`, `AMBIGUOUS`, `PARTIAL`, `NOT_RECOVERED`, `INVALID_INPUT`.
