# P12.1 MP11 Runtime Build Execution Plan

Phase 12 is the first MP11 lane that builds Patchworks runtime artifacts. It
starts from the Phase 11 candidate model-input/XML handoff and then runs Matrix
Builder, assembles a candidate runtime package, launches Patchworks directly,
and smoke-tests representative scenarios before any Phase 13 release claim.

P12.1 does not run Matrix Builder. It creates the runtime-build issue tree,
records the command surface for P12.2, and verifies that the Phase 11 handoff
inputs exist before runtime outputs are created.

## Issue Tree

- Parent: `#69` Phase 12 MP11 Patchworks runtime and scenario smoke.
- P12.1: `#114` launch MP11 runtime-build execution plan and child issues.
- P12.2: `#115` run Matrix Builder from MP11 candidate XML and fragments.
- P12.3: `#116` assemble MP11 candidate Patchworks runtime package.
- P12.4: `#117` smoke-test direct MP11 Patchworks launch.
- P12.5: `#118` smoke-test MP11 base and sensitivity scenarios.
- P12.6: `#119` close MP11 runtime smoke and hand off Phase 13 QA.

## Phase 11 Inputs

P12 consumes these generated, ignored local inputs:

- `data/mp11_model_input_bundle/export_compat/bridge_manifest.json`
- `output/patchworks_tfl6_mp11_candidate/forestmodel.xml`
- `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp`
- `output/patchworks_tfl6_mp11_candidate/fragments/fragments.dbf`

Tracked provenance for those inputs:

- `planning/tfl6_mp11_phase11_closeout.{csv,json,md}`
- `planning/tfl6_mp11_phase12_runtime_handoff.{csv,json,md}`
- `planning/tfl6_mp11_forestmodel_xml_generation_qa.{csv,json,md}`
- `planning/tfl6_mp11_candidate_bundle_build_summary.{csv,json,md}`

## P12.2 Matrix Builder Command

Use the MP11 candidate config added in P12.1:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks matrix-build `
  --instance-root external/femic-tfl6-instance `
  --config config/patchworks.runtime.mp11_candidate.windows.yaml `
  --run-id tfl6_mp11_candidate_p12_2_matrix_build
```

The config intentionally writes tracks to:

```text
models/tfl6_patchworks_model_mp11_candidate/tracks/
```

P12.2 must inspect the generated track surfaces directly before reporting
success. Matrix Builder success alone is not enough.

## Required P12.2 Inspection

At minimum, inspect:

- `features.csv`;
- `protoaccounts.csv`;
- `accounts.csv`;
- products and curve references emitted into the tracks;
- treatment/group/stratum signal expected from the candidate XML;
- Matrix Builder manifest, stdout, and stderr logs; and
- any warnings, parser errors, missing field reports, or zero-signal accounts.

If Matrix Builder fails, P12.2 should write a blocker report instead of
continuing to runtime assembly.

## Generated Output Boundaries

Runtime outputs belong under ignored generated roots:

- Matrix Builder tracks:
  `models/tfl6_patchworks_model_mp11_candidate/tracks/`
- blocks and topology:
  `models/tfl6_patchworks_model_mp11_candidate/blocks/`
- launch/runtime manifests:
  `models/tfl6_patchworks_model_mp11_candidate/metadata/`
- scenario smoke outputs:
  `models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runs/`

Do not overwrite the accepted Phase 5 runtime package under
`models/tfl6_patchworks_model/`.

## Carried Caveats

- This is an MP11 candidate scaffold, not a final release model.
- The Phase 5 stand universe and treatment/transition scaffold are reused.
- P9RF source/THLB caveats remain visible until a later source-layer rebuild.
- The 27 accepted Phase 10R Table 57 rows materialize as 18 active MP11
  candidate curves because duplicate rows map to canonical AU identities.
- Tables 54/55 remain excluded until a public-safe AU-code mapping exists.
- Harvest-system assignment remains deferred comparison metadata, not a
  stand-level treatment classifier.

## P12.1 Acceptance

P12.1 is complete when:

- child issues `#114` through `#119` exist and are linked from the roadmap;
- `config/patchworks.runtime.mp11_candidate.windows.yaml` points to MP11
  candidate XML/fragments and candidate tracks;
- the Phase 11 handoff inputs are present locally;
- Matrix Builder/runtime/scenario output roots are still absent before P12.2;
- `ROADMAP.md`, `CHANGE_LOG.md`, and issue comments are synchronized; and
- no Matrix Builder run has been performed in P12.1.
