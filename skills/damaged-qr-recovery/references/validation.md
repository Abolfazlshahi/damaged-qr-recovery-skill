# Validation Contract

A recovery is a proof-producing workflow.

## Minimum checks

- [ ] version and matrix dimensions agree;
- [ ] format information is valid or uncertainty is preserved;
- [ ] ECC and mask are consistent;
- [ ] function modules are excluded;
- [ ] exact RS block structure is used;
- [ ] recovered codewords satisfy parity;
- [ ] candidate payload re-encodes cleanly;
- [ ] every trusted known source module matches;
- [ ] independent decoder succeeds;
- [ ] no competing candidate survives.

## Strongest final test

Given candidate payload `P`:

```text
P
 ↓
exact QR encoder
 ↓
reconstructed module matrix M
 ↓
compare M against every known source module
```

For a confirmed candidate, trusted known-module mismatch count should be zero.

## Failure semantics

A decoder failure does not prove impossibility. A semantic match does not prove recovery. A partial RS solution is valuable but should be reported as `PARTIAL` until end-to-end validation succeeds.
