# TFL 6 Instrument Boundary Reconciliation

## Purpose

This note records the post-2011 TFL 6 instrument scrape used to investigate why
the 2011 Management Plan 10 historical land-base area differs from the current
FADM-derived TFL 6 AOI.

Governing issue: `#7`.

No geometry was changed, no recipe YAML was created, and no netdown execution
was run.

## Source Page

Scraped page:

- `https://www2.gov.bc.ca/gov/content/industry/forestry/forest-tenures/timber-harvesting-rights/tfl/tfl-6`

Observed page metadata:

- page reported last updated: `2025-02-25`
- scrape date: `2026-06-23`
- filter applied: instrument links with displayed source-page date year
  `>= 2011`

The scrape initially exposed one relevant post-2011 instrument:

| Source page label | Local PDF | Status |
| --- | --- | --- |
| Instrument 101 - Jan 1, 2015 | `reference/tfl-06-inst-101-january-1-2015.pdf` | Strong post-2011 additional-area evidence. |

Instrument 10 is deliberately excluded from this post-2011 scrape result. The
current source page label is misleading for this purpose: the linked document is
clearly a 1957 amendment and is not relevant to the post-2011 AOI expansion
question.

The PDFs are image-backed scans. `pypdf` text extraction produced no useful
searchable text, so embedded page images were extracted under
`reference/extracted_images/` for visual review and later OCR.

## Instrument 101 Evidence

Visual review of `reference/tfl-06-inst-101-january-1-2015.pdf` found the key
boundary-reconciliation evidence:

- the agreement is effective `January 1, 2015`;
- it amends Tree Farm Licence 6 by adding the area known as `Block 4` of Tree
  Farm Licence 39;
- it adds all lands described on the attached map labelled `TFL 6 Instrument
  101`;
- it adds these timber licences to Schedule A lands: `T0223`, `T0230`,
  `T0237`, `T0242`, `T0251`, `T0256`, `T0260`, `T0262`, `T0270`, `T0274`,
  `T0281`, and `T0288`; and
- the attached map labels two TFL 6 addition areas:
  - `44,612 ha +/-`
  - `2,096 ha +/-`

The labelled addition areas total about `46,708 ha`.

## Area-Reconciliation Hypothesis

Current relevant area anchors:

| Area surface | Area ha | Source |
| --- | ---: | --- |
| MP10 historical GLB | `171,441` | 2011 information package Table 4 |
| Current accepted TFL 6 AOI | `217,042.718950` | P1.6 FADM-derived boundary/input manifest |
| Current minus MP10 historical GLB | `45,601.718950` | arithmetic comparison |
| Instrument 101 labelled additions | `46,708` | visual review of Instrument 101 attached map |
| Instrument additions minus observed AOI delta | `1,106.281050` | arithmetic comparison |

Instrument 101 plausibly explains most or all of the difference between the
2011 MP10 historical GLB and the current FADM-derived AOI. The labelled
addition total is close to, but not exactly equal to, the current-minus-MP10
difference: the map-labelled additions exceed the observed AOI delta by about
`1,106 ha`. Treat the mismatch as unresolved until we compare the current FADM
TFL 6 geometry against the instrument map, timber-licence parcels, and any
post-2015 boundary cleanups or exclusions.

For the teaching-instance build, this is close enough to use Instrument 101 as
the working explanation for scaling MP10 Table 4 to current-AOI validation
targets. The remaining difference may reflect smaller boundary edits, parcel
exclusions, measurement/vintage differences, or other post-MP10 tenure changes.
One unverified candidate to keep in mind is a possible later K3Z/community
forest carve-out from TFL 6; do not treat that as established fact unless a
source document or boundary overlay confirms it.

## Metadata Surfaces Updated

Updated reference metadata:

- `reference/tfl6_reference_index.json`
- `reference/tfl6_reference_index.md`
- `reference/extracted_text/tfl-06-inst-101-january-1-2015.txt`
- `reference/extracted_images/`

The JSON index now records:

- source-page label and URL for Instrument 101;
- image-only text-extraction status;
- extracted page-image paths;
- Instrument 101 as strong post-2011 additional-area evidence.

## P1.7 Handoff

Before any TFL 6 recipe skeleton treats MP10 Table 4 as a current AOI
benchmark, P1.7c should classify the boundary-vintage issue explicitly:

- MP10 Table 4 remains the historical 2011 benchmark;
- P1.6 FADM remains the current active AOI;
- Instrument 101 is the leading documented explanation for the boundary-area
  increase; and
- `planning/tfl6_adjusted_thlb_benchmarks.md` and
  `planning/tfl6_adjusted_thlb_benchmarks.json` provide provisional scaled
  current-AOI validation targets; and
- a later geometry-reconciliation task should decide whether to model the 2011
  historical AOI, the current post-2015 AOI, or both as separate benchmark
  contexts.
