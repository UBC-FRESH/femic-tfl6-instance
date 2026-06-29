"""Build Phase 13 MP11 scenario comparison tables."""

from __future__ import annotations

import csv
import json
import statistics
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"

FIGURE2_REVIEW = PLANNING / "tfl6_mp11_figure2_review_manifest.json"
SCENARIO_QA = PLANNING / "tfl6_mp11_scenario_smoke_qa.json"
PHASE12_CLOSEOUT = PLANNING / "tfl6_mp11_phase12_runtime_closeout.json"
MODEL_BEHAVIOR = PLANNING / "tfl6_mp11_model_behavior_crosswalk.csv"
SCENARIO_ENDPOINTS = PLANNING / "tfl6_mp11_model_behavior_scenario_endpoints.csv"

TARGET_SUMMARY = (
    ROOT
    / "models/tfl6_patchworks_model_mp11_candidate/analysis"
    / "p12_5_harvest_smoke200k/scenario/targetSummary.csv"
)

OUT_SUMMARY_CSV = PLANNING / "tfl6_mp11_phase13_scenario_comparison.csv"
OUT_PERIOD_CSV = PLANNING / "tfl6_mp11_phase13_scenario_period_comparison.csv"
OUT_JSON = PLANNING / "tfl6_mp11_phase13_scenario_comparison.json"
OUT_MD = PLANNING / "tfl6_mp11_phase13_scenario_comparison.md"

BASE_TARGET = "product.HarvestedVolume.managed.Total.CC"
FLOW_TARGET = "flow.even.product.HarvestedVolume.managed.Total.CC"

MP11_BASE_CASE = 1_061_600.0
MP11_CURRENT_AAC = 1_362_000.0
MP11_BASE_DECREASE = 300_400.0
MP11_ADJUSTED_LRSY = 1_182_900.0
MAINTAINER_INTERACTIVE = 1_150_000.0
MP11_DECLARED_THLB_HA = 120_099.0
P9RF_CANDIDATE_THLB_HA = 122_763.421


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _pct_delta(value: float, reference: float) -> float:
    return ((value - reference) / reference) * 100.0


