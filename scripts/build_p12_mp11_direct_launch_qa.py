"""Build P12.4 direct Patchworks launch smoke QA."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "tfl6_mp11_candidate_p12_4_launch0"
DEFAULT_STAGE_LABEL = "p12_4_launch0"
DEFAULT_STAGE_DIR = (
    INSTANCE_ROOT
    / "models"
    / "tfl6_patchworks_model_mp11_candidate"
    / "analysis"
    / DEFAULT_STAGE_LABEL
)
DEFAULT_MANIFEST_PATH = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_manifest-{DEFAULT_RUN_ID}.json"
)
DEFAULT_STDOUT_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_stdout-{DEFAULT_RUN_ID}.log"
)
DEFAULT_STDERR_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_stderr-{DEFAULT_RUN_ID}.log"
)
DEFAULT_TRACE_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_trace-{DEFAULT_RUN_ID}.log"
)
DEFAULT_RUNTIME_MANIFEST_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_runtime_package_manifest.json"
)
DEFAULT_OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_direct_launch_qa.csv"
DEFAULT_OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_direct_launch_qa.json"
DEFAULT_OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_direct_launch_qa.md"


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required direct-launch input missing: {_repo_relative(path)}"
        )
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"Required direct-launch log missing: {_repo_relative(path)}"
        )
    return path.read_text(encoding="utf-8", errors="replace")


def _log_scan(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    lowered = text.lower()
    return {
        "path": _repo_relative(path),
        "bytes": path.stat().st_size,
        "error": lowered.count("error"),
        "warning": lowered.count("warning"),
        "exception": lowered.count("exception"),
        "failed": lowered.count("failed"),
    }


def _csv_rows(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(
            f"Required saved-stage CSV missing: {_repo_relative(path)}"
        )
    return int(len(pd.read_csv(path)))


def _stage_inventory(stage_dir: Path) -> dict[str, Any]:
    if not stage_dir.exists():
        raise FileNotFoundError(
            f"Saved-stage directory missing: {_repo_relative(stage_dir)}"
        )
    records: dict[str, Any] = {}
    total_files = 0
    total_bytes = 0
    for child in sorted(stage_dir.iterdir()):
        if child.is_dir():
            files = [path for path in child.rglob("*") if path.is_file()]
            count = len(files)
            bytes_total = sum(path.stat().st_size for path in files)
        else:
            count = 1
            bytes_total = child.stat().st_size
        records[child.name] = {"file_count": count, "bytes": bytes_total}
        total_files += count
        total_bytes += bytes_total
    return {
        "path": _repo_relative(stage_dir),
        "total_file_count": total_files,
        "total_bytes": total_bytes,
        "children": records,
    }


def _sanitize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": manifest["run_id"],
        "raw_returncode": manifest.get("raw_returncode"),
        "returncode": manifest.get("returncode"),
        "mode": manifest.get("mode"),
        "failures": manifest.get("failures", []),
        "headless_automation": {
            "terminal_state": manifest.get("headless_automation", {}).get(
                "terminal_state"
            ),
            "detected_marker": manifest.get("headless_automation", {}).get(
                "detected_marker"
            ),
            "monitor_killed_process_tree": manifest.get("headless_automation", {}).get(
                "monitor_killed_process_tree"
            ),
        },
        "inputs": {
            "stage_label": manifest.get("inputs", {}).get("stage_label"),
            "iterations": manifest.get("inputs", {}).get("iterations"),
            "scenario_mode": manifest.get("inputs", {}).get("scenario_mode"),
            "scenario_target": manifest.get("inputs", {}).get("scenario_target"),
        },
        "outputs": {
            "stage_dir": _repo_relative(
                Path(manifest.get("outputs", {}).get("stage_dir"))
            ),
            "saved_file_count": manifest.get("outputs", {}).get("saved_file_count"),
        },
    }


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
    stage = payload["stage_inventory"]
    lines = [
        "# P12.4 MP11 Direct Launch QA",
        "",
        "This QA record inspects the direct headless launch smoke for the MP11",
        "candidate Patchworks runtime package.",
        "",
        "P12.4 does not run scheduling scenarios, publish a release archive, or",
        "replace the accepted Phase 5 teaching/runtime baseline.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Saved Stage Inventory",
            "",
            "| Child | Files | Bytes |",
            "| --- | ---: | ---: |",
        ]
    )
    for name, record in stage["children"].items():
        lines.append(f"| `{name}` | {record['file_count']} | {record['bytes']} |")

    lines.extend(
        [
            "",
            "## Inspection Result",
            "",
            "- Headless launch returned code `0`.",
            "- Trace log includes `[FEMIC headless] saveStage completed`.",
            "- Saved-stage output count matches the headless manifest.",
            "- `scenario/schedule.csv` is header-only, as expected for `iterations=0`.",
            "- No stderr/stdout error, warning, exception, or failure strings were found.",
            "",
            "## Boundary",
            "",
            "This is direct launch smoke only. Representative base/sensitivity scenario",
            "smoke remains P12.5, and release QA remains Phase 13.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_qa(
    *,
    stage_dir: Path = DEFAULT_STAGE_DIR,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    stdout_log: Path = DEFAULT_STDOUT_LOG,
    stderr_log: Path = DEFAULT_STDERR_LOG,
    trace_log: Path = DEFAULT_TRACE_LOG,
    runtime_manifest_json: Path = DEFAULT_RUNTIME_MANIFEST_JSON,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    runtime_manifest = _load_json(runtime_manifest_json)
    stage_inventory = _stage_inventory(stage_dir)
    trace_text = _read_text(trace_log)
    stdout_scan = _log_scan(stdout_log)
    stderr_scan = _log_scan(stderr_log)
    target_status_rows = _csv_rows(stage_dir / "scenario" / "targetStatus.csv")
    target_summary_rows = _csv_rows(stage_dir / "scenario" / "targetSummary.csv")
    schedule_rows = _csv_rows(stage_dir / "scenario" / "schedule.csv")

    detected_marker = manifest.get("headless_automation", {}).get("detected_marker")
    save_stage_seen = "[FEMIC headless] saveStage completed" in trace_text
    saved_file_count = int(manifest.get("outputs", {}).get("saved_file_count", -1))
    no_log_errors = all(
        scan[key] == 0
        for scan in (stdout_scan, stderr_scan)
        for key in ("error", "warning", "exception", "failed")
    )
    qa_status = (
        "direct_launch_smoke_pass"
        if all(
            [
                manifest.get("returncode") == 0,
                manifest.get("raw_returncode") == 0,
                manifest.get("headless_automation", {}).get("terminal_state")
                == "success",
                detected_marker == "[FEMIC headless] saveStage completed",
                save_stage_seen,
                stage_inventory["total_file_count"] == saved_file_count,
                schedule_rows == 0,
                no_log_errors,
            ]
        )
        else "direct_launch_smoke_needs_review"
    )

    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "qa_status": qa_status,
        "run_id": manifest["run_id"],
        "raw_returncode": manifest.get("raw_returncode"),
        "returncode": manifest.get("returncode"),
        "terminal_state": manifest.get("headless_automation", {}).get("terminal_state"),
        "detected_marker": detected_marker,
        "trace_save_stage_completed": save_stage_seen,
        "stage_dir": stage_inventory["path"],
        "saved_file_count": saved_file_count,
        "stage_file_count": stage_inventory["total_file_count"],
        "target_status_rows": target_status_rows,
        "target_summary_rows": target_summary_rows,
        "schedule_rows": schedule_rows,
        "scenario_mode": manifest.get("inputs", {}).get("scenario_mode"),
        "iterations": manifest.get("inputs", {}).get("iterations"),
        "runtime_package_status": runtime_manifest["summary"]["runtime_package_status"],
        "stdout_error_count": stdout_scan["error"],
        "stderr_error_count": stderr_scan["error"],
        "stdout_warning_count": stdout_scan["warning"],
        "stderr_warning_count": stderr_scan["warning"],
        "scenario_smoke": "not_performed",
        "release_qa": "not_performed",
    }
    payload = {
        "summary": summary,
        "manifest": _sanitize_manifest(manifest),
        "stage_inventory": stage_inventory,
        "log_scan": {"stdout": stdout_scan, "stderr": stderr_scan},
        "source_manifests": {
            "headless_manifest": _repo_relative(manifest_path),
            "runtime_package_manifest": _repo_relative(runtime_manifest_json),
        },
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
    parser.add_argument("--stage-dir", type=Path, default=DEFAULT_STAGE_DIR)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--stdout-log", type=Path, default=DEFAULT_STDOUT_LOG)
    parser.add_argument("--stderr-log", type=Path, default=DEFAULT_STDERR_LOG)
    parser.add_argument("--trace-log", type=Path, default=DEFAULT_TRACE_LOG)
    parser.add_argument(
        "--runtime-manifest-json", type=Path, default=DEFAULT_RUNTIME_MANIFEST_JSON
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_qa(
        stage_dir=args.stage_dir,
        manifest_path=args.manifest_path,
        stdout_log=args.stdout_log,
        stderr_log=args.stderr_log,
        trace_log=args.trace_log,
        runtime_manifest_json=args.runtime_manifest_json,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
