# Example sources and licensing

The PDF exercise uses a real institutional publication. The sentence sample and
occupation responses are fictional teaching materials and contain no real
respondent data. The text examples do not estimate the policy brief's statistics.

## Reused publication and teaching materials

Chapter 1 reuses *From Stateless to Citizens: The Journey of Shona in Kenya*,
the 12-page policy brief used in the Data Snapshot cookbook. Figure 1 and
Table 1 appear on PDF page 4. Readers obtain the PDF from its publication
page or attachment:

https://reliefweb.int/report/kenya/policy-brief-stateless-citizens-journey-shona-community-kenya

https://reliefweb.int/attachments/831aca28-6777-4cb9-9b84-8976c63061fb/Policy%20Brief%20on%20Shona%20community_From%20Stateless%20to%20Citizens.pdf

The full PDF is not redistributed with this cookbook. The publication retains
its source attribution and applicable terms; the repository's license does
not grant rights to the source publication. Verification used an existing
local copy, not a newly downloaded or altered publication.

Chapter 2 reuses all 14 sentences from the Monitoring of Data Use cookbook's
`labelled_sample.csv`:
https://github.com/worldbank/ai4data/blob/main/website/static/cookbook-files/monitoring-data-use/labelled_sample.csv

The doccano input keeps every sentence and original document identifier
unchanged. It adds source_id values m01–m14 in CSV row order and empty label
lists, omitting mention_text answers and notes. The source sample defines
12 mentions and two negative sentences. Its broad data-source policy includes
indicator series and a specific report cited as a source. The reference
phrase "the labour survey" in row 7 is lowercase in the CSV's mention_text,
while its sentence starts "The labour survey". Annotation offsets preserve
the sentence's original capital T.

The response texts and source IDs are selected from the existing fictional
AI4Data occupation-coding example. Its reference codes, model suggestions,
and confidence values are not included in the unlabeled import:
https://github.com/worldbank/ai4data/blob/main/website/static/cookbook-files/language-models-in-production/occupation_coding.csv

Original teaching assets and adapted World Bank code are distributed under
the repository's MIT License with the World Bank IGO rider, reproduced in
`LICENSE.txt`. The project-creation script adapts World Bank PDF annotation
utilities; their copyright notice is retained in the script and license.
Readers do not need a separate research repository.

## Occupation reference

The codebook uses these ISCO-08 titles: 2341, Primary School Teachers; 8322,
Car, Taxi and Van Drivers; 5211, Stall and Market Salespersons; and 7231,
Motor Vehicle Mechanics and Repairers. Teaching rules are short original
paraphrases of the official category scope, not a redistributed manual.
NEEDS_REVIEW is a local workflow label, not an ISCO code.

The titles, scope, and boundary examples were checked on November 12, 2026
against the ILO's linked structure-and-definition spreadsheets for major
groups 2, 5, 7, and 8:
https://ilostat.ilo.org/methods/concepts-and-definitions/classification-occupation/

That source includes fresh-food market vendors within 5211 and motorcycle
mechanics within 7231. The source also distinguishes nearby occupations,
including prepared-food vending and bicycle repair. The complete classification
and any reproduction of official reference material retain the ILO's terms.

## Native service exports

`labelstudio-export.json` is a user-provided native Label Studio export of
the Shona policy brief. It contains one 12-page task with Figure and Table
results on page index 3 and retains the publisher's original download filename
in source_file.

The doccano file `entities-export.jsonl` was captured on November 18, 2026.
It contains 14 records with 12 spans. The occupation file `codes-export.jsonl`
was captured on November 12, 2026. Teaching labels were entered through the
APIs and exported using doccano's native exporter. JSONL bytes were
extracted from the archives without rewriting the records. These examples
demonstrate the export representation; they do not certify annotation quality.

The exports retain native internal IDs and local media paths. Those IDs can
change in another installation, and the media paths refer to the
installation that produced each file. Inspecting the files needs no service.
Reopening them as a restored project would require matching media and project configuration;
project restoration is outside this tutorial. The source PDF and setup script
produce each reader's own images and project instead.

## Tool licenses

Label Studio Community declares Apache-2.0:
https://github.com/HumanSignal/label-studio/blob/develop/LICENSE

Doccano declares MIT:
https://github.com/doccano/doccano/blob/v1.8.4/LICENSE

PyMuPDF is available under AGPL or commercial terms:
https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright

These software licenses are separate from the teaching assets and source publication.
The cookbook does not redistribute annotation-tool packages, model weights,
third-party publication pages, or official classification manuals.
