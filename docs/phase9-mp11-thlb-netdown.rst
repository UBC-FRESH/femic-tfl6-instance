Phase 9 MP11 THLB Netdown
=========================

Purpose
-------

Phase 9 rebuilt the MP11 timber harvesting land base netdown for this public
TFL 6 teaching instance. The accepted lane is the ``p9rf`` resultant-fragment
workflow, not the earlier ``p9r`` partial-area prototype.

This page documents the user-facing logic for the accepted public-data THLB
surface. It is intended for students, collaborators, and maintainers who need
to understand what the model uses, which public data sources were applied, and
where the public teaching instance intentionally diverges from the published
MP11 benchmark because WFP private inputs are unavailable.

Accepted Endpoint
-----------------

The accepted public-data endpoint after the Phase 9R/P9D/P9E repairs is:

.. list-table::
   :header-rows: 1

   * - Checkpoint
     - P9RF area
     - MP11 benchmark
     - Delta
     - Delta percent
   * - Current THLB, MP11 Table 12 Step 290
     - ``122,763.421 ha``
     - ``120,099.000 ha``
     - ``+2,664.421 ha``
     - ``+2.2185%``
   * - Long-term land base, MP11 Table 12 Step 310
     - ``121,336.593 ha``
     - ``118,672.000 ha``
     - ``+2,664.593 ha``
     - ``+2.2453%``

This is close enough for the unrestricted public teaching and research lane.
It is not a claim that the public rebuild reproduces WFP's private Patchworks
model, LiDAR-derived surfaces, proprietary inventory attributes, cultural/TUS
inputs, or unpublished operational decisions.

Why Resultant Fragments Matter
------------------------------

The first P9R prototype retained source polygons and carried net-area
attributes through later overlays. That was useful for diagnostics, but it is
not the spatial fabric required for downstream model inputs. The accepted P9RF
lane physically splits geometry at each spatial deduction. After each step, the
active checkpoint geometry area equals the reported active net area.

This matters because later overlays must intersect the remaining active
geometry, not a source polygon with a uniformly distributed residual area
attribute. The accepted P9RF artifacts therefore provide the spatial basis for
future model-input rebuilds.

Canonical Evidence
------------------

The main tracked audit surfaces are:

- ``config/tsr/mp11_table12_thlb_netdown.recipe.yaml``;
- ``planning/tfl6_mp11_p9rf_table12_resultant_vs_p9r_comparison.{md,csv,json}``;
- ``planning/tfl6_mp11_p9rf_table12_step_*.{md,csv,json}``;
- ``planning/tfl6_mp11_p9d_public_dem_source_manifest.{md,csv,json}``;
- ``planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.{md,csv,json}``;
- ``planning/tfl6_mp11_p9e_public_tsm_source_manifest.{md,csv,json}``; and
- ``planning/tfl6_mp11_p9e_step210_tsm_scenarios.{md,csv,json}``.

Large resultant-fragment GeoPackages are generated checkpoints. They are
review artifacts and model-build inputs, but they are not all tracked in git.

Source Layers And Rules
-----------------------

The public-data implementation uses deterministic spatial or attribute rules
where credible public data exist. It records explicit skips or deferred rows
where MP11 uses sensitive, private, or unavailable sources.

