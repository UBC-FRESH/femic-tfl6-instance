# TFL 6 MP11 Managed-Yield Parameter Library

## Purpose

This P10.2 artifact converts reviewed MP11 growth-and-yield parameter
evidence into a compact public-safe parameter library. It is a curve
rebuild input surface only; it does not generate curves or promote any
row to model-input status.

## Files

- `planning/tfl6_mp11_managed_yield_parameter_library.md`
- `planning/tfl6_mp11_managed_yield_parameter_library.csv`
- `planning/tfl6_mp11_managed_yield_parameter_library.json`

## Source Window

- Source package: `tfl6_mp11_202606_public_pdf`
- Source SHA256: `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Relevant PDF pages: `358-377`
- Relevant Appendix B pages: `112-131 of 183`
- Primary tables: `54-60`

## Status

- Parameter rows: `48`
- Parameter families: `9`
- Curve lanes: `5`
- Model-input status: `not_model_input`

## Parameter Family Counts

- `genetic_gain`: `9`
- `nsr`: `2`
- `per_au_tipsy_inputs`: `3`
- `regeneration_delay`: `1`
- `site_index`: `1`
- `spacing_density`: `1`
- `stocking_density`: `3`
- `utilization`: `8`
- `vraf`: `20`

## Review Status Counts

- `parser_review_required`: `3`
- `reviewed_parameter_candidate`: `45`

## Key Use Boundary

- Tables 54, 55, and 57 are anchored and represented, but their
  multi-page per-AU TIPSY rows are marked
  `requires_p10_5_parser_review` before managed-curve generation.
- Table 56 genetic-gain, Table 58 VRAF, Table 59 NSR, and Table 60
  utilization values are normalized into parameter rows.
- VRAF rows are parameters for harvest-time yield impact review and
  should not be hidden inside base managed yield curves.
- All rows remain `not_model_input` until a later phase explicitly
  promotes them through the Phase 8 evidence-promotion contract.

## Parameter Rows

| record_id | source_table | parameter_family | curve_lane | au_scope | species_or_zone | parameter_name | value | unit | dependency_status | review_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p10_mp11_param_001 | Table 54 | spacing_density | early_managed | Early managed AUs with remaining juvenile spacing treatment areas | all | juvenile_spacing_density_sequence | 1600 to 900 | stems_per_ha | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_002 | Table 54 | genetic_gain | early_managed | Stands established 1961-2000; age 23-62 years | all | genetic_gain_applied | 0 | percent | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_003 | Table 54 | per_au_tipsy_inputs | early_managed | Early managed AU rows E100-E422 | mixed | large_table_row_parse_status | requires_p10_5_parser_review | status | public_table_fragmented | parser_review_required |
| p10_mp11_param_004 | Table 55 | stocking_density | recent_managed | Recently managed stands established 2001-2023; age 1-22 years | all | typical_table_density | 1000 | stems_per_ha | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_005 | Table 55 | genetic_gain | recent_managed | Recently managed stands established 2001-2023; age 1-22 years | Cw/Fd/Hw/Yc | genetic_gain_source | seedlot averages since 2012 | source_description | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_006 | Table 55 | per_au_tipsy_inputs | recent_managed | Recent managed AU rows R100-R422 | mixed | large_table_row_parse_status | requires_p10_5_parser_review | status | public_table_fragmented | parser_review_required |
| p10_mp11_param_007 | Narrative before Table 56 | stocking_density | future_managed | Most future AUs | all | default_planting_density | 1200 | stems_per_ha | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_008 | Narrative before Table 56 | stocking_density | future_managed | Low-productivity sites such as CWHvm1 33/33 and MHmmp22 | all | low_productivity_planting_density | 800 | stems_per_ha | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_009 | Narrative before Table 56 | regeneration_delay | future_managed | Future managed planted stands | all | tipsy_regeneration_delay | 1 | year | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_010 | Table 56 | genetic_gain | future_managed | Future AUs | Cw | future_au_genetic_gain | 21.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_011 | Table 56 | genetic_gain | future_managed | Future AUs | Fd low elevation | future_au_genetic_gain | 16.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_012 | Table 56 | genetic_gain | future_managed | Future AUs | Fd high elevation | future_au_genetic_gain | 11.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_013 | Table 56 | genetic_gain | future_managed | Future AUs | Hw low elevation | future_au_genetic_gain | 1.7 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_014 | Table 56 | genetic_gain | future_managed | Future AUs | Hw high elevation | future_au_genetic_gain | 1.1 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_015 | Table 56 | genetic_gain | future_managed | Future AUs | Yc | future_au_genetic_gain | 10.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_016 | Table 56 | genetic_gain | future_managed | Future AUs | Dr in CWHvm1 | future_au_genetic_gain | 32.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_017 | Table 57 | site_index | future_managed | Future AUs | area_weighted_average | future_au_thlb_site_index | 24.5 | metres | public_text_parameter | reviewed_parameter_candidate |
| p10_mp11_param_018 | Table 57 | per_au_tipsy_inputs | future_managed | Future AU rows Fvh101-Fvm2* | mixed | large_table_row_parse_status | requires_p10_5_parser_review | status | public_table_fragmented | parser_review_required |
| p10_mp11_param_019 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Windy | retention_level | 15 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_020 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Windy | average_vraf | 3.4 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_021 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Windy | percent_of_harvest_area | 30 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_022 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Windy | average_yield_impact_to_apply | 1.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_023 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Basic | retention_level | 15 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_024 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Basic | average_vraf | 3.4 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_025 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Basic | percent_of_harvest_area | 50 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_026 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Enhanced Basic | average_yield_impact_to_apply | 1.7 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_027 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Windy | retention_level | 20 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_028 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Windy | average_vraf | 4.8 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_029 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Windy | percent_of_harvest_area | 40 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_030 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Windy | average_yield_impact_to_apply | 1.9 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_031 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Basic | retention_level | 20 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_032 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Basic | average_vraf | 4.8 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_033 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Basic | percent_of_harvest_area | 60 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_034 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | General Basic | average_yield_impact_to_apply | 2.9 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_035 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Special | retention_level | 25 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_036 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Special | average_vraf | 6.0 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_037 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Special | percent_of_harvest_area | 90 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_038 | Table 58 | vraf | recent_and_future_managed | Western Stewardship and Conservation Plan zones | Special | average_yield_impact_to_apply | 5.4 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_039 | Table 59 | nsr | future_managed | NSR areas assigned to future AUs during initial planning period | all | productive_area | 1167 | ha | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_040 | Table 59 | nsr | future_managed | NSR areas assigned to future AUs during initial planning period | all | thlb_area | 1096 | ha | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_041 | Table 60 | utilization | natural_and_managed | mature_gt_120 | all | minimum_dbh | 17.5 | cm | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_042 | Table 60 | utilization | natural_and_managed | mature_gt_120 | all | stump_height | 30.0 | cm | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_043 | Table 60 | utilization | natural_and_managed | mature_gt_120 | all | top_dib | 10.0 | cm | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_044 | Table 60 | utilization | natural_and_managed | mature_gt_120 | all | firmwood_standard | 50 | percent | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_045 | Table 60 | utilization | natural_and_managed | immature_le_120_and_future_managed | all | minimum_dbh | 12.5 | cm | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_046 | Table 60 | utilization | natural_and_managed | immature_le_120_and_future_managed | all | stump_height | 30.0 | cm | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_047 | Table 60 | utilization | natural_and_managed | immature_le_120_and_future_managed | all | top_dib | 10.0 | cm | public_table_parameter | reviewed_parameter_candidate |
| p10_mp11_param_048 | Table 60 | utilization | natural_and_managed | immature_le_120_and_future_managed | all | firmwood_standard | 50 | percent | public_table_parameter | reviewed_parameter_candidate |
