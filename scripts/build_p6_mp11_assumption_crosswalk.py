"""Build the P6.4 MP11 inventory/yield/operability assumption crosswalk."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"


@dataclass(frozen=True)
class AssumptionComparison:
    """Reviewed comparison row for one MP11 modelling-assumption family."""

    assumption_id: str
    assumption_family: str
    mp11_summary: str
    mp11_pdf_pages: str
    mp11_source_context: str
    phase5_surface: str
    phase5_summary: str
    delta_class: str
    implementation_class: str
    phase7_plus_followup: str
    review_status: str
    downstream_use: str
    model_input_status: str
    notes: str


ROWS = [
    AssumptionComparison(
        assumption_id="inventory_vri_lidar_iti",
        assumption_family="inventory",
        mp11_summary=(
            "MP11 uses VRI updated to December 31, 2023, LiDAR-derived stand heights, "
            "Land Base Blocking, and LiDAR-derived Individual Tree Inventory proposals "
            "for natural-stand sensitivity work."
        ),
        mp11_pdf_pages="266-279",
        mp11_source_context=(
            "Appendix B sections 3.5.2 and 5.1-5.2 describe full-TFL LiDAR, "
            "LBB, LEFI-style height assignment, ITI attributes, and VRI currency."
        ),
        phase5_surface=(
            "config/run_profile.tfl6.yaml; config/tsr/source_layers.recipe.yaml; "
            "docs/phase5-rebuild-provenance.rst"
        ),
        phase5_summary=(
            "Phase 5 uses public 2025 R1/VRI and VDYP7 source surfaces, with no "
            "accepted proprietary LBB, LEFI, or ITI attributes."
        ),
        delta_class="unresolved_wfp_inventory_gap",
        implementation_class="public_vri_refresh_plus_private_lidar_iti_gap",
        phase7_plus_followup=(
            "Refresh public inventory surfaces where possible, then create an explicit "
            "LiDAR/ITI gap lane for unavailable WFP-derived attributes."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="This row is a planning comparison only; ITI/LEFI values are not accepted as FEMIC inputs.",
    ),
    AssumptionComparison(
        assumption_id="physical_operability_lbb",
        assumption_family="operability",
        mp11_summary=(
            "MP11 physical operability is mapped from the LBB process using LiDAR and "
            "professional review; inoperable area removes 21,193 ha from THLB."
        ),
        mp11_pdf_pages="257-258, 265-267, 297-299",
        mp11_source_context=(
            "Appendix B sections 3.1, 3.5.1.4, 3.5.2.2, and 6.8; Tables 18-20."
        ),
        phase5_surface=(
            "config/tsr/thlb_netdown.recipe.yaml; planning/tfl6_operability_netdown_proxy.md; "
            "docs/phase5-known-limitations-release-readiness.rst"
        ),
        phase5_summary=(
            "Phase 5 carries a benchmark-calibrated operability placeholder and explicitly "
            "defers reviewed ground/cable/heli assignment."
        ),
        delta_class="proxy_replacement_required",
        implementation_class="model_spatial_layer_update",
        phase7_plus_followup=(
            "Replace the placeholder with a reviewed public DEM/slope proxy where possible, "
            "and keep WFP LBB as an unavailable reference benchmark unless a shareable layer appears."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="Do not infer WFP LBB geometry from summarized areas.",
    ),
    AssumptionComparison(
        assumption_id="economic_operability_helicopter",
        assumption_family="operability",
        mp11_summary=(
            "MP11 treats conventional land as economically viable and applies flight-distance, "
            "minimum volume, and Cw+Fd+Yc component thresholds to helicopter-operable stands; "
            "only 20 ha are netted down as non-conventional uneconomic."
        ),
        mp11_pdf_pages="311-313",
        mp11_source_context="Appendix B section 6.13; Tables 27-29.",
        phase5_surface="docs/phase5-known-limitations-release-readiness.rst; planning/tfl6_treatment_option_contract.md",
        phase5_summary=(
            "Phase 5 does not implement delivered-cost or harvest-system-specific economic "
            "operability logic; it records cost and system splits as later work."
        ),
        delta_class="new_model_parameter_and_cost_proxy_gap",
        implementation_class="sensitivity_candidate",
        phase7_plus_followup=(
            "Add a helicopter economic-operability sensitivity lane using public stand volume, "
            "species share, and distance/access proxies."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="The exact flight-distance/access basis remains unavailable from the public PDF.",
    ),
    AssumptionComparison(
        assumption_id="analysis_unit_definition",
        assumption_family="analysis_units",
        mp11_summary=(
            "MP11 managed AUs are defined by AU era, BEC variant, site series, leading "
            "species, and silvicultural treatments; natural stands older than 62 years "
            "are projected polygon-by-polygon."
        ),
        mp11_pdf_pages="348-354",
        mp11_source_context="Appendix B section 7.3; Tables 47-51.",
        phase5_surface="planning/tfl6_au_yield_curve_contract.md; docs/phase3-au-yield-curves.rst",
        phase5_summary=(
            "Phase 5 static AUs are BEC/species/SI classes with top-area selection and "
            "remapping; MP10 AU codes are retained as parameter evidence, not canonical identity."
        ),
        delta_class="model_contract_update",
        implementation_class="analysis_unit_overhaul",
        phase7_plus_followup=(
            "Decide whether to migrate to MP11 era/site-series/treatment AU identity or "
            "preserve Phase 5 static AU identity with MP11 attributes as crosswalk fields."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="This is one of the largest structural differences between MP11 and the teaching prototype.",
    ),
    AssumptionComparison(
        assumption_id="growth_yield_software",
        assumption_family="growth_yield",
        mp11_summary=(
            "MP11 uses VDYP 7.33b for natural stands and BatchTIPSY/TIPSY 4.6 for "
            "managed and future managed stands."
        ),
        mp11_pdf_pages="272, 348, 355",
        mp11_source_context="Appendix B section 3.6.3, 7.3.1, and 8; Table 52.",
        phase5_surface="config/tipsy/tfl6.yaml; planning/tfl6_tipsy_btc_handoff_manifest.md",
        phase5_summary=(
            "Phase 5 uses accepted VDYP first-growth curves and MP10-derived BatchTIPSY "
            "parameter evidence; the TIPSY config records MP10 Tables 27-29 as the source library."
        ),
        delta_class="model_parameter_update",
        implementation_class="yield_pipeline_refresh",
        phase7_plus_followup=(
            "Regenerate natural and managed curves only in a later implementation phase, "
            "after AU identity and MP11 TIPSY parameter extraction are reviewed."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="P6.4 records the version/contract delta but does not regenerate curves.",
    ),
    AssumptionComparison(
        assumption_id="site_index_sibec_tem_lefi",
        assumption_family="site_productivity",
        mp11_summary=(
            "MP11 uses RESULTS-derived SI for existing managed stands, SIBEC/TEM site "
            "series for future stands, and LEFI/LiDAR height-derived SI in sensitivity work."
        ),
        mp11_pdf_pages="272, 278-279, 349-350, 356-357",
        mp11_source_context="Appendix B sections 3.6.3, 5.2.3, 7.3.2, and 8.2.1.",
        phase5_surface="planning/tfl6_au_yield_curve_contract.md; config/run_profile.tfl6.yaml",
        phase5_summary=(
            "Phase 5 uses public VRI/VDYP attributes and an L/M/H SI class contract; "
            "it does not implement MP11 SIBEC/site-series future-stand SI or LEFI sensitivity."
        ),
        delta_class="mixed_public_and_private_data_update",
        implementation_class="model_parameter_update",
        phase7_plus_followup=(
            "Assess public SIBEC/TEM reproducibility first, then separate unavailable "
            "LEFI/LiDAR sensitivity assumptions from base public inputs."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="Public/private reproducibility must be resolved before promotion.",
    ),
    AssumptionComparison(
        assumption_id="managed_stand_inputs_genetic_gain_fertilization_spacing",
        assumption_family="managed_yield",
        mp11_summary=(
            "MP11 differentiates early, recent, and future managed stands, uses planting "
            "densities of 900/1000/1200 sph with exceptions, applies future genetic gains, "
            "and carries fertilization/spacing markers into managed AUs."
        ),
        mp11_pdf_pages="262-264, 352-358, 372-375",
        mp11_source_context="Appendix B sections 3.5.1.1-3.5.1.2, 7.3.4, and 8.2.2-8.2.7.",
        phase5_surface="config/tipsy/tfl6.yaml; planning/tfl6_tipsy_parameter_crosswalk.csv",
        phase5_summary=(
            "Phase 5 managed curves come from reviewed MP10 parameter evidence and do not "
            "yet encode MP11 managed-stand eras, updated genetic gain table, or MP11 AU markers."
        ),
        delta_class="model_parameter_update",
        implementation_class="tipsy_parameter_library_rebuild",
        phase7_plus_followup=(
            "Extract MP11 Tables 54-57 into a reviewed managed-yield parameter library "
            "before any curve rebuild."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="Large table extraction is required; this row is not a substitute for that table library.",
    ),
    AssumptionComparison(
        assumption_id="oaf_vraf_retention_yield_adjustment",
        assumption_family="yield_adjustment",
        mp11_summary=(
            "MP11 uses standard OAF1 15% and OAF2 5%, and applies a Variable Retention "
            "Adjustment Factor shading effect for recent and future managed stands."
        ),
        mp11_pdf_pages="258-259, 273, 375-377, 406-409",
        mp11_source_context="Appendix B sections 3.1, 3.6.4, 8.2.8, and 10.4.3; Tables 58 and 74.",
        phase5_surface="config/tipsy/tfl6.yaml; planning/tfl6_state_transition_contract.md",
        phase5_summary=(
            "Phase 5 TIPSY metadata carries OAF2 0.95 and MP10-derived OAF/utilization "
            "parameter evidence; stand-level retention is not yet implemented as MP11 VRAF."
        ),
        delta_class="model_parameter_update",
        implementation_class="yield_adjustment_and_retention_rule_update",
        phase7_plus_followup=(
            "Promote OAF and VRAF only after MP11 managed-yield tables and retention zones "
            "are extracted into reviewed parameter surfaces."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="OAF/VRAF affect both yield curves and post-harvest transition assumptions.",
    ),
    AssumptionComparison(
        assumption_id="utilization_standards",
        assumption_family="utilization",
        mp11_summary=(
            "MP11 uses 17.5 cm DBH for mature stands older than 120 years, 12.5 cm DBH "
            "for immature and future managed stands, 30 cm stump height, 10 cm top DIB, "
            "and 50% firmwood standard."
        ),
        mp11_pdf_pages="377",
        mp11_source_context="Appendix B section 8.3; Table 60.",
        phase5_surface="config/tipsy/tfl6.yaml; planning/tfl6_tipsy_parameter_library.csv",
        phase5_summary=(
            "Phase 5 carries MP10-derived utilization evidence in the TIPSY parameter "
            "library and a default 17.5 cm utilization fallback in config."
        ),
        delta_class="model_parameter_update",
        implementation_class="yield_pipeline_refresh",
        phase7_plus_followup=(
            "Compare MP11 utilization by age class against the MP10 table library before "
            "curve regeneration."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="Direct table extraction is needed before any model-input promotion.",
    ),
    AssumptionComparison(
        assumption_id="non_recoverable_losses",
        assumption_family="disturbance_loss",
        mp11_summary=(
            "MP11 accounts for windthrow, insects/disease, fire, and NCLB disturbance; "
            "future-stand LRSY is reported after a 1.5% non-recoverable loss reduction."
        ),
        mp11_pdf_pages="379-381, 403",
        mp11_source_context="Appendix B sections 9.1-9.5 and Table 72.",
        phase5_surface="planning/tfl6_model_input_bundle_qa.md; docs/phase5-known-limitations-release-readiness.rst",
        phase5_summary=(
            "Phase 5 runtime release does not expose a reviewed MP11 NRL schedule as a "
            "separate model-input contract."
        ),
        delta_class="model_parameter_update",
        implementation_class="scenario_and_account_update",
        phase7_plus_followup=(
            "Create an explicit NRL/disturbance-loss parameter surface and test whether it "
            "belongs in yield curves, accounts, harvest-flow comparison, or sensitivity runs."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="The 1.5% NRL signal is a comparison target, not an accepted input.",
    ),
    AssumptionComparison(
        assumption_id="minimum_harvest_age",
        assumption_family="harvest_rules",
        mp11_summary=(
            "MP11 replaces MP10 DBH/harvest-system MHA criteria with 95% CMAI age plus "
            "a minimum 350 m3/ha volume requirement; future stands have weighted average "
            "MHA 64 years and average volume 586 m3/ha."
        ),
        mp11_pdf_pages="258, 273, 400-404",
        mp11_source_context="Appendix B sections 3.1, 3.6.4, and 10.4.1; Tables 71-72.",
        phase5_surface="planning/tfl6_state_transition_contract.md; planning/tfl6_treatment_option_contract.md",
        phase5_summary=(
            "Phase 5 transition/treatment contracts require a future MHA or merchantability "
            "rule but do not yet implement MP11's 95% CMAI plus 350 m3/ha table surface."
        ),
        delta_class="model_rule_update",
        implementation_class="transition_rule_update",
        phase7_plus_followup=(
            "Extract MP11 Tables 71-72 and attach MHA to AU/curve records before model-input rebuild."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="This rule affects treatment eligibility and harvest scheduling.",
    ),
    AssumptionComparison(
        assumption_id="harvest_system_distribution",
        assumption_family="harvest_system",
        mp11_summary=(
            "MP11 reports recent harvest and THLB distributions by ground, cable, and "
            "non-conventional systems; THLB is 57.3% ground, 39.6% cable, and 3.1% "
            "non-conventional by area."
        ),
        mp11_pdf_pages="265-266, 298, 405",
        mp11_source_context="Appendix B sections 3.5.1.4, 6.8, and 10.4.2.2; Tables 7, 20, and 73.",
        phase5_surface="planning/tfl6_treatment_option_contract.md; docs/phase5-known-limitations-release-readiness.rst",
        phase5_summary=(
            "Phase 5 requires ground/cable/heli fields in the treatment contract but leaves "
            "actual assignment deferred and uses generic CC treatment in the runtime."
        ),
        delta_class="deferred_phase5_surface_now_has_mp11_target",
        implementation_class="harvest_system_classifier_update",
        phase7_plus_followup=(
            "Build a harvest-system assignment lane and calibrate public proxies against "
            "MP11 reported THLB and recent-harvest distributions."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="MP11 percentages can be calibration targets, not direct stand-level assignments.",
    ),
    AssumptionComparison(
        assumption_id="spatial_patchworks_harvest_rules",
        assumption_family="model_structure",
        mp11_summary=(
            "MP11 uses Patchworks spatial optimization with green-up, adjacency, patch-size, "
            "visual-quality, biodiversity, watershed, and old-growth constraints; harvest "
            "patch target is 2 ha."
        ),
        mp11_pdf_pages="257-258, 274, 404-410",
        mp11_source_context="Appendix B sections 3.1, 4, and 10.4.2-10.4.5.",
        phase5_surface="docs/phase5-runtime-release.rst; docs/phase5-rebuild-provenance.rst",
        phase5_summary=(
            "Phase 5 produces a teaching Patchworks runtime, but some MP11 constraint "
            "surfaces remain simplified, fallback, or deferred."
        ),
        delta_class="model_constraint_update",
        implementation_class="patchworks_runtime_overhaul",
        phase7_plus_followup=(
            "Separate constraints that can be rebuilt from public layers from constraints "
            "that require WFP-specific model surfaces."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="P6.4 scopes the overhaul; it does not alter the current runtime package.",
    ),
    AssumptionComparison(
        assumption_id="riparian_terrain_karst_retention_resource_netdowns",
        assumption_family="resource_constraints",
        mp11_summary=(
            "MP11 uses LiDAR stream classification, terrain/DTSM plus LiDAR slope, karst "
            "features, OGMAs/WHAs/UWRs, research/PSP/big-tree reserves, and future WTRAs "
            "as explicit land-base and constraint assumptions."
        ),
        mp11_pdf_pages="258, 272-273, 300-310, 406-409",
        mp11_source_context=(
            "Appendix B sections 3.1, 3.6, 6.9-6.23, and 10.4.3; Tables 21-26 and 74."
        ),
        phase5_surface="config/tsr/thlb_netdown.recipe.yaml; planning/tfl6_mp11_netdown_delta_crosswalk.md",
        phase5_summary=(
            "Phase 5 has public-layer and benchmark-calibrated netdown surfaces, but MP11 "
            "adds or refines several WFP/LiDAR/practice-based categories."
        ),
        delta_class="mixed_public_proxy_and_private_data_update",
        implementation_class="source_layer_and_constraint_overhaul",
        phase7_plus_followup=(
            "Drive follow-on issue breakdown from the P6.3 netdown delta crosswalk and "
            "treat LiDAR/practice-derived categories as explicit reproducibility gaps."
        ),
        review_status="reviewed_evidence",
        downstream_use="phase6_assumption_comparison_only",
        model_input_status="not_model_input",
        notes="This row links P6.3 netdown work with the broader P6.4 assumption review.",
    ),
]


def write_outputs(output_csv: Path, output_json: Path, output_md: Path, generated_at_utc: str) -> list[AssumptionComparison]:
    """Write the P6.4 crosswalk to CSV, JSON, and Markdown."""

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(ROWS[0]).keys()))
        writer.writeheader()
        for row in ROWS:
            writer.writerow(asdict(row))

    delta_counts: dict[str, int] = {}
    implementation_counts: dict[str, int] = {}
    for row in ROWS:
        delta_counts[row.delta_class] = delta_counts.get(row.delta_class, 0) + 1
        implementation_counts[row.implementation_class] = implementation_counts.get(row.implementation_class, 0) + 1

    payload = {
        "generated_at_utc": generated_at_utc,
        "source_sha256": SOURCE_SHA256,
        "crosswalk_csv": output_csv.as_posix(),
        "row_count": len(ROWS),
        "review_status_counts": {"reviewed_evidence": len(ROWS)},
        "downstream_use_counts": {"phase6_assumption_comparison_only": len(ROWS)},
        "model_input_status_counts": {"not_model_input": len(ROWS)},
        "delta_class_counts": delta_counts,
        "implementation_class_counts": implementation_counts,
        "rows": [asdict(row) for row in ROWS],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, payload)
    return list(ROWS)


def _write_markdown(path: Path, payload: dict[str, object]) -> None:
    lines = [
        "# TFL 6 MP11 Inventory, Yield, Operability, And Harvest-System Assumption Crosswalk",
        "",
        "## Purpose",
        "",
        "This P6.4 note compares MP11 inventory, LiDAR/ITI, yield, operability,",
        "harvest-system, and harvest-rule assumptions against the accepted Phase 5",
        "FEMIC/Patchworks teaching prototype surfaces. It is a planning and",
        "implementation-scoping artifact only. It does not promote any MP11 value",
        "or rule to model-input status.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`",
        "- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.csv`",
        "- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.json`",
        "",
        "## Status",
        "",
        f"- Rows: `{payload['row_count']}`",
        "- Review status: `reviewed_evidence`",
        "- Downstream use: `phase6_assumption_comparison_only`",
        "- Model-input status: `not_model_input`",
        "",
        "## Classification Counts",
        "",
        "### Delta Classes",
        "",
    ]

    for key, value in sorted(dict(payload["delta_class_counts"]).items()):
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "### Implementation Classes", ""])

    for key, value in sorted(dict(payload["implementation_class_counts"]).items()):
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(
        [
            "",
            "## Crosswalk",
            "",
            "| Assumption | Family | Delta class | Implementation class | Phase 7+ follow-up |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for raw_row in payload["rows"]:
        row = dict(raw_row)
        lines.append(
            "| "
            f"`{row['assumption_id']}` | "
            f"{row['assumption_family']} | "
            f"`{row['delta_class']}` | "
            f"`{row['implementation_class']}` | "
            f"{row['phase7_plus_followup']} |"
        )

    lines.extend(["", "## Reviewed Rows", ""])
    for raw_row in payload["rows"]:
        row = dict(raw_row)
        lines.extend(
            [
                f"### `{row['assumption_id']}`",
                "",
                f"- Family: `{row['assumption_family']}`",
                f"- MP11 pages: `{row['mp11_pdf_pages']}`",
                f"- Delta class: `{row['delta_class']}`",
                f"- Implementation class: `{row['implementation_class']}`",
                f"- Review status: `{row['review_status']}`",
                f"- Downstream use: `{row['downstream_use']}`",
                f"- Model-input status: `{row['model_input_status']}`",
                "",
                "MP11 summary:",
                "",
                row["mp11_summary"],
                "",
                "Phase 5 comparison surface:",
                "",
                row["phase5_summary"],
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
            "P6.4 confirms that an MP11-aligned model is not a small parameter update.",
            "The future implementation lane needs a source-layer refresh, AU/yield",
            "contract decision, managed-yield parameter extraction, harvest-system",
            "classifier, MHA rule extraction, and Patchworks constraint review. Every",
            "row in this crosswalk remains comparison evidence only until a later",
            "phase explicitly promotes it through reviewed implementation artifacts.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("planning"),
        help="Directory for crosswalk outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    output_dir = args.output_dir
    write_outputs(
        output_csv=output_dir / "tfl6_mp11_inventory_yield_operability_crosswalk.csv",
        output_json=output_dir / "tfl6_mp11_inventory_yield_operability_crosswalk.json",
        output_md=output_dir / "tfl6_mp11_inventory_yield_operability_crosswalk.md",
        generated_at_utc=generated_at_utc,
    )


if __name__ == "__main__":
    main()
