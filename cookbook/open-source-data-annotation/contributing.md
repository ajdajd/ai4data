---
id: contributing
title: Contributing
sidebar_position: 92
description: This page explains how to improve the annotation recipes with reproducible inputs, native outputs, and clearly bounded verification evidence.
---

# Contributing

Corrections can be proposed through [GitHub issues](https://github.com/worldbank/ai4data/issues)
or a pull request. The [authoring guide](/cookbook/authoring/) defines the
structure and writing rules. A proposal should state the tool version,
input, action, output, and evidence that the procedure works.

## Criteria for a recipe

- The recipe answers a practical labeling question and produces a checkable native output.
- The chapter remains understandable independently, with setup before annotation instructions.
- The explanation introduces fields and unfamiliar terms before the procedure uses them.
- A worked example names concrete input, action, output, and verification limits.
- Code preserves the chapter's documented source text and identifiers, has an offline test, and states additional dependencies.
- Captured service behavior is distinguished from browser actions, illustrative arithmetic, and unexecuted proposals.

This cookbook uses three task-specific examples: a real policy brief,
fictional dataset-mention passages, and fictional occupation responses.
Contributions should retain their source and
licensing notes and keep each chapter independently usable.

## Recipe template

```markdown
<Recipe title="N.M Produce the named annotation result" level="Foundational" skills="Data curator" time="An indicative duration">

**Result:** The organization has a concrete output that a reader can inspect.

One or two paragraphs explain the artifact, its fields, and its purpose.

1. Complete the first action and explain why it matters.
2. Apply the task-specific labeling rules.
3. Check the resulting native output.

**Worked example.** The running example supplies the input, action, output,
and evidence for this procedure.

**What this does not do.** The example states its practical limits.

</Recipe>
```

## Verification evidence

Describe the service and browser checks performed for a contribution.
A screenshot must come from the stated application and example;
an expected export must not be presented as an observed export.

## Glossary scope

The qualified terms **Data annotation**, **Annotation label**,
**Image bounding box**, and **Format-conversion adapter** describe the meanings
used by the recipes. Definitions live in `cookbook/_shared/glossary.md`.
Run `python scripts/docs/build_glossaries.py` after updating the cookbook;
do not edit the generated glossary by hand or redefine an existing shared
term for this cookbook.

The generator uses substring matching without distinguishing meanings.
It can include unrelated entries or definitions that do not apply to data
annotation, including Annotation, Adapter, Label, and Bounding box. The
qualified terms above explain the intended meanings. Correcting glossary
selection requires a separate change to the shared documentation tooling.
