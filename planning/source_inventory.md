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

## BCGW Landscape Unit Clip Zip Inventory

Inspection date: 2026-06-23

Source:
`data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip`

Order notes:

- Order ID: `2572861`
- Order date: `20260623`
- Feature type: `Landscape Units of British Columbia - Current`
- Source directory noted by order file: `RMP_LU_SVW`

Zip contents:

| Path in zip | Size bytes | Notes |
| --- | ---: | --- |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.cpg` | 5 | Encoding metadata |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.dbf` | 25774 | Attribute table |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.prj` | 489 | Projection metadata |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.shp` | 2122796 | Polygon geometry |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.shx` | 316 | Shape index |
| `Contents of Order.txt` | 303 | DataBC order summary |
| `README.txt` | 426 | DataBC download/licence notice |
| `licence.txt` | 275 | BC Data Catalogue licence notice |
| `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW_metadata.json` | 9494 | BCGW metadata |
| `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW_metadata.html` | 15194 | BCGW metadata |

Layer summary:

- Candidate layer: `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.shp`
- Feature count: `27`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(778342.188, 528411.500, 990334.625, 680314.312)`
- Geometry validity: `27` valid, `0` invalid
- Total measured area in EPSG:3005: `1489608.005 ha`

Landscape unit names and measured area:

| LU name | Biodiversity emphasis | Area ha |
| --- | --- | ---: |
| Artlish | Intermediate | 16207.928 |
| Bonanza | Intermediate | 45710.608 |
| Brooks | Low | 38203.204 |
| Broughton | Low | 87908.649 |
| Eliza | Low | 56765.240 |
| Gilford | Low | 92764.025 |
| Holberg | Low | 45020.737 |
| Kaouk | Intermediate | 29656.299 |
| Kashutl | Low | 91834.101 |
| Keogh | Low | 64281.620 |
| Klaskish | High | 28848.336 |
| Lower Nimpkish | Low | 82079.594 |
| Mahatta | Low | 59062.085 |
| Malcolm | Low | 41731.272 |
| Marble | Intermediate | 56286.499 |
| Nahwitti | Intermediate | 43172.007 |
| Nasparti | Low | 21213.956 |
| Neroutsos | Low | 31079.820 |
| Nigei | Low | 46468.310 |
| San Josef | Intermediate | 195967.476 |
| Shushartie | High | 20285.114 |
| Tahsish | Intermediate | 28772.463 |
| Tsitika | High | 35910.103 |
| Tsulquate | Intermediate | 25638.715 |
| Upper Nimpkish | Intermediate | 120083.281 |
| Walker | NA | 64856.499 |
| Zeballos | Low | 19800.065 |

Overlap with the `NICF_FDU_2024` AOI candidate:

| FDU candidate name | Matching BCGW LU | FDU candidate area ha | Full LU area ha | Difference ha |
| --- | --- | ---: | ---: | ---: |
| Holberg | Holberg | 41649.362 | 45020.737 | 3371.375 |
| Keogh | Keogh | 50693.492 | 64281.620 | 13588.129 |
| Marble | Marble | 55455.538 | 56286.499 | 830.961 |
| Nahwitti | Nahwitti | 17477.455 | 43172.007 | 25694.552 |
| Shushartie | Shushartie | 15681.191 | 20285.114 | 4603.923 |
| Tsulquate | Tsulquate | 23205.472 | 25638.715 | 2433.244 |

Interpretation:

- The LU zip is a broader BCGW landscape-unit clip with `27` full LU features,
  not a narrow three-LU package.
- The six `NICF_FDU_2024` features align by name with six full BCGW LU records:
  Holberg, Keogh, Marble, Nahwitti, Shushartie, and Tsulquate.
- Each FDU candidate feature is equal to or smaller than its corresponding full
  BCGW LU, so `NICF_FDU_2024` appears to be a clipped FDU/AOI surface derived
  from LU boundaries rather than the full LU boundary layer.
- The initial project note mentions three relevant LUs, but the inspected
  spatial payloads currently expose six named FDU/LU overlaps. Do not close the
  relevant-LU decision until the FSP PDF is checked against these layer names.
