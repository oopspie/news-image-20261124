#!/usr/bin/env python3
"""Entry point for news-image-20261124.

Copies the pre-drawn front page (entry.png) to the output directory
the grader provides, honouring MAKEFUN_OUTPUT_DIR like the kit starter.
Standard library only, no network, deterministic: the bytes written are
always the bytes of entry.png next to this file.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    # plain copy: the file is already the finished front page, so the
    # output is byte-identical on every run by construction
    shutil.copyfile(src, dst)
    # sanity check the copy is whole: size must match the source
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