.. list-table::
   :header-rows: 1
   :widths: 12 22 26 40

   * - Step
     - MP11 row
     - Public implementation
     - Rationale and caveat
   * - 010
     - Less Non-forest
     - VRI/R1 attribute review split into forest/non-forest and non-treed
       components.
     - Public VRI can reproduce the forested checkpoint after the reviewed
       Level 1/Level 2 BCLCS split.
   * - 020
     - Existing roads and powerlines
     - Public DRA road/bridge buffer proxy.
     - Existing roads are represented; powerline contribution is not
       separately materialized.
   * - 040
     - Non-productive
     - Public VRI/VDYP productivity proxy.
     - WFP LBB/ITI/LEFI-style productivity evidence is unavailable, so a
       public proxy is locked with a residual caveat.
   * - 060
     - Low sites
     - Public site-index proxy.
     - MP11 uses richer private inventory evidence; public proxy is accepted
       because the step-level delta is small.
   * - 070
     - Inoperable
     - Public volume/operability proxy.
     - WFP physical-operability and private inventory evidence are unavailable.
   * - 090
     - Riparian management
     - FWA streams buffered at the reviewed public proxy width plus FWA lake
       and wetland footprints.
     - MP11 uses LiDAR-classified streams and shoreline logic; public FWA is
       a transparent proxy, not equivalence.
   * - 100
     - Ungulate winter ranges
     - Approved public UWR polygons.
     - Accepted with current-vintage public-data caveat.
   * - 110
     - Legal old growth management areas
     - Current public legal OGMA polygons.
     - Accepted because the public legal geometry is credible; the ordered net
       delta likely reflects vintage, overlap, or private upstream differences.
   * - 120
     - Proposed old growth management areas
     - Oldest-remaining-fragment proxy calibrated to the published net
       deduction.
     - Proposed OGMA geometry is unavailable; this row is accepted as a
       benchmark proxy with explicit source caveat.
   * - 130
     - Legal wildlife habitat areas
     - Public legal WHA overlay.
     - Accepted despite a small absolute residual because public legal WHA is
       the defensible open source.
   * - 140
     - Proposed wildlife habitat areas
     - No deduction.
     - Proposed WHA source is unavailable in the public source stack.
   * - 150
     - Uneconomic
     - No deduction.
     - WFP economic operability source is unavailable; no public equivalent was
       accepted.
   * - 160
     - Deciduous-leading
     - Public VRI species-composition threshold calibrated and reviewed.
     - Accepted as an auditable public inventory rule.
   * - 170
     - Recreation
     - Public recreation overlay.
     - Target area is small; public overlay result is accepted.
   * - 180
     - Known archaeological sites
     - Skipped.
     - Sensitive archaeological source data are intentionally excluded so the
       teaching instance remains unrestricted and public.
   * - 190
     - Existing stand-level reserves
     - Public-data old-seral / reserve proxy.
     - Accepted because it matches the MP11 net deduction closely.
   * - 200
     - Research site
     - Skipped.
     - Sensitive or non-public site source is excluded from the public teaching
       instance.
   * - 210
     - Terrain stability, Class 5
     - Public Terrain Stability Mapping detailed polygons, strict Class V.
     - Source exists and is now applied, but it explains only ``1.425 ha`` of
       the MP11 ``1,993 ha`` row; residual is a public-source coverage and
       semantic gap.
   * - 220
     - LiDAR 90% plus slope
     - Public CDED steep-slope proxy: fragments with at least 75% valid CDED
       pixels at ``>=70%`` slope.
     - Accepted public DEM proxy; CDED is coarser than LiDAR but the step delta
       is only ``-18.295 ha``.
   * - 230
     - Permanent sample plots
     - Public active PSP source clipped to TFL 6.
     - Accepted; public PSP footprint is close to MP11.
   * - 240
     - Big tree reserves
     - Deferred.
     - No accepted public big-tree reserve source has been materialized.
   * - 250
     - Karst
     - Deferred.
     - No accepted public karst source has been materialized. This is the
       largest known remaining public-data gap.
   * - 260
     - Unknown cultural features within Quatsino TUS zone
     - Skipped.
     - Sensitive cultural/TUS data are intentionally excluded from the public
       teaching instance.
   * - 270
     - Future stand-level reserves
     - Public old-seral proxy candidate.
     - Accepted for this public teaching lane because the net deduction is
       within ``1.646 ha`` of MP11, but it remains a proxy for future reserves.
   * - 300
     - Future roads
     - Aspatial area proxy.
     - Future road alignments are unknown. The deduction is an area accounting
       placeholder, not predicted future road geometry.

MP11 Table 12 Comparison
------------------------

The following table reports the accepted P9RF retained area after each MP11
Table 12 row, the row deduction, the MP11 comparison target, and the residual.
For deduction rows, the MP11 target is the published deduction. For checkpoint
rows, it is the published checkpoint area.

