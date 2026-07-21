#!/usr/bin/env python3
"""Build the minimal static payload deployed to Cloudflare Pages."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()

    for filename in ("index.html", "_headers", "favicon.svg"):
        shutil.copy2(ROOT / filename, OUTPUT / filename)

    shutil.copytree(ROOT / ".well-known", OUTPUT / ".well-known")
    print("Built the Cloudflare Pages payload in _site/.")


if __name__ == "__main__":
    main()
