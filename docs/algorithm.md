# Algorithm Walkthrough

This is the implementation map behind the Agent Skill.

## A. Image evidence

1. Preserve the original image and record dimensions, channels, and transformations.
2. Detect finder-pattern candidates or accept trusted manual QR bounds.
3. Estimate the quadrilateral and rectify to a square grid.
4. Keep a confidence map; never turn blur or paint into false certainty.

## B. Structural metadata

For a QR version `v`, the module count is `17 + 4*v` (equivalently `21 + 4*(v-1)`). Read both format-information copies and version information for versions 7+ when present. Use BCH/Hamming-distance logic only when the evidence supports choosing a codeword.

## C. Module matrix

Sample module centers after rectification. Classify each cell as known black, known white, or unknown. Mark function modules separately.

## D. Codewords

Exclude function modules, unmask data modules, then follow the official two-column zig-zag. Convert bits into codewords and apply the exact version/ECC block table before RS decoding.

## E. Reed–Solomon

Map unknown module bits into uncertain symbols. Solve pure erasures first. If necessary, handle bounded symbol errors next. Verify the complete block against parity after every candidate.

## F. Payload

Parse mode/count/data/terminator/padding exactly. Preserve raw bytes and ECI semantics; do not normalize a string into a different byte sequence.

## G. Proof

Re-encode a surviving payload with the same structural parameters, compare every known source module, and use an independent decoder. Search for competing candidates before declaring uniqueness.