def _load_runtime_period_rows() -> list[dict[str, Any]]:
    rows = [row for row in _read_csv(TARGET_SUMMARY) if row["TARGET"] == BASE_TARGET]
    period_rows: list[dict[str, Any]] = []
    for row in rows:
        period_width = float(row["PERIODWIDTH"])
        current_period_volume = float(row["CURRENT"])
        annual_volume = current_period_volume / period_width if period_width else 0.0
        period_rows.append(
            {
                "period": int(row["PERIOD"]),
                "year": int(row["YEAR"]),
                "period_width": period_width,
                "candidate_period_volume_m3": current_period_volume,
                "candidate_annual_volume_m3_per_year": annual_volume,
                "mp11_base_case_m3_per_year": MP11_BASE_CASE,
                "delta_vs_mp11_base_m3_per_year": annual_volume - MP11_BASE_CASE,
                "pct_delta_vs_mp11_base": _pct_delta(annual_volume, MP11_BASE_CASE)
                if MP11_BASE_CASE
                else 0.0,
                "evidence_strength": "tracked_runtime_output",
                "candidate_source": str(TARGET_SUMMARY.relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "mp11_source": "planning/tfl6_mp11_figure2_review_manifest.json",
                "notes": "P12.5 smoke target output; not the maintainer interactive base scenario.",
            }
        )
    return period_rows


def _summary_row(
    comparison_id: str,
    label: str,
    value: float,
    source: str,
    evidence_strength: str,
    evidence_role: str,
    caveat: str,
    release_implication: str,
) -> dict[str, Any]:
    return {
        "comparison_id": comparison_id,
        "label": label,
        "value_m3_per_year": value,
        "delta_vs_mp11_base_m3_per_year": value - MP11_BASE_CASE,
        "pct_delta_vs_mp11_base": _pct_delta(value, MP11_BASE_CASE),
        "delta_vs_adjusted_lrsy_m3_per_year": value - MP11_ADJUSTED_LRSY,
        "pct_delta_vs_adjusted_lrsy": _pct_delta(value, MP11_ADJUSTED_LRSY),
        "source": source,
        "evidence_strength": evidence_strength,
        "evidence_role": evidence_role,
        "caveat": caveat,
        "release_implication": release_implication,
    }


def build_comparison() -> dict[str, Any]:
    figure2 = _read_json(FIGURE2_REVIEW)
    scenario_qa = _read_json(SCENARIO_QA)
    phase12 = _read_json(PHASE12_CLOSEOUT)
    behavior_rows = _read_csv(MODEL_BEHAVIOR)
    endpoints = _read_csv(SCENARIO_ENDPOINTS)
    period_rows = _load_runtime_period_rows()
    comparable_runtime_rows = [row for row in period_rows if row["period"] > 0]
    annual_values = [
        row["candidate_annual_volume_m3_per_year"] for row in comparable_runtime_rows
    ]

    runtime_mean = statistics.mean(annual_values)
    runtime_min = min(annual_values)
    runtime_max = max(annual_values)
    runtime_final = comparable_runtime_rows[-1]["candidate_annual_volume_m3_per_year"]

    thlb_delta_ha = P9RF_CANDIDATE_THLB_HA - MP11_DECLARED_THLB_HA
    thlb_delta_pct = _pct_delta(P9RF_CANDIDATE_THLB_HA, MP11_DECLARED_THLB_HA)

    summary_rows = [
        _summary_row(
            "mp11_base_case",
            "WFP MP11 base case",
            MP11_BASE_CASE,
            "Figure 2 review plus MP11 text/Table 11 context; PDF page 82, Appendix A page 18",
            "tracked_mp11_table_or_text",
            "comparison_target",
            "Accepted as MP11 comparison evidence only; not model input.",
            "Primary harvest-flow target for Phase 13 comparison.",
        ),
        _summary_row(
            "mp11_figure2_recovered_mean",
            "Reviewed Figure 2 recovered mean",
            float(figure2["figures"][0]["y_mean"]),
            "planning/tfl6_mp11_figure2_review_manifest.json",
            "reviewed_mp11_figure_extraction",
            "comparison_context",
            "Accepted for comparison planning; do not use as model input.",
            "Supports the flat MP11 base-case trajectory anchor.",
        ),
        _summary_row(
            "mp11_adjusted_lrsy",
            "MP11 adjusted LRSY context",
            MP11_ADJUSTED_LRSY,
            "MP11 Figure 2 surrounding text; PDF page 82, Appendix A page 18",
            "tracked_mp11_table_or_text",
            "context",
            "LRSY is not the base-case AAC/harvest level.",
            "Context only; do not compare candidate runtime as if LRSY were the base case.",
        ),
        _summary_row(
            "candidate_p12_5_runtime_mean",
            "P12.5 tracked runtime smoke mean annual harvest",
            runtime_mean,
            str(TARGET_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            "tracked_runtime_output",
            "runtime_smoke_output",
            "P12.5 used a high minimum harvested-volume smoke target and did not include the maintainer's maintain-initial-growing-stock target.",
            "Shows runtime capability and order of magnitude, not release-calibrated base-case behavior.",
        ),
        _summary_row(
            "candidate_p12_5_runtime_min",
            "P12.5 tracked runtime smoke minimum annual harvest",
            runtime_min,
            str(TARGET_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            "tracked_runtime_output",
            "runtime_smoke_output",
            "Period-level minimum across nonzero P12.5 smoke periods.",
            "Useful runtime diagnostic only.",
        ),
        _summary_row(
            "candidate_p12_5_runtime_max",
            "P12.5 tracked runtime smoke maximum annual harvest",
            runtime_max,
            str(TARGET_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            "tracked_runtime_output",
            "runtime_smoke_output",
            "Period-level maximum across nonzero P12.5 smoke periods.",
            "Useful runtime diagnostic only.",
        ),
        _summary_row(
            "candidate_p12_5_runtime_final",
            "P12.5 tracked runtime smoke final-period annual harvest",
            runtime_final,
            str(TARGET_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            "tracked_runtime_output",
            "runtime_smoke_output",
            "Final period is a smoke-run endpoint, not a release target.",
            "Useful runtime diagnostic only.",
        ),
        _summary_row(
            "candidate_maintainer_interactive_context",
            "Maintainer interactive basic scenario context",
            MAINTAINER_INTERACTIVE,
            "planning/tfl6_mp11_phase13_candidate_runtime_positioning.md",
            "maintainer_context",
            "context_not_release_evidence",
            "Approximate screenshot/context value; no tracked exported scenario table yet.",
            "Motivates formal reproducible scenario export before release decisions.",
        ),
    ]

    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "phase": "P13.1b",
        "parent_issue": "#70",
        "child_issue": "#127",
        "comparison_status": "scenario_comparison_tables_built",
        "mp11_base_case_m3_per_year": MP11_BASE_CASE,
        "mp11_adjusted_lrsy_m3_per_year": MP11_ADJUSTED_LRSY,
        "candidate_maintainer_context_m3_per_year": MAINTAINER_INTERACTIVE,
        "candidate_runtime_smoke_mean_m3_per_year": runtime_mean,
        "candidate_runtime_smoke_min_m3_per_year": runtime_min,
        "candidate_runtime_smoke_max_m3_per_year": runtime_max,
        "candidate_runtime_smoke_final_m3_per_year": runtime_final,
        "candidate_vs_mp11_base_context_delta_m3_per_year": MAINTAINER_INTERACTIVE
        - MP11_BASE_CASE,
        "candidate_vs_mp11_base_context_pct": _pct_delta(
            MAINTAINER_INTERACTIVE, MP11_BASE_CASE
        ),
        "candidate_thlb_ha": P9RF_CANDIDATE_THLB_HA,
        "mp11_declared_thlb_ha": MP11_DECLARED_THLB_HA,
        "candidate_thlb_delta_ha": thlb_delta_ha,
        "candidate_thlb_delta_pct": thlb_delta_pct,
        "runtime_smoke_run_id": scenario_qa["summary"]["run_id"],
        "runtime_smoke_iterations": scenario_qa["summary"]["iterations"],
        "runtime_smoke_schedule_rows": scenario_qa["summary"]["schedule_rows"],
        "phase12_closeout_status": phase12["summary"]["closeout_status"],
        "mp11_behavior_rows_available": len(behavior_rows),
        "mp11_scenario_endpoint_rows_available": len(endpoints),
        "release_qa": "not_performed",
        "release_decision": "pending_p13_5",
    }

    return {
        "summary": summary,
        "summary_rows": summary_rows,
        "period_rows": period_rows,
        "source_files": [
            str(FIGURE2_REVIEW.relative_to(ROOT)).replace("\\", "/"),
            str(SCENARIO_QA.relative_to(ROOT)).replace("\\", "/"),
            str(PHASE12_CLOSEOUT.relative_to(ROOT)).replace("\\", "/"),
            str(TARGET_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            str(MODEL_BEHAVIOR.relative_to(ROOT)).replace("\\", "/"),
            str(SCENARIO_ENDPOINTS.relative_to(ROOT)).replace("\\", "/"),
        ],
        "caveats": [
            "P12.5 tracked runtime output is a scenario smoke run, not the maintainer interactive basic base scenario.",
            "The maintainer interactive value is context only until a reproducible export is tracked.",
            "MP11 adjusted LRSY is context, not the MP11 base-case harvest level.",
            "No release, AAC, Phase 5 replacement, or WFP-equivalence decision is made by P13.1b.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: dict[str, Any]) -> None:
    with OUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_markdown(data: dict[str, Any]) -> None:
    summary = data["summary"]
    lines = [
        "# TFL 6 MP11 Phase 13 Scenario Comparison",
        "",
        "This note converts the Phase 13 candidate-runtime positioning into tracked comparison tables. It separates MP11 comparison targets, tracked P12.5 runtime smoke output, and maintainer interactive context so later release QA does not confuse screenshot evidence with reproducible model output.",
        "",
        "## Summary",
        "",
        f"- comparison_status: `{summary['comparison_status']}`",
        f"- parent_issue: `{summary['parent_issue']}`",
        f"- child_issue: `{summary['child_issue']}`",
        f"- mp11_base_case_m3_per_year: `{summary['mp11_base_case_m3_per_year']}`",
        f"- mp11_adjusted_lrsy_m3_per_year: `{summary['mp11_adjusted_lrsy_m3_per_year']}`",
        f"- candidate_maintainer_context_m3_per_year: `{summary['candidate_maintainer_context_m3_per_year']}`",
        f"- candidate_vs_mp11_base_context_delta_m3_per_year: `{summary['candidate_vs_mp11_base_context_delta_m3_per_year']}`",
        f"- candidate_vs_mp11_base_context_pct: `{summary['candidate_vs_mp11_base_context_pct']:.2f}`",
        f"- candidate_runtime_smoke_mean_m3_per_year: `{summary['candidate_runtime_smoke_mean_m3_per_year']:.2f}`",
        f"- runtime_smoke_run_id: `{summary['runtime_smoke_run_id']}`",
        f"- runtime_smoke_iterations: `{summary['runtime_smoke_iterations']}`",
        f"- runtime_smoke_schedule_rows: `{summary['runtime_smoke_schedule_rows']}`",
        f"- release_qa: `{summary['release_qa']}`",
        f"- release_decision: `{summary['release_decision']}`",
        "",
        "## Comparison Rows",
        "",
        "| ID | Label | Value | Evidence | Role | Caveat |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in data["summary_rows"]:
        lines.append(
            f"| `{row['comparison_id']}` | {row['label']} | "
            f"`{row['value_m3_per_year']:.2f}` | `{row['evidence_strength']}` | "
            f"`{row['evidence_role']}` | {row['caveat']} |"
        )
    lines.extend(
        [
            "",
            "## Period Table",
            "",
            "`planning/tfl6_mp11_phase13_scenario_period_comparison.csv` records each P12.5 non-release smoke period against the MP11 base-case anchor. Period `0` is retained for completeness but should not be used as a harvest-flow comparison value.",
            "",
            "## Interpretation",
            "",
            "The maintainer interactive context value of approximately `1.15 million m3/year` is about "
            f"`{summary['candidate_vs_mp11_base_context_pct']:.2f}%` above the MP11 base-case anchor. That is plausible given the candidate runtime's slightly larger public-data THLB scaffold and incomplete WFP constraint coverage, but it is not yet reproducible release evidence.",
            "",
            "The P12.5 tracked runtime smoke output is intentionally separated from the maintainer interactive value. It proves runtime scheduling and target behavior from tracked saved-stage outputs, but it used a high harvested-volume minimum and was not the same basic scenario shown in the maintainer screenshot.",
            "",
            "## Caveats",
            "",
        ]
    )
    lines.extend(f"- {caveat}" for caveat in data["caveats"])
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = build_comparison()
    write_csv(OUT_SUMMARY_CSV, data["summary_rows"])
    write_csv(OUT_PERIOD_CSV, data["period_rows"])
    write_json(data)
    write_markdown(data)
    print(f"wrote {OUT_SUMMARY_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_PERIOD_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"comparison_status={data['summary']['comparison_status']}")


if __name__ == "__main__":
    main()
