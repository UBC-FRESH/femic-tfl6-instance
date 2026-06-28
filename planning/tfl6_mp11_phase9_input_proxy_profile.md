# TFL 6 MP11 Phase 9 Inventory And Proxy Input Profile

## Purpose

This P9.3 profile records candidate public inventory fields, public
proxy variables, and overlay-source field summaries needed before an
MP11 public-data THLB overlay recipe can be implemented. It does not
accept final overlay rules and does not generate THLB outputs.

## Files

- `planning/tfl6_mp11_phase9_input_proxy_profile.md`
- `planning/tfl6_mp11_phase9_input_proxy_profile.csv`
- `planning/tfl6_mp11_phase9_input_proxy_profile.json`

## Status Counts

- Rows: `51`
- Candidate family counts: `{'field_distribution': 30, 'forest_status': 2, 'hydrology': 3, 'inventory_attribute_join': 2, 'join_qa': 2, 'legal_reserves': 4, 'operability_proxy': 3, 'productivity': 2, 'qa_signal': 1, 'roads': 1, 'species': 1}`
- Phase 9 decision counts: `{'candidate_for_p9_3_review': 3, 'candidate_for_p9_4_review': 5, 'profile_for_p9_3_review': 40, 'qa_only': 3}`

## Candidate Profile Table

