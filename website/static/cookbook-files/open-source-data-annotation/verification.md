# Annotation workflow verification record

## Input reuse checks — November 18, 2026

The current PDF exercise uses the published Shona policy brief from the
Data Snapshot cookbook. The main entity exercise reuses all 14 sentences
from the Monitoring of Data Use cookbook. The original two Unicode cases
are separate optional inputs. The occupation exercise is unchanged.
No model weights were downloaded and no inference was run.

The PDF check used an existing local copy of the 12-page publication at
300 DPI. Its text and rendered PDF page 4 were inspected to locate Figure 1
and Table 1. The publisher links identify the source, but automated retrieval
returned an access error during this check. The full PDF is not bundled or
redistributed with this cookbook.

## Environments and installation

The API checks used isolated Python 3.10.19 environments, new temporary
SQLite databases, and loopback-only web applications. Existing annotation
projects were not modified. Label Studio 1.22.0 used PyMuPDF 1.28.2 and
requests 2.32.5. Legacy-token authentication was enabled on its temporary
organization. The repository's Python 3.13 environment ran offline checks.

Doccano 1.8.4 used the supplied requirements-doccano.txt bounds. Its published
package metadata requires Pydantic 2, conflicting with the Pydantic 1 pin
used by the tested import/export environment. A plain resolver install of that file
fails. The recipes therefore use uv with the same file as an explicit
override, which reproduced the working environment. Marshmallow 3,
NumPy 1, setuptools 80.9.0, and auto-labeling-pipeline 0.1.21 remain pinned
for the compatibility reasons described in the requirements file. No
automatic labeling was used. A real task worker handled imports and exports;
the web application used Gunicorn with one worker on a loopback-only port.

## Executed Label Studio checks

- The unchanged standalone command accepted a directory containing the full
  Shona PDF and created one task with 12 ordered page images.
- A separate offline rendering check also produced one task with 12 pages.
- All 12 authenticated local-media requests returned HTTP 200 and image data.
- Two rectangles were entered through the API for Figure 1 and Table 1 on
  PDF page 4, both with item_index 3. An API update changed and then restored
  the figure boundary.
- The native exporter returned one 12-page task with the two saved regions.
  Its response bytes are labelstudio-export.json. No detector predictions
  or model-generated labels were used.

The standalone command printed the following actual output in the temporary
verification installation. Project IDs, absolute paths, and ports vary by
installation; the chapter's command uses port 8080 and batch shona.

    Created project 1: 1 PDF task(s).
    Rendered 12 page(s).
    Tasks: /tmp/annotation-reuse-pdf-check/media/verified-shona/tasks.json
    Open http://127.0.0.1:18081/projects/1/data

The two page-4 rectangles demonstrate the native representation. They are
not a complete annotation of all 12 source pages, independently adjudicated
ground truth, or evidence of browser drawing.

## Executed doccano checks

- A fresh sequence-labeling project imported the 14-sentence JSONL through
  the file-upload API and real task worker with no import errors.
- Every sentence and D01–D06 document identifier remained unchanged; source_id
  values m01–m14 identify CSV rows in source order.
- Twelve spans were entered through the API using the reused CSV reference
  phrases. The capital T in m07's original sentence was preserved even
  though the CSV reference phrase begins with a lowercase t.
- An overlong selection was created and corrected through the API. All 14
  records, including both negatives, were confirmed through the service.
- The confirmed-record native exporter produced entities-export.jsonl with
  14 records and 12 spans.
- A separate fresh project imported unicode-passages.jsonl with overlapping
  entities, relations, and grapheme mode disabled. Both records were
  confirmed and exported as unicode-export.jsonl with two spans. Backend
  persistence retained composed and combining accents, an emoji, and a newline.
- Both JSONL fixture files were extracted from the real exporter archives
  without rewriting their records. inspect_doccano.py validates them against
  their corresponding unchanged inputs.

The labels are teaching/reference decisions entered through the API, not
independently reviewed human annotations. Correct offsets do not establish
semantic correctness or browser compatibility.

## Offline and website checks

- The focused annotation suite passed 19 tests. The complete cookbook CI
  test command passed 158 tests; its three warnings were the existing RDFLib
  JSON-LD parser deprecations.
- The tests compare all 14 imported sentences, source IDs, and document IDs
  with the unchanged Data Use CSV and check native spans against its reference
  phrases. The optional Unicode and unchanged classification fixtures pass
  the same source-preservation checks.
- PDF setup safety tests create a minimal two-page PDF in temporary storage,
  so automated tests need no publisher download. The real 12-page rendering
  and API checks are recorded separately above.
- Strict validation passed for all 17 cookbooks with zero errors or warnings.
  Index/card synchronization, shared example facts, glossary drift, and
  quoted-output checks passed. The glossary generator remains unchanged;
  only this cookbook's generated page changed.
- Black, Ruff lint/format, and git diff --check passed. The website build
  succeeded with the existing hub/tools anchor warnings.

## Earlier verification and unchanged occupation exercise

The November 12, 2026 run used an original two-page fictional PDF and seven
constructed entity passages. Those main inputs and their native fixtures
have been replaced. The two Unicode input cases are retained separately.
Historical two-page counts and page indices do not describe the Shona task.

The occupation input, codebook, and codes-export.jsonl are unchanged from
that run. The native classification exporter had preserved six confirmed
records, four official-code assignments, and two NEEDS_REVIEW assignments.
Those labels were API-entered teaching decisions, and the current offline
validator still checks them against their original inputs. Classification
browser interactions have not been tested.

## Remaining manual verification

Complete manual-testing.md for browser drawing, resizing, deleting,
selecting spans, completion controls, reopening saved work, and UI exports.
Backend persistence does not establish that browser Unicode selection uses
the same offsets for every string. Compare the emoji and combining-accent
cases directly before claiming browser compatibility.

The service rerun was on Linux only. Windows, macOS, Docker, multiuser use,
long documents beyond this publication, and large batches remain untested.
The 10–20 PDF batch suggestion is a starting guideline, not measured capacity.
No browser screenshots or model-assisted workflows are supplied.
