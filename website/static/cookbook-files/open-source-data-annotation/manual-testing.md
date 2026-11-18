# Manual workflow checks and Pass 2 handoff

Use new local state and fresh output names. These checks concern the published policy brief and supplied
teaching text. Preserve existing projects and state when testing a new batch.
Record the application version, platform, date, and actual observations.
Service/API execution evidence is recorded separately in `verification.md`.

## Label Studio

1. Follow recipe 1.1 in a clean Python 3.10 environment. Start Label Studio
   1.22.0, create an account, and enable legacy tokens in the organization
   settings if needed. Confirm the token is not written into downloaded files.
2. Obtain the Shona policy brief from its publisher, as in recipe 1.1. Place
   only policy_brief_on_shona_community_from_stateless_to_citizens.pdf in
   pdf-input. Run create_pdf_project.py with the configured media root and
   a fresh batch name. Confirm one task has 12 pages in source order.
3. Inspect the page images and navigate to PDF page 4. Draw Figure around
   Figure 1, including its title, axes, legend, and source line. Resize one
   boundary. Add a temporary box over prose and delete it.
4. On the same page, draw Table around Table 1, including its title, headings,
   cells, and source line. Change an intentionally wrong label to Table.
   Confirm one Figure and one Table, both on page index 3. The exercise covers
   only these two selected regions, not all targets in the publication.
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
   Confirm 14 records and no import errors. Check preserved source_id values
   m01–m14 and original document_id values D01–D06.
3. Apply the reused sample's broad data-source policy. Select Household
   Budget Survey 2021 in m01, HBS in m02, and the entire Household Budget
   Survey (HBS) 2021 phrase in m08. Include the specific report cited as a
   source in m04 and the descriptive reference The labour survey in m07.
   Deliberately select an overlong span, delete it, and select the correct
   words. Confirm m13 and m14 as reviewed without creating entities.
4. Save and confirm every record, reopen it, and check the highlighted words.
   Export native JSONL, extract the annotator's file, and run:

   python inspect_doccano.py entities entities-export.jsonl --source passages.jsonl

5. Verify the same 14 source IDs, unchanged strings, 12 intended spans, and
   two empty label lists. The original CSV reference spells row 7's mention
   with a lowercase t; preserve the sentence's capital T in the annotation.
6. For optional Unicode verification, create a separate project with the same
   settings and import unicode-passages.jsonl. Confirm two records, p06 and
   p07. They contain a composed accent and a leading emoji, combining accent,
   and newline. Select exactly Labour Force Survey in each, save, reopen,
   and export as unicode-export.jsonl. Run:

   python inspect_doccano.py entities unicode-export.jsonl --source unicode-passages.jsonl

7. Compare Python text[start:end] with browser highlights in both Unicode
   cases. If they differ, preserve the evidence and do not normalize or shift
   offsets by guesswork. Record that installation's offset limitation.

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
Verify every download and embedded script. Confirm that the cookbook appears
on the landing page and that its downloadable files are available in the
production build. The working draft retains the site's normal noindex status.

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
