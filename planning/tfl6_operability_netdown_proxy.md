# TFL 6 Operability Netdown Proxy and Sensitivity Lane

## Purpose

Governing issue: `#20`.

This note records the P2.1a operability design lane. It is planning-only: no
DEM data is materialized, no slope raster is built, no recipe YAML is created,
and no THLB netdown is executed.

Operability should not be treated as a hidden, permanently locked aspatial
deduction. The base-case teaching model still needs rationale-backed
assumptions, but operability is also a strong candidate for student sensitivity
work because it controls which stands enter or leave the THLB through physical
access, economic access, terrain, yarding-system, and timber-value assumptions.

## Source Evidence

### MP10 Information Package

The MP10 information package defines TFL 6 operability classes as a function of
harvesting system, timber quality, terrain stability, and economic
accessibility. The 1999 reclassification was approved by the MoFR Port McNeill
Forest District in September 1998. It separated physically inaccessible areas
from economically marginal conventional and heli areas
(`Ocm`/`Ohm`). The MP10 deduction from productive forest was `12,438 ha`, made
up of `11,600 ha` physically inoperable, `424 ha` marginal conventional, and
`415 ha` marginal heli. The operable subtotal was `134,621 ha`, including
`129,221 ha` conventional and `5,400 ha` heli.

Local extracted-text anchors:

- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:655`
- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:678`

MP10 also says there was no additional terrain-stability netdown beyond areas
identified as inoperable. Class IV and V terrain remained in the THLB in
material proportions, and spatial logging history records showed harvesting had
occurred in both classes. This means "unstable terrain" was not a simple
standalone exclusion in the base-case landbase; it was partly embedded in the
operability inventory and partly handled as sensitivity/context.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:694`

The MP10 analysis dataset assigned logging system from operability class plus
slope class: conventionally operable areas with slope from `0%` to `30%` were
assumed ground-based, conventionally operable areas on steeper slopes were
assumed cable, and heli-operable areas occurred across all slope classes.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:2502`

MP10 minimum-harvest criteria were also tied to harvesting system. The analysis
report says minimum criteria included average stand DBH by harvest system plus
minimum volume per hectare; ground-based stands used `30 cm`, while cable and
heli criteria were higher and were explicitly tested in sensitivity analysis.

Local extracted-text anchors:

- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:9723`
- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:10019`

MP10 Section 5.3 identifies economic access as a major uncertainty. It says the
dataset used a broad economic-operability allowance based on inventory
information rather than detailed cost/value modelling, and that low-volume
mature forest in lower height and stocking classes classified with economic
constraints was excluded in the base case.

Local extracted-text anchors:

- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:9940`
- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:9997`

### MP9 Information Package

MP9 Appendix III gives stronger stand-level clues for reconstructing a teaching
proxy. It describes operability classes using the same general factors:
harvesting system, timber quality, terrain stability, and economic
accessibility. It also reports a 1999 operability reclassification and a
deduction of `12,579 ha` from productive forest, split between physically
inoperable and economically constrained classes.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_9_01_appendix_1_7.txt:1267`

The MP9 yarding-system forest-cover constraints are the most useful proxy
evidence found so far:

- conventional operability included height class `4+`, height class `3` with
  cedar, cypress, Douglas-fir, or spruce as primary species, and nearby height
  class `3` hemlock/balsam types;
- conventional-economic classes included height class `3` hemlock/balsam not
  near better conventional types, stocking class `3` with preferred species,
  and deciduous stands based on local knowledge;
- heli classes used similar height/species/proximity logic for non-conventional
  yarding;
- heli-economic classes included height class `3` preferred species away from
  better heli/conventional types, but excluded some stocking-class `3`
  combinations and pure hemlock/balsam height class `3` stands;
- economically inoperable forest included mature height classes `1` and `2`,
  pure hemlock/balsam height class `3` stocking class `3` open stands, and
  pine-dominant stands; and
- physically inoperable lands included non-productive types, major land-feature
  limitations, and extreme terrain or distance/access constraints.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_9_01_appendix_1_7.txt:4993`

