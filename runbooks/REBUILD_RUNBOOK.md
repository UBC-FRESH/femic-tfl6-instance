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
