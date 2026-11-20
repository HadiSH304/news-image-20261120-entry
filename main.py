#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the pre-rendered front-page image (image.png, next to this file)
to /output/entry.png. Deterministic: identical bytes on every run.
Standard library only; no network access. The grader's runtime is
standard-library-only (RULES.txt: "nothing is installed before it
runs"), so this entrypoint must not import Pillow or any other
third-party package; compose.py is kept in the repo as the build
script that produced image.png, but it is not run here.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "image.png")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("wrote %s" % dst)


if __name__ == "__main__":
    main()
