# `/validate`

A candidate reconstruction is valid only after:

- QR structure checks pass;
- version/ECC/mask are consistent;
- QR parity checks pass;
- every known source module matches;
- regenerated QR independently decodes;
- no alternative candidate survives the same evidence.

A generic decoder result alone is not confirmation.
