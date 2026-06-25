# TFL 6 R1 / VDYP7 Field Profile

## Purpose

This note starts P2.2 by profiling the accepted 2025 TFL 6 R1 and VDYP7 inputs
for later THLB field-mapping review.

Governing issue: `#22`.

This is a schema/profile slice only. It does not fetch source layers, create
recipe YAML, execute THLB netdown logic, generate model inputs, derive DEM or
slope products, or build Patchworks runtime artifacts.

## Accepted Inputs Profiled

| Source ID | Path | Role |
| --- | --- | --- |
| `vri_2025_r1_tfl6` | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` | accepted current-AOI R1 geometry and area surface |
| `vdyp7_2025_poly_tfl6` | `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet` | accepted current-AOI VDYP7 polygon attribute table |
| `vdyp7_2025_layer_tfl6` | `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` | accepted current-AOI VDYP7 layer/species table |

Area summaries below use geometry-derived `area_ha_calc` from the clipped R1
polygon surface.

## Join Integrity

`feature_id` is present in all three accepted inputs and remains the preferred
join key for P2.2 review.

| Check | Result |
| --- | ---: |
| R1 rows | `26959` |
| R1 total area | `217042.719 ha` |
| R1 unique `feature_id` values | `26959` |
| VDYP7 polygon rows | `26833` |
| VDYP7 polygon unique `feature_id` values | `26833` |
| VDYP7 layer rows | `25585` |
| VDYP7 layer unique `feature_id` values | `25356` |
| VDYP7 polygon IDs missing from R1 | `0` |
| VDYP7 layer IDs missing from R1 | `0` |
| R1 IDs missing from VDYP7 polygon | `126` |
| R1 IDs missing from VDYP7 layer | `1603` |
| VDYP7 polygon IDs missing from VDYP7 layer | `1477` |
| VDYP7 layer IDs missing from VDYP7 polygon | `0` |

Interpretation:

- R1 is the complete current-AOI area surface for THLB accounting.
- VDYP7 polygon and layer tables are subsets of the R1 universe.
- The missing VDYP7 rows must be reviewed before recipe execution. The first
  hypothesis is that many missing rows are non-forest, non-vegetated,
  non-productive, or otherwise outside VDYP yield scope, but that has not yet
  been accepted as executable logic.

## R1 Candidate Field Summaries

### Forest Management Land Base Indicator

| `for_mgmt_land_base_ind` | Rows | Area |
| --- | ---: | ---: |
| `Y` | `24522` | `198389.921 ha` |
| `N` | `2437` | `18652.798 ha` |

This field is a strong review candidate for the first non-forest and
non-productive screens, but it should not be treated as a complete MP10 Table 4
translation by itself.

### BCLCS Levels

| Field | Dominant values by area |
| --- | --- |
| `bclcs_level_1` | `V` `206349.273 ha`; `N` `9283.337 ha`; `U` `1410.109 ha` |
| `bclcs_level_2` | `T` `191168.597 ha`; `N` `15180.676 ha`; `L` `5664.579 ha`; `W` `3618.758 ha`; null `1410.109 ha` |
| `bclcs_level_3` | `U` `211616.731 ha`; `W` `4013.153 ha`; null `1410.109 ha`; `A` `2.726 ha` |
| `bclcs_level_4` | `TC` `186871.818 ha`; `SL` `8587.608 ha`; null `8075.842 ha`; `HE` `4935.585 ha`; `TB` `3267.802 ha`; `EL` `2560.295 ha`; `TM` `2293.630 ha` |
| `bclcs_level_5` | `DE` `96421.042 ha`; `OP` `72681.363 ha`; `SP` `37244.091 ha`; null `6013.183 ha`; `ES` `2451.354 ha`; `LA` `1540.116 ha`; `RI` `493.379 ha` |

BCLCS is the first explicit candidate for MP10 non-forest translation. P2.2b
must decide which combinations map to non-forest, water/wetland, brush, rock,
alpine, sparse, and potentially low-productivity categories.

### Non-Productive Fields

| Field | Dominant values by area |
| --- | --- |
| `non_productive_descriptor_cd` | null `213800.885 ha`; `L` `1692.418 ha`; `NP` `1162.117 ha`; `R` `135.154 ha`; `C` `126.765 ha`; `A` `116.550 ha` |
| `non_productive_cd` | null `211447.591 ha`; `15` `2072.155 ha`; `12` `2043.385 ha`; `35` `678.636 ha`; `25` `372.113 ha`; `11` `223.927 ha`; `42` `127.935 ha` |

These fields directly support non-productive review, but their standalone area
is smaller than the adjusted MP10 non-productive benchmark. They likely need to
be combined with BCLCS, land-cover, site/productivity, and yield fields.

### Land Cover and Non-Vegetated Signals

| Field | Dominant values by area |
| --- | --- |
| `land_cover_class_cd_1` | `TC` `120517.391 ha`; null `81164.517 ha`; `HE` `4909.442 ha`; `SL` `3340.087 ha`; `TB` `2492.458 ha`; `TM` `1607.272 ha`; `LA` `1428.437 ha` |
| `non_veg_cover_type_1` | null `184173.653 ha`; `RZ` `17883.346 ha`; `BR` `8426.913 ha`; `LA` `2717.957 ha`; `RI` `1168.277 ha`; `ES` `990.272 ha` |

These fields are important candidates for translating MP10 non-forest and
non-productive classes. P2.2b should compare them against BCLCS and the
`for_mgmt_land_base_ind` split before accepting any one field as authoritative.

## Species and Deciduous-Leading Candidates

Top `species_cd_1` values by area:

| `species_cd_1` | Area |
| --- | ---: |
| `HW` | `132289.102 ha` |
| `CW` | `35056.931 ha` |
| null | `17078.826 ha` |
| `YC` | `9419.022 ha` |
| `HM` | `6963.222 ha` |
| `DR` | `4381.520 ha` |
| `BA` | `3780.131 ha` |
| `SS` | `3600.092 ha` |
| `FDC` | `3226.480 ha` |
| `FD` | `771.171 ha` |

Derived first-pass lead-species grouping:

| Group | Rows | Area |
| --- | ---: | ---: |
| conifer candidate | `23840` | `195546.480 ha` |
| null lead species | `2109` | `17078.826 ha` |
| deciduous candidate | `1007` | `4395.795 ha` |
| other/unknown | `3` | `21.618 ha` |

The deciduous-leading candidate area is larger than the scaled MP10 benchmark
for the deciduous-leading deduction. That is not necessarily a mismatch because
the benchmark is a marginal netdown after earlier overlaps, while this profile
is gross current-AOI area. P2.2b should keep marginal-vs-gross accounting
explicit when proposing a deciduous-leading recipe rule.

## BEC Candidate Fields

| Field | Dominant values by area |
| --- | --- |
| `bec_zone_code` | `CWH` `206749.038 ha`; `MH` `10205.488 ha`; `CMA` `88.193 ha` |
| `bec_subzone` | `vm` `192286.056 ha`; `vh` `14462.982 ha`; `mm` `10205.488 ha`; `unp` `88.193 ha` |
| `bec_variant` | `1` `182460.302 ha`; `2` `34494.223 ha`; null `88.193 ha` |

R1 carries BEC-style attribution and the materialized BEC polygon layer also
exists for review. P2.2b should decide whether recipe inputs use R1 attributes,
the materialized BEC overlay, or both for reporting/validation consistency.

## Numeric Candidate Fields

| Field | Non-null rows | Minimum | Median | Maximum |
| --- | ---: | ---: | ---: | ---: |
| `site_index` | `24960` | `0.000` | `20.900` | `58.400` |
| `est_site_index` | `17330` | `0.000` | `22.000` | `51.000` |
| `proj_height_1` | `24808` | `0.000` | `25.500` | `91.800` |
| `proj_age_1` | `24808` | `1.000` | `70.000` | `825.000` |
| `crown_closure` | `24326` | `1.000` | `55.000` | `99.000` |
| `live_stand_volume_125` | `20999` | `0.116` | `374.829` | `1815.359` |
| `live_stand_volume_175` | `20999` | `0.079` | `369.572` | `1815.359` |
| `basal_area` | `22267` | `0.000` | `52.095` | `141.816` |
| `vri_live_stems_per_ha` | `24840` | `0.000` | `560.000` | `20760.000` |
| `shrub_height` | `7396` | `0.100` | `1.000` | `10.000` |
| `shrub_crown_closure` | `7396` | `2.000` | `10.000` | `100.000` |

These fields are candidates for low-productivity, open-stand, marginal
operability, and student sensitivity logic. They are not yet accepted as
thresholds.

## Operability-Proxy Candidate Signals

P2.1a keeps operability as a proxy/sensitivity design lane rather than a locked
source-layer deduction. The accepted R1/VDYP7 inputs still provide useful
candidate signals for later proxy work:

| Candidate surface | Relevant fields | Review use |
| --- | --- | --- |
| Height/open stand | `proj_height_class_cd_1`, `proj_height_1`, `bclcs_level_4`, `bclcs_level_5` | screen immature, open, sparse, or low-height stands |
| Productivity/yield | `site_index`, `est_site_index`, `yield_factor`, `live_stand_volume_125`, `live_stand_volume_175` | test economic-access and marginal-volume assumptions |
| Species group | `species_cd_1` and VDYP layer species fields | distinguish hemlock/cypress/fir/deciduous cases where yarding economics differ |
| Stand density | `crown_closure`, `crown_closure_class_cd`, `basal_area`, `vri_live_stems_per_ha` | identify understocked or low-density stands |
| Status/openings | `free_to_grow_ind` plus opening/disturbance fields if used later | avoid treating recent/regenerating stands as permanently inoperable |
| Slope | future DEM-derived slope statistics | later issue; not part of this profile slice |

## P2.2a Status

P2.2a is complete as a schema and join-coverage profile:

- accepted inputs, row counts, area totals, and join coverage are recorded;
- first-pass candidate field surfaces are identified for P2.2b mapping review;
- no mapping has been accepted as executable recipe logic; and
- no THLB recipe, model-input, DEM/slope, or Patchworks work has started.

The next bounded P2.2 slice is to draft candidate field mappings and gross-area
diagnostics for non-forest, non-productive, deciduous-leading, productivity,
and operability-proxy inputs, keeping marginal netdown acceptance for later
recipe-readiness review.
