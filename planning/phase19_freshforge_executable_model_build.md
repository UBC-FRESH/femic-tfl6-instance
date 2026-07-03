# Phase 19: FreshForge Executable Model-Build Acceptance

## Purpose

Phase 19 promotes the TFL6 FreshForge model-build workflow from a planning
contract into an explicit executable acceptance lane. The workflow runs from the
parent FEMIC checkout and uses generic FEMIC FreshForge provider stages through
Patchworks Matrix Builder.

## Workflow Ownership

The workflow remains instance-owned:

```text
workflows/freshforge/tfl6_model_build_workflow.yaml
```

FEMIC core must not grow a `tfl6.*` provider for this phase. TFL6-specific
orchestration, if later needed, should live in an instance-owned adapter package.

## Parent-Checkout Execution Contract

The workflow is intended to run from the parent FEMIC repository root. Each node
uses:

```yaml
instance_root: external/femic-tfl6-instance
```

Other paths remain relative to that instance root, including run config,
Patchworks config, bundle, checkpoint, output, runtime log, and artifact paths.

The first workflow node should run generic case preflight through
`femic prep validate-case`. Rebuild-spec validation remains a separate operator
check:

```powershell
python -m femic instance validate-spec --instance-root external/femic-tfl6-instance --spec config/rebuild.spec.yaml
```

## Operator Flow

Operators should use the parent FEMIC workflow discovery helper first:

```powershell
python -m femic freshforge workflows list
python -m femic freshforge workflows commands external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml
```

Then run the non-mutating FreshForge checks:

```powershell
freshforge validate external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml
freshforge inspect external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml
freshforge plan external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml
```

The executable acceptance command is:

```powershell
freshforge run external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml --workdir runtime/freshforge --namespace tfl6/model-build --json
```

`freshforge plan` is non-mutating. `freshforge run` executes FEMIC, BTC, and
Patchworks stages.

## Acceptance Checks

Phase 19 should inspect:

- FreshForge run records under the parent `runtime/freshforge/` tree.
- FEMIC runtime logs and manifests under `runtime/logs/`.
- Exported Patchworks package content under
  `output/patchworks_tfl6_mp11_harvest_system_candidate/`.
- Matrix Builder manifest.
- Compiled Patchworks tracks under
  `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks`.
- TFL6 Git status after execution.

If tracked model outputs changed, treat them as reviewable rebuild output rather
than incidental runtime noise.
