"""Build public-safe Phase 6 source and extraction-manifest records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SOURCE_URL = (
    "https://www.westernforest.com/wp-content/uploads/2026/06/"
    "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf"
)
EXPECTED_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"


@dataclass(frozen=True)
class DocumentComponent:
    """Contiguous PDF page range belonging to one MP11 package component."""

    component_id: str
    label: str
    pdf_page_start: int
    pdf_page_end: int
    report_page_start: str
    report_page_end: str
    extraction_role: str
    notes: str


@dataclass(frozen=True)
class ManifestField:
    """Required or recommended extraction-manifest field."""

    field_name: str
    required: bool
    value_type: str
    description: str
    example: str


DOCUMENT_COMPONENTS = [
    DocumentComponent(
        component_id="management_plan_main",
        label="Management Plan 11 main document",
        pdf_page_start=1,
        pdf_page_end=44,
        report_page_start="i",
        report_page_end="33 of 37",
        extraction_role="front_matter_governance_context",
        notes="Includes MP purpose, AAC history, public review, appendices listing, and governance context.",
    ),
    DocumentComponent(
        component_id="appendix_a_divider",
        label="Appendix A divider page",
        pdf_page_start=45,
        pdf_page_end=45,
        report_page_start="34 of 37",
        report_page_end="34 of 37",
        extraction_role="component_boundary",
        notes="Management Plan divider page identifying Appendix A as the Timber Supply Analysis Report.",
    ),
    DocumentComponent(
        component_id="appendix_a_timber_supply_analysis",
        label="Appendix A Timber Supply Analysis",
        pdf_page_start=46,
        pdf_page_end=226,
        report_page_start="i",
        report_page_end="113 of 113",
        extraction_role="primary_mp11_analysis_source",
        notes="Primary source for land-base, THLB, sensitivity, model-behavior, and AAC-recommendation evidence.",
    ),
    DocumentComponent(
        component_id="appendix_a_trailing_blank",
        label="Appendix A trailing blank page",
        pdf_page_start=227,
        pdf_page_end=227,
        report_page_start="35 of 37",
        report_page_end="35 of 37",
        extraction_role="blank_component_boundary",
        notes="Blank management-plan page between Appendix A and Appendix B divider.",
    ),
    DocumentComponent(
        component_id="appendix_b_divider",
        label="Appendix B divider page",
        pdf_page_start=228,
        pdf_page_end=228,
        report_page_start="36 of 37",
        report_page_end="36 of 37",
        extraction_role="component_boundary",
        notes="Management Plan divider page identifying Appendix B as the Timber Supply Analysis Information Package.",
    ),
    DocumentComponent(
        component_id="appendix_b_acceptance_letter",
        label="Appendix B acceptance letter",
        pdf_page_start=229,
        pdf_page_end=229,
        report_page_start="letter",
        report_page_end="letter",
        extraction_role="information_package_acceptance_context",
        notes="Ministry acceptance correspondence preceding the information package.",
    ),
    DocumentComponent(
        component_id="appendix_b_information_package",
        label="Appendix B Timber Supply Analysis Information Package",
        pdf_page_start=230,
        pdf_page_end=475,
        report_page_start="i",
        report_page_end="37 of 37",
        extraction_role="assumption_and_input_package_source",
        notes="Source for timber-supply inputs, assumptions, inventory, land base, yield, and nested appendix evidence.",
    ),
]


MANIFEST_FIELDS = [
    ManifestField("record_id", True, "string", "Stable unique extraction row identifier.", "mp11-table-001"),
    ManifestField("source_package_id", True, "string", "Source package identifier.", "tfl6_mp11_202606_public_pdf"),
    ManifestField("source_sha256", True, "string", "SHA256 of the public PDF used for extraction.", EXPECTED_SHA256),
    ManifestField("document_component", True, "string", "Component ID from the source manifest.", "appendix_a_timber_supply_analysis"),
    ManifestField("pdf_page", True, "integer", "One-based PDF page number.", "82"),
    ManifestField("reported_page_label", False, "string", "Visible report page label where available.", "Page 18 of 113"),
    ManifestField("section_path", True, "string", "Hierarchical section heading path.", "3 Base Case > 3.1 Base Case Harvest Forecast"),
    ManifestField("object_type", True, "enum", "Extracted object class.", "table|figure|paragraph|heading|assumption|reference"),
    ManifestField("object_id", False, "string", "Table, figure, section, or assumption identifier.", "Figure 2"),
    ManifestField("object_title", False, "string", "Caption, table title, or normalized heading.", "Base Case Harvest Level"),
    ManifestField("claim_text", True, "string", "Verbatim or tightly paraphrased extracted claim.", "Base-case harvest level is approximately 1,061,600 m3/year."),
    ManifestField("normalized_value", False, "string|number", "Normalized structured value when available.", "1061600"),
    ManifestField("units", False, "string", "Units for normalized value.", "m3/year"),
    ManifestField("comparison_topic", True, "enum", "Phase 6 comparison lane.", "land_base|inventory_yield|model_behavior|aac|metadata"),
    ManifestField("extraction_method", True, "string", "Tool or method used to create the row.", "PyMuPDF text extraction"),
    ManifestField("tool_versions", True, "object", "Relevant parser/package versions.", '{"pymupdf": "1.27.2.3"}'),
    ManifestField("source_artifact", False, "string", "Ignored runtime artifact path if one exists.", "runtime/mp11/pages/page-0082.png"),
    ManifestField("review_status", True, "enum", "Review state for use in downstream planning.", "raw_extraction|reviewed_evidence|accepted_contract|rejected|deferred"),
    ManifestField("downstream_use", True, "string", "Permitted downstream use of this row.", "phase6_comparison_only"),
    ManifestField("model_input_status", True, "enum", "Whether row may enter model inputs.", "not_model_input"),
    ManifestField("reviewer", False, "string", "Reviewer identity or role after review.", "maintainer"),
    ManifestField("reviewed_at_utc", False, "datetime", "UTC timestamp for reviewed rows.", "2026-06-28T00:00:00Z"),
    ManifestField("notes", False, "string", "Important caveats, failures, or unresolved questions.", "Requires table cross-check."),
]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inspect_pdf(path: Path) -> dict[str, Any]:
    import fitz

    doc = fitz.open(path)
    return {
        "byte_size": path.stat().st_size,
        "sha256": _sha256(path),
        "page_count": doc.page_count,
        "format": doc.metadata.get("format", ""),
        "producer": doc.metadata.get("producer", ""),
        "mod_date": doc.metadata.get("modDate", ""),
        "encrypted": bool(doc.needs_pass),
        "pymupdf_version": fitz.version[0],
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_manifest(
    source_pdf: Path,
    output_json: Path,
    output_md: Path,
    component_csv: Path,
    field_csv: Path,
    accessed_at_utc: str,
) -> dict[str, Any]:
    inspection = _inspect_pdf(source_pdf)
    checksum_status = "passed" if inspection["sha256"] == EXPECTED_SHA256 else "failed"
    component_rows = [asdict(row) for row in DOCUMENT_COMPONENTS]
    field_rows = [asdict(row) for row in MANIFEST_FIELDS]
    manifest = {
        "source_package_id": "tfl6_mp11_202606_public_pdf",
        "source_url": SOURCE_URL,
        "accessed_at_utc": accessed_at_utc,
        "local_source_copy_policy": {
            "tracked_in_git": False,
            "allowed_locations": [
                "runtime/mp11/source/",
                "data/downloads/mp11/",
                "external public-data cache with matching SHA256",
            ],
            "required_before_extraction": "verify URL, byte size, page count, and SHA256",
        },
        "document_identity": {
            "title": "Tree Farm Licence 6 Management Plan 11",
            "version": "Version 1, June 2026",
            "publisher": "Western Forest Products Inc.",
            "document_date": "June 2026",
            "governance_caveat": (
                "Treat as a public planning and AAC-analysis package. Do not treat "
                "the AAC analysis as a final Chief Forester AAC decision unless a "
                "separate approved decision is located and reviewed."
            ),
        },
        "inspection": inspection,
        "expected_sha256": EXPECTED_SHA256,
        "checksum_status": checksum_status,
        "document_components": component_rows,
        "extraction_manifest_fields": field_rows,
        "phase6_non_goals": [
            "do not change accepted model inputs",
            "do not rerun THLB",
            "do not regenerate yield curves",
            "do not regenerate ForestModel XML or Matrix Builder outputs",
            "do not republish the Phase 5 runtime package",
        ],
    }
    output_json.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    _write_csv(component_csv, component_rows, list(component_rows[0]))
    _write_csv(field_csv, field_rows, list(field_rows[0]))
    _write_markdown(output_md, manifest, component_csv, field_csv)
    return manifest


def _write_markdown(path: Path, manifest: dict[str, Any], component_csv: Path, field_csv: Path) -> None:
    inspection = manifest["inspection"]
    components = manifest["document_components"]
    fields = manifest["extraction_manifest_fields"]
    lines = [
        "# TFL 6 MP11 Source Package Manifest",
        "",
        "## Purpose",
        "",
        "This P6.1 note records the public source identity, local source-copy",
        "convention, document-component ranges, and extraction-manifest contract",
        "for the TFL 6 Management Plan 11 package. It is a provenance surface, not",
        "a model-input change.",
        "",
        "## Source Identity",
        "",
        f"- Source package ID: `{manifest['source_package_id']}`",
        f"- Source URL: `{manifest['source_url']}`",
        f"- Accessed at UTC: `{manifest['accessed_at_utc']}`",
        "- Document title: `Tree Farm Licence 6 Management Plan 11`",
        "- Version/date: `Version 1, June 2026`",
        "- Publisher: `Western Forest Products Inc.`",
        f"- Byte size: `{inspection['byte_size']}`",
        f"- Page count: `{inspection['page_count']}`",
        f"- SHA256: `{inspection['sha256']}`",
        f"- Expected SHA256: `{manifest['expected_sha256']}`",
        f"- Checksum status: `{manifest['checksum_status']}`",
        f"- PDF format: `{inspection['format']}`",
        f"- Producer: `{inspection['producer']}`",
        f"- Modification date: `{inspection['mod_date']}`",
        f"- PyMuPDF version used for inspection: `{inspection['pymupdf_version']}`",
        "",
        "## Governance Caveat",
        "",
        manifest["document_identity"]["governance_caveat"],
        "",
        "## Local Source-Copy Policy",
        "",
        "The PDF is not tracked in this repository. A local source copy may live in",
        "ignored runtime/download/cache space only after URL, byte size, page count,",
        "and SHA256 are verified.",
        "",
        "Accepted ignored locations:",
        "",
    ]
    for location in manifest["local_source_copy_policy"]["allowed_locations"]:
        lines.append(f"- `{location}`")
    lines.extend(
        [
            "",
            "## Document Components",
            "",
            f"Machine-readable component table: `{component_csv.as_posix()}`",
            "",
            "| Component | PDF pages | Role | Notes |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for row in components:
        lines.append(
            f"| `{row['component_id']}` | `{row['pdf_page_start']}-{row['pdf_page_end']}` | "
            f"`{row['extraction_role']}` | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Extraction-Manifest Contract",
            "",
            f"Machine-readable field table: `{field_csv.as_posix()}`",
            "",
            "Every P6.2+ extracted claim must preserve page/component provenance,",
            "method/tool provenance, review status, downstream-use classification,",
            "and model-input status. Raw extracted values must remain separate from",
            "reviewed evidence and accepted model contracts.",
            "",
            "Required fields:",
            "",
        ]
    )
    for field in fields:
        if field["required"]:
            lines.append(f"- `{field['field_name']}`: {field['description']}")
    lines.extend(
        [
            "",
            "## Phase 6 Non-Goals",
            "",
        ]
    )
    for non_goal in manifest["phase6_non_goals"]:
        lines.append(f"- {non_goal};")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_pdf", type=Path)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_source_package_manifest.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_source_package_manifest.md"),
    )
    parser.add_argument(
        "--component-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_document_components.csv"),
    )
    parser.add_argument(
        "--field-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_extraction_manifest_fields.csv"),
    )
    parser.add_argument(
        "--accessed-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()
    manifest = build_manifest(
        source_pdf=args.source_pdf,
        output_json=args.output_json,
        output_md=args.output_md,
        component_csv=args.component_csv,
        field_csv=args.field_csv,
        accessed_at_utc=args.accessed_at_utc,
    )
    print(args.output_md)
    print(args.output_json)
    print(args.component_csv)
    print(args.field_csv)
    print(manifest["checksum_status"])


if __name__ == "__main__":
    main()
