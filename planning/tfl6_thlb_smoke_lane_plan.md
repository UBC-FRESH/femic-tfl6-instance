# TFL 6 THLB Smoke-Lane Plan

## Purpose

This note starts P2.4 by defining the first executable THLB recipe/scaffold and
smoke-run boundary for TFL 6.

Governing issue: `#24`.

This is a P2.4 planning slice only. It does not create executable recipe YAML,
run THLB netdown, fetch source layers, build DEM/slope products, generate model
inputs, or build Patchworks runtime artifacts.

## Existing FEMIC Recipe Convention

Until a dedicated TFL/general-FMU recipe wrapper exists, the first smoke lane
should use the existing FEMIC reviewed TSR recipe convention because it already
has CLI, status, audit, and workbench guardrails:

| Artifact | Planned TFL 6 path | Notes |
| --- | --- | --- |
| Source-layer recipe | `config/tsr/source_layers.recipe.yaml` | Instance-local reviewed source-layer contract. |
| THLB netdown recipe | `config/tsr/thlb_netdown.recipe.yaml` | First executable THLB scaffold; must preserve MP10 row order and P2.3 statuses. |
| THLB status report | `config/tsr/thlb_netdown.status.md` | Review/status surface for scaffold/build. |
| Runtime status report | `runtime/logs/tsr/` | Runtime-only logs; do not track by default. |
| Smoke output checkpoint | `data/tsr/tfl6_thlb_smoke_checkpoint.feather` | Planned first smoke output; track only if accepted by later issue review. |
| Smoke audit | `config/tsr/tfl6_thlb_smoke.audit.json` | Planned first smoke audit if compact and reviewable. |

P2.4 may later create recipe YAML under these paths, but this slice only
defines the boundary.

## First Smoke-Lane Scope

The first executable smoke lane should be a full ordered skeleton with
provisional/fallback rows visible, not a hidden partial netdown. It may execute
only after recipe YAML exists and the command/stop-line are recorded.

Required first-lane properties:

- preserve MP10 Table 4 row order from `tfl6_nd_000` through `tfl6_nd_210`;
- use accepted R1 geometry as the complete area accounting universe;
- expose whether each row is R1-only, VDYP-joined, spatial overlay,
  aspatial fallback, context-only, or deferred sensitivity;
- report gross candidate area before overlap removal for every executable
  attribute/spatial rule;
- report ordered marginal area for every deduction row;
- report cumulative area at every checkpoint row;
- keep provisional/review-required rows visible in status and audit outputs;
- keep aspatial fallback rows visible with their deduction values;
- compare outputs to scaled current-AOI benchmarks; and
- warn if any R1 polygon is dropped because a joined VDYP table is missing.

## Candidate Step Execution Classes

| Step class | First smoke-lane treatment |
| --- | --- |
| `tfl6_nd_000`, `030`, `050`, `070`, `160`, `170`, `190`, `210` | Checkpoint/report rows only. |
| `tfl6_nd_010`, `040`, `140` | Attribute rules from accepted R1/VDYP fields using P2.2c candidates. |
| `tfl6_nd_020`, `080`, `090`, `100`, `120`, `130` | Provisional spatial overlays from materialized P2.1 source layers, with filters/buffers exposed as recipe parameters. |
| `tfl6_nd_110`, `150`, `180` | Explicit aspatial fallback rows for the first base lane. |
| `tfl6_nd_060` | Do not implement a spatial operability proxy in the first generic smoke lane unless P2.4 explicitly narrows to operability. Use a visible benchmark-calibrated placeholder or keep as deferred sensitivity. |
| `tfl6_nd_200` | Context-only future-road row; exclude from current THLB execution. |

## Bounded P2.4 Subtasks

P2.4 should proceed in small slices:

1. **P2.4a**: open/link the P2.4 child issue under Phase 2 parent `#12`.
2. **P2.4b**: record this smoke-lane plan without creating recipe YAML or
   executing THLB netdown.
3. **P2.4c**: create the first recipe YAML scaffold under `config/tsr/`
   without executing it.
4. **P2.4d**: run syntax/schema/readiness validation against the scaffold and
   record the exact bounded smoke-run command, stop-line, outputs, and
   acceptance checks.
5. **P2.4e**: execute the first bounded smoke run only after recording the
   exact command, stop-line, expected outputs, and acceptance checks.
   Inspect the produced checkpoint/audit/status artifacts and record
   benchmark/tolerance findings before deciding whether P2.4 is complete or
   needs another repair slice.

## Non-Goals

- No source fetches.
- No recipe YAML creation in this slice.
- No THLB netdown execution in this slice.
- No DEM/slope materialization or operability zonal statistics.
- No model-input, XML, Matrix Builder, or Patchworks runtime work.
- No final THLB reconstruction claim from the first smoke lane.
