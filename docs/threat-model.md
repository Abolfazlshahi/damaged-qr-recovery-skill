# Threat Model

The project receives hostile or malformed images and potentially sensitive payloads.

## Threats

- forged or misleading external metadata;
- OCR mistakes presented as ground truth;
- malicious URLs inside QR payloads;
- parser edge cases and malformed mode/ECI data;
- image-processing artifacts that convert uncertainty into false bits;
- accidental publication of ticket identifiers or secrets.

## Mitigations

- evidence provenance;
- tri-state module maps;
- exact QR structural validation;
- bounded candidate search;
- independent decoding;
- never execute recovered payloads;
- redact fixtures and logs.