## Available Current Inputs

The accepted current-AOI inventory surfaces already provide several useful
attributes for a proxy design:

- 2025 VRI R1 clipped polygon layer:
  `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`.
- 2025 VDYP7 polygon table:
  `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet`.
- 2025 VDYP7 layer table:
  `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet`.

Candidate VRI/VDYP fields observed during previous read-smoke and field
inspection include:

- height: `proj_height_class_cd_1`, `proj_height_class_cd_2`,
  `est_height_spp1`, `est_height_spp2`, `lorey_height_75`;
- species: `species_cd_1` through `species_cd_6`,
  `species_pct_1` through `species_pct_6`, `line_3_tree_species`;
- stand structure and productivity clues: `crown_closure_class_cd`,
  `proj_age_class_cd_1`, `proj_age_class_cd_2`, `line_4_classes_indexes`,
  `site_index`;
- volume: `live_stand_volume_125`, `live_stand_volume_175`,
  `live_stand_volume_225`, `ws_vol_per_ha_75`, `ws_vol_per_ha_125`,
  `cu_vol_per_ha_125`; and
- join key: `feature_id`.

These surfaces do not carry the historical WFP operability polygons, terrain
stability classes, road-cost model, or yarding-system class directly. A proxy
therefore needs to combine inventory attributes with derived GIS evidence and
benchmark calibration.

## Proxy Design Direction

### Base-Case Lane

The base-case lane should remain benchmark-aware but not purely aspatial. A
reasonable first design is:

1. Treat recovered 1999 WFP operability geometry, if found, as preferred
   evidence.
2. If geometry is not found, build a VRI/VDYP-informed candidate exclusion
   surface using MP9/MP10 inventory clues:
   - low height classes;
   - hemlock/balsam-dominated low/open stands;
   - pine-dominant stands;
   - low volume per hectare;
   - stocking/open-stand proxy from VRI class fields; and
   - harvest-system cost pressure derived from slope and possibly access.
3. Calibrate the base-case removal against the MP10 Table 8 / adjusted
   current-AOI benchmark deduction, while documenting any mismatch.
4. Keep the calibrated proxy explicitly provisional for a teaching model, not
   a claim that the historical WFP operability inventory has been reproduced.

### Sensitivity Lane

The sensitivity lane should expose one or more parameters that students can
vary to move stands into or out of THLB. Candidate parameters include:

- minimum height class for economic operability;
- species group handling for hemlock/balsam, cedar/cypress/Douglas-fir/spruce,
  pine, and deciduous-leading stands;
- minimum volume per hectare by harvest-system proxy;
- threshold for classifying a stand as steep/cable-pressure based on DEM
  slope;
- threshold for classifying a stand as heli/high-cost candidate;
- whether marginal economic classes are included, excluded, or partially
  discounted; and
- whether heli stands are included with a harvest-flow constraint, excluded, or
  treated as a separate scenario lane.

This matches the TSR pattern where THLB netdown and timber-supply sensitivity
analysis commonly tests landbase, operability, volume, and minimum-harvest
assumptions rather than locking all uncertainty into one base-case surface.

## Base-Case Versus Sensitivity Parameters

This table defines the first design boundary between base-case teaching-model
assumptions and student-tunable sensitivity inputs. The default values are not
yet executable recipe parameters; they are the contract that a later recipe
implementation should translate into reviewed config.

