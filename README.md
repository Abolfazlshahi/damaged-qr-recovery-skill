# Damaged QR Recovery Skill

![Status](https://img.shields.io/badge/status-experimental-orange)
![Skill](https://img.shields.io/badge/agent%20skill-SKILL.md-purple)
![License](https://img.shields.io/badge/license-MIT-green)

> An Agent Skill for recovering data from partially damaged, scratched, obscured, blurred, or incomplete QR codes using the QR specification itself, known-position erasures, Reed–Solomon constraints, and independent reconstruction checks.

This project is designed for AI coding agents and other Agent Skills-compatible runtimes. It is intentionally **method-first**: the Skill describes how an agent should attack a damaged QR, while implementation-specific tools can be swapped underneath it.

## Why this exists

A normal QR decoder is optimized for a readable QR image. A damaged QR is a different problem.

When a region is covered or erased, the goal is not to ask an AI to visually guess the missing pixels. The recovery process should instead turn the image into a constrained QR decoding problem:

```text
image
  ↓
QR geometry
  ↓
version / format / ECC / mask
  ↓
known + unknown module matrix
  ↓
masked data extraction
  ↓
codewords + block deinterleaving
  ↓
Reed–Solomon erasure recovery
  ↓
payload constraints
  ↓
exact QR reconstruction
  ↓
visible-module comparison
  ↓
independent decode
```

The QR's own redundancy is the central source of truth. Printed text, known URL formats, ticket metadata, filenames, or other external information may narrow a search, but they are not proof on their own.

## What the Skill covers

- Detecting and cropping damaged QR codes
- Perspective correction and module-grid estimation
- QR version discovery
- Format-information parsing
- Error-correction level and mask detection
- Finder/timing/alignment functional-pattern handling
- Known/unknown/uncertain module maps
- Explicit treatment of covered regions as **erasures**
- Data-module traversal and mask removal
- Codeword extraction
- QR block layout and interleaving
- Reed–Solomon erasure/error recovery over GF(256)
- Partially known byte constraints
- Payload mode/count parsing
- Constrained candidate search
- Exact QR re-encoding
- Matrix-level validation against all visible source modules
- Independent final decoding
- Uniqueness/ambiguity reporting
- Multi-image evidence merging
- Failure analysis and recovery escalation

## Install as a Skill

Clone or copy the repository into the Skill location supported by your agent runtime. The canonical Skill file is:

```text
skills/damaged-qr-recovery/SKILL.md
```

For tools that discover Agent Skills recursively, keep that path intact.

## Repository layout

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
├── examples/
├── benchmark/
├── tests/
├── scripts/
├── docs/
├── AGENTS.md
├── LICENSE
└── README.md
```

## Recovery philosophy

### 1. Never guess first

A damaged QR should first be represented as data with uncertainty:

```text
0 = known white
1 = known black
? = erased / unknown
```

Do not turn uncertain pixels into permanent facts prematurely.

### 2. Erasures are different from errors

If the location of the damaged symbol/module is known but its value is unknown, Reed–Solomon can exploit that knowledge more efficiently than it can handle an unknown error location.

### 3. QR structure comes before payload semantics

Version, format information, mask, functional patterns, codeword placement and block layout should be established before attempting payload reconstruction.

### 4. A plausible URL is not a recovery

A candidate payload is only confirmed after mathematical and image-level validation.

### 5. Re-encode and compare

The recovered payload should be encoded back into a QR and compared module-by-module against every confidently visible module in the source image.

## Validation standard

The Skill uses the following evidence ladder:

| Level | Check |
|---|---|
| 1 | QR syntax / mode / length is valid |
| 2 | Reed–Solomon parity constraints pass |
| 3 | Reconstructed QR matches all visible source modules |
| 4 | Functional patterns and format information remain consistent |
| 5 | An independent decoder successfully decodes the reconstruction |
| 6 | The solution is unique under the available constraints |

Only the strongest supported claim should be reported:

```text
CONFIRMED_UNIQUE
CONFIRMED
AMBIGUOUS
NOT_RECOVERED
```

## Working with real tickets and documents

A QR may belong to a:

- train ticket
- boarding pass
- event ticket
- invoice
- payment slip
- shipping label
- Wi-Fi card
- vCard/contact card
- URL or activation document

Visible document fields can be useful constraints. The Skill explicitly separates:

```text
OBSERVED
RECOVERED_BY_RS
CONSTRAINED_BY_METADATA
UNVERIFIED_INFERENCE
```

This prevents the agent from silently converting contextual hints into fabricated QR data.

## Benchmarks

The benchmark directory is intended for reproducible synthetic damage cases. Recommended dimensions include:

- percentage of erased modules
- number of erased codeword symbols
- known vs unknown error positions
- contiguous paint/marker occlusion
- random erasures
- blur
- perspective distortion
- JPEG compression
- low resolution
- multiple images of the same QR
- partially known payloads

A benchmark case should record both success and *why* a recovery was rejected.

## Roadmap

- [ ] Production-ready QR module sampler
- [ ] Complete version/ECC block-table implementation
- [ ] GF(256) Reed–Solomon erasure solver
- [ ] Multi-image registration/merge
- [ ] Exact segmentation-preserving re-encoder
- [ ] Automated benchmark corpus
- [ ] CI recovery tests
- [ ] Adapters/examples for Codex, Claude Code, Cursor and other Skill runtimes
- [ ] CLI for forensic inspection and validation

## Safety

Use this project only with QR images and documents you are authorized to recover. Do not use recovered authentication secrets, payment information, session tokens, tickets, or credentials to access systems or services without authorization.

## Author / community

Built and maintained by **Abolfazl Shahi**.

Telegram community: [@pythash](https://t.me/pythash)

GitHub: [@Abolfazlshahi](https://github.com/Abolfazlshahi)

## Support the project

If this Skill saves you time and you want to support development:

| Network | Donation address |
|---|---|
| TON | `UQDfjVk2UdpiMg-bsxqoLa0O_icuaF20D-wWJgIJwK1Ha2Ul` |
| USDT (TRC20) | `TR8ibZGKutPKoDm5nMbHFwGPFBuMKwjG6j` |
| USDT (BEP20) | `0x8c45d6bae8a5a572b2a776779fe0bcae3d3f9107` |

Please verify the network before sending funds.

## License

MIT — see [LICENSE](./LICENSE).
