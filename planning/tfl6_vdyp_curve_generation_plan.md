# TFL 6 Natural VDYP Curve Generation Plan

## Purpose

This note starts P3.4d by defining the bounded execution plan for generating
and QAing natural/untreated VDYP curves for the refined TFL 6 AU universe.

This is a preflight/design artifact only. It does not generate curves, write
`data/model_input_bundle`, run BatchTIPSY, emit ForestModel XML, run Matrix
Builder, or assemble a Patchworks runtime package.

## Governing Scope

Roadmap lane: P3.4d.

Governing issue: `#29`.

Parent phase issue: `#13`.

Default method authority: parent FEMIC `UBC-FRESH/femic#187`.

The accepted method is the shared FEMIC AU-level first-growth selector:

- module: `femic.pipeline.au_first_growth`;
- selector: `select_au_first_growth_curve`;
- selected path: `smoothed_bin_pchip`;
- default source age window: `60-300`;
- output curve age range: `1-299`;
- smoothing: seven-point weights, four passes;
- toe handling: legacy exponential toe splice into the smoothed PCHIP body; and
- unsupported AU handling: explicit `insufficient_source_stands` diagnostics,
  not hidden curve borrowing or synthetic fabrication.

## Current Inputs

| Artifact | Path | Status |
| --- | --- | --- |
| Static AU universe | `planning/tfl6_static_au_universe.csv` | available |
| Stand-to-AU review table | `planning/tfl6_stand_to_au_review.csv` | available |
| VDYP7 polygon source attributes | `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet` | available |
| VDYP7 layer source attributes | `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` | available |
| R1 geometry / area surface | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` | available |
| Stage 01a VDYP run surface | `femic run --run-config config/run_profile.tfl6.yaml` | next executable step |

The available VDYP7 parquet files are source attributes. They are not the
stand-level `FEATURE_ID` x projected-age yield table needed by
`build_mkrf_first_growth_curves` or `select_au_first_growth_curve`.

## Standard FEMIC Stage 01a Surface

Do not create a TFL6-specific VDYP runner. The established wheel already exists:
the parent FEMIC Stage 01a path used by K3Z, TSA29, and the MKRF rebuild work.

Use the same operator sequence:

```bash
femic prep validate-case --run-config config/run_profile.tfl6.yaml --tipsy-config-dir config/tipsy
femic run --run-config config/run_profile.tfl6.yaml --run-id tfl6_stage01a
```

That path owns:

- top-strata selection;
- SI binning and sparse-bin handling;
- VDYP polygon/layer handoff through `femic.pipeline.vdyp_stage`;
- VDYP run logs under the established VDYP runtime/log locations;
- smoothed VDYP curve tables and diagnostics; and
- the later BatchTIPSY handoff boundary.

TFL6-specific work should therefore focus on making the run profile, tipsy
config, AU definitions, and accepted source inputs compatible with that Stage
01a surface. Runtime scratch and logs stay ignored; reviewed summaries and
figures can be promoted into `planning/`, `plots/`, and `docs/` after the run.

## Reused FEMIC Interfaces

The existing MKRF path is the closest implementation example:

- `femic.pipeline.mkrf_first_growth.build_mkrf_first_growth_curves`
  accepts:
  - `vdyp_yields`: columns `FEATURE_ID`, `PRJ_TOTAL_AGE`, `PRJ_VOL_DWB`;
  - `assignment`: columns that can collapse to `forest_cover_id` and `au_id`;
  - optional `source_table` for MKRF lexmatch fallback; and
  - `min_source_stands`, currently defaulting to `2`.
- `femic.pipeline.au_first_growth.select_au_first_growth_curve`
  implements the accepted shared `smoothed_bin_pchip` selector.
- MKRF plot helpers show the expected QA surfaces:
  - AU L/M/H comparison plots;
  - fit diagnostic plots with raw curves, observed binned medians/P25/P75, the
    selected fit, and residuals; and
  - curve diagnostics with RMSE, MAPE, tail RMSE, source stand count, observed
    bin count, sparse warnings, selected path, and accepted flag.

TFL 6 should reuse those selector semantics but should not reuse MKRF-specific
lexmatch or source-table assumptions unless they are refactored into a generic
helper.

## Proposed P3.4d Execution Surfaces

The next executable slice should produce review-only outputs under
`planning/` and `plots/`, not under `data/model_input_bundle/`.

Expected review outputs:

| Output | Proposed path |
| --- | --- |
| Natural first-growth curves | `planning/tfl6_vdyp_first_growth_curves.csv` |
| Natural first-growth diagnostics | `planning/tfl6_vdyp_first_growth_diagnostics.csv` |
| Natural first-growth manifest | `planning/tfl6_vdyp_first_growth_manifest.json` |
| Review note | `planning/tfl6_vdyp_first_growth_review.md` |
| L/M/H envelope plots | `plots/vdyp_lmh_tfl6-*.png` |
| Fit diagnostic plots | `plots/vdyp_fitdiag_tfl6-*.png` |

The actual model-input bundle copy can be made later only after P3.4f locks the
curve-selection and sparse-support QA surfaces.

## Required Preflight Checks Before Running Curves

1. Validate `config/run_profile.tfl6.yaml` with `femic prep validate-case`.
2. Confirm every yield-table `FEATURE_ID` is either present in
   `planning/tfl6_stand_to_au_review.csv` or explicitly excluded with a reason.
3. Build a TFL6 assignment frame from `planning/tfl6_stand_to_au_review.csv`
   with:
   - `forest_cover_id = feature_id`;
   - `au_id`;
   - `res_key = feature_id`; and
   - `shape_area_ha = area_ha`.
4. Run the standard Stage 01a path and inspect the emitted VDYP curve and log
   artifacts before promoting review summaries.
5. Treat `insufficient_source_stands` as an accepted diagnostic state, not as a
   silent failure.
6. Confirm no output path writes into `data/model_input_bundle/`.

## QA Gates

Minimum P3.4d acceptance checks:

- every selected top-area AU has either a natural/untreated VDYP curve or an
  explicit missing-curve rationale;
- diagnostics report source stand count, observed bin count, curve point count,
  selected path, accepted flag, RMSE, MAPE, and tail RMSE;
- sparse and insufficient-support AUs are listed explicitly;
- L/M/H envelope plots exist for selected AUs with enough source support;
- representative fit diagnostics exist for high-area selected AUs and for any
  suspect sparse/high-error cases;
- no natural-curve availability field is used as a proxy for managed/unmanaged
  treatment eligibility; and
- no model-input bundle, TIPSY, XML, Matrix Builder, or Patchworks runtime
  artifacts are created in this slice.

## Next Implementation Step

Run `femic prep validate-case` against `config/run_profile.tfl6.yaml`, resolve
any stale TFL6 configuration/path blockers, then run the standard `femic run`
Stage 01a lane from the instance root. If the generic Stage 01a lane cannot
consume the reviewed TFL6 AU contract, fix the generic FEMIC surface or the
TFL6 run-profile/config contract rather than introducing a parallel
instance-local VDYP runner.

Do not start BatchTIPSY or model-input bundle generation until this natural
curve QA surface is reviewed.
