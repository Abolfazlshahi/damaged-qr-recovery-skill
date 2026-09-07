"""Serializable recovery result model."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RecoveryResult:
    status: str
    payload: str | bytes | None = None
    version: int | None = None
    error_correction: str | None = None
    mask: int | None = None
    observed_modules: int = 0
    unknown_modules: int = 0
    visible_mismatches: int | None = None
    independent_decode_ok: bool | None = None
    unique: bool = False
    notes: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def is_confirmed(self) -> bool:
        return self.status == "CONFIRMED" and self.unique
