# TFL 6 TIPSY Parameter Crosswalk Review

## Purpose

This note completes the P3.4c planning crosswalk from the refined static TFL 6
AU universe to reviewed MP10 Tables 27, 28, and 29 TIPSY parameter rows. It is a
review surface for curve generation, not executable BatchTIPSY configuration.

This slice does not generate curves, write `data/model_input_bundle`, emit
ForestModel XML, run Matrix Builder, or assemble a Patchworks runtime package.

## Inputs

| Input | Path |
| --- | --- |
| Static AU universe | `planning/tfl6_static_au_universe.csv` |
| Stand-to-AU review table | `planning/tfl6_stand_to_au_review.csv` |
| MP10 TIPSY parameter library | `planning/tfl6_mp10_tipsy_parameter_library.csv` |

## Matching Method

Each static AU is matched separately to three MP10 parameter lanes:

| Curve lane | MP10 source table | Use |
| --- | --- | --- |
| `existing_managed_11_50` | `mp10_table_27` | existing managed stands aged 11-50 |
| `existing_managed_1_10` | `mp10_table_28` | existing managed stands aged 1-10 |
| `future_managed` | `mp10_table_29` | future managed/regenerated stands |

AU species percentages are area-weighted from `planning/tfl6_stand_to_au_review.csv`
and collapsed into MP10 species buckets: `ba`, `cw`, `cy`, `fd`, `hw`, `ss`, and
`other`. Matching uses species-share L1 distance as the primary signal and
weighted MP10 SI difference as a secondary signal. The score is:

`species_l1_pct + 2 * capped_si_abs_diff + 10 if dominant species bucket differs`

Confidence classes are review aids, not executable acceptance flags. Low and
fallback rows must be reviewed before BatchTIPSY curve generation.

## Outputs

| Output | Path |
| --- | --- |
| Crosswalk CSV | `planning/tfl6_tipsy_parameter_crosswalk.csv` |
| Crosswalk JSON manifest | `planning/tfl6_tipsy_parameter_crosswalk.json` |
| Review note | `planning/tfl6_tipsy_parameter_crosswalk.md` |

## Counts

| Metric | Value |
| --- | ---: |
| Static AU count | `384` |
| Selected top-area AU count | `77` |
| Curve lanes per AU | `3` |
| Crosswalk rows | `1152` |

## Confidence Counts: All AUs

| curve_lane             |   fallback_review_required |   high |   low |   medium |
|:-----------------------|---------------------------:|-------:|------:|---------:|
| existing_managed_11_50 |                        104 |     74 |    69 |      137 |
| existing_managed_1_10  |                        132 |     37 |    86 |      129 |
| future_managed         |                        134 |     30 |   103 |      117 |

## Confidence Counts: Selected Top-Area AUs

| curve_lane             |   fallback_review_required |   high |   low |   medium |
|:-----------------------|---------------------------:|-------:|------:|---------:|
| existing_managed_11_50 |                         12 |     34 |     8 |       23 |
| existing_managed_1_10  |                         11 |     19 |    15 |       32 |
| future_managed         |                         11 |     11 |    19 |       36 |

## Largest Selected Future-Managed Matches

