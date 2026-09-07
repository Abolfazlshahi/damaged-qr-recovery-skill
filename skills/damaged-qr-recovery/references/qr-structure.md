# QR Structure Reference

## Matrix size

For version `v` (1..40):

```text
size = 17 + 4*v = 21 + 4*(v-1)
```

## Function modules

Exclude from payload extraction:

- finder patterns and separators;
- timing patterns;
- alignment patterns;
- format information;
- version information for versions 7+;
- the fixed dark module;
- reserved cells occupied by structural metadata.

## Format information

Format information encodes ECC level and mask pattern. Two copies exist. Use BCH/Hamming-distance validation rather than trusting raw pixels blindly.

## Masking

The mask is applied to data/ECC modules only. Unmask with XOR using the selected one of eight mask formulas. Structural modules are never unmasked as data.

## Data traversal

Data and ECC bits use the two-column vertical zig-zag path starting at the lower-right. Alternate direction for each column pair and skip the timing column.

## Version information

Versions 7–40 include duplicated version information. When both copies are readable, agreement is a useful structural check.
