"""Small QR facts used by higher-level recovery code."""


def version_from_size(size: int) -> int:
    version = (size - 17) // 4
    if 17 + 4 * version != size or not 1 <= version <= 40:
        raise ValueError(f"invalid QR module size: {size}")
    return version


def size_from_version(version: int) -> int:
    if not 1 <= version <= 40:
        raise ValueError("QR version must be 1..40")
    return 17 + 4 * version


def mask_bit(mask: int, row: int, col: int) -> int:
    if not 0 <= mask <= 7:
        raise ValueError("mask must be 0..7")
    if mask == 0:
        return int((row + col) % 2 == 0)
    if mask == 1:
        return int(row % 2 == 0)
    if mask == 2:
        return int(col % 3 == 0)
    if mask == 3:
        return int((row + col) % 3 == 0)
    if mask == 4:
        return int(((row // 2) + (col // 3)) % 2 == 0)
    if mask == 5:
        return int(((row * col) % 2 + (row * col) % 3) == 0)
    if mask == 6:
        return int((((row * col) % 2 + (row * col) % 3) % 2) == 0)
    return int((((row * col) % 3 + (row + col) % 2) % 2) == 0)