| au_id           | stratum_code   | si_class   |   area_ha |   mean_si | matched_legacy_au_code   | matched_legacy_au_key   | match_confidence         |   species_l1_pct |   mp10_weighted_si |   si_abs_diff | fallback_or_review_note                                                                             |
|:----------------|:---------------|:-----------|----------:|----------:|:-------------------------|:------------------------|:-------------------------|-----------------:|-------------------:|--------------:|:----------------------------------------------------------------------------------------------------|
| cwhvm1_hw_cw_m  | CWHvm1_HW+CW   | M          |  14576.5  |     26.41 | `1500`                   | mp10_au_1500            | high                     |            33.02 |              27.04 |          0.63 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm1_hw_ba_m  | CWHvm1_HW+BA   | M          |  13083.9  |     26.28 | `1510`                   | mp10_au_1510            | high                     |            12.8  |              27.51 |          1.24 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm1_hw_cw_l  | CWHvm1_HW+CW   | L          |   7117.88 |     16.01 | `1500`                   | mp10_au_1500            | low                      |            30.88 |              26.79 |         10.78 | low-confidence nearest MP10 row; review species/SI mismatch before executable BatchTIPSY use        |
| cwhvm1_hw_ba_h  | CWHvm1_HW+BA   | H          |   6336.71 |     31.17 | `1510`                   | mp10_au_1510            | high                     |            10.73 |              27.67 |          3.5  | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm1_hw_ba_l  | CWHvm1_HW+BA   | L          |   6328.04 |     17.14 | `9510`                   | mp10_au_9510            | high                     |            19.3  |              20.23 |          3.08 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm1_cw_hw_h  | CWHvm1_CW+HW   | H          |   6154.4  |     23.79 | `7500`                   | mp10_au_7500            | medium                   |            46.98 |              19.54 |          4.25 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_cw_hw_l  | CWHvm1_CW+HW   | L          |   6107.94 |     13.36 | `7500`                   | mp10_au_7500            | medium                   |            36.61 |              19.46 |          6.1  | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_m     | CWHvm1_HW      | M          |   4138.94 |     26.36 | `1510`                   | mp10_au_1510            | medium                   |            40    |              28    |          1.64 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_ss_l  | CWHvm1_HW+SS   | L          |   4135.64 |     24.46 | `1510`                   | mp10_au_1510            | medium                   |            47.81 |              28.32 |          3.86 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_cw_hw_m  | CWHvm1_CW+HW   | M          |   4015.12 |     18.59 | `7500`                   | mp10_au_7500            | medium                   |            44.96 |              19.51 |          0.92 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm2_hw_ba_h  | CWHvm2_HW+BA   | H          |   3577.02 |     27.75 | `1510`                   | mp10_au_1510            | high                     |            17.61 |              27.38 |          0.36 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm2_hw_ba_l  | CWHvm2_HW+BA   | L          |   3095.37 |     13.79 | `9510`                   | mp10_au_9510            | medium                   |            14.93 |              20.2  |          6.41 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_cw_h  | CWHvm1_HW+CW   | H          |   2899.43 |     30.8  | `1500`                   | mp10_au_1500            | medium                   |            38.36 |              27.23 |          3.56 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm2_hw_ba_m  | CWHvm2_HW+BA   | M          |   2418.08 |     20.06 | `9510`                   | mp10_au_9510            | high                     |            19.85 |              20.2  |          0.15 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm1_hw_ss_h  | CWHvm1_HW+SS   | H          |   2240.22 |     32.36 | `1510`                   | mp10_au_1510            | medium                   |            49    |              28.52 |          3.85 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_h     | CWHvm1_HW      | H          |   1645.05 |     31.36 | `1510`                   | mp10_au_1510            | medium                   |            40    |              28    |          3.36 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_l     | CWHvm1_HW      | L          |   1582.41 |     15.99 | `1510`                   | mp10_au_1510            | fallback_review_required |            40    |              28    |         12.01 | nearest MP10 species/productivity row only; review before executable BatchTIPSY use                 |
| cwhvm1_cw_h     | CWHvm1_CW      | H          |   1331.28 |     21.74 | `6501`                   | mp10_au_6501            | high                     |             0    |              23.8  |          2.06 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvm1_cw_yc_l  | CWHvm1_CW+YC   | L          |   1293.87 |     10.13 | `7500`                   | mp10_au_7500            | low                      |            76.68 |              19.35 |          9.22 | low-confidence nearest MP10 row; review species/SI mismatch before executable BatchTIPSY use        |
| cwhvm1_hw_fdc_l | CWHvm1_HW+FDC  | L          |   1288.94 |     27.36 | `1510`                   | mp10_au_1510            | medium                   |            52.09 |              28.45 |          1.08 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_dr_m  | CWHvm1_HW+DR   | M          |   1157.28 |     27.52 | `1510`                   | mp10_au_1510            | medium                   |            36.76 |              27.9  |          0.38 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm2_hw_cw_h  | CWHvm2_HW+CW   | H          |   1136.41 |     25.9  | `1500`                   | mp10_au_1500            | high                     |            29.25 |              26.82 |          0.92 | high-confidence nearest MP10 row by species/SI similarity                                           |
| cwhvh1_cw_hw_l  | CWHvh1_CW+HW   | L          |   1104.14 |     12.23 | `7500`                   | mp10_au_7500            | medium                   |            21.58 |              19.42 |          7.19 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvh1_cw_hw_h  | CWHvh1_CW+HW   | H          |   1076.78 |     20.72 | `7500`                   | mp10_au_7500            | medium                   |            39.93 |              19.5  |          1.22 | medium-confidence nearest MP10 row; acceptable for planning crosswalk, review before final curve QA |
| cwhvm1_hw_dr_l  | CWHvm1_HW+DR   | L          |    983.33 |     19.37 | `1510`                   | mp10_au_1510            | low                      |            39.08 |              27.92 |          8.55 | low-confidence nearest MP10 row; review species/SI mismatch before executable BatchTIPSY use        |

## Schema Notes

- `matched_legacy_au_code` is zero-padded MP10 AU code text. Preserve leading
  zeroes such as `0500`.
- `matched_legacy_au_key` is an explicitly non-numeric provenance key for CSV
  consumers that infer code columns as integers.

## Review Notes

- MP10 legacy AU codes remain provenance and parameter keys only; they are not
  canonical TFL 6 Patchworks AU identities.
- This first crosswalk deliberately keeps separate matches for existing managed
  11-50, existing managed 1-10, and future managed curve lanes because MP10
  uses different tables and assumptions for those contexts.
- Species matching maps `FDC`/`FD` to MP10 `fd`, `YC` to `cy`, `HM` to `hw`, and
  deciduous or unsupported species such as `DR` to `other`.
- Low-confidence and `fallback_review_required` rows are expected for some
  minor or unusual AUs because MP10 provides a finite set of legacy parameter
  rows, not a one-to-one parameter row for every refined TFL 6 static AU.
- P3.4d/P3.4e should use this artifact to decide which AUs are ready for curve
  generation and which require row-level maintainer review or aggregation.
