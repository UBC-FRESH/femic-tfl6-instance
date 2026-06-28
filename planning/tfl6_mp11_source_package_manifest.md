# TFL 6 MP11 Source Package Manifest

## Purpose

This P6.1 note records the public source identity, local source-copy
convention, document-component ranges, and extraction-manifest contract
for the TFL 6 Management Plan 11 package. It is a provenance surface, not
a model-input change.

## Source Identity

- Source package ID: `tfl6_mp11_202606_public_pdf`
- Source URL: `https://www.westernforest.com/wp-content/uploads/2026/06/TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf`
- Accessed at UTC: `2026-06-28T00:00:00Z`
- Document title: `Tree Farm Licence 6 Management Plan 11`
- Version/date: `Version 1, June 2026`
- Publisher: `Western Forest Products Inc.`
- Byte size: `9147004`
- Page count: `475`
- SHA256: `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Expected SHA256: `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Checksum status: `passed`
- PDF format: `PDF 1.7`
- Producer: `Pdftools SDK`
- Modification date: `D:20260622195710Z`
- PyMuPDF version used for inspection: `1.27.2.3`

## Governance Caveat

Treat as a public planning and AAC-analysis package. Do not treat the AAC analysis as a final Chief Forester AAC decision unless a separate approved decision is located and reviewed.

## Local Source-Copy Policy

The PDF is not tracked in this repository. A local source copy may live in
ignored runtime/download/cache space only after URL, byte size, page count,
and SHA256 are verified.

Accepted ignored locations:

- `runtime/mp11/source/`
- `data/downloads/mp11/`
- `external public-data cache with matching SHA256`

## Document Components

Machine-readable component table: `planning/tfl6_mp11_document_components.csv`

| Component | PDF pages | Role | Notes |
| --- | ---: | --- | --- |
| `management_plan_main` | `1-44` | `front_matter_governance_context` | Includes MP purpose, AAC history, public review, appendices listing, and governance context. |
| `appendix_a_divider` | `45-45` | `component_boundary` | Management Plan divider page identifying Appendix A as the Timber Supply Analysis Report. |
| `appendix_a_timber_supply_analysis` | `46-226` | `primary_mp11_analysis_source` | Primary source for land-base, THLB, sensitivity, model-behavior, and AAC-recommendation evidence. |
| `appendix_a_trailing_blank` | `227-227` | `blank_component_boundary` | Blank management-plan page between Appendix A and Appendix B divider. |
| `appendix_b_divider` | `228-228` | `component_boundary` | Management Plan divider page identifying Appendix B as the Timber Supply Analysis Information Package. |
| `appendix_b_acceptance_letter` | `229-229` | `information_package_acceptance_context` | Ministry acceptance correspondence preceding the information package. |
| `appendix_b_information_package` | `230-475` | `assumption_and_input_package_source` | Source for timber-supply inputs, assumptions, inventory, land base, yield, and nested appendix evidence. |

## Extraction-Manifest Contract

Machine-readable field table: `planning/tfl6_mp11_extraction_manifest_fields.csv`

Every P6.2+ extracted claim must preserve page/component provenance,
method/tool provenance, review status, downstream-use classification,
and model-input status. Raw extracted values must remain separate from
reviewed evidence and accepted model contracts.

Required fields:

- `record_id`: Stable unique extraction row identifier.
- `source_package_id`: Source package identifier.
- `source_sha256`: SHA256 of the public PDF used for extraction.
- `document_component`: Component ID from the source manifest.
- `pdf_page`: One-based PDF page number.
- `section_path`: Hierarchical section heading path.
- `object_type`: Extracted object class.
- `claim_text`: Verbatim or tightly paraphrased extracted claim.
- `comparison_topic`: Phase 6 comparison lane.
- `extraction_method`: Tool or method used to create the row.
- `tool_versions`: Relevant parser/package versions.
- `review_status`: Review state for use in downstream planning.
- `downstream_use`: Permitted downstream use of this row.
- `model_input_status`: Whether row may enter model inputs.

## Phase 6 Non-Goals

- do not change accepted model inputs;
- do not rerun THLB;
- do not regenerate yield curves;
- do not regenerate ForestModel XML or Matrix Builder outputs;
- do not republish the Phase 5 runtime package;
