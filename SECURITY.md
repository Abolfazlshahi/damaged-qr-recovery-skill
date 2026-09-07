# Security Policy

QR payloads can contain tickets, payment information, access tokens, URLs with bearer secrets, or other personal data.

## Safe handling

- Prefer local processing over uploading source images to third-party services.
- Treat every recovered payload as untrusted input until parsed and validated.
- Never execute recovered URLs, commands, scripts, or embedded data automatically.
- Redact personal identifiers and live credentials from public issue reports and fixtures.
- Keep private ticket/payment examples outside the public repository.

## Reporting

For security bugs, use GitHub's private security-reporting flow when available. Never publish a live token or credential in a public issue.

## Scope

This project is a recovery methodology and validation toolkit. It does not bypass authentication, decrypt protected QR payloads, or guarantee recovery when mathematical evidence is insufficient.
