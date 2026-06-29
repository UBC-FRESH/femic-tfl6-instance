# P12.2 MP11 Matrix Builder Track QA

This QA record inspects the MP11 candidate Matrix Builder tracks generated
from the Phase 11 candidate ForestModel XML and fragments.

P12.2 does not assemble the Patchworks runtime package, run Patchworks
direct launch smoke, run scenarios, or publish a release archive.

## Summary

- generated_at_utc: `2026-06-29T04:22:20+00:00`
- qa_status: `matrix_builder_tracks_generated_inspection_pass`
- run_id: `tfl6_mp11_candidate_p12_2_matrix_build`
- matrix_builder_returncode: `0`
- matrix_builder_raw_returncode: `1`
- expected_track_files_present: `True`
- track_file_count: `13`
- features_rows: `86574`
- accounts_rows: `823`
- protoaccounts_rows: `823`
- accounts_proto_equal: `True`
- products_rows: `26085`
- curves_rows: `1004368`
- groups_rows: `24879`
- strata_rows: `28858`
- treatments_rows: `17390`
- blocks_rows: `47218`
- messages_rows: `0`
- block_area_ha: `191168.565448`
- phase11_fragment_area_ha: `191168.566447`
- block_fragment_area_delta_ha: `-0.000999`
- manifest_failures_count: `0`
- manifest_warnings_count: `1`
- generic_warning_only: `True`
- stdout_error_count: `0`
- stderr_error_count: `0`
- runtime_bundle_generation: `not_performed`
- direct_launch_smoke: `not_performed`
- scenario_smoke: `not_performed`

## Track Files

| File | Rows | Key Counts |
| --- | ---: | --- |
| `features.csv` | 86574 | track_nunique=14429, label_nunique=820, curve_nunique=10491, managed_label_rows=28858, harvested_volume_rows=0 |
| `protoaccounts.csv` | 823 | account_nunique=823, attribute_nunique=823, group_nunique=3, area_account_rows=818, harvested_volume_account_rows=1 |
| `accounts.csv` | 823 | account_nunique=823, attribute_nunique=823, group_nunique=3, area_account_rows=818, harvested_volume_account_rows=1 |
| `products.csv` | 26085 | track_nunique=8695, label_nunique=3, treatment_nunique=1, curve_nunique=4842, managed_label_rows=26085, harvested_volume_rows=8695 |
| `curves.csv` | 1004368 | curve_nunique=15333 |
| `groups.csv` | 24879 | group_nunique=1, block_nunique=24879 |
| `strata.csv` | 28858 | track_nunique=14429 |
| `treatments.csv` | 17390 | track_nunique=8695, treatment_nunique=1, curve_nunique=0 |
| `blocks.csv` | 47218 | track_nunique=11277, block_nunique=24879 |
| `tracknames.csv` | 14429 | track_nunique=14429, strata_nunique=14429 |
| `packages.csv` | 0 | track_nunique=0, treatment_nunique=0 |
| `packageSequences.csv` | 0 | treatment_nunique=0 |
| `messages.csv` | 0 |  |

## Inspection Result

- Matrix Builder generated all expected track CSV files.
- `accounts.csv` and `protoaccounts.csv` are identical after FEMIC account sync.
- `messages.csv` is header-only.
- `packages.csv` and `packageSequences.csv` are header-only, consistent with
  the current candidate scaffold having no package-sequence treatments.
- Track block area is within rounding tolerance of the Phase 11 fragment area.
- The only recorded Matrix Builder warning text is the generic Patchworks
  completion prompt to review warnings and exit.

## Boundary

This is a candidate Matrix Builder track set. Runtime assembly, direct
launch smoke, scenario smoke, and release QA remain downstream Phase 12
and Phase 13 work.
