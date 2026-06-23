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
