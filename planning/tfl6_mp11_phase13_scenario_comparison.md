# TFL 6 MP11 Phase 13 Scenario Comparison

This note converts the Phase 13 candidate-runtime positioning into tracked comparison tables. It separates MP11 comparison targets, tracked P12.5 runtime smoke output, and maintainer interactive context so later release QA does not confuse screenshot evidence with reproducible model output.

## Summary

- comparison_status: `scenario_comparison_tables_built`
- parent_issue: `#70`
- child_issue: `#127`
- mp11_base_case_m3_per_year: `1061600.0`
- mp11_adjusted_lrsy_m3_per_year: `1182900.0`
- candidate_maintainer_context_m3_per_year: `1150000.0`
- candidate_vs_mp11_base_context_delta_m3_per_year: `88400.0`
- candidate_vs_mp11_base_context_pct: `8.33`
- candidate_runtime_smoke_mean_m3_per_year: `1407237.42`
- runtime_smoke_run_id: `tfl6_mp11_candidate_p12_5_harvest_smoke200k`
- runtime_smoke_iterations: `200000`
- runtime_smoke_schedule_rows: `76726`
- release_qa: `not_performed`
- release_decision: `pending_p13_5`

## Comparison Rows

| ID | Label | Value | Evidence | Role | Caveat |
| --- | --- | ---: | --- | --- | --- |
| `mp11_base_case` | WFP MP11 base case | `1061600.00` | `tracked_mp11_table_or_text` | `comparison_target` | Accepted as MP11 comparison evidence only; not model input. |
| `mp11_figure2_recovered_mean` | Reviewed Figure 2 recovered mean | `1056896.06` | `reviewed_mp11_figure_extraction` | `comparison_context` | Accepted for comparison planning; do not use as model input. |
| `mp11_adjusted_lrsy` | MP11 adjusted LRSY context | `1182900.00` | `tracked_mp11_table_or_text` | `context` | LRSY is not the base-case AAC/harvest level. |
| `candidate_p12_5_runtime_mean` | P12.5 tracked runtime smoke mean annual harvest | `1407237.42` | `tracked_runtime_output` | `runtime_smoke_output` | P12.5 used a high minimum harvested-volume smoke target and did not include the maintainer's maintain-initial-growing-stock target. |
| `candidate_p12_5_runtime_min` | P12.5 tracked runtime smoke minimum annual harvest | `1376196.00` | `tracked_runtime_output` | `runtime_smoke_output` | Period-level minimum across nonzero P12.5 smoke periods. |
| `candidate_p12_5_runtime_max` | P12.5 tracked runtime smoke maximum annual harvest | `1462762.40` | `tracked_runtime_output` | `runtime_smoke_output` | Period-level maximum across nonzero P12.5 smoke periods. |
| `candidate_p12_5_runtime_final` | P12.5 tracked runtime smoke final-period annual harvest | `1410478.40` | `tracked_runtime_output` | `runtime_smoke_output` | Final period is a smoke-run endpoint, not a release target. |
| `candidate_maintainer_interactive_context` | Maintainer interactive basic scenario context | `1150000.00` | `maintainer_context` | `context_not_release_evidence` | Approximate screenshot/context value; no tracked exported scenario table yet. |

## Period Table

`planning/tfl6_mp11_phase13_scenario_period_comparison.csv` records each P12.5 non-release smoke period against the MP11 base-case anchor. Period `0` is retained for completeness but should not be used as a harvest-flow comparison value.

## Interpretation

The maintainer interactive context value of approximately `1.15 million m3/year` is about `8.33%` above the MP11 base-case anchor. That is plausible given the candidate runtime's slightly larger public-data THLB scaffold and incomplete WFP constraint coverage, but it is not yet reproducible release evidence.

The P12.5 tracked runtime smoke output is intentionally separated from the maintainer interactive value. It proves runtime scheduling and target behavior from tracked saved-stage outputs, but it used a high harvested-volume minimum and was not the same basic scenario shown in the maintainer screenshot.

## Caveats

- P12.5 tracked runtime output is a scenario smoke run, not the maintainer interactive basic base scenario.
- The maintainer interactive value is context only until a reproducible export is tracked.
- MP11 adjusted LRSY is context, not the MP11 base-case harvest level.
- No release, AAC, Phase 5 replacement, or WFP-equivalence decision is made by P13.1b.
