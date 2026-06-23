# NICF FSP FEMIC Instance Quickstart

1. Validate CLI install:
   `femic --help`
2. Validate the rebuild-spec scaffold:
   `femic instance validate-spec --spec config/rebuild.spec.yaml`
3. Review the accepted source AOI/LU paths in `planning/source_inventory.md`.
4. Confirm `config/run_profile.nicffsp.yaml` points at the accepted AOI and LU
   reference source paths.
5. Validate geospatial runtime dependencies:
   `femic prep geospatial-preflight`
6. Validate case paths:
   `femic prep validate-case --run-config config/run_profile.nicffsp.yaml --tipsy-config-dir config/tipsy`
7. Run compile workflow from this instance root only after the roadmap accepts
   the source-normalization boundary.
