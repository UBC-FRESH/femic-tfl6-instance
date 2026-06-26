# TFL 6 Embedded NICF/K3Z Identity Contract

## Purpose

The TFL 6 teaching model must embed the original NICF/K3Z teaching area inside
the larger TFL 6 model while preserving distinct identities for:

- the broader TFL 6 model area;
- the K3Z/NICF core teaching AOI; and
- expansion candidate areas considered for NICF-style teaching scenarios.

This is a Phase 3 design contract for P3.2 / `#9`. It does not build geometry,
model-input tables, ForestModel XML, Matrix Builder outputs, or Patchworks
runtime files.

Related stakeholder framing is recorded in
`planning/tfl6_stakeholder_context.md`. The embedded identity contract should
support NICF-facing community/expansion reporting and WFP-facing
fibre-supply/value/cost comparison in the same runtime.

## Design Principle

NICF/K3Z and expansion identity must be represented as stand-level or
block-level grouping attributes, not as AU identity.

Reason:

- AUs define yield-curve families and should remain focused on stable
  ecological/species/SI strata.
- NICF/K3Z membership and expansion-candidate membership are planning/reporting
  identities and scenario groupings.
- Patchworks needs these identities for group accounts, matching targets, and
  reports, but they should not force duplicate AU families or duplicate yield
  curves.

## Required Identity Classes

The first reviewed contract should define at least these mutually auditable
classes:

| Identity | Meaning | Expected use |
| --- | --- | --- |
| `tfl6_base` | Area inside the accepted TFL 6 AOI but outside the embedded NICF/K3Z core and outside active expansion-candidate classes. | Whole-TFL accounting, comparison reports, broader teaching context. |
| `nicf_k3z_core` | Original K3Z/NICF teaching AOI identity from the K3Z tenure source; under the current TFL 6 AOI it is mostly an external/reference carve-out rather than a material current-AOI class. | Separate area/yield/account reporting where present, continuity with the K3Z teaching instance, and explicit carve-out audit. |
| `nicf_expansion_candidate` | Area outside `nicf_k3z_core` that is eligible for candidate expansion scenarios. | Scenario toggles, candidate pool accounting, AAC-uplift comparisons, matching targets. |
| `nicf_expansion_rejected` | Area considered but screened out by productivity, THLB, operability, constraint, or review criteria. | Audit trail, teaching comparison, rejected-pool reporting. |

The implementation can use a more compact coded field, but it must preserve
these distinctions in auditable form.

## P3.2b K3Z/NICF Core AOI Overlay Identity

P3.2b reviewed the original K3Z/NICF core source against the accepted current
TFL 6 AOI. The accepted K3Z/NICF core source remains the K3Z teaching-instance
tenure boundary:

