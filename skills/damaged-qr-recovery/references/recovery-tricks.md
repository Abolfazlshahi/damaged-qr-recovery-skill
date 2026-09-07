# Advanced Damaged-QR Recovery Tricks

This reference collects practical deductions and recovery patterns that are easy to miss when treating a damaged QR as an ordinary image-decoding task.

## 1. Think in symbols, not pixels

QR damage happens in pixels, but Reed-Solomon correction happens in byte-sized codeword symbols. Always translate image damage into:

```text
pixels → modules → bits → codewords → RS blocks
```

A large rectangle in the image can affect surprisingly few useful symbols, while scattered one-module defects can affect many symbols.

## 2. Keep erasures explicit

Use a tri-state matrix and a partial-byte representation. Knowing that a bit is unknown is information; turning it into a random 0/1 loses information and can make later correction harder.

Recommended states:

```text
known 0
known 1
unknown
uncertain
```

## 3. Use the QR itself to discover payload length

Do not infer length from a filename, ticket field, visual text, or what a URL “normally” looks like. Read mode/count bits as early as possible.

When the count field is itself partially damaged, keep several legal count hypotheses and eliminate them with capacity and RS constraints.

## 4. The “we expected N bytes” trap

A frequent mistake is assuming an expected payload length and then forcing a byte count that agrees with that assumption. A single damaged count bit changes the interpretation of everything after it.

Always distinguish:

```text
expected length from document schema
vs.
encoded length from QR bits
```

## 5. Prefix/suffix subtraction

If an application has a known schema:

```text
fixed prefix + unknown token + known field + fixed suffix
```

calculate the exact token length from the QR-derived character count first. This often turns an apparently huge unknown region into a manageable finite search.

## 6. Use a reference QR from the same generator

An intact QR from the same producer is useful for discovering:

- version tendencies;
- ECC selection;
- mask/encoding patterns;
- segment style;
- fixed URL syntax;
- field widths;
- token alphabet;
- whether the producer uses ECI;
- whether a library's automatic segmentation must be disabled for exact re-encoding.

It is a schema oracle, not a byte oracle. Never copy unknown payload bytes merely because they occur in a reference.

## 7. Format BCH is a finite search space

Format information is protected and has only a small legal set of codewords. When a few modules are missing, enumerate the legal format words and use Hamming distance rather than guessing ECC/mask.

The same principle applies to version information for versions that carry it.

## 8. Test all eight masks when necessary

There are only eight QR data masks. If mask information is questionable, branch over the eight possibilities and score them using:

```text
mode legality
count plausibility
known bits
RS consistency
re-encoding agreement
```

This is dramatically cheaper than blind payload brute force.

## 9. Traversal bugs masquerade as bad data

If bytes become nonsense early, inspect the module-coordinate generator before touching the RS solver. Common mistakes:

- reading rows instead of QR zig-zag order;
- forgetting the timing column;
- accidentally including format/version modules;
- reversing a column pair incorrectly;
- unmasking function modules.

A single coordinate error can shift all downstream codewords.

## 10. Measure damage after deinterleaving

Do not estimate recoverability from the percentage of the image covered. Map unknown modules to codeword positions and then to RS blocks.

What matters is the number and location of unknown symbols per block.

## 11. RS parity is a candidate fingerprint

For a candidate payload, regenerate data codewords and parity. Compare with every ECC byte that survived the damage.

A candidate can look perfect semantically yet be mathematically impossible.

Visible parity is often enough to kill bad candidates without regenerating the entire source image mentally or manually.

## 12. Use GF(256) linearity

For a small set of unknown bytes, RS parity equations are linear over GF(256). If candidate A differs from candidate B in only a few symbols, the induced parity difference is also predictable.

This enables delta-based pruning:

```text
baseline candidate
→ change one symbol
→ update parity delta
→ reject/keep immediately
```

## 13. Solve small erasure systems directly

When only a few symbol values are unknown and their positions are known, a direct linear-system approach may be simpler than implementing an entire general-purpose decoder. Still run a complete parity/syndrome verification after solving.

## 14. Separate error and erasure models

An erasure means:

> “I know this symbol position is unreliable.”

An error means:

> “I have a symbol value but its location may be wrong.”

Do not turn a known erasure into a guessed value and force the decoder to treat it as an unknown-location error.

## 15. Partial bytes are valuable

A byte such as:

```text
010?1???
```

has only 16 possibilities, not 256. Track the fixed-bit mask and delay expansion when later structure can prune it further.

## 16. Early structure is disproportionately valuable

The first codewords can contain mode, count, ECI, or segment headers. Recovering just a few early bits can establish a global interpretation for the rest of the symbol stream.

Therefore prioritize high-confidence modules that map to the beginning of the serialized data stream.

## 17. Segment boundaries matter

The same text can be represented using different QR segments and produce different bitstreams/matrices. Exact reconstruction therefore requires more than matching decoded text.

Preserve observed mode/segment structure when possible.

## 18. “One decoder succeeds” proves very little

A decoder proves that a candidate matrix is a valid QR. It does not prove that it is the original QR.

Use:

```text
candidate validity
+ source-module agreement
+ RS agreement
+ structural agreement
```

## 19. Zero mismatches on the trusted subset is powerful

When large areas are occluded, compare the regenerated QR only against modules classified as confidently visible. If every trusted module agrees, the missing area becomes constrained by the QR construction rather than by image guessing.

## 20. Cluster mismatch coordinates

If a candidate has mismatches, save their `(row, col)` coordinates.

Patterns can diagnose the problem:

