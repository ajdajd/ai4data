---
id: glossary
title: Glossary
sidebar_position: 91
description: Terms used in the open-source-data-annotation cookbook, in plain language.
---

# Glossary

**Adapter.** A small set of trained parameters added to a model for a task, so that fine-tuning fits on modest hardware (parameter-efficient fine-tuning).

**AI-ready.** Data and metadata that software, including AI systems, can find, retrieve, interpret, and cite without manual steps. See the [AI-ready data framework](/docs/ai-ready-framework).

**Annotation.** Optional properties on a tool that describe its behaviour (for example that it is read-only); hints that clients treat as untrusted unless the server is trusted.

**API.** Application programming interface: the address at which a program asks a system for data and receives it in a structured form.

**Benchmark (population).** The share of each group in the population, from the census or population estimates, against which a dataset's composition is compared.

**Bounding box.** The rectangle that encloses a detected table or figure on a page, written as the left, top, right, and bottom edges as fractions of the page width and height, with the origin at the top left.

**Candidate.** A model shortlisted for a task, with its licence classified and its card checked, to be run on the suite.

**Data annotation.** The assignment of reviewed labels to data records or selected regions, such as document bounding boxes, text spans, or survey responses. This qualified term distinguishes data labeling from annotations that describe software tools.

**Data snapshot.** A bounded visual region of a document page containing structured or semi-structured information for analytical interpretation or operational reuse, such as a statistical table, chart, analytical map, or monitoring dashboard. A crop should retain the context needed to interpret it.

**DDI.** The Data Documentation Initiative, the standard for documenting surveys and their variables, value labels, and files; the World Bank microdata schema is based on it.

**Decision.** A curator's recorded verdict on a suggestion: accept, edit (with the final text), or reject (with a reason).

**ISCO-08.** The International Standard Classification of Occupations, whose four-digit codes classify jobs; the label of the coding examples in this guide.

**Label.** The column a model is trained to predict: the occupation code, the transcribed value, the series a question refers to.

**Language model.** A model that reads and writes text; used in these guides to draft, flag, code, explain, and translate, with a person deciding.

**Map.** The table of model-assisted tasks with phase, role, review, data sensitivity, model location, and owner.

**Maturity level.** One of three states used in this guide: foundational, AI-ready, AI-native.

**Mention.** A reference to a dataset in a document, named or unnamed.

**ML-ready dataset.** A fixed, versioned set of examples with a documented structure, a stated purpose, a split for training and testing, a statement of whom the examples represent, and a licence that covers model training.

**OCR.** Optical character recognition: reading text from the image of a page, which is what a scanned document needs before anything can be extracted from it.

**Prompt.** The instructions and context given to a language model for one task; kept as a versioned file when it is part of a workflow.

**Provenance.** The record of where a value came from: the series, the release, the source, the document and page, the method, and the version, carried with the value.

**RAG.** Retrieval-augmented generation. A pattern where the system retrieves records first and the model writes the answer from them.

**Resource.** Context a server offers to the model or the user, such as code lists or a release calendar, identified by a URI.

**Stable identifier.** An identifier for a series or dataset that does not change across releases or site redesigns.

**Suite.** A question set, the scripts that score it, the required scores, and the record of runs.

**Token.** The unit in which language models read and write text, roughly three quarters of a word; prices, context limits, and throughput are counted in tokens.

**Use.** A document whose analysis, decision, or statement depends on the data, as opposed to a mention that cites them as context.

**Verified.** The status of an extracted value that matched a printed label, a total, a derivation, or a catalog value.

**Vocabulary.** A concept scheme with preferred labels, alternates, and URIs, to which free-text keywords and topics are mapped.
