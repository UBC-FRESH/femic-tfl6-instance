# TFL 6 MP11 Managed-Curve Diagnostics

## Purpose

This P10.5 artifact records the managed-curve status after P10.2 and
P10.3. It does not generate MP11 managed curves because Tables 54, 55,
and 57 still require reviewed per-AU TIPSY row parsing. Existing Phase 5
MP10-derived managed curves are retained as comparison baselines.

## Files

- `planning/tfl6_mp11_managed_curve_diagnostics.md`
- `planning/tfl6_mp11_managed_curve_diagnostics.csv`
- `planning/tfl6_mp11_managed_curve_diagnostics.json`

## Status

- Diagnostic rows: `1152`
- Canonical AU count: `384`
- Selected top-90 managed lane rows: `231`
- Phase 5 comparison curve rows available: `231`
- MP11 managed curve rows generated: `0`
- Model-input status: `not_model_input`

## MP11 Generation Status Counts

- `blocked_pending_per_au_table_parser`: `1152`

## Review Status Counts

- `mp11_parser_blocked_no_phase5_comparison`: `921`
- `mp11_parser_blocked_with_phase5_comparison`: `231`

## Use Boundary

- MP11 managed curves remain blocked until Tables 54, 55, and 57 have
  reviewed per-AU row parsers and QA outputs.
- Existing Phase 5 managed curves remain comparison/fallback evidence,
  not MP11-equivalent curves.
- VRAF parameters from P10.2 are not hidden inside base managed curves;
  they require later harvest-time implementation review.
- All rows remain `not_model_input` until Phase 11 promotion review.

## High-Area Selected Managed Rows

| au_id | curve_lane | area_ha | mp11_status | phase5_match | max_treated_volume | ratio_to_natural |
| --- | --- | ---: | --- | --- | ---: | ---: |
| `cwhvm1_hw_cw_m` | `early_managed` | 14576.474 | `blocked_pending_per_au_table_parser` | `high` | 1831.500 | 1.745 |
| `cwhvm1_hw_cw_m` | `future_managed` | 14576.474 | `blocked_pending_per_au_table_parser` | `high` | 1873.100 | 1.785 |
| `cwhvm1_hw_cw_m` | `recent_managed` | 14576.474 | `blocked_pending_per_au_table_parser` | `medium` | 1315.900 | 1.254 |
| `cwhvm1_hw_ba_m` | `early_managed` | 13083.871 | `blocked_pending_per_au_table_parser` | `high` | 1958.900 | 1.805 |
| `cwhvm1_hw_ba_m` | `future_managed` | 13083.871 | `blocked_pending_per_au_table_parser` | `high` | 1977.600 | 1.822 |
| `cwhvm1_hw_ba_m` | `recent_managed` | 13083.871 | `blocked_pending_per_au_table_parser` | `medium` | 1330.600 | 1.226 |
| `cwhvm1_hw_cw_l` | `early_managed` | 7117.880 | `blocked_pending_per_au_table_parser` | `low` | 1831.500 | 2.197 |
| `cwhvm1_hw_cw_l` | `future_managed` | 7117.880 | `blocked_pending_per_au_table_parser` | `low` | 1873.100 | 2.247 |
| `cwhvm1_hw_cw_l` | `recent_managed` | 7117.880 | `blocked_pending_per_au_table_parser` | `high` | 1315.900 | 1.579 |
| `cwhvm1_hw_ba_h` | `early_managed` | 6336.709 | `blocked_pending_per_au_table_parser` | `high` | 1958.900 | 1.717 |
| `cwhvm1_hw_ba_h` | `future_managed` | 6336.709 | `blocked_pending_per_au_table_parser` | `high` | 1977.600 | 1.734 |
| `cwhvm1_hw_ba_h` | `recent_managed` | 6336.709 | `blocked_pending_per_au_table_parser` | `high` | 2082.200 | 1.826 |
| `cwhvm1_hw_ba_l` | `early_managed` | 6328.041 | `blocked_pending_per_au_table_parser` | `high` | 1359.800 | 1.516 |
| `cwhvm1_hw_ba_l` | `future_managed` | 6328.041 | `blocked_pending_per_au_table_parser` | `high` | 1340.400 | 1.495 |
| `cwhvm1_hw_ba_l` | `recent_managed` | 6328.041 | `blocked_pending_per_au_table_parser` | `high` | 1330.600 | 1.484 |
| `cwhvm1_cw_hw_h` | `early_managed` | 6154.404 | `blocked_pending_per_au_table_parser` | `high` | 1631.500 | 1.729 |
| `cwhvm1_cw_hw_h` | `future_managed` | 6154.404 | `blocked_pending_per_au_table_parser` | `medium` | 1091.900 | 1.157 |
| `cwhvm1_cw_hw_h` | `recent_managed` | 6154.404 | `blocked_pending_per_au_table_parser` | `high` | 1634.100 | 1.732 |
| `cwhvm1_cw_hw_l` | `early_managed` | 6107.944 | `blocked_pending_per_au_table_parser` | `medium` | 1127.000 | 1.439 |
| `cwhvm1_cw_hw_l` | `future_managed` | 6107.944 | `blocked_pending_per_au_table_parser` | `medium` | 1091.900 | 1.394 |
| `cwhvm1_cw_hw_l` | `recent_managed` | 6107.944 | `blocked_pending_per_au_table_parser` | `low` | 1634.100 | 2.087 |
| `cwhvm1_hw_m` | `early_managed` | 4138.939 | `blocked_pending_per_au_table_parser` | `high` | 1963.200 | 2.041 |
| `cwhvm1_hw_m` | `future_managed` | 4138.939 | `blocked_pending_per_au_table_parser` | `medium` | 1977.600 | 2.056 |
| `cwhvm1_hw_m` | `recent_managed` | 4138.939 | `blocked_pending_per_au_table_parser` | `medium` | 1330.600 | 1.384 |
| `cwhvm1_hw_ss_l` | `early_managed` | 4135.639 | `blocked_pending_per_au_table_parser` | `high` | 1321.400 | 1.250 |
