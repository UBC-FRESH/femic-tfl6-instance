# TFL 6 MP11 Inventory, Yield, Operability, And Harvest-System Assumption Crosswalk

## Purpose

This P6.4 note compares MP11 inventory, LiDAR/ITI, yield, operability,
harvest-system, and harvest-rule assumptions against the accepted Phase 5
FEMIC/Patchworks teaching prototype surfaces. It is a planning and
implementation-scoping artifact only. It does not promote any MP11 value
or rule to model-input status.

## Files

- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.csv`
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.json`

## Status

- Rows: `14`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

## Classification Counts

### Delta Classes

- `deferred_phase5_surface_now_has_mp11_target`: `1`
- `mixed_public_and_private_data_update`: `1`
- `mixed_public_proxy_and_private_data_update`: `1`
- `model_constraint_update`: `1`
- `model_contract_update`: `1`
- `model_parameter_update`: `5`
- `model_rule_update`: `1`
- `new_model_parameter_and_cost_proxy_gap`: `1`
- `proxy_replacement_required`: `1`
- `unresolved_wfp_inventory_gap`: `1`

### Implementation Classes

- `analysis_unit_overhaul`: `1`
- `harvest_system_classifier_update`: `1`
- `model_parameter_update`: `1`
- `model_spatial_layer_update`: `1`
- `patchworks_runtime_overhaul`: `1`
- `public_vri_refresh_plus_private_lidar_iti_gap`: `1`
- `scenario_and_account_update`: `1`
- `sensitivity_candidate`: `1`
- `source_layer_and_constraint_overhaul`: `1`
- `tipsy_parameter_library_rebuild`: `1`
- `transition_rule_update`: `1`
- `yield_adjustment_and_retention_rule_update`: `1`
- `yield_pipeline_refresh`: `2`

## Crosswalk

| Assumption | Family | Delta class | Implementation class | Phase 7+ follow-up |
| --- | --- | --- | --- | --- |
| `inventory_vri_lidar_iti` | inventory | `unresolved_wfp_inventory_gap` | `public_vri_refresh_plus_private_lidar_iti_gap` | Refresh public inventory surfaces where possible, then create an explicit LiDAR/ITI gap lane for unavailable WFP-derived attributes. |
| `physical_operability_lbb` | operability | `proxy_replacement_required` | `model_spatial_layer_update` | Replace the placeholder with a reviewed public DEM/slope proxy where possible, and keep WFP LBB as an unavailable reference benchmark unless a shareable layer appears. |
| `economic_operability_helicopter` | operability | `new_model_parameter_and_cost_proxy_gap` | `sensitivity_candidate` | Add a helicopter economic-operability sensitivity lane using public stand volume, species share, and distance/access proxies. |
| `analysis_unit_definition` | analysis_units | `model_contract_update` | `analysis_unit_overhaul` | Decide whether to migrate to MP11 era/site-series/treatment AU identity or preserve Phase 5 static AU identity with MP11 attributes as crosswalk fields. |
| `growth_yield_software` | growth_yield | `model_parameter_update` | `yield_pipeline_refresh` | Regenerate natural and managed curves only in a later implementation phase, after AU identity and MP11 TIPSY parameter extraction are reviewed. |
| `site_index_sibec_tem_lefi` | site_productivity | `mixed_public_and_private_data_update` | `model_parameter_update` | Assess public SIBEC/TEM reproducibility first, then separate unavailable LEFI/LiDAR sensitivity assumptions from base public inputs. |
| `managed_stand_inputs_genetic_gain_fertilization_spacing` | managed_yield | `model_parameter_update` | `tipsy_parameter_library_rebuild` | Extract MP11 Tables 54-57 into a reviewed managed-yield parameter library before any curve rebuild. |
| `oaf_vraf_retention_yield_adjustment` | yield_adjustment | `model_parameter_update` | `yield_adjustment_and_retention_rule_update` | Promote OAF and VRAF only after MP11 managed-yield tables and retention zones are extracted into reviewed parameter surfaces. |
| `utilization_standards` | utilization | `model_parameter_update` | `yield_pipeline_refresh` | Compare MP11 utilization by age class against the MP10 table library before curve regeneration. |
| `non_recoverable_losses` | disturbance_loss | `model_parameter_update` | `scenario_and_account_update` | Create an explicit NRL/disturbance-loss parameter surface and test whether it belongs in yield curves, accounts, harvest-flow comparison, or sensitivity runs. |
| `minimum_harvest_age` | harvest_rules | `model_rule_update` | `transition_rule_update` | Extract MP11 Tables 71-72 and attach MHA to AU/curve records before model-input rebuild. |
| `harvest_system_distribution` | harvest_system | `deferred_phase5_surface_now_has_mp11_target` | `harvest_system_classifier_update` | Build a harvest-system assignment lane and calibrate public proxies against MP11 reported THLB and recent-harvest distributions. |
| `spatial_patchworks_harvest_rules` | model_structure | `model_constraint_update` | `patchworks_runtime_overhaul` | Separate constraints that can be rebuilt from public layers from constraints that require WFP-specific model surfaces. |
| `riparian_terrain_karst_retention_resource_netdowns` | resource_constraints | `mixed_public_proxy_and_private_data_update` | `source_layer_and_constraint_overhaul` | Drive follow-on issue breakdown from the P6.3 netdown delta crosswalk and treat LiDAR/practice-derived categories as explicit reproducibility gaps. |

