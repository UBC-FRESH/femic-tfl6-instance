# TFL 6 MP11 Phase 8+ Implementation Roadmap

## Purpose

This P6.6 note converts the reviewed MP11 evidence from Phase 6 and the MP11
figure-extraction handoff from Phase 7 into the next implementation roadmap.
It does not start the MP11-aligned rebuild. It defines the lanes, sequencing,
issue structure, acceptance gates, and evidence boundaries needed before the
Phase 5 teaching runtime can be replaced or revised.

The Phase 5 package remains the accepted public teaching baseline until a
future MP11-aligned package has passed direct source, model-input, XML, Matrix
Builder, runtime, documentation, and scenario-output QA.

## Evidence Inputs

- `planning/tfl6_mp11_source_package_manifest.md`
- `planning/tfl6_mp11_extraction_inventory.csv`
- `planning/tfl6_mp11_land_base_crosswalk.md`
- `planning/tfl6_mp11_netdown_delta_crosswalk.md`
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`
- `planning/tfl6_mp11_model_behavior_crosswalk.md`
- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`
- `planning/tfl6_mp11_figure_extraction_closeout.md`

All MP11 evidence rows remain planning or comparison evidence. No recovered
figure value or MP11 summary value is a model input until a later task
explicitly promotes it through a reviewed implementation artifact.

## Phase 8 Scope

Phase 8 should be the first MP11-aligned implementation foundation phase:

**Phase 8: MP11-Aligned Public-Data Implementation Foundation (`#58`)**

Goal: convert Phase 6/7 MP11 evidence into reviewed public-data contracts and
implementation-ready recipes for the next model rebuild, while preserving the
Phase 5 runtime as the accepted baseline.

Phase 8 should not attempt to rebuild and publish a complete replacement
runtime in one slice. It should make the next rebuild tractable by locking the
public-data contract, source-layer/THLB strategy, AU/yield strategy,
operability/harvest-system/MHA strategy, and behavior/KPI validation targets.

## Proposed Phase 8 Issue Tree

Issue numbers are recorded in `ROADMAP.md` and mirrored here.

### P8.1 Preserve Phase 5 Baseline And Lock MP11 Promotion Rules (`#59`)

Goal: define the governance boundary for moving MP11 evidence into model
contracts.

Subtasks:

- Record Phase 5 runtime archive, manifest, docs, and smoke evidence as the
  active baseline.
- Define promotion states for MP11 values: `planning_only`,
  `comparison_target`, `implementation_candidate`, `accepted_model_contract`,
  `rejected`, and `unavailable_non_public`.
- Define source and figure-evidence rules for when MP11 values can become
  model inputs.
- Define rollback rules if a future MP11 rebuild fails QA.
- Update docs and planning notes to make the baseline boundary visible.

Acceptance:

- No Phase 5 artifact is replaced.
- MP11 promotion states are explicit and reusable by later tasks.
- Every future model-input promotion requires a source, reviewer, and QA path.

### P8.2 Design MP11 Public Source-Layer And THLB Rebuild Contract (`#60`)

Goal: translate P6.3 netdown deltas into a public-data rebuild strategy.

Subtasks:

- Split MP11 land-base categories into public-source, proxy, sensitivity, and
  unavailable WFP-model lanes.
- Decide which public layers can be materialized or refreshed before a THLB
  rebuild.
- Design a LiDAR/LBB/ITI gap strategy that does not fabricate WFP proprietary
  layers from summary tables.
- Define expected GLB/AFLB/THLB checkpoints against MP11 values, including
  tolerances and caveats.
- Draft executable recipe changes only after the contract is reviewed.

Acceptance:

- Public reproducibility limits are explicit.
- The target MP11 THLB `120,099 ha` is treated as a comparison target, not as
  a value to force-fit without source support.
- The next THLB implementation task has a reviewed contract to execute.

### P8.3 Decide MP11 AU/Yield And Managed-Stand Parameter Strategy (`#61`)

Goal: decide how the Phase 5 AU/yield architecture changes in response to
MP11's AU, VDYP, TIPSY, SI, OAF, VRAF, and managed-stand assumptions.

Subtasks:

- Decide whether to adopt MP11 AU era/site-series/treatment identity or keep
  Phase 5 static AU identity with MP11 crosswalk attributes.
- Extract or scope extraction for MP11 Tables 47-60 and related managed-yield
  assumptions.
- Separate public SIBEC/TEM/RESULTS inputs from unavailable LEFI/ITI inputs.
- Define OAF, VRAF, utilization, genetic-gain, fertilization, spacing, and NRL
  parameter surfaces.
