# TFL 6 First-Growth Curve Shape Diagnostics

## Purpose

Classify the current P3.4d natural/untreated first-growth curve shapes
before changing smoothing parameters, borrowing rules, or Phase 4 bundle
inputs. This report is diagnostic only: it does not alter
`planning/tfl6_first_growth_au_curves.csv`.

## Summary Counts

- Total AU diagnostic rows: `380`
- Accepted curve rows assessed: `276`
- OK shape rows: `74`
- Review shape rows: `194`
- Critical shape rows: `8`
- Insufficient-source rows: `104`

## Flag Counts

- `large_single_year_drop`: `80`
- `last_20_year_gain`: `7`
- `last_50_year_gain`: `18`
- `late_start_ge10_after_age100`: `7`
- `late_start_ge50_after_age160`: `7`
- `lmh_order_violation`: `193`
- `near_zero_to_old_age_then_jump`: `6`
- `not_accepted`: `104`
- `old_age_terminal_uptick`: `5`
- `wobbly_multi_extrema`: `5`

## Recommended Action Counts

- `accept_shape`: `74`
- `apply_tail_constraint_or_terminal_cap`: `15`
- `borrow_or_fallback_required`: `104`
- `increase_smoothing_or_shape_constraint`: `76`
- `reject_current_fit_and_borrow_adjacent_au`: `7`
- `review_lmh_order_or_borrowing`: `104`

## Critical Cases

Critical cases are accepted curves that appear unusable without a
replacement rule, especially curves that stay effectively zero until
old ages and then jump upward.

| au_id          |   source_stand_count | shape_flags                                                                                                                                           |   first_age_ge_10 |   volume_at_120 |   terminal_volume | recommended_action                        |
|:---------------|---------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------|------------------:|----------------:|------------------:|:------------------------------------------|
| cwhvm1_ba_l    |                    2 | late_start_ge50_after_age160;last_20_year_gain;last_50_year_gain                                                                                      |                88 |       18.3623   |           66.6768 | apply_tail_constraint_or_terminal_cap     |
| cwhvm1_fd_m    |                    3 | late_start_ge10_after_age100;late_start_ge50_after_age160;near_zero_to_old_age_then_jump;last_50_year_gain;lmh_order_violation                        |               257 |        0.346844 |          755.6    | reject_current_fit_and_borrow_adjacent_au |
| cwhvm2_fd_l    |                    2 | late_start_ge10_after_age100;late_start_ge50_after_age160;near_zero_to_old_age_then_jump;last_50_year_gain                                            |               257 |        0.346844 |          452      | reject_current_fit_and_borrow_adjacent_au |
| cwhvm2_hm_cw_m |                    2 | late_start_ge10_after_age100;late_start_ge50_after_age160;near_zero_to_old_age_then_jump;last_50_year_gain;lmh_order_violation                        |               257 |        0.298127 |          286.5    | reject_current_fit_and_borrow_adjacent_au |
| cwhvm2_hw_fd_l |                    4 | late_start_ge10_after_age100;late_start_ge50_after_age160;near_zero_to_old_age_then_jump;last_50_year_gain;wobbly_multi_extrema;lmh_order_violation   |               247 |        0.346844 |          596      | reject_current_fit_and_borrow_adjacent_au |
| mhmm1_hw_cw_h  |                    2 | late_start_ge10_after_age100;lmh_order_violation                                                                                                      |               104 |       24.5355   |          554.744  | reject_current_fit_and_borrow_adjacent_au |
| mhmm1_yc_h     |                    3 | late_start_ge10_after_age100;late_start_ge50_after_age160;near_zero_to_old_age_then_jump;last_50_year_gain;large_single_year_drop;lmh_order_violation |               247 |        0.298127 |          213.928  | reject_current_fit_and_borrow_adjacent_au |
| mhmm1_yc_hw_m  |                    4 | late_start_ge10_after_age100;late_start_ge50_after_age160;near_zero_to_old_age_then_jump;last_20_year_gain;last_50_year_gain;lmh_order_violation      |               247 |        0.325493 |          105.368  | reject_current_fit_and_borrow_adjacent_au |

