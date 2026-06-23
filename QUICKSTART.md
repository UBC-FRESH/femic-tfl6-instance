# NICF FSP FEMIC Instance Quickstart

1. Validate CLI install:
   `femic --help`
2. Validate the rebuild-spec scaffold:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
3. Inspect and extract the source AOI/LU zip payloads listed in
   `planning/source_inventory.md`.
4. Update `config/run_profile.nicffsp.yaml` after the authoritative AOI layer
   is available as a stable tracked file.
5. Validate geospatial runtime dependencies:
   `femic prep geospatial-preflight`
6. Validate case paths:
   `femic prep validate-case --run-config config/run_profile.nicffsp.yaml --tipsy-config-dir config/tipsy`
7. Run compile workflow from this instance root only after the roadmap accepts
   the source-normalization boundary.