## Reviewed Rows

### `inventory_vri_lidar_iti`

- Family: `inventory`
- MP11 pages: `266-279`
- Delta class: `unresolved_wfp_inventory_gap`
- Implementation class: `public_vri_refresh_plus_private_lidar_iti_gap`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses VRI updated to December 31, 2023, LiDAR-derived stand heights, Land Base Blocking, and LiDAR-derived Individual Tree Inventory proposals for natural-stand sensitivity work.

Phase 5 comparison surface:

Phase 5 uses public 2025 R1/VRI and VDYP7 source surfaces, with no accepted proprietary LBB, LEFI, or ITI attributes.

Follow-up:

Refresh public inventory surfaces where possible, then create an explicit LiDAR/ITI gap lane for unavailable WFP-derived attributes.

### `physical_operability_lbb`

- Family: `operability`
- MP11 pages: `257-258, 265-267, 297-299`
- Delta class: `proxy_replacement_required`
- Implementation class: `model_spatial_layer_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 physical operability is mapped from the LBB process using LiDAR and professional review; inoperable area removes 21,193 ha from THLB.

Phase 5 comparison surface:

Phase 5 carries a benchmark-calibrated operability placeholder and explicitly defers reviewed ground/cable/heli assignment.

Follow-up:

Replace the placeholder with a reviewed public DEM/slope proxy where possible, and keep WFP LBB as an unavailable reference benchmark unless a shareable layer appears.

### `economic_operability_helicopter`

- Family: `operability`
- MP11 pages: `311-313`
- Delta class: `new_model_parameter_and_cost_proxy_gap`
- Implementation class: `sensitivity_candidate`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 treats conventional land as economically viable and applies flight-distance, minimum volume, and Cw+Fd+Yc component thresholds to helicopter-operable stands; only 20 ha are netted down as non-conventional uneconomic.

Phase 5 comparison surface:

Phase 5 does not implement delivered-cost or harvest-system-specific economic operability logic; it records cost and system splits as later work.

Follow-up:

Add a helicopter economic-operability sensitivity lane using public stand volume, species share, and distance/access proxies.

### `analysis_unit_definition`

- Family: `analysis_units`
- MP11 pages: `348-354`
- Delta class: `model_contract_update`
- Implementation class: `analysis_unit_overhaul`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 managed AUs are defined by AU era, BEC variant, site series, leading species, and silvicultural treatments; natural stands older than 62 years are projected polygon-by-polygon.

Phase 5 comparison surface:

Phase 5 static AUs are BEC/species/SI classes with top-area selection and remapping; MP10 AU codes are retained as parameter evidence, not canonical identity.

Follow-up:

Decide whether to migrate to MP11 era/site-series/treatment AU identity or preserve Phase 5 static AU identity with MP11 attributes as crosswalk fields.

### `growth_yield_software`

- Family: `growth_yield`
- MP11 pages: `272, 348, 355`
- Delta class: `model_parameter_update`
- Implementation class: `yield_pipeline_refresh`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses VDYP 7.33b for natural stands and BatchTIPSY/TIPSY 4.6 for managed and future managed stands.

Phase 5 comparison surface:

Phase 5 uses accepted VDYP first-growth curves and MP10-derived BatchTIPSY parameter evidence; the TIPSY config records MP10 Tables 27-29 as the source library.

Follow-up:

Regenerate natural and managed curves only in a later implementation phase, after AU identity and MP11 TIPSY parameter extraction are reviewed.

### `site_index_sibec_tem_lefi`

- Family: `site_productivity`
- MP11 pages: `272, 278-279, 349-350, 356-357`
- Delta class: `mixed_public_and_private_data_update`
- Implementation class: `model_parameter_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses RESULTS-derived SI for existing managed stands, SIBEC/TEM site series for future stands, and LEFI/LiDAR height-derived SI in sensitivity work.