- edge/boundary clusters → sampling or homography issue;
- one function-pattern region → function-map bug;
- periodic/stripe-like differences → traversal/mask issue;
- widespread differences → wrong payload/version/mask/segmentation.

Do not interpret mismatch count without spatial context.

## 21. Compare both format copies

A damaged copy can be repaired conceptually by the intact copy. If the two copies disagree, do not simply pick one; use BCH distance and the downstream QR structure to resolve the hypothesis.

## 22. Use capacity as a checksum

Once version, ECC, mode, and character count are hypothesized, verify that the segment fits exactly within the available data capacity after terminator and padding rules. Impossible capacities are cheap early rejections.

## 23. Padding is evidence too

A valid QR has constrained terminator/padding behavior after the payload. If a candidate creates illegal or inconsistent trailing bits, reject it even when the human-readable payload looks correct.

## 24. Do not assume byte encoding is UTF-8

Byte mode is a byte stream. Human-readable interpretation may depend on ECI or application-level encoding. Preserve raw bytes until the encoding has been established.

## 25. Preserve casing and punctuation

During recovery, do not normalize:

- URL case;
- slashes;
- percent escapes;
- whitespace;
- Unicode normalization;
- punctuation.

Two strings that look equivalent to a human can encode different bytes.

## 26. Search from constraints, not from characters

If a token has a known alphabet, fixed length, and several observed bits, enumerate only compatible bytes. Add parity and matrix constraints as soon as possible.

Prefer:

```text
finite constraints → enumerate survivors
```

over:

```text
all strings → decode everything → inspect manually
```

## 27. Use an uncertainty budget

At every stage record:

```text
known bits
unknown bits
known symbols
unknown symbols
known RS parity
remaining degrees of freedom
```

This makes it possible to tell the user whether the task is mathematically promising or fundamentally underdetermined.

## 28. Hypothesis branching should be narrow

Good branch dimensions are small finite sets:

```text
version: plausible candidates only
ECC: 4 values
mask: 8 values
format BCH candidates: finite legal set
segment mode: small set
```

Do not branch on arbitrary semantic strings until structural branches are exhausted.

## 29. Recovery can be staged

A good solver can emit intermediate results:

```text
geometry recovered
→ metadata recovered
→ codeword map recovered
→ RS block partially solved
→ payload header recovered
→ candidate payloads generated
→ exact reconstruction validated
```

This is useful for agent reasoning and for debugging false recoveries.

## 30. Independent implementation beats repeated same-tool decoding

Running the exact same decoder three times does not create three independent proofs. Prefer a different implementation for final validation when practical.

## 31. Exact re-encoding must control segmentation

A common validation failure is:

```text
recovered text
→ generic QR library
→ visually different but valid QR
```

That can be a perfectly valid QR and still fail source-matrix comparison. Reproduce mode/segment/ECI/version/ECC/mask parameters as closely as the evidence supports.

## 32. Search with the cheapest rejection first

A strong ordering is:

```text
fixed bits
→ mode/count legality
→ byte-level constraints
→ capacity/padding
→ parity fingerprint
→ matrix comparison
→ independent decode
```

Do not render PNGs or invoke expensive decoders for candidates that already fail a parity byte.

## 33. Never overfit to a vendor URL

A known vendor prefix can dramatically shrink the search space. But multiple vendors can share prefixes and token formats.

Treat vendor knowledge as a constraint layer, not a source of truth.

## 34. Use metadata to predict, then QR to prove

The right relationship is:

```text
metadata → hypothesis
QR structure → constraint
RS parity → mathematical filter
visible modules → image proof
independent decoder → sanity check
```

The wrong relationship is:

```text
metadata → answer
```

## 35. Deliberately search for a second solution

To test uniqueness, after finding candidate A ask:

> What is the nearest alternative candidate that still satisfies every observed module and parity constraint?

If one exists, uniqueness is false even if candidate A was found first.

## 36. Relax external assumptions one at a time

A candidate may depend on a printed serial, token alphabet, or vendor prefix. Disable each assumption independently and repeat the uniqueness test.

This reveals whether the QR itself proves the result or the metadata does.

## 37. Multi-image evidence should be coordinate-based

Do not combine images by visual intuition. Transform them into the same module coordinate system first. Then maintain per-source evidence.

A useful record is:

```text
module (r,c)
  image A: black, confidence .99
  image B: unknown
  image C: white, confidence .98
```

Conflicts can then be investigated rather than hidden by averaging.

## 38. Image quality can be asymmetric

One photo may have better geometry; another may have better visibility. Use each image for what it is good at instead of choosing one “best” source globally.

## 39. Preserve a forensic artifact bundle

For every recovery, save:

```text
original image(s)
rectified image
module grid visualization
tri-state matrix
format/version hypotheses
codeword map
RS block state
candidate list
reconstructed matrix
mismatch coordinates
decoder outputs
final report
```

This makes a recovery reproducible and auditable.

## 40. Public examples must be synthetic or redacted

Never publish real ticket numbers, session URLs, authentication tokens, private contact data, or payment secrets in fixtures simply because they made a successful recovery case.

Use generated identifiers while retaining the same structural pattern.

## 41. Know when to stop

A solver should explicitly stop when:

- geometry is irrecoverable;
- format/version hypotheses remain contradictory;
- too many RS symbols are erased in a critical block;
- the payload segment is underdetermined;
- multiple exact candidates remain.

A correct `NOT_RECOVERED` is a successful forensic result when the evidence does not support more.

## 42. The three-proof rule

For high-confidence real-world recovery, aim for three independent layers:

```text
1. mathematical: RS / QR structure
2. physical: visible-module agreement
3. independent: second decoder or implementation
```

A semantic guess belongs to none of these three.
