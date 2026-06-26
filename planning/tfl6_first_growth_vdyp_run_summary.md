# TFL 6 P3.4d AFLB VDYP First-Growth Run Summary

## Purpose

Materialize natural/untreated first-growth curve evidence for the static TFL 6
AU universe by running VDYP only for the VDYP records whose feature IDs match
stands in the AU-assigned AFLB review table.

This is narrower than a full Stage 01a rebuild. The accepted input surface for
this pass was:

- AU assignment: `planning/tfl6_stand_to_au_review.csv`
- VDYP polygon input: `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet`
- VDYP layer input: `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet`

The tracked run driver is
`scripts/run_p3_4_aflb_vdyp_first_growth.py`.

## Run Artifacts

Review artifacts promoted to `planning/`:

- `planning/tfl6_first_growth_au_curves.csv`
- `planning/tfl6_first_growth_au_fit_diagnostics.csv`

Large runtime/audit artifacts remain under ignored runtime output:

- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_yield_timeseries.parquet`
- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_yield_timeseries.csv`
- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_runs.jsonl`
- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_stdout.log`

## Results

- AU-assigned AFLB feature IDs requested: `17,223`
- Feature IDs with VDYP yield evidence: `16,659`
- Stand-level VDYP yield rows generated: `3,220,953`
- AU diagnostics generated: `380`
- AUs with accepted first-growth curves: `276`
- AUs with insufficient source-stand support: `104`
- Sparse-support diagnostic flags: `186`
- Selected accepted curve family: `smoothed_bin_pchip`

## Notes

VDYP output tables used VDYP table/polygon identifiers rather than the source
feature IDs for some batches. The run therefore applied the same order-based
source-ID remap pattern used by the established FEMIC VDYP runner when output
table counts and requested feature counts align closely but output keys do not
match input feature IDs.

The first-growth selector intentionally leaves low-support AUs without accepted
natural curves. Those AUs must either receive a reviewed borrowing/fallback rule
in a later P3.4 QA pass or be carried forward as managed-only / insufficient
support cases, depending on the downstream treatment and runtime contract.
