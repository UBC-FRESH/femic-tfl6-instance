# TFL 6 MP11 Phase 9 Source-Layer And THLB Execution Plan

## Purpose

This P9.1 plan launches Phase 9 and turns the accepted Phase 8
source-layer/THLB contract into an executable rebuild sequence. It defines the
issue tree, branch, artifact layout, source dependency checklist, generated
output hygiene, and promotion gates before any new MP11 THLB outputs are
generated.

This plan does not materialize new public layers, execute THLB overlays, create
model-input tables, or promote MP11 values to model inputs.

## Branch And Issue Tree

- Branch: `feature/p9-mp11-source-layer-thlb-rebuild`
- Parent issue: `#66`
- Child issues:
  - P9.1 launch execution plan: `#72`;
  - P9.2 materialize and verify public source layers: `#73`;
  - P9.3 profile inventory and proxy inputs: `#74`;
  - P9.4 implement ordered overlay THLB recipe scaffold: `#75`;
  - P9.5 execute and compare public-data THLB rebuild: `#76`;
  - P9.6 close Phase 9 and hand off rebuild outputs: `#77`.

## Governing Contracts

Phase 9 executes these Phase 8 contracts:

- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_mp11_source_layer_thlb_rebuild_contract.md`;
- `planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md`;
- `planning/tfl6_mp11_kpi_qa_reporting_contract.md`.

The central rule remains unchanged: MP11 current THLB `120,099 ha` is a
comparison target, not a forced output or accepted model input.

## Artifact Layout

Tracked planning and compact QA outputs:

- `planning/tfl6_mp11_phase9_execution_plan.md`;
- `planning/tfl6_mp11_phase9_source_layer_manifest.*`;
- `planning/tfl6_mp11_phase9_field_profile.*`;
- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.*`;
- `planning/tfl6_mp11_phase9_closeout.md`.

Potential generated runtime outputs should remain ignored until explicitly
accepted:

- `runtime/mp11_source_layers/`;
- `runtime/mp11_thlb/`;
- `runtime/logs/mp11_thlb/`;
- `plots/mp11_thlb/`;
- `output/mp11_thlb/`.

Large public downloads should stay under ignored data-download paths unless a
reviewed compact source artifact is intentionally tracked:

- `data/downloads/`;
- `data/bc/`;
- other generated scratch paths covered by `.gitignore`.

Existing accepted source artifacts under `data/source/tfl_6/` and
`data/input/tfl_6/` may be verified and reused.

## Source Dependency Checklist

| Dependency family | Current local state | Phase 9 treatment |
| --- | --- | --- |
| TFL 6 AOI | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg` is tracked from prior phases. | Verify CRS, area, schema, and geometry validity in P9.2. |
| VRI/R1 inventory | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` is tracked. | Verify and re-profile for MP11 forest/productivity/low-site logic in P9.2/P9.3. |
| VDYP polygon/layer tables | `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet` and `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` are tracked. | Verify joins and profile support fields in P9.2/P9.3. |
| Roads | `data/source/tfl_6/roads/dra_roads_tfl6.gpkg` is tracked. | Verify schema and define class/buffer candidate status before overlay use. |
| Hydrology | FWA streams, lakes, and wetlands are tracked. | Verify schema and profile riparian class/buffer candidates. |
| Shoreline | No accepted high-precision MP11 shoreline layer is tracked. | Keep as unresolved/coarse-proxy unless P9.2 identifies a public-safe source. |
| Legal OGMAs | Current legal OGMA layer is tracked. | Verify current-vs-MP11 vintage and overlay status. |
| Non-legal/proposed OGMAs | Current non-legal OGMA layer is tracked as proxy evidence. | Treat as proxy/review evidence, not direct proposed-area equivalence. |
| WHA/UWR | Approved WHA and UWR layers are tracked. | Verify IDs, vintage, and overlay status. |
| Recreation/reserve layers | Recreation polygons, trails, site points, and details are tracked. | Verify schema and decide P9.3 overlay candidate fields. |
| BEC/LU strata | BEC and landscape-unit layers are tracked. | Use as QA/reporting/proxy support, not silent deductions. |
| DEM/slope | No accepted MP11 DEM/slope derivative is tracked. | P9.2/P9.3 must either materialize a public DEM workflow or mark as deferred/proxy gap. |
| WFP LBB/ITI/LEFI | Not public and not tracked. | Keep unavailable unless a public-safe source is supplied and reviewed. |
| Research/PSP/local reserves | Not fully public from current evidence. | Keep unavailable/proxy/deferred unless public-safe geometry is identified. |

## Execution Gates

Phase 9 must proceed through these gates:

1. P9.1 execution plan and issue tree are synchronized.
2. P9.2 source-layer verification records local availability and source QA.
3. P9.3 field/proxy profiling accepts or rejects candidate mappings.
4. P9.4 recipe scaffold implements ordered overlay only from accepted P9.2/P9.3
   inputs.
5. P9.5 full run compares outputs against MP11 and Phase 5 checkpoints with
   residual-gap classification.
6. P9.6 closes the phase only after PR merge, validation, and handoff notes.

No step may skip directly from MP11 summary values to generated model inputs.

## No-Force-Fit Rules

Disallowed in Phase 9:

- scaling a public THLB output to match `120,099 ha`;
- inventing proprietary WFP geometry from aggregate MP11 tables;
- using WFP LBB, ITI, LEFI, or private objective assumptions without a
  public-safe source and explicit review;
- treating current non-legal/proposed public layers as exact MP11 proposed
  reserves without vintage/source review;
- hiding aspatial or proxy deductions inside scripts; and
- replacing the Phase 5 baseline before later model-input/runtime QA phases.

## Promotion Gates

Generated Phase 9 outputs can be assigned only these states until later phases:

- `generated_diagnostic`;
- `implementation_candidate`;
- `comparison_output`;
- `deferred`;
- `rejected`;
- `unavailable_non_public`.

No Phase 9 artifact becomes `accepted_model_input` until a later model-input
phase explicitly promotes it through the Phase 8 promotion contract.

## Minimum Validation

Every Phase 9 child issue must run, at minimum:

```bash
python -m ruff check .
sphinx-build -b html docs docs/_build/html -W
```

Implementation issues must add source-layer, recipe, or THLB-specific checks
before closeout.

## P9.1 Acceptance

P9.1 is complete when:

- this plan is tracked in `planning/`;
- Phase 9 child issues are created and linked from the roadmap;
- `ROADMAP.md` marks Phase 9 active and P9.1 complete;
- `CHANGE_LOG.md` records the Phase 9 launch;
- issue `#72` is closed with validation evidence; and
- no generated THLB outputs are created or tracked.
