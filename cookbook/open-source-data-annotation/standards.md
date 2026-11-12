---
id: standards
title: Standards and representations used in this guide
sidebar_position: 90
description: This page distinguishes published standards, statistical classifications, and tool-native annotation representations used by the recipes.
---

# Standards and representations used in this guide

Native application formats are documented representations with application-specific
contracts. This guide makes no claim that every listed format is
an adopted World Bank institutional standard.

## Data interchange

| Standard or representation | Use | World Bank use | In this guide |
|---|---|---|---|
| [JSON, RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) | Structured records contain named fields and lists. | AI4Data publishes JSON data and schemas. | Chapter 1 explains native task and rectangle records. |
| [JSON Lines](https://jsonlines.org/) | UTF-8 text stores one JSON value per line. This is a format convention. | AI4Data cookbook examples use JSONL records. | Chapters 2 and 3 preserve native text and labels. |
| [Unicode](https://www.unicode.org/standard/standard.html) | Character representation distinguishes code points from encoded bytes and displayed graphemes. | This guide makes no institutional adoption claim. | Chapter 2 checks exact text and documents the selected offset convention. |

## Statistical classification

| Standard | Use | World Bank use | In this guide |
|---|---|---|---|
| [ISCO-08](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-occupation/) | Occupation unit groups categorize work by tasks and duties. | The AI4Data statistical-coding cookbook uses occupation codes. | Chapter 3 uses four unit groups; NEEDS_REVIEW is a separate workflow status. |

## Annotation representations

| Representation | Use | World Bank use | In this guide |
|---|---|---|---|
| [Label Studio JSON](https://labelstud.io/guide/export) | Native task exports retain images, annotations, labels, and percentage rectangles. | The Data Snapshot dataset was annotated with Label Studio. | Chapter 1 retains this primary output without conversion. |
| [doccano 1.8.4 JSONL](https://github.com/doccano/doccano/blob/v1.8.4/backend/data_export/pipeline/factories.py) | Native exports retain span triples or category lists. | This cookbook supplies a practical tool workflow; no broader institutional deployment is asserted. | Chapters 2 and 3 inspect singular `label` fields and stable source identity. |
| [COCO](https://cocodataset.org/#format-data) | A widely used computer-vision format connects images, categories, and annotations. | This guide makes no institutional adoption claim. | Chapter 1 introduces a possible downstream target without implementing conversion. |
| [Data Snapshot unified evaluation schema](https://huggingface.co/datasets/ai4data/data-snapshot) | A custom contract aligns document/page identity, normalized boxes, ground truth, and detector outputs. | The published Data Snapshot benchmarking dataset documents this representation. | Chapter 1 explains adapters conceptually and keeps the custom schema outside the manual workflow. |