## Review Cases

Review cases are softer warnings: terminal upticks, wobbly multi-extrema
behavior, large one-year drops, or L/M/H ordering violations.

| au_id           |   source_stand_count | shape_flags                                                                                         |   terminal_uptick_from_post_peak_min |   last_20_gain |   sign_change_count | recommended_action                     |
|:----------------|---------------------:|:----------------------------------------------------------------------------------------------------|-------------------------------------:|---------------:|--------------------:|:---------------------------------------|
| cwhvm2_yc_cw_l  |                   14 | old_age_terminal_uptick;last_50_year_gain;large_single_year_drop;lmh_order_violation                |                           246.253    |      19.1381   |                   2 | apply_tail_constraint_or_terminal_cap  |
| cwhvm1_yc_hm_l  |                   18 | old_age_terminal_uptick;last_50_year_gain;large_single_year_drop;lmh_order_violation                |                           152.253    |      13.3193   |                   3 | apply_tail_constraint_or_terminal_cap  |
| cwhvm1_yc_cw_m  |                   28 | old_age_terminal_uptick;last_50_year_gain;large_single_year_drop;lmh_order_violation                |                            92.2683   |      11.7591   |                   2 | apply_tail_constraint_or_terminal_cap  |
| cwhvm1_cw_dr_l  |                    6 | old_age_terminal_uptick;lmh_order_violation                                                         |                            54.0796   |      -1.40559  |                   2 | apply_tail_constraint_or_terminal_cap  |
| cwhvh1_hw_h     |                   18 | old_age_terminal_uptick;lmh_order_violation                                                         |                            44.9616   |      -8.29931  |                   3 | apply_tail_constraint_or_terminal_cap  |
| cwhvh1_ss_hw_m  |                   18 | last_20_year_gain;large_single_year_drop;lmh_order_violation                                        |                            44.4123   |      28.8474   |                   3 | apply_tail_constraint_or_terminal_cap  |
| cwhvm2_yc_cw_h  |                   10 | large_single_year_drop;lmh_order_violation                                                          |                            37.6267   |       6.57766  |                   2 | increase_smoothing_or_shape_constraint |
| cwhvh1_hw_l     |                   20 | lmh_order_violation                                                                                 |                            24.5424   |      -7.79408  |                   3 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_cw_l  |                   50 | large_single_year_drop;lmh_order_violation                                                          |                            24.0833   |       8.81254  |                   2 | increase_smoothing_or_shape_constraint |
| mhmm1_cw_hw_m   |                    3 | lmh_order_violation                                                                                 |                            20.1364   |      -3.56059  |                   3 | review_lmh_order_or_borrowing          |
| cwhvm2_yc_hw_l  |                   48 | large_single_year_drop;lmh_order_violation                                                          |                            18.944    |      10.8019   |                   2 | increase_smoothing_or_shape_constraint |
| mhmm1_hw_ba_m   |                   21 | wobbly_multi_extrema;lmh_order_violation                                                            |                            13.8176   |      12.115    |                   4 | increase_smoothing_or_shape_constraint |
| cwhvm2_hw_yc_m  |                   33 | large_single_year_drop                                                                              |                            12.5317   |      -0.359751 |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm2_yc_cw_m  |                   10 | lmh_order_violation                                                                                 |                             4.2426   |       0.854775 |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_pl_cw_m  |                    2 | large_single_year_drop;lmh_order_violation                                                          |                             3.56344  |       0.621266 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvh1_dr_h     |                    5 | wobbly_multi_extrema;lmh_order_violation                                                            |                             1        |       0.472629 |                   4 | increase_smoothing_or_shape_constraint |
| cwhvh1_dr_l     |                    5 | large_single_year_drop;lmh_order_violation                                                          |                             1        |      -6.06597  |                   2 | increase_smoothing_or_shape_constraint |
| cwhvm1_yc_l     |                    5 | large_single_year_drop;lmh_order_violation                                                          |                             0.40042  |       0.138989 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_yc_l     |                    3 | large_single_year_drop;lmh_order_violation                                                          |                             0.205406 |       0.059767 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_pli_sx_h |                    2 | last_20_year_gain;last_50_year_gain;wobbly_multi_extrema;large_single_year_drop;lmh_order_violation |                             0        |     141.342    |                   4 | apply_tail_constraint_or_terminal_cap  |
| cwhvm1_pli_sx_l |                    2 | last_20_year_gain;last_50_year_gain;lmh_order_violation                                             |                             0        |     111.408    |                   2 | apply_tail_constraint_or_terminal_cap  |
| mhmm1_hm_yc_m   |                    4 | last_20_year_gain;last_50_year_gain;lmh_order_violation                                             |                             0        |      29.6496   |                   1 | apply_tail_constraint_or_terminal_cap  |
| mhmm1_cw_hw_h   |                    2 | last_20_year_gain;last_50_year_gain;lmh_order_violation                                             |                             0        |      23.2776   |                   0 | apply_tail_constraint_or_terminal_cap  |
| cwhvm2_fd_h     |                    2 | last_50_year_gain                                                                                   |                             0        |      15.9168   |                   0 | apply_tail_constraint_or_terminal_cap  |
| cwhvm2_yc_hm_m  |                   26 | last_50_year_gain;lmh_order_violation                                                               |                             0        |       5.16037  |                   3 | apply_tail_constraint_or_terminal_cap  |
| cwhvm2_ba_hm_l  |                    3 | last_50_year_gain;lmh_order_violation                                                               |                             0        |       2.50243  |                   1 | apply_tail_constraint_or_terminal_cap  |
| cwhvm1_cw_hm_l  |                    2 | last_50_year_gain                                                                                   |                             0        |       2.18898  |                   0 | apply_tail_constraint_or_terminal_cap  |
| mhmm1_ba_hw_l   |                   15 | lmh_order_violation                                                                                 |                             0        |       1.34699  |                   0 | review_lmh_order_or_borrowing          |
| mhmm1_hw_yc_m   |                    4 | lmh_order_violation                                                                                 |                             0        |       0.79898  |                   0 | review_lmh_order_or_borrowing          |
| cwhvh1_yc_cw_h  |                    6 | lmh_order_violation                                                                                 |                             0        |       0.758364 |                   2 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hm_m  |                    5 | lmh_order_violation                                                                                 |                             0        |       0.510117 |                   0 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_pl_m  |                   10 | lmh_order_violation                                                                                 |                             0        |       0.127166 |                   0 | review_lmh_order_or_borrowing          |
| mhmm1_hm_ba_m   |                    4 | lmh_order_violation                                                                                 |                             0        |      -0.239699 |                   0 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_yc_h  |                   65 | large_single_year_drop;lmh_order_violation                                                          |                             0        |      -0.394568 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_yc_hw_m  |                   21 | large_single_year_drop;lmh_order_violation                                                          |                             0        |      -0.790439 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_ss_l     |                    4 | lmh_order_violation                                                                                 |                             0        |      -0.867806 |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_cw_ba_h  |                    2 | lmh_order_violation                                                                                 |                             0        |      -1.07415  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_dr_hw_m  |                    2 | lmh_order_violation                                                                                 |                             0        |      -1.19149  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_yc_l  |                   91 | large_single_year_drop;lmh_order_violation                                                          |                             0        |      -1.52413  |                   1 | increase_smoothing_or_shape_constraint |
| cwhvh1_cw_hw_m  |                  118 | lmh_order_violation                                                                                 |                             0        |      -1.97234  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_dr_hw_h  |                    3 | lmh_order_violation                                                                                 |                             0        |      -2.07385  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_hw_m  |                   26 | lmh_order_violation                                                                                 |                             0        |      -2.13447  |                   3 | review_lmh_order_or_borrowing          |
| cwhvh1_cw_yc_h  |                   14 | lmh_order_violation                                                                                 |                             0        |      -2.21367  |                   0 | review_lmh_order_or_borrowing          |
| cwhvh1_yc_cw_m  |                   11 | large_single_year_drop;lmh_order_violation                                                          |                             0        |      -2.46216  |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_dr_cw_m  |                    9 | lmh_order_violation                                                                                 |                             0        |      -2.52953  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_yc_m  |                   30 | lmh_order_violation                                                                                 |                             0        |      -2.59861  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_pli_sx_m |                    2 | lmh_order_violation                                                                                 |                             0        |      -2.68716  |                   0 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_cw_l  |                    2 | large_single_year_drop;lmh_order_violation                                                          |                             0        |      -2.82666  |                   1 | increase_smoothing_or_shape_constraint |
| mhmm1_ba_hw_h   |                    9 | lmh_order_violation                                                                                 |                             0        |      -3.22724  |                   0 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hw_m  |                   23 | lmh_order_violation                                                                                 |                             0        |      -3.35654  |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_dr_hw_h  |                    6 | lmh_order_violation                                                                                 |                             0        |      -3.39826  |                   1 | review_lmh_order_or_borrowing          |
| mhmm1_hw_yc_h   |                    9 | lmh_order_violation                                                                                 |                             0        |      -3.74157  |                   0 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hm_h  |                   12 | large_single_year_drop;lmh_order_violation                                                          |                             0        |      -4.02133  |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_hm_ba_h  |                    7 | lmh_order_violation                                                                                 |                             0        |      -4.04129  |                   0 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_h     |                    4 | lmh_order_violation                                                                                 |                             0        |      -4.16995  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ss_m     |                    3 | lmh_order_violation                                                                                 |                             0        |      -4.19685  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_dr_m     |                    2 | lmh_order_violation                                                                                 |                             0        |      -4.22638  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_cw_yc_l  |                   19 | lmh_order_violation                                                                                 |                             0        |      -4.50667  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_yc_h     |                    3 | lmh_order_violation                                                                                 |                             0        |      -4.53833  |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_dr_hw_l  |                    6 | lmh_order_violation                                                                                 |                             0        |      -4.64548  |                   1 | review_lmh_order_or_borrowing          |

