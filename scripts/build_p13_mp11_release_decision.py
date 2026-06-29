"""Build Phase 13 MP11 release-status decision outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = Path("planning") / "tfl6_mp11_phase13_release_decision.csv"
JSON_PATH = Path("planning") / "tfl6_mp11_phase13_release_decision.json"
MD_PATH = Path("planning") / "tfl6_mp11_phase13_release_decision.md"

DECISION = "supplement_phase5"

REQUIRED_EVIDENCE = {
    "scenario_comparison": Path("planning/tfl6_mp11_phase13_scenario_comparison.md"),
    "kpi_caveat_report": Path("planning/tfl6_mp11_phase13_kpi_caveat_report.md"),
    "candidate_runtime_docs": Path("docs/phase13-mp11-candidate-runtime.rst"),
    "archive_materialization_qa": Path(
        "planning/tfl6_mp11_phase13_archive_materialization_qa.md"
    ),
    "archive_manifest": Path(
        "releases/tfl6_mp11_candidate_runtime_p13_4_manifest.yaml"
    ),
    "phase12_runtime_closeout": Path("planning/tfl6_mp11_phase12_runtime_closeout.md"),
}


def _evidence_status() -> dict[str, bool]:
    return {
        name: (REPO_ROOT / path).is_file() for name, path in REQUIRED_EVIDENCE.items()
    }


def _rows(evidence: dict[str, bool]) -> list[dict[str, str]]:
    evidence_status = (
        "present" if all(evidence.values()) else "missing_required_evidence"
    )
    return [
        {
            "id": "release_decision",
            "decision": DECISION,
            "status": evidence_status,
            "evidence": "P13.1-P13.4 evidence surfaces",
            "rationale": (
                "MP11 candidate is smoke-tested, documented, and archive-manifested, "
                "but not published or clean-checkout materialized."
            ),
        },
        {
            "id": "phase5_baseline",
            "decision": "retain_as_accepted_baseline",
            "status": "accepted",
            "evidence": "Phase 5 release QA and public archive remain unchanged",
            "rationale": "P13 does not replace the accepted Phase 5 public teaching runtime.",
        },
        {
            "id": "mp11_candidate_runtime",
            "decision": "documented_candidate_supplement",
            "status": "accepted_for_candidate_teaching_and_comparison",
            "evidence": "Phase 12 smoke pass, P13 docs, P13 archive QA",
            "rationale": (
                "Candidate runtime is useful for MP11-aligned teaching and comparison "
                "without claiming WFP model equivalence."
            ),
        },
        {
            "id": "replace_phase5",
            "decision": "not_selected",
            "status": "blocked_by_release_gates",
            "evidence": "P13.2 caveats and P13.4 materialization boundary",
            "rationale": (
                "Candidate archive is local/unpublished, clean-checkout materialization "
                "is pending, maintainer base scenario lacks reproducible export, and "
                "MP11 caveats remain."
            ),
        },
        {
            "id": "experimental_only",
            "decision": "not_selected",
            "status": "too_conservative_for_current_evidence",
            "evidence": "Phase 12 smoke pass and P13 documentation/archive QA",
            "rationale": (
                "The candidate has enough build, launch, scheduling, docs, and archive "
                "QA evidence to supplement Phase 5 as a labelled candidate."
            ),
        },
        {
            "id": "clean_checkout_materialization",
            "decision": "defer_until_publication",
            "status": "pending",
            "evidence": "planning/tfl6_mp11_phase13_archive_materialization_qa.md",
            "rationale": (
                "Materialization is not required for the supplement decision because the "
                "candidate is not replacing the public Phase 5 runtime archive."
            ),
        },
        {
            "id": "phase13_closeout",
            "decision": "complete",
            "status": "ready_after_pr_issue_sync",
            "evidence": "roadmap, changelog, PR, and issue comments",
            "rationale": "P13.1 through P13.5 are complete once this change is merged.",
        },
    ]


def _write_csv(rows: list[dict[str, str]]) -> None:
    with (REPO_ROOT / CSV_PATH).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "decision", "status", "evidence", "rationale"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_json(rows: list[dict[str, str]], evidence: dict[str, bool]) -> None:
    payload = {
        "decision": DECISION,
        "phase5_baseline_status": "accepted_public_runtime_baseline",
        "mp11_candidate_status": "candidate_supplement_for_teaching_and_comparison",
        "replace_phase5": False,
        "experimental_only": False,
        "required_evidence_present": evidence,
        "rows": rows,
    }
    (REPO_ROOT / JSON_PATH).write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def _write_md(rows: list[dict[str, str]], evidence: dict[str, bool]) -> None:
    lines = [
        "# TFL 6 MP11 Phase 13 Release Decision",
        "",
        "P13.5 decides the relationship between the completed Phase 5 public "
        "teaching/runtime baseline and the smoke-tested MP11 candidate runtime.",
        "",
        "## Decision",
        "",
        f"- release_decision: `{DECISION}`",
        "- phase5_baseline_status: `accepted_public_runtime_baseline`",
        "- mp11_candidate_status: `candidate_supplement_for_teaching_and_comparison`",
        "- replace_phase5: `False`",
        "- experimental_only: `False`",
        "",
        "The MP11 candidate runtime supplements Phase 5. It can be used as a "
        "labelled MP11-aligned candidate for comparison, advanced teaching, and "
        "future release work. It does not replace the Phase 5 public runtime "
        "baseline because the candidate archive is local and unpublished, "
        "clean-checkout materialization has not been proven, the maintainer "
        "interactive base scenario still needs reproducible export, and MP11 "
        "source/constraint caveats remain.",
        "",
        "## Evidence Surface",
        "",
        "| Evidence | Present | Path |",
        "| --- | --- | --- |",
    ]
    for name, path in REQUIRED_EVIDENCE.items():
        lines.append(f"| `{name}` | `{evidence[name]}` | `{path.as_posix()}` |")

    lines.extend(
        [
            "",
            "## Decision Rows",
            "",
            "| ID | Decision | Status | Evidence | Rationale |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['id']}` | `{row['decision']}` | `{row['status']}` | "
            f"{row['evidence']} | {row['rationale']} |"
        )

    lines.extend(
        [
            "",
            "## Closeout Boundary",
            "",
            "- P13.1 scenario comparison tables are complete.",
            "- P13.2 KPI/caveat report is complete.",
            "- P13.3 public Sphinx documentation is complete.",
            "- P13.4 archive/materialization QA is complete.",
            "- P13.5 records `supplement_phase5` and closes Phase 13 after PR and issue sync.",
            "",
            "The Phase 5 archive remains the accepted public release package. The MP11 "
            "candidate archive remains a local candidate payload until a future "
            "publication/materialization task annexes or otherwise publishes it and "
            "proves no-credential clean-checkout access.",
        ]
    )
    (REPO_ROOT / MD_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    evidence = _evidence_status()
    missing = [name for name, exists in evidence.items() if not exists]
    if missing:
        missing_text = ", ".join(missing)
        raise FileNotFoundError(
            f"Missing required P13 decision evidence: {missing_text}"
        )
    rows = _rows(evidence)
    _write_csv(rows)
    _write_json(rows, evidence)
    _write_md(rows, evidence)
    print(f"wrote {MD_PATH.as_posix()} with decision {DECISION}")


if __name__ == "__main__":
    main()
