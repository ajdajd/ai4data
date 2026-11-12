"""Inspect native doccano JSONL against the unchanged imported records.

Usage: python inspect_doccano.py entities exported.jsonl --source passages.jsonl
       python inspect_doccano.py classification exported.jsonl \
           --source responses.jsonl --codebook occupation-codebook.csv

Only the Python standard library is required. Exit status is 0 when the
structural checks pass and 1 otherwise. Files are read without modification.
Offsets use Python Unicode code points, with an exclusive end. The selected
doccano installation must pass the Unicode round-trip checks in manual-testing.md.

What this does not check: whether a human selected the correct entity or
occupation, whether a record was reviewed in the UI, or coding agreement.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def read_records(path: Path) -> dict[str, dict]:
    """Read native JSONL records keyed by their preserved source identifier.

    Parameters
    ----------
    path : pathlib.Path
        UTF-8 JSONL input or native doccano export.

    Returns
    -------
    dict[str, dict]
        Records indexed by unique, nonempty source_id strings.

    Raises
    ------
    ValueError
        If a record is malformed, duplicated, lacks text or identity, or is empty.
    TypeError
        If a JSON line contains a value other than an object.
    """
    records = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict):
            raise TypeError(f"Line {number}: expected a JSON object.")
        source_id = record.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f"Line {number}: missing string source_id.")
        if source_id in records:
            raise ValueError(f"Duplicate source_id: {source_id}")
        if not isinstance(record.get("text"), str) or not record["text"].strip():
            raise ValueError(f"{source_id}: text must be a nonempty string.")
        records[source_id] = record
    if not records:
        raise ValueError("No records were found.")
    return records


def inspect_entities(record: dict) -> int:
    """Validate native span triples and display their selected text.

    Parameters
    ----------
    record : dict
        Exported record containing text, source_id, and singular label fields.

    Returns
    -------
    int
        Number of structurally valid entity spans.

    Raises
    ------
    ValueError
        If labels, offsets, entity types, or nonoverlapping spans are invalid.
    TypeError
        If the native label field is not a list.
    """
    labels = record.get("label")
    if not isinstance(labels, list):
        raise TypeError(f"{record['source_id']}: expected native label list.")
    spans = []
    for span in labels:
        if not isinstance(span, list) or len(span) != 3:
            raise ValueError(f"{record['source_id']}: expected [start, end, label].")
        start, end, label = span
        if (
            type(start) is not int
            or type(end) is not int
            or not 0 <= start < end <= len(record["text"])
            or label != "DATASET"
        ):
            raise ValueError(f"{record['source_id']}: invalid DATASET span {span!r}.")
        spans.append((start, end))
    previous_end = -1
    for start, end in sorted(spans):
        if start < previous_end:
            raise ValueError(f"{record['source_id']}: duplicate or overlapping spans.")
        previous_end = end
        print(f"{record['source_id']} [{start}:{end}] {record['text'][start:end]!r}")
    return len(spans)


def main(argv: list[str] | None = None) -> int:
    """Validate a native entity or classification export without rewriting it.

    Parameters
    ----------
    argv : list[str] | None
        Command arguments, or process arguments when omitted.

    Returns
    -------
    int
        Zero when every source record is preserved and labels are valid, else one.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=["entities", "classification"])
    parser.add_argument("export", type=Path)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--codebook", type=Path)
    args = parser.parse_args(argv)
    try:
        source = read_records(args.source)
        exported = read_records(args.export)
        if source.keys() != exported.keys():
            raise ValueError("Export source identifiers differ from imported records.")
        allowed = set()
        if args.task == "classification":
            if args.codebook is None:
                raise ValueError("Classification requires --codebook.")
            with args.codebook.open(encoding="utf-8", newline="") as handle:
                allowed = {row["code"] for row in csv.DictReader(handle)}
            if not allowed:
                raise ValueError("The codebook contains no codes.")
        count = 0
        for source_id, record in exported.items():
            if record["text"] != source[source_id]["text"]:
                raise ValueError(
                    f"{source_id}: exported text differs from imported text."
                )
            if args.task == "entities":
                count += inspect_entities(record)
            else:
                labels = record.get("label")
                if (
                    not isinstance(labels, list)
                    or len(labels) != 1
                    or not isinstance(labels[0], str)
                    or labels[0] not in allowed
                ):
                    raise ValueError(
                        f"{source_id}: expected one string code from codebook."
                    )
                count += 1
                print(f"{source_id} {labels[0]}")
        unit = "span(s)" if args.task == "entities" else "code(s)"
        print(f"PASS: {len(exported)} unchanged record(s); {count} {unit}.")
        return 0
    except (OSError, ValueError, TypeError, KeyError, csv.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