| Parameter | Base-case design stance | Student sensitivity knob | Evidence / rationale | Implementation status |
| --- | --- | --- | --- | --- |
| Historical operability geometry | Use recovered 1999 WFP/TFL operability geometry if a reviewed local copy is found; otherwise use the proxy lane below. | Compare proxy-derived THLB against any recovered historical geometry, if supplied later. | MP9/MP10 both identify a 1999 operability reclassification approved by the district. | Preferred source, but not currently materialized. |
| Benchmark calibration | Calibrate the proxy so total operability removal is checked against MP10 Table 8 and the adjusted current-AOI benchmark. | Test relaxed/tighter calibration tolerances around the adjusted benchmark. | MP10 Table 8 provides `12,438 ha` historical operability removal; adjusted current-AOI targets provide teaching validation context. | Planning only; no calibration code yet. |
| Minimum height class | Treat mature height classes `1` and `2` as strong economic-inoperability candidates. Treat height class `3` as conditional on species, stocking/open signal, volume, and slope/access. | Vary the minimum accepted height class or decide whether height class `3` is retained, marginal, or excluded under different species groups. | MP9 identifies mature height classes `1` and `2` as economically inoperable and uses height class `3` in both economic and operable classes. | Requires P2.2 field profiling of VRI height-class fields. |
| Species group | Use preferred coastal operability species groups from MP9: cedar/cypress/Douglas-fir/spruce as stronger economic signals; hemlock/balsam height class `3` as conditional; pine-dominant as inoperability candidate; deciduous based on local/proxy judgment. | Toggle hemlock/balsam height class `3`, pine-dominant, and deciduous-leading handling between retained, marginal, and excluded. | MP9 yarding-system constraints explicitly reference these species groups. MP10 economic-access uncertainty highlights low-valued hembal. | Requires P2.2 species-code grouping. |
| Stocking/open-stand signal | Treat stocking class `3` / open-stand proxy as a marginal or exclusion signal only when paired with lower height, low volume, or lower-value species. | Vary whether stocking/open signal is used as a hard exclusion or a marginal penalty. | MP9 excludes selected stocking class `3` combinations and pure hemlock/balsam height class `3` stocking class `3` open stands. | Requires review of `line_4_classes_indexes` and any usable VRI crown-closure fields. |
| Volume threshold | Use volume per hectare as a calibration and economic-access proxy, not a standalone hard rule in the first design. | Vary minimum volume per hectare by inferred harvest system or species group. | MP10 says economic access was based broadly on inventory information, and minimum harvest criteria often include volume per hectare. | Requires P2.2 profiling of R1/VDYP volume fields. |
| Slope threshold | Preserve MP10's `30%` slope split as the first ground-versus-cable threshold for conventionally operable stands. | Vary slope cutoff `X` in rules such as `p_slope_ge_X >= Y`; candidate `X` values include `30%` for ground/cable split and a higher threshold for high-cost/heli pressure. | MP10 assigns conventionally operable `0-30%` slopes to ground-based systems and steeper conventional slopes to cable. | Requires DEM materialization and zonal statistics. |
| Proportion-of-stand slope threshold | Use stand-level slope proportions, not a single max/mean slope, when classifying steepness pressure. First implementation should expose the threshold `Y` instead of hard-coding it. | Vary `Y` in rules such as "at least `Y` proportion of pixels have slope >= `X%`." | This avoids overreacting to tiny steep inclusions while still allowing students to test steepness assumptions. | Requires DEM-derived percent-slope raster and zonal statistics. |
| Heli inclusion | Keep heli-operable stands in the base-case design as a distinct high-cost harvest-system lane, not an automatic exclusion. | Test no-heli, heli-included-with-constraint, or relaxed-heli scenarios. | MP10 includes `5,400 ha` heli operable land, constrains heli volume, and separately tests excluding heli landbase. | Requires future model/runtime scenario design; do not execute in P2.1a. |
| Marginal economic classes | Treat `Ocm`/`Ohm` semantics as base-case exclusion/calibration candidates, but document them separately from physically inoperable `I`. | Include, exclude, or partially discount marginal economic stands under different market/economic-access scenarios. | MP10 separates physical inoperability from economically marginal conventional and heli classes. | Planning only; no executable class assignment yet. |
| Road/access pressure | Do not include road-distance/access as a hard base-case parameter until DRA roads and any access-cost assumptions are materialized and reviewed. | Later sensitivity can test distance-to-road/access thresholds after road materialization. | MP9 physical inoperability includes extreme terrain/distance/access constraints, but current public road source is not materialized yet. | Defer to P2.1 source materialization and later recipe design. |

