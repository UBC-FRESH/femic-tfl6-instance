# TFL 6 Source-Layer Recipe Contracts

## Purpose

This note starts P2.3 by defining reviewed current-AOI source-layer recipe
contracts for the first TFL 6 THLB lane.

Governing issue: `#23`.

This is a contract-planning slice only. It does not fetch source layers, create
executable recipe YAML, run THLB netdown, build DEM/slope products, generate
model inputs, or build Patchworks runtime artifacts.

## Contract Vocabulary

| Status | Meaning for P2.3 |
| --- | --- |
| `contract_draft_ready` | Source surface and first rule boundary are clear enough to draft a reviewed recipe contract, but not to execute it. |
| `contract_review_required` | Source exists, but filtering, overlap order, vintage, or null handling must be reviewed before P2.4 execution. |
| `aspatial_fallback` | Base teaching lane may use a non-spatial deduction or benchmark-calibrated treatment; do not imply recovered geometry. |
| `qa_only` | Field/source may be used for diagnostics and reconciliation only. |
| `deferred_sensitivity` | Keep out of the first base lane; may become a later student/sensitivity/enhancement task. |
| `context_only` | Preserve in reports/validation, not as a current THLB deduction. |

## Source-Layer Contract Table

| Step | Contract status | Source surface | First contract boundary | Required QA before P2.4 execution |
| --- | --- | --- | --- | --- |
| `tfl6_nd_000` total landbase | `contract_draft_ready` | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`; `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` | Use the accepted current TFL 6 AOI and clipped R1 geometry as the area universe. | Confirm R1 area sums to accepted AOI, use R1 geometry-derived area for accounting, and preserve MP10 historical GLB as benchmark context only. |
| `tfl6_nd_010` non-forest | `contract_draft_ready` | clipped R1 BCLCS, land-cover, and non-vegetated fields | Draft a high-side review envelope from `bclcs_level_2 in {N, W}` or null, with `bclcs_level_1 in {N, U}` as conservative comparison. Use `for_mgmt_land_base_ind == N` as QA-only. | Final code mapping, null/unreported treatment, and ordered marginal area comparison against scaled `17069.353 ha` deduction. |
| `tfl6_nd_020` existing roads | `contract_review_required` | `data/source/tfl_6/roads/dra_roads_tfl6.gpkg`; MP10 Table 6 road-width rules | Draft a road-line buffer overlay contract using DRA class/surface/type fields and MP10 width classes as review targets. Keep existing roads separate from future roads. | Decide included road classes, bridge/trail/virtual handling, buffer widths by class, overlap order, and comparison against scaled `4981.674 ha` deduction. |
| `tfl6_nd_030` total forested | `context_only` | prior ordered state | Report-only checkpoint after non-forest and existing-road deductions. | Confirm cumulative area accounting, not a source-layer deduction. |
| `tfl6_nd_040` non-productive forest | `contract_draft_ready` | clipped R1 `non_productive_*`, site/productivity, volume, and BCLCS fields | Draft from explicit `non_productive_descriptor_cd` / `non_productive_cd` presence plus a reviewed productivity threshold candidate. First benchmark-proximate review rule is explicit non-productive signal or `site_index < 5`. | Accept or revise threshold; map CP/MH/MH1/S7/S8/PG5-style MP10 classes; avoid double-counting non-forest; compare ordered marginal area against scaled `8816.360 ha` deduction. |
| `tfl6_nd_050` total productive forest | `context_only` | prior ordered state | Report-only AFLB-style checkpoint. | Confirm cumulative area accounting against scaled `186175.333 ha` target. |
| `tfl6_nd_060` inoperable/uneconomic | `deferred_sensitivity` | P2.1a operability proxy design; R1/VDYP proxy fields; future DEM/slope surface | Do not draft executable base-lane spatial rule yet. Carry candidate fields forward for contract design: height, site index, estimated site index, live volume, crown closure, basal area, stems per hectare, species group, free-to-grow/open-stand signals. | Needs a reviewed multi-factor proxy, DEM/slope materialization or explicit aspatial fallback decision, and calibration to scaled `15746.393 ha` deduction. |
| `tfl6_nd_070` total operable | `context_only` | prior ordered state | Report-only LHLB-style checkpoint. | Confirm cumulative area accounting against scaled `170428.940 ha` target. |
| `tfl6_nd_080` riparian management | `contract_review_required` | `data/source/tfl_6/hydrology/` FWA streams, lakes, wetlands; optional shoreline candidate still unresolved | Draft operational riparian RMA/RRZ/RMZ overlay contract from FWA hydrology, with MP10 Table 9 and FPPR-style widths as rule references. Preserve 40 m ocean shoreline rule as accepted MP10 rule, but keep coastline geometry under review. | Decide stream/lake/wetland class fields, buffer widths, RRZ vs RMZ retention treatment, ocean shoreline geometry source, overlap order, and comparison against scaled `13460.014 ha` deduction. |
| `tfl6_nd_090` ungulate winter ranges | `contract_review_required` | `data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg` | Draft UWR overlay contract targeting MP10 U-1-010 plus small U-1-011 overlap. | Verify UWR IDs, current-vs-2011 consistency, overlap with prior deductions, and comparison against scaled `1662.246 ha` deduction. |
| `tfl6_nd_100` established OGMAs | `contract_review_required` | `data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg` | Draft current legal OGMA overlay contract as the established-OGMA review candidate. | Verify legal-current dates and IDs against MP10 established OGMAs, handle current-vs-2011 vintage risk, and compare against scaled `4747.465 ha` deduction. |
| `tfl6_nd_110` draft OGMAs | `aspatial_fallback` | `data/source/tfl_6/ogma/ogma_non_legal_current_tfl6.gpkg` as proxy clue only; MP10 Table 11 fallback | Do not use the tiny current non-legal OGMA intersection as a direct draft-OGMA rule. Draft the base lane as an aspatial/benchmark-calibrated fallback unless historical/local draft geometry appears. | Preserve warning that current non-legal OGMA is not 2011 draft geometry; compare against scaled `4391.722 ha` deduction. |
| `tfl6_nd_120` wildlife habitat areas | `contract_review_required` | `data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg` | Draft WHA overlay contract targeting listed MP10 WHA IDs. | Verify WHA IDs, current-vs-2011 consistency, overlap with OGMAs/UWR, and comparison against scaled `3.798 ha` deduction. |
| `tfl6_nd_130` recreation sites and trails | `contract_review_required` | `data/source/tfl_6/recreation/` polygons, trails, site points, and details/closures context | Draft recreation overlay/buffer contract with MP10 10 m buffer candidate for accepted geometry classes. | Decide lifecycle/status filters, point/line/polygon treatment, 10 m buffer application, details/closures context-only handling, and comparison against scaled `63.300 ha` deduction. |
| `tfl6_nd_140` deciduous-leading forest | `contract_draft_ready` | clipped R1 and VDYP7 layer leading species fields | Draft leading-species attribute contract using `species_cd_1 in {DR, AC, MB}` from R1 with VDYP7 layer cross-check. Do not remove deciduous secondary components in conifer-leading stands. | Decide missing VDYP7 layer handling, final deciduous species-code set, ordered marginal result, and comparison against scaled `2245.868 ha` deduction. |
| `tfl6_nd_150` cultural heritage resources | `aspatial_fallback` | MP10 Table 15; no public sensitive TUS/CMT geometry | Draft base lane as aspatial/proxy fallback. Do not seek or imply access to sensitive geometry. | If proxy is later spatialized, it must use a reviewed EFZ plus 1 km ocean-proximity logic; otherwise compare aspatial deduction against scaled `167.111 ha` target. |
| `tfl6_nd_160` total operable reductions | `context_only` | prior ordered state | Report-only checkpoint. | Preserve MP10 rounding note; no source-layer deduction. |
| `tfl6_nd_170` reduced landbase | `context_only` | prior ordered state | Report-only checkpoint before stand-level retention. | Confirm cumulative area accounting. |
| `tfl6_nd_180` stand-level retention | `aspatial_fallback` | MP10 Table 16; `data/source/tfl_6/strata/` LU/BEC as context; no materialized strategic RMZ geometry | Draft base lane as aspatial Table 16 deduction: historical `5686 ha` or scaled `7198.423 ha` validation target. | Do not block on strategic RMZ geometry. Keep geometry-backed RMZ/LU/BEC replacement as advanced student/sensitivity challenge. |
| `tfl6_nd_190` current THLB | `context_only` | prior ordered state | Report-only current THLB checkpoint. | Compare against scaled `136487.728 ha` target after executable P2.4 run exists. |
| `tfl6_nd_200` future roads | `context_only` | MP10 Table 17 | Keep out of current THLB base lane; reserve for long-term landbase/scenario context. | Do not mix with existing-road overlay unless a later scenario explicitly opens it. |
| `tfl6_nd_210` long-term landbase | `context_only` | prior ordered state plus future roads | Report-only long-term context. | Not part of current THLB base-lane execution. |

## P2.3c Accepted P2.4 Handoff

P2.3 accepts the contract table above as the starting point for P2.4 executable
recipe work, with the following boundaries.

P2.4 may create the first executable THLB recipe YAML only if the recipe keeps
the contract statuses visible in outputs and treats the first run as a smoke
lane, not a final THLB reconstruction.

Authorized first-lane contract:

| Step class | P2.4 authorization |
| --- | --- |
| Area universe | Use accepted TFL 6 AOI and R1 geometry as the complete accounting surface. |
| Inventory-derived rows | Encode `tfl6_nd_010`, `tfl6_nd_040`, and `tfl6_nd_140` from the accepted R1/VDYP field surfaces. Use the P2.2c rule candidates as initial parameters, and report both gross candidate area and ordered marginal area. |
| Existing roads | Encode DRA roads as a provisional spatial overlay with explicit road-class/filter/buffer parameters in the recipe. Do not claim road semantics final until the P2.4 smoke report compares marginal area against the scaled road benchmark. |
| Riparian management | Encode FWA streams/lakes/wetlands as provisional operational riparian overlays if P2.4 defines the exact class/buffer table in the recipe. Keep ocean shoreline as unresolved unless a reviewed coastline source or aspatial fallback is explicitly selected in that P2.4 slice. |
| UWR, WHA, established OGMA, recreation | Encode materialized public overlays as provisional spatial overlays with ID/status/vintage filters exposed as parameters. Current-vs-2011 warnings must remain in the smoke report. |
| Draft OGMA | Use an aspatial/benchmark-calibrated fallback for the first base lane unless historical draft geometry is supplied and reviewed before execution. The current non-legal OGMA proxy must remain context-only for this row. |
| Cultural heritage | Use an aspatial fallback only. Do not seek or imply access to sensitive TUS/CMT geometry. |
| Stand-level retention | Use the accepted aspatial Table 16 fallback for the first base lane. Strategic RMZ geometry replacement remains a later student/sensitivity challenge. |
| Operability | Do not implement a spatial operability proxy in the first base lane unless P2.4 explicitly opens that as the smoke target and includes P2.1a constraints. Otherwise use an aspatial benchmark-calibrated placeholder and leave DEM/slope implementation for a later issue. |
| Future roads | Keep out of current THLB execution. Preserve as long-term/context row only. |
| Checkpoint rows | Preserve GLB/AFLB/LHLB/THLB and long-term milestones as report rows, not deductions. |

Minimum P2.4 smoke-report requirements:

- ordered marginal area for every deduction row;
- cumulative area at every MP10 checkpoint row;
- gross candidate area for every spatial/attribute rule before overlap removal;
- explicit list of aspatial fallback rows and their deduction values;
- explicit list of provisional/review-required rows;
- comparison to scaled current-AOI benchmark targets; and
- warning if any R1 polygon is dropped because a joined VDYP table is missing.

Rows still not final after P2.3:

- DRA road filters and class-to-buffer mapping;
- riparian class/buffer table and ocean-shoreline geometry;
- current-vs-2011 interpretation for UWR, WHA, and established OGMA;
- draft OGMA historical geometry;
- operability spatial/proxy implementation; and
- strategic RMZ geometry for Table 16.

These unresolved items do not block a P2.4 smoke lane, but they must remain
visible as provisional, fallback, or sensitivity-bound assumptions.

## P2.4 Handoff Boundary

P2.4 may start executable recipe work only after P2.3 closes with reviewed
source-layer contracts. The first executable lane should:

- preserve MP10 Table 4 row order;
- use R1 as the complete area accounting universe;
- explicitly state whether each row evaluates from R1 alone, a joined VDYP
  table, a spatial overlay, or an aspatial fallback;
- prevent R1 polygons missing VDYP rows from being silently dropped;
- keep all fallback rows visible in validation output; and
- compare ordered marginal results against the scaled current-AOI benchmark
  targets, while retaining MP10 historical values as provenance.

## P2.3 Closeout

P2.3 is complete:

- a child issue is open and linked under the Phase 2 parent;
- reviewed source-layer contract rows are recorded for every MP10 Table 4 row;
- accepted source surfaces, unresolved rule decisions, QA checks, and execution
  blockers are visible;
- aspatial fallback rows are explicit and do not masquerade as recovered
  geometry; and
- the P2.4 smoke-lane handoff boundary is defined.

P2.3 did not fetch source layers, create executable recipe YAML, execute THLB
netdown, build DEM/slope products, generate model inputs, or start XML, Matrix
Builder, or Patchworks runtime work.

## Non-Goals

- No source fetches.
- No executable recipe YAML.
- No THLB netdown execution.
- No DEM/slope materialization or zonal statistics.
- No model-input, XML, Matrix Builder, or Patchworks runtime work.
