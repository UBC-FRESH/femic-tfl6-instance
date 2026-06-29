# TFL 6 MP11 Phase 13 Release Decision

P13.5 decides the relationship between the completed Phase 5 public teaching/runtime baseline and the smoke-tested MP11 candidate runtime.

## Decision

- release_decision: `supplement_phase5`
- phase5_baseline_status: `accepted_public_runtime_baseline`
- mp11_candidate_status: `candidate_supplement_for_teaching_and_comparison`
- replace_phase5: `False`
- experimental_only: `False`

The MP11 candidate runtime supplements Phase 5. It can be used as a labelled MP11-aligned candidate for comparison, advanced teaching, and future release work. It does not replace the Phase 5 public runtime baseline because the candidate archive is local and unpublished, clean-checkout materialization has not been proven, the maintainer interactive base scenario still needs reproducible export, and MP11 source/constraint caveats remain.

## Evidence Surface

| Evidence | Present | Path |
| --- | --- | --- |
| `scenario_comparison` | `True` | `planning/tfl6_mp11_phase13_scenario_comparison.md` |
| `kpi_caveat_report` | `True` | `planning/tfl6_mp11_phase13_kpi_caveat_report.md` |
| `candidate_runtime_docs` | `True` | `docs/phase13-mp11-candidate-runtime.rst` |
| `archive_materialization_qa` | `True` | `planning/tfl6_mp11_phase13_archive_materialization_qa.md` |
| `archive_manifest` | `True` | `releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml` |
| `phase12_runtime_closeout` | `True` | `planning/tfl6_mp11_phase12_runtime_closeout.md` |

## Decision Rows

| ID | Decision | Status | Evidence | Rationale |
| --- | --- | --- | --- | --- |
| `release_decision` | `supplement_phase5` | `present` | P13.1-P13.4 evidence surfaces | MP11 candidate is smoke-tested, documented, and archive-manifested, but not published or clean-checkout materialized. |
| `phase5_baseline` | `retain_as_accepted_baseline` | `accepted` | Phase 5 release QA and public archive remain unchanged | P13 does not replace the accepted Phase 5 public teaching runtime. |
| `mp11_candidate_runtime` | `documented_candidate_supplement` | `accepted_for_candidate_teaching_and_comparison` | Phase 12 smoke pass, P13 docs, P13 archive QA | Candidate runtime is useful for MP11-aligned teaching and comparison without claiming WFP model equivalence. |
| `replace_phase5` | `not_selected` | `blocked_by_release_gates` | P13.2 caveats and P13.4 materialization boundary | Candidate archive is local/unpublished, clean-checkout materialization is pending, maintainer base scenario lacks reproducible export, and MP11 caveats remain. |
| `experimental_only` | `not_selected` | `too_conservative_for_current_evidence` | Phase 12 smoke pass and P13 documentation/archive QA | The candidate has enough build, launch, scheduling, docs, and archive QA evidence to supplement Phase 5 as a labelled candidate. |
| `clean_checkout_materialization` | `defer_until_publication` | `pending` | planning/tfl6_mp11_phase13_archive_materialization_qa.md | Materialization is not required for the supplement decision because the candidate is not replacing the public Phase 5 runtime archive. |
| `phase13_closeout` | `complete` | `ready_after_pr_issue_sync` | roadmap, changelog, PR, and issue comments | P13.1 through P13.5 are complete once this change is merged. |

## Closeout Boundary

- P13.1 scenario comparison tables are complete.
- P13.2 KPI/caveat report is complete.
- P13.3 public Sphinx documentation is complete.
- P13.4 archive/materialization QA is complete.
- P13.5 records `supplement_phase5` and closes Phase 13 after PR and issue sync.

The Phase 5 archive remains the accepted public release package. The MP11 candidate archive remains a local candidate payload until a future publication/materialization task annexes or otherwise publishes it and proves no-credential clean-checkout access.
