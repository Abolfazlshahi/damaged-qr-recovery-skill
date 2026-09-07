# Benchmarks

Measure exact recovery rather than decoder success alone.

## Metrics

- exact payload recovery;
- confirmed recovery;
- false-confirmation rate;
- visible-module mismatch rate;
- erasure-solver success;
- runtime/memory;
- surviving-candidate count.

## Damage matrix

Generate synthetic fixtures across QR versions, all ECC levels, all eight masks, random erasures, rectangles, scratches, blur, perspective, clipping, mixed damage, misleading metadata, and ambiguous cases.

## Reporting rule

Every benchmark result must record the fixture seed, implementation commit, environment, damage model, QR parameters, validation criteria, and independent decoder used.
