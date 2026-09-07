# Recovery Strategies

## Stage 0 — direct decode

Try a standard QR decoder first. A successful decode is cheap evidence, but still re-encode and validate when the source is damaged and exactness matters.

## Stage 1 — better geometry

Improve cropping, perspective correction, scale, and module-center sampling.

## Stage 2 — structural extraction

Recover version, format, mask, and function modules. Build a tri-state matrix.

## Stage 3 — algebraic recovery

Serialize bits, deinterleave blocks, and solve RS erasures. This is the preferred way to recover truly missing symbols.

## Stage 4 — constrained search

If a few fields remain unknown, use exact constraints such as fixed prefixes, lengths, alphabets, and printed identifiers. Search the smallest remaining variable set.

## Stage 5 — multiple images

Register additional images and fuse only module observations supported by alignment/confidence evidence.

## Search discipline

- Never brute-force a large unconstrained token space.
- Never select the first candidate that decodes.
- Keep all candidates until source-module validation and uniqueness checks finish.
- Record the constraints used to prune the search.
