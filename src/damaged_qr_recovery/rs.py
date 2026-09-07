"""GF(256) primitives for QR Reed–Solomon implementations.

This module provides finite-field arithmetic only; block tables, generator
polynomials, and erasure solvers belong in higher-level layers so they can be
validated independently.
"""

PRIMITIVE = 0x11D


def _build_tables():
    exp = [0] * 512
    log = [0] * 256
    x = 1
    for i in range(255):
        exp[i] = x
        log[x] = i
        x <<= 1
        if x & 0x100:
            x ^= PRIMITIVE
    for i in range(255, 512):
        exp[i] = exp[i - 255]
    return exp, log


EXP, LOG = _build_tables()


def gf_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]


def gf_div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("GF(256) division by zero")
    if a == 0:
        return 0
    return EXP[(LOG[a] - LOG[b]) % 255]


def gf_pow(a: int, power: int) -> int:
    if power == 0:
        return 1
    if a == 0:
        return 0
    return EXP[(LOG[a] * power) % 255]


def gf_inverse(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError("GF(256) inverse of zero")
    return EXP[(255 - LOG[a]) % 255]
