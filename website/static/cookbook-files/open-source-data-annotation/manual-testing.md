# Manual workflow checks and Pass 2 handoff

Use new local state and fresh output names. These checks concern the supplied
fictional data. Preserve existing projects and state when testing a new batch.
Record the application version, platform, date, and actual observations.
Service/API execution evidence is recorded separately in `verification.md`.

## Label Studio

1. Follow recipe 1.1 in a clean Python 3.10 environment. Start Label Studio
   1.22.0, create an account, and enable legacy tokens in the organization
   settings if needed. Confirm the token is not written into downloaded files.
2. Place only EX-REP-2025-02.pdf in pdf-input. Run create_pdf_project.py with
   the configured media root and a fresh batch name. Confirm one task has two
   pages, with the chart first and the table second.
3. Open both images in the browser. Draw Figure around the chart, its title,
   unit, source, and note. Resize one boundary. Add a temporary box over prose
   and delete it. Confirm that only the intended Figure remains on page 1.
4. On page 2, draw Table around the title, unit, headings, cells, source, and
   note. Change an intentionally wrong label to Table. Confirm there is one
   Figure and one Table, associated with the correct images.
5. Submit the document task, reopen it, make a small correction, and save the
   update. Check the difference between an unfinished draft and submitted work.
6. Export native JSON. Inspect data.pages, meta.source_file, annotations,
   item_index, rectanglelabels, dimensions, and percentage coordinates. Confirm
   both regions persist. Do not expect coordinates to match the API fixture.
7. Try the existing batch name again and confirm the command refuses to
   overwrite it. For a multi-PDF check, use a fresh batch and an additional
   copy under a different input subdirectory. Confirm one task per PDF.

## Doccano entity spans

1. Follow recipe 2.1 independently. Install the supplied requirements, start
   the web application and task worker, and create a Sequence Labeling project.
   Disable overlapping spans, relations, and grapheme mode.
2. Create DATASET. Import passages.jsonl with text/label column names.
   Confirm seven records and no import errors. Check preserved source_id metadata.
3. Select the full dataset names and the two LFS acronyms in p02. Deliberately
   select an overlong span, delete it, and label the correct words. Confirm p05
   as inspected without creating an entity.
4. Inspect p06 with its composed accent. Inspect p07 with its leading emoji,
   decomposed combining accent, and newline. Select exactly Labour Force Survey
   in each, save, reopen, and check the highlighted words.
5. Export native JSONL, extract the annotator's file, and run:

   python inspect_doccano.py entities entities-export.jsonl --source passages.jsonl

6. Verify the same seven source IDs, unchanged strings, and the intended eight
   spans. Specifically compare Python text[start:end] with the browser highlights
   for p06 and p07. If they differ, preserve the evidence and do not normalize or
   shift offsets by guesswork. Record that installation's offset limitation.

## Doccano occupation coding

1. Follow recipe 3.1 independently, or use a new project in a working
   installation. Select Text Classification and enable single-label mode.
2. Define the exact codes from occupation-codebook.csv. Import responses.jsonl.
   Confirm six records and no import errors. Check retained source_id metadata.
3. Assign r01=2341, r02=8322, r03=5211, and r06=7231. Assign NEEDS_REVIEW to
   r07 and r14. Keep that workflow status separate from valid occupation codes.
4. Change an incorrect category to the correct one and reopen the record.
   Confirm only one category remains. Save/confirm completion for every record.
5. Export the native JSONL and run:

   python inspect_doccano.py classification codes-export.jsonl --source responses.jsonl --codebook occupation-codebook.csv

6. Confirm six unchanged responses, unique source IDs, quoted string codes,
   four occupation assignments, and two review assignments. Inspect a proposed
   source-table join by source_id; internal numeric IDs and row order are not keys.

## Review of the draft website

Review the three chapters independently. Confirm that each first recipe
contains its own setup and that none depends on a different task chapter.
Verify every download and embedded script. Hidden production builds remove
this cookbook's downloadable directory, so use a local development preview
or repository files for the complete review. Hidden pages should remain out
of landing cards, search, and the sitemap until editorial approval.

## Pass 2 extension points

The completed manual recipes remain the baseline. A later optional fourth
recipe can be added to each of the first two chapters without moving setup,
manual correction, or native export instructions.

- Bounding boxes: generate DocLayout-YOLO predictions for the same rendered
  images; map detector classes and normalized coordinates into native Label
  Studio predictions; demonstrate adding a miss, deleting a false positive,
  and correcting a box before export. Preserve document/page identity and
  model provenance. Do not require the full benchmarking pipeline.
- Entities: load the verified GLiNER2 base and extraction adapter; predict
  against exactly the imported text; map types to the agreed DATASET policy;
  import suggestions into a separate project; demonstrate correction and
  unchanged Unicode offsets. Preserve the original prediction record and
  distinguish model suggestions from reviewed labels.

Neither model integration is implemented or executed in Pass 1. Training,
model-assisted classification, custom completion tracking, and downstream
evaluation/COCO converters remain outside this handoff.
