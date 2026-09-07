# Reed–Solomon / GF(256) Reference

QR error correction uses Reed–Solomon coding over GF(256) with primitive polynomial:

```text
x^8 + x^4 + x^3 + x^2 + 1
```

## Symbol arithmetic

Elements are bytes. Multiplication and division are finite-field operations, not ordinary integer arithmetic.

For nonzero symbols:

```text
log(a*b) = log(a) + log(b) mod 255
log(a/b) = log(a) - log(b) mod 255
```

## Correction budget

For a block with `t` parity symbols, the classical bound is:

```text
2e + s <= t
```

where `e` is unknown-location erroneous symbols and `s` is known-position erasures. This bound is per RS block.

## Erasure-first recovery

1. identify unknown symbol positions;
2. build parity equations for the exact generator polynomial;
3. solve missing symbols;
4. re-evaluate every parity symbol;
5. only then consider error-location recovery.

## Candidate fingerprints

When only a few data symbols remain unknown, compute the RS parity for each candidate assignment. Matching observed parity symbols is a strong mathematical filter.