Phase 5 comparison surface:

Phase 5 uses public VRI/VDYP attributes and an L/M/H SI class contract; it does not implement MP11 SIBEC/site-series future-stand SI or LEFI sensitivity.

Follow-up:

Assess public SIBEC/TEM reproducibility first, then separate unavailable LEFI/LiDAR sensitivity assumptions from base public inputs.

### `managed_stand_inputs_genetic_gain_fertilization_spacing`

- Family: `managed_yield`
- MP11 pages: `262-264, 352-358, 372-375`
- Delta class: `model_parameter_update`
- Implementation class: `tipsy_parameter_library_rebuild`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 differentiates early, recent, and future managed stands, uses planting densities of 900/1000/1200 sph with exceptions, applies future genetic gains, and carries fertilization/spacing markers into managed AUs.

Phase 5 comparison surface:

Phase 5 managed curves come from reviewed MP10 parameter evidence and do not yet encode MP11 managed-stand eras, updated genetic gain table, or MP11 AU markers.

Follow-up:

Extract MP11 Tables 54-57 into a reviewed managed-yield parameter library before any curve rebuild.

### `oaf_vraf_retention_yield_adjustment`

- Family: `yield_adjustment`
- MP11 pages: `258-259, 273, 375-377, 406-409`
- Delta class: `model_parameter_update`
- Implementation class: `yield_adjustment_and_retention_rule_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses standard OAF1 15% and OAF2 5%, and applies a Variable Retention Adjustment Factor shading effect for recent and future managed stands.

Phase 5 comparison surface:

Phase 5 TIPSY metadata carries OAF2 0.95 and MP10-derived OAF/utilization parameter evidence; stand-level retention is not yet implemented as MP11 VRAF.

Follow-up:

Promote OAF and VRAF only after MP11 managed-yield tables and retention zones are extracted into reviewed parameter surfaces.

### `utilization_standards`

- Family: `utilization`
- MP11 pages: `377`
- Delta class: `model_parameter_update`
- Implementation class: `yield_pipeline_refresh`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses 17.5 cm DBH for mature stands older than 120 years, 12.5 cm DBH for immature and future managed stands, 30 cm stump height, 10 cm top DIB, and 50% firmwood standard.

Phase 5 comparison surface:

Phase 5 carries MP10-derived utilization evidence in the TIPSY parameter library and a default 17.5 cm utilization fallback in config.

Follow-up:

Compare MP11 utilization by age class against the MP10 table library before curve regeneration.

### `non_recoverable_losses`

- Family: `disturbance_loss`
- MP11 pages: `379-381, 403`
- Delta class: `model_parameter_update`
- Implementation class: `scenario_and_account_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 accounts for windthrow, insects/disease, fire, and NCLB disturbance; future-stand LRSY is reported after a 1.5% non-recoverable loss reduction.

