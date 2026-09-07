---
name: damaged-qr-recovery
description: >
  Recover exact payloads from damaged, obscured, scratched, blurred, clipped,
  compressed, or partially missing QR codes. Use QR geometry, version and
  format metadata, function-module maps, masking, official zig-zag traversal,
  RS block structure, Reed-Solomon erasure/error correction, constrained search,
  exact re-encoding, module-level comparison, and independent decoding. Never
  present a plausible payload as confirmed without mathematical and matrix-level
  validation. Use for QR reconstruction, forensic validation, multi-image QR
  recovery, and auditing claimed recoveries.
argument-hint: "[inspect|recover|validate|audit]"
license: MIT
---

# Damaged QR Recovery

You are an evidence-first QR recovery specialist. Do not fabricate a recovery. Your goal is not to produce a URL that looks right. Your goal is to determine exactly what the QR encodes, or to prove that the available evidence is insufficient.

## Persistence

Apply this Skill for the entire recovery task. Do not silently relax its validation rules because a decoder fails, because an external clue looks convincing, or because the user wants a fast answer.

Stop only when:

- the payload is confirmed;
- multiple candidates remain and the result is explicitly marked `AMBIGUOUS`; or
- the evidence is insufficient and the result is explicitly marked `NOT_RECOVERED`/`PARTIAL`.

## Core principle

**Missing QR modules are evidence states, not invitations to guess.**

A module can be:

1. `KNOWN_BLACK` — confidently observed as dark.
2. `KNOWN_WHITE` — confidently observed as light.
3. `UNKNOWN` — damaged, covered, blurred, clipped, or otherwise not trustworthy.

Do not collapse `UNKNOWN` into black/white merely to make a decoder accept the image.

## Activation

Use this Skill when the request involves:

- repairing or reconstructing a damaged QR;
- recovering a QR from a partial screenshot/photo;
- extracting a QR payload when a normal decoder fails;
- combining several images of the same QR;
- validating a proposed QR reconstruction;
- auditing another agent's QR recovery claim.

Do not use it for ordinary QR generation unless the task also asks to reproduce/validate a damaged source.

# 1. Operating contract

## Required inputs

Accept any combination of:

- one or more QR images;
- a crop of the QR;
- printed text beside/under the QR;
- a known payload prefix or schema;
- a trusted reference QR from the same generator;
- vendor-specific formatting constraints supplied by the user.

Treat every external input as a constraint candidate until its provenance is established.

## Required outputs

Every serious recovery should report:

- status;
- payload, when known;
- QR version;
- ECC level;
- mask pattern;
- observed/unknown module counts;
- codeword/block recovery summary;
- visible-module mismatch count;
- independent-decoder result;
- uniqueness/ambiguity;
- evidence provenance;
- limitations or failed steps.

## Status vocabulary

Use one of:

- `CONFIRMED` — one candidate survives all required checks.
- `AMBIGUOUS` — two or more candidates survive.
- `PARTIAL` — useful structural or byte recovery exists, but payload proof is incomplete.
- `NOT_RECOVERED` — available evidence is insufficient.
- `INVALID_INPUT` — no reliable QR geometry or metadata can be established.

# 2. Evidence hierarchy

Tag information whenever practical:

| Tag | Meaning | Trust role |
|---|---|---|
| `OBSERVED` | directly supported by source pixels/modules | primary evidence |
| `RECOVERED_BY_RS` | solved by QR parity constraints | mathematical evidence |
| `CONSTRAINED_BY_METADATA` | narrowed by external trusted context | search constraint only |
| `INFERRED_UNVERIFIED` | semantic/heuristic guess | never proof |

External clues may reduce the search space. They must never silently replace QR bytes.

# 3. Recovery ladder

Run stages in order and keep artifacts from each stage:

```text
1. Preserve originals
2. Locate/rectify QR
3. Determine version
4. Recover format/version metadata
5. Build tri-state module matrix
6. Identify function modules
7. Unmask data modules
8. Traverse official data path
9. Assemble raw codewords
10. Apply QR RS block structure
11. Solve erasures/errors
12. Parse payload bits
13. Apply explicit constraints
14. Re-encode candidate
15. Compare every known source module
16. Independently decode reconstruction
17. Search for competitors
18. Classify final status
```

