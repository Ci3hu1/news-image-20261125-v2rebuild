#!/usr/bin/env python3
"""NI25 v2 entrypoint: copy the bundled poster to the output path.

Writes exactly one file: entry.png (1024x1024, the 46-story poster).
Pure Python standard library, deterministic: same input, same output.
"""

import os
import shutil


def output_path():
    """Resolve the output file path, in priority order."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.png")
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return "output.png"


def validate(src):
    """Fail loudly instead of shipping a missing or empty poster."""
    if not os.path.isfile(src):
        raise FileNotFoundError("bundled entry.png is missing: %s" % src)
    if os.path.getsize(src) == 0:
        raise ValueError("bundled entry.png is empty")
    with open(src, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("bundled entry.png is not a PNG file")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    validate(src)
    dst = output_path()
    parent = os.path.dirname(os.path.abspath(dst))
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise ValueError("copied entry.png size mismatch")
    try:
        os.chmod(dst, 0o644)
    except OSError:
        pass


if __name__ == "__main__":
    main()
