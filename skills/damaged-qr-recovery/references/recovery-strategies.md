# Recovery Strategies

This document is the decision tree behind the main Skill. The goal is to spend effort only where it reduces uncertainty.

## Stage 0 — direct decode

Run a standard decoder first. A successful decode is cheap evidence.

When the source is damaged and exact recovery matters, still validate the result against the source matrix. “Decoder succeeded” and “source payload proven” are different claims.

## Stage 1 — geometry

Improve, in order:

```text
crop
→ scale
→ grayscale/threshold variants
→ finder-based corner estimation
→ perspective correction
→ module-center sampling
```

Do not inpaint missing data and then feed the inpainted pixels back as if they were observations.

## Stage 2 — structural extraction

Recover:

```text
version
format
ECC
mask
function-module map
tri-state matrix
```

Branch only over small finite hypotheses. A wrong version or mask poisons every downstream stage.

## Stage 3 — codeword extraction

Serialize only data/ECC modules using the official QR traversal. Then:

```text
bits
→ bytes
→ interleaved codewords
→ RS blocks
```

Keep the exact coordinate-to-codeword mapping. It becomes extremely valuable when relating an image occlusion to a missing RS symbol.

## Stage 4 — algebraic recovery

Prefer known-position erasures over guessed errors.

For each RS block:

1. enumerate unknown symbol positions;
2. preserve all known symbols;
3. solve erasures when possible;
4. verify the full block's parity/syndromes;
5. only then consider bounded error/erasure search.

## Stage 5 — payload constraints

Once a valid partial payload interpretation exists, apply hard constraints:

- fixed prefix/suffix;
- exact length;
- known mode/segment type;
- token alphabet;
- printed identifier equality;
- ECI/encoding expectations;
- trusted vendor schema.

Constraints are filters, not replacements for recovered bytes.

## Stage 6 — candidate search

If unknown fields remain:

```text
calculate degrees of freedom
→ derive fixed bits
→ derive allowed bytes
→ prune with mode/count/capacity
→ prune with RS parity
→ re-encode survivors
→ compare visible modules
```

Search the smallest variable set, not the largest human-readable string.

## Stage 7 — exact reconstruction

For each serious candidate, reproduce:

- version;
- ECC;
- segmentation/mode;
- byte representation/ECI;
- mask;
- exact matrix construction.

Automatic encoder optimization may produce a different but valid QR. Control it when exact source matching matters.

## Stage 8 — source proof

Compare every trusted source module with the candidate matrix.

```text
mismatch == 0
```

is the strongest simple physical test when geometry and the trusted evidence map are correct.

Save mismatch coordinates when non-zero; their shape often diagnoses the failing layer.

## Stage 9 — independent validation

Decode the regenerated QR with an implementation independent from the reconstruction logic. More than one decoder is useful when available.

## Stage 10 — uniqueness

Do not stop because the first candidate works. Search for a competing candidate whenever the residual search space is small enough.

If multiple exact candidates survive, report `AMBIGUOUS`.

---

# High-value decision patterns

## Pattern A — damaged QR but mostly readable

Do not start with brute force.

Use:

```text
geometry
→ module map
→ mask/traversal
→ codewords
→ RS
```

The QR's redundancy may solve the missing region directly.

## Pattern B — payload schema is obvious, token is missing

Use:

```text
mode/count bits
→ exact payload length
→ fixed-prefix/suffix subtraction
→ token byte constraints
→ visible RS parity
→ exact re-encode
```

The common mistake is assuming token length from visual guesswork.

## Pattern C — printed serial is visible, QR is damaged

Treat the printed serial as a strong external constraint. Test equality between the candidate QR field and the printed field, but preserve the provenance label `CONSTRAINED_BY_METADATA` until QR evidence itself confirms the bytes.

## Pattern D — reference QR is available

Extract generator conventions first:

```text
format/version tendencies
segment style
field sizes
alphabet
fixed strings
encoding/ECI
```

Then use those facts to shrink the search of the damaged QR.

## Pattern E — decoder gives a plausible but untrusted result

Do not accept it immediately. Run:

```text
candidate
→ RS parity check
→ source-module comparison
→ independent decode
→ alternative-candidate search
```

## Pattern F — only a few bytes remain unknown

Use RS parity as a fingerprint. Candidate bytes that are semantically plausible but induce the wrong ECC bytes should be discarded immediately.

## Pattern G — several photos exist

Use the photos as complementary observations, not competing “best images”. Register each to module coordinates and merge evidence at the module level.

---

# Search heuristics

## Structural constraints before semantic constraints

A useful order is:

```text
format/version
→ function map
→ traversal
→ mode/count
→ fixed bits
→ byte alphabet
→ payload schema
→ metadata
→ RS parity
→ matrix proof
```

## Cheap rejection before expensive rendering

Reject candidates before generating PNGs or calling external decoders when they already fail:

- fixed payload bytes;
- mode/count legality;
- capacity;
- known ECC symbols;
- RS parity.

## Branch-and-bound

When a partial assignment already causes a contradiction, prune it immediately. For large candidate spaces, branch on the byte with the strongest available constraint first.

## Delta updates

When candidates differ by only one or two data symbols, exploit the linearity of RS parity and update the parity delta instead of recomputing all candidate reasoning from scratch.

## Coordinate-aware diagnosis

When source-module comparison fails, inspect the spatial mismatch pattern before changing the payload hypothesis.

---

# Anti-patterns

### Brute-force first

Bad:

```text
all strings of length N
```

Good:

```text
derive N
→ derive alphabet
→ derive fixed positions
→ derive RS constraints
→ enumerate survivors
```

### Trusting visual similarity

Two matrices can look almost identical while encoding different data. Use exact module comparison.

### Treating all damage as random errors

Known-position occlusion is an erasure problem. Preserve that information.

### Assuming one RS block

QR data is interleaved across blocks. Always use the exact version/ECC layout.

### Assuming the decoded text uniquely identifies the matrix

Different segmentations or encoder choices can encode the same text into different matrices.

### Publishing real recovery fixtures

Use synthetic or redacted payloads in public tests/benchmarks.

---

# Stopping rules

Return `NOT_RECOVERED` when:

- geometry cannot be established;
- structural hypotheses remain contradictory;
- a critical RS block is underdetermined beyond available constraints;
- candidate search is unbounded and no legitimate narrowing information exists.

Return `AMBIGUOUS` when two or more candidates satisfy the same trusted constraints and source-module proof.

A solver that refuses to invent missing data is behaving correctly.
