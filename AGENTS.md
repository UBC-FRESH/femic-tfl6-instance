# AGENTS.md

This file is the working contract for AI coding agents in this repository.

## Project Purpose

`femic-nicffsp-instance` is the standalone FEMIC deployment instance for the
FRST 558 North Island Community Forest / Forest Stewardship Plan teaching case.
The target runtime is Patchworks, using the existing K3Z teaching model as the
closest style and structure reference.

## Current Repo State

The repository is in bootstrap state. It contains:

- FEMIC instance scaffolding under `config/`, `runbooks/`, and runtime folders;
- source payloads under `data/source/nicf_fsp/`;
- planning notes under `planning/`; and
- no accepted compiled model package yet.

Do not describe this repository as a runnable model package until the roadmap
records rebuilt model inputs, Patchworks Matrix Builder output, direct artifact
inspection, and launch/scenario smoke evidence.

## Source Data Handling

- Keep raw source provenance explicit.
- Use lowercase names for new canonical tracked paths.
- Do not publish machine-specific personal paths.
- Do not treat zipped source payloads as usable FEMIC inputs until their
  contents have been inspected and extracted into stable source paths.
- Keep generated model outputs, runtime logs, and scratch artifacts out of git
  unless the roadmap explicitly accepts a compact release payload.

## Planning Workflow

This repo uses an agent-assisted roadmap and GitHub issue workflow, modeled on
`modelwright` and aligned with FEMIC parent-repo practice.

- Keep the current plan in `ROADMAP.md`.
- Keep the immediate edge of work in the `Current Next Steps` section of
  `ROADMAP.md`.
- Record completed deliverables in `CHANGE_LOG.md` with dated bullets.
- Use `planning/` for focused notes and contracts that are too detailed for the
  roadmap.
- Before non-trivial work, update or confirm the roadmap entry that governs it.
- Use GitHub issues with `gh` in tandem with the roadmap.
- Keep roadmap, changelog, commits, and issue comments synchronized as task
  state changes.

## FEMIC/Patchworks Guardrails

- Preserve the FEMIC parent-repo Patchworks semantics:
  `managed` / `unmanaged` means treatment eligibility, while
  `natural` / `treated` means curve provenance.
- Regenerate Patchworks-facing XML before Matrix Builder whenever exporter,
  silviculture, seral, treatment, state, product, account, or curve semantics
  change.
- Do not report Patchworks success from command exit codes alone. Inspect the
  concrete rebuilt outputs that could reveal regressions.
- The K3Z repository is a template/reference, not a blind copy target. Any
  copied assumption must be checked against the NICF FSP source payload and the
  FRST 558 teaching mission.

## Verification

Bootstrap-level validation:

```bash
femic instance validate-spec --spec config/rebuild.spec.yaml
```

Later runnable-model milestones should add, at minimum:

```bash
femic prep validate-case --run-config config/run_profile.nicffsp.yaml --tipsy-config-dir config/tipsy
femic instance rebuild --run-config config/run_profile.nicffsp.yaml --spec config/rebuild.spec.yaml
sphinx-build -b html docs docs/_build/html -W
```

Only run broad rebuilds after the roadmap states the exact question being
answered and the required source inputs are materialized.