.. list-table::
   :header-rows: 1
   :widths: 12 28 15 15 15 15 25

   * - Step
     - Row
     - P9RF retained
     - P9RF deducted
     - MP11 target
     - Delta
     - Status
   * - 020
     - Existing roads and powerlines
     - ``196,232.991``
     - ``3,161.060``
     - ``5,021.000``
     - ``-1,859.940``
     - locked public proxy
   * - 030
     - Total forested
     - ``196,232.991``
     - ``0.000``
     - ``196,233.000``
     - ``-0.009``
     - checkpoint
   * - 040
     - Non-productive
     - ``188,144.665``
     - ``8,088.326``
     - ``8,808.000``
     - ``-719.674``
     - locked public proxy
   * - 050
     - Total productive
     - ``188,144.665``
     - ``0.000``
     - ``187,425.000``
     - ``+719.665``
     - checkpoint
   * - 060
     - Low sites
     - ``178,194.497``
     - ``9,950.168``
     - ``9,927.000``
     - ``+23.168``
     - locked public proxy
   * - 070
     - Inoperable
     - ``157,048.169``
     - ``21,146.328``
     - ``21,193.000``
     - ``-46.672``
     - locked public proxy
   * - 080
     - Total operable
     - ``157,048.169``
     - ``0.000``
     - ``156,305.000``
     - ``+743.169``
     - checkpoint
   * - 090
     - Riparian management
     - ``152,218.332``
     - ``4,829.837``
     - ``5,479.000``
     - ``-649.163``
     - locked public proxy
   * - 100
     - Ungulate winter ranges
     - ``150,173.751``
     - ``2,044.581``
     - ``1,619.000``
     - ``+425.581``
     - locked public overlay
   * - 110
     - Legal OGMA
     - ``140,600.986``
     - ``9,572.766``
     - ``5,491.000``
     - ``+4,081.766``
     - locked public overlay
   * - 120
     - Proposed OGMA
     - ``135,281.007``
     - ``5,319.978``
     - ``5,317.000``
     - ``+2.978``
     - locked proxy
   * - 130
     - Legal WHA
     - ``133,998.658``
     - ``1,282.349``
     - ``414.000``
     - ``+868.349``
     - locked public overlay
   * - 140
     - Proposed WHA
     - ``133,998.658``
     - ``0.000``
     - ``17.000``
     - ``-17.000``
     - source unavailable
   * - 150
     - Uneconomic
     - ``133,998.658``
     - ``0.000``
     - ``20.000``
     - ``-20.000``
     - source unavailable
   * - 160
     - Deciduous-leading
     - ``132,307.081``
     - ``1,691.577``
     - ``1,576.000``
     - ``+115.577``
     - locked public attribute rule
   * - 170
     - Recreation
     - ``132,297.495``
     - ``9.586``
     - ``6.000``
     - ``+3.586``
     - locked public overlay
   * - 180
     - Known archaeological sites
     - ``132,297.495``
     - ``0.000``
     - ``527.000``
     - ``-527.000``
     - skipped sensitive source
   * - 190
     - Existing stand-level reserves
     - ``129,210.103``
     - ``3,087.393``
     - ``3,089.000``
     - ``-1.607``
     - locked public proxy
   * - 200
     - Research site
     - ``129,210.103``
     - ``0.000``
     - ``13.000``
     - ``-13.000``
     - skipped sensitive source
   * - 210
     - Terrain stability, Class 5
     - ``129,208.678``
     - ``1.425``
     - ``1,993.000``
     - ``-1,991.575``
     - locked public TSM proxy
   * - 220
     - LiDAR 90% plus slope
     - ``127,406.973``
     - ``1,801.705``
     - ``1,820.000``
     - ``-18.295``
     - locked public CDED proxy
   * - 230
     - Permanent sample plots
     - ``127,248.067``
     - ``158.906``
     - ``134.000``
     - ``+24.906``
     - locked public PSP proxy
   * - 240
     - Big tree reserves
     - ``127,248.067``
     - ``0.000``
     - ``42.000``
     - ``-42.000``
     - deferred source needed
   * - 250
     - Karst
     - ``127,248.067``
     - ``0.000``
     - ``3,721.000``
     - ``-3,721.000``
     - deferred source needed
   * - 260
     - Unknown cultural/TUS features
     - ``127,248.067``
     - ``0.000``
     - ``453.000``
     - ``-453.000``
     - skipped sensitive source
   * - 270
     - Future stand-level reserves
     - ``122,763.421``
     - ``4,484.646``
     - ``4,483.000``
     - ``+1.646``
     - accepted proxy candidate
   * - 280
     - Total operable reductions
     - ``122,763.421``
     - ``34,284.748``
     - ``36,216.000``
     - ``-1,931.252``
     - checkpoint
   * - 290
     - Current THLB
     - ``122,763.421``
     - ``0.000``
     - ``120,099.000``
     - ``+2,664.421``
     - accepted endpoint
   * - 300
     - Future roads
     - ``121,336.593``
     - ``1,426.829``
     - ``1,427.000``
     - ``-0.171``
     - locked aspatial proxy
   * - 310
     - Long-term land base
     - ``121,336.593``
     - ``0.000``
     - ``118,672.000``
     - ``+2,664.593``
     - accepted endpoint

Known Public-Data Gaps
----------------------

The residual ``+2,664.593 ha`` at Step 310 is mostly explained by data and
semantic differences that are not resolvable from the current unrestricted
public source stack:

- WFP private inventory, LiDAR, ITI/LEFI, DTSM, and Patchworks surfaces are not
  available.
- Sensitive archaeological, cultural, and TUS features are intentionally
  excluded.
- Karst and big-tree reserve rows remain deferred until an accepted public
  source is materialized.
- Proposed WHA, proposed OGMA, future reserves, and future roads include
  planning assumptions that are not fully represented by current public
  geometry.

These gaps are documented so students can understand the difference between a
transparent public teaching model and a private operational planning model.
