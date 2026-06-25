# TFL 6 THLB Smoke-Lane Plan

## Purpose

This note starts P2.4 by defining the first executable THLB recipe/scaffold and
smoke-run boundary for TFL 6.

Governing issue: `#24`.

P2.4b was a planning slice only. P2.4c added the first tracked recipe
scaffolds under `config/tsr/`, but still did not run THLB netdown, fetch source
layers, build DEM/slope products, generate model inputs, or build Patchworks
runtime artifacts.

## Existing FEMIC Recipe Convention

Until a dedicated TFL/general-FMU recipe wrapper exists, the first smoke lane
should use the existing FEMIC reviewed TSR recipe convention because it already
has CLI, status, audit, and workbench guardrails:

| Artifact | Planned TFL 6 path | Notes |
| --- | --- | --- |
| Source-layer recipe | `config/tsr/source_layers.recipe.yaml` | Instance-local reviewed source-layer scaffold created in P2.4c. |
| THLB netdown recipe | `config/tsr/thlb_netdown.recipe.yaml` | First THLB scaffold created in P2.4c; preserves MP10 row order and P2.3 statuses. |
| THLB status report | `config/tsr/thlb_netdown.status.md` | Review/status surface for scaffold/build. |
| Runtime status report | `runtime/logs/tsr/` | Runtime-only logs; do not track by default. |
| Smoke output checkpoint | `data/tsr/tfl6_thlb_smoke_checkpoint.feather` | Planned first smoke output; track only if accepted by later issue review. |
| Smoke audit | `config/tsr/tfl6_thlb_smoke.audit.json` | Planned first smoke audit if compact and reviewable. |

P2.4c created the two recipe scaffold files under these paths. P2.4d must
validate the scaffold and record the exact bounded smoke-run command, stop-line,
outputs, and acceptance checks before P2.4e execution.

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

## P2.4c Scaffold Status

P2.4c is complete:

- `config/tsr/source_layers.recipe.yaml` lists the already-materialized TFL 6
  source artifacts needed by the first smoke lane;
- `config/tsr/thlb_netdown.recipe.yaml` contains one parent step and one
  scaffolded step for each MP10 Table 4 row from `tfl6_nd_000` through
  `tfl6_nd_210`;
- the scaffold keeps attribute, provisional spatial overlay, aspatial fallback,
  context-only, and deferred-sensitivity statuses visible;
- the scaffold loads through FEMIC's TSR recipe loaders; and
- no recipe execution, source fetch, DEM/slope derivation, model-input
  generation, XML, Matrix Builder, or Patchworks runtime work occurred.

The next bounded slice is P2.4d validation/readiness: record the exact
non-executing validation command set, the future smoke-run command, stop-line,
expected outputs, and acceptance checks before P2.4e execution.

## P2.4d Checkpoint Input Format Note

FEMIC issue `UBC-FRESH/femic#203` records the parent-code support needed for
this smoke lane: explicit THLB checkpoint inputs may be Feather or readable
vector datasets such as GeoPackage. The older Feather checkpoint convention is
still useful for large repeated TSA29 restart/debug cycles, but it is not a
raw-input requirement for TFL 6.

For this instance, the first P2.4e smoke command should use the accepted R1
GeoPackage directly as the explicit checkpoint/accounting surface:

```powershell
& .\.venv\Scripts\python.exe -m femic tsr thlb-netdown-run `
  --instance-root external/femic-tfl6-instance `
  --thlb-netdown-recipe-path config/tsr/thlb_netdown.recipe.yaml `
  --checkpoint-path data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg `
  --output-path data/tsr/tfl6_thlb_smoke_checkpoint.feather `
  --audit-path config/tsr/tfl6_thlb_smoke.audit.json `
  --execution-mode reconstructed `
  --parallel-mode serial
```

P2.4d still needs to validate the scaffold and record acceptance checks before
this command is executed in P2.4e.

## Non-Goals

- No source fetches.
- No THLB netdown execution in this slice.
- No DEM/slope materialization or operability zonal statistics.
- No model-input, XML, Matrix Builder, or Patchworks runtime work.
- No final THLB reconstruction claim from the first smoke lane.
