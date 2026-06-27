# TFL 6 Phase 5 Release QA

## Purpose

This checklist records final release QA for the first TFL 6 teaching runtime
package. It is the Phase 5 closeout evidence surface for issue `#40` under
Phase 5 parent `#15`.

The goal is to prove that the release is public, documented, materializable,
launch-smoked, and honest about its first-release limitations. This checklist
does not reopen model design, THLB netdown, yield curves, Matrix Builder, or
runtime-package construction unless QA exposes a release-blocking defect.

## Release Inputs

- Runtime archive: `releases/tfl6_patchworks_runtime_p5_2.zip`
- Runtime manifest: `releases/tfl6_patchworks_runtime_p5_2_manifest.yaml`
- Public annex remote: `arbutus-s3`
- Runtime launch file inside package:
  `models/tfl6_patchworks_model/analysis/base.pin`
- Representative harvest product:
  `product.HarvestedVolume.managed.Total.CC`
- Release docs:
  - `docs/phase5-runtime-release.rst`
  - `docs/phase5-runtime-quickstart.rst`
  - `docs/phase5-rebuild-provenance.rst`
  - `docs/phase5-scenario-teaching-workflows.rst`
  - `docs/phase5-known-limitations-release-readiness.rst`

## QA Checklist

| ID | Check | Evidence | Result | Notes |
| --- | --- | --- | --- | --- |
| P5.4a | Create release-QA issue and checklist surface. | Issue `#40`; this file; Phase 5 parent `#15` body updated. | Pass | Created before executable QA checks. |
| P5.4b | Verify archive, manifest, and public materialization. | TBD | Pending | Confirm public `arbutus-s3` materialization and manifest checksum consistency. |
| P5.4c | Verify Patchworks launch and baseline signal smoke evidence. | TBD | Pending | Confirm accepted launch/signal evidence remains aligned with the published package. |
| P5.4d | Verify docs build, docs links, and published Pages surface. | TBD | Pending | Sphinx warning-clean plus public documentation availability. |
| P5.4e | Close Phase 5 after QA evidence is recorded. | TBD | Pending | Close issue `#40` and parent `#15` only after QA passes. |

## Deferred Follow-On Scope

The following items are documented follow-on work and do not block the first
teaching release:

- ground/cable/heli harvest-system modeling;
- geometry-backed strategic RMZ replacement;
- outside-AOI NICF expansion implementation;
- cedar-specific reserve or utility-pole-grade policy design;
- VDYP/TIPSY sensitivity projects; and
- production-grade economic modeling.

## Current Status

P5.4a is complete. No archive rematerialization, Patchworks run, or docs
publication check has been executed in this checklist yet. The next bounded
slice is P5.4b archive, manifest, and public materialization verification.