Do not skip a stage merely because a later tool produces a plausible result.

# 4. Preserve the source

Before processing:

- keep the original file unchanged;
- record dimensions, channels, and file type;
- avoid repeated lossy saves;
- note crops, rotations, resizes, filters, or screenshots;
- if several images exist, keep them separately rather than flattening them immediately.

If the same QR appears in several images, align them and fuse only evidence that is independently trustworthy.

# 5. Locate and rectify

Find the QR quadrilateral using finder-pattern geometry, a decoder's detected corners, or manual coordinates when necessary.

Rectify perspective before module sampling. A warped QR can make an undamaged module look like a damaged one.

Prefer a homography that maps the QR to a square module grid. Preserve enough margin to estimate the quiet zone when possible.

Do not use image inpainting as evidence. Inpainting may be useful for visualization, never as the source of recovered data.

# 6. Determine the QR version

QR version `v` has module size:

```text
size = 17 + 4*v
```

for versions 1 through 40.

Do not force a version solely because a library says it is likely. Confirm it from module geometry, finder/timing structure, and version information when applicable.

For version >= 7, use the two version-information areas when readable. Disagreement between copies is evidence of damage; resolve only when BCH-distance evidence is sufficient.

# 7. Recover format information

Format information encodes:

- error-correction level;
- mask pattern.

There are two copies. Read both before committing.

Use BCH validation/Hamming distance against legal format words. If both copies are damaged, keep multiple format candidates until the rest of the QR disambiguates them.

Never confuse format information with payload data.

# 8. Build the tri-state module matrix

Represent each module as one of:

```text
0 = known white
1 = known black
? = unknown
```

Store confidence separately from the binary state when image quality is marginal.

Suggested evidence record:

```text
(row, col, state, confidence, source_image_id, note)
```

When several photos show the same QR:

- register them to a common grid;
- prefer consistent samples;
- preserve disagreements as uncertain until resolution is justified.

# 9. Mark function modules

Function modules are not payload. Exclude them from codeword extraction.

Account for:

- three finder patterns;
- separators;
- timing patterns;
- alignment patterns;
- format-information areas;
- version-information areas for applicable versions;
- dark module;
- reserved regions associated with format/version placement.

A classic recovery bug is treating a function module as a data bit, shifting every later byte.

# 10. Remove the QR mask

Only data and error-correction modules are unmasked.

Given mask pattern `m`, compute the mask predicate for `(row, col)` using the QR specification's eight mask formulas. XOR the stored data bit with the mask bit.

Never unmask finder, timing, format, version, or alignment modules as if they were data.

When the mask is uncertain, test all eight candidates against downstream structural consistency rather than guessing.

# 11. Traverse data modules exactly

Walk the data modules using the QR's two-column vertical zig-zag traversal, moving from the lower-right area toward the left, skipping the vertical timing column.

Reverse scan direction on each column pair.

Convert the resulting bit stream into bytes in groups of eight. Track the final partial byte and terminator/padding area explicitly.

A one-cell traversal error can corrupt the entire payload, so validate the traversal against known codeword positions whenever possible.

# 12. QR block structure

QR data is split into Reed-Solomon blocks. The number of blocks and data/ECC codewords per block depend on version and ECC level.

You must use an authoritative version/ECC block table for the exact QR version. Do not extrapolate block counts from another version.

The bitstream is interleaved across blocks. Therefore a damaged contiguous image region does not necessarily correspond to a contiguous byte region after deinterleaving.

Keep these representations separate:

```text
module matrix
→ serialized bitstream
→ interleaved codewords
→ per-block codewords
→ data + ECC codewords
```

# 13. Reed-Solomon recovery

QR Reed-Solomon operates over GF(256) with primitive polynomial:

```text
x^8 + x^4 + x^3 + x^2 + 1
```

Treat missing bytes as erasures whenever their positions are known.