| Candidate | Family | Source | Rows | Area ha | Length km | Decision |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `vri_bclcs_level1_nonforest_candidate` | forest_status | `vri_2025_r1_tfl6` | 1,288 | 10,693.446 |  | `candidate_for_p9_4_review` |
| `vri_bclcs_level2_non_treed_water_null_candidate` | forest_status | `vri_2025_r1_tfl6` | 2,195 | 20,209.542 |  | `candidate_for_p9_4_review` |
| `vri_explicit_nonproductive_candidate` | productivity | `vri_2025_r1_tfl6` | 965 | 5,850.363 |  | `candidate_for_p9_4_review` |
| `vri_site_index_lt5_candidate` | productivity | `vri_2025_r1_tfl6` | 473 | 4,608.853 |  | `candidate_for_p9_4_review` |
| `vri_deciduous_leading_candidate` | species | `vri_2025_r1_tfl6` | 1,007 | 4,395.795 |  | `candidate_for_p9_4_review` |
| `vri_low_height_operability_candidate` | operability_proxy | `vri_2025_r1_tfl6` | 9,023 | 86,027.920 |  | `candidate_for_p9_3_review` |
| `vri_low_volume_operability_candidate` | operability_proxy | `vri_2025_r1_tfl6` | 3,883 | 32,340.149 |  | `candidate_for_p9_3_review` |
| `vri_hembal_height3_operability_candidate` | operability_proxy | `vri_2025_r1_tfl6` | 3,277 | 27,971.218 |  | `candidate_for_p9_3_review` |
| `vri_for_mgmt_land_base_no_qa_signal` | qa_signal | `vri_2025_r1_tfl6` | 2,437 | 18,652.798 |  | `qa_only` |
| `vri_2025_r1_tfl6_bclcs_level_1_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vri_2025_r1_tfl6_bclcs_level_2_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vri_2025_r1_tfl6_non_productive_descriptor_cd_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vri_2025_r1_tfl6_non_productive_cd_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vri_2025_r1_tfl6_species_cd_1_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vri_2025_r1_tfl6_proj_height_class_cd_1_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vri_2025_r1_tfl6_crown_closure_class_cd_top_values` | field_distribution | `vri_2025_r1_tfl6` | 26,959 |  |  | `profile_for_p9_3_review` |
| `vdyp7_2025_poly_tfl6_table_schema_summary` | inventory_attribute_join | `vdyp7_2025_poly_tfl6` | 26,833 |  |  | `profile_for_p9_3_review` |
| `vdyp7_2025_poly_tfl6_feature_id_uniqueness` | join_qa | `vdyp7_2025_poly_tfl6` | 26,833 |  |  | `qa_only` |
| `vdyp7_2025_layer_tfl6_table_schema_summary` | inventory_attribute_join | `vdyp7_2025_layer_tfl6` | 25,585 |  |  | `profile_for_p9_3_review` |
| `vdyp7_2025_layer_tfl6_feature_id_uniqueness` | join_qa | `vdyp7_2025_layer_tfl6` | 25,356 |  |  | `qa_only` |
| `dra_roads_tfl6_geometry_summary` | roads | `dra_roads_tfl6` | 10,706 |  | 4,255.863 | `profile_for_p9_3_review` |
| `fwa_stream_networks_tfl6_STREAM_ORDER_top_values` | field_distribution | `fwa_stream_networks_tfl6` | 12,078 |  |  | `profile_for_p9_3_review` |
| `fwa_stream_networks_tfl6_STREAM_MAGNITUDE_top_values` | field_distribution | `fwa_stream_networks_tfl6` | 12,078 |  |  | `profile_for_p9_3_review` |
| `fwa_stream_networks_tfl6_WATERSHED_GROUP_CODE_top_values` | field_distribution | `fwa_stream_networks_tfl6` | 12,078 |  |  | `profile_for_p9_3_review` |
| `fwa_stream_networks_tfl6_GNIS_NAME_top_values` | field_distribution | `fwa_stream_networks_tfl6` | 12,078 |  |  | `profile_for_p9_3_review` |
| `fwa_stream_networks_tfl6_geometry_summary` | hydrology | `fwa_stream_networks_tfl6` | 12,078 |  | 4,748.715 | `profile_for_p9_3_review` |
| `fwa_lakes_tfl6_WATERBODY_TYPE_top_values` | field_distribution | `fwa_lakes_tfl6` | 599 |  |  | `profile_for_p9_3_review` |
| `fwa_lakes_tfl6_WATERSHED_GROUP_CODE_top_values` | field_distribution | `fwa_lakes_tfl6` | 599 |  |  | `profile_for_p9_3_review` |
| `fwa_lakes_tfl6_geometry_summary` | hydrology | `fwa_lakes_tfl6` | 599 | 3,243.849 |  | `profile_for_p9_3_review` |
| `fwa_wetlands_tfl6_WATERSHED_GROUP_CODE_top_values` | field_distribution | `fwa_wetlands_tfl6` | 572 |  |  | `profile_for_p9_3_review` |
| `fwa_wetlands_tfl6_geometry_summary` | hydrology | `fwa_wetlands_tfl6` | 572 | 982.424 |  | `profile_for_p9_3_review` |
| `ogma_legal_current_tfl6_OGMA_TYPE_top_values` | field_distribution | `ogma_legal_current_tfl6` | 165 |  |  | `profile_for_p9_3_review` |
| `ogma_legal_current_tfl6_OGMA_PRIMARY_REASON_top_values` | field_distribution | `ogma_legal_current_tfl6` | 165 |  |  | `profile_for_p9_3_review` |
| `ogma_legal_current_tfl6_LEGALIZATION_FRPA_DATE_top_values` | field_distribution | `ogma_legal_current_tfl6` | 165 |  |  | `profile_for_p9_3_review` |
| `ogma_legal_current_tfl6_LAST_AMENDMENT_DATE_top_values` | field_distribution | `ogma_legal_current_tfl6` | 165 |  |  | `profile_for_p9_3_review` |
| `ogma_legal_current_tfl6_geometry_summary` | legal_reserves | `ogma_legal_current_tfl6` | 165 | 16,131.032 |  | `profile_for_p9_3_review` |
| `ogma_non_legal_current_tfl6_OGMA_TYPE_top_values` | field_distribution | `ogma_non_legal_current_tfl6` | 2 |  |  | `profile_for_p9_3_review` |
| `ogma_non_legal_current_tfl6_OGMA_PRIMARY_REASON_top_values` | field_distribution | `ogma_non_legal_current_tfl6` | 2 |  |  | `profile_for_p9_3_review` |
| `ogma_non_legal_current_tfl6_ORIGINAL_DECISION_DATE_top_values` | field_distribution | `ogma_non_legal_current_tfl6` | 2 |  |  | `profile_for_p9_3_review` |
| `ogma_non_legal_current_tfl6_LAST_AMENDMENT_DATE_top_values` | field_distribution | `ogma_non_legal_current_tfl6` | 2 |  |  | `profile_for_p9_3_review` |
| `ogma_non_legal_current_tfl6_geometry_summary` | legal_reserves | `ogma_non_legal_current_tfl6` | 2 | 0.687 |  | `profile_for_p9_3_review` |
| `wha_approved_tfl6_TAG_top_values` | field_distribution | `wha_approved_tfl6` | 45 |  |  | `profile_for_p9_3_review` |
| `wha_approved_tfl6_COMMON_SPECIES_NAME_top_values` | field_distribution | `wha_approved_tfl6` | 45 |  |  | `profile_for_p9_3_review` |
| `wha_approved_tfl6_APPROVAL_DATE_top_values` | field_distribution | `wha_approved_tfl6` | 45 |  |  | `profile_for_p9_3_review` |
| `wha_approved_tfl6_FEATURE_AREA_SQM_top_values` | field_distribution | `wha_approved_tfl6` | 45 |  |  | `profile_for_p9_3_review` |
| `wha_approved_tfl6_geometry_summary` | legal_reserves | `wha_approved_tfl6` | 45 | 2,942.796 |  | `profile_for_p9_3_review` |
| `uwr_approved_tfl6_UWR_NUMBER_top_values` | field_distribution | `uwr_approved_tfl6` | 22 |  |  | `profile_for_p9_3_review` |
| `uwr_approved_tfl6_SPECIES_1_top_values` | field_distribution | `uwr_approved_tfl6` | 22 |  |  | `profile_for_p9_3_review` |
| `uwr_approved_tfl6_APPROVAL_DATE_top_values` | field_distribution | `uwr_approved_tfl6` | 22 |  |  | `profile_for_p9_3_review` |
| `uwr_approved_tfl6_FEATURE_AREA_SQM_top_values` | field_distribution | `uwr_approved_tfl6` | 22 |  |  | `profile_for_p9_3_review` |
| `uwr_approved_tfl6_geometry_summary` | legal_reserves | `uwr_approved_tfl6` | 22 | 2,365.514 |  | `profile_for_p9_3_review` |

## Key Findings

- R1/VRI contains candidate signals for non-forest, explicit
  non-productive, low-site, deciduous-leading, low-height, low-volume,
  and hemlock/balsam height-class-three proxy review.
- VDYP polygon/layer parquet tables are readable and should remain join
  attribute sources; R1 remains the complete area accounting surface.
- Roads, hydrology, legal reserve, and recreation layers have profile
  summaries, but final filters, buffers, and overlay order remain
  P9.4 decisions.
- DEM/slope and shoreline are still unresolved source/proxy gaps from
  P9.2; no slope or shoreline proxy is accepted by this profile.

## Use Boundary

Rows in this profile are `candidate_profile_only` or `qa_only`. They
are not accepted model inputs and do not authorize final THLB overlay
execution without the P9.4 recipe review.
