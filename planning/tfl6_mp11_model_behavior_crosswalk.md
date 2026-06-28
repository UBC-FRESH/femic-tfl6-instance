# TFL 6 MP11 Model Behavior, Sensitivity, AAC, And KPI Crosswalk

## Purpose

This P6.5 note compares MP11 model-behavior outputs, sensitivity results,
AAC recommendation evidence, and KPI reporting surfaces against the Phase 5
teaching runtime. It is a planning artifact only. It does not claim
equivalence to WFP's unpublished forest estate model and does not promote
any MP11 value to model-input status.

## Files

- `planning/tfl6_mp11_model_behavior_crosswalk.md`
- `planning/tfl6_mp11_model_behavior_crosswalk.csv`
- `planning/tfl6_mp11_model_behavior_crosswalk.json`
- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`

## Headline Values

- Current AAC: `1,362,000 m3/year`
- MP11 Base Case: `1,061,600 m3/year`
- MP11 AAC recommendation: `1,252,700 m3/year`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

## Figure Evidence Status

### `phase7_status`

- `accepted_for_comparison`: `22`
- `deferred_not_extracted`: `20`
- `inventory_context_only`: `5`
- `reviewed_for_planning`: `14`

### `downstream_use`

- `future_optional_review`: `20`
- `phase6_mp11_age_class_planning_only`: `2`
- `phase6_mp11_cedar_planning_only`: `4`
- `phase6_mp11_comparison_only`: `22`
- `phase6_mp11_old_seral_planning_only`: `8`
- `qualitative_context_only`: `5`

### `model_input_status`

- `not_model_input`: `61`

## Behavior Crosswalk

| Behavior | Family | Comparison class | Implementation gap | Follow-up |
| --- | --- | --- | --- | --- |
| `base_case_harvest_level` | base_case | `mp11_numeric_target_without_phase5_equivalent` | `aac_calibrated_runtime_behavior` | Use the MP11 base-case harvest level as a future calibration and QA target after source-layer, AU/yield, MHA, and constraint rebuilds are complete. |
| `alternate_harvest_flows` | harvest_flow | `scenario_design_gap` | `harvest_flow_policy_and_objective_update` | Add explicit harvest-flow scenario definitions and QA metrics after MP11 model inputs are rebuilt. |
| `yield_sensitivity_response` | sensitivity | `sensitivity_suite_missing` | `yield_sensitivity_and_private_inventory_gap` | Build a public-data sensitivity suite and isolate WFP-only LiDAR/ITI/LEFI uplift as an unavailable or explicitly approximated scenario. |
| `policy_and_constraint_sensitivities` | sensitivity | `scenario_design_gap` | `policy_constraint_sensitivity_suite` | Prioritize MHA, harvest-system exclusion, THLB adjustment, and genetic-gain sensitivities because their MP11 effects are numerically clear. |
| `aac_recommendation_bridge` | aac_recommendation | `mp11_numeric_target_without_phase5_equivalent` | `aac_recommendation_scenario_missing` | Treat the AAC recommendation as a high-level target for a future MP11-aligned scenario, gated on inventory/yield and flow-policy decisions. |
| `growing_stock_dynamics` | kpi | `kpi_reporting_gap` | `growing_stock_kpi_reporting` | Add comparable growing-stock reports once MP11-aligned Patchworks outputs exist. |
| `harvest_system_and_operational_kpis` | kpi | `kpi_reporting_and_classifier_gap` | `harvest_system_classifier_and_kpi_reports` | Create public-data harvest-system proxies before attempting MP11-style operational KPI reports. |
| `cedar_age_old_seral_kpis` | kpi | `planning_evidence_only` | `cedar_age_old_seral_reporting_and_policy_gap` | Use planning-only evidence to design reports and stronger validation checks before promoting these KPI families. |

## Scenario Endpoint Snapshot

| Figure | Scenario | Expected m3/year | Delta vs base | Percent vs base | Endpoint QA error |
| --- | --- | ---: | ---: | ---: | ---: |
| Figure 21 | Maintaining Current AAC | 1,055,200 | -6,400 | -0.60% | 0.127% |
| Figure 22 | Maximum short-term | 1,095,500 | 33,900 | 3.19% | 0.008% |
| Figure 23 | Increased Natural Stand Yields | 1,075,300 | 13,700 | 1.29% | 0.018% |
| Figure 24 | Decreased Natural Stand Yields | 1,036,600 | -25,000 | -2.35% | 0.123% |
| Figure 25 | Increased Managed Stand Yields | 1,138,800 | 77,200 | 7.27% | 0.140% |
| Figure 26 | Decreased Managed Stand Yields | 970,900 | -90,700 | -8.54% | 0.110% |
| Figure 29 | Adjusted Iti Volume | 1,079,000 | 17,400 | 1.64% | 0.503% |
| Figure 30 | Adjusted Iti Volume Lidar Height Site Index | 1,095,200 | 33,600 | 3.17% | 0.391% |
| Figure 31 | Lidar Adjusted Yields Reduced Oaf1 | 1,150,300 | 88,700 | 8.36% | 0.095% |
| Figure 32 | Adjusted ITI and LiDAR reduced OAF1 even flow | 1,150,300 | 88,700 | 8.36% | 0.055% |
| Figure 32 | Adjusted ITI and LiDAR reduced OAF1 max short-term | 1,164,200 | 102,600 | 9.66% | 0.079% |
| Figure 33 | No Genetic Gain | 1,004,000 | -57,600 | -5.43% | 0.244% |
| Figure 34 | Full NSOG Order Targets | 1,049,400 | -12,200 | -1.15% | 0.016% |
| Figure 35 | Mha Increased By 10 Years | 956,000 | -105,600 | -9.95% | 0.296% |
| Figure 36 | Mha Decreased By 10 Years | 1,074,300 | 12,700 | 1.20% | 0.352% |
| Figure 37 | Helicopter Operable Land Base Excluded | 1,021,900 | -39,700 | -3.74% | 0.104% |
| Figure 38 | 10% THLB Increases | 1,118,200 | 56,600 | 5.33% | 0.050% |
| Figure 39 | Thlb Decreased By 10 Percent | 953,500 | -108,100 | -10.18% | 0.197% |

## Reviewed Rows

### `base_case_harvest_level`

- Evidence family: `base_case`
- MP11 pages: `82-83, 100-101`
- Comparison class: `mp11_numeric_target_without_phase5_equivalent`
- Implementation gap: `aac_calibrated_runtime_behavior`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

Base Case `1,061,600 m3/year`; current AAC `1,362,000 m3/year`; reported decrease `22.1%`.

MP11 summary:

MP11 Base Case is an even-flow harvest projection over 300 years, net of 1.5% non-recoverable losses, and represents about 90% of adjusted LRSY.

Phase 5 comparison:

Phase 5 has a launch-smoked teaching runtime with generic managed CC harvest signals, but no accepted AAC-equivalent base-case calibration.

Follow-up:

Use the MP11 base-case harvest level as a future calibration and QA target after source-layer, AU/yield, MHA, and constraint rebuilds are complete.

### `alternate_harvest_flows`

- Evidence family: `harvest_flow`
- MP11 pages: `102-104`
- Comparison class: `scenario_design_gap`
- Implementation gap: `harvest_flow_policy_and_objective_update`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

Maintain-current-AAC long-term endpoint `1,055,200`; maximize-short-term first decade `1,147,700` and long-term endpoint `1,095,500` m3/year.

MP11 summary:

MP11 evaluates maintaining current AAC for 10 years and maximizing short-term harvest with controlled mid-term effects.

Phase 5 comparison:

Phase 5 includes a representative max-even-flow smoke mode, but it was a runtime-signal smoke rather than a reviewed MP11-style flow comparison.

Follow-up:

Add explicit harvest-flow scenario definitions and QA metrics after MP11 model inputs are rebuilt.

### `yield_sensitivity_response`

- Evidence family: `sensitivity`
- MP11 pages: `105-123, 142-143`
- Comparison class: `sensitivity_suite_missing`
- Implementation gap: `yield_sensitivity_and_private_inventory_gap`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

Natural +10% `1,075,300`; natural -10% `1,036,600`; managed +10% `1,138,800`; managed -10% `970,900`; ITI/LEFI/OAF1 even-flow `1,150,300`.

MP11 summary:

MP11 is more sensitive to managed-stand yield changes than natural-stand yield changes; LiDAR/ITI/LEFI and reduced OAF1 produce the largest uplift.

Phase 5 comparison:

Phase 5 has reviewed VDYP/TIPSY curve surfaces, but no MP11-style sensitivity suite and no accepted LiDAR/ITI/LEFI input surface.

Follow-up:

Build a public-data sensitivity suite and isolate WFP-only LiDAR/ITI/LEFI uplift as an unavailable or explicitly approximated scenario.

### `policy_and_constraint_sensitivities`

- Evidence family: `sensitivity`
- MP11 pages: `124-141`
- Comparison class: `scenario_design_gap`
- Implementation gap: `policy_constraint_sensitivity_suite`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

No genetic gain `1,004,000`; full NSOG `1,049,400`; MHA +10 `956,000`; MHA -10 `1,074,300`; helicopter excluded `1,021,900`; THLB -10 `953,500`; THLB +10 `1,118,200` m3/year.

MP11 summary:

MP11 tests no genetic gain, full NSOG old-seral targets, MHA +/- 10 years, helicopter exclusion, and THLB +/- 10%.

Phase 5 comparison:

Phase 5 documents these as deferred or scenario-worthy concepts, not as implemented MP11-equivalent sensitivity runs.

Follow-up:

Prioritize MHA, harvest-system exclusion, THLB adjustment, and genetic-gain sensitivities because their MP11 effects are numerically clear.

### `aac_recommendation_bridge`

- Evidence family: `aac_recommendation`
- MP11 pages: `142-143, 157-158`
- Comparison class: `mp11_numeric_target_without_phase5_equivalent`
- Implementation gap: `aac_recommendation_scenario_missing`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

AAC recommendation `1,252,700 m3/year`; uplift from Base Case `191,100 m3/year`; about `1.1%` below the scheduled MP10 decline benchmark.

MP11 summary:

MP11 recommends a step-down LiDAR/ITI/LEFI/OAF1 scenario for the next 10 years after the base-case analysis.

Phase 5 comparison:

Phase 5 has no AAC-recommendation lane and must not be represented as a Chief-Forester-ready or WFP-model-equivalent forecast.

Follow-up:

Treat the AAC recommendation as a high-level target for a future MP11-aligned scenario, gated on inventory/yield and flow-policy decisions.

### `growing_stock_dynamics`

- Evidence family: `kpi`
- MP11 pages: `83, 143`
- Comparison class: `kpi_reporting_gap`
- Implementation gap: `growing_stock_kpi_reporting`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

Base-case total THLB GS min/max `35,088,106`/`41,629,956`; AAC recommendation min/max `37,823,276`/`40,829,741` m3.

MP11 summary:

MP11 reports base-case and AAC-recommendation THLB growing-stock trajectories split by <=120 and >120 year categories.

Phase 5 comparison:

Phase 5 exposes managed/unmanaged area and yield signals, but does not publish MP11-style THLB growing-stock KPI trajectories.

Follow-up:

Add comparable growing-stock reports once MP11-aligned Patchworks outputs exist.

### `harvest_system_and_operational_kpis`

- Evidence family: `kpi`
- MP11 pages: `87-93, 144-152`
- Comparison class: `kpi_reporting_and_classifier_gap`
- Implementation gap: `harvest_system_classifier_and_kpi_reports`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

Base-case harvest-system average is 57% ground, 40% cable, and 3% helicopter; average block size is 19.1 ha; long-term harvested area averages 1,430 ha/year.

MP11 summary:

MP11 reports harvest-system, block-size, harvest-age, harvested-area, volume-per-ha, species-composition, and elevation-band behavior for base-case and AAC scenarios.

Phase 5 comparison:

Phase 5 explicitly defers ground/cable/heli assignment and carries harvest-system placeholders, so MP11 operational KPI comparison is mostly a future reporting gap.

Follow-up:

Create public-data harvest-system proxies before attempting MP11-style operational KPI reports.

### `cedar_age_old_seral_kpis`

- Evidence family: `kpi`
- MP11 pages: `85-86, 153-157`
- Comparison class: `planning_evidence_only`
- Implementation gap: `cedar_age_old_seral_reporting_and_policy_gap`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_model_behavior_comparison_only`
- Model-input status: `not_model_input`

MP11 anchor:

Phase 7 reviewed age-class, cedar, and old-seral figures for planning only; they were not promoted to comparison-accepted status.

MP11 summary:

MP11 reports age-class, cedar, old-cedar, and old-seral trajectories for base-case and AAC-recommendation scenarios.

Phase 5 comparison:

Phase 5 carries cedar signals for teaching/reporting, but no hard cedar reserve, utility-pole-grade, or MP11 old-seral KPI calibration.

Follow-up:

Use planning-only evidence to design reports and stronger validation checks before promoting these KPI families.

## Closeout Boundary

P6.5 confirms that the Phase 5 teaching runtime is structurally useful
but not MP11-behavior-equivalent. Future implementation work must rebuild
or approximate the MP11 source-layer, AU/yield, MHA, harvest-system,
constraint, and scenario-policy surfaces before AAC-style behavior can be
meaningfully compared from model output rather than from MP11 evidence.
