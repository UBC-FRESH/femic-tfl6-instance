"""Build the P6.5 MP11 model-behavior, sensitivity, AAC, and KPI crosswalk."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"
BASE_CASE_M3_PER_YEAR = 1_061_600.0
CURRENT_AAC_M3_PER_YEAR = 1_362_000.0
AAC_RECOMMENDATION_M3_PER_YEAR = 1_252_700.0


@dataclass(frozen=True)
class BehaviorComparison:
    """Reviewed comparison row for one MP11 model-behavior or KPI family."""

    behavior_id: str
    evidence_family: str
    mp11_summary: str
    mp11_pdf_pages: str
    mp11_numeric_anchor: str
    phase7_figure_evidence: str
    phase5_surface: str
    phase5_comparison: str
    comparison_class: str
    implementation_gap: str
    phase7_plus_followup: str
    review_status: str
    downstream_use: str
    model_input_status: str
    notes: str


@dataclass(frozen=True)
class ScenarioEndpoint:
    """Normalized MP11 harvest-flow or sensitivity endpoint."""

    figure_id: str
    series_name: str
    label: str
    expected_m3_per_year: float
    difference_vs_base_m3_per_year: float
    percent_vs_base: float
    endpoint_abs_percent_error: float
    evidence_source: str
    review_status: str
    downstream_use: str
    model_input_status: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _f(value: str) -> float:
    return float(value.replace(",", ""))


def _build_scenario_rows(planning_dir: Path) -> list[ScenarioEndpoint]:
    rows: list[ScenarioEndpoint] = []

    for row in _read_csv(planning_dir / "tfl6_mp11_remaining_harvest_series_summary.csv"):
        if row["series_name"] == "base_case":
            continue
        expected = _f(row["expected_endpoint_m3_per_year"])
        rows.append(
            ScenarioEndpoint(
                figure_id=row["figure_id"],
                series_name=row["series_name"],
                label=row["label"],
                expected_m3_per_year=expected,
                difference_vs_base_m3_per_year=expected - BASE_CASE_M3_PER_YEAR,
                percent_vs_base=(expected - BASE_CASE_M3_PER_YEAR) / BASE_CASE_M3_PER_YEAR * 100.0,
                endpoint_abs_percent_error=_f(row["endpoint_abs_percent_error"]),
                evidence_source=row["expected_source"],
                review_status="accepted_for_comparison",
                downstream_use="phase6_mp11_comparison_only",
                model_input_status="not_model_input",
            )
        )

    for row in _read_csv(planning_dir / "tfl6_mp11_harvest_sensitivity_series_summary.csv"):
        if row["series_name"] == "base_case":
            continue
        expected = _f(row["expected_table_value"])
        rows.append(
            ScenarioEndpoint(
                figure_id=row["figure_id"],
                series_name=row["series_name"],
                label=row["series_name"].replace("_", " ").title(),
                expected_m3_per_year=expected,
                difference_vs_base_m3_per_year=expected - BASE_CASE_M3_PER_YEAR,
                percent_vs_base=(expected - BASE_CASE_M3_PER_YEAR) / BASE_CASE_M3_PER_YEAR * 100.0,
                endpoint_abs_percent_error=_f(row["absolute_percent_error"]),
                evidence_source="adjacent_mp11_table_value",
                review_status="accepted_for_comparison",
                downstream_use="phase6_mp11_comparison_only",
                model_input_status="not_model_input",
            )
        )
    return sorted(rows, key=lambda item: (item.figure_id, item.series_name))


def _figure_status_counts(planning_dir: Path) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in _read_csv(planning_dir / "tfl6_mp11_figure_extraction_closeout.csv"):
        for field in ["phase7_status", "downstream_use", "model_input_status"]:
            counts.setdefault(field, {})
            value = row[field]
            counts[field][value] = counts[field].get(value, 0) + 1
    return counts


def _impact_endpoint(impact_rows: list[dict[str, str]], figure_id: str, label: str) -> float:
    for row in impact_rows:
        if row["figure_id"] == figure_id and row["step_label"] == label:
            return _f(row["printed_value_m3_per_year"])
    raise ValueError(f"Missing impact endpoint: {figure_id} {label}")


def _growing_stock_summary(planning_dir: Path, figure_id: str) -> dict[str, float]:
    rows = [
        row
        for row in _read_csv(planning_dir / "tfl6_mp11_growing_stock_series_summary.csv")
        if row["figure_id"] == figure_id and row["series_name"] == "thlb_gs_total"
    ]
    if len(rows) != 1:
        raise ValueError(f"Expected one total growing-stock row for {figure_id}, found {len(rows)}")
    row = rows[0]
    return {
        "min": _f(row["y_min"]),
        "max": _f(row["y_max"]),
        "mean": _f(row["y_mean"]),
    }


def _build_behavior_rows(planning_dir: Path, scenario_rows: list[ScenarioEndpoint]) -> list[BehaviorComparison]:
    impact_rows = _read_csv(planning_dir / "tfl6_mp11_impact_chart_rows.csv")
    base_case_endpoint = _impact_endpoint(impact_rows, "Figure 20", "MP 11 Base Case")
    recommendation_endpoint = _impact_endpoint(impact_rows, "Figure 57", "MP 11 AAC Recommendation")
    max_short_term = _impact_endpoint(impact_rows, "Figure 20", "MP 11 max short-term flow")
    base_gs = _growing_stock_summary(planning_dir, "Figure 3")
    recommendation_gs = _growing_stock_summary(planning_dir, "Figure 40")
    sensitivity_values = {row.series_name: row.expected_m3_per_year for row in scenario_rows}

    return [
        BehaviorComparison(
            behavior_id="base_case_harvest_level",
            evidence_family="base_case",
            mp11_summary=(
                "MP11 Base Case is an even-flow harvest projection over 300 years, net of "
                "1.5% non-recoverable losses, and represents about 90% of adjusted LRSY."
            ),
            mp11_pdf_pages="82-83, 100-101",
            mp11_numeric_anchor=(
                f"Base Case `{base_case_endpoint:,.0f} m3/year`; current AAC "
                f"`{CURRENT_AAC_M3_PER_YEAR:,.0f} m3/year`; reported decrease `22.1%`."
            ),
            phase7_figure_evidence="Figure 2 and Figure 20 accepted for comparison.",
            phase5_surface="planning/tfl6_phase5_release_qa.md; docs/phase5-runtime-release.rst",
            phase5_comparison=(
                "Phase 5 has a launch-smoked teaching runtime with generic managed CC "
                "harvest signals, but no accepted AAC-equivalent base-case calibration."
            ),
            comparison_class="mp11_numeric_target_without_phase5_equivalent",
            implementation_gap="aac_calibrated_runtime_behavior",
            phase7_plus_followup=(
                "Use the MP11 base-case harvest level as a future calibration and QA target "
                "after source-layer, AU/yield, MHA, and constraint rebuilds are complete."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="Do not claim the Phase 5 teaching runtime reproduces this AAC forecast.",
        ),
        BehaviorComparison(
            behavior_id="alternate_harvest_flows",
            evidence_family="harvest_flow",
            mp11_summary=(
                "MP11 evaluates maintaining current AAC for 10 years and maximizing "
                "short-term harvest with controlled mid-term effects."
            ),
            mp11_pdf_pages="102-104",
            mp11_numeric_anchor=(
                f"Maintain-current-AAC long-term endpoint `{sensitivity_values['maintaining_current_aac']:,.0f}`; "
                f"maximize-short-term first decade `{max_short_term:,.0f}` and long-term endpoint "
                f"`{sensitivity_values['maximize_short_term']:,.0f}` m3/year."
            ),
            phase7_figure_evidence="Figures 21 and 22 accepted for comparison.",
            phase5_surface="planning/tfl6_runtime_package_p44.md; docs/phase5-scenario-teaching-workflows.rst",
            phase5_comparison=(
                "Phase 5 includes a representative max-even-flow smoke mode, but it was a "
                "runtime-signal smoke rather than a reviewed MP11-style flow comparison."
            ),
            comparison_class="scenario_design_gap",
            implementation_gap="harvest_flow_policy_and_objective_update",
            phase7_plus_followup=(
                "Add explicit harvest-flow scenario definitions and QA metrics after MP11 "
                "model inputs are rebuilt."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="The existing runtime smoke proves capability, not MP11-equivalent behavior.",
        ),
        BehaviorComparison(
            behavior_id="yield_sensitivity_response",
            evidence_family="sensitivity",
            mp11_summary=(
                "MP11 is more sensitive to managed-stand yield changes than natural-stand "
                "yield changes; LiDAR/ITI/LEFI and reduced OAF1 produce the largest uplift."
            ),
            mp11_pdf_pages="105-123, 142-143",
            mp11_numeric_anchor=(
                f"Natural +10% `{sensitivity_values['increased_natural_stand_yields']:,.0f}`; "
                f"natural -10% `{sensitivity_values['decreased_natural_stand_yields']:,.0f}`; "
                f"managed +10% `{sensitivity_values['increased_managed_stand_yields']:,.0f}`; "
                f"managed -10% `{sensitivity_values['decreased_managed_stand_yields']:,.0f}`; "
                f"ITI/LEFI/OAF1 even-flow `{sensitivity_values['lidar_adjusted_yields_reduced_oaf1']:,.0f}`."
            ),
            phase7_figure_evidence="Figures 23-26 and 29-32 accepted for comparison.",
            phase5_surface="planning/tfl6_au_yield_curve_contract.md; planning/tfl6_tipsy_btc_handoff_manifest.md",
            phase5_comparison=(
                "Phase 5 has reviewed VDYP/TIPSY curve surfaces, but no MP11-style "
                "sensitivity suite and no accepted LiDAR/ITI/LEFI input surface."
            ),
            comparison_class="sensitivity_suite_missing",
            implementation_gap="yield_sensitivity_and_private_inventory_gap",
            phase7_plus_followup=(
                "Build a public-data sensitivity suite and isolate WFP-only LiDAR/ITI/LEFI "
                "uplift as an unavailable or explicitly approximated scenario."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="The high-yield LiDAR/OAF1 scenario is evidence for scoping, not a public-data input.",
        ),
        BehaviorComparison(
            behavior_id="policy_and_constraint_sensitivities",
            evidence_family="sensitivity",
            mp11_summary=(
                "MP11 tests no genetic gain, full NSOG old-seral targets, MHA +/- 10 years, "
                "helicopter exclusion, and THLB +/- 10%."
            ),
            mp11_pdf_pages="124-141",
            mp11_numeric_anchor=(
                f"No genetic gain `{sensitivity_values['no_genetic_gain']:,.0f}`; "
                f"full NSOG `{sensitivity_values['full_nsog_order_targets']:,.0f}`; "
                f"MHA +10 `{sensitivity_values['mha_increased_by_10_years']:,.0f}`; "
                f"MHA -10 `{sensitivity_values['mha_decreased_by_10_years']:,.0f}`; "
                f"helicopter excluded `{sensitivity_values['helicopter_operable_land_base_excluded']:,.0f}`; "
                f"THLB -10 `{sensitivity_values['thlb_decreased_by_10_percent']:,.0f}`; "
                f"THLB +10 `{sensitivity_values['thlb_increased_by_10_percent']:,.0f}` m3/year."
            ),
            phase7_figure_evidence="Figures 33-39 accepted for comparison.",
            phase5_surface=(
                "planning/tfl6_treatment_option_contract.md; planning/tfl6_state_transition_contract.md; "
                "docs/phase5-known-limitations-release-readiness.rst"
            ),
            phase5_comparison=(
                "Phase 5 documents these as deferred or scenario-worthy concepts, not as "
                "implemented MP11-equivalent sensitivity runs."
            ),
            comparison_class="scenario_design_gap",
            implementation_gap="policy_constraint_sensitivity_suite",
            phase7_plus_followup=(
                "Prioritize MHA, harvest-system exclusion, THLB adjustment, and genetic-gain "
                "sensitivities because their MP11 effects are numerically clear."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="These are candidate future scenario tests, not Phase 5 behavior claims.",
        ),
        BehaviorComparison(
            behavior_id="aac_recommendation_bridge",
            evidence_family="aac_recommendation",
            mp11_summary=(
                "MP11 recommends a step-down LiDAR/ITI/LEFI/OAF1 scenario for the next "
                "10 years after the base-case analysis."
            ),
            mp11_pdf_pages="142-143, 157-158",
            mp11_numeric_anchor=(
                f"AAC recommendation `{recommendation_endpoint:,.0f} m3/year`; uplift "
                f"from Base Case `{recommendation_endpoint - BASE_CASE_M3_PER_YEAR:,.0f} m3/year`; "
                "about `1.1%` below the scheduled MP10 decline benchmark."
            ),
            phase7_figure_evidence="Figures 32, 40, and 57 accepted for comparison.",
            phase5_surface="planning/tfl6_runtime_release_archive_manifest.md; planning/tfl6_phase5_release_qa.md",
            phase5_comparison=(
                "Phase 5 has no AAC-recommendation lane and must not be represented as a "
                "Chief-Forester-ready or WFP-model-equivalent forecast."
            ),
            comparison_class="mp11_numeric_target_without_phase5_equivalent",
            implementation_gap="aac_recommendation_scenario_missing",
            phase7_plus_followup=(
                "Treat the AAC recommendation as a high-level target for a future MP11-aligned "
                "scenario, gated on inventory/yield and flow-policy decisions."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="The recommendation depends on WFP inventory/model assumptions that are not fully public.",
        ),
        BehaviorComparison(
            behavior_id="growing_stock_dynamics",
            evidence_family="kpi",
            mp11_summary=(
                "MP11 reports base-case and AAC-recommendation THLB growing-stock trajectories "
                "split by <=120 and >120 year categories."
            ),
            mp11_pdf_pages="83, 143",
            mp11_numeric_anchor=(
                f"Base-case total THLB GS min/max `{base_gs['min']:,.0f}`/`{base_gs['max']:,.0f}`; "
                f"AAC recommendation min/max `{recommendation_gs['min']:,.0f}`/`{recommendation_gs['max']:,.0f}` m3."
            ),
            phase7_figure_evidence="Figures 3 and 40 accepted for comparison.",
            phase5_surface="docs/phase5-runtime-quickstart.rst; planning/tfl6_phase5_release_qa.md",
            phase5_comparison=(
                "Phase 5 exposes managed/unmanaged area and yield signals, but does not "
                "publish MP11-style THLB growing-stock KPI trajectories."
            ),
            comparison_class="kpi_reporting_gap",
            implementation_gap="growing_stock_kpi_reporting",
            phase7_plus_followup=(
                "Add comparable growing-stock reports once MP11-aligned Patchworks outputs exist."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="Figure values are comparison evidence from recovered chart data, not model input.",
        ),
        BehaviorComparison(
            behavior_id="harvest_system_and_operational_kpis",
            evidence_family="kpi",
            mp11_summary=(
                "MP11 reports harvest-system, block-size, harvest-age, harvested-area, volume-per-ha, "
                "species-composition, and elevation-band behavior for base-case and AAC scenarios."
            ),
            mp11_pdf_pages="87-93, 144-152",
            mp11_numeric_anchor=(
                "Base-case harvest-system average is 57% ground, 40% cable, and 3% helicopter; "
                "average block size is 19.1 ha; long-term harvested area averages 1,430 ha/year."
            ),
            phase7_figure_evidence=(
                "Some KPI figures were inventoried or deferred; not all medium-priority KPI charts "
                "were extracted in Phase 7."
            ),
            phase5_surface="docs/phase5-known-limitations-release-readiness.rst; planning/tfl6_model_input_bundle_qa.md",
            phase5_comparison=(
                "Phase 5 explicitly defers ground/cable/heli assignment and carries harvest-system "
                "placeholders, so MP11 operational KPI comparison is mostly a future reporting gap."
            ),
            comparison_class="kpi_reporting_and_classifier_gap",
            implementation_gap="harvest_system_classifier_and_kpi_reports",
            phase7_plus_followup=(
                "Create public-data harvest-system proxies before attempting MP11-style operational KPI reports."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="Do not backfill stand-level harvest systems from aggregate MP11 percentages.",
        ),
        BehaviorComparison(
            behavior_id="cedar_age_old_seral_kpis",
            evidence_family="kpi",
            mp11_summary=(
                "MP11 reports age-class, cedar, old-cedar, and old-seral trajectories for "
                "base-case and AAC-recommendation scenarios."
            ),
            mp11_pdf_pages="85-86, 153-157",
            mp11_numeric_anchor=(
                "Phase 7 reviewed age-class, cedar, and old-seral figures for planning only; "
                "they were not promoted to comparison-accepted status."
            ),
            phase7_figure_evidence=(
                "Figures 6, 14, 15, 45, 51, 52, 16-19, and 53-56 reviewed for planning only."
            ),
            phase5_surface="planning/tfl6_cedar_signal_design.md; docs/phase5-known-limitations-release-readiness.rst",
            phase5_comparison=(
                "Phase 5 carries cedar signals for teaching/reporting, but no hard cedar reserve, "
                "utility-pole-grade, or MP11 old-seral KPI calibration."
            ),
            comparison_class="planning_evidence_only",
            implementation_gap="cedar_age_old_seral_reporting_and_policy_gap",
            phase7_plus_followup=(
                "Use planning-only evidence to design reports and stronger validation checks before "
                "promoting these KPI families."
            ),
            review_status="reviewed_evidence",
            downstream_use="phase6_model_behavior_comparison_only",
            model_input_status="not_model_input",
            notes="Planning-only figure evidence should not be mixed with accepted comparison rows.",
        ),
    ]


def write_outputs(planning_dir: Path, generated_at_utc: str) -> None:
    scenario_rows = _build_scenario_rows(planning_dir)
    behavior_rows = _build_behavior_rows(planning_dir, scenario_rows)
    figure_counts = _figure_status_counts(planning_dir)

    behavior_csv = planning_dir / "tfl6_mp11_model_behavior_crosswalk.csv"
    with behavior_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(behavior_rows[0]).keys()))
        writer.writeheader()
        for row in behavior_rows:
            writer.writerow(asdict(row))

    scenario_csv = planning_dir / "tfl6_mp11_model_behavior_scenario_endpoints.csv"
    with scenario_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(scenario_rows[0]).keys()))
        writer.writeheader()
        for row in scenario_rows:
            writer.writerow(asdict(row))

    comparison_counts: dict[str, int] = {}
    implementation_counts: dict[str, int] = {}
    for row in behavior_rows:
        comparison_counts[row.comparison_class] = comparison_counts.get(row.comparison_class, 0) + 1
        implementation_counts[row.implementation_gap] = implementation_counts.get(row.implementation_gap, 0) + 1

    payload: dict[str, Any] = {
        "generated_at_utc": generated_at_utc,
        "source_sha256": SOURCE_SHA256,
        "base_case_m3_per_year": BASE_CASE_M3_PER_YEAR,
        "current_aac_m3_per_year": CURRENT_AAC_M3_PER_YEAR,
        "aac_recommendation_m3_per_year": AAC_RECOMMENDATION_M3_PER_YEAR,
        "behavior_crosswalk_csv": behavior_csv.as_posix(),
        "scenario_endpoint_csv": scenario_csv.as_posix(),
        "behavior_row_count": len(behavior_rows),
        "scenario_endpoint_count": len(scenario_rows),
        "figure_status_counts": figure_counts,
        "comparison_class_counts": comparison_counts,
        "implementation_gap_counts": implementation_counts,
        "review_status_counts": {"reviewed_evidence": len(behavior_rows)},
        "downstream_use_counts": {"phase6_model_behavior_comparison_only": len(behavior_rows)},
        "model_input_status_counts": {"not_model_input": len(behavior_rows)},
        "behavior_rows": [asdict(row) for row in behavior_rows],
        "scenario_endpoint_rows": [asdict(row) for row in scenario_rows],
    }
    json_path = planning_dir / "tfl6_mp11_model_behavior_crosswalk.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(planning_dir / "tfl6_mp11_model_behavior_crosswalk.md", payload)


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# TFL 6 MP11 Model Behavior, Sensitivity, AAC, And KPI Crosswalk",
        "",
        "## Purpose",
        "",
        "This P6.5 note compares MP11 model-behavior outputs, sensitivity results,",
        "AAC recommendation evidence, and KPI reporting surfaces against the Phase 5",
        "teaching runtime. It is a planning artifact only. It does not claim",
        "equivalence to WFP's unpublished forest estate model and does not promote",
        "any MP11 value to model-input status.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_model_behavior_crosswalk.md`",
        "- `planning/tfl6_mp11_model_behavior_crosswalk.csv`",
        "- `planning/tfl6_mp11_model_behavior_crosswalk.json`",
        "- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`",
        "",
        "## Headline Values",
        "",
        f"- Current AAC: `{payload['current_aac_m3_per_year']:,.0f} m3/year`",
        f"- MP11 Base Case: `{payload['base_case_m3_per_year']:,.0f} m3/year`",
        f"- MP11 AAC recommendation: `{payload['aac_recommendation_m3_per_year']:,.0f} m3/year`",
        "- Review status: `reviewed_evidence`",
        "- Downstream use: `phase6_model_behavior_comparison_only`",
        "- Model-input status: `not_model_input`",
        "",
        "## Figure Evidence Status",
        "",
    ]

    for family, counts in payload["figure_status_counts"].items():
        lines.append(f"### `{family}`")
        lines.append("")
        for key, value in sorted(counts.items()):
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")

    lines.extend(
        [
            "## Behavior Crosswalk",
            "",
            "| Behavior | Family | Comparison class | Implementation gap | Follow-up |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in payload["behavior_rows"]:
        lines.append(
            "| "
            f"`{row['behavior_id']}` | "
            f"{row['evidence_family']} | "
            f"`{row['comparison_class']}` | "
            f"`{row['implementation_gap']}` | "
            f"{row['phase7_plus_followup']} |"
        )

    lines.extend(
        [
            "",
            "## Scenario Endpoint Snapshot",
            "",
            "| Figure | Scenario | Expected m3/year | Delta vs base | Percent vs base | Endpoint QA error |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["scenario_endpoint_rows"]:
        lines.append(
            "| "
            f"{row['figure_id']} | {row['label']} | "
            f"{row['expected_m3_per_year']:,.0f} | "
            f"{row['difference_vs_base_m3_per_year']:,.0f} | "
            f"{row['percent_vs_base']:.2f}% | "
            f"{row['endpoint_abs_percent_error']:.3f}% |"
        )

    lines.extend(["", "## Reviewed Rows", ""])
    for row in payload["behavior_rows"]:
        lines.extend(
            [
                f"### `{row['behavior_id']}`",
                "",
                f"- Evidence family: `{row['evidence_family']}`",
                f"- MP11 pages: `{row['mp11_pdf_pages']}`",
                f"- Comparison class: `{row['comparison_class']}`",
                f"- Implementation gap: `{row['implementation_gap']}`",
                f"- Review status: `{row['review_status']}`",
                f"- Downstream use: `{row['downstream_use']}`",
                f"- Model-input status: `{row['model_input_status']}`",
                "",
                "MP11 anchor:",
                "",
                row["mp11_numeric_anchor"],
                "",
                "MP11 summary:",
                "",
                row["mp11_summary"],
                "",
                "Phase 5 comparison:",
                "",
                row["phase5_comparison"],
                "",
                "Follow-up:",
                "",
                row["phase7_plus_followup"],
                "",
            ]
        )

    lines.extend(
        [
            "## Closeout Boundary",
            "",
            "P6.5 confirms that the Phase 5 teaching runtime is structurally useful",
            "but not MP11-behavior-equivalent. Future implementation work must rebuild",
            "or approximate the MP11 source-layer, AU/yield, MHA, harvest-system,",
            "constraint, and scenario-policy surfaces before AAC-style behavior can be",
            "meaningfully compared from model output rather than from MP11 evidence.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--planning-dir",
        type=Path,
        default=Path("planning"),
        help="Directory containing Phase 7 summaries and receiving P6.5 outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    write_outputs(args.planning_dir, generated_at_utc)


if __name__ == "__main__":
    main()