First implementation should keep the base-case proxy transparent:

1. classify candidate marginal/economic-inoperable stands from VRI/VDYP
   signals;
2. classify slope/yarding pressure from DEM-derived stand metrics;
3. compare total removal against the adjusted MP10 Table 8 target; and
4. report residual mismatch rather than hiding it with an unexplained area
   plug.

## DEM and Slope Workflow

A later implementation issue should use FEMIC's data-layer discovery functions
to resolve and materialize an appropriate DEM source. The intended workflow is:

1. Resolve a public DEM authority and record publication/version metadata.
2. Materialize only the TFL 6 AOI subset or a minimal AOI-plus-buffer subset.
3. Reproject/align to the accepted EPSG:3005 TFL 6 working CRS as needed.
4. Derive a percent-slope raster clipped to the TFL 6 AOI.
5. Compute zonal statistics by VRI stand polygon, keyed by `feature_id`.
6. Store stand-level metrics such as:
   - mean slope;
   - maximum slope;
   - `p_slope_ge_30`;
   - `p_slope_ge_50`; and
   - optional area-weighted slope-bin proportions.
7. Test rules of the form:
   - `p_slope_ge_X >= Y` for steep/cable-pressure classification;
   - `p_slope_ge_X >= Y` plus low volume or low preferred-species signal for
     marginal economic classification; and
   - alternate `X` and `Y` values as student sensitivity inputs.

No DEM or slope artifact is accepted by this planning note.

## DEM Discovery Evidence

This P2.1a resolver slice was metadata-only. It did not download DEM data,
clip rasters, build slope rasters, or compute zonal statistics.

Commands:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'Digital Elevation Model' `
  'BC DEM' `
  'TRIM DEM' `
  'CDEM' `
  'Canadian Digital Elevation Model' `
  'Provincial Digital Elevation Model' `
  'LiDAR DEM' `
  'BC elevation raster' `
  'Terrain Resource Information Management DEM' `
  'Forest Analysis Inventory DEM slope' `
  --limit 10 `
  --summary-csv runtime\logs\p2_1a_dem_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1a_dem_bcdc_manifest.json

..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'DEM 1:20,000 British Columbia' `
  'CDED 1:50,000 British Columbia' `
  'CDED 1:250,000 British Columbia' `
  'BC geographic warehouse elevation' `
  'BC DEM raster' `
  'TRIM elevation' `
  'TRIM contours' `
  'elevation contours British Columbia' `
  'digital terrain model British Columbia' `
  'bare earth DEM British Columbia' `
  'slope raster British Columbia' `
  'LidarBC DEM' `
  --limit 10 `
  --summary-csv runtime\logs\p2_1a_dem_targeted_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1a_dem_targeted_bcdc_manifest.json
