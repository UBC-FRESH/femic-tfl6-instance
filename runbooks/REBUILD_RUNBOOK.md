# NICF FSP Rebuild Runbook

Use this file as the operator-facing rebuild procedure for this instance.
The repository is currently at bootstrap stage. Full case preflight and
Patchworks rebuild commands are blocked until the AOI source zip has been
inspected and extracted into stable runtime input paths.

## Required Inputs
- `config/run_profile.tfl6.yaml`
- `config/rebuild.spec.yaml`
- `config/rebuild.allowlist.yaml`
- `data/source/nicf_fsp/` raw source payloads
- extracted AOI/LU layers, once accepted by the source-normalization task
- Patchworks licensing/runtime for Patchworks-facing rebuild steps

## Bootstrap Validation
```bash
femic instance validate-spec --spec config/rebuild.spec.yaml
```

## Standard Rebuild Commands
```bash
femic instance rebuild \
  --run-config config/run_profile.tfl6.yaml \
  --spec config/rebuild.spec.yaml \
  --baseline config/rebuild.baseline.json \
  --allowlist config/rebuild.allowlist.yaml
```

## Evidence to Archive
- `runtime/logs/instance_rebuild_report-<run_id>.json`
- Referenced manifests/logs listed under `artifact_references`.

## FreshForge Model-Build Workflow

Phase 17 adds a FreshForge workflow document at
`workflows/freshforge/tfl6_model_build_workflow.yaml`. Use it to validate,
inspect, and plan the TFL6 model-build graph from the instance root:

```bash
freshforge providers
freshforge validate workflows/freshforge/tfl6_model_build_workflow.yaml
freshforge inspect workflows/freshforge/tfl6_model_build_workflow.yaml
freshforge plan workflows/freshforge/tfl6_model_build_workflow.yaml
```

The Phase 17 workflow uses generic `femic.*` provider stages. It does not add a
`tfl6.*` provider namespace and does not make FreshForge materialize DataLad
payloads. The current FreshForge release does not expose `freshforge run --dry-run`;
full execution through BTC and Patchworks should be treated as a separate
acceptance step.

## FreshForge Materialization Workflow

Phase 18 adds a parent-checkout materialization workflow at
`workflows/freshforge/tfl6_materialization_workflow.yaml`. Run it from the
parent FEMIC checkout root, not from inside this instance directory:

```bash
freshforge providers
freshforge validate external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml
freshforge inspect external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml
freshforge plan external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml
freshforge run external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml --workdir runtime/freshforge --namespace tfl6/materialization --json
```

`freshforge plan` is non-mutating. `freshforge run` performs real submodule,
Python environment, DataLad, and git-annex work, enables `arbutus-s3`,
materializes the configured TFL6 paths, audits `models/` remote coverage, and
writes a local report under the parent `runtime/freshforge/` tree.

## Evidence Refresh Step (Release Prep)
```bash
femic instance refresh-reference-evidence --reference-root .
```
After refresh, verify:
- `evidence/reference_rebuild_report.latest.json` exists,
- `status` is `ok`,
- `regression_gate` booleans are all false.

## Local Notes
- Do not run full rebuild as proof of model readiness until
  `config/run_profile.tfl6.yaml` references extracted source layers rather
  than raw zip payloads.
- Document case-specific overrides, expected warnings, and accepted deltas here.

## Species-Surface Diagnostics (When Total Looks OK but Species Look Empty)
```bash
  femic instance account-surface \
  --config config/patchworks.runtime.windows.yaml \
  --output runtime/logs/account_surface-<run_id>.json
```
After running, verify in the JSON/report:
- `diagnosis.total_ok_species_empty_signature` is `false`.
- If `true`, follow `diagnosis.recommended_next_checks` before changing allowlists.
