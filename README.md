# femic-nicffsp-instance

Standalone FEMIC teaching instance for the FRST 558 North Island Community
Forest / Forest Stewardship Plan case.

## Purpose

This repository will host the Patchworks model package and rebuild workflow for
the expanded NICF FSP student case. The case starts from the existing K3Z
teaching model style, but scales the area of interest from the small K3Z
community forest tenure to the surrounding Forest Stewardship Plan area.

The teaching mission is being designed around two active management questions:

- cedar allocation and value: represent cedar cultural-reserve and utility-pole
  production signals clearly enough for student scenario design; and
- K3Z expansion: provide a bounded pool of candidate unallocated areas from
  which student groups can recommend an expansion package that supports an
  approximate 8,000 m3/year AAC increase.

## Current Status

This is a bootstrap snapshot. It contains source payload inventory, FEMIC
instance scaffolding, and the first build-plan boundary. It is not yet a
compiled or runnable Patchworks model package.

## Source Payloads

Initial source files are tracked under `data/source/nicf_fsp/`:

- `nicf_fsp_amendment_3_spatial.zip`
- `bcgw_lu_clip_2026_06.zip`
- `nicf_forest_stewardship_plan_2020.pdf`

See `planning/source_inventory.md` for original filenames, hashes, and the
first interpretation boundary.

## Workflow

This repository uses the same control-surface pattern as recent FRESH agent-led
projects:

- `AGENTS.md` is the working contract for coding agents.
- `ROADMAP.md` is the active plan and next-step tracker.
- `CHANGE_LOG.md` is the append-only project narrative.
- `planning/` contains focused design and provenance notes.
- GitHub Issues carry active workflow state and should be kept synchronized with
  roadmap and changelog entries.

## FEMIC Rebuild Entry Points

The initial scaffold is present but not yet accepted as runnable:

```bash
femic instance validate-spec --spec config/rebuild.spec.yaml
```

Case preflight and rebuild commands should wait until the AOI zip is inspected,
the boundary layer is extracted into a stable tracked path, and
`config/run_profile.nicffsp.yaml` is updated from placeholder to real source
paths.
