# TFL 6 MP11 Phase 10R Curve Rebuild Closeout

## Purpose

This note closes Phase 10R: MP11 curve parser and curve rebuild. Phase 10R
parsed the public MP11 managed-yield TIPSY row tables, built the BatchTIPSY
handoff, generated 25 Table 57 future-managed candidate curves through FEMIC's
parent-package BTC runner, reused the valid canonical AU TIPSY curve for 2 FMH
rows, regenerated managed and natural comparison plots, and locked a
reproducible curve-generation recipe.

The 27 generated Table 57 managed curves are accepted for the Phase 11 curve
handoff. They remain `not_model_input` in these review artifacts until Phase 11
materializes explicit model-input tables, ForestModel XML, and Patchworks
packages.

## Branch And Issue Tree

- Branch: `feature/p10r-curve-rebuild-roadmap-correction`
- Parent issue: `#92`
- Child issues:
  - P10R.1 launch MP11 curve-rebuild execution plan: `#93`;
  - P10R.2 parse MP11 Tables 54, 55, and 57 per-AU TIPSY rows: `#94`;
  - P10R.3 QA managed-yield rows and build BatchTIPSY handoff inputs: `#95`;
  - P10R.4 run and parse MP11 managed curve generation: `#96`;
  - P10R.5 regenerate natural and managed curve plots and overlays: `#97`;
  - P10R.6 close curve-rebuild phase and hand off accepted curve candidates:
    `#98`.

## Locked Recipe

The reproducible curve-generation recipe is locked in:

- `scripts/run_p10r_mp11_curve_generation_recipe.py`;
- `planning/tfl6_mp11_curve_generation_recipe.md`; and
- `planning/tfl6_mp11_curve_generation_recipe_lock.json`.

Run it from the parent FEMIC checkout:

```powershell
& .\.venv\Scripts\python.exe external/femic-tfl6-instance/scripts/run_p10r_mp11_curve_generation_recipe.py
```

The recipe uses FEMIC's supported BTC command surface:

```powershell
& .\.venv\Scripts\python.exe -m femic tipsy run-btc `
  planning/tfl6_mp11_tipsy_handoff.csv `
  --output-csv runtime/mp11_yield/p10r_mp11_candidate_04_output.csv `
  --error-csv runtime/mp11_yield/p10r_mp11_candidate_04_error.csv `
  --scratch-dir runtime/mp11_yield/scratch `
  --log-dir runtime/mp11_yield/logs `
  --run-id p10r_mp11_candidate `
  --instance-root external/femic-tfl6-instance
