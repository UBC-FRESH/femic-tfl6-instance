# TFL 6 MP11 Phase 9 Ordered Overlay Scaffold

## Purpose

This P9.4 note validates the MP11 public-data ordered-overlay THLB
recipe scaffold against the P9.2 source manifest and P9.3 input/proxy
profile. It is a scaffold smoke only; it does not execute overlays or
produce THLB outputs.

## Files

- `config/tsr/mp11_thlb_rebuild.recipe.yaml`
- `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.md`
- `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.csv`
- `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.json`

## Status Counts

- Rows: `13`
- Execution class counts: `{'aspatial_policy_candidate': 1, 'attribute_candidate': 2, 'checkpoint': 4, 'overlay_candidate': 3, 'proxy_candidate': 2, 'unavailable_or_proxy_gap': 1}`
- Phase 9 status counts: `{'comparison_target_only': 1, 'deferred_public_dem_needed': 1, 'deferred_unavailable_or_public_proxy_needed': 1, 'mixed_public_proxy_review_required': 1, 'ready_for_recipe_scaffold': 3, 'review_required_before_execution': 6}`
- Source reference status counts: `{'ok': 13}`
- Candidate reference status counts: `{'ok': 13}`

## Ordered Steps

| Order | Step | Class | Status | Source refs | Candidate refs | MP11 target ha |
| ---: | --- | --- | --- | --- | --- | ---: |
| 0 | `mp11_nd_000` Total land base / accounting universe | `checkpoint` | `ready_for_recipe_scaffold` | `ok` | `ok` | 217,197.000 |
| 10 | `mp11_nd_010` Non-forest and non-treed review candidates | `attribute_candidate` | `review_required_before_execution` | `ok` | `ok` |  |
| 20 | `mp11_nd_020` Existing roads | `overlay_candidate` | `review_required_before_execution` | `ok` | `ok` |  |
| 30 | `mp11_nd_030` Total forested checkpoint | `checkpoint` | `ready_for_recipe_scaffold` | `ok` | `ok` | 196,233.000 |
| 40 | `mp11_nd_040` Non-productive and low-site candidates | `attribute_candidate` | `review_required_before_execution` | `ok` | `ok` |  |
| 50 | `mp11_nd_050` Productive forest / AFLB checkpoint | `checkpoint` | `ready_for_recipe_scaffold` | `ok` | `ok` | 187,425.000 |
| 60 | `mp11_nd_060` Legal/proposed OGMAs, WHAs, UWRs, and conservation candidates | `overlay_candidate` | `mixed_public_proxy_review_required` | `ok` | `ok` |  |
| 70 | `mp11_nd_070` Additional values: research, PSPs, big trees, and karst | `unavailable_or_proxy_gap` | `deferred_unavailable_or_public_proxy_needed` | `ok` | `ok` |  |
| 80 | `mp11_nd_080` Physical/economic operability proxy | `proxy_candidate` | `review_required_before_execution` | `ok` | `ok` | 156,305.000 |
| 90 | `mp11_nd_090` Riparian management | `overlay_candidate` | `review_required_before_execution` | `ok` | `ok` |  |
| 100 | `mp11_nd_100` Terrain stability and LiDAR 90 percent slope | `proxy_candidate` | `deferred_public_dem_needed` | `ok` | `ok` |  |
| 110 | `mp11_nd_110` Existing/future WTRAs and stand-level retention | `aspatial_policy_candidate` | `review_required_before_execution` | `ok` | `ok` |  |
| 120 | `mp11_nd_120` Current THLB checkpoint | `checkpoint` | `comparison_target_only` | `ok` | `ok` | 120,099.000 |

## Key Findings

- The scaffold preserves ordered checkpoint, attribute, overlay, proxy,
  unavailable-gap, and aspatial-policy rows.
- All referenced source IDs and candidate IDs resolve against the P9.2
  and P9.3 manifests.
- Current THLB `120,099 ha` is represented as a comparison target only.
- Shoreline, DEM/slope, and WFP LBB/ITI/LEFI remain explicit gaps or
  proxy dependencies before execution.

## Use Boundary

This scaffold authorizes P9.5 implementation planning and bounded smoke
design only. It does not authorize accepted THLB outputs or model-input
promotion.
