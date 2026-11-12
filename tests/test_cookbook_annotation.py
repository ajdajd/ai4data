"""Verify the annotation cookbook's files, safety boundaries, and native records."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pymupdf
import pytest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "website/static/cookbook-files/open-source-data-annotation"


def load_script(name: str) -> ModuleType:
    """Load a standalone asset without requiring package installation.

    Parameters
    ----------
    name : str
        Script filename without its suffix.

    Returns
    -------
    types.ModuleType
        Loaded script module.
    """
    spec = importlib.util.spec_from_file_location(name, ASSETS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pdf_matches_shared_facts(tmp_path: Path) -> None:
    """Rebuild the report and check its page order and fictional values.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary output directory.
    """
    output = tmp_path / "report.pdf"
    builder = load_script("build_example")
    facts_path = ROOT / "website/static/cookbook-files/_example/facts.json"
    assert builder.main(["--facts", str(facts_path), "--output", str(output)]) == 0
    facts = json.loads(facts_path.read_text())
    for path in [output, ASSETS / "EX-REP-2025-02.pdf"]:
        with pymupdf.open(path) as document:
            assert len(document) == 2
            assert "Figure 1." in document[0].get_text()
            assert "Table 1." in document[1].get_text()
            for value in facts["series"]["LF_UNEMP_PCT"]["values"].values():
                assert str(value) in document[1].get_text()
            assert "Fictional" in document[0].get_text()
    before = output.read_bytes()
    assert builder.main(["--facts", str(facts_path), "--output", str(output)]) == 1
    assert output.read_bytes() == before


def test_directory_tasks_preserve_documents_and_pages(tmp_path: Path) -> None:
    """Keep same-named PDFs in separate tasks and refuse an existing batch.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary input and media root.
    """
    source = tmp_path / "input"
    for directory in ["first", "second"]:
        folder = source / directory
        folder.mkdir(parents=True)
        (folder / "report.PDF").write_bytes(
            (ASSETS / "EX-REP-2025-02.pdf").read_bytes()
        )
    output = tmp_path / "media" / "batch"
    script = load_script("create_pdf_project")
    tasks = script.prepare_tasks(source, output, "batch")
    assert len(tasks) == 2
    assert {task["meta"]["source_file"] for task in tasks} == {
        "first/report.PDF",
        "second/report.PDF",
    }
    assert all(len(task["data"]["pages"]) == 2 for task in tasks)
    assert len({url for task in tasks for url in task["data"]["pages"]}) == 4
    image = pymupdf.Pixmap(output / "document-001/page-000.png")
    assert image.width > 2000
    before = (output / "tasks.json").read_bytes()
    with pytest.raises(FileExistsError):
        script.prepare_tasks(source, output, "batch")
    assert (output / "tasks.json").read_bytes() == before


@pytest.mark.parametrize("batch", ["../escape", "/absolute", "Bad name"])
def test_invalid_batch_cannot_escape(tmp_path: Path, batch: str) -> None:
    """Reject path-like batch names before rendering.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary data root.
    batch : str
        Unsafe batch name.
    """
    with pytest.raises(ValueError):
        load_script("create_pdf_project").prepare_tasks(
            tmp_path, tmp_path / batch, batch
        )


def test_project_creation_and_partial_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Exercise the API sequence and preserve a batch after a failed import.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary PDF input and media root.
    monkeypatch : pytest.MonkeyPatch
        Environment and HTTP replacements.
    """
    script = load_script("create_pdf_project")
    source = tmp_path / "pdfs"
    source.mkdir()
    (source / "report.pdf").write_bytes((ASSETS / "EX-REP-2025-02.pdf").read_bytes())
    session = MagicMock()
    session.__enter__.return_value = session
    response = MagicMock()
    response.json.return_value = {"id": 17}
    session.post.return_value = response
    monkeypatch.setattr(script.requests, "Session", lambda: session)
    monkeypatch.setenv("LABEL_STUDIO_API_KEY", "test-token")
    arguments = [
        "--input-dir",
        str(source),
        "--data-root",
        str(tmp_path / "media"),
        "--batch",
        "success",
        "--title",
        "Fictional project",
    ]
    assert script.main(arguments) == 0
    calls = session.post.call_args_list
    assert len(calls) == 3
    assert "valueList" in calls[0].kwargs["json"]["label_config"]
    assert calls[1].kwargs["json"]["project"] == 17
    assert len(calls[2].kwargs["json"][0]["data"]["pages"]) == 2
    session.post.side_effect = [
        response,
        response,
        script.requests.HTTPError("test failure"),
    ]
    arguments[arguments.index("success")] = "partial"
    assert script.main(arguments) == 1
    assert (tmp_path / "media/partial/tasks.json").is_file()
    monkeypatch.delenv("LABEL_STUDIO_API_KEY")
    arguments[arguments.index("partial")] = "missing-token"
    assert script.main(arguments) == 1
    assert not (tmp_path / "media/missing-token").exists()


