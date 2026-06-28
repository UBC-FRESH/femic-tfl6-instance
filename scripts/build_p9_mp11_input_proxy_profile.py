"""Build Phase 9 inventory and public-proxy input profiles for MP11 THLB work."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd


@dataclass(frozen=True)
class CandidateProfile:
    """Candidate field or proxy profile for later MP11 THLB rule review."""

    candidate_id: str
    candidate_family: str
    source_layer: str
    candidate_expression: str
    row_count: int | None
    area_ha: float | None
    length_km: float | None
    field_names: str
    review_status: str
    phase9_decision: str
    model_input_status: str
    notes: str


def _area_ha(frame: gpd.GeoDataFrame, mask: pd.Series) -> float:
    if frame.empty:
        return 0.0
    return float(frame.loc[mask, frame.geometry.name].area.sum() / 10_000.0)


def _candidate(
    candidate_id: str,
    family: str,
    source_layer: str,
    expression: str,
    row_count: int | None,
    area_ha: float | None,
    length_km: float | None,
    fields: list[str],
    decision: str,
    notes: str,
) -> CandidateProfile:
    return CandidateProfile(
        candidate_id=candidate_id,
        candidate_family=family,
        source_layer=source_layer,
        candidate_expression=expression,
        row_count=row_count,
        area_ha=area_ha,
        length_km=length_km,
        field_names=", ".join(fields),
        review_status="candidate_profile_only",
        phase9_decision=decision,
        model_input_status="not_model_input",
        notes=notes,
    )


def _read_vector(path: str) -> gpd.GeoDataFrame:
    return gpd.read_file(path)


def _top_values(frame: pd.DataFrame, fields: list[str], source_layer: str) -> list[CandidateProfile]:
    rows: list[CandidateProfile] = []
    for field in fields:
        if field not in frame.columns:
            continue
        value_counts = frame[field].value_counts(dropna=False).head(10)
        rows.append(
            _candidate(
                f"{source_layer}_{field}_top_values",
                "field_distribution",
                source_layer,
                f"top values for `{field}`",
                int(len(frame)),
                None,
                None,
                [field],
                "profile_for_p9_3_review",
                "; ".join(f"{value}: {count}" for value, count in value_counts.items()),
            )
        )
    return rows


def _profile_vri() -> list[CandidateProfile]:
    frame = _read_vector("data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg")
    rows: list[CandidateProfile] = []
    layer = "vri_2025_r1_tfl6"

    bclcs_nonforest = frame["bclcs_level_1"].isin(["N", "U"])
    rows.append(
        _candidate(
            "vri_bclcs_level1_nonforest_candidate",
            "forest_status",
            layer,
            "bclcs_level_1 in {'N', 'U'}",
            int(bclcs_nonforest.sum()),
            _area_ha(frame, bclcs_nonforest),
            None,
            ["bclcs_level_1"],
            "candidate_for_p9_4_review",
            "Conservative non-forest/unreported candidate. Final null handling remains review-required.",
        )
    )

    bclcs_level2_not_treed = frame["bclcs_level_2"].isin(["N", "W"]) | frame["bclcs_level_2"].isna()
    rows.append(
        _candidate(
            "vri_bclcs_level2_non_treed_water_null_candidate",
            "forest_status",
            layer,
            "bclcs_level_2 in {'N', 'W'} or null",
            int(bclcs_level2_not_treed.sum()),
            _area_ha(frame, bclcs_level2_not_treed),
            None,
            ["bclcs_level_2"],
            "candidate_for_p9_4_review",
            "Broader non-treed/water/null review envelope; not an accepted exclusion rule.",
        )
    )

    explicit_nonproductive = frame["non_productive_descriptor_cd"].notna() | frame["non_productive_cd"].notna()
    rows.append(
        _candidate(
            "vri_explicit_nonproductive_candidate",
            "productivity",
            layer,
            "non_productive_descriptor_cd not null or non_productive_cd not null",
            int(explicit_nonproductive.sum()),
            _area_ha(frame, explicit_nonproductive),
            None,
            ["non_productive_descriptor_cd", "non_productive_cd"],
            "candidate_for_p9_4_review",
            "Explicit non-productive signal candidate; overlap with non-forest must be handled by ordered overlay.",
        )
    )

    low_site = frame["site_index"].notna() & (frame["site_index"] < 5)
    rows.append(
        _candidate(
            "vri_site_index_lt5_candidate",
            "productivity",
            layer,
            "site_index < 5",
            int(low_site.sum()),
            _area_ha(frame, low_site),
            None,
            ["site_index"],
            "candidate_for_p9_4_review",
            "Low-site threshold candidate inherited from earlier teaching-lane review; MP11 LiDAR/LEFI gap remains.",
        )
    )

    deciduous = frame["species_cd_1"].isin(["DR", "AC", "MB"])
    rows.append(
        _candidate(
            "vri_deciduous_leading_candidate",
            "species",
            layer,
            "species_cd_1 in {'DR', 'AC', 'MB'}",
            int(deciduous.sum()),
            _area_ha(frame, deciduous),
            None,
            ["species_cd_1"],
            "candidate_for_p9_4_review",
            "Leading deciduous candidate; does not remove conifer-leading stands with deciduous components.",
        )
    )

    low_height = frame["proj_height_class_cd_1"].isin(["0", "1", "2"])
    rows.append(
        _candidate(
            "vri_low_height_operability_candidate",
            "operability_proxy",
            layer,
            "proj_height_class_cd_1 in {'0', '1', '2'}",
            int(low_height.sum()),
            _area_ha(frame, low_height),
            None,
            ["proj_height_class_cd_1"],
            "candidate_for_p9_3_review",
            "Economic/physical operability proxy candidate only; not a final exclusion.",
        )
    )

    low_volume = frame["live_stand_volume_125"].notna() & (frame["live_stand_volume_125"] < 100)
    rows.append(
        _candidate(
            "vri_low_volume_operability_candidate",
            "operability_proxy",
            layer,
            "live_stand_volume_125 < 100",
            int(low_volume.sum()),
            _area_ha(frame, low_volume),
            None,
            ["live_stand_volume_125"],
            "candidate_for_p9_3_review",
            "Public volume proxy for marginal economic operability; threshold is review-only.",
        )
    )

    hembal_height3 = (
        frame["species_cd_1"].isin(["HW", "HM", "BA"])
        & frame["proj_height_class_cd_1"].isin(["3"])
    )
    rows.append(
        _candidate(
            "vri_hembal_height3_operability_candidate",
            "operability_proxy",
            layer,
            "species_cd_1 in {'HW', 'HM', 'BA'} and proj_height_class_cd_1 == '3'",
            int(hembal_height3.sum()),
            _area_ha(frame, hembal_height3),
            None,
            ["species_cd_1", "proj_height_class_cd_1"],
            "candidate_for_p9_3_review",
            "Earlier operability evidence treats lower-value hembal height class 3 as conditional/marginal.",
        )
    )

    management_no = frame["for_mgmt_land_base_ind"].eq("N")
    rows.append(
        _candidate(
            "vri_for_mgmt_land_base_no_qa_signal",
            "qa_signal",
            layer,
            "for_mgmt_land_base_ind == 'N'",
            int(management_no.sum()),
            _area_ha(frame, management_no),
            None,
            ["for_mgmt_land_base_ind"],
            "qa_only",
            "Useful QA signal only; do not use as a hidden THLB deduction.",
        )
    )

    rows.extend(
        _top_values(
            frame,
            [
                "bclcs_level_1",
                "bclcs_level_2",
                "non_productive_descriptor_cd",
                "non_productive_cd",
                "species_cd_1",
                "proj_height_class_cd_1",
                "crown_closure_class_cd",
            ],
            layer,
        )
    )
    return rows


def _profile_vector_schema(path: str, layer: str, family: str, fields: list[str]) -> list[CandidateProfile]:
    frame = _read_vector(path)
    rows = _top_values(frame, [field for field in fields if field in frame.columns], layer)
    if frame.geometry.geom_type.isin(["LineString", "MultiLineString"]).any():
        length_km = float(frame.geometry.length.sum() / 1_000.0)
        area_ha = None
    elif frame.geometry.geom_type.isin(["Polygon", "MultiPolygon"]).any():
        area_ha = float(frame.geometry.area.sum() / 10_000.0)
        length_km = None
    else:
        area_ha = None
        length_km = None
    rows.append(
        _candidate(
            f"{layer}_geometry_summary",
            family,
            layer,
            "geometry summary",
            int(len(frame)),
            area_ha,
            length_km,
            [field for field in fields if field in frame.columns],
            "profile_for_p9_3_review",
            "Geometry and field summary only; final overlay filters remain review-required.",
        )
    )
    return rows


def _profile_vdyp_tables() -> list[CandidateProfile]:
    rows: list[CandidateProfile] = []
    for path, layer in [
        ("data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet", "vdyp7_2025_poly_tfl6"),
        ("data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet", "vdyp7_2025_layer_tfl6"),
    ]:
        frame = pd.read_parquet(path)
        fields = [str(column) for column in frame.columns[:20]]
        rows.append(
            _candidate(
                f"{layer}_table_schema_summary",
                "inventory_attribute_join",
                layer,
                "parquet row and field summary",
                int(len(frame)),
                None,
                None,
                fields,
                "profile_for_p9_3_review",
                "VDYP table is a join attribute source; R1 remains the complete accounting surface.",
            )
        )
        if "feature_id" in frame.columns:
            rows.append(
                _candidate(
                    f"{layer}_feature_id_uniqueness",
                    "join_qa",
                    layer,
                    "feature_id uniqueness profile",
                    int(frame["feature_id"].nunique()),
                    None,
                    None,
                    ["feature_id"],
                    "qa_only",
                    f"Rows={len(frame):,}; unique feature_id={frame['feature_id'].nunique():,}.",
                )
            )
    return rows


def build_profiles(output_csv: Path, output_json: Path, output_md: Path) -> list[CandidateProfile]:
    rows: list[CandidateProfile] = []
    rows.extend(_profile_vri())
    rows.extend(_profile_vdyp_tables())
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/roads/dra_roads_tfl6.gpkg",
            "dra_roads_tfl6",
            "roads",
            ["TRANSPORT_LINE_TYPE_CODE", "ROAD_SURFACE_TYPE_CODE", "LEFT_LOCALITY", "RIGHT_LOCALITY"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/hydrology/fwa_stream_networks_tfl6.gpkg",
            "fwa_stream_networks_tfl6",
            "hydrology",
            ["STREAM_ORDER", "STREAM_MAGNITUDE", "WATERSHED_GROUP_CODE", "GNIS_NAME"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/hydrology/fwa_lakes_tfl6.gpkg",
            "fwa_lakes_tfl6",
            "hydrology",
            ["WATERBODY_TYPE", "GNIS_NAME", "WATERSHED_GROUP_CODE"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/hydrology/fwa_wetlands_tfl6.gpkg",
            "fwa_wetlands_tfl6",
            "hydrology",
            ["WETLAND_TYPE", "WATERSHED_GROUP_CODE"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg",
            "ogma_legal_current_tfl6",
            "legal_reserves",
            ["OGMA_TYPE", "OGMA_PRIMARY_REASON", "LEGALIZATION_FRPA_DATE", "LAST_AMENDMENT_DATE"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/ogma/ogma_non_legal_current_tfl6.gpkg",
            "ogma_non_legal_current_tfl6",
            "legal_reserves",
            ["OGMA_TYPE", "OGMA_PRIMARY_REASON", "ORIGINAL_DECISION_DATE", "LAST_AMENDMENT_DATE"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg",
            "wha_approved_tfl6",
            "legal_reserves",
            ["TAG", "COMMON_SPECIES_NAME", "APPROVAL_DATE", "FEATURE_AREA_SQM"],
        )
    )
    rows.extend(
        _profile_vector_schema(
            "data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg",
            "uwr_approved_tfl6",
            "legal_reserves",
            ["UWR_NUMBER", "SPECIES_1", "APPROVAL_DATE", "FEATURE_AREA_SQM"],
        )
    )

    _write_outputs(output_csv, output_json, output_md, rows)
    return rows


def _write_outputs(output_csv: Path, output_json: Path, output_md: Path, rows: list[CandidateProfile]) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    payload: dict[str, Any] = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "row_count": len(rows),
        "candidate_family_counts": _counts(rows, "candidate_family"),
        "phase9_decision_counts": _counts(rows, "phase9_decision"),
        "outputs": {
            "csv": output_csv.as_posix(),
            "json": output_json.as_posix(),
            "markdown": output_md.as_posix(),
        },
        "rows": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, rows, payload)


def _counts(rows: list[CandidateProfile], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(getattr(row, field))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _fmt(value: float | None) -> str:
    return "" if value is None else f"{value:,.3f}"


def _write_markdown(path: Path, rows: list[CandidateProfile], payload: dict[str, Any]) -> None:
    lines = [
        "# TFL 6 MP11 Phase 9 Inventory And Proxy Input Profile",
        "",
        "## Purpose",
        "",
        "This P9.3 profile records candidate public inventory fields, public",
        "proxy variables, and overlay-source field summaries needed before an",
        "MP11 public-data THLB overlay recipe can be implemented. It does not",
        "accept final overlay rules and does not generate THLB outputs.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_phase9_input_proxy_profile.md`",
        "- `planning/tfl6_mp11_phase9_input_proxy_profile.csv`",
        "- `planning/tfl6_mp11_phase9_input_proxy_profile.json`",
        "",
        "## Status Counts",
        "",
        f"- Rows: `{payload['row_count']}`",
        f"- Candidate family counts: `{payload['candidate_family_counts']}`",
        f"- Phase 9 decision counts: `{payload['phase9_decision_counts']}`",
        "",
        "## Candidate Profile Table",
        "",
        "| Candidate | Family | Source | Rows | Area ha | Length km | Decision |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        count = "" if row.row_count is None else f"{row.row_count:,}"
        lines.append(
            f"| `{row.candidate_id}` | {row.candidate_family} | `{row.source_layer}` | "
            f"{count} | {_fmt(row.area_ha)} | {_fmt(row.length_km)} | "
            f"`{row.phase9_decision}` |"
        )
    lines.extend(
        [
            "",
            "## Key Findings",
            "",
            "- R1/VRI contains candidate signals for non-forest, explicit",
            "  non-productive, low-site, deciduous-leading, low-height, low-volume,",
            "  and hemlock/balsam height-class-three proxy review.",
            "- VDYP polygon/layer parquet tables are readable and should remain join",
            "  attribute sources; R1 remains the complete area accounting surface.",
            "- Roads, hydrology, legal reserve, and recreation layers have profile",
            "  summaries, but final filters, buffers, and overlay order remain",
            "  P9.4 decisions.",
            "- DEM/slope and shoreline are still unresolved source/proxy gaps from",
            "  P9.2; no slope or shoreline proxy is accepted by this profile.",
            "",
            "## Use Boundary",
            "",
            "Rows in this profile are `candidate_profile_only` or `qa_only`. They",
            "are not accepted model inputs and do not authorize final THLB overlay",
            "execution without the P9.4 recipe review.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_input_proxy_profile.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_input_proxy_profile.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_input_proxy_profile.md"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_profiles(args.output_csv, args.output_json, args.output_md)


if __name__ == "__main__":
    main()