- Define curve-regeneration acceptance checks and comparison plots.

Acceptance:

- AU identity and yield-parameter choices are explicit before any curve rebuild.
- MP11 private-data dependencies are isolated.
- Curve rebuild work can proceed without changing treatment or runtime logic
  silently.

### P8.4 Define Operability, Harvest-System, MHA, And Scenario Rules (`#62`)

Goal: convert P6.4/P6.5 findings into model-rule contracts for treatment
eligibility and scenario behavior.

Subtasks:

- Define public-data harvest-system classifier options for ground, cable, and
  helicopter/non-conventional classes.
- Define economic-operability sensitivity rules for helicopter areas.
- Extract or scope extraction for MP11 MHA Tables 71-72.
- Define how 95% CMAI and `350 m3/ha` interact with treatment eligibility.
- Define harvest-flow scenario rules for base case, maximum short-term flow,
  AAC recommendation, and selected sensitivity runs.

Acceptance:

- Treatment eligibility, harvest-system class, and MHA are separate from AU
  identity.
- Scenario rules are explicit before Patchworks outputs are interpreted.
- Aggregate MP11 harvest-system percentages are not used as stand-level
  assignments.

### P8.5 Define MP11 KPI, QA, And Reporting Targets (`#63`)

Goal: define the public reporting surfaces required for MP11-style comparison.

Subtasks:

- Define mandatory outputs for base case, selected sensitivities, and AAC
  recommendation scenarios.
- Define growing-stock, harvest-flow, harvest-system, species, elevation,
  age-class, cedar, old-cedar, old-seral, and block-size reporting surfaces.
- Separate comparison-accepted figure targets from planning-only figure
  evidence.
- Define tolerances for comparing future model outputs to MP11 published
  values.
- Identify which medium-priority Phase 7 figures should be extracted later
  only if needed for QA or docs.

Acceptance:

- KPI targets and validation strengths are explicit.
- Planning-only figure evidence is not mixed with accepted comparison targets.
- Future docs can show MP11 comparison results without overstating precision.

### P8.6 Close Phase 8 And Split Rebuild Phases (`#64`)

Goal: close Phase 8 with implementation-ready contracts and a branch/PR
closeout, then split actual rebuild work into follow-on phases.

Subtasks:

- Confirm roadmap, changelog, planning notes, and issue comments match.
- Confirm validation commands pass.
- Open a PR and merge Phase 8 contracts to `main`.
- Draft follow-on parent issues for THLB/source rebuild, yield rebuild,
  model-input rebuild, runtime rebuild, and MP11 behavior/KPI QA.
- Keep actual rebuild implementation out of Phase 8 unless explicitly approved.

Acceptance:

- Phase 8 ends with reviewed contracts, not a partially rebuilt runtime.
- Follow-on rebuild phases have clear dependency order and acceptance gates.
- Phase 5 remains the accepted baseline until a replacement passes QA.

## Later Phase Sketch

The following phases should be created only after Phase 8 contracts are
accepted or when the maintainer explicitly approves more detailed issue
scaffolding:

- Phase 9: MP11 source-layer and THLB rebuild.
- Phase 10: MP11 AU/yield curve rebuild.
- Phase 11: MP11 model-input bundle and ForestModel XML rebuild.
- Phase 12: MP11 Patchworks runtime, Matrix Builder, and launch/scenario smoke.
- Phase 13: MP11 comparison documentation, teaching update, and release QA.

## Priority Dependencies

1. Preserve Phase 5 baseline and MP11 evidence-promotion rules.
2. Decide public-data reproducibility for source layers, THLB, LiDAR, LBB, and
   ITI gaps.
3. Decide AU/yield identity and managed-stand parameter extraction before
   curve regeneration.
4. Decide harvest-system, MHA, and scenario policy before interpreting
   Patchworks behavior.
5. Define KPI and QA surfaces before publishing comparison claims.
6. Rebuild runtime only after the above contracts are accepted.

## Non-Public Or Unresolved Gaps

- WFP LBB physical operability geometry.
- WFP LiDAR-derived ITI and LEFI attribute surfaces.
- WFP Patchworks model internals and exact objective weights.
- Flight-distance/access assumptions behind helicopter economic operability.
- Full source tables for several published KPI figures.

These gaps should be represented as unavailable, approximated with public
proxies, or handled as sensitivity lanes. They should not be silently
backfilled from MP11 summary values.

## Closeout Boundary

P6.6 is complete when this roadmap, the GitHub Phase 8 parent/child issue
structure, `ROADMAP.md`, `CHANGE_LOG.md`, and issue closeout comments are
synchronized. P6.6 does not begin Phase 8 implementation.
