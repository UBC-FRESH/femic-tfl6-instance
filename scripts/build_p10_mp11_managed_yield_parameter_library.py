"""Build the P10.2 MP11 managed-yield parameter library."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import fitz
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_yield_parameter_library.md"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_yield_parameter_library.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_yield_parameter_library.json"

SOURCE_PACKAGE_ID = "tfl6_mp11_202606_public_pdf"
SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"

PDF_CANDIDATES = [
    INSTANCE_ROOT / "runtime" / "mp11" / "source" / "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf",
    INSTANCE_ROOT / "data" / "downloads" / "mp11" / "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf",
    INSTANCE_ROOT.parent / "figrecover" / "examples" / "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf",
]


@dataclass(frozen=True)
class ParameterRecord:
    record_id: str
    source_package_id: str
    source_sha256: str
    pdf_page: int
    info_package_page: str
    section: str
    source_table: str
    source_anchor: str
    parameter_family: str
    curve_lane: str
    au_scope: str
    species_or_zone: str
    parameter_name: str
    value: str
    unit: str
    dependency_status: str
    extraction_method: str
    review_status: str
    downstream_use: str
    model_input_status: str
    notes: str


def _find_pdf() -> Path:
    for candidate in PDF_CANDIDATES:
        if candidate.exists():
            return candidate
    searched = "\n".join(str(path) for path in PDF_CANDIDATES)
    raise FileNotFoundError(
        "Could not find the MP11 PDF. Place a verified public source copy in one "
        f"of these ignored paths:\n{searched}"
    )


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def _markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for _, row in df[columns].iterrows():
        values = []
        for column in columns:
            value = _clean(row[column]).replace("|", "\\|")
            values.append(value)
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def _table_rows(doc: fitz.Document, pdf_page: int) -> list[list[str]]:
    page = doc[pdf_page - 1]
    tables = page.find_tables().tables
    if not tables:
        return []
    table = tables[0]
    return [[_clean(cell) for cell in row] for row in table.extract()]


def _record(
    index: int,
    *,
    pdf_page: int,
    info_package_page: str,
    section: str,
    source_table: str,
    parameter_family: str,
    curve_lane: str,
    au_scope: str,
    species_or_zone: str,
    parameter_name: str,
    value: str,
    unit: str,
    dependency_status: str,
    extraction_method: str,
    review_status: str = "reviewed_parameter_candidate",
    downstream_use: str = "phase10_parameter_library_only",
    model_input_status: str = "not_model_input",
    notes: str = "",
) -> ParameterRecord:
    return ParameterRecord(
        record_id=f"p10_mp11_param_{index:03d}",
        source_package_id=SOURCE_PACKAGE_ID,
        source_sha256=SOURCE_SHA256,
        pdf_page=pdf_page,
        info_package_page=info_package_page,
        section=section,
        source_table=source_table,
        source_anchor=f"PDF page {pdf_page}; Appendix B page {info_package_page}; {source_table}",
        parameter_family=parameter_family,
        curve_lane=curve_lane,
        au_scope=au_scope,
        species_or_zone=species_or_zone,
        parameter_name=parameter_name,
        value=value,
        unit=unit,
        dependency_status=dependency_status,
        extraction_method=extraction_method,
        review_status=review_status,
        downstream_use=downstream_use,
        model_input_status=model_input_status,
        notes=notes,
    )


def build_records(doc: fitz.Document) -> list[ParameterRecord]:
    records: list[ParameterRecord] = []
    idx = 1

    def add(**kwargs: Any) -> None:
        nonlocal idx
        records.append(_record(idx, **kwargs))
        idx += 1

    add(
        pdf_page=358,
        info_package_page="112 of 183",
        section="8.2.4 Spacing; 8.2.5 Volumes for Early Managed Stands",
        source_table="Table 54",
        parameter_family="spacing_density",
        curve_lane="early_managed",
        au_scope="Early managed AUs with remaining juvenile spacing treatment areas",
        species_or_zone="all",
        parameter_name="juvenile_spacing_density_sequence",
        value="1600 to 900",
        unit="stems_per_ha",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review plus table-anchor extraction",
        notes=(
            "Spacing-marked early managed AUs use initial establishment density "
            "1600 sph followed by pre-commercial thinning to 900 sph."
        ),
    )
    add(
        pdf_page=358,
        info_package_page="112 of 183",
        section="8.2.5 Volumes for Early Managed Stands",
        source_table="Table 54",
        parameter_family="genetic_gain",
        curve_lane="early_managed",
        au_scope="Stands established 1961-2000; age 23-62 years",
        species_or_zone="all",
        parameter_name="genetic_gain_applied",
        value="0",
        unit="percent",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review plus table-anchor extraction",
        notes="Genetic gain is explicitly not applied to this age range.",
    )
    add(
        pdf_page=358,
        info_package_page="112 of 183",
        section="8.2.5 Volumes for Early Managed Stands",
        source_table="Table 54",
        parameter_family="per_au_tipsy_inputs",
        curve_lane="early_managed",
        au_scope="Early managed AU rows E100-E422",
        species_or_zone="mixed",
        parameter_name="large_table_row_parse_status",
        value="requires_p10_5_parser_review",
        unit="status",
        dependency_status="public_table_fragmented",
        extraction_method="PyMuPDF table detection smoke",
        review_status="parser_review_required",
        notes=(
            "Table 54 spans PDF pages 358-364. PyMuPDF detects table geometry, "
            "but multi-line species and SI cells require a dedicated row parser "
            "before managed-curve generation."
        ),
    )
    add(
        pdf_page=364,
        info_package_page="118 of 183",
        section="8.2.6 Volumes for Recent Managed Stands",
        source_table="Table 55",
        parameter_family="stocking_density",
        curve_lane="recent_managed",
        au_scope="Recently managed stands established 2001-2023; age 1-22 years",
        species_or_zone="all",
        parameter_name="typical_table_density",
        value="1000",
        unit="stems_per_ha",
        dependency_status="public_table_parameter",
        extraction_method="PyMuPDF text review plus table-anchor extraction",
        notes="The visible Table 55 rows use 1000 sph; row-level validation remains required.",
    )
    add(
        pdf_page=364,
        info_package_page="118 of 183",
        section="8.2.6 Volumes for Recent Managed Stands",
        source_table="Table 55",
        parameter_family="genetic_gain",
        curve_lane="recent_managed",
        au_scope="Recently managed stands established 2001-2023; age 1-22 years",
        species_or_zone="Cw/Fd/Hw/Yc",
        parameter_name="genetic_gain_source",
        value="seedlot averages since 2012",
        unit="source_description",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review plus table-anchor extraction",
        notes="Genetic gain values are based on seedlots planted in TFL 6 since 2012.",
    )
    add(
        pdf_page=365,
        info_package_page="119 of 183",
        section="8.2.6 Volumes for Recent Managed Stands",
        source_table="Table 55",
        parameter_family="per_au_tipsy_inputs",
        curve_lane="recent_managed",
        au_scope="Recent managed AU rows R100-R422",
        species_or_zone="mixed",
        parameter_name="large_table_row_parse_status",
        value="requires_p10_5_parser_review",
        unit="status",
        dependency_status="public_table_fragmented",
        extraction_method="PyMuPDF table detection smoke",
        review_status="parser_review_required",
        notes=(
            "Table 55 spans PDF pages 365-370. Extracted cell order is fragmented "
            "by line wrapping, so row-level parsing must be reviewed before use."
        ),
    )
    add(
        pdf_page=370,
        info_package_page="124 of 183",
        section="8.2.7 Future Stand Volumes",
        source_table="Narrative before Table 56",
        parameter_family="stocking_density",
        curve_lane="future_managed",
        au_scope="Most future AUs",
        species_or_zone="all",
        parameter_name="default_planting_density",
        value="1200",
        unit="stems_per_ha",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review",
        notes="Low-productivity exceptions are tracked separately.",
    )
    add(
        pdf_page=370,
        info_package_page="124 of 183",
        section="8.2.7 Future Stand Volumes",
        source_table="Narrative before Table 56",
        parameter_family="stocking_density",
        curve_lane="future_managed",
        au_scope="Low-productivity sites such as CWHvm1 33/33 and MHmmp22",
        species_or_zone="all",
        parameter_name="low_productivity_planting_density",
        value="800",
        unit="stems_per_ha",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review",
        notes="This is an explicit exception to the 1200 sph future-stand default.",
    )
    add(
        pdf_page=371,
        info_package_page="125 of 183",
        section="8.2.7.1 Regeneration Delay",
        source_table="Narrative before Table 56",
        parameter_family="regeneration_delay",
        curve_lane="future_managed",
        au_scope="Future managed planted stands",
        species_or_zone="all",
        parameter_name="tipsy_regeneration_delay",
        value="1",
        unit="year",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review",
        notes="One-year regeneration delay accounts for establishment processes beyond germination.",
    )

    table56_rows = _table_rows(doc, 371)
    table56_values = [
        ("Cw", "21.0"),
        ("Fd low elevation", "16.0"),
        ("Fd high elevation", "11.0"),
        ("Hw low elevation", "1.7"),
        ("Hw high elevation", "1.1"),
        ("Yc", "10.0"),
        ("Dr in CWHvm1", "32.0"),
    ]
    if len(table56_rows) < 8:
        raise RuntimeError("Table 56 extraction returned fewer rows than expected.")
    for species, value in table56_values:
        add(
            pdf_page=371,
            info_package_page="125 of 183",
            section="8.2.7.2 Genetic Gain",
            source_table="Table 56",
            parameter_family="genetic_gain",
            curve_lane="future_managed",
            au_scope="Future AUs",
            species_or_zone=species,
            parameter_name="future_au_genetic_gain",
            value=value,
            unit="percent",
            dependency_status="public_table_parameter",
            extraction_method="PyMuPDF table extraction with reviewed normalization",
            notes="Normalized from Table 56; footnoted restrictions remain in notes/source context.",
        )

    add(
        pdf_page=372,
        info_package_page="126 of 183",
        section="8.2.7.3 Yields",
        source_table="Table 57",
        parameter_family="site_index",
        curve_lane="future_managed",
        au_scope="Future AUs",
        species_or_zone="area_weighted_average",
        parameter_name="future_au_thlb_site_index",
        value="24.5",
        unit="metres",
        dependency_status="public_text_parameter",
        extraction_method="PyMuPDF text review plus table-anchor extraction",
        notes="Area-weighted average THLB site index for future AUs.",
    )
    add(
        pdf_page=372,
        info_package_page="126 of 183",
        section="8.2.7.3 Yields",
        source_table="Table 57",
        parameter_family="per_au_tipsy_inputs",
        curve_lane="future_managed",
        au_scope="Future AU rows Fvh101-Fvm2*",
        species_or_zone="mixed",
        parameter_name="large_table_row_parse_status",
        value="requires_p10_5_parser_review",
        unit="status",
        dependency_status="public_table_fragmented",
        extraction_method="PyMuPDF table detection smoke",
        review_status="parser_review_required",
        notes=(
            "Table 57 spans PDF pages 372-375. Extracted cells are line-wrapped "
            "and must be parsed/QAed before BatchTIPSY handoff."
        ),
    )

    vraf_zones = [
        ("Enhanced Windy", "15", "3.4", "30", "1.0"),
        ("Enhanced Basic", "15", "3.4", "50", "1.7"),
        ("General Windy", "20", "4.8", "40", "1.9"),
        ("General Basic", "20", "4.8", "60", "2.9"),
        ("Special", "25", "6.0", "90", "5.4"),
    ]
    for zone, retention, average_vraf, harvest_area, yield_impact in vraf_zones:
        add(
            pdf_page=376,
            info_package_page="130 of 183",
            section="8.2.8.2 Shading from Retained Trees",
            source_table="Table 58",
            parameter_family="vraf",
            curve_lane="recent_and_future_managed",
            au_scope="Western Stewardship and Conservation Plan zones",
            species_or_zone=zone,
            parameter_name="retention_level",
            value=retention,
            unit="percent",
            dependency_status="public_table_parameter",
            extraction_method="PyMuPDF table extraction with reviewed normalization",
            notes="Retention-zone VRAF parameter. Yield impact is separate and applied at harvest.",
        )
        add(
            pdf_page=376,
            info_package_page="130 of 183",
            section="8.2.8.2 Shading from Retained Trees",
            source_table="Table 58",
            parameter_family="vraf",
            curve_lane="recent_and_future_managed",
            au_scope="Western Stewardship and Conservation Plan zones",
            species_or_zone=zone,
            parameter_name="average_vraf",
            value=average_vraf,
            unit="percent",
            dependency_status="public_table_parameter",
            extraction_method="PyMuPDF table extraction with reviewed normalization",
            notes="Average VRAF from TIPSY scenario summaries.",
        )
        add(
            pdf_page=376,
            info_package_page="130 of 183",
            section="8.2.8.2 Shading from Retained Trees",
            source_table="Table 58",
            parameter_family="vraf",
            curve_lane="recent_and_future_managed",
            au_scope="Western Stewardship and Conservation Plan zones",
            species_or_zone=zone,
            parameter_name="percent_of_harvest_area",
            value=harvest_area,
            unit="percent",
            dependency_status="public_table_parameter",
            extraction_method="PyMuPDF table extraction with reviewed normalization",
            notes="Zone share used to derive average yield impact.",
        )
        add(
            pdf_page=377,
            info_package_page="131 of 183",
            section="8.2.8.2 Shading from Retained Trees",
            source_table="Table 58",
            parameter_family="vraf",
            curve_lane="recent_and_future_managed",
            au_scope="Western Stewardship and Conservation Plan zones",
            species_or_zone=zone,
            parameter_name="average_yield_impact_to_apply",
            value=yield_impact,
            unit="percent",
            dependency_status="public_table_parameter",
            extraction_method="PyMuPDF table extraction with reviewed normalization",
            notes="Applied when individual stands are harvested, not by altering base yield curves.",
        )

    add(
        pdf_page=377,
        info_package_page="131 of 183",
        section="8.2.9 Not Satisfactorily Restocked Areas",
        source_table="Table 59",
        parameter_family="nsr",
        curve_lane="future_managed",
        au_scope="NSR areas assigned to future AUs during initial planning period",
        species_or_zone="all",
        parameter_name="productive_area",
        value="1167",
        unit="ha",
        dependency_status="public_table_parameter",
        extraction_method="PyMuPDF table extraction with reviewed normalization",
        notes="NSR area is a model initialization/transition parameter, not a yield curve row.",
    )
    add(
        pdf_page=377,
        info_package_page="131 of 183",
        section="8.2.9 Not Satisfactorily Restocked Areas",
        source_table="Table 59",
        parameter_family="nsr",
        curve_lane="future_managed",
        au_scope="NSR areas assigned to future AUs during initial planning period",
        species_or_zone="all",
        parameter_name="thlb_area",
        value="1096",
        unit="ha",
        dependency_status="public_table_parameter",
        extraction_method="PyMuPDF table extraction with reviewed normalization",
        notes="NSR area is a model initialization/transition parameter, not a yield curve row.",
    )

    utilization_rows = [
        ("mature_gt_120", "minimum_dbh", "17.5", "cm"),
        ("mature_gt_120", "stump_height", "30.0", "cm"),
        ("mature_gt_120", "top_dib", "10.0", "cm"),
        ("mature_gt_120", "firmwood_standard", "50", "percent"),
        ("immature_le_120_and_future_managed", "minimum_dbh", "12.5", "cm"),
        ("immature_le_120_and_future_managed", "stump_height", "30.0", "cm"),
        ("immature_le_120_and_future_managed", "top_dib", "10.0", "cm"),
        ("immature_le_120_and_future_managed", "firmwood_standard", "50", "percent"),
    ]
    for age_class, parameter, value, unit in utilization_rows:
        add(
            pdf_page=377,
            info_package_page="131 of 183",
            section="8.3 Utilization Levels",
            source_table="Table 60",
            parameter_family="utilization",
            curve_lane="natural_and_managed",
            au_scope=age_class,
            species_or_zone="all",
            parameter_name=parameter,
            value=value,
            unit=unit,
            dependency_status="public_table_parameter",
            extraction_method="PyMuPDF table extraction with reviewed normalization",
            notes="Utilization parameter for later curve and model-input review.",
        )

    return records


def write_outputs(records: list[ParameterRecord], pdf_path: Path) -> None:
    rows = [asdict(record) for record in records]
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)

    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_pdf": str(pdf_path),
        "record_count": len(records),
        "parameter_family_counts": df["parameter_family"].value_counts().sort_index().to_dict(),
        "curve_lane_counts": df["curve_lane"].value_counts().sort_index().to_dict(),
        "dependency_status_counts": df["dependency_status"].value_counts().sort_index().to_dict(),
        "review_status_counts": df["review_status"].value_counts().sort_index().to_dict(),
        "model_input_status_counts": df["model_input_status"].value_counts().sort_index().to_dict(),
        "records": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# TFL 6 MP11 Managed-Yield Parameter Library",
        "",
        "## Purpose",
        "",
        "This P10.2 artifact converts reviewed MP11 growth-and-yield parameter",
        "evidence into a compact public-safe parameter library. It is a curve",
        "rebuild input surface only; it does not generate curves or promote any",
        "row to model-input status.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_managed_yield_parameter_library.md`",
        "- `planning/tfl6_mp11_managed_yield_parameter_library.csv`",
        "- `planning/tfl6_mp11_managed_yield_parameter_library.json`",
        "",
        "## Source Window",
        "",
        "- Source package: `tfl6_mp11_202606_public_pdf`",
        "- Source SHA256: "
        "`44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`",
        "- Relevant PDF pages: `358-377`",
        "- Relevant Appendix B pages: `112-131 of 183`",
        "- Primary tables: `54-60`",
        "",
        "## Status",
        "",
        f"- Parameter rows: `{len(df)}`",
        f"- Parameter families: `{df['parameter_family'].nunique()}`",
        f"- Curve lanes: `{df['curve_lane'].nunique()}`",
        "- Model-input status: `not_model_input`",
        "",
        "## Parameter Family Counts",
        "",
    ]
    for key, value in summary["parameter_family_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Review Status Counts", ""])
    for key, value in summary["review_status_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Key Use Boundary", ""])
    lines.extend(
        [
            "- Tables 54, 55, and 57 are anchored and represented, but their",
            "  multi-page per-AU TIPSY rows are marked",
            "  `requires_p10_5_parser_review` before managed-curve generation.",
            "- Table 56 genetic-gain, Table 58 VRAF, Table 59 NSR, and Table 60",
            "  utilization values are normalized into parameter rows.",
            "- VRAF rows are parameters for harvest-time yield impact review and",
            "  should not be hidden inside base managed yield curves.",
            "- All rows remain `not_model_input` until a later phase explicitly",
            "  promotes them through the Phase 8 evidence-promotion contract.",
            "",
            "## Parameter Rows",
            "",
        ]
    )
    display_cols = [
        "record_id",
        "source_table",
        "parameter_family",
        "curve_lane",
        "au_scope",
        "species_or_zone",
        "parameter_name",
        "value",
        "unit",
        "dependency_status",
        "review_status",
    ]
    lines.append(_markdown_table(df, display_cols))
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    pdf_path = _find_pdf()
    with fitz.open(pdf_path) as doc:
        records = build_records(doc)
    write_outputs(records, pdf_path)


if __name__ == "__main__":
    main()
