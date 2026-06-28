# TFL 6 MP11 Phase 9 Source-Layer Verification Manifest

## Purpose

This P9.2 manifest verifies existing public source-layer dependencies
for the MP11 source-layer and THLB rebuild. It records source
availability, read status, schema summaries, geometry summaries, and
public/proxy/private status. It does not execute THLB overlays.

## Files

- `planning/tfl6_mp11_phase9_source_layer_manifest.md`
- `planning/tfl6_mp11_phase9_source_layer_manifest.csv`
- `planning/tfl6_mp11_phase9_source_layer_manifest.json`

## Status Counts

- Rows: `21`
- Existing sources: `18`
- Read status counts: `{'not_materialized': 3, 'read_ok': 18}`
- Public/private status counts: `{'public_proxy': 3, 'public_rebuild': 17, 'unavailable_non_public': 1}`

## Verification Table

| Source | Family | Exists | Read status | Features | Area ha | Length km | Status | Decision |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- | --- |
| `tfl6_aoi_current` | aoi | True | `read_ok` | 182 | 217,042.719 |  | `public_rebuild` | `verify_for_p9_2` |
| `vri_2025_r1_tfl6` | inventory | True | `read_ok` | 26,959 | 217,042.719 |  | `public_rebuild` | `verify_for_p9_2` |
| `vdyp7_2025_poly_tfl6` | inventory | True | `read_ok` | 26,833 |  |  | `public_rebuild` | `verify_for_p9_2` |
| `vdyp7_2025_layer_tfl6` | inventory | True | `read_ok` | 25,585 |  |  | `public_rebuild` | `verify_for_p9_2` |
| `dra_roads_tfl6` | roads | True | `read_ok` | 10,706 |  | 4,255.863 | `public_rebuild` | `verify_for_p9_2` |
| `fwa_stream_networks_tfl6` | hydrology | True | `read_ok` | 12,078 |  | 4,748.715 | `public_rebuild` | `verify_for_p9_2` |
| `fwa_lakes_tfl6` | hydrology | True | `read_ok` | 599 | 3,243.849 |  | `public_rebuild` | `verify_for_p9_2` |
| `fwa_wetlands_tfl6` | hydrology | True | `read_ok` | 572 | 982.424 |  | `public_rebuild` | `verify_for_p9_2` |
| `shoreline_candidate` | shoreline | False | `not_materialized` |  |  |  | `public_proxy` | `defer_or_materialize_if_public_source_is_accepted` |
| `ogma_legal_current_tfl6` | legal_reserves | True | `read_ok` | 165 | 16,131.032 |  | `public_rebuild` | `verify_for_p9_2` |
| `ogma_non_legal_current_tfl6` | legal_reserves | True | `read_ok` | 2 | 0.687 |  | `public_proxy` | `verify_as_proxy_for_p9_2` |
| `wha_approved_tfl6` | legal_reserves | True | `read_ok` | 45 | 2,942.796 |  | `public_rebuild` | `verify_for_p9_2` |
| `uwr_approved_tfl6` | legal_reserves | True | `read_ok` | 22 | 2,365.514 |  | `public_rebuild` | `verify_for_p9_2` |
| `recreation_polygons_tfl6` | recreation | True | `read_ok` | 26 | 187.868 |  | `public_rebuild` | `verify_for_p9_2` |
| `recreation_trails_tfl6` | recreation | True | `read_ok` | 3 |  | 1.737 | `public_rebuild` | `verify_for_p9_2` |
| `recreation_site_points_tfl6` | recreation | True | `read_ok` | 10 |  |  | `public_rebuild` | `verify_for_p9_2` |
| `recreation_details_closures_tfl6` | recreation | True | `read_ok` | 13 |  |  | `public_rebuild` | `verify_for_p9_2` |
| `bec_tfl6` | strata | True | `read_ok` | 107 | 217,042.719 |  | `public_rebuild` | `verify_for_p9_2` |
| `landscape_units_tfl6` | strata | True | `read_ok` | 13 | 217,042.719 |  | `public_rebuild` | `verify_for_p9_2` |
| `public_dem_slope_candidate` | dem_slope | False | `not_materialized` |  |  |  | `public_proxy` | `defer_or_materialize_if_public_source_is_accepted` |
| `wfp_lbb_iti_lefi` | private_dependency | False | `not_materialized` |  |  |  | `unavailable_non_public` | `do_not_materialize_without_public_safe_source` |

## Key Findings

- Core tracked GeoPackage sources for AOI, VRI/R1, roads, hydrology,
  legal reserves, recreation, BEC, and landscape units are present and
  readable in this environment.
- VDYP parquet artifacts are present and readable in this environment.
- No accepted shoreline or DEM/slope source is currently tracked for the
  MP11 public-data rebuild lane.
- WFP LBB, ITI, and LEFI dependencies remain `unavailable_non_public` and
  must not be reconstructed from aggregate MP11 summaries.

## Use Boundary

This manifest verifies source availability and coarse schema/geometry
status only. P9.3 must still profile fields and proxy variables before
P9.4 can run an ordered overlay recipe. No row in this manifest is an
accepted model input.
