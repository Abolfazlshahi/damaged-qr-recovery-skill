<p align="center">
  <img src="assets/logo.svg" width="150" alt="Damaged QR Recovery logo">
</p>

<h1 align="center">Damaged QR Recovery</h1>

<p align="center">
  <strong>The QR is damaged. The data doesn't have to be.</strong>
</p>

<p align="center">
  An Agent Skill and recovery toolkit for reconstructing QR payloads from damaged, obscured, scratched, blurred, clipped, or incomplete codes — using the QR's own structure and error-correction redundancy instead of guessing.
</p>

<p align="center">
  <a href="skills/damaged-qr-recovery/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-Damaged%20QR-2563eb?style=flat-square" alt="Agent Skill"></a>
  <a href="https://github.com/Abolfazlshahi/damaged-qr-recovery-skill/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/Abolfazlshahi/damaged-qr-recovery-skill/test.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square" alt="Python 3.10+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111827?style=flat-square" alt="MIT License"></a>
</p>

<p align="center">
  <a href="https://t.me/pythash">Telegram</a>
  &nbsp;·&nbsp;
  <a href="skills/damaged-qr-recovery/SKILL.md">Skill</a>
  &nbsp;·&nbsp;
  <a href="docs/USING_AS_A_SKILL.md">Use as a Skill</a>
  &nbsp;·&nbsp;
  <a href="benchmark/README.md">Benchmarks</a>
  &nbsp;·&nbsp;
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## The idea

You show an agent a QR with a corner covered by a marker.

A normal decoder says **nothing**.

A guessing system invents a plausible URL.

This project takes a different route:

```text
                 DAMAGED QR
                     │
                     ▼
             locate + rectify
                     │
                     ▼
           version / format / mask
                     │
                     ▼
          known / unknown modules
                     │
                     ▼
        official QR data traversal
                     │
                     ▼
       codewords + RS block layout
                     │
                     ▼
       Reed–Solomon erasure solving
                     │
                     ▼
       payload structure + constraints
                     │
                     ▼
             candidate search
                     │
                     ▼
              exact re-encode
                     │
                     ▼
       visible-module proof (0 diff)
                     │
                     ▼
          independent verification
                     │
                     ▼
        UNIQUE / AMBIGUOUS / UNKNOWN
```

> **The goal is not to find a string that works. The goal is to prove what the QR encoded.**

---

## Why ordinary decoding is not enough

QR codes are not just black and white pictures. They are structured error-correcting symbols with function patterns, masking, interleaved codewords, and Reed–Solomon redundancy.

That changes the problem completely.

A decoder is optimized for:

```text
clean image → payload
```

This project is designed for:

```text
damaged image → evidence model → constraints → reconstruction → proof
```

A redacted region is therefore represented as **unknown evidence**, not as a blank area the model is free to imagine.

---

## What makes this different

<table>
<tr>
<td width="50%">

### Evidence-first

Unknown modules stay unknown.

Pixel guesses are never silently promoted into facts.

</td>
<td width="50%">

### QR-native

The recovery process follows the actual QR structure: format, mask, traversal, codewords, blocks, and ECC.

</td>
</tr>
<tr>
<td>

### Algebra before brute force

Reed–Solomon constraints eliminate impossible candidates before expensive searching.

</td>
<td>

### Proof, not plausibility

Recovered data is re-encoded and compared against every trusted visible module.

</td>
</tr>
</table>

---

## The recovery ladder

The Skill deliberately escalates instead of jumping straight to brute force.

| Stage | Objective |
|---|---|
| `01` | Try a normal decoder |
| `02` | Improve crop, scale, threshold, and perspective |
| `03` | Establish version, format, ECC, and mask |
| `04` | Build a tri-state module matrix |
| `05` | Traverse the QR data area correctly |
| `06` | Recover codewords and RS blocks |
| `07` | Solve erasures algebraically |
| `08` | Parse partial payload structure |
| `09` | Apply exact external constraints |
| `10` | Search only the remaining variables |
| `11` | Re-encode the candidate exactly |
| `12` | Compare every known source module |
| `13` | Independently decode the reconstruction |
| `14` | Search for surviving alternatives |

The expensive steps only happen after the cheap structural information has done its work.

---

## The tricks that matter

The repository includes a dedicated hard-case playbook with the practical deductions that make difficult recoveries tractable.

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md)

A few of the important ones:

### 1. Read the mode/count bits before trusting human expectations

A damaged payload may look like it should have 42 bytes while the actual QR count field says 43. That one-byte difference can determine the unknown token length and completely collapse a search space.

### 2. Solve lengths algebraically

When a payload has a known prefix, variable token, known identifier, and fixed suffix:

```text
unknown_length = total_length - known_prefix - known_id - known_suffix
```

Do this before searching characters.

