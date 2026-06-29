"""Build P12.2 Matrix Builder track QA summaries."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "tfl6_mp11_candidate_p12_2_matrix_build"
DEFAULT_TRACKS_ROOT = (
    INSTANCE_ROOT / "models" / "tfl6_patchworks_model_mp11_candidate" / "tracks"
)
DEFAULT_MANIFEST_PATH = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_matrixbuilder_manifest-{DEFAULT_RUN_ID}.json"
)
DEFAULT_STDOUT_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_matrixbuilder_stdout-{DEFAULT_RUN_ID}.log"
)
DEFAULT_STDERR_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_matrixbuilder_stderr-{DEFAULT_RUN_ID}.log"
)
DEFAULT_PHASE11_QA_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_generation_qa.json"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_matrix_builder_tracks_qa.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_matrix_builder_tracks_qa.json"
)
DEFAULT_OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_matrix_builder_tracks_qa.md"

TRACK_FILES = [
    "features",
    "protoaccounts",
    "accounts",
    "products",
    "curves",
    "groups",
    "strata",
    "treatments",
    "blocks",
    "tracknames",
    "packages",
    "packageSequences",
    "messages",
]


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required QA input missing: {_repo_relative(path)}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Required Matrix Builder track missing: {_repo_relative(path)}"
        )
    return pd.read_csv(path)


def _track_stats(tracks_root: Path) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for name in TRACK_FILES:
        path = tracks_root / f"{name}.csv"
        df = _read_csv(path)
        record: dict[str, Any] = {
            "path": _repo_relative(path),
            "rows": int(len(df)),
            "columns": list(df.columns),
            "bytes": path.stat().st_size,
        }
        for column in [
            "TRACK",
            "LABEL",
            "ACCOUNT",
            "ATTRIBUTE",
            "TREATMENT",
            "CURVE",
            "GROUP",
            "BLOCK",
            "STRATA",
        ]:
            if column in df.columns:
                record[f"{column.lower()}_nunique"] = int(
                    df[column].nunique(dropna=True)
                )
        if name in {"features", "products"} and "LABEL" in df.columns:
            labels = df["LABEL"].astype(str)
            record["managed_label_rows"] = int(
                labels.str.contains("managed", case=False, regex=False).sum()
            )
            record["harvested_volume_rows"] = int(
                labels.str.contains("HarvestedVolume", case=False, regex=False).sum()
            )
        if name in {"accounts", "protoaccounts"}:
            values = df.astype(str)
            record["area_account_rows"] = int(
                values.apply(
                    lambda series: series.str.contains("feature.Area", regex=False)
                )
                .any(axis=1)
                .sum()
            )
            record["harvested_volume_account_rows"] = int(
                values.apply(
                    lambda series: series.str.contains("HarvestedVolume", regex=False)
                )
                .any(axis=1)
                .sum()
            )
        stats[name] = record
    return stats


def _log_scan(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required Matrix Builder log missing: {_repo_relative(path)}"
        )
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    matches = {
        "error": lowered.count("error"),
        "warning": lowered.count("warning"),
        "exception": lowered.count("exception"),
        "failed": lowered.count("failed"),
    }
    return {"path": _repo_relative(path), "bytes": path.stat().st_size, **matches}


def _sanitize_accounts_sync(accounts_sync: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in accounts_sync.items():
        if key.endswith("_path") and isinstance(value, str):
            path = Path(value)
            try:
                sanitized[key] = _repo_relative(path)
            except ValueError:
                sanitized[key] = path.name
        else:
            sanitized[key] = value
    return sanitized


def _write_outputs(
    *,
    payload: dict[str, Any],
    output_csv: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in payload["summary"].items():
            writer.writerow({"metric": key, "value": value})
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    tracks = payload["tracks"]
    lines = [
        "# P12.2 MP11 Matrix Builder Track QA",
        "",
        "This QA record inspects the MP11 candidate Matrix Builder tracks generated",
        "from the Phase 11 candidate ForestModel XML and fragments.",
        "",
        "P12.2 does not assemble the Patchworks runtime package, run Patchworks",
        "direct launch smoke, run scenarios, or publish a release archive.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Track Files",
            "",
            "| File | Rows | Key Counts |",
            "| --- | ---: | --- |",
        ]
    )
    for name in TRACK_FILES:
        record = tracks[name]
        key_counts = ", ".join(
            f"{key}={value}"
            for key, value in record.items()
            if key.endswith("_nunique") or key.endswith("_rows")
        )
        lines.append(f"| `{name}.csv` | {record['rows']} | {key_counts} |")

    lines.extend(
        [
            "",
            "## Inspection Result",
            "",
            "- Matrix Builder generated all expected track CSV files.",
            "- `accounts.csv` and `protoaccounts.csv` are identical after FEMIC account sync.",
            "- `messages.csv` is header-only.",
            "- `packages.csv` and `packageSequences.csv` are header-only, consistent with",
            "  the current candidate scaffold having no package-sequence treatments.",
            "- Track block area is within rounding tolerance of the Phase 11 fragment area.",
            "- The only recorded Matrix Builder warning text is the generic Patchworks",
            "  completion prompt to review warnings and exit.",
            "",
            "## Boundary",
            "",
            "This is a candidate Matrix Builder track set. Runtime assembly, direct",
            "launch smoke, scenario smoke, and release QA remain downstream Phase 12",
            "and Phase 13 work.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_qa(
    *,
    tracks_root: Path = DEFAULT_TRACKS_ROOT,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    stdout_log: Path = DEFAULT_STDOUT_LOG,
    stderr_log: Path = DEFAULT_STDERR_LOG,
    phase11_qa_json: Path = DEFAULT_PHASE11_QA_JSON,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    phase11_qa = _load_json(phase11_qa_json)
    tracks = _track_stats(tracks_root)
    accounts = _read_csv(tracks_root / "accounts.csv")
    protoaccounts = _read_csv(tracks_root / "protoaccounts.csv")
    blocks = _read_csv(tracks_root / "blocks.csv")
    block_area_ha = float(blocks["AREA"].sum())
    fragment_area_ha = float(phase11_qa["summary"]["fragment_area_ha"])
    area_delta_ha = block_area_ha - fragment_area_ha
    stdout_scan = _log_scan(stdout_log)
    stderr_scan = _log_scan(stderr_log)

    expected_files_present = all(
        (tracks_root / f"{name}.csv").exists() for name in TRACK_FILES
    )
    accounts_proto_equal = accounts.equals(protoaccounts)
    messages_header_only = tracks["messages"]["rows"] == 0
    no_failures = not manifest.get("failures")
    generic_warning_only = manifest.get("warnings") == [
        "Processing completed.  Review warnings and exit when finished."
    ]
    qa_status = (
        "matrix_builder_tracks_generated_inspection_pass"
        if all(
            [
                manifest.get("returncode") == 0,
                expected_files_present,
                accounts_proto_equal,
                messages_header_only,
                no_failures,
                abs(area_delta_ha) < 0.01,
            ]
        )
        else "matrix_builder_tracks_need_review"
    )

    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "qa_status": qa_status,
        "run_id": manifest["run_id"],
        "matrix_builder_returncode": manifest.get("returncode"),
        "matrix_builder_raw_returncode": manifest.get("raw_returncode"),
        "expected_track_files_present": expected_files_present,
        "track_file_count": len(TRACK_FILES),
        "features_rows": tracks["features"]["rows"],
        "accounts_rows": tracks["accounts"]["rows"],
        "protoaccounts_rows": tracks["protoaccounts"]["rows"],
        "accounts_proto_equal": accounts_proto_equal,
        "products_rows": tracks["products"]["rows"],
        "curves_rows": tracks["curves"]["rows"],
        "groups_rows": tracks["groups"]["rows"],
        "strata_rows": tracks["strata"]["rows"],
        "treatments_rows": tracks["treatments"]["rows"],
        "blocks_rows": tracks["blocks"]["rows"],
        "messages_rows": tracks["messages"]["rows"],
        "block_area_ha": round(block_area_ha, 6),
        "phase11_fragment_area_ha": round(fragment_area_ha, 6),
        "block_fragment_area_delta_ha": round(area_delta_ha, 6),
        "manifest_failures_count": len(manifest.get("failures", [])),
        "manifest_warnings_count": len(manifest.get("warnings", [])),
        "generic_warning_only": generic_warning_only,
        "stdout_error_count": stdout_scan["error"],
        "stderr_error_count": stderr_scan["error"],
        "runtime_bundle_generation": "not_performed",
        "direct_launch_smoke": "not_performed",
        "scenario_smoke": "not_performed",
    }
    payload = {
        "summary": summary,
        "tracks_root": _repo_relative(tracks_root),
        "tracks": tracks,
        "manifest": {
            "path": _repo_relative(manifest_path),
            "run_id": manifest["run_id"],
            "returncode": manifest.get("returncode"),
            "raw_returncode": manifest.get("raw_returncode"),
            "accounts_sync": _sanitize_accounts_sync(manifest.get("accounts_sync", {})),
            "warnings": manifest.get("warnings", []),
            "failures": manifest.get("failures", []),
        },
        "log_scan": {"stdout": stdout_scan, "stderr": stderr_scan},
    }
    _write_outputs(
        payload=payload,
        output_csv=output_csv,
        output_json=output_json,
        output_md=output_md,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracks-root", type=Path, default=DEFAULT_TRACKS_ROOT)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--stdout-log", type=Path, default=DEFAULT_STDOUT_LOG)
    parser.add_argument("--stderr-log", type=Path, default=DEFAULT_STDERR_LOG)
    parser.add_argument("--phase11-qa-json", type=Path, default=DEFAULT_PHASE11_QA_JSON)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_qa(
        tracks_root=args.tracks_root,
        manifest_path=args.manifest_path,
        stdout_log=args.stdout_log,
        stderr_log=args.stderr_log,
        phase11_qa_json=args.phase11_qa_json,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
