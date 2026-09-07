"""Geometry helpers for QR module grids."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GridSpec:
    version: int
    size: int

    @classmethod
    def from_version(cls, version: int) -> "GridSpec":
        if not 1 <= version <= 40:
            raise ValueError("QR version must be between 1 and 40")
        return cls(version, 17 + 4 * version)


def module_centers(size: int, width: float, height: float) -> Iterable[tuple[float, float]]:
    if size <= 0:
        raise ValueError("size must be positive")
    sx, sy = width / size, height / size
    for row in range(size):
        for col in range(size):
            yield ((col + 0.5) * sx, (row + 0.5) * sy)
