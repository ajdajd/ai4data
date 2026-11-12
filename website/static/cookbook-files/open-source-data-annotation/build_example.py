"""Build the fictional two-page report from the shared cookbook facts.

Usage: python build_example.py --facts ../_example/facts.json \
           --output pdf-input/EX-REP-2025-02.pdf

Dependency beyond the shared cookbook requirements: PyMuPDF. Exit status is
0 on success and 1 on invalid input. Existing output files are not replaced.
The report and chart are original teaching materials. No model is used.

What this does not check: statistical validity of the invented observations,
survey estimation, or the quality of a reader's annotations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pymupdf


def main(argv: list[str] | None = None) -> int:
    """Write the example PDF using the canonical fictional facts.

    Parameters
    ----------
    argv : list[str] | None
        Command arguments, or process arguments when omitted.

    Returns
    -------
    int
        Zero when the PDF is created, or one when inputs or output are invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--facts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise FileExistsError("Output exists; choose a new PDF path.")
        facts = json.loads(args.facts.read_text(encoding="utf-8"))
        series = facts["series"]["LF_UNEMP_PCT"]
        values = series["values"]
        organization = facts["organization"]
        with pymupdf.open() as document:
            page = document.new_page(width=595, height=842)
            page.insert_text(
                (56, 55), facts["documents"]["EX-REP-2025-02"], fontsize=20
            )
            page.insert_text((56, 82), organization, fontsize=11)
            page.insert_text(
                (56, 104), "Fictional teaching report - EX-REP-2025-02", fontsize=10
            )
            page.insert_textbox(
                (56, 120, 535, 166),
                "These invented estimates belong to the shared cookbook case. "
                "The separate occupation-response examples do not produce "
                "these national indicators.",
                fontsize=11,
            )
            page.insert_text((72, 200), "Figure 1. Unemployment rate", fontsize=15)
            page.insert_text((72, 222), "Percent of labour force", fontsize=11)
            for index, period in enumerate(["2025-Q1", "2025-Q2"]):
                x = 162 + index * 175
                height = values[period] * 30
                page.draw_rect(
                    (x, 460 - height, x + 70, 460),
                    color=(0.15, 0.35, 0.60),
                    fill=(0.15, 0.35, 0.60),
                )
                page.insert_text(
                    (x + 21, 450 - height), str(values[period]), fontsize=13
                )
                page.insert_text((x, 483), period, fontsize=11)
            page.draw_line((120, 460), (465, 460), color=(0.2, 0.2, 0.2))
            page.insert_text(
                (72, 510), "Source: fictional Labour Force Survey.", fontsize=10
            )
            page.insert_text((72, 530), "Note: 2025-Q2 is provisional.", fontsize=10)
            page.insert_text(
                (56, 795), "Fictional example. PDF page 1 of 2.", fontsize=10
            )

            page = document.new_page(width=595, height=842)
            page.insert_text((56, 55), "Labour market report 2025 Q2", fontsize=20)
            page.insert_text((56, 82), organization, fontsize=11)
            page.insert_text((72, 180), "Table 1. Unemployment rate", fontsize=15)
            page.insert_text((72, 202), "Percent of labour force", fontsize=11)
            for row, (left, right) in enumerate(
                [
                    ("Period", "Rate (%)"),
                    ("2025-Q1", str(values["2025-Q1"])),
                    ("2025-Q2", str(values["2025-Q2"])),
                ]
            ):
                y = 225 + row * 40
                page.draw_rect((72, y, 520, y + 40), color=(0.3, 0.3, 0.3))
                page.draw_line((350, y), (350, y + 40), color=(0.3, 0.3, 0.3))
                page.insert_text((84, y + 25), left, fontsize=12)
                page.insert_text((365, y + 25), right, fontsize=12)
            page.insert_text(
                (72, 371), "Source: fictional Labour Force Survey.", fontsize=10
            )
            page.insert_text((72, 391), "Note: 2025-Q2 is provisional.", fontsize=10)
            page.insert_text((72, 450), "Research context", fontsize=14)
            page.insert_textbox(
                (72, 467, 520, 560),
                "We used the Labour Force Survey to describe employment. "
                "The Household Budget Survey 2021 provides a separate source "
                "on consumption. These sentences are fictional annotation inputs, "
                "not findings about actual surveys.",
                fontsize=11,
            )
            page.insert_text(
                (56, 795), "Fictional example. PDF page 2 of 2.", fontsize=10
            )
            document.set_metadata(
                {
                    "title": facts["documents"]["EX-REP-2025-02"],
                    "author": organization,
                    "subject": "Original fictional annotation example",
                }
            )
            args.output.parent.mkdir(parents=True, exist_ok=True)
            document.save(args.output, deflate=True)
        print("Created fictional report: 2 pages, 1 figure, 1 table.")
        return 0
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
