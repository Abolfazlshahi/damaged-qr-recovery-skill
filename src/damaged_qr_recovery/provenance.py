"""Evidence/provenance primitives."""
from dataclasses import dataclass
from enum import Enum


class Provenance(str, Enum):
    OBSERVED = "OBSERVED"
    RECOVERED_BY_RS = "RECOVERED_BY_RS"
    CONSTRAINED_BY_METADATA = "CONSTRAINED_BY_METADATA"
    INFERRED_UNVERIFIED = "INFERRED_UNVERIFIED"


@dataclass(frozen=True)
class Evidence:
    label: str
    provenance: Provenance
    detail: str = ""
