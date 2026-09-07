# `/recover`

Run the full damaged-QR recovery pipeline:

1. preserve/inspect source;
2. locate and rectify;
3. establish version/ECC/mask;
4. build a tri-state module matrix;
5. exclude function modules;
6. unmask and traverse codewords;
7. deinterleave correct RS blocks;
8. solve erasures, then bounded errors;
9. apply explicit external constraints;
10. re-encode each survivor;
11. compare all known modules;
12. independently decode;
13. check uniqueness;
14. report status and provenance.