```

Resolver findings:

| Candidate | Dataset / object | Access evidence | Use decision |
| --- | --- | --- | --- |
| LidarBC / open LiDAR | `LiDAR`; `LidarBC - Open LiDAR Data Portal`; open LiDAR data portal, open LiDAR data index, and map grid resources | Resolver returned direct application/index resources. The generic `LiDAR` catalogue record is under the Open Government Licence - British Columbia; the portal/index record is application-mediated rather than a simple stable raster URL. | Primary high-resolution discovery route for a future slope raster, subject to coverage and tile/materialization review for the TFL 6 AOI. Use only after a bounded materialization plan identifies the needed AOI tiles and storage convention. |
| CDED DEM | `Digital Elevation Model for British Columbia - CDED - 1:250,000`; zipped DEM CDED files by map letterblock | Resolver returned a direct public zip root under `https://pub.data.gov.bc.ca/datasets/175624/`; Open Government Licence - British Columbia. | Coarse fallback or smoke-test DEM only. It is likely too coarse for defensible stand-level yarding/slope-bin classification, but it may be useful to prove the raster-processing pipeline before LiDAR tile materialization. |
| RESULTS slope/aspect/elevation | `WHSE_FOREST_VEGETATION.RSLT_OPEN_SLOPE_ASPCT_ELEV_SVW` | Resolver returned a WFS-queryable BCGW service candidate for opening-level slope/aspect/elevation attributes. | Attribute clue only. It is not a continuous DEM and should not replace stand-level slope zonal statistics, but it may be useful later for comparing derived slope bins against reported opening-level terrain attributes. |
| TRIM contour lines/points | `WHSE_BASEMAPPING.TRIM_CONTOUR_LINES`; `WHSE_BASEMAPPING.TRIM_CONTOUR_POINTS` | Resolver found WFS-queryable TRIM contour surfaces, but access metadata is government/access-only. | Not the first public teaching route. Contours are also an inferior path for raster slope when DEM/LiDAR sources are available. |
| Ready-made provincial slope raster | No useful public candidate found by the resolver queries. | The targeted slope-raster queries returned no accepted slope-raster source. | Build slope from an accepted DEM rather than relying on a discovered slope raster. |

Current DEM decision:

- Treat LidarBC/open LiDAR as the preferred future source for a defensible
  stand-level slope surface, if TFL 6 coverage and tile materialization are
  practical.
- Treat CDED 1:250,000 as a coarse fallback/smoke-test raster, not as the
  preferred teaching-model operability source.
- Do not use RESULTS opening slope/aspect/elevation as a DEM substitute.
- Do not use TRIM contours as the first route unless later DEM materialization
  is blocked.
- The next implementation slice for DEM work should be a materialization plan,
  not a download: identify the LidarBC index/grid source, intersect it with
  TFL 6, estimate tile count/volume, and decide whether to materialize LiDAR
  tiles directly or first prove the slope workflow on a coarse CDED subset.

## Later DEM Materialization Plan Requirements

A later DEM materialization issue should answer these questions before any
download begins:

1. Which LidarBC index or grid layer is the authoritative tile-selection
   surface for TFL 6?
2. Which tiles intersect the TFL 6 AOI plus any necessary processing buffer?
3. What are the estimated tile count, total download size, working-disk
   footprint, and expected derived raster size?
4. Are the relevant tiles available as open/public artifacts suitable for a
   teaching instance public-data lane?
5. Should the first implementation prove the slope/zonal-stat pipeline on a
   coarse CDED subset before LiDAR tile materialization?
6. What canonical tracked/annexed paths should hold raw DEM tiles, clipped DEM,
   slope raster, and stand-level zonal-stat tables?
7. Which QA checks are required: CRS, pixel size, nodata handling, AOI coverage,
   slope-unit check, zonal-stat row count keyed to `feature_id`, and spot checks
   against visible terrain?

Until those questions are answered, P2.1a accepts only the design requirement
for DEM-derived slope metrics, not any DEM source artifact.

## Open Decisions

- How to parse `line_4_classes_indexes` into a defensible stocking/open-stand
  signal.
- How to express the MP9 "near better operability types" concept. Possible
  proxies include adjacency, distance to higher-quality stands, distance to
  roads, or no first-lane implementation.
- Whether road distance/access should be part of P2.1a or a later source-layer
  enhancement after Digital Road Atlas materialization.
- How closely the adjusted Table 8 benchmark should constrain the teaching
  base case when the active current AOI includes post-2011 TFL 6 boundary
  additions.

## Non-Goals

- No DEM fetch or clipping.
- No slope raster or zonal-stat computation.
- No recipe YAML.
- No THLB execution.
- No model-input, ForestModel/XML, Matrix Builder, or Patchworks runtime work.