### 3. Treat the QR as a codeword problem, not a pixel problem

A painted rectangle may cover hundreds of pixels while only a much smaller number of QR data/ECC symbols are actually unknown after module mapping.

### 4. Use both format-information copies

Format information has BCH redundancy. Keep alternate format hypotheses alive until downstream evidence resolves them instead of committing to the first noisy read.

### 5. Search all eight masks when necessary

If format information is partially damaged, the mask itself becomes a finite hypothesis set. Test the eight possibilities against the rest of the matrix instead of guessing.

### 6. Use visible ECC bytes as fingerprints

A candidate payload can look perfectly plausible while producing the wrong parity symbols. Regenerated Reed–Solomon parity is often a much stronger filter than text semantics.

### 7. Use GF(256) deltas instead of recomputing everything

When candidates differ in only a few symbols, parity deltas can be used to prune branches faster than fully rebuilding every candidate from scratch.

### 8. Keep segmentation under control

Two encoders can encode the same text but choose different QR segments and therefore produce different matrices. Exact reconstruction may require matching the original segment structure, not merely the decoded text.

### 9. Read mismatch *patterns*, not only mismatch counts

A dense shifted mismatch band often points to geometry or sampling error. Scattered mismatches concentrated around payload regions can indicate a content/encoding mismatch.

### 10. Multi-image evidence beats aggressive guessing

One photograph can hide a module while another reveals it. Register the images to the same grid and merge observations without majority-voting misaligned pixels.

### 11. Search for competitors

Finding one candidate does not prove uniqueness. A forensic recovery should actively attempt to find a second candidate that satisfies the same evidence.

### 12. `NOT_RECOVERED` is a valid success state

When the evidence is insufficient, the correct result is an honest failure — not a confident fabrication.

---

## What the Skill knows

The canonical contract in [`SKILL.md`](skills/damaged-qr-recovery/SKILL.md) covers:

- finder-pattern and quiet-zone geometry;
- perspective correction and module-grid estimation;
- version detection for the QR family;
- BCH-protected format/version information;
- all eight QR mask hypotheses;
- functional-module exclusion;
- uncertainty-aware sampling;
- official zig-zag data traversal;
- codeword reconstruction;
- QR block deinterleaving;
- GF(256) arithmetic;
- Reed–Solomon erasure and error/erasure reasoning;
- partial-bit and partial-byte constraints;
- numeric/alphanumeric/byte/kanji/ECI-aware parsing;
- vendor/schema metadata as explicit constraints;
- bounded candidate search;
- exact matrix regeneration;
- module-by-module validation;
- independent decoder checks;
- multi-image evidence fusion;
- uniqueness analysis;
- failure classification and provenance.

---

## Evidence has provenance

Every important fact should be traceable.

| Tag | Meaning |
|---|---|
| `OBSERVED` | Directly visible in the source evidence |
| `RECOVERED_BY_RS` | Determined by QR parity constraints |
| `CONSTRAINED_BY_METADATA` | Narrowed by trusted external context |
| `INFERRED_UNVERIFIED` | Plausible but not proven |

This distinction matters because a printed ticket number can constrain a QR candidate without being proof that the same bytes were encoded inside the QR.

---

## Confirmation standard

A serious recovery should survive a chain like this:

```text
✓ structural consistency
✓ correct version / ECC / mask
✓ valid codeword and block layout
✓ RS parity consistency
✓ valid payload representation
✓ exact re-encoding
✓ zero trusted visible-module contradictions
✓ independent decoder success
✓ competing-candidate search
```

The final result is classified as:

```text
CONFIRMED
AMBIGUOUS
PARTIAL
NOT_RECOVERED
INVALID_INPUT
```

---

## A tiny example of the mindset

Suppose the damaged QR appears to have this shape:

```text
Http://example/P/<unknown-token><known-id>/True
```

Do **not** start by generating random tokens.

First derive:

```text
mode
count
fixed bytes
unknown byte positions
RS block membership
visible parity symbols
```

Then:

```text
candidate token
      ↓
construct codewords
      ↓
RS parity
      ↓
reject/keep
      ↓
exact matrix
      ↓
visible-module comparison
```

That is the difference between **guessing a QR** and **recovering a QR**.

---

## Repository anatomy

```text
.
├── skills/
│   └── damaged-qr-recovery/
│       ├── SKILL.md                  # canonical agent contract
│       └── references/               # deep technical knowledge
│           ├── qr-structure.md
│           ├── reed-solomon.md
│           ├── block-layout.md
│           ├── recovery-strategies.md
│           ├── validation.md
│           └── recovery-tricks.md
│
├── src/damaged_qr_recovery/          # reusable Python primitives
├── commands/                         # inspect/recover/validate/audit entry points
├── adapters/                         # agent-runtime guidance
├── scripts/                          # small forensic helpers
├── examples/                         # safe/redacted examples
├── benchmark/                        # reproducible recovery benchmark design
├── tests/                            # unit + smoke tests
├── docs/                             # architecture, threat model, contracts
├── .github/                          # CI + issue templates
├── AGENTS.md                         # repository-level agent guidance
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── pyproject.toml
└── LICENSE
```