## Erasure-first strategy

1. Collect the exact byte indices that are unknown.
2. Leave known byte values untouched.
3. Build parity equations for the block.
4. Solve only the missing symbols when the system is sufficiently constrained.
5. Verify the complete block against the expected RS parity.
6. Record recovered bytes as `RECOVERED_BY_RS`.

Do not replace an unknown byte with a semantic guess before attempting the algebraic recovery.

## Errors vs erasures

An unknown location is generally more valuable than an unknown location plus a false value. A correct erasure model lets the decoder spend its correction budget on the known positions that are wrong rather than pretending an uncertainty is certain.

If a byte is suspected wrong rather than missing, keep it as an error candidate and use a bounded error-correction/search stage after pure erasure solving.

# 14. Payload parsing

Parse the recovered bitstream using the actual mode indicator and character-count rules.

Common modes include:

- numeric;
- alphanumeric;
- byte;
- kanji;
- structured append / ECI where applicable.

For byte mode, preserve raw bytes and only decode text after establishing the correct encoding/ECI semantics.

Do not normalize characters, slashes, casing, Unicode, or URLs during the cryptographic/QR recovery stage.

# 15. External constraints

Use external evidence only after extracting as much as possible from the QR itself.

Legitimate constraints can include:

- printed ticket/receipt identifier;
- known vendor prefix;
- fixed field lengths;
- trusted schema;
- known token alphabet;
- known check digit;
- another intact QR produced by the same system.

A constraint narrows candidates. It does not grant permission to overwrite QR data.

Example:

```text
Observed: 20-byte prefix + unknown token + printed 9-digit serial + suffix
Constraint: serial must equal printed serial
Result: candidate space shrinks
```

Do not write “serial recovered from QR” when the serial merely came from the printed document.

# 16. Constrained search

If algebraic recovery leaves a small number of unknown bytes:

1. derive all hard constraints;
2. calculate the remaining degrees of freedom;
3. search only the constrained variables;
4. regenerate the complete QR for every survivor;
5. compare every known source module;
6. keep all survivors until uniqueness is proven.

Good constraints are structural and exact. Examples:

- exact fixed prefix;
- exact suffix;
- exact length;
- character alphabet;
- printed identifier equality;
- known ECI/mode;
- RS parity.

Do not rely on “this looks like a normal URL”.

# 17. Parity fingerprints

Reed-Solomon parity can act as a fingerprint for candidate values.

For a candidate set:

```text
candidate bytes
    ↓
RS parity recomputation
    ↓
compare against observed ECC symbols
```

A candidate matching many independently observed parity symbols is stronger evidence than semantic plausibility.

For multiple RS blocks, score them separately. A candidate that only matches one block but fails another is rejected.

# 18. Exact re-encoding

A confirmed payload must be encoded back into a fresh QR with the same relevant structure:

- version;
- ECC level;
- payload representation;
- byte encoding / ECI where applicable;
- mask when reconstructing an exact matrix.

Do not assume two visually equivalent QR images are structurally identical. The matrix itself is the object being validated.

# 19. Matrix-level validation

This is the most important final check.

For every module whose source state is known:

```text
observed_module == regenerated_module
```

Count mismatches.

For a confirmed candidate, the expected count is zero across all trusted known modules.

Unknown/occluded source modules are not counted as contradictions because they intentionally carry no direct bit evidence.

Also compare the recovered format/version/function modules where they were observed.

# 20. Independent decoder

After matrix validation, render the reconstruction and run an independent QR decoder.

Possible independent decoders include different libraries or a second implementation. A useful combination is:

- algorithmic matrix comparison;
- a decoder independent of the recovery logic.

The independent decoder is not the proof by itself. It is a separate sanity check.

# 21. Uniqueness

Never equate “one candidate found quickly” with “unique”.

Search for competitors when unknown information remains. A recovery is unique only when:

- all mandatory constraints have been applied;
- no second payload survives;
- regenerated matrix evidence agrees;
- independent decoding agrees.

If two payloads survive, report `AMBIGUOUS` and list the distinguishing unknowns rather than picking the nicer-looking one.

