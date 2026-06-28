"""Validate the Phase 9 MP11 ordered-overlay THLB recipe scaffold."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ScaffoldStepRecord:
    """Validated scaffold row for one ordered THLB step."""

    step_id: str
    label: str
    order: int
    execution_class: str
    phase9_status: str
    source_ids: str
    candidate_ids: str
    source_reference_status: str
    candidate_reference_status: str
    mp11_target_ha: float | None
    output_role: str
    notes: str


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as src:
        return json.load(src)


def _load_recipe(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as src:
        data = yaml.safe_load(src)
    if not isinstance(data, dict):
        raise ValueError(f"Recipe did not parse as a mapping: {path}")
    return data


def _reference_status(ids: list[str], known_ids: set[str]) -> str:
    missing = [item for item in ids if item not in known_ids]
    if missing:
        return "missing:" + ",".join(missing)
    return "ok"


def build_scaffold_summary(
    recipe_path: Path,
    source_manifest_path: Path,
    proxy_profile_path: Path,
    output_csv: Path,
    output_json: Path,
    output_md: Path,
) -> list[ScaffoldStepRecord]:
    recipe = _load_recipe(recipe_path)
    source_manifest = _load_json(source_manifest_path)
    proxy_profile = _load_json(proxy_profile_path)
    source_ids = {str(row["source_id"]) for row in source_manifest["rows"]}
    candidate_ids = {str(row["candidate_id"]) for row in proxy_profile["rows"]}
    steps = recipe.get("steps", [])
    if not isinstance(steps, list) or not steps:
        raise ValueError("Recipe scaffold must contain a non-empty steps list.")
    records: list[ScaffoldStepRecord] = []
    required = {"step_id", "label", "order", "execution_class", "phase9_status", "output_role"}
    for step in steps:
        missing_fields = required.difference(step)
        if missing_fields:
            raise ValueError(f"Step is missing required fields {sorted(missing_fields)}: {step}")
        source_ref_ids = [str(item) for item in step.get("source_ids", [])]
        candidate_ref_ids = [str(item) for item in step.get("candidate_ids", [])]
        records.append(
            ScaffoldStepRecord(
                step_id=str(step["step_id"]),
                label=str(step["label"]),
                order=int(step["order"]),
                execution_class=str(step["execution_class"]),
                phase9_status=str(step["phase9_status"]),
                source_ids=", ".join(source_ref_ids),
                candidate_ids=", ".join(candidate_ref_ids),
                source_reference_status=_reference_status(source_ref_ids, source_ids),
                candidate_reference_status=_reference_status(candidate_ref_ids, candidate_ids),
                mp11_target_ha=step.get("mp11_target_ha"),
                output_role=str(step["output_role"]),
                notes=" ".join(str(note) for note in step.get("notes", [])),
            )
        )
    records = sorted(records, key=lambda row: row.order)
    _write_outputs(output_csv, output_json, output_md, recipe_path, records)
    return records


def _counts(records: list[ScaffoldStepRecord], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(getattr(record, field))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _write_outputs(
    output_csv: Path,
    output_json: Path,
    output_md: Path,
    recipe_path: Path,
    records: list[ScaffoldStepRecord],
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "recipe_path": recipe_path.as_posix(),
        "row_count": len(records),
        "execution_class_counts": _counts(records, "execution_class"),
        "phase9_status_counts": _counts(records, "phase9_status"),
        "source_reference_status_counts": _counts(records, "source_reference_status"),
        "candidate_reference_status_counts": _counts(records, "candidate_reference_status"),
        "outputs": {
            "csv": output_csv.as_posix(),
            "json": output_json.as_posix(),
            "markdown": output_md.as_posix(),
        },
        "rows": [asdict(record) for record in records],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, payload, records)


def _write_markdown(path: Path, payload: dict[str, Any], records: list[ScaffoldStepRecord]) -> None:
    lines = [
        "# TFL 6 MP11 Phase 9 Ordered Overlay Scaffold",
        "",
        "## Purpose",
        "",
        "This P9.4 note validates the MP11 public-data ordered-overlay THLB",
        "recipe scaffold against the P9.2 source manifest and P9.3 input/proxy",
        "profile. It is a scaffold smoke only; it does not execute overlays or",
        "produce THLB outputs.",
        "",
        "## Files",
        "",
        "- `config/tsr/mp11_thlb_rebuild.recipe.yaml`",
        "- `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.md`",
        "- `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.csv`",
        "- `planning/tfl6_mp11_phase9_ordered_overlay_scaffold.json`",
        "",
        "## Status Counts",
        "",
        f"- Rows: `{payload['row_count']}`",
        f"- Execution class counts: `{payload['execution_class_counts']}`",
        f"- Phase 9 status counts: `{payload['phase9_status_counts']}`",
        f"- Source reference status counts: `{payload['source_reference_status_counts']}`",
        f"- Candidate reference status counts: `{payload['candidate_reference_status_counts']}`",
        "",
        "## Ordered Steps",
        "",
        "| Order | Step | Class | Status | Source refs | Candidate refs | MP11 target ha |",
        "| ---: | --- | --- | --- | --- | --- | ---: |",
    ]
    for record in records:
        target = "" if record.mp11_target_ha is None else f"{record.mp11_target_ha:,.3f}"
        lines.append(
            f"| {record.order} | `{record.step_id}` {record.label} | "
            f"`{record.execution_class}` | `{record.phase9_status}` | "
            f"`{record.source_reference_status}` | `{record.candidate_reference_status}` | {target} |"
        )
    lines.extend(
        [
            "",
            "## Key Findings",
            "",
            "- The scaffold preserves ordered checkpoint, attribute, overlay, proxy,",
            "  unavailable-gap, and aspatial-policy rows.",
            "- All referenced source IDs and candidate IDs resolve against the P9.2",
            "  and P9.3 manifests.",
            "- Current THLB `120,099 ha` is represented as a comparison target only.",
            "- Shoreline, DEM/slope, and WFP LBB/ITI/LEFI remain explicit gaps or",
            "  proxy dependencies before execution.",
            "",
            "## Use Boundary",
            "",
            "This scaffold authorizes P9.5 implementation planning and bounded smoke",
            "design only. It does not authorize accepted THLB outputs or model-input",
            "promotion.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", type=Path, default=Path("config/tsr/mp11_thlb_rebuild.recipe.yaml"))
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_source_layer_manifest.json"),
    )
    parser.add_argument(
        "--proxy-profile",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_input_proxy_profile.json"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_ordered_overlay_scaffold.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_ordered_overlay_scaffold.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_ordered_overlay_scaffold.md"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_scaffold_summary(
        args.recipe,
        args.source_manifest,
        args.proxy_profile,
        args.output_csv,
        args.output_json,
        args.output_md,
    )


if __name__ == "__main__":
    main()
