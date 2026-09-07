#!/usr/bin/env python3
import argparse

import cv2
import numpy as np


def load_matrix(path: str, size: int) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise SystemExit(f"Cannot read image: {path}")
    image = cv2.resize(image, (size, size), interpolation=cv2.INTER_NEAREST)
    return image < 128


def main() -> None:
    parser = argparse.ArgumentParser(description="Coarse module-wise image comparison helper.")
    parser.add_argument("observed")
    parser.add_argument("reconstructed")
    parser.add_argument("--size", type=int, default=33)
    args = parser.parse_args()
    a = load_matrix(args.observed, args.size)
    b = load_matrix(args.reconstructed, args.size)
    mismatches = int(np.count_nonzero(a != b))
    total = args.size * args.size
    print(f"size={args.size}x{args.size}")
    print(f"mismatches={mismatches}")
    print(f"match_rate={(1 - mismatches / total):.6f}")


if __name__ == "__main__":
    main()