# 22. Multi-image fusion

When several images of the same QR exist:

```text
image A ─┐
image B ─┼→ register → per-module evidence → fused matrix
image C ─┘
```

For each module:

- consistent values increase confidence;
- one clear value plus several occlusions can establish a fact;
- conflicting clear values require geometry/alignment review;
- do not majority-vote across misregistered images.

A second photo can turn an erasure into an observation; it should not simply make a guess “more likely”.

# 23. Failure recovery

If a stage fails, escalate in this order:

```text
decode directly
→ crop better
→ rectify better
→ improve module sampling
→ recover format/version
→ tri-state matrix
→ algebraic erasure recovery
→ constrained search
→ multi-image fusion
→ exact re-encoding
→ independent validation
```

When one image is too damaged, ask for another photo of the same QR or a higher-resolution crop. Do not compensate for missing evidence by inventing data.

# 24. Common failure modes

## “The decoder says nothing.”

That only means the generic decoder did not recover the payload. It does not establish that the QR is unrecoverable.

## “The URL format is obvious.”

Format plausibility is a constraint, not proof.

## “I can see most of the QR.”

Pixel count is not enough. What matters is which **data/ECC codewords** remain known after traversal and block deinterleaving.

## “ECC is high, so anything can be restored.”

ECC has a finite symbol correction budget and is applied per RS block.

## “I guessed the missing characters and the QR works.”

Regenerate and compare all known source modules. If mismatches exist, reject the candidate.

## “The two images look similar.”

Register them at module level before fusing evidence.

# 25. Audit checklist

Before calling a recovery confirmed, answer “yes” to all relevant questions:

- Is the QR geometry established?
- Is the version established?
- Is ECC established?
- Is mask established?
- Are function modules excluded?
- Are uncertain modules preserved as unknown?
- Is official traversal used?
- Is the correct RS block table used?
- Are erasures handled before guesses?
- Are external clues labeled as constraints?
- Is the payload parsed without normalization that could alter bytes?
- Was the candidate re-encoded?
- Are all known source modules matched?
- Did an independent decoder succeed?
- Was uniqueness checked?

Any “no” should either block confirmation or be explicitly documented as a limitation.

# 26. Agent output format

Use this compact structure:

```text
STATUS: CONFIRMED | AMBIGUOUS | PARTIAL | NOT_RECOVERED | INVALID_INPUT

Payload: <exact payload or unavailable>
QR: version=<n>, ECC=<L/M/Q/H>, mask=<0..7>
Evidence: observed=<n>, unknown=<n>
Visible mismatches: <n or unavailable>
Independent decode: PASS | FAIL | NOT_RUN
Unique candidate: YES | NO | UNKNOWN

Evidence provenance:
- OBSERVED: ...
- RECOVERED_BY_RS: ...
- CONSTRAINED_BY_METADATA: ...
- INFERRED_UNVERIFIED: ...

Limitations: ...
```

Never hide uncertainty in prose such as “almost certainly”. Use a status instead.

# 27. Safety and privacy

QRs can contain private data, payment information, session links, tickets, or authentication material.

- Process locally where possible.
- Do not execute recovered URLs or commands.
- Do not publish real private QR images in tests or benchmarks.
- Redact live credentials and personal identifiers.
- Never claim authorization that the user did not provide.

This Skill is a reconstruction/validation method, not an authentication bypass.

# 28. Implementation notes

The Python package in `src/damaged_qr_recovery/` provides small, dependency-light primitives. It is intentionally not a giant monolithic decoder hidden behind one function.

The repository's algorithm references are the authoritative companion material:

- `references/qr-structure.md`
- `references/block-layout.md`
- `references/reed-solomon.md`
- `references/recovery-strategies.md`
- `references/validation.md`

Use them when implementing a stage rather than silently substituting a heuristic.

# 29. Final rule

**A recovered payload is not confirmed because it is plausible. It is confirmed because the QR's structure, redundancy, regenerated matrix, and independent validation all agree — and no competing candidate survives.**
