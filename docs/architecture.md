# Architecture

The project is layered so agents can use the Skill without installing the Python package, while developers can extend deterministic primitives.

```text
Agent runtime
    │
    ├── SKILL.md (behavior contract)
    ├── references/ (technical knowledge)
    └── commands/ (task entry points)

Python toolkit
    ├── geometry.py
    ├── qr.py
    ├── rs.py
    ├── provenance.py
    └── models.py

Validation surface
    ├── scripts/
    ├── tests/
    └── benchmark/
```

The generic algorithm must not contain assumptions about a particular railway, payment provider, or ticket vendor. Vendor-specific constraints belong in adapters/examples.
