"""Build the P10.5 MP11 managed-curve diagnostic surface."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_au_curve_lane_crosswalk.csv"
PHASE5_DIAGNOSTICS_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_managed_curve_diagnostics.csv"
OVERLAY_MANIFEST_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_vdyp_overlay_manifest.csv"
PARAMETER_LIBRARY_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_yield_parameter_library.csv"

OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_diagnostics.md"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_diagnostics.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_diagnostics.json"

LANE_TO_PHASE5 = {
    "early_managed": "existing_managed_11_50",
    "recent_managed": "existing_managed_1_10",
    "future_managed": "future_managed",
}


def build_diagnostics() -> pd.DataFrame:
    crosswalk = pd.read_csv(CROSSWALK_PATH)
    managed = crosswalk[crosswalk["curve_lane"].isin(LANE_TO_PHASE5)].copy()
    managed["phase5_curve_lane"] = managed["curve_lane"].map(LANE_TO_PHASE5)

    phase5 = pd.read_csv(PHASE5_DIAGNOSTICS_PATH).rename(
        columns={
            "curve_lane": "phase5_curve_lane",
            "match_confidence": "phase5_mp10_match_confidence",
        }
    )
    overlays = pd.read_csv(OVERLAY_MANIFEST_PATH)[["au_id", "plot_path", "has_natural_curve"]]
    params = pd.read_csv(PARAMETER_LIBRARY_PATH)

    parser_required_tables = set(
        params.loc[params["review_status"] == "parser_review_required", "source_table"]
        .dropna()
        .astype(str)
    )
    diagnostics = managed.merge(
        phase5[
            [
                "au_id",
                "phase5_curve_lane",
                "feature_id",
                "matched_legacy_au_code",
                "phase5_mp10_match_confidence",
                "max_treated_volume",
                "age_at_max_treated_volume",
                "treated_volume_age_40",
                "treated_volume_age_60",
                "treated_volume_age_80",
                "treated_volume_age_100",
                "natural_max_volume",
                "treated_to_natural_max_ratio",
                "other_species_pct_encoded_as_dr",
            ]
        ],
        on=["au_id", "phase5_curve_lane"],
        how="left",
    )
    diagnostics = diagnostics.merge(overlays, on="au_id", how="left")
    diagnostics["phase5_comparison_curve_available"] = diagnostics["feature_id"].notna()
    diagnostics["mp11_curve_generation_status"] = diagnostics["mp11_source_table"].map(
        lambda table: (
            "blocked_pending_per_au_table_parser"
            if table in parser_required_tables
            else "parameter_candidate_available"
        )
    )
    diagnostics["review_status"] = diagnostics.apply(
        lambda row: (
            "mp11_parser_blocked_with_phase5_comparison"
            if row["phase5_comparison_curve_available"]
            else "mp11_parser_blocked_no_phase5_comparison"
        ),
        axis=1,
    )
    diagnostics["downstream_use"] = "phase10_managed_curve_diagnostics_only"
    diagnostics["model_input_status"] = "not_model_input"
    return diagnostics.sort_values(
        ["selected_top_90_stratum", "area_ha", "curve_lane"], ascending=[False, False, True]
    )


def write_outputs(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_CSV, index=False)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "row_count": int(len(df)),
        "au_count": int(df["au_id"].nunique()),
        "curve_lane_counts": df["curve_lane"].value_counts().sort_index().to_dict(),
        "mp11_curve_generation_status_counts": df["mp11_curve_generation_status"]
        .value_counts()
        .sort_index()
        .to_dict(),
        "review_status_counts": df["review_status"].value_counts().sort_index().to_dict(),
        "phase5_comparison_curve_available_rows": int(df["phase5_comparison_curve_available"].sum()),
        "selected_top_90_rows": int(df["selected_top_90_stratum"].sum()),
        "model_input_status_counts": df["model_input_status"].value_counts().sort_index().to_dict(),
    }
    OUTPUT_JSON.write_text(
        json.dumps({**summary, "records": df.to_dict(orient="records")}, indent=2) + "\n",
        encoding="utf-8",
    )

    selected = df[df["selected_top_90_stratum"]]
    high_area = selected.sort_values("area_ha", ascending=False).head(25)
    lines = [
        "# TFL 6 MP11 Managed-Curve Diagnostics",
        "",
        "## Purpose",
        "",
        "This P10.5 artifact records the managed-curve status after P10.2 and",
        "P10.3. It does not generate MP11 managed curves because Tables 54, 55,",
        "and 57 still require reviewed per-AU TIPSY row parsing. Existing Phase 5",
        "MP10-derived managed curves are retained as comparison baselines.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_managed_curve_diagnostics.md`",
        "- `planning/tfl6_mp11_managed_curve_diagnostics.csv`",
        "- `planning/tfl6_mp11_managed_curve_diagnostics.json`",
        "",
        "## Status",
        "",
        f"- Diagnostic rows: `{summary['row_count']}`",
        f"- Canonical AU count: `{summary['au_count']}`",
        f"- Selected top-90 managed lane rows: `{summary['selected_top_90_rows']}`",
        f"- Phase 5 comparison curve rows available: `{summary['phase5_comparison_curve_available_rows']}`",
        "- MP11 managed curve rows generated: `0`",
        "- Model-input status: `not_model_input`",
        "",
        "## MP11 Generation Status Counts",
        "",
    ]
    for key, value in summary["mp11_curve_generation_status_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Review Status Counts",
            "",
        ]
    )
    for key, value in summary["review_status_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "- MP11 managed curves remain blocked until Tables 54, 55, and 57 have",
            "  reviewed per-AU row parsers and QA outputs.",
            "- Existing Phase 5 managed curves remain comparison/fallback evidence,",
            "  not MP11-equivalent curves.",
            "- VRAF parameters from P10.2 are not hidden inside base managed curves;",
            "  they require later harvest-time implementation review.",
            "- All rows remain `not_model_input` until Phase 11 promotion review.",
            "",
            "## High-Area Selected Managed Rows",
            "",
            "| au_id | curve_lane | area_ha | mp11_status | phase5_match | max_treated_volume | ratio_to_natural |",
            "| --- | --- | ---: | --- | --- | ---: | ---: |",
        ]
    )
    for _, row in high_area.iterrows():
        max_vol = "" if pd.isna(row["max_treated_volume"]) else f"{float(row['max_treated_volume']):.3f}"
        ratio = (
            ""
            if pd.isna(row["treated_to_natural_max_ratio"])
            else f"{float(row['treated_to_natural_max_ratio']):.3f}"
        )
        lines.append(
            f"| `{row['au_id']}` | `{row['curve_lane']}` | {float(row['area_ha']):.3f} | "
            f"`{row['mp11_curve_generation_status']}` | "
            f"`{row['phase5_mp10_match_confidence']}` | {max_vol} | {ratio} |"
        )
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_outputs(build_diagnostics())


if __name__ == "__main__":
    main()
