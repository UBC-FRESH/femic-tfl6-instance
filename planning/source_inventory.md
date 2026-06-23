# Source Inventory

## Initial Payloads

| Tracked path | Original uploaded filename | SHA-256 | Notes |
| --- | --- | --- | --- |
| `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` | `NICF FSP amend #3 spatial.zip` | `de3776cda77d056390ffdee03aed6e3a914501a4c2c8adc34ba8481e02bbabcc` | Candidate source for the Forest Stewardship Plan amendment AOI. Contents still need layer-level inspection. |
| `data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip` | `BCGW_LU_Clip_06-2026.zip` | `03477133df626104a60e07699fdb6025a712af1a0a6a710ca5958d44792c0a47` | Candidate source for the Landscape Unit boundaries referenced by the FSP. Contents still need layer-level inspection. |
| `data/source/nicf_fsp/nicf_forest_stewardship_plan_2020.pdf` | `NICF-Forest-Stewardship-Plan-2020-2.pdf` | `9bccd37a9666b4b1262f54afcb152bbbe9ec0475435cdc53434656194bdc3895` | FSP document used to interpret AOI/LU context and management constraints. |

## Interpretation Boundary

These files are raw source payloads only. The next task is to inspect the zip
contents, identify authoritative layers, record CRS and geometry properties,
and extract canonical source layers into stable lowercase paths.

Do not point FEMIC runtime config at zip payloads as if they were ready-to-use
case inputs.

## NICF FSP Amendment Spatial Zip Inventory

Inspection date: 2026-06-23

Source:
`data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip`

Zip contents:

| Path in zip | Size bytes | Notes |
| --- | ---: | --- |
| `NICF FSP Shapefiles/NICF_FDU_2024.dbf` | 7148 | Attribute table |
| `NICF FSP Shapefiles/NICF_FDU_2024.prj` | 466 | Projection metadata |
| `NICF FSP Shapefiles/NICF_FDU_2024.sbn` | 204 | Spatial index |
| `NICF FSP Shapefiles/NICF_FDU_2024.sbx` | 132 | Spatial index |
| `NICF FSP Shapefiles/NICF_FDU_2024.shp` | 686436 | Polygon geometry |
| `NICF FSP Shapefiles/NICF_FDU_2024.shx` | 148 | Shape index |

Layer summary:

- Candidate layer: `NICF FSP Shapefiles/NICF_FDU_2024.shp`
- Feature count: `6`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(849931.438, 580387.812, 928536.312, 653037.313)`
- Geometry validity: `6` valid, `0` invalid
- Total measured area in EPSG:3005: `204162.510 ha`

Feature labels and measured area:

| Label | Landscape unit name | Biodiversity emphasis | Area ha |
| --- | --- | --- | ---: |
| `FDU  1 Holberg LU` | Holberg | Low | 41649.362 |
| `FDU 2 Keogh LU` | Keogh | Low | 50693.492 |
| `FDU 3 Marble LU` | Marble | Intermediate | 55455.538 |
| `FDU 4 Nahwitti LU` | Nahwitti | Intermediate | 17477.455 |
| `FDU 5 Tsulquate LU` | Tsulquate | Intermediate | 23205.472 |
| `FDU 6 Shushartie LU` | Shushartie | High | 15681.191 |

Interpretation:

- This zip contains a single shapefile family, but that shapefile is not a
  single dissolved AOI polygon. It is a six-feature FDU/LU-style layer.
- Treat `NICF_FDU_2024.shp` as the current authoritative AOI candidate only,
  pending cross-check against the FSP document and the separate LU boundary zip.
- Do not extract or wire this layer into `config/run_profile.nicffsp.yaml` until
  the accepted runtime boundary convention is decided: either a dissolved FSP
  AOI, selected FDU/LU features, or a preserved multi-feature FDU boundary.
