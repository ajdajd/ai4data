# Example sources and licensing

The report, research-style passages, and occupation responses are fictional
teaching materials for the National Statistics Office (example). They contain
no respondent data. The six responses do not estimate national indicators.

## Example facts and original materials

The organization, report EX-REP-2025-02, survey EX-LFS-2025-Q2, dataset names,
and unemployment values come from AI4Data's shared `facts.json`:
https://github.com/worldbank/ai4data/blob/main/website/static/cookbook-files/_example/facts.json

The two-page PDF and its chart/table are original assets built with
`build_example.py`. Rebuilding requires the shared facts file, not a model.
The passages are original fictional prose. The decomposed accent in passage
p07 and its leading emoji are intentional offset-check inputs.

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

`labelstudio-export.json`, `entities-export.jsonl`, and `codes-export.jsonl`
were produced by actual local annotation services on November 12, 2026.
The teaching labels were entered programmatically through the services' APIs
and exported using their native exporters. These files demonstrate persisted
representations, not human annotation quality or a completed browser test.

The exports retain native internal IDs and local media paths. Those IDs can
change in another installation, and the media paths refer to the temporary
verification service. Inspecting the files needs no service. Reopening them
as a restored project would require matching media and project configuration;
project restoration is outside this pass. The supplied PDF and setup script
produce each reader's own images and project instead.

## Tool licenses

Label Studio Community declares Apache-2.0:
https://github.com/HumanSignal/label-studio/blob/develop/LICENSE

Doccano declares MIT:
https://github.com/doccano/doccano/blob/v1.8.4/LICENSE

PyMuPDF is available under AGPL or commercial terms:
https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright

These software licenses are separate from the fictional example assets.
The cookbook does not redistribute annotation-tool packages, model weights,
third-party publication pages, or official classification manuals.
