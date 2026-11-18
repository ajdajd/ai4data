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
- Code uses the shared fictional facts, has an offline test, and states additional dependencies.
- Captured service behavior is distinguished from browser actions, illustrative arithmetic, and unexecuted proposals.

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
The manual checklist describes browser steps for reviewing the workflows.
A screenshot must come from the stated application and example;
an expected export must not be presented as an observed export.

## Glossary scope

The qualified terms **Data annotation**, **Annotation label**,
**Image bounding box**, and **Format-conversion adapter** describe the meanings
used by the recipes. Add definitions to `cookbook/_shared/glossary.md` and run
the existing generator; do not edit this cookbook's generated glossary by hand.
The generator selects terms by substring matching without disambiguating their
senses, so unrelated entries and other meanings can also appear. This known
limitation remains; the generator and existing definitions are unchanged.

## Pass 2 scope

DocLayout-YOLO suggestions can extend the completed multipage project recipe.
GLiNER2 suggestions can extend the completed entity export recipe. Both
extensions must preserve the manual path, identify model provenance, and
demonstrate correction before a reviewed export. Neither is implemented in
this pass; model-assisted classification is outside the planned extension.
