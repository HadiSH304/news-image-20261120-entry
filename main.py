#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Renders the Friday 20 November 2026 front page with compose.render()
and writes it to /output/entry.png. Deterministic: no network, no clock,
no randomness anywhere in the render path.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compose import render


def main() -> None:
    out = os.environ.get("OUTPUT_PATH", "/output/entry.png")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    render(out)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