---

## Use it as an Agent Skill

The Skill itself is dependency-free Markdown.

```text
skills/damaged-qr-recovery/SKILL.md
```

For a generic Skill runtime, copy the directory into its skill collection:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

Then let the agent activate it for tasks involving damaged QR reconstruction, validation, or recovery auditing.

See [`docs/USING_AS_A_SKILL.md`](docs/USING_AS_A_SKILL.md) for runtime-agnostic guidance.

---

## Optional Python toolkit

The repository also contains implementation primitives and small CLI helpers.

```bash
python -m pip install -e '.[all]'
pytest
```

Inspect a QR image:

```bash
python scripts/inspect_qr.py image.png
```

Compare two matrices/images at a coarse level:

```bash
python scripts/compare_modules.py observed.png reconstructed.png --size 33
```

Validate an independently generated reconstruction:

```bash
python scripts/validate_reconstruction.py reconstructed.png
```

The helpers are intentionally conservative: they support the workflow but do not pretend generic image decoding can replace algebraic reconstruction.

---

## Commands

| Command | Purpose |
|---|---|
| [`inspect`](commands/inspect.md) | Establish structure and evidence without guessing |
| [`recover`](commands/recover.md) | Run the full evidence-first recovery workflow |
| [`validate`](commands/validate.md) | Test a proposed reconstruction |
| [`audit`](commands/audit.md) | Try to break a claimed recovery |

Think of `audit` as the “prove you're not fooling yourself” step.

---

## Benchmarks

The benchmark philosophy is intentionally different from a normal QR decoder benchmark.

We care about:

```text
exact recovery
+ false-confirmation resistance
+ reproducibility
```

Useful dimensions include:

| Dimension | Examples |
|---|---|
| Damage | random erasure, rectangle, scratch, clipping |
| Image quality | blur, JPEG, low resolution, thresholding |
| Geometry | perspective, rotation, skew |
| QR structure | version, ECC level, mask |
| Evidence | single image vs. multiple images |
| Knowledge | no metadata vs. partial schema/identifier |
| Outcome | recovered, ambiguous, not recoverable |

See [`benchmark/README.md`](benchmark/README.md).

---

## Safety & privacy

A QR can contain far more than a harmless URL. It may encode:

- personal information;
- ticket identifiers;
- payment information;
- private links;
- session identifiers;
- authentication material;
- contact records.

The toolkit therefore treats payloads as **data**, not commands.

It does not automatically visit recovered URLs, authenticate to services, or turn recovered secrets into actions.

For public benchmarks, use synthetic or redacted fixtures.

See [`SECURITY.md`](SECURITY.md) and [`docs/threat-model.md`](docs/threat-model.md).

---

## Design rule

The project follows one rule above everything else:

> **Never spend certainty you do not have.**

A blurry module can remain uncertain.

A partially recovered byte can remain partially recovered.

A payload can remain ambiguous.

The system only becomes confident when the QR itself provides enough evidence to justify that confidence.

---

## Roadmap

The architecture is already split so the recovery method and implementation can evolve independently.

### Core engine

- [ ] complete QR version 1–40 capacity/block tables;
- [ ] production-grade geometry estimator;
- [ ] soft-confidence module sampler;
- [ ] complete error + erasure RS solver;
- [ ] exact segment-preserving encoder;
- [ ] bounded candidate-search engine;
- [ ] multi-image registration/fusion;
- [ ] forensic replay/export format.

### Agent ecosystem

- [ ] richer Claude/Codex/Gemini/OpenClaw adapters;
- [ ] plugin manifests where runtimes support them;
- [ ] reusable audit command for agent-generated claims;
- [ ] portable example packs.

### Verification

- [ ] synthetic damage generator;
- [ ] property-based tests;
- [ ] fuzzing;
- [ ] adversarial false-confirmation suite;
- [ ] reproducible benchmark reports.

---

## Community

Built and maintained by **Abolfazl Shahi**.

<p align="center">
  <a href="https://github.com/Abolfazlshahi">GitHub</a>
  &nbsp;·&nbsp;
  <a href="https://t.me/pythash">Telegram / @pythash</a>
</p>

---

## Support the project

Optional project donations are documented in [`docs/DONATIONS.md`](docs/DONATIONS.md).

Please verify the network before sending any funds.

---

## License

MIT — see [`LICENSE`](LICENSE).

<p align="center">
  <sub>Recover evidence. Rebuild structure. Prove the result.</sub>
</p>
