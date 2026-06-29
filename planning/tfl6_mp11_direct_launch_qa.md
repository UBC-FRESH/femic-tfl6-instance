# P12.4 MP11 Direct Launch QA

This QA record inspects the direct headless launch smoke for the MP11
candidate Patchworks runtime package.

P12.4 does not run scheduling scenarios, publish a release archive, or
replace the accepted Phase 5 teaching/runtime baseline.

## Summary

- generated_at_utc: `2026-06-29T04:39:31+00:00`
- qa_status: `direct_launch_smoke_pass`
- run_id: `tfl6_mp11_candidate_p12_4_launch0`
- raw_returncode: `0`
- returncode: `0`
- terminal_state: `success`
- detected_marker: `[FEMIC headless] saveStage completed`
- trace_save_stage_completed: `True`
- stage_dir: `models/tfl6_patchworks_model_mp11_candidate/analysis/p12_4_launch0`
- saved_file_count: `3359`
- stage_file_count: `3359`
- target_status_rows: `824`
- target_summary_rows: `25544`
- schedule_rows: `0`
- scenario_mode: `none`
- iterations: `0`
- runtime_package_status: `candidate_runtime_package_assembled_pending_launch_smoke`
- stdout_error_count: `0`
- stderr_error_count: `0`
- stdout_warning_count: `0`
- stderr_warning_count: `0`
- scenario_smoke: `not_performed`
- release_qa: `not_performed`

## Saved Stage Inventory

| Child | Files | Bytes |
| --- | ---: | ---: |
| `html` | 34 | 770356 |
| `index-frames.html` | 1 | 810 |
| `index.csv` | 1 | 195 |
| `index.fld` | 1 | 292 |
| `index.html` | 1 | 966 |
| `scenario` | 16 | 2636712 |
| `targets` | 3305 | 21343990 |

## Inspection Result

- Headless launch returned code `0`.
- Trace log includes `[FEMIC headless] saveStage completed`.
- Saved-stage output count matches the headless manifest.
- `scenario/schedule.csv` is header-only, as expected for `iterations=0`.
- No stderr/stdout error, warning, exception, or failure strings were found.

## Boundary

This is direct launch smoke only. Representative base/sensitivity scenario
smoke remains P12.5, and release QA remains Phase 13.
