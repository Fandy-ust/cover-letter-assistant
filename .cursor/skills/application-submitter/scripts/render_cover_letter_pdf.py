#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the active cover letter Markdown file to a PDF using WeasyPrint."
    )
    parser.add_argument(
        "--src",
        default="active_application/final_draft.md",
        help="Source Markdown file.",
    )
    parser.add_argument(
        "--css",
        default="memory/cover_letter.css",
        help="CSS file used for PDF styling.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output PDF path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    src = Path(args.src)
    css_path = Path(args.css)
    out = Path(args.out)

    if not src.exists():
        raise FileNotFoundError(f"Source Markdown file not found: {src}")
    if not css_path.exists():
        raise FileNotFoundError(f"CSS file not found: {css_path}")

    try:
        import markdown
        from weasyprint import CSS, HTML
    except ImportError as exc:
        missing = exc.name or "dependency"
        raise RuntimeError(
            f"Missing Python dependency: {missing}. Install requirements first."
        ) from exc

    out.parent.mkdir(parents=True, exist_ok=True)

    md_text = src.read_text(encoding="utf-8")
    html_body = markdown.markdown(md_text, extensions=["nl2br"])

    html = f"""
    <html>
      <body>
        {html_body}
      </body>
    </html>
    """

    HTML(string=html, base_url=".").write_pdf(
        out,
        stylesheets=[CSS(filename=str(css_path))],
    )
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
