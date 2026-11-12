"""Create a multipage Label Studio project from a directory of PDFs.

Usage: python create_pdf_project.py --input-dir pdf-input --data-root ls-media
       --batch lfs-q2 --title "Labour market report"

Dependencies beyond the shared cookbook requirements: PyMuPDF and requests.
Set LABEL_STUDIO_API_KEY to a legacy token. The server must serve data-root
as its LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT. Exit status is 0 on success
and 1 on invalid input or an unsuccessful service request. Existing batches
are never overwritten. A failed service operation can leave a partial project;
the error identifies the project when one has been created.

What this does not check: annotation quality, page completion, server backups,
or downstream annotation schemas. No model is loaded.

Adapted from World Bank PDF annotation utilities, copyright 2024 The World Bank
Group. Distributed under the MIT License with the World Bank IGO rider;
see LICENSE.txt in this download directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlsplit

import pymupdf
import requests


def prepare_tasks(input_dir: Path, output_dir: Path, batch: str) -> list[dict]:
    """Render PDF pages and group each document into one native task.

    Parameters
    ----------
    input_dir : pathlib.Path
        Directory searched recursively for PDFs, including uppercase extensions.
    output_dir : pathlib.Path
        New batch directory beneath the server's local-file document root.
    batch : str
        Name of that batch directory, used in server-relative image URLs.

    Returns
    -------
    list[dict]
        Native Label Studio tasks with ordered pages and source metadata.

    Raises
    ------
    ValueError
        If no PDFs exist, a PDF is encrypted or empty, or batch is invalid.
    FileExistsError
        If the output directory already exists.
    """
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", batch):
        raise ValueError("Batch must contain lowercase letters, digits, - or _.")
    if not input_dir.is_dir():
        raise ValueError(f"PDF input directory does not exist: {input_dir}")
    if output_dir.exists():
        raise FileExistsError(f"Batch already exists; choose a new name: {output_dir}")
    pdfs = sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )
    if not pdfs:
        raise ValueError("The input directory contains no PDF files.")
    for path in pdfs:
        with pymupdf.open(path) as document:
            if document.needs_pass or document.page_count == 0:
                raise ValueError(f"PDF must be readable without a password: {path}")

    output_dir.mkdir(parents=True, exist_ok=False)
    tasks = []
    for number, path in enumerate(pdfs, 1):
        image_dir = output_dir / f"document-{number:03d}"
        image_dir.mkdir()
        pages = []
        with pymupdf.open(path) as document:
            for page_index, page in enumerate(document):
                image_path = image_dir / f"page-{page_index:03d}.png"
                page.get_pixmap(dpi=300, alpha=False).save(image_path)
                relative = f"{batch}/{image_dir.name}/{image_path.name}"
                pages.append(f"/data/local-files/?d={quote(relative, safe='/')}")
        tasks.append(
            {
                "data": {"pages": pages},
                "meta": {
                    "source_file": path.relative_to(input_dir).as_posix(),
                    "page_count": len(pages),
                },
            }
        )
    (output_dir / "tasks.json").write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return tasks


def main(argv: list[str] | None = None) -> int:
    """Prepare pages, create a project, and import its native tasks.

    Parameters
    ----------
    argv : list[str] | None
        Command arguments, or process arguments when omitted.

    Returns
    -------
    int
        Zero on success, or one when preparation or a service operation fails.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--url", default="http://127.0.0.1:8080")
    args = parser.parse_args(argv)
    project_id = None
    try:
        token = os.environ.get("LABEL_STUDIO_API_KEY", "").strip()
        if not token:
            raise ValueError("Set LABEL_STUDIO_API_KEY to a Label Studio legacy token.")
        url = urlsplit(args.url)
        if (
            url.scheme not in {"http", "https"}
            or not url.netloc
            or url.username
            or url.password
            or url.query
            or url.fragment
        ):
            raise ValueError(
                "URL must be an HTTP(S) server address without credentials."
            )
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", args.batch):
            raise ValueError("Batch must contain lowercase letters, digits, - or _.")
        config = (
            Path(__file__).with_name("multipage-labels.xml").read_text(encoding="utf-8")
        )
        base_url = args.url.rstrip("/")
        with requests.Session() as session:
            session.headers["Authorization"] = f"Token {token}"
            response = session.get(f"{base_url}/api/projects/", timeout=(5, 30))
            response.raise_for_status()
            root = args.data_root.resolve()
            output = root / args.batch
            tasks = prepare_tasks(args.input_dir.resolve(), output, args.batch)
            response = session.post(
                f"{base_url}/api/projects/",
                json={"title": args.title, "label_config": config},
                timeout=(5, 60),
            )
            response.raise_for_status()
            project_id = response.json()["id"]
            response = session.post(
                f"{base_url}/api/storages/localfiles/",
                json={
                    "project": project_id,
                    "path": str(output),
                    "title": args.batch,
                    "use_blob_urls": True,
                },
                timeout=(5, 60),
            )
            response.raise_for_status()
            response = session.post(
                f"{base_url}/api/projects/{project_id}/import",
                json=tasks,
                timeout=(5, 60),
            )
            response.raise_for_status()
        print(f"Created project {project_id}: {len(tasks)} PDF task(s).")
        print(f"Rendered {sum(len(task['data']['pages']) for task in tasks)} page(s).")
        print(f"Tasks: {output / 'tasks.json'}")
        print(f"Open {base_url}/projects/{project_id}/data")
        return 0
    except (
        OSError,
        ValueError,
        KeyError,
        RuntimeError,
        requests.RequestException,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        if project_id is not None:
            print(
                f"Project {project_id} may be incomplete. Inspect it before retrying; "
                "no project or existing files were deleted.",
                file=sys.stderr,
            )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
