# TFL 6 First-Growth Curve Shape Diagnostics

## Purpose

Classify the current P3.4d natural/untreated first-growth curve shapes
for the selected top-area AU set before changing smoothing parameters,
borrowing rules, or Phase 4 bundle inputs. This report is diagnostic
only: it does not alter
`planning/tfl6_first_growth_au_curves.csv`.

## Summary Counts

- Selected top-area AU diagnostic rows: `77`
- Accepted curve rows assessed: `77`
- OK shape rows: `32`
- Review shape rows: `45`
- Critical shape rows: `0`
- Insufficient-source rows: `0`

## Flag Counts

- `large_single_year_drop`: `17`
- `last_50_year_gain`: `1`
- `lmh_order_violation`: `42`
- `old_age_terminal_uptick`: `1`

## Recommended Action Counts

- `accept_shape`: `32`
- `apply_tail_constraint_or_terminal_cap`: `1`
- `increase_smoothing_or_shape_constraint`: `16`
- `review_lmh_order_or_borrowing`: `28`

## Critical Cases

Critical cases are accepted curves that appear unusable without a
replacement rule, especially curves that stay effectively zero until
old ages and then jump upward.

No critical accepted-curve shape cases were flagged.

## Review Cases

Review cases are softer warnings: terminal upticks, wobbly multi-extrema
behavior, large one-year drops, or L/M/H ordering violations.

| au_id          |   source_stand_count | shape_flags                                                                          |   terminal_uptick_from_post_peak_min |   last_20_gain |   sign_change_count | recommended_action                     |
|:---------------|---------------------:|:-------------------------------------------------------------------------------------|-------------------------------------:|---------------:|--------------------:|:---------------------------------------|
| cwhvm1_yc_cw_m |                   28 | old_age_terminal_uptick;last_50_year_gain;large_single_year_drop;lmh_order_violation |                              92.2683 |      11.7591   |                   2 | apply_tail_constraint_or_terminal_cap  |
| cwhvm1_yc_cw_l |                   50 | large_single_year_drop;lmh_order_violation                                           |                              24.0833 |       8.81254  |                   2 | increase_smoothing_or_shape_constraint |
| cwhvm2_yc_hw_l |                   48 | large_single_year_drop;lmh_order_violation                                           |                              18.944  |      10.8019   |                   2 | increase_smoothing_or_shape_constraint |
| cwhvm2_hw_yc_m |                   33 | large_single_year_drop                                                               |                              12.5317 |      -0.359751 |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_yc_h |                   65 | large_single_year_drop;lmh_order_violation                                           |                               0      |      -0.394568 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_yc_hw_m |                   21 | large_single_year_drop;lmh_order_violation                                           |                               0      |      -0.790439 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_yc_l |                   91 | large_single_year_drop;lmh_order_violation                                           |                               0      |      -1.52413  |                   1 | increase_smoothing_or_shape_constraint |
| cwhvh1_cw_hw_m |                  118 | lmh_order_violation                                                                  |                               0      |      -1.97234  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_hw_m |                   26 | lmh_order_violation                                                                  |                               0      |      -2.13447  |                   3 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_yc_m |                   30 | lmh_order_violation                                                                  |                               0      |      -2.59861  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hw_m |                   23 | lmh_order_violation                                                                  |                               0      |      -3.35654  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_yc_hw_h |                   33 | lmh_order_violation                                                                  |                               0      |      -8.02923  |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_cw_hw_l |                  172 | lmh_order_violation                                                                  |                               0      |      -8.33861  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_yc_l |                   63 | large_single_year_drop                                                               |                               0      |      -8.78548  |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_hw_ba_l |                  434 | lmh_order_violation                                                                  |                               0      |      -9.19724  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_cw_hw_h |                   51 | lmh_order_violation                                                                  |                               0      |      -9.33469  |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_hw_cw_l |                  117 | lmh_order_violation                                                                  |                               0      |      -9.71481  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hw_h |                   27 | lmh_order_violation                                                                  |                               0      |      -9.88675  |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_cw_hw_h |                  138 | lmh_order_violation                                                                  |                               0      |     -10.2452   |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_hw_cw_m |                   69 | lmh_order_violation                                                                  |                               0      |     -10.7231   |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_hw_cw_h |                   96 | lmh_order_violation                                                                  |                               0      |     -11.0265   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_cw_h |                   30 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -11.2391   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_hw_m |                  544 | lmh_order_violation                                                                  |                               0      |     -12.7541   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hw_l |                   34 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -13.5813   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_ba_hw_l |                   46 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -13.7559   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm2_hw_ba_m |                  299 | lmh_order_violation                                                                  |                               0      |     -14.1334   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_fd_m |                   54 | lmh_order_violation                                                                  |                               0      |     -14.1399   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_ss_l |                  449 | lmh_order_violation                                                                  |                               0      |     -14.3869   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_hw_l |                  884 | lmh_order_violation                                                                  |                               0      |     -15.3246   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_ss_m |                   72 | lmh_order_violation                                                                  |                               0      |     -15.367    |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_cw_h |                  125 | lmh_order_violation                                                                  |                               0      |     -15.6777   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_cw_m |                  114 | lmh_order_violation                                                                  |                               0      |     -16.5036   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_ba_h |                  315 | lmh_order_violation                                                                  |                               0      |     -16.5953   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_cw_l |                  134 | lmh_order_violation                                                                  |                               0      |     -17.0649   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_hw_h |                   35 | lmh_order_violation                                                                  |                               0      |     -17.8867   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_hw_h |                  694 | lmh_order_violation                                                                  |                               0      |     -18.197    |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_ss_h |                  228 | lmh_order_violation                                                                  |                               0      |     -18.5818   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_fd_l |                   63 | lmh_order_violation                                                                  |                               0      |     -18.7686   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_l    |                  147 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -23.7602   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_hw_fd_h |                   56 | lmh_order_violation                                                                  |                               0      |     -25.4488   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_cw_hw_m |                   44 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -25.6406   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_h    |                  128 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -33.8751   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_m    |                  140 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -35.3354   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_ss_hw_h |                   49 | large_single_year_drop                                                               |                               0      |     -43.3898   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_cw_hw_l |                   61 | large_single_year_drop;lmh_order_violation                                           |                               0      |     -73.2361   |                   3 | increase_smoothing_or_shape_constraint |

## Insufficient-Source Cases

`0` selected top-area AUs still require borrowing/fallback review.

## Parameter-Tuning Implications

The selected-set curve shapes are accepted as good enough to continue Phase 3.
The flags below remain useful for a later optional smoothing/tail-constraint
revisit before final model-input bundle lock, but they do not block P3.4e
treated/managed curves, P3.5 treatment options, or P3.6 transition logic.

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
- Non-selected AU imputation is audited separately in
  `planning/tfl6_first_growth_au_remap_audit.csv`.
- Inputs: `planning/tfl6_first_growth_au_curves.csv` and
  `planning/tfl6_first_growth_au_fit_diagnostics.csv`
