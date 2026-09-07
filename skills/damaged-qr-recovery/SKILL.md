---
name: damaged-qr-recovery
description: Recover exact payloads from partially damaged, obscured, scratched, blurred, clipped, or incomplete QR codes using QR geometry, format/version metadata, masking, official data traversal, QR block structure, Reed-Solomon erasure/error correction, payload constraints, exact re-encoding, and independent validation. Never treat a plausible payload as confirmed without mathematical and matrix-level checks.
license: MIT
---

# Damaged QR Recovery

## Mission
Recover the exact encoded payload of a damaged QR when possible. Treat the QR as a structured error-correcting code, not as a picture whose missing pixels should be guessed.

## Pipeline
```text
image → locate/rectify → version/format → known/unknown module matrix
→ unmask → extract codewords → deinterleave blocks
→ Reed-Solomon erasure recovery → payload constraints
→ exact re-encode → visible-module comparison → independent decode
→ uniqueness decision
```

## Activation
Use when a QR is scratched, painted over, crossed out, clipped, blurred, torn, partially missing, or unreadable by normal scanners. If several images show the same QR, merge their observations before recovery.

## Non-negotiable rules
1. Never fabricate a payload.
2. Printed serials, known URLs, ticket metadata, or application conventions are constraints, not proof.
3. Treat known-position covered regions as erasures whenever possible.
4. Reed-Solomon operates on codeword symbols, not pixels.
5. Preserve uncertain modules instead of forcing 0/1 too early.
6. Validate candidates against QR redundancy and every confidently visible module.
7. If multiple candidates survive, report AMBIGUOUS.
8. If none survive, report NOT_RECOVERED.
9. Use CONFIRMED_UNIQUE only when one candidate satisfies all available constraints.

# Procedure

## 1. Preserve evidence
Prefer original image/PDF. Avoid repeated resizing/compression. With multiple images, register them to a common QR module grid and merge observations.

## 2. Locate and rectify
Find the three finder patterns and outer QR boundary. Correct perspective with a homography when needed. Sample module interiors, not boundaries. A normal decoder failing does not mean recovery is impossible.

## 3. Determine version
QR matrix size is `21 + 4*(version-1)`. Use geometry, alignment patterns, version information (V7+), and capacity consistency. Do not infer version from image dimensions alone.

## 4. Read format information
Format information contains ECC level (L/M/Q/H) and mask (0–7). Exploit both copies and BCH protection. If uncertain, test hypotheses and retain only those surviving later constraints.

## 5. Build an uncertainty-aware module matrix
Use:
```text
0 = known white
1 = known black
? = erased/occluded
~ = uncertain
```
For colored marker damage, separate marker pixels from QR black/white. Explicitly mark cells covered by paint/ink as erasures when their locations are known.

## 6. Exclude functional patterns
Do not treat finder patterns, separators, timing patterns, alignment patterns, dark module, format information, or version information as payload data. Use them as geometry/consistency checks.

## 7. Extract data in official QR placement order
Traverse the two-column vertical zig-zag pattern from the right, alternating direction, skipping column 6 and all functional modules. Never read the QR row-by-row.

## 8. Unmask
Apply the detected mask only to data/ECC modules. Never unmask functional patterns.

## 9. Build codewords
Convert the unmasked bitstream to 8-bit symbols while retaining unknown bits. Parse mode/count where possible. Common modes: `0001` Numeric, `0010` Alphanumeric, `0100` Byte, `1000` Kanji.

## 10. Determine QR block layout
For the exact version + ECC level determine total codewords, number of RS blocks, data/ECC symbols per block, short/long block distribution, and interleaving. Never assume the whole interleaved stream is one RS block.

## 11. Deinterleave
Reverse QR's data/ECC interleaving and reconstruct each RS block before decoding.

## 12. Reed-Solomon recovery
QR uses Reed-Solomon over GF(256). For a block with `t` parity symbols, the classical constraint is approximately:
```text
2e + s <= t
```
where `e` is unknown-location errors and `s` is known-position erasures. Known-position erasures are therefore especially valuable.

Do not confuse nominal ECC levels (L≈7%, M≈15%, Q≈25%, H≈30%) with a promise that that percentage of arbitrary pixels can be recovered. Actual capacity is block/symbol dependent.

