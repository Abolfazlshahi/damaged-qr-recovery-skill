<p align="center">
  <img src="assets/logo.svg" width="150" alt="Damaged QR Recovery logo">
</p>

<h1 align="center">Damaged QR Recovery</h1>

<p align="center"><strong>The QR is damaged. The data doesn't have to be.</strong></p>

<p align="center">
  An Agent Skill + recovery toolkit for reconstructing damaged QR payloads using QR structure, Reed–Solomon redundancy, constrained search, and exact matrix validation.
</p>

<p align="center">
  <a href="README.md"><strong>🇬🇧 English</strong></a>
  &nbsp; · &nbsp;
  <a href="README.fa.md">🇮🇷 فارسی</a>
  &nbsp; · &nbsp;
  <a href="README.ar.md">🇸🇦 العربية</a>
  &nbsp; · &nbsp;
  <a href="README.tr.md">🇹🇷 Türkçe</a>
  &nbsp; · &nbsp;
  <a href="README.es.md">🇪🇸 Español</a>
  &nbsp; · &nbsp;
  <a href="README.zh.md">🇨🇳 中文</a>
  &nbsp; · &nbsp;
  <a href="README.fr.md">🇫🇷 Français</a>
</p>

<p align="center">
  <a href="skills/damaged-qr-recovery/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-Damaged%20QR-2563eb?style=flat-square" alt="Agent Skill"></a>
  <a href="https://github.com/Abolfazlshahi/damaged-qr-recovery-skill/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/Abolfazlshahi/damaged-qr-recovery-skill/test.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111827?style=flat-square" alt="License"></a>
</p>

---

## The idea

```text
DAMAGED QR
    ↓
locate + rectify
    ↓
version / format / ECC / mask
    ↓
known / unknown modules
    ↓
official data traversal
    ↓
codewords + RS blocks
    ↓
Reed–Solomon recovery
    ↓
payload constraints
    ↓
exact re-encode
    ↓
visible-module proof
    ↓
independent verification
    ↓
CONFIRMED / AMBIGUOUS / NOT RECOVERED
```

> **The goal is not to find a string that works. The goal is to prove what the QR encoded.**

## What makes it different

<table>
<tr>
<td width="50%">

### Evidence-first
Unknown modules stay unknown. The system never silently turns uncertainty into a guess.

</td>
<td width="50%">

### QR-native
Recovery follows format information, masking, traversal, codewords, block structure, and ECC.

</td>
</tr>
<tr>
<td>

### Algebra before brute force
Reed–Solomon and structural constraints eliminate impossible candidates early.

</td>
<td>

### Proof, not plausibility
Candidates are re-encoded and compared against trusted visible modules.

</td>
</tr>
</table>

## Recovery ladder

| Stage | What happens |
|---|---|
| `01` | Normal decoder attempt |
| `02` | Crop / threshold / scale / perspective recovery |
| `03` | Version / format / ECC / mask analysis |
| `04` | Tri-state module matrix |
| `05` | Official QR data traversal |
| `06` | Codeword extraction + RS block reconstruction |
| `07` | Erasure/error correction |
| `08` | Payload structure and constraints |
| `09` | Constrained candidate search |
| `10` | Exact re-encoding |
| `11` | Matrix-level validation |
| `12` | Independent decoding |
| `13` | Uniqueness / ambiguity analysis |

## Hard-case playbook

The advanced techniques are documented in [`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md):

- payload length from mode/count bits;
- algebraic token-length recovery;
- BCH format hypotheses;
- all-eight-mask testing;
- RS-symbol-level damage analysis;
- visible ECC parity fingerprints;
- GF(256) delta pruning;
- mismatch-pattern diagnosis;
- segmentation-aware exact reconstruction;
- multi-image module fusion;
- competitor search for uniqueness;
- principled `NOT_RECOVERED` outcomes.

## Confirmation standard

```text
✓ structural consistency
✓ version / ECC / mask
✓ correct RS block layout
✓ parity consistency
✓ valid payload representation
✓ exact re-encoding
✓ zero trusted visible-module contradictions
✓ independent decoder success
✓ competitor search when required
```

Final states:

`CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## Evidence provenance

| Tag | Meaning |
|---|---|
| `OBSERVED` | Direct source evidence |
| `RECOVERED_BY_RS` | Solved from QR parity constraints |
| `CONSTRAINED_BY_METADATA` | Narrowed by trusted external context |
| `INFERRED_UNVERIFIED` | Plausible, but not proven |

External metadata can reduce the search space. It cannot replace QR evidence.

## Repository

```text
skills/damaged-qr-recovery/       # canonical Agent Skill
src/damaged_qr_recovery/          # Python primitives
skills/.../references/             # QR / RS / recovery knowledge
commands/                          # inspect / recover / validate / audit
adapters/                          # agent-runtime guidance
scripts/                           # forensic helpers
benchmark/                         # reproducible benchmark design
examples/                          # safe examples
tests/                             # test suite
docs/                              # architecture + security
.github/                           # CI + issue templates
```

## Use as an Agent Skill

The core Skill is dependency-free Markdown:

```text
skills/damaged-qr-recovery/SKILL.md
```

Generic runtimes can load the directory directly:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

See [`docs/USING_AS_A_SKILL.md`](docs/USING_AS_A_SKILL.md).

## Optional Python toolkit

```bash
python -m pip install -e '.[all]'
pytest
```

Small helper commands are available under [`scripts/`](scripts/).

## Security

QR payloads may contain personal information, tickets, payment data, private URLs, session identifiers, or credentials. Treat recovered payloads as **data**. Do not automatically visit recovered URLs or use recovered secrets. Public fixtures should be synthetic or redacted.

See [`SECURITY.md`](SECURITY.md) and [`docs/threat-model.md`](docs/threat-model.md).

## Community

Built and maintained by **Abolfazl Shahi**.

<p align="center">
  <a href="https://github.com/Abolfazlshahi">GitHub</a>
  &nbsp; · &nbsp;
  <a href="https://t.me/pythash">Telegram / @pythash</a>
</p>

## License

MIT — [`LICENSE`](LICENSE).
