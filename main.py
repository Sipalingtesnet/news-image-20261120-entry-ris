#!/usr/bin/env python3
"""Copy the repo-held entry.png to /output/entry.png (plain byte copy).

Python 3.13, stdlib only, no network. Deterministic: the output is
byte-identical to entry.png. Prints the output path, size in bytes,
and sha256. Exits nonzero with a clear message on any error.
"""
import hashlib
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"
DST = Path("/output/entry.png")


def main() -> int:
    try:
        if not SRC.is_file():
            print(f"error: source image not found: {SRC}", file=sys.stderr)
            return 1
        DST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SRC, DST)  # plain byte copy, no re-encoding
        data = DST.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"path: {DST}")
    print(f"size: {len(data)} bytes")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
