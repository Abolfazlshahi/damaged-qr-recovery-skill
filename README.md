# Damaged QR Recovery

> **Recover what the QR actually encodes — not what an agent thinks it probably encodes.**

[![Skill](https://img.shields.io/badge/Agent%20Skill-Damaged%20QR-1f6feb)](skills/damaged-qr-recovery/SKILL.md)
[![CI](https://github.com/Abolfazlshahi/damaged-qr-recovery-skill/actions/workflows/test.yml/badge.svg)](https://github.com/Abolfazlshahi/damaged-qr-recovery-skill/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](pyproject.toml)

`damaged-qr-recovery` is a production-oriented **Agent Skill + reference implementation toolkit** for reconstructing QR payloads from partially obscured, scratched, blurred, clipped, compressed, or otherwise damaged QR codes.

It is deliberately bigger than a prompt. The repository contains the Skill contract, algorithm references, validation rules, CLI helpers, Python primitives, examples, benchmarks, test scaffolding, agent adapters, security guidance, and contribution rules needed to turn the method into repeatable engineering rather than a one-off chat trick.

## Why this exists

A damaged QR often still contains enough information to recover the original payload exactly. The reliable route is to exploit the QR specification itself:

```text
image evidence
   ↓
QR geometry / rectification
   ↓
version + format information
   ↓
tri-state module map
   ↓
unmask + official data traversal
   ↓
codewords + RS block structure
   ↓
Reed–Solomon erasure/error recovery
   ↓
payload parsing + explicit constraints
   ↓
exact re-encoding
   ↓
known-module proof
   ↓
independent decode
   ↓
UNIQUE / AMBIGUOUS / NOT RECOVERED
```

The important word is **exactly**. A decoder returning a plausible URL is not enough.

## What the Skill covers

- locator/finder-pattern reasoning and perspective correction;
- QR version, format, ECC, and mask recovery;
- functional-module identification;
- unknown/erasure-aware module maps;
- official zig-zag data traversal;
- byte extraction and block deinterleaving;
- QR Reed–Solomon block reasoning over GF(256);
- erasure-first recovery and bounded candidate search;
- payload-mode parsing;
- external metadata as constraints rather than truth;
- exact QR regeneration;
- module-for-module validation against source evidence;
- independent-decoder confirmation;
- ambiguity detection and honest failure states.

## Repository map

```text
.
├── skills/
│   └── damaged-qr-recovery/
│       ├── SKILL.md
│       └── references/
│           ├── qr-structure.md
│           ├── reed-solomon.md
│           ├── block-layout.md
│           ├── recovery-strategies.md
│           └── validation.md
├── src/damaged_qr_recovery/
│   ├── geometry.py
│   ├── models.py
│   ├── provenance.py
│   ├── qr.py
│   ├── rs.py
│   └── __main__.py
├── commands/
│   ├── recover.md
│   ├── inspect.md
│   ├── validate.md
│   └── audit.md
├── adapters/
├── scripts/
├── examples/
├── benchmark/
├── docs/
├── tests/
├── .github/
├── AGENTS.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── pyproject.toml
└── LICENSE
```

## The core Skill

The canonical agent contract lives at:

```text
skills/damaged-qr-recovery/SKILL.md
```

The Skill is explicit about when to activate, what to inspect, how to treat uncertain modules, when to use Reed–Solomon, when external clues are allowed, how to validate, and when to refuse false certainty.

## Evidence model

Every recovered fact should have provenance:

| Provenance | Meaning |
|---|---|
| `OBSERVED` | Stable source evidence directly read from the image/document |
| `RECOVERED_BY_RS` | Determined from QR codeword/parity constraints |
| `CONSTRAINED_BY_METADATA` | Narrowed by trusted external context |
| `INFERRED_UNVERIFIED` | Plausible but not mathematically established |

A **confirmed** recovery requires the QR itself to validate the candidate. External context may narrow the search space, but it must not silently manufacture bytes.

## What makes a result confirmed?

The minimum proof chain is:

1. QR structure is internally consistent.
2. Candidate codewords satisfy the correct RS constraints.
3. The payload can be re-encoded with the same structural parameters.
4. Every source module marked known agrees with the reconstruction.
5. An independent decoder can decode the regenerated QR.
6. No competing candidate survives the same constraints.

Any missing step can downgrade the result to `PARTIAL`, `AMBIGUOUS`, or `NOT_RECOVERED`.

## Install

The agent Skill itself is dependency-free Markdown. The optional Python helpers can be installed with:

```bash
python -m pip install -e '.[all]'
```

Run the tests:

```bash
pytest
```

## CLI / scripts

Basic QR inspection:

```bash
python scripts/inspect_qr.py image.png
```

Coarse image-level comparison:

```bash
python scripts/compare_modules.py observed.png reconstructed.png --size 33
```

Independent decoder validation:

```bash
python scripts/validate_reconstruction.py reconstructed.png
```

Package smoke commands:

```bash
qr-recovery size 4
qr-recovery version 33
```

The scripts are intentionally small. They are helpers around the Skill workflow, not a claim that generic OpenCV decoding alone can solve arbitrary damaged QR cases.

## Agent integration

### Generic Agent Skills runtimes

Copy the skill directory into the runtime's skill search path:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

Keep `references/` beside `SKILL.md`; the main file points agents toward those documents when deeper reasoning is needed.

### Hermes

Use the dedicated adapter in [`adapters/hermes.md`](adapters/hermes.md) and preserve the same skill directory layout.

### Other agents

For runtimes with `AGENTS.md` support, the repository root instructions provide the safety and evidence rules. For plugin/skill systems, use `SKILL.md` as the canonical behavior contract and the files under `commands/` as task entry points.

## Commands

- [`commands/inspect.md`](commands/inspect.md) — inspect only, no speculation.
- [`commands/recover.md`](commands/recover.md) — full evidence-first recovery.
- [`commands/validate.md`](commands/validate.md) — proof-check a candidate reconstruction.
- [`commands/audit.md`](commands/audit.md) — challenge a claimed recovery.

## References

- [`qr-structure.md`](skills/damaged-qr-recovery/references/qr-structure.md) — module geometry, function patterns, format/version information, masking, traversal.
- [`block-layout.md`](skills/damaged-qr-recovery/references/block-layout.md) — RS blocks and interleaving.
- [`reed-solomon.md`](skills/damaged-qr-recovery/references/reed-solomon.md) — GF(256), parity equations, erasures, solver notes.
- [`recovery-strategies.md`](skills/damaged-qr-recovery/references/recovery-strategies.md) — escalation ladder and constrained search.
- [`validation.md`](skills/damaged-qr-recovery/references/validation.md) — exact proof and failure states.

## Benchmarking

The benchmark is designed around **exact recovery** and **false-confirmation resistance**, not just decoder success. See [`benchmark/README.md`](benchmark/README.md).

Recommended benchmark dimensions include QR version, ECC level, mask, random erasures, rectangular occlusions, blur, perspective, clipping, mixed damage, misleading metadata, and genuinely ambiguous cases.

## Security and privacy

QR codes may carry personal data, ticket identifiers, payment addresses, session links, authentication secrets, or other sensitive content. Prefer local processing, redact public fixtures, and never execute a recovered URL or payload automatically.

See [`SECURITY.md`](SECURITY.md) and [`docs/threat-model.md`](docs/threat-model.md).

## Scope boundaries

This project does **not** promise recovery when the evidence is mathematically insufficient. It does not bypass authentication, decrypt protected content, or treat semantic plausibility as proof.

## Donations / community

Community: [@pythash](https://t.me/pythash)

Optional project donations and supported networks are documented in [`docs/DONATIONS.md`](docs/DONATIONS.md).

## Roadmap

The repository is structured so the next engineering stages can be added without rewriting the Skill:

- complete version/ECC RS block tables;
- production-grade erasure solver;
- robust grid detection and confidence maps;
- synthetic damage generator;
- property-based and fuzz testing;
- multi-image evidence fusion;
- richer vendor-constraint adapters;
- additional agent/plugin adapters;
- reproducible end-to-end benchmark reports.

## License

MIT — see [`LICENSE`](LICENSE).
