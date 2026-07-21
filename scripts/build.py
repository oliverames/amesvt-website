#!/usr/bin/env python3
"""Build the minimal static payload deployed to Cloudflare Pages."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"
R2_FAVICON_URL = "https://assets.amesvt.com/amesvt/favicon.svg"


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    index = index.replace('href="/favicon.svg"', f'href="{R2_FAVICON_URL}"')
    (OUTPUT / "index.html").write_text(index, encoding="utf-8")

    for filename in ("_headers",):
        shutil.copy2(ROOT / filename, OUTPUT / filename)

    shutil.copytree(ROOT / ".well-known", OUTPUT / ".well-known")
    assert R2_FAVICON_URL in (OUTPUT / "index.html").read_text(encoding="utf-8")
    assert not (OUTPUT / "favicon.svg").exists()
    print("Built the Cloudflare Pages payload in _site/.")


if __name__ == "__main__":
    main()
