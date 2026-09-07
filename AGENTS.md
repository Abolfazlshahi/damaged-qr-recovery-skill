# AGENTS.md

## Mission

Maintain a rigorous, evidence-first QR recovery Skill. Prefer mathematically validated reconstruction over plausible guesses.

## Non-negotiable rules

- Never fabricate missing QR payload bytes.
- Treat paint/occlusion with known location as erasure whenever possible.
- Keep uncertain image samples as unknown until enough evidence exists.
- Separate direct observations, Reed–Solomon recovery, metadata constraints, and unverified inference.
- A plausible URL is not a successful recovery.
- Confirm candidates by regenerating the QR and comparing every known source module.
- Prefer an independent decoder for final confirmation.
- Report ambiguity when multiple candidates survive.

## Implementation style

- Keep algorithmic stages modular.
- Do not hard-code one vendor's ticket format into the generic recovery algorithm.
- Vendor-specific metadata may be implemented as optional constraints under `examples/`, `adapters/`, or `docs/`.
- Avoid unnecessary dependencies in the core Skill.
- Tests must include successful, ambiguous, and failing cases.

## Changes

When modifying the Skill, update the relevant reference document and add/adjust a regression test when behavior changes.