```

Do not hand-build BatchTIPSY command syntax for this lane.

## Locked Input Policy

The active handoff emits only MP11 rows that map to canonical top-N TFL 6 AUs:

- accepted AUs are the L/M/H site-index class splits of the top-N strata;
- emitted TIPSY BEC zone/subzone comes from the target canonical AU VRI record;
- candidate rows must have species overlap with the canonical AU species combo;
- rows with no canonical top-N target AU remain blocked;
- rows with invalid duplicate row-derived parameters can reuse the existing
  canonical AU TIPSY curve; and
- blocked or reuse rows are not emitted to the BTC handoff.

TIPSY site index is locked to the VRI-derived target canonical AU median SI:

- `tipsy_input_si` is copied from `tfl6_static_au_universe.csv:median_si`;
- every positive planted-species SI column in the BTC input row must equal
  `tipsy_input_si`; and
- parsed MP11 per-species SI values are retained as
  `mp11_parsed_weighted_si` provenance only.

`FMH01` and `FMH22` are accepted through the explicit target-AU assignment
`cwhvm2_hw_ba_l`, so their emitted TIPSY BEC is `CWH/vm` and their emitted
TIPSY SI is the target AU median VRI SI `14.0`. They are not emitted as
duplicate BTC rows because their row-derived parameters produced invalid
TIPSY-vs-VDYP diagnostics; instead they reuse the valid canonical
`cwhvm2_hw_ba_l` future-managed TIPSY curve.

## Rebuilt Outputs

The locked recipe currently validates:

| Surface | Output | Current result |
| --- | --- | --- |
| Parsed MP11 TIPSY rows | `planning/tfl6_mp11_tipsy_row_parse.{csv,json,md}` | `141` parsed rows from Tables 54, 55, and 57. |
| BTC handoff | `planning/tfl6_mp11_tipsy_handoff.{csv,json,md}` | `25` Table 57 generation rows. |
| Handoff map | `planning/tfl6_mp11_tipsy_handoff_map.csv` | `25` BTC candidates, `2` canonical AU curve reuse rows, `105` Tables 54/55 blocked rows, and `9` parser-review rows. |
| Raw BTC output | `runtime/mp11_yield/p10r_mp11_candidate_04_output.csv` | `25` output rows, retained under ignored runtime space. |
| Raw BTC errors | `runtime/mp11_yield/p10r_mp11_candidate_04_error.csv` | `0` error rows. |
| Parsed managed curves | `planning/tfl6_mp11_managed_curves.{csv,json}` | `972` age-by-curve rows across `27` feature IDs. |
| Managed curve comparison | `planning/tfl6_mp11_managed_curve_comparison.{csv,json,md}` | `27` comparison rows accepted for Phase 11 handoff. |
| Managed plot manifest | `planning/tfl6_mp11_managed_curve_plot_manifest.{csv,json,md}` | `27` managed Phase 10R-vs-Phase 5 plots. |
| TIPSY-vs-VDYP diagnostics | `planning/tfl6_mp11_tipsy_vdyp_diagnostic_manifest.{csv,json,md}` | `27` AU-wise diagnostic plots. |
| Reproducibility lock | `planning/tfl6_mp11_curve_generation_recipe_lock.json` | Command sequence, validation, and artifact hashes. |

The PNG plot libraries are intentionally under ignored runtime/review space:

- `plots/mp11_managed_curve_comparison/`;
- `plots/mp11_tipsy_vdyp_diagnostics/`.

## Deferred Rows

Tables 54 and 55 remain deferred for curve generation because their existing
and recent managed AU codes do not carry enough public BEC/site-series
information for direct BatchTIPSY handoff. They require a public-safe MP11
AU-code to BEC/site-series mapping before they can enter this recipe.

No Table 57 future-managed row is blocked for the Phase 11 curve handoff.

## Diagnostic Context

The current TIPSY-vs-VDYP diagnostic class counts are:

| Diagnostic class | Row count |
| --- | ---: |
| `tipsy_substantially_above_vdyp` | `19` |
| `tipsy_substantially_below_vdyp` | `1` |
| `tipsy_vdyp_close` | `2` |
| `tipsy_vdyp_moderate_difference` | `5` |

These classes remain diagnostic context attached to the accepted Phase 11 curve
handoff. They do not reopen the Phase 10R curve-generation recipe.

## Validation

The locked recipe validation reports:

- BTC manifest status: `ok`;
- BTC exit code: `0`;
- BTC error rows: `0`;
- BTC handoff rows: `25`;
- BTC generation candidate rows: `25`;
- canonical curve reuse rows: `2`;
- accepted curve rows: `27`;
- managed curve features: `27`;
- managed curve rows: `972`;
- managed plot rows: `27`;
- diagnostic plot rows: `27`;
- BEC mismatch count: `0`;
- candidate/target BEC mismatch counts: `0` and `0`; and
- SI mismatch count: `0`.

Focused closeout checks also confirmed:

- stale 25-row plot libraries were removed before regeneration;
- the FMH rows use the target AU `CWH/vm` BEC and the existing canonical
  `cwhvm2_hw_ba_l` future-managed TIPSY curve, not row-derived `MH/mm` or
  duplicate FMH BTC outputs;
- every positive BTC SI column equals the target AU median VRI SI;
- the new recipe and lock surfaces contain no personal local path fragments;
  and
- the active recipe/generator scripts pass Ruff.

## Phase 11 Boundary

Phase 10R closes with all 27 Table 57 future-managed curves accepted for the
Phase 11 curve handoff. Phase 11 can proceed to model-input table, ForestModel
XML, and Patchworks package work from this locked recipe.

Phase 11 still must explicitly materialize the accepted curves into the
model-contract surface before Patchworks consumes them. Tables 54/55 remain
deferred unless a later public-safe existing/recent AU-code mapping is supplied.
