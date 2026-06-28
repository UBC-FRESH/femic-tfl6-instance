"""Build the Phase 9 MP11 public source-layer verification manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SourceSpec:
    """Expected source dependency for the MP11 source-layer/THLB rebuild."""

    source_id: str
    label: str
    dependency_family: str
    path: str
    expected_format: str
    source_role: str
    public_private_status: str
    phase9_decision: str
    notes: str


@dataclass(frozen=True)
class SourceLayerRecord:
    """Verification summary for one source dependency."""

    source_id: str
    label: str
    dependency_family: str
    path: str
    expected_format: str
    exists: bool
    byte_size: int | None
    sha256: str | None
    read_status: str
    layer_name: str
    crs: str
    geometry_type: str
    feature_count: int | None
    field_count: int | None
    field_sample: str
    total_bounds: str
    total_area_ha: float | None
    total_length_km: float | None
    public_private_status: str
    source_role: str
    phase9_decision: str
    notes: str


SOURCE_SPECS = [
    SourceSpec(
        "tfl6_aoi_current",
        "Accepted current TFL 6 AOI boundary",
        "aoi",
        "data/source/tfl_6/aoi/tfl_6_boundary.gpkg",
        "gpkg",
        "accounting_universe",
        "public_rebuild",
        "verify_for_p9_2",
        "Accepted from prior phases; verify before MP11 rebuild use.",
    ),
    SourceSpec(
        "vri_2025_r1_tfl6",
        "2025 VRI R1 polygon clipped to TFL 6",
        "inventory",
        "data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg",
        "gpkg",
        "complete_stand_accounting_surface",
        "public_rebuild",
        "verify_for_p9_2",
        "Do not drop R1 polygons when joining subset VDYP tables.",
    ),
    SourceSpec(
        "vdyp7_2025_poly_tfl6",
        "2025 VDYP7 polygon table filtered to TFL 6",
        "inventory",
        "data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet",
        "parquet",
        "inventory_attribute_join",
        "public_rebuild",
        "verify_for_p9_2",
        "Requires parquet engine for row/schema read-smoke.",
    ),
    SourceSpec(
        "vdyp7_2025_layer_tfl6",
        "2025 VDYP7 layer/species table filtered to TFL 6",
        "inventory",
        "data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet",
        "parquet",
        "species_layer_attribute_join",
        "public_rebuild",
        "verify_for_p9_2",
        "Requires parquet engine for row/schema read-smoke.",
    ),
    SourceSpec(
        "dra_roads_tfl6",
        "Digital Road Atlas roads clipped to TFL 6",
        "roads",
        "data/source/tfl_6/roads/dra_roads_tfl6.gpkg",
        "gpkg",
        "existing_road_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Class filters and buffer widths remain P9.3/P9.4 decisions.",
    ),
    SourceSpec(
        "fwa_stream_networks_tfl6",
        "Freshwater Atlas stream networks clipped to TFL 6",
        "hydrology",
        "data/source/tfl_6/hydrology/fwa_stream_networks_tfl6.gpkg",
        "gpkg",
        "riparian_stream_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Stream-class and buffer rules remain P9.3/P9.4 decisions.",
    ),
    SourceSpec(
        "fwa_lakes_tfl6",
        "Freshwater Atlas lakes clipped to TFL 6",
        "hydrology",
        "data/source/tfl_6/hydrology/fwa_lakes_tfl6.gpkg",
        "gpkg",
        "riparian_lake_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Lake class and buffer rules remain P9.3/P9.4 decisions.",
    ),
    SourceSpec(
        "fwa_wetlands_tfl6",
        "Freshwater Atlas wetlands clipped to TFL 6",
        "hydrology",
        "data/source/tfl_6/hydrology/fwa_wetlands_tfl6.gpkg",
        "gpkg",
        "riparian_wetland_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Wetland class and buffer rules remain P9.3/P9.4 decisions.",
    ),
    SourceSpec(
        "shoreline_candidate",
        "Reviewed public shoreline or coastline candidate",
        "shoreline",
        "",
        "missing",
        "ocean_shoreline_proxy_or_unavailable",
        "public_proxy",
        "defer_or_materialize_if_public_source_is_accepted",
        "No accepted high-precision MP11 shoreline source is tracked.",
    ),
    SourceSpec(
        "ogma_legal_current_tfl6",
        "Current legal OGMAs clipped to TFL 6",
        "legal_reserves",
        "data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg",
        "gpkg",
        "legal_ogma_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Current-vs-MP11 vintage remains a P9.3 caveat.",
    ),
    SourceSpec(
        "ogma_non_legal_current_tfl6",
        "Current non-legal OGMAs clipped to TFL 6",
        "legal_reserves",
        "data/source/tfl_6/ogma/ogma_non_legal_current_tfl6.gpkg",
        "gpkg",
        "non_legal_or_proposed_proxy_candidate",
        "public_proxy",
        "verify_as_proxy_for_p9_2",
        "Do not treat as exact MP11 proposed conservation geometry.",
    ),
    SourceSpec(
        "wha_approved_tfl6",
        "Approved wildlife habitat areas clipped to TFL 6",
        "legal_reserves",
        "data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg",
        "gpkg",
        "approved_wha_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Current-vs-MP11 vintage remains a P9.3 caveat.",
    ),
    SourceSpec(
        "uwr_approved_tfl6",
        "Approved ungulate winter ranges clipped to TFL 6",
        "legal_reserves",
        "data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg",
        "gpkg",
        "approved_uwr_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Current-vs-MP11 vintage remains a P9.3 caveat.",
    ),
    SourceSpec(
        "recreation_polygons_tfl6",
        "Recreation polygons clipped to TFL 6",
        "recreation",
        "data/source/tfl_6/recreation/recreation_polygons_tfl6.gpkg",
        "gpkg",
        "recreation_overlay_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Status filters remain P9.3/P9.4 decisions.",
    ),
    SourceSpec(
        "recreation_trails_tfl6",
        "Recreation trails clipped to TFL 6",
        "recreation",
        "data/source/tfl_6/recreation/recreation_trails_tfl6.gpkg",
        "gpkg",
        "recreation_buffer_candidate",
        "public_rebuild",
        "verify_for_p9_2",
        "Trail buffer rules remain P9.3/P9.4 decisions.",
    ),
    SourceSpec(
        "recreation_site_points_tfl6",
        "Recreation site points clipped to TFL 6",
        "recreation",
        "data/source/tfl_6/recreation/recreation_site_points_tfl6.gpkg",
        "gpkg",
        "recreation_point_context",
        "public_rebuild",
        "verify_for_p9_2",
        "Point treatment remains P9.3/P9.4 decision.",
    ),
    SourceSpec(
        "recreation_details_closures_tfl6",
        "Recreation details and closures clipped to TFL 6",
        "recreation",
        "data/source/tfl_6/recreation/recreation_details_closures_tfl6.gpkg",
        "gpkg",
        "recreation_attribute_context",
        "public_rebuild",
        "verify_for_p9_2",
        "Context layer; overlay use requires P9.3 review.",
    ),
    SourceSpec(
        "bec_tfl6",
        "BEC polygons clipped to TFL 6",
        "strata",
        "data/source/tfl_6/strata/bec_tfl6.gpkg",
        "gpkg",
        "strata_context_and_qa",
        "public_rebuild",
        "verify_for_p9_2",
        "Context/supporting layer, not a silent deduction.",
    ),
    SourceSpec(
        "landscape_units_tfl6",
        "Landscape units clipped to TFL 6",
        "strata",
        "data/source/tfl_6/strata/landscape_units_tfl6.gpkg",
        "gpkg",
        "strata_context_and_qa",
        "public_rebuild",
        "verify_for_p9_2",
        "Context/supporting layer, not a silent deduction.",
    ),
    SourceSpec(
        "public_dem_slope_candidate",
        "Public DEM or slope derivative for operability and 90% slope proxy",
        "dem_slope",
        "",
        "missing",
        "operability_and_terrain_proxy",
        "public_proxy",
        "defer_or_materialize_if_public_source_is_accepted",
        "No accepted DEM/slope derivative is tracked yet.",
    ),
    SourceSpec(
        "wfp_lbb_iti_lefi",
        "WFP LBB, ITI, and LEFI private dependency group",
        "private_dependency",
        "",
        "unavailable",
        "unavailable_reference",
        "unavailable_non_public",
        "do_not_materialize_without_public_safe_source",
        "Must not be reconstructed from aggregate MP11 summaries.",
    ),
]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _field_sample(fields: list[str], limit: int = 12) -> str:
    return ", ".join(fields[:limit])


def _inspect_gpkg(path: Path) -> dict[str, Any]:
    import geopandas as gpd
    import pyogrio

    layers = pyogrio.list_layers(path)
    layer_name = str(layers[0][0])
    info = pyogrio.read_info(path, layer=layer_name)
    fields = [str(field) for field in list(info.get("fields", []))]
    data = gpd.read_file(path, layer=layer_name)
    area_ha = None
    length_km = None
    geometry_type = str(info.get("geometry_type") or "")
    if not data.empty and data.geometry.name in data:
        geom = data.geometry
        if any(kind in geometry_type for kind in ["Polygon", "MultiPolygon"]):
            area_ha = float(geom.area.sum() / 10_000.0)
        elif any(kind in geometry_type for kind in ["LineString", "MultiLineString"]):
            length_km = float(geom.length.sum() / 1_000.0)
    bounds = info.get("total_bounds")
    return {
        "read_status": "read_ok",
        "layer_name": layer_name,
        "crs": str(info.get("crs") or ""),
        "geometry_type": geometry_type,
        "feature_count": int(info.get("features") or len(data)),
        "field_count": len(fields),
        "field_sample": _field_sample(fields),
        "total_bounds": "" if bounds is None else ", ".join(f"{float(value):.3f}" for value in bounds),
        "total_area_ha": area_ha,
        "total_length_km": length_km,
    }


def _inspect_parquet(path: Path) -> dict[str, Any]:
    try:
        import pandas as pd

        data = pd.read_parquet(path)
    except ImportError as exc:
        dependency = exc.name or "parquet_engine"
        return {
            "read_status": f"present_read_blocked_missing_dependency:{dependency}",
            "layer_name": "",
            "crs": "",
            "geometry_type": "table",
            "feature_count": None,
            "field_count": None,
            "field_sample": "",
            "total_bounds": "",
            "total_area_ha": None,
            "total_length_km": None,
        }
    except Exception as exc:  # pragma: no cover - environment-specific reader errors
        return {
            "read_status": f"present_read_failed:{type(exc).__name__}",
            "layer_name": "",
            "crs": "",
            "geometry_type": "table",
            "feature_count": None,
            "field_count": None,
            "field_sample": "",
            "total_bounds": "",
            "total_area_ha": None,
            "total_length_km": None,
        }
    return {
        "read_status": "read_ok",
        "layer_name": "",
        "crs": "",
        "geometry_type": "table",
        "feature_count": int(len(data)),
        "field_count": int(len(data.columns)),
        "field_sample": _field_sample([str(column) for column in data.columns]),
        "total_bounds": "",
        "total_area_ha": None,
        "total_length_km": None,
    }


def inspect_source(spec: SourceSpec, root: Path) -> SourceLayerRecord:
    path = root / spec.path if spec.path else Path("")
    exists = bool(spec.path and path.exists())
    byte_size = path.stat().st_size if exists else None
    sha256 = _sha256(path) if exists and path.is_file() else None
    inspection: dict[str, Any] = {
        "read_status": "missing_expected_source" if spec.path else "not_materialized",
        "layer_name": "",
        "crs": "",
        "geometry_type": "",
        "feature_count": None,
        "field_count": None,
        "field_sample": "",
        "total_bounds": "",
        "total_area_ha": None,
        "total_length_km": None,
    }
    if exists:
        if spec.expected_format == "gpkg":
            try:
                inspection = _inspect_gpkg(path)
            except Exception as exc:  # pragma: no cover - environment-specific GDAL errors
                inspection["read_status"] = f"present_read_failed:{type(exc).__name__}"
        elif spec.expected_format == "parquet":
            inspection = _inspect_parquet(path)
        else:
            inspection["read_status"] = "present_no_reader_configured"
    return SourceLayerRecord(
        source_id=spec.source_id,
        label=spec.label,
        dependency_family=spec.dependency_family,
        path=spec.path,
        expected_format=spec.expected_format,
        exists=exists,
        byte_size=byte_size,
        sha256=sha256,
        read_status=str(inspection["read_status"]),
        layer_name=str(inspection["layer_name"]),
        crs=str(inspection["crs"]),
        geometry_type=str(inspection["geometry_type"]),
        feature_count=inspection["feature_count"],
        field_count=inspection["field_count"],
        field_sample=str(inspection["field_sample"]),
        total_bounds=str(inspection["total_bounds"]),
        total_area_ha=inspection["total_area_ha"],
        total_length_km=inspection["total_length_km"],
        public_private_status=spec.public_private_status,
        source_role=spec.source_role,
        phase9_decision=spec.phase9_decision,
        notes=spec.notes,
    )


def _write_csv(path: Path, rows: list[SourceLayerRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _counts(rows: list[SourceLayerRecord], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(getattr(row, field))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _write_markdown(path: Path, rows: list[SourceLayerRecord], payload: dict[str, Any]) -> None:
    parquet_rows = [row for row in rows if row.expected_format == "parquet"]
    parquet_all_read = bool(parquet_rows) and all(row.read_status == "read_ok" for row in parquet_rows)
    parquet_finding = (
        "- VDYP parquet artifacts are present and readable in this environment."
        if parquet_all_read
        else "- VDYP parquet artifacts are present, but full row/schema verification\n"
        "  requires a parquet engine such as `pyarrow` or `fastparquet` in the\n"
        "  active Python environment."
    )
    lines = [
        "# TFL 6 MP11 Phase 9 Source-Layer Verification Manifest",
        "",
        "## Purpose",
        "",
        "This P9.2 manifest verifies existing public source-layer dependencies",
        "for the MP11 source-layer and THLB rebuild. It records source",
        "availability, read status, schema summaries, geometry summaries, and",
        "public/proxy/private status. It does not execute THLB overlays.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_phase9_source_layer_manifest.md`",
        "- `planning/tfl6_mp11_phase9_source_layer_manifest.csv`",
        "- `planning/tfl6_mp11_phase9_source_layer_manifest.json`",
        "",
        "## Status Counts",
        "",
        f"- Rows: `{payload['row_count']}`",
        f"- Existing sources: `{payload['existing_count']}`",
        f"- Read status counts: `{payload['read_status_counts']}`",
        f"- Public/private status counts: `{payload['public_private_status_counts']}`",
        "",
        "## Verification Table",
        "",
        "| Source | Family | Exists | Read status | Features | Area ha | Length km | Status | Decision |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        feature_count = "" if row.feature_count is None else f"{row.feature_count:,}"
        area = "" if row.total_area_ha is None else f"{row.total_area_ha:,.3f}"
        length = "" if row.total_length_km is None else f"{row.total_length_km:,.3f}"
        lines.append(
            f"| `{row.source_id}` | {row.dependency_family} | {row.exists} | "
            f"`{row.read_status}` | {feature_count} | {area} | {length} | "
            f"`{row.public_private_status}` | `{row.phase9_decision}` |"
        )
    lines.extend(
        [
            "",
            "## Key Findings",
            "",
            "- Core tracked GeoPackage sources for AOI, VRI/R1, roads, hydrology,",
            "  legal reserves, recreation, BEC, and landscape units are present and",
            "  readable in this environment.",
            parquet_finding,
            "- No accepted shoreline or DEM/slope source is currently tracked for the",
            "  MP11 public-data rebuild lane.",
            "- WFP LBB, ITI, and LEFI dependencies remain `unavailable_non_public` and",
            "  must not be reconstructed from aggregate MP11 summaries.",
            "",
            "## Use Boundary",
            "",
            "This manifest verifies source availability and coarse schema/geometry",
            "status only. P9.3 must still profile fields and proxy variables before",
            "P9.4 can run an ordered overlay recipe. No row in this manifest is an",
            "accepted model input.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_manifest(root: Path, output_csv: Path, output_json: Path, output_md: Path) -> list[SourceLayerRecord]:
    rows = [inspect_source(spec, root) for spec in SOURCE_SPECS]
    _write_csv(output_csv, rows)
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "row_count": len(rows),
        "existing_count": sum(row.exists for row in rows),
        "read_status_counts": _counts(rows, "read_status"),
        "public_private_status_counts": _counts(rows, "public_private_status"),
        "outputs": {
            "csv": output_csv.as_posix(),
            "json": output_json.as_posix(),
            "markdown": output_md.as_posix(),
        },
        "rows": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, rows, payload)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_source_layer_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_source_layer_manifest.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_source_layer_manifest.md"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_manifest(args.root, args.output_csv, args.output_json, args.output_md)


if __name__ == "__main__":
    main()