Only the first `60` review rows are shown here; see CSV for all `194`.

## Insufficient-Source Cases

`104` AUs still require borrowing/fallback review.

## Parameter-Tuning Implications

- Curves with `near_zero_to_old_age_then_jump` should not be accepted from
  the current fit. Prefer borrowing from an adjacent SI class or similar
  base AU until a support threshold or source-filter problem is resolved.
- Curves with `old_age_terminal_uptick`, `last_20_year_gain`, or
  `last_50_year_gain` need a tail constraint. Candidate tweaks include a
  no-upturn-after-terminal-decline rule, a terminal cap after the last
  reliable observed age bin, or a stronger old-age tail penalty.
- Curves with `wobbly_multi_extrema` or `large_single_year_drop` need
  stronger smoothing or a shape-constrained post-process before they are
  eligible for model-input bundle use.
- L/M/H order violations should be reviewed at the base-AU family level.
  If the low or medium SI curve crosses a higher SI curve materially,
  either borrow from the better-supported adjacent SI class or apply a
  family-level ordering constraint.

## Artifacts

- `planning/tfl6_first_growth_shape_diagnostics.csv`
- `planning/tfl6_first_growth_shape_diagnostics.md`
- Inputs: `planning/tfl6_first_growth_au_curves.csv` and
  `planning/tfl6_first_growth_au_fit_diagnostics.csv`