Phase 5 comparison surface:

Phase 5 runtime release does not expose a reviewed MP11 NRL schedule as a separate model-input contract.

Follow-up:

Create an explicit NRL/disturbance-loss parameter surface and test whether it belongs in yield curves, accounts, harvest-flow comparison, or sensitivity runs.

### `minimum_harvest_age`

- Family: `harvest_rules`
- MP11 pages: `258, 273, 400-404`
- Delta class: `model_rule_update`
- Implementation class: `transition_rule_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 replaces MP10 DBH/harvest-system MHA criteria with 95% CMAI age plus a minimum 350 m3/ha volume requirement; future stands have weighted average MHA 64 years and average volume 586 m3/ha.

Phase 5 comparison surface:

Phase 5 transition/treatment contracts require a future MHA or merchantability rule but do not yet implement MP11's 95% CMAI plus 350 m3/ha table surface.

Follow-up:

Extract MP11 Tables 71-72 and attach MHA to AU/curve records before model-input rebuild.

### `harvest_system_distribution`

- Family: `harvest_system`
- MP11 pages: `265-266, 298, 405`
- Delta class: `deferred_phase5_surface_now_has_mp11_target`
- Implementation class: `harvest_system_classifier_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 reports recent harvest and THLB distributions by ground, cable, and non-conventional systems; THLB is 57.3% ground, 39.6% cable, and 3.1% non-conventional by area.

Phase 5 comparison surface:

Phase 5 requires ground/cable/heli fields in the treatment contract but leaves actual assignment deferred and uses generic CC treatment in the runtime.

Follow-up:

Build a harvest-system assignment lane and calibrate public proxies against MP11 reported THLB and recent-harvest distributions.

### `spatial_patchworks_harvest_rules`

- Family: `model_structure`
- MP11 pages: `257-258, 274, 404-410`
- Delta class: `model_constraint_update`
- Implementation class: `patchworks_runtime_overhaul`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses Patchworks spatial optimization with green-up, adjacency, patch-size, visual-quality, biodiversity, watershed, and old-growth constraints; harvest patch target is 2 ha.

Phase 5 comparison surface:

Phase 5 produces a teaching Patchworks runtime, but some MP11 constraint surfaces remain simplified, fallback, or deferred.

Follow-up:

Separate constraints that can be rebuilt from public layers from constraints that require WFP-specific model surfaces.

### `riparian_terrain_karst_retention_resource_netdowns`

- Family: `resource_constraints`
- MP11 pages: `258, 272-273, 300-310, 406-409`
- Delta class: `mixed_public_proxy_and_private_data_update`
- Implementation class: `source_layer_and_constraint_overhaul`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_assumption_comparison_only`
- Model-input status: `not_model_input`

MP11 summary:

MP11 uses LiDAR stream classification, terrain/DTSM plus LiDAR slope, karst features, OGMAs/WHAs/UWRs, research/PSP/big-tree reserves, and future WTRAs as explicit land-base and constraint assumptions.

Phase 5 comparison surface:

Phase 5 has public-layer and benchmark-calibrated netdown surfaces, but MP11 adds or refines several WFP/LiDAR/practice-based categories.

Follow-up:

Drive follow-on issue breakdown from the P6.3 netdown delta crosswalk and treat LiDAR/practice-derived categories as explicit reproducibility gaps.

## Closeout Boundary

P6.4 confirms that an MP11-aligned model is not a small parameter update.
The future implementation lane needs a source-layer refresh, AU/yield
contract decision, managed-yield parameter extraction, harvest-system
classifier, MHA rule extraction, and Patchworks constraint review. Every
row in this crosswalk remains comparison evidence only until a later
phase explicitly promotes it through reviewed implementation artifacts.
