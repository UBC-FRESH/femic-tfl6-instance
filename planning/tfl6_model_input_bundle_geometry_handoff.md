# TFL 6 P4.1c THLB Geometry Handoff

## Purpose

This note records the P4.1c handoff from the accepted Phase 2 THLB netdown lane
to the Phase 4 model-input bundle lane. It exists because the regenerated
geometry artifacts under `data/model_input_bundle/` are generated runtime
outputs, while the planning surface needs a tracked audit trail explaining what
was regenerated and how it should be consumed.

## Regeneration Command

The final THLB geometry was regenerated from the accepted clipped 2025 TFL 6 R1
VRI input using the reviewed THLB recipe:

```powershell
python -m femic tsr thlb-netdown-run `
  --instance-root external/femic-tfl6-instance `
  --thlb-netdown-recipe-path config/tsr/thlb_netdown.recipe.yaml `
  --checkpoint-path data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg `
  --output-path data/model_input_bundle/input_geometry/thlb_current.feather `
  --audit-path data/model_input_bundle/input_geometry/thlb_checkpoint_manifest.json `
  --execution-mode reconstructed `
  --parallel-mode serial
```

The GeoPackage mirror was then written from the Feather handoff so downstream
tools that prefer OGR-compatible inputs can inspect the same geometry:

- `data/model_input_bundle/input_geometry/thlb_current.feather`
- `data/model_input_bundle/input_geometry/thlb_current.gpkg`
- `data/model_input_bundle/input_geometry/thlb_checkpoint_manifest.json`

## Direct Inspection

- Generated UTC: `2026-06-26T13:59:08.454708+00:00`
- Source input: `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`
- Recipe: `config/tsr/thlb_netdown.recipe.yaml`
- CRS: `EPSG:3005`
- Rows: `29892`
- Geometry type: `MultiPolygon`
- Feather size: `31636290` bytes
- GeoPackage size: `60403712` bytes
- Manifest size: `52935` bytes
- Total geometry area: `186567.162340 ha`
- Weighted THLB area using `thlb_fact`: `144203.484774 ha`
- Manifest final managed area: `144203.48477359748 ha`

The weighted THLB area matches the accepted Phase 2 benchmark. For this handoff,
`thlb_fact` is the authoritative final THLB weighting field. The positive
geometry area alone is not the final THLB area because several accepted
aspatial fallback deductions are represented fractionally.

## Companion Outputs

The THLB runner also wrote legacy companion checkpoint files under `data/tsr/`.
Those files are not the P4 handoff contract and were not retained in the tracked
planning surface. If an AFLB or LHLB restart checkpoint is needed later, it
should be regenerated deliberately and either added to the accepted artifact
policy or treated as local runtime cache.

## Scope Boundary

This pass regenerated the final THLB geometry handoff only. It did not build
bundle CSV tables, generate ForestModel XML, run Matrix Builder, assemble a
Patchworks runtime package, or start Phase 5 publication policy work.

The next P4.1c move is to build the first core model-input bundle tables from
this handoff geometry plus the accepted AU, curve, treatment, transition, cedar,
and embedded-identity contracts.