| Surface | Path | Role |
| --- | --- | --- |
| K3Z/NICF core tenure | `external/femic-k3z-instance/data/bc/cfa/k3z/CFA K3Z Tenure.shp` | authoritative source for the original K3Z teaching AOI identity |
| Current TFL 6 AOI | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg` | active model extraction boundary accepted under P1.6 |
| Pre-pivot FDU 1/2/3 FSP AOI | `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp` | historical NICF FSP planning context, not the K3Z tenure and not the active model boundary |

Non-mutating overlay diagnostics in EPSG:3005:

| Surface | Rows | Gross area | Area intersecting current TFL 6 AOI | Area outside current TFL 6 AOI |
| --- | ---: | ---: | ---: | ---: |
| K3Z/NICF core tenure | `3` | `2391.511 ha` | `0.072 ha` | `2391.440 ha` |
| Pre-pivot FDU 1/2/3 FSP AOI | `3` | `147798.392 ha` | `118617.247 ha` | `29181.145 ha` |
| Current TFL 6 AOI | `182` | `217042.719 ha` | `217042.719 ha` | `0.000 ha` |

Interpretation:

- The K3Z/NICF core tenure is the correct identity source for continuity with
  the original K3Z teaching instance.
- The current FADM-derived TFL 6 AOI appears to exclude essentially all of the
  K3Z community-forest tenure. This is consistent with the working hypothesis
  that K3Z/community-forest lands may have been carved out of TFL 6 before the
  current boundary vintage.
- The pre-pivot FDU 1/2/3 FSP AOI is a broader planning context and overlaps a
  large part of current TFL 6, but it is not the same thing as the K3Z tenure.
- Therefore the first TFL 6 model-input bundle cannot honestly label a large
  current-AOI area as `nicf_k3z_core` unless the maintainer explicitly chooses
  to expand the model boundary beyond the accepted current TFL 6 AOI or adds an
  external adjacent/community-forest overlay surface.

Accepted P3.2b identity behavior for the first bundle:

| Field / class | First behavior |
| --- | --- |
| `is_nicf_k3z_core` | `true` only for stands or fragments that materially intersect the accepted K3Z tenure source after the final bundle overlay; expected current-AOI area is effectively zero under the current TFL 6 boundary. |
| `embedded_area_class` | use `wfp_tfl6_remainder` or equivalent for current-AOI stands outside any future accepted expansion class; do not silently assign FDU 1/2/3 area to `nicf_k3z_core`. |
| `embedded_area_id` | preserve `k3z_tenure` as a source identity/provenance ID where the K3Z overlay is present; preserve FDU/LU IDs separately as planning context if used. |
| `nicf_k3z_core_external_reference` | recommended review flag for the K3Z tenure source when it is reported alongside, but mostly outside, the current TFL 6 AOI. |
| `core_overlay_status` | record `inside_current_tfl6`, `outside_current_tfl6`, or `tiny_boundary_overlap` during Phase 4 QA so the carve-out condition is auditable. |

Rejected P3.2b shortcuts:

- Do not use the pre-pivot FDU 1/2/3 FSP AOI as a synonym for
  `nicf_k3z_core`.
- Do not force the K3Z tenure into the current TFL 6 AOI by dissolving or
  snapping geometry.
- Do not create separate AU or yield-curve families for K3Z identity.
- Do not gate CT/fertilization across broad FDU 1/2/3 area as though it were
  the K3Z/NICF core.

Open design consequence for P3.2c/P3.2d:

- Expansion-candidate classes should be defined inside the current TFL 6 AOI
  unless the maintainer explicitly broadens the model geography.
- If student scenarios need direct comparison with the original K3Z tenure,
  the first design should treat K3Z as an external/reference group or adjacent
  carve-out group, not as a large current-AOI embedded core.
- Group accounts and reports should preserve the distinction between K3Z
  tenure, FDU/LU planning context, expansion candidates, and the WFP/TFL 6
  remainder.

## P3.2c Expansion And Remainder Identity Classes

P3.2c defines the identity classes that Phase 4 must be able to carry, but it
does not materialize candidate geometry or execute screening logic. Candidate
status is a model-design/reporting identity, not an AU or yield-curve identity.

Accepted class vocabulary:

| `embedded_area_class` | Meaning | First-bundle behavior |
| --- | --- | --- |
| `wfp_tfl6_remainder` | Current-AOI TFL 6 stands that are not accepted K3Z core and are not in an accepted expansion-candidate or rejected-candidate class. | Default current-AOI class for the first bundle unless a later P3.2 screen assigns a candidate/rejected class. |
| `nicf_expansion_candidate` | Current-AOI stands outside the near-zero K3Z core overlay that pass the reviewed expansion screen and are available for NICF-style scenario toggles. | Scenario/reporting class only; does not alter AU identity, curve family, or base treatment eligibility by itself. |
| `nicf_expansion_rejected` | Current-AOI stands considered by the expansion screen but rejected by productivity, THLB, operability, reserve/retention, constraint, source-quality, or maintainer-review rules. | Audit/reporting class; keeps rejected-pool evidence visible. |
| `nicf_expansion_pool_unreviewed` | Current-AOI stands inside the candidate search envelope before the P3.2d/P4 screen assigns accepted or rejected status. | Temporary planning/QA status only; should not be used as an active scenario class in the first runtime package. |
| `nicf_k3z_core_reference` | K3Z tenure identity carried as a provenance/external-reference group because the current TFL 6 AOI contains only a tiny boundary overlap. | Reference/reporting class only unless the maintainer later broadens model geography. |

Candidate-area pool semantics for the active TFL 6 AOI:

- Candidate areas are searched inside the accepted current TFL 6 AOI unless the
  maintainer explicitly broadens the model geography.
- Candidate areas are outside the accepted K3Z tenure source under the current
  overlay, because the K3Z core is effectively external to the active AOI.
- Candidate areas must be separately identifiable from the WFP/TFL 6 remainder
  so scenario toggles can move or compare them without relabeling the whole
  TFL 6 model.
- Candidate status is not equivalent to THLB status. A candidate may need
  separate fields for source-pool membership, active THLB, treatment
  eligibility, operability, and scenario activation.
- Rejected candidates remain valuable teaching evidence; they explain why a
  plausible-looking area is not used for expansion scenarios.

Required source/provenance fields for the first candidate screen:

| Field family | Candidate field(s) | Purpose |
| --- | --- | --- |
| Stand key and area | `feature_id`, `map_id`, `polygon_id`, `area_ha` | trace candidate decisions to final bundle stands/fragments |
| Current AOI membership | `inside_tfl6_aoi` or implicit bundle membership | ensure candidates are inside the accepted active geography |
| K3Z reference overlay | `is_nicf_k3z_core`, `core_overlay_status`, `nicf_k3z_core_external_reference` | keep K3Z tenure continuity separate from expansion decisions |
| Expansion identity | `embedded_area_class`, `embedded_area_id`, `is_nicf_expansion_candidate`, `is_nicf_expansion_rejected` | carry candidate/rejected/remainder classes into Patchworks groups |
| Candidate set | `expansion_candidate_set`, `expansion_scenario_group` | support multiple future candidate-pool definitions or scenario toggles |
| Screen status | `expansion_screen_status`, `expansion_screen_reason` | explain accepted/rejected/unreviewed decisions |
| THLB and eligibility | final Phase 4 THLB flag, `IFM`, `RETENTION`, reserve/non-THLB status | prevent candidate status from silently overriding land-base eligibility |
| Productivity | `site_index`, `est_site_index`, `estimated_site_index`, AU/SI class, VDYP curve availability | support productivity screening and AAC-uplift plausibility |
| Operability/cost | `HARVEST_SYSTEM`, operability/slope proxy fields, ground/cable/heli class | support delivered-cost proxy and operability screening |
| Constraints/context | UWR/WHA/OGMA/recreation/riparian/retention/context flags where carried by Phase 4 | keep constrained/rejected reasons auditable |
| Stakeholder grouping | `wfp_tfl6_remainder`, whole-TFL group, FDU/LU context where carried | support WFP-facing comparison and FDU/LU context reporting |

First screen-status vocabulary:

| `expansion_screen_status` | Meaning |
| --- | --- |
| `accepted_candidate` | passed the reviewed candidate screen and may be toggled in expansion scenarios |
| `rejected_productivity` | failed the reviewed productivity/SI/yield screen |
| `rejected_non_thlb` | outside active THLB or otherwise not schedulable under the base land-base contract |
| `rejected_operability` | failed the reviewed operability/harvest-system/slope/cost screen |
| `rejected_constraint` | rejected by reserve, retention, UWR/WHA/OGMA, riparian, recreation, or other constraint context |
| `rejected_source_quality` | missing or ambiguous source fields prevent reliable classification |
| `rejected_review` | maintainer-reviewed rejection not covered by a more specific code |
| `unreviewed_pool` | inside the search envelope but not yet screened |
| `not_in_pool` | current-AOI remainder not considered for expansion |

P3.2c accepts only the identity/class vocabulary. P3.2d must define the
Patchworks group-account, matching-target, scenario-toggle, and report
requirements that consume these classes. Any executable screen or candidate
geometry materialization belongs to Phase 4 or a later explicitly scoped
implementation lane.

## Candidate Stand Attributes

Phase 4 model-input generation should receive explicit fields such as:

- `embedded_area_class`;
- `embedded_area_id`;
- `is_nicf_k3z_core`;
- `is_nicf_expansion_candidate`;
- `is_nicf_expansion_rejected`;
- `expansion_candidate_set`;
- `expansion_screen_status`;
- `expansion_screen_reason`;
- `expansion_scenario_group`; and
- optional source geometry/provenance fields for K3Z/NICF and expansion
  overlays.

Exact field names can be finalized in P3.7 / the model-input contract, but the
identity content must be available before P4.1 starts.

## Patchworks-Facing Requirements

The embedded identity contract must support:

- group accounts for the whole TFL 6 area, NICF/K3Z core, expansion candidates,
  rejected candidates, and TFL 6 remainder;
- matching targets that can compare NICF/K3Z core behavior against expansion
  candidate behavior;
- matching targets and reports that compare NICF-preferred expansion outcomes
  against broader TFL 6 and WFP-facing fibre-supply, value, and delivered-cost
  signals where available;
- area/yield/product reports split by embedded area class;
- scenario toggles that add or exclude expansion candidates without altering
  base AU identity;
- AAC-uplift reporting for expansion scenarios; and
- continuity reports that help students compare the former K3Z teaching model
  with the embedded TFL 6 model.

The reporting design should make tradeoffs visible. Expansion candidates that
increase NICF opportunity may still affect WFP fibre supply, fibre value, or
delivered unit cost in the TFL 6 remainder; those effects should be reportable
rather than hidden inside a single whole-model total.

## Dependencies

- P3.3 / `#28` owns AU identity and curve-lane semantics.
- P3.4 / `#29` owns actual yield-curve build and QA.
- P3.5 / `#30` owns treatment options.
- P3.6 / `#31` owns base state-transition logic and should expose hook points
  for embedded-area groups without completing expansion details.
- P3.2 / `#9` owns the embedded NICF/K3Z and expansion-candidate identity
  design.
- P3.7 owns final run-profile/model-input field naming after P3.2 is reviewed.

## Acceptance Checks

- The K3Z/NICF core tenure source can be overlaid against the current TFL 6
  AOI, and the near-zero current-AOI intersection is reported rather than
  hidden.
- A stand in an expansion-candidate pool can be identified separately from the
  K3Z/NICF core and from the TFL 6 remainder.
- Group-account, matching-target, and report requirements are listed before
  P4.1 starts.
- Embedded identity fields do not change AU assignment or curve family.
- Expansion scenarios can change inclusion/eligibility/reporting without
  redefining AUs.
