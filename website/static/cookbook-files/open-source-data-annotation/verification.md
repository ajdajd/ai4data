# Pass 1 verification record

Checked on November 12, 2026. This record distinguishes service execution,
deterministic file checks, and browser actions. No model inference was run.

## Environments

The tool checks used isolated Python 3.10.19 environments and new temporary
SQLite databases. They did not modify existing annotation projects. The
repository's existing Python 3.13 environment ran the offline tests and
documentation checks. Docker access was unavailable, so container setup was
not tested.

Label Studio 1.22.0 installed and started. The standalone PDF command also
ran under Python 3.10 with PyMuPDF 1.28.2 and requests 2.32.5. Legacy token
authentication was enabled on the temporary organization. Its first startup
had already created that organization without legacy tokens, so the later
CLI flag alone did not update the existing token setting. Recipe 1.1 includes
the corresponding organization-settings check.

Doccano 1.8.4 installed with the supplied requirements-doccano.txt bounds.
An unconstrained installation failed because environs expected marshmallow 3,
doccano's parsers expected Pydantic 1, and an older dependency imported
pkg_resources. The NumPy 1 bound preserves pandas 1.5's binary compatibility.
The auto-labeling package was pinned because its newer release required a
Pydantic 2 API during application startup. No automatic labeling was used.
Database initialization and user creation completed, and the real task
worker handled imports and exports. The test web application ran through
the same Gunicorn WSGI entry point on a loopback-only port with one worker.

## Executed Label Studio checks

- The standalone command accepted a directory containing the supplied PDF.
- It rendered two PNGs, created one project, configured local storage, and
  imported one multipage task with source_file and page_count metadata.
- Both authenticated local-media requests returned HTTP 200 with image data.
- The configured Figure and Table results were submitted through the API,
  associated with page indices 0 and 1, and persisted in the task.
- An API update changed a rectangle, added a temporary result, and removed
  that result. The final native exporter returned one task with two regions.
- The exact documented Python 3.10 rendering dependencies also created a
  second fresh project successfully.

The downloadable labelstudio-export.json is the actual native export after
those operations. It is an API-entered service fixture, not evidence that a
person drew or reviewed the boxes in a browser. Its local image paths refer
to the temporary verification batch.

## Executed doccano checks

- Sequence-labeling and single-label classification projects were created.
- Imports used the actual file-upload API and task worker. Omitting the
  configured label field initially produced import warnings. Supplying the
  native empty list, label: [], produced error-free imports into fresh projects.
- Seven passages and six occupation responses retained their stable source
  identifiers in metadata and later in the flattened native export records.
- Eight entity spans and six category assignments were entered through the
  API. The negative passage was confirmed without an entity label.
- All records were confirmed through the service and exported with the
  confirmed-record filter. Each archive contained annotator.jsonl.
- Both native JSONL files passed inspect_doccano.py against the original text.
- The backend persisted offsets after a composed accent, a leading emoji,
  a decomposed accent, and a newline. Python slicing reconstructed the
  intended dataset names. Grapheme mode was disabled.
- Creating a replacement occupation category left exactly one category in
  single-label mode. The intended code was restored. A temporary entity
  selection was created and deleted, leaving the intended span intact.

The downloadable entities-export.jsonl and codes-export.jsonl are the actual
native exporter files, without postprocessing. The semantic labels are
teaching decisions entered through the API, not independently adjudicated
human reference labels. Internal IDs are installation-specific.

## Offline checks

The focused cookbook suite covers PDF rebuilding against shared facts,
document/page grouping, duplicate basenames, uppercase PDF extensions,
refusal to overwrite batches, unsafe batch paths, HTTP failure preservation,
source identity, changed text, Unicode code-point spans, invalid entity
bounds, single string-valued categories, and the captured native exports.

Executed repository checks passed:

- The focused annotation suite passed 19 tests. The existing cookbook CI test
  command, extended with that suite, passed 158 tests. Its three warnings came
  from the existing RDFLib JSON-LD parser deprecation.
- Strict validation passed for all 17 cookbooks with zero errors and warnings.
- Index/card synchronization reported zero changes or missing items. Glossary
  checks and shared example facts reported no differences or findings.
- Quoted-output checks passed across all 17 cookbooks, including both actual
  native-export validator examples in this guide.
- Black, Ruff lint, and Ruff format checks passed for the new Python files.
  The existing global cookbook/script lint and investment-view check passed.
- The Docusaurus build and subsequent CI-mode build succeeded. Seven new
  routes were registered. All seven built pages carried noindex metadata,
  and the hidden cookbook's downloads were removed from production output
  as configured. Existing hub/tool anchor warnings remain outside this change.
- The development preview returned HTTP 200 for all seven pages and all
  sixteen downloadable files. Each download matched the source bytes.
  Rendered chapters contained all nine recipe headers, and their internal
  page links resolved. The hidden cookbook was absent from landing-page links.

The quoted validator outputs in the chapters are executable against the
captured fixtures. They are not invented UI results. The shared facts and
all source inputs remain unchanged by the validators.

## Remaining manual verification

Browser-based drawing, resizing, deleting, selecting spans, keyboard behavior,
completion controls, reopening saved work, and exporting through the UI have
not been exercised in this environment. In particular, backend Unicode
persistence does not establish that browser selection uses the same offsets
for every string. Complete manual-testing.md on the installed release,
including the emoji and combining-accent cases, before claiming full browser
compatibility.

The installation was tested on this Linux environment only. Windows, macOS,
Docker, multiuser operation, long documents, and large batches remain untested.
The 10–20 PDF batch suggestion is a starting practice guideline, not measured
capacity. No screenshots are supplied because none were captured from the UI.

## Pass 2 boundary

DocLayout-YOLO and GLiNER2 integration, model downloads, model-assisted
classification, training, custom page-completion tracking, and downstream
COCO/evaluation converters were neither implemented nor executed.
