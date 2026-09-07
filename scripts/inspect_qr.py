#!/usr/bin/env python3
import argparse

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a QR image using OpenCV.")
    parser.add_argument("image")
    args = parser.parse_args()
    image = cv2.imread(args.image)
    if image is None:
        raise SystemExit(f"Cannot read image: {args.image}")
    detector = cv2.QRCodeDetector()
    value, points, _ = detector.detectAndDecode(image)
    print(f"decoded={value!r}")
    print(f"detected={points is not None}")
    if points is not None:
        print(f"points={points.reshape(-1, 2).tolist()}")


if __name__ == "__main__":
    main()
