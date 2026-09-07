from __future__ import annotations

import argparse

from .qr import size_from_version, version_from_size


def main() -> int:
    p = argparse.ArgumentParser(prog="qr-recovery")
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("version", help="derive version from module count")
    v.add_argument("size", type=int)
    s = sub.add_parser("size", help="derive module count from version")
    s.add_argument("version", type=int)
    args = p.parse_args()
    if args.cmd == "version":
        print(version_from_size(args.size))
    else:
        print(size_from_version(args.version))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
