# Phase 18 FreshForge materialization overlay

Phase 18 adds the first TFL6-owned FreshForge materialization workflow. It uses
the parent FEMIC `femic.materialization` provider and is run from the parent
FEMIC checkout, not from a standalone TFL6-only clone.

The workflow captures the deterministic materialization ritual that users
typically miss: initialize the TFL6 submodule, use the parent `.venv`, install
FEMIC with FreshForge support, initialize and enable the TFL6 `arbutus-s3`
git-annex remote, materialize required TFL6 paths, audit model payload remote
coverage, and write a FreshForge materialization report.

Phase 18 does not add a `tfl6.*` provider, does not change the TFL6 model-build
workflow, and does not implement MKRF, K3Z, or TSA29 materialization overlays.
