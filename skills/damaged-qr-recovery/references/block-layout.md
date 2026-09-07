# Reed–Solomon Block Layout Reference

QR codewords are interleaved from one or more Reed–Solomon blocks. The exact block layout depends on **version and ECC level**.

An implementation needs:

```text
version
ECC level
total codewords
number of blocks
data codewords per block
ECC codewords per block
short/long block distribution
interleaving order
```

## Correct workflow

```text
serialized QR codewords
        ↓
undo interleaving
        ↓
block 1 ... block N
        ↓
RS decode each block separately
        ↓
restore data codewords
```

Never run RS over the full interleaved stream unless the actual QR block table contains exactly one block.

## Long vs short blocks

Some QR configurations have blocks whose total lengths differ by one symbol. Data-codeword counts are distributed according to the specification's block grouping. Do not assume equal-sized blocks.

## Verification

After deinterleaving, verify that the sum of block lengths equals the QR's total codeword capacity for the detected version.