def test_unicode_native_spans(tmp_path: Path) -> None:
    """Check code-point spans after an emoji, combining accent, and newline.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary synthetic native-format record files.
    """
    script = load_script("inspect_doccano")
    text = "📊 Cafe\u0301\nLabour Force Survey"
    start = text.index("Labour")
    record = {"source_id": "unicode", "text": text}
    source = tmp_path / "source.jsonl"
    source.write_text(json.dumps(record) + "\n", encoding="utf-8")
    record["label"] = [[start, len(text), "DATASET"]]
    output = tmp_path / "export.jsonl"
    output.write_text(json.dumps(record) + "\n", encoding="utf-8")
    before = output.read_bytes()
    assert script.main(["entities", str(output), "--source", str(source)]) == 0
    assert output.read_bytes() == before


@pytest.mark.parametrize(
    "label",
    [
        None,
        [[-1, 5, "DATASET"]],
        [[0, 999, "DATASET"]],
        [[True, 3, "DATASET"]],
        [[0, 2, "OTHER"]],
        [[0, 3, "DATASET"], [2, 4, "DATASET"]],
    ],
)
def test_entity_validation_rejects_invalid_labels(label: object) -> None:
    """Reject unsupported or ambiguous native entity records.

    Parameters
    ----------
    label : object
        Invalid native label field.
    """
    record = {"source_id": "p01", "text": "dataset", "label": label}
    with pytest.raises((ValueError, TypeError)):
        load_script("inspect_doccano").inspect_entities(record)


@pytest.mark.parametrize("label", [[], [2341], ["9999"], ["2341", "8322"]])
def test_classification_requires_one_string_code(tmp_path: Path, label: list) -> None:
    """Reject empty, numeric, unknown, or multiple categories.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary synthetic export directory.
    label : list
        Invalid native classification label list.
    """
    record = json.loads((ASSETS / "responses.jsonl").read_text().splitlines()[0])
    source = tmp_path / "source.jsonl"
    source.write_text(json.dumps(record) + "\n")
    record["label"] = label
    exported = tmp_path / "export.jsonl"
    exported.write_text(json.dumps(record) + "\n")
    assert (
        load_script("inspect_doccano").main(
            [
                "classification",
                str(exported),
                "--source",
                str(source),
                "--codebook",
                str(ASSETS / "occupation-codebook.csv"),
            ]
        )
        == 1
    )


def test_export_identity_and_text_are_immutable(tmp_path: Path) -> None:
    """Reject lost identity, duplicate records, and changed passage text.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Temporary synthetic exports.
    """
    script = load_script("inspect_doccano")
    record = {"source_id": "p01", "text": "Unchanged text", "label": []}
    source = tmp_path / "source.jsonl"
    source.write_text(json.dumps(record) + "\n")
    exported = tmp_path / "export.jsonl"
    for changed in [
        {**record, "source_id": "other"},
        {**record, "text": "Changed text"},
        {"text": record["text"], "label": []},
    ]:
        exported.write_text(json.dumps(changed) + "\n")
        assert script.main(["entities", str(exported), "--source", str(source)]) == 1
    exported.write_text((json.dumps(record) + "\n") * 2)
    assert script.main(["entities", str(exported), "--source", str(source)]) == 1


def test_captured_service_exports() -> None:
    """Inspect actual native exporter files without contacting either service."""
    script = load_script("inspect_doccano")
    assert (
        script.main(
            [
                "entities",
                str(ASSETS / "entities-export.jsonl"),
                "--source",
                str(ASSETS / "passages.jsonl"),
            ]
        )
        == 0
    )
    assert (
        script.main(
            [
                "classification",
                str(ASSETS / "codes-export.jsonl"),
                "--source",
                str(ASSETS / "responses.jsonl"),
                "--codebook",
                str(ASSETS / "occupation-codebook.csv"),
            ]
        )
        == 0
    )
    tasks = json.loads((ASSETS / "labelstudio-export.json").read_text())
    assert len(tasks) == 1
    assert tasks[0]["meta"]["source_file"] == "EX-REP-2025-02.pdf"
    assert len(tasks[0]["data"]["pages"]) == 2
    annotations = tasks[0]["annotations"]
    assert len(annotations) == 1 and not annotations[0]["was_cancelled"]
    regions = annotations[0]["result"]
    assert [(r["item_index"], r["value"]["rectanglelabels"]) for r in regions] == [
        (0, ["Figure"]),
        (1, ["Table"]),
    ]
