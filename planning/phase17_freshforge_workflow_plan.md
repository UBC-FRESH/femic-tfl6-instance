# Phase 17 FreshForge Workflow Plan

## Purpose

Phase 17 introduces the first TFL6-owned FreshForge workflow document. The
first slice is intentionally narrow: represent the model-build lane as a
FreshForge graph that can be validated, inspected, and planned without adding a
TFL6-specific provider namespace.

The workflow uses the generic FEMIC provider stages. If later work needs
TFL6-specific script orchestration, that code should live in a TFL6-owned
adapter package rather than in `femic.tfl6`.

## Workflow Sequence

The first graph uses this order:

1. validate case;
2. geospatial preflight;
3. compile upstream FEMIC inputs;
4. run BTC/post-TIPSY bundle processing;
5. export the Patchworks XML/fragments package;
6. run Patchworks preflight; and
7. dry-run or explicitly run Matrix Builder.

The initial workflow points at the current MP11 harvest-system candidate
surfaces:

- `config/run_profile.tfl6.yaml`;
- `config/rebuild.spec.yaml`;
- `data/mp11_harvest_system_model_input_bundle/export_compat/`;
- `output/patchworks_tfl6_mp11_harvest_system_candidate/`;
- `config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml`; and
- `models/tfl6_patchworks_model_mp11_harvest_system_candidate/`.

## Follow-On Workflow Families

The agreed FreshForge workflow sequence for TFL6 is:

1. model-build workflow;
2. generic instance materialization/bootstrap workflow;
3. scenario-running and analysis workflows;
4. THLB accepted-pipeline wrapper workflow;
5. TSR/THLB step-sequence planning workflow;
6. THLB input data resolution and materialization workflow; and
7. THLB step planning and stepwise validation workflow.

The THLB stepwise validation lane is intentionally last. It should enforce
bounded one-step validation, explicit evidence artifacts, and immediate stop on
area or ledger mismatch rather than automating scientific judgment.

## Boundaries

- Phase 17 does not implement a `tfl6.*` FreshForge provider.
- Phase 17 does not reroute FEMIC command outputs into FreshForge namespaces.
- FreshForge `v0.1.0a4` does not expose `freshforge run --dry-run`; Phase 17
  uses `freshforge plan` as the non-executing check and leaves full execution
  acceptance to a later lane.
- Phase 17 does not perform a full Matrix Builder acceptance run by default.
- Runtime outputs under `runtime/freshforge/` remain local/generated and must
  not be tracked.
