#!/usr/bin/env python3
"""Validate the files Cloudflare Pages publishes for amesvt.com."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_main = False
        self.title_parts: list[str] = []
        self._in_title = False
        self.canonical_href: str | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "main":
            self.has_main = True
        elif tag == "title":
            self._in_title = True
        elif tag == "link" and attributes.get("rel") == "canonical":
            self.canonical_href = attributes.get("href")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)


def read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def main() -> None:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    assert index.lstrip().lower().startswith("<!doctype html>"), "missing HTML doctype"

    parser = DocumentParser()
    parser.feed(index)
    parser.close()

    assert "amesvt.com" in "".join(parser.title_parts), "page title is missing"
    assert parser.has_main, "page needs a main landmark"
    assert parser.canonical_href == "https://amesvt.com/", "canonical URL changed"
    assert 'name="robots" content="noindex, nofollow"' in index
    assert "https://ames.consulting" in index
    assert (ROOT / "favicon.svg").is_file(), "favicon is missing"
    for hostname in (
        "home.amesvt.com",
        "abs.amesvt.com",
        "channels.amesvt.com",
        "plex.amesvt.com",
        "mcp.amesvt.com",
        "applecore.amesvt.com",
        "ynab.amesvt.com",
        "drafts.amesvt.com",
    ):
        assert hostname in index, f"missing utility link: {hostname}"

    server = read_json(ROOT / ".well-known/matrix/server")
    client = read_json(ROOT / ".well-known/matrix/client")
    assert server == {"m.server": "matrix.amesvt.com:443"}
    assert client == {
        "m.homeserver": {"base_url": "https://matrix.amesvt.com"}
    }

    headers = (ROOT / "_headers").read_text(encoding="utf-8")
    assert "X-Robots-Tag: noindex, nofollow" in headers
    assert "Access-Control-Allow-Origin: *" in headers
    assert not (ROOT / "CNAME").exists(), "GitHub Pages CNAME file remains"
    print("Validated the Cloudflare site and Matrix discovery files.")


if __name__ == "__main__":
    main()
