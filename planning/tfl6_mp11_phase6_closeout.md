# TFL 6 MP11 Phase 6 Closeout

## Purpose

Phase 6 ingested the public TFL 6 Management Plan 11 package and converted it
into reviewed planning evidence for a future MP11-aligned model overhaul. It
did not modify the accepted Phase 5 teaching runtime, model-input bundle,
ForestModel XML, Matrix Builder outputs, or runtime archive.

## Completed Issue Tree

- Parent: `#42` Phase 6: ingest MP11 and plan TFL6 model overhaul.
- `#43` P6.1: archive MP11 source package and extraction manifest.
- `#44` P6.2: extract MP11 tables, figures, sections, assumptions, and
  metadata.
- `#45` P6.3: compare MP11 land base and THLB assumptions against the Phase 5
  prototype.
- `#46` P6.4: compare MP11 inventory, LiDAR/ITI, yield, operability, and
  harvest-system assumptions.
- `#47` P6.5: compare MP11 model behavior, sensitivities, AAC recommendation,
  and KPI outputs.
- `#48` P6.6: write the Phase 8+ implementation roadmap for the MP11-aligned
  model overhaul.

## Tracked Outputs

- `planning/tfl6_mp11_source_package_manifest.md`
- `planning/tfl6_mp11_source_package_manifest.json`
- `planning/tfl6_mp11_document_components.csv`
- `planning/tfl6_mp11_extraction_manifest_fields.csv`
- `planning/tfl6_mp11_extraction_inventory.csv`
- `planning/tfl6_mp11_extraction_inventory_summary.md`
- `planning/tfl6_mp11_extraction_inventory_summary.json`
- `planning/tfl6_mp11_land_base_crosswalk.md`
- `planning/tfl6_mp11_land_base_crosswalk.csv`
- `planning/tfl6_mp11_land_base_crosswalk.json`
- `planning/tfl6_mp11_netdown_delta_crosswalk.md`
- `planning/tfl6_mp11_netdown_delta_crosswalk.csv`
- `planning/tfl6_mp11_netdown_delta_crosswalk.json`
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.csv`
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.json`
- `planning/tfl6_mp11_model_behavior_crosswalk.md`
- `planning/tfl6_mp11_model_behavior_crosswalk.csv`
- `planning/tfl6_mp11_model_behavior_crosswalk.json`
- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`
- `planning/tfl6_mp11_phase8_implementation_roadmap.md`
- `planning/tfl6_mp11_phase6_closeout.md`

## Headline Findings

- MP11 public source package checksum:
  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`.
- MP11 total land base is effectively aligned with the Phase 5 FADM-derived
  AOI after rounding.
- MP11 current THLB is `120,099 ha`, compared with the Phase 5 accepted
  weighted THLB of `139,995.798 ha`.
- The THLB delta is `-19,896.798 ha`, or `-14.21%`.
- MP11 Base Case harvest level is `1,061,600 m3/year`.
- MP11 AAC recommendation evidence records `1,252,700 m3/year`.
- MP11 alignment requires source-layer/THLB, AU/yield, operability,
  harvest-system, MHA, scenario, KPI, and runtime-contract work; it is not a
  small edit to the Phase 5 teaching runtime.

## Phase 8 Handoff

Phase 8 is scaffolded as an implementation-foundation phase, not as a one-step
runtime rebuild:

- Parent: `#58` Phase 8: MP11-aligned public-data implementation foundation.
- `#59` P8.1: preserve Phase 5 baseline and lock MP11 promotion rules.
- `#60` P8.2: design MP11 public source-layer and THLB rebuild contract.
- `#61` P8.3: decide MP11 AU/yield and managed-stand parameter strategy.
- `#62` P8.4: define operability, harvest-system, MHA, and scenario rules.
- `#63` P8.5: define MP11 KPI, QA, and reporting targets.
- `#64` P8.6: close Phase 8 and split rebuild phases.

## Validation

Passed locally before phase closeout:

```bash
python -m ruff check .
sphinx-build -b html docs docs/_build/html -W
```

## Closeout Boundary

Phase 6 leaves every MP11 value as planning or comparison evidence unless a
future phase explicitly promotes it through reviewed model contracts. The Phase
5 teaching runtime remains the accepted baseline until a future MP11-aligned
package passes direct source, model-input, XML, Matrix Builder, runtime,
documentation, and scenario-output QA.
