#!/usr/bin/env python3
import argparse

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a reconstructed QR with OpenCV.")
    parser.add_argument("image")
    args = parser.parse_args()
    image = cv2.imread(args.image)
    if image is None:
        raise SystemExit(f"Cannot read image: {args.image}")
    detector = cv2.QRCodeDetector()
    value, points, _ = detector.detectAndDecode(image)
    if value:
        print("status=PASS")
        print(f"payload={value}")
        print(f"points={points.reshape(-1, 2).tolist() if points is not None else None}")
    else:
        print("status=FAIL")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