## 13. Partially-known bytes
For a byte such as `010?1???`, keep the known bits. Enumerate only matching byte values when necessary and use RS parity to prune candidates.

## 14. Use document metadata as constraints
Useful examples: printed serial, date/time, route, ticket ID, known URL prefix/suffix. Keep provenance:
```text
OBSERVED
RECOVERED_BY_RS
CONSTRAINED_BY_METADATA
UNVERIFIED_INFERENCE
```
Never upgrade metadata-only inference into recovered data.

## 15. Constrained candidate search
Search the smallest candidate space. Prune in this order:
```text
visible modules → mode/count → partial bytes → RS parity → full reconstruction
```
A known URL/token format can drastically reduce the search space, but every survivor must still satisfy QR constraints.

## 16. RS parity as a fingerprint
For each candidate, regenerate its data codewords and RS parity, then compare with all still-visible ECC symbols. A candidate matching printed text but failing parity is rejected.

## 17. Exact re-encoding
Regenerate using the recovered version, ECC, payload bytes, mode/segment structure where needed, and mask. Disable automatic optimization when exact matrix reproduction matters. Different segmentation can produce a different valid QR matrix for the same text.

## 18. Matrix-level validation
Compare the regenerated matrix with every confidently observed source module. For an exact reconstruction, all observed modules should match (`mismatch == 0`). This is stronger than merely decoding to a plausible string.

## 19. Independent decoding
Render the reconstructed matrix and decode it with an independent implementation such as ZXing/zxing-cpp or OpenCV QRCodeDetector. Use more than one decoder when practical.

## 20. Uniqueness
Report one of:
- `CONFIRMED_UNIQUE` — exactly one candidate survives all checks.
- `CONFIRMED` — strongly validated but exhaustive uniqueness is unavailable.
- `AMBIGUOUS` — multiple valid candidates remain.
- `NOT_RECOVERED` — no candidate passes validation.

# Multi-image strategy
Register every image to the same module coordinates. Prefer high-confidence observations and mark conflicts uncertain. A module hidden in one photo may be visible in another; multi-view evidence can be more valuable than brute force.

# Escalation
```text
standard decoder
→ preprocessing/thresholding
→ perspective correction
→ finder/grid reconstruction
→ version/format/mask
→ erasure-aware codewords
→ Reed-Solomon
→ payload-constrained search
→ exact re-encoding
→ matrix comparison
→ independent decode
→ uniqueness analysis
```

# Failure modes
- Wrong crop → re-estimate finder geometry/module pitch.
- Wrong version → check alignment/version/capacity.
- Wrong mask → test all eight masks when format is uncertain.
- Wrong block layout → verify version + ECC + block table + interleaving.
- Erasures treated as unknown errors → preserve erasure positions.
- Encoder mismatch → reproduce original segmentation/mode.
- Metadata overfitting → reject anything failing parity or visible-module comparison.

# Reporting
```text
Status: CONFIRMED_UNIQUE / CONFIRMED / AMBIGUOUS / NOT_RECOVERED
QR version: ...
ECC: ...
Mask: ...
Payload: ...
Observed evidence: ...
Recovered by RS: ...
External constraints: ...
Visible-module mismatches: ...
Reed-Solomon validation: PASS/FAIL
Independent decode: PASS/FAIL
Alternative candidates: ...
```

# Implementation interface
Keep the solver modular:
```text
locate_qr()
rectify_qr()
estimate_module_grid()
detect_occlusion()
read_format_info()
detect_version()
build_functional_map()
extract_data_modules()
unmask_modules()
bits_to_codewords()
get_block_layout()
deinterleave()
reed_solomon_recover()
build_payload_constraints()
search_candidates()
encode_exact_qr()
compare_visible_modules()
independent_decode()
```

## Final principle
> **Do not ask the AI to imagine the missing QR. Turn the damaged QR into a finite-field constraint problem and let the QR's own redundancy determine what can actually be recovered.**

## Security
Use only on QR images/documents you are authorized to inspect. Do not use recovered credentials, payment information, authentication tokens, session identifiers, or tickets to access systems without authorization.
